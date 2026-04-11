import Foundation
import AppKit
import Combine
import Darwin

struct AutoRefreshPlatformStatus {
    var headline: String = ""
    var cadence: String = ""
    var detail: String = ""
    var queuedCount: Int = 0
    var lastSuccessAt: Date?
    var isWatching: Bool = false
    var isEnabled: Bool = true
}

private final class SlackPendingBucket {
    let key: String
    let teamId: String?
    var workspaceHint: String?
    var channels: Set<String> = []
    var threadsByChannel: [String: Set<String>] = [:]
    var needsReconcile = false
    var needsDiscovery = false
    var timer: Timer?
    var lastReason = "event"

    init(key: String, teamId: String?, workspaceHint: String?) {
        self.key = key
        self.teamId = teamId
        self.workspaceHint = workspaceHint
    }

    var queuedCount: Int {
        let threadCount = threadsByChannel.values.reduce(0) { $0 + $1.count }
        return channels.count + threadCount + (needsReconcile ? 1 : 0) + (needsDiscovery ? 1 : 0)
    }
}

private final class SlackLogWatch {
    let path: String
    let fd: Int32
    let source: DispatchSourceFileSystemObject
    var offset: UInt64
    var partialLine = ""
    let parser = SlackLogParser()

    init?(path: String, queue: DispatchQueue) {
        let fd = open(path, O_EVTONLY)
        guard fd >= 0 else { return nil }
        self.path = path
        self.fd = fd
        self.offset = SlackLogWatch.currentFileSize(path)
        self.source = DispatchSource.makeFileSystemObjectSource(
            fileDescriptor: fd,
            eventMask: [.write, .extend, .attrib, .rename, .delete, .revoke],
            queue: queue
        )
    }

    func cancel() {
        source.cancel()
    }

    static func currentFileSize(_ path: String) -> UInt64 {
        let attrs = try? FileManager.default.attributesOfItem(atPath: path)
        return attrs?[.size] as? UInt64 ?? 0
    }
}

final class ChatAutoRefreshCoordinator: ObservableObject {
    @Published var slackEnabled: Bool {
        didSet { handleToggleChange(platform: .slack, enabled: slackEnabled) }
    }
    @Published var teamsEnabled: Bool {
        didSet { handleToggleChange(platform: .teams, enabled: teamsEnabled) }
    }
    @Published var slackStatus = AutoRefreshPlatformStatus(
        headline: "Watching Slack logs",
        cadence: "10s event • 15m reconcile • 60m discovery",
        detail: "Waiting for new message activity"
    )
    @Published var teamsStatus = AutoRefreshPlatformStatus(
        headline: "Polling Teams",
        cadence: "3m fast poll • 60m manifest refresh",
        detail: "Waiting for the first manifest refresh"
    )

    private let syncRunner: ChatSyncRunner
    private let slackQueue = DispatchQueue(label: "brain.chat.slack-logs")
    private var heartbeatTimer: Timer?
    private var slackDirFD: Int32 = -1
    private var slackDirSource: DispatchSourceFileSystemObject?
    private var slackLogWatches: [String: SlackLogWatch] = [:]
    private var slackBuckets: [String: SlackPendingBucket] = [:]
    private var slackWorkspaceMap: [String: String] = [:]
    private var lastSlackReconcileRequestAt: Date?
    private var lastSlackDiscoveryRequestAt: Date?
    private var lastSlackSuccessAt: Date?
    private var lastTeamsFastSyncRequestAt: Date?
    private var lastTeamsDiscoveryRequestAt: Date?
    private var lastTeamsSuccessAt: Date?
    private var lastTeamsStorageMutation: Date?
    private var pendingTeamsFastSync = false
    private var pendingTeamsDiscovery = false
    private var pendingTeamsFollowUpFastSync = false
    private var pendingTeamsReason = "timer"
    private var cancellables = Set<AnyCancellable>()
    private let defaults = UserDefaults.standard
    private let slackToggleKey = "brain.autoRefresh.slackEnabled"
    private let teamsToggleKey = "brain.autoRefresh.teamsEnabled"
    private let slackLastSuccessKey = "brain.autoRefresh.slackLastSuccessAt"
    private let teamsLastSuccessKey = "brain.autoRefresh.teamsLastSuccessAt"

    init(syncRunner: ChatSyncRunner) {
        self.syncRunner = syncRunner
        self.slackEnabled = defaults.object(forKey: slackToggleKey) as? Bool ?? true
        self.teamsEnabled = defaults.object(forKey: teamsToggleKey) as? Bool ?? true
        self.lastSlackSuccessAt = defaults.object(forKey: slackLastSuccessKey) as? Date
        self.lastTeamsSuccessAt = defaults.object(forKey: teamsLastSuccessKey) as? Date
        syncRunner.objectWillChange
            .receive(on: DispatchQueue.main)
            .sink { [weak self] _ in
                self?.publishStatuses()
            }
            .store(in: &cancellables)
    }

    func start() {
        refreshSlackWorkspaceMap()
        installSlackDirectoryWatch()
        rescanSlackLogFiles()
        lastTeamsStorageMutation = latestTeamsStorageMutation()
        baselineAutoRefreshSchedule(reason: "launch")
        heartbeatTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            self?.heartbeat()
        }
        publishStatuses()
    }

    func stop() {
        heartbeatTimer?.invalidate()
        heartbeatTimer = nil

        slackDirSource?.cancel()
        slackDirSource = nil
        slackDirFD = -1

        for watch in slackLogWatches.values {
            watch.cancel()
        }
        slackLogWatches.removeAll()

        for bucket in slackBuckets.values {
            bucket.timer?.invalidate()
        }
        slackBuckets.removeAll()
        publishStatuses()
    }

    private func heartbeat() {
        refreshSlackWorkspaceMap()
        rescanSlackLogFiles()

        let now = Date()
        if slackEnabled && isSlackRunning() {
            if shouldRequest(now, lastRequestAt: lastSlackReconcileRequestAt, interval: 15 * 60) {
                lastSlackReconcileRequestAt = now
                enqueueSlackReconcileAll(reason: "reconcile")
            }
            if shouldRequest(now, lastRequestAt: lastSlackDiscoveryRequestAt, interval: 60 * 60) {
                lastSlackDiscoveryRequestAt = now
                enqueueSlackDiscoveryAll(reason: "discovery")
            }
        }

        if teamsEnabled
            && (isTeamsContextRunning() || !teamsManifestExists())
            && shouldRequest(now, lastRequestAt: lastTeamsDiscoveryRequestAt, interval: 60 * 60) {
            lastTeamsDiscoveryRequestAt = now
            queueTeamsDiscovery(reason: "manifest-refresh", followWithFastSync: true)
        }

        if teamsEnabled
            && isTeamsContextRunning()
            && shouldRequest(now, lastRequestAt: lastTeamsFastSyncRequestAt, interval: 3 * 60) {
            lastTeamsFastSyncRequestAt = now
            queueTeamsFastSync(reason: "interval")
        }

        if teamsEnabled,
           let latestMutation = latestTeamsStorageMutation(),
           latestMutation > (lastTeamsStorageMutation ?? .distantPast) {
            lastTeamsStorageMutation = latestMutation
            if isTeamsContextRunning(),
               shouldRequest(now, lastRequestAt: lastTeamsFastSyncRequestAt, interval: 30) {
                lastTeamsFastSyncRequestAt = now
                queueTeamsFastSync(reason: "storage-change")
            }
        }

        publishStatuses()
    }

    private func shouldRequest(_ now: Date, lastRequestAt: Date?, interval: TimeInterval) -> Bool {
        guard let lastRequestAt else { return true }
        return now.timeIntervalSince(lastRequestAt) >= interval
    }

    // MARK: - Slack directory and file watches

    private func installSlackDirectoryWatch() {
        guard slackDirSource == nil else { return }
        let fd = open(kSlackLogDir, O_EVTONLY)
        guard fd >= 0 else { return }
        slackDirFD = fd
        let source = DispatchSource.makeFileSystemObjectSource(
            fileDescriptor: fd,
            eventMask: [.write, .rename, .delete, .attrib],
            queue: slackQueue
        )
        source.setEventHandler { [weak self] in
            DispatchQueue.main.async {
                self?.rescanSlackLogFiles()
            }
        }
        source.setCancelHandler { [fd] in
            close(fd)
        }
        source.resume()
        slackDirSource = source
    }

    private func rescanSlackLogFiles() {
        let dirURL = URL(fileURLWithPath: kSlackLogDir)
        guard let files = try? FileManager.default.contentsOfDirectory(at: dirURL, includingPropertiesForKeys: nil) else {
            publishStatuses()
            return
        }
        let matchingPaths = Set(files
            .filter { $0.lastPathComponent.hasPrefix("webapp-console") && $0.lastPathComponent.hasSuffix(".log") }
            .map(\.path))

        for (path, watch) in slackLogWatches where !matchingPaths.contains(path) {
            watch.cancel()
            slackLogWatches.removeValue(forKey: path)
        }

        for path in matchingPaths where slackLogWatches[path] == nil {
            guard let watch = SlackLogWatch(path: path, queue: slackQueue) else { continue }
            watch.source.setEventHandler { [weak self, weak watch] in
                guard let self, let watch else { return }
                let events = watch.source.data
                if events.contains(.delete) || events.contains(.rename) || events.contains(.revoke) {
                    DispatchQueue.main.async {
                        self.rescanSlackLogFiles()
                    }
                    return
                }
                self.readSlackUpdates(from: watch)
            }
            watch.source.setCancelHandler { [fd = watch.fd] in
                close(fd)
            }
            watch.source.resume()
            slackLogWatches[path] = watch
        }

        publishStatuses()
    }

    private func readSlackUpdates(from watch: SlackLogWatch) {
        let currentSize = SlackLogWatch.currentFileSize(watch.path)
        if currentSize < watch.offset {
            watch.offset = 0
            watch.partialLine = ""
        }
        guard let handle = FileHandle(forReadingAtPath: watch.path) else { return }
        defer { try? handle.close() }
        do {
            try handle.seek(toOffset: watch.offset)
            let data = try handle.readToEnd() ?? Data()
            watch.offset = currentSize
            guard !data.isEmpty, let text = String(data: data, encoding: .utf8) else { return }
            watch.partialLine += text
            let segments = watch.partialLine.components(separatedBy: "\n")
            watch.partialLine = segments.last ?? ""
            for line in segments.dropLast() {
                processSlackLogLine(line, watch: watch)
            }
        } catch {
            log("Slack auto-refresh: failed reading \(watch.path): \(error)")
        }
    }

    private func processSlackLogLine(_ rawLine: String, watch: SlackLogWatch) {
        for event in watch.parser.feed(line: rawLine) {
            DispatchQueue.main.async {
                self.enqueueSlackHint(teamId: event.teamId, channel: event.channel, threadTS: event.threadTS, reason: event.source)
            }
        }
    }

    // MARK: - Slack scheduling

    private func enqueueSlackHint(teamId: String?, channel: String?, threadTS: String?, reason: String) {
        guard slackEnabled else { return }
        let workspaceHint = teamId.flatMap { slackWorkspaceMap[$0] }
        let key = slackBucketKey(teamId: teamId, workspaceHint: workspaceHint)
        let bucket = slackBuckets[key] ?? SlackPendingBucket(key: key, teamId: teamId, workspaceHint: workspaceHint)
        bucket.workspaceHint = bucket.workspaceHint ?? workspaceHint
        bucket.lastReason = reason
        if let channel {
            bucket.channels.insert(channel)
            if let threadTS {
                bucket.threadsByChannel[channel, default: []].insert(threadTS)
            }
        } else {
            bucket.needsReconcile = true
        }
        slackBuckets[key] = bucket
        scheduleSlackBucket(bucket, after: 10)
        publishStatuses()
    }

    private func enqueueSlackReconcileAll(reason: String) {
        guard slackEnabled else { return }
        let workspaces = knownSlackWorkspaceHints()
        if workspaces.isEmpty {
            let bucket = slackBuckets["__all__"] ?? SlackPendingBucket(key: "__all__", teamId: nil, workspaceHint: nil)
            bucket.needsReconcile = true
            bucket.lastReason = reason
            slackBuckets[bucket.key] = bucket
            scheduleSlackBucket(bucket, after: 1)
            publishStatuses()
            return
        }

        for workspace in workspaces {
            let key = slackBucketKey(teamId: nil, workspaceHint: workspace)
            let bucket = slackBuckets[key] ?? SlackPendingBucket(key: key, teamId: nil, workspaceHint: workspace)
            bucket.workspaceHint = workspace
            bucket.needsReconcile = true
            bucket.lastReason = reason
            slackBuckets[key] = bucket
            scheduleSlackBucket(bucket, after: 1)
        }
        publishStatuses()
    }

    private func enqueueSlackDiscoveryAll(reason: String) {
        guard slackEnabled else { return }
        let workspaces = knownSlackWorkspaceHints()
        if workspaces.isEmpty {
            let bucket = slackBuckets["__all__"] ?? SlackPendingBucket(key: "__all__", teamId: nil, workspaceHint: nil)
            bucket.needsDiscovery = true
            bucket.lastReason = reason
            slackBuckets[bucket.key] = bucket
            scheduleSlackBucket(bucket, after: 1)
            publishStatuses()
            return
        }

        for workspace in workspaces {
            let key = slackBucketKey(teamId: nil, workspaceHint: workspace)
            let bucket = slackBuckets[key] ?? SlackPendingBucket(key: key, teamId: nil, workspaceHint: workspace)
            bucket.workspaceHint = workspace
            bucket.needsDiscovery = true
            bucket.lastReason = reason
            slackBuckets[key] = bucket
            scheduleSlackBucket(bucket, after: 1)
        }
        publishStatuses()
    }

    private func scheduleSlackBucket(_ bucket: SlackPendingBucket, after delay: TimeInterval) {
        guard slackEnabled else { return }
        bucket.timer?.invalidate()
        bucket.timer = Timer.scheduledTimer(withTimeInterval: delay, repeats: false) { [weak self, weak bucket] _ in
            guard let self, let bucket else { return }
            self.executeSlackBucket(bucket.key)
        }
    }

    private func executeSlackBucket(_ key: String) {
        guard let bucket = slackBuckets[key] else { return }
        guard slackEnabled else {
            bucket.timer?.invalidate()
            slackBuckets.removeValue(forKey: key)
            publishStatuses()
            return
        }
        if syncRunner.isRunning(.slack) {
            scheduleSlackBucket(bucket, after: 5)
            return
        }
        bucket.timer?.invalidate()
        slackBuckets.removeValue(forKey: key)

        var arguments: [String] = []
        if let workspace = bucket.workspaceHint {
            arguments += ["--workspace", workspace]
        }

        if bucket.needsDiscovery {
            arguments += []
        } else {
            arguments += ["--skip-discovery", "--skip-users"]
            let channels = Array(bucket.channels).sorted()
            if !channels.isEmpty {
                arguments += ["--channels", channels.joined(separator: ",")]
            }
            let threadSpecs = bucket.threadsByChannel
                .flatMap { channel, threadSet in threadSet.map { "\(channel):\($0)" } }
                .sorted()
            if !threadSpecs.isEmpty {
                arguments += ["--thread", threadSpecs.joined(separator: ",")]
            }
        }

        let reason = "auto-\(bucket.lastReason)"
        let launched = syncRunner.runSlackExport(arguments: arguments, reason: reason) { [weak self] result in
            self?.handleSlackCompletion(result, discoveryRequested: bucket.needsDiscovery)
        }
        if !launched {
            slackBuckets[key] = bucket
            scheduleSlackBucket(bucket, after: 5)
        }
        publishStatuses()
    }

    private func handleSlackCompletion(_ result: ExportResult, discoveryRequested: Bool) {
        if result.succeeded {
            lastSlackSuccessAt = result.finishedAt
            defaults.set(result.finishedAt, forKey: slackLastSuccessKey)
            if discoveryRequested {
                refreshSlackWorkspaceMap()
            }
        }
        publishStatuses()
    }

    private func slackBucketKey(teamId: String?, workspaceHint: String?) -> String {
        if let workspaceHint {
            return "workspace:\(workspaceHint)"
        }
        if let teamId {
            return "team:\(teamId)"
        }
        return "__all__"
    }

    private func knownSlackWorkspaceHints() -> [String] {
        var workspaces = Set(slackWorkspaceMap.values)
        let root = URL(fileURLWithPath: kSlackDataDir)
        if let children = try? FileManager.default.contentsOfDirectory(at: root, includingPropertiesForKeys: nil) {
            for child in children where child.hasDirectoryPath {
                workspaces.insert(child.lastPathComponent)
            }
        }
        return Array(workspaces).sorted()
    }

    private func refreshSlackWorkspaceMap() {
        let root = URL(fileURLWithPath: kSlackDataDir)
        guard let children = try? FileManager.default.contentsOfDirectory(at: root, includingPropertiesForKeys: nil) else { return }
        var map: [String: String] = [:]
        for child in children where child.hasDirectoryPath {
            let metaURL = child.appendingPathComponent("workspace.json")
            guard let data = try? Data(contentsOf: metaURL),
                  let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                  let teamID = json["team_id"] as? String else { continue }
            map[teamID] = child.lastPathComponent
        }
        slackWorkspaceMap = map
    }

    // MARK: - Teams scheduling

    private func queueTeamsDiscovery(reason: String, followWithFastSync: Bool) {
        guard teamsEnabled else { return }
        pendingTeamsReason = reason
        if syncRunner.isRunning(.teams) {
            pendingTeamsDiscovery = true
            pendingTeamsFollowUpFastSync = pendingTeamsFollowUpFastSync || followWithFastSync
            publishStatuses()
            return
        }
        let launched = syncRunner.runTeamsExport(arguments: ["--discover-only"], reason: "auto-\(reason)") { [weak self] result in
            self?.handleTeamsCompletion(result, wasDiscovery: true, followWithFastSync: followWithFastSync)
        }
        if !launched {
            pendingTeamsDiscovery = true
            pendingTeamsFollowUpFastSync = pendingTeamsFollowUpFastSync || followWithFastSync
        }
        publishStatuses()
    }

    private func queueTeamsFastSync(reason: String) {
        guard teamsEnabled else { return }
        pendingTeamsReason = reason
        if syncRunner.isRunning(.teams) {
            pendingTeamsFastSync = true
            publishStatuses()
            return
        }
        let launched = syncRunner.runTeamsExport(arguments: ["--sync-known"], reason: "auto-\(reason)") { [weak self] result in
            self?.handleTeamsCompletion(result, wasDiscovery: false, followWithFastSync: false)
        }
        if !launched {
            pendingTeamsFastSync = true
        }
        publishStatuses()
    }

    private func handleTeamsCompletion(_ result: ExportResult, wasDiscovery: Bool, followWithFastSync: Bool) {
        if result.succeeded {
            lastTeamsSuccessAt = result.finishedAt
            defaults.set(result.finishedAt, forKey: teamsLastSuccessKey)
            if !wasDiscovery {
                lastTeamsFastSyncRequestAt = result.finishedAt
            }
        }

        if !teamsEnabled {
            pendingTeamsDiscovery = false
            pendingTeamsFastSync = false
            pendingTeamsFollowUpFastSync = false
            publishStatuses()
            return
        }

        if wasDiscovery && result.succeeded && followWithFastSync {
            queueTeamsFastSync(reason: "post-discovery")
            return
        }

        if pendingTeamsDiscovery {
            pendingTeamsDiscovery = false
            let follow = pendingTeamsFollowUpFastSync
            pendingTeamsFollowUpFastSync = false
            queueTeamsDiscovery(reason: pendingTeamsReason, followWithFastSync: follow)
            return
        }

        if pendingTeamsFastSync {
            pendingTeamsFastSync = false
            queueTeamsFastSync(reason: pendingTeamsReason)
            return
        }

        publishStatuses()
    }

    private func latestTeamsStorageMutation() -> Date? {
        var latest: Date?
        for dir in kTeamsStorageDirs {
            let url = URL(fileURLWithPath: dir)
            guard let files = try? FileManager.default.contentsOfDirectory(at: url, includingPropertiesForKeys: [.contentModificationDateKey]) else {
                continue
            }
            for file in files {
                guard let values = try? file.resourceValues(forKeys: [.contentModificationDateKey]),
                      let mod = values.contentModificationDate else { continue }
                if latest == nil || mod > latest! {
                    latest = mod
                }
            }
        }
        return latest
    }

    private func teamsManifestExists() -> Bool {
        let path = URL(fileURLWithPath: kTeamsDataDir)
            .appendingPathComponent("sierra")
            .appendingPathComponent("manifest.json")
            .path
        return FileManager.default.fileExists(atPath: path)
    }

    private func isSlackRunning() -> Bool {
        NSWorkspace.shared.runningApplications.contains { app in
            guard let bundleID = app.bundleIdentifier else { return false }
            return bundleID == "com.tinyspeck.slackmacgap"
        }
    }

    private func isTeamsContextRunning() -> Bool {
        NSWorkspace.shared.runningApplications.contains { app in
            guard let bundleID = app.bundleIdentifier else { return false }
            return bundleID == "com.microsoft.teams"
                || bundleID == "com.microsoft.teams2"
                || bundleID == kBraveBundleID
        }
    }

    // MARK: - Status publishing

    private func handleToggleChange(platform: ChatPlatform, enabled: Bool) {
        let key = platform == .slack ? slackToggleKey : teamsToggleKey
        defaults.set(enabled, forKey: key)
        switch platform {
        case .slack:
            if !enabled {
                clearSlackPending()
            }
        case .teams:
            if !enabled {
                pendingTeamsFastSync = false
                pendingTeamsDiscovery = false
                pendingTeamsFollowUpFastSync = false
            } else {
                lastTeamsStorageMutation = latestTeamsStorageMutation()
            }
        }
        if enabled {
            baselineAutoRefreshSchedule(reason: "\(platform.rawValue.lowercased()) enabled")
            publishStatuses()
        } else {
            publishStatuses()
        }
    }

    private func clearSlackPending() {
        for bucket in slackBuckets.values {
            bucket.timer?.invalidate()
        }
        slackBuckets.removeAll()
    }

    private func baselineAutoRefreshSchedule(reason: String) {
        let now = Date()
        lastSlackReconcileRequestAt = now
        lastSlackDiscoveryRequestAt = now
        lastTeamsFastSyncRequestAt = now
        lastTeamsDiscoveryRequestAt = now
        log("Chat auto-refresh: baselined periodic timers on \(reason); no boot-time full sync")
    }

    private func publishStatuses() {
        let slackQueued = slackBuckets.values.reduce(0) { $0 + $1.queuedCount }
        var slackHeadline = ""
        if slackEnabled && syncRunner.slackRunning {
            slackHeadline = "Syncing"
        } else if slackEnabled && slackQueued > 0 {
            slackHeadline = "Queued"
        } else if !slackEnabled {
            slackHeadline = "Off"
        }
        slackStatus = AutoRefreshPlatformStatus(
            headline: slackHeadline,
            cadence: "10s event • 15m reconcile • 60m discovery",
            detail: slackDetailText(queued: slackQueued),
            queuedCount: slackQueued,
            lastSuccessAt: lastSlackSuccessAt,
            isWatching: slackEnabled && !slackLogWatches.isEmpty,
            isEnabled: slackEnabled
        )

        let teamsQueued = (pendingTeamsDiscovery ? 1 : 0) + (pendingTeamsFastSync ? 1 : 0)
        var teamsHeadline = ""
        if teamsEnabled && syncRunner.teamsRunning {
            teamsHeadline = "Syncing"
        } else if teamsEnabled && teamsQueued > 0 {
            teamsHeadline = "Queued"
        } else if !teamsEnabled {
            teamsHeadline = "Off"
        }
        teamsStatus = AutoRefreshPlatformStatus(
            headline: teamsHeadline,
            cadence: "3m fast poll • 60m manifest refresh",
            detail: teamsDetailText(queued: teamsQueued),
            queuedCount: teamsQueued,
            lastSuccessAt: lastTeamsSuccessAt,
            isWatching: teamsEnabled,
            isEnabled: teamsEnabled
        )
    }

    private func slackDetailText(queued: Int) -> String {
        guard slackEnabled else { return "Auto-refresh disabled" }
        var parts: [String] = []
        if slackLogWatches.count > 0 {
            parts.append("\(slackLogWatches.count) log file(s)")
        }
        if let lastSlackSuccessAt {
            parts.append("Last success \(relativeTimeString(from: lastSlackSuccessAt))")
        }
        return parts.isEmpty ? "Waiting for Slack activity" : parts.joined(separator: " • ")
    }

    private func teamsDetailText(queued: Int) -> String {
        guard teamsEnabled else { return "Auto-refresh disabled" }
        var parts: [String] = []
        if let lastTeamsStorageMutation {
            parts.append("Browser activity \(relativeTimeString(from: lastTeamsStorageMutation))")
        }
        if let lastTeamsSuccessAt {
            parts.append("Last success \(relativeTimeString(from: lastTeamsSuccessAt))")
        }
        return parts.isEmpty ? "Waiting for Teams activity" : parts.joined(separator: " • ")
    }

    private func relativeTimeString(from date: Date) -> String {
        let delta = max(0, Int(Date().timeIntervalSince(date)))
        if delta < 60 { return "\(delta)s ago" }
        if delta < 3600 { return "\(delta / 60)m ago" }
        return "\(delta / 3600)h ago"
    }
}
