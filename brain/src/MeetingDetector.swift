import Foundation
import CoreMediaIO
import CoreAudio
import AppKit
import ApplicationServices

class MeetingDetector: ObservableObject {
    @Published var detectedApp: String?
    @Published var detectedMatch: MeetingMatch?

    private struct RecentActivation {
        let bundleID: String
        let appName: String
        let at: Date
    }

    private struct ProbeCandidate {
        let app: NSRunningApplication
        let appName: String
        let kind: MeetingProbeKind
    }

    private var cameraListenerBlocks: [(CMIOObjectID, CMIOObjectPropertyListenerBlock)] = []
    private var micListenerBlock: AudioObjectPropertyListenerBlock?
    private var defaultInputListenerBlock: AudioObjectPropertyListenerBlock?
    private var activationObserver: NSObjectProtocol?
    private var micDeviceID: AudioObjectID = kAudioObjectUnknown
    private var lastNotificationTime: Date = .distantPast
    private var monitoring = false
    private var micSettleTimer: Timer?
    private var recentActivation: RecentActivation?
    private var transitionTracker = MeetingSignalTransitionTracker()
    private var suppressionState = MeetingSuppressionState()

    var onMeetingDetected: ((MeetingMatch) -> Void)?
    var isSuppressed: (() -> Bool)?

    func startMonitoring() {
        guard !monitoring else { return }
        monitoring = true
        log("MeetingDetector: starting monitoring")
        installCameraListeners()
        installMicListener()
        installDefaultInputListener()
        installActivationObserver()
        let camera = isCameraOn()
        let mic = isMicOn()
        transitionTracker = MeetingSignalTransitionTracker(lastMicActive: mic, lastCameraActive: camera)
        log("MeetingDetector: camera=\(camera) mic=\(mic)")
    }

    func stopMonitoring() {
        guard monitoring else { return }
        monitoring = false
        micSettleTimer?.invalidate()
        micSettleTimer = nil
        removeCameraListeners()
        removeMicListener()
        removeDefaultInputListener()
        removeActivationObserver()
        log("MeetingDetector: stopped")
    }

    func suppress(for duration: TimeInterval, reason: String) {
        guard duration > 0 else { return }
        suppressionState.suppress(for: duration, reason: reason)
        log("MeetingDetector: suppressed for \(Int(duration.rounded()))s (\(reason))")
    }

    // MARK: - Camera monitoring via CoreMediaIO

    private func installCameraListeners() {
        CMIOObjectPropertyAddress.allCameraDeviceIDs().forEach { deviceID in
            var address = CMIOObjectPropertyAddress(
                mSelector: CMIOObjectPropertySelector(kCMIODevicePropertyDeviceIsRunningSomewhere),
                mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeGlobal),
                mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementMain)
            )
            let block: CMIOObjectPropertyListenerBlock = { [weak self] _, _ in
                DispatchQueue.main.async { self?.handleCameraChange() }
            }
            let status = CMIOObjectAddPropertyListenerBlock(deviceID, &address, DispatchQueue.main, block)
            if status == noErr {
                cameraListenerBlocks.append((deviceID, block))
            }
        }
        log("MeetingDetector: installed camera listeners on \(cameraListenerBlocks.count) device(s)")
    }

    private func removeCameraListeners() {
        for (deviceID, block) in cameraListenerBlocks {
            var address = CMIOObjectPropertyAddress(
                mSelector: CMIOObjectPropertySelector(kCMIODevicePropertyDeviceIsRunningSomewhere),
                mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeGlobal),
                mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementMain)
            )
            CMIOObjectRemovePropertyListenerBlock(deviceID, &address, DispatchQueue.main, block)
        }
        cameraListenerBlocks.removeAll()
    }

    private func handleCameraChange() {
        let on = isCameraOn()
        guard transitionTracker.consumeCameraState(on) else { return }
        log("MeetingDetector: camera state changed → \(on ? "on" : "off")")
        guard on else { return }
        evaluateMeetingSignal(trigger: "camera")
    }

    private func isCameraOn() -> Bool {
        for deviceID in CMIOObjectPropertyAddress.allCameraDeviceIDs() {
            var address = CMIOObjectPropertyAddress(
                mSelector: CMIOObjectPropertySelector(kCMIODevicePropertyDeviceIsRunningSomewhere),
                mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeGlobal),
                mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementMain)
            )
            var isRunning: UInt32 = 0
            let size = UInt32(MemoryLayout<UInt32>.size)
            var dataUsed: UInt32 = 0
            let status = CMIOObjectGetPropertyData(deviceID, &address, 0, nil, size, &dataUsed, &isRunning)
            if status == noErr && isRunning != 0 { return true }
        }
        return false
    }

    // MARK: - Microphone monitoring via CoreAudio

    private func installMicListener() {
        var defaultInput = AudioObjectID(kAudioObjectUnknown)
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioHardwarePropertyDefaultInputDevice,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        var size = UInt32(MemoryLayout<AudioObjectID>.size)
        guard AudioObjectGetPropertyData(
            AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size, &defaultInput
        ) == noErr, defaultInput != kAudioObjectUnknown else {
            log("MeetingDetector: could not find default input device")
            return
        }
        micDeviceID = defaultInput
        let name = audioDeviceName(defaultInput) ?? "unknown"

        var runningAddress = AudioObjectPropertyAddress(
            mSelector: kAudioDevicePropertyDeviceIsRunningSomewhere,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        let block: AudioObjectPropertyListenerBlock = { [weak self] _, _ in
            DispatchQueue.main.async { self?.handleMicChange() }
        }
        micListenerBlock = block
        AudioObjectAddPropertyListenerBlock(micDeviceID, &runningAddress, DispatchQueue.main, block)
        log("MeetingDetector: installed mic listener on device \(micDeviceID) (\(name))")
    }

    private func removeMicListener() {
        guard let block = micListenerBlock, micDeviceID != kAudioObjectUnknown else { return }
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioDevicePropertyDeviceIsRunningSomewhere,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        AudioObjectRemovePropertyListenerBlock(micDeviceID, &address, DispatchQueue.main, block)
        micListenerBlock = nil
    }

    // MARK: - Default input device change tracking

    private func installDefaultInputListener() {
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioHardwarePropertyDefaultInputDevice,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        let block: AudioObjectPropertyListenerBlock = { [weak self] _, _ in
            DispatchQueue.main.async { self?.handleDefaultInputChanged() }
        }
        defaultInputListenerBlock = block
        AudioObjectAddPropertyListenerBlock(
            AudioObjectID(kAudioObjectSystemObject), &address, DispatchQueue.main, block
        )
        log("MeetingDetector: watching for default input device changes")
    }

    private func removeDefaultInputListener() {
        guard let block = defaultInputListenerBlock else { return }
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioHardwarePropertyDefaultInputDevice,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        AudioObjectRemovePropertyListenerBlock(
            AudioObjectID(kAudioObjectSystemObject), &address, DispatchQueue.main, block
        )
        defaultInputListenerBlock = nil
    }

    private func handleDefaultInputChanged() {
        var newDevice = AudioObjectID(kAudioObjectUnknown)
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioHardwarePropertyDefaultInputDevice,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        var size = UInt32(MemoryLayout<AudioObjectID>.size)
        guard AudioObjectGetPropertyData(
            AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size, &newDevice
        ) == noErr, newDevice != kAudioObjectUnknown else {
            log("MeetingDetector: default input changed but could not resolve new device")
            return
        }

        guard newDevice != micDeviceID else { return }

        let name = audioDeviceName(newDevice) ?? "unknown"
        log("MeetingDetector: default input changed → device \(newDevice) (\(name))")
        removeMicListener()
        installMicListener()
        transitionTracker = MeetingSignalTransitionTracker(
            lastMicActive: isMicOn(),
            lastCameraActive: transitionTracker.lastCameraActive
        )
    }

    private func audioDeviceName(_ deviceID: AudioObjectID) -> String? {
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioObjectPropertyName,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        var size = UInt32(MemoryLayout<CFString?>.size)
        let storage = UnsafeMutableRawPointer.allocate(
            byteCount: Int(size),
            alignment: MemoryLayout<CFString?>.alignment
        )
        defer { storage.deallocate() }
        storage.initializeMemory(as: CFString?.self, repeating: nil, count: 1)
        defer { storage.assumingMemoryBound(to: CFString?.self).deinitialize(count: 1) }

        guard AudioObjectGetPropertyData(deviceID, &address, 0, nil, &size, storage) == noErr else { return nil }
        return storage.load(as: CFString?.self) as String?
    }

    private func handleMicChange() {
        let on = isMicOn()
        guard transitionTracker.consumeMicState(on) else { return }
        log("MeetingDetector: mic state changed → \(on ? "on" : "off")")

        if !on {
            if micSettleTimer != nil {
                micSettleTimer?.invalidate()
                micSettleTimer = nil
                log("MeetingDetector: mic turned off before settle delay — ignoring transient")
            }
            return
        }

        guard micSettleTimer == nil else { return }
        log("MeetingDetector: mic on — waiting \(Int(kMicSettleDelaySec))s to confirm sustained")
        micSettleTimer = Timer.scheduledTimer(withTimeInterval: kMicSettleDelaySec, repeats: false) { [weak self] _ in
            guard let self = self else { return }
            self.micSettleTimer = nil
            guard self.isMicOn() else {
                log("MeetingDetector: mic no longer on after settle delay — skipping")
                return
            }
            log("MeetingDetector: mic sustained for \(Int(kMicSettleDelaySec))s — evaluating")
            self.evaluateMeetingSignal(trigger: "mic")
        }
    }

    private func isMicOn() -> Bool {
        guard micDeviceID != kAudioObjectUnknown else { return false }
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioDevicePropertyDeviceIsRunningSomewhere,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        var isRunning: UInt32 = 0
        var size = UInt32(MemoryLayout<UInt32>.size)
        return AudioObjectGetPropertyData(micDeviceID, &address, 0, nil, &size, &isRunning) == noErr
            && isRunning != 0
    }

    // MARK: - Activation tracking

    private func installActivationObserver() {
        activationObserver = NSWorkspace.shared.notificationCenter.addObserver(
            forName: NSWorkspace.didActivateApplicationNotification,
            object: nil,
            queue: .main
        ) { [weak self] note in
            self?.handleApplicationActivated(note)
        }
        log("MeetingDetector: watching app activations")
    }

    private func removeActivationObserver() {
        guard let observer = activationObserver else { return }
        NSWorkspace.shared.notificationCenter.removeObserver(observer)
        activationObserver = nil
    }

    private func handleApplicationActivated(_ note: Notification) {
        guard let app = note.userInfo?[NSWorkspace.applicationUserInfoKey] as? NSRunningApplication,
              let bundleID = app.bundleIdentifier,
              kMeetingRelevantBundleIDs.contains(bundleID) else {
            return
        }
        let appName = normalizedAppName(for: app)
        recentActivation = RecentActivation(bundleID: bundleID, appName: appName, at: Date())
        log("MeetingDetector: recent activation → \(appName) (bundle: \(bundleID))")
    }

    // MARK: - Meeting app correlation

    private func evaluateMeetingSignal(trigger: String) {
        if let reason = currentSuppressionReason() {
            log("MeetingDetector: suppressed (\(reason))")
            return
        }

        let elapsed = Date().timeIntervalSince(lastNotificationTime)
        guard elapsed > kMeetingDebounceSec else {
            log("MeetingDetector: debounced (\(Int(elapsed))s since last, need \(Int(kMeetingDebounceSec))s)")
            return
        }

        let camera = isCameraOn()
        let mic = isMicOn()
        log("MeetingDetector: evaluating signal from \(trigger) — camera=\(camera) mic=\(mic)")

        if let match = detectMeetingMatch(camera: camera, mic: mic) {
            log("MeetingDetector: meeting detected → \(match.appName) [\(match.evidenceSummary)]")
            detectedApp = match.appName
            detectedMatch = match
            lastNotificationTime = Date()
            onMeetingDetected?(match)
        } else {
            log("MeetingDetector: no app-specific proof found")
        }
    }

    private func detectMeetingMatch(camera: Bool, mic: Bool) -> MeetingMatch? {
        let candidates = probeCandidates()
        guard !candidates.isEmpty else { return nil }

        for candidate in candidates {
            let recentActivationName = recentActivationWithinWindow()?.bundleID == candidate.app.bundleIdentifier
                ? candidate.appName
                : nil
            switch candidate.kind {
            case .googleMeet:
                guard let bundleID = candidate.app.bundleIdentifier else {
                    continue
                }
                guard isFrontmost(candidate.app) || recentActivationName != nil else { continue }
                let observation = MeetingProbeObservation(
                    appName: candidate.appName,
                    micActive: mic,
                    cameraActive: camera,
                    recentActivationAppName: recentActivationName,
                    frontTabURL: frontTabURL(for: bundleID),
                    focusedWindowTitle: nil
                )
                if let match = MeetingDetectionHeuristics.match(kind: .googleMeet, observation: observation) {
                    return match
                }

            case let .focusedWindowTitle(keywords, allowCameraFallback):
                guard isFrontmost(candidate.app) || recentActivationName != nil else { continue }
                guard let title = focusedWindowTitle(for: candidate.app) else { continue }
                let observation = MeetingProbeObservation(
                    appName: candidate.appName,
                    micActive: mic,
                    cameraActive: camera,
                    recentActivationAppName: recentActivationName,
                    frontTabURL: nil,
                    focusedWindowTitle: title
                )
                if let match = MeetingDetectionHeuristics.match(
                    kind: .focusedWindowTitle(keywords: keywords, allowCameraFallback: allowCameraFallback),
                    observation: observation
                ) {
                    return match
                }
            }
        }

        return nil
    }

    private func probeCandidates() -> [ProbeCandidate] {
        var candidates: [ProbeCandidate] = []
        var seenBundleIDs = Set<String>()

        if let frontmost = NSWorkspace.shared.frontmostApplication,
           let candidate = probeCandidate(for: frontmost),
           let bundleID = frontmost.bundleIdentifier {
            candidates.append(candidate)
            seenBundleIDs.insert(bundleID)
        }

        if let recent = recentActivationWithinWindow(),
           let app = runningApplication(bundleID: recent.bundleID),
           !seenBundleIDs.contains(recent.bundleID),
           let candidate = probeCandidate(for: app) {
            candidates.append(candidate)
        }

        if !candidates.isEmpty {
            let names = candidates.map(\.appName).joined(separator: ", ")
            log("MeetingDetector: probing candidates → \(names)")
        }

        return candidates
    }

    private func probeCandidate(for app: NSRunningApplication) -> ProbeCandidate? {
        guard let bundleID = app.bundleIdentifier else { return nil }

        if kMeetingBrowserBundleIDs.contains(bundleID) {
            return ProbeCandidate(app: app, appName: "Google Meet", kind: .googleMeet)
        }

        guard let appName = kMeetingAppBundleIDs[bundleID] else { return nil }
        switch appName {
        case "Slack":
            return ProbeCandidate(
                app: app,
                appName: appName,
                kind: .focusedWindowTitle(keywords: kMeetingSlackWindowKeywords, allowCameraFallback: false)
            )
        case "Teams":
            return ProbeCandidate(
                app: app,
                appName: appName,
                kind: .focusedWindowTitle(keywords: kMeetingTeamsWindowKeywords, allowCameraFallback: true)
            )
        default:
            return nil
        }
    }

    private func normalizedAppName(for app: NSRunningApplication) -> String {
        guard let bundleID = app.bundleIdentifier else {
            return app.localizedName ?? "unknown"
        }
        if let name = kMeetingAppBundleIDs[bundleID] {
            return name
        }
        if kMeetingBrowserBundleIDs.contains(bundleID) {
            return app.localizedName ?? bundleID
        }
        return app.localizedName ?? bundleID
    }

    private func recentActivationWithinWindow() -> RecentActivation? {
        guard let recentActivation else { return nil }
        guard Date().timeIntervalSince(recentActivation.at) <= kMeetingRecentActivationWindowSec else { return nil }
        return recentActivation
    }

    private func runningApplication(bundleID: String) -> NSRunningApplication? {
        NSWorkspace.shared.runningApplications.first(where: { $0.bundleIdentifier == bundleID })
    }

    private func isFrontmost(_ app: NSRunningApplication) -> Bool {
        NSWorkspace.shared.frontmostApplication?.processIdentifier == app.processIdentifier
    }

    private func currentSuppressionReason() -> String? {
        suppressionState.currentReason(externalSuppressed: isSuppressed?() == true)
    }

    private func frontTabURL(for bundleID: String) -> String? {
        guard let appName = kMeetingBrowserScriptNames[bundleID] else { return nil }

        let scriptSource: String
        switch bundleID {
        case "com.apple.Safari":
            scriptSource = """
                tell application "\(appName)"
                    if (count of windows) = 0 then return ""
                    return URL of current tab of front window
                end tell
            """
        default:
            scriptSource = """
                tell application "\(appName)"
                    if (count of windows) = 0 then return ""
                    return URL of active tab of front window
                end tell
            """
        }

        guard let script = NSAppleScript(source: scriptSource) else { return nil }
        var error: NSDictionary?
        let result = script.executeAndReturnError(&error)
        if let error {
            log("MeetingDetector: failed reading front tab URL from \(appName) — \(error)")
            return nil
        }
        let url = result.stringValue?.trimmingCharacters(in: .whitespacesAndNewlines)
        if let url, !url.isEmpty {
            log("MeetingDetector: front tab URL from \(appName) → \(url)")
        }
        return url?.isEmpty == false ? url : nil
    }

    private func focusedWindowTitle(for app: NSRunningApplication) -> String? {
        guard accessibilityTrusted() else {
            log("MeetingDetector: accessibility unavailable — skipping \(normalizedAppName(for: app)) probe")
            return nil
        }

        let appElement = AXUIElementCreateApplication(app.processIdentifier)
        if let focusedWindow = axElementValue(from: appElement, attribute: kAXFocusedWindowAttribute),
           let title = axStringValue(from: focusedWindow, attribute: kAXTitleAttribute) {
            log("MeetingDetector: focused window title for \(normalizedAppName(for: app)) → \(title)")
            return title
        }

        if let mainWindow = axElementValue(from: appElement, attribute: kAXMainWindowAttribute),
           let title = axStringValue(from: mainWindow, attribute: kAXTitleAttribute) {
            log("MeetingDetector: main window title for \(normalizedAppName(for: app)) → \(title)")
            return title
        }

        log("MeetingDetector: no AX window title for \(normalizedAppName(for: app))")
        return nil
    }

    private func accessibilityTrusted() -> Bool {
        let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: false] as CFDictionary
        return AXIsProcessTrustedWithOptions(options)
    }

    private func axElementValue(from element: AXUIElement, attribute: String) -> AXUIElement? {
        var value: CFTypeRef?
        guard AXUIElementCopyAttributeValue(element, attribute as CFString, &value) == .success else { return nil }
        return (value as! AXUIElement)
    }

    private func axStringValue(from element: AXUIElement, attribute: String) -> String? {
        var value: CFTypeRef?
        guard AXUIElementCopyAttributeValue(element, attribute as CFString, &value) == .success else { return nil }
        return value as? String
    }

    func resetDebounce() {
        lastNotificationTime = .distantPast
    }
}

// MARK: - CoreMediaIO helpers

extension CMIOObjectPropertyAddress {
    static func allCameraDeviceIDs() -> [CMIOObjectID] {
        var address = CMIOObjectPropertyAddress(
            mSelector: CMIOObjectPropertySelector(kCMIOHardwarePropertyDevices),
            mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeGlobal),
            mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementMain)
        )
        var size: UInt32 = 0
        guard CMIOObjectGetPropertyDataSize(
            CMIOObjectID(kCMIOObjectSystemObject), &address, 0, nil, &size
        ) == noErr, size > 0 else { return [] }

        let count = Int(size) / MemoryLayout<CMIOObjectID>.size
        var deviceIDs = [CMIOObjectID](repeating: 0, count: count)
        var dataUsed: UInt32 = 0
        guard CMIOObjectGetPropertyData(
            CMIOObjectID(kCMIOObjectSystemObject), &address, 0, nil, size, &dataUsed, &deviceIDs
        ) == noErr else { return [] }

        return deviceIDs.filter { isVideoDevice($0) }
    }

    private static func isVideoDevice(_ deviceID: CMIOObjectID) -> Bool {
        var address = CMIOObjectPropertyAddress(
            mSelector: CMIOObjectPropertySelector(kCMIODevicePropertyStreams),
            mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeGlobal),
            mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementMain)
        )
        var size: UInt32 = 0
        return CMIOObjectGetPropertyDataSize(deviceID, &address, 0, nil, &size) == noErr && size > 0
    }
}
