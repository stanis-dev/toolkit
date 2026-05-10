import Foundation
import Combine

enum ChatPlatform: String {
    case slack = "Slack"
    case teams = "Teams"
}

struct ExportResult {
    var summary: String = ""
    var succeeded: Bool = false
    var elapsed: TimeInterval = 0
    var finishedAt: Date?
}

final class ChatSyncRunner: ObservableObject {
    @Published var slackRunning = false
    @Published var teamsRunning = false
    @Published var slackProgress = ""
    @Published var teamsProgress = ""
    @Published var slackResult = ExportResult()
    @Published var teamsResult = ExportResult()

    private var slackProcess: Process?
    private var teamsProcess: Process?
    private var completionHandlers: [ChatPlatform: [(ExportResult) -> Void]] = [:]

    @discardableResult
    func runSlackExport(arguments: [String] = [], reason: String = "manual",
                        completion: ((ExportResult) -> Void)? = nil) -> Bool {
        run(platform: .slack, script: kSlackExportScript, arguments: arguments, reason: reason, completion: completion)
    }

    @discardableResult
    func runTeamsExport(arguments: [String] = [], reason: String = "manual",
                        completion: ((ExportResult) -> Void)? = nil) -> Bool {
        run(platform: .teams, script: kTeamsExportScript, arguments: arguments, reason: reason, completion: completion)
    }

    func isRunning(_ platform: ChatPlatform) -> Bool {
        switch platform {
        case .slack: return slackRunning
        case .teams: return teamsRunning
        }
    }

    private func run(platform: ChatPlatform, script: String, arguments: [String], reason: String,
                     completion: ((ExportResult) -> Void)?) -> Bool {
        if isRunning(platform) {
            return false
        }
        if let completion {
            completionHandlers[platform, default: []].append(completion)
        }

        setRunning(true, platform: platform)
        setProgress("Starting…", platform: platform)
        setResult(ExportResult(), platform: platform)

        let startTime = Date()
        let process = Process()
        process.executableURL = URL(fileURLWithPath: kPython)
        process.arguments = ["-u", script] + arguments
        process.currentDirectoryURL = URL(fileURLWithPath: kOutputDir)
        var env = ProcessInfo.processInfo.environment
        env["PATH"] = "/Users/stan/.local/bin:/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:" + (env["PATH"] ?? "")
        process.environment = env

        log("\(platform.rawValue) sync: starting (\(reason)) args=\(arguments)")

        let pipe = Pipe()
        process.standardOutput = pipe
        process.standardError = pipe

        var lineBuffer = ""
        var lastProgressLine = ""
        var summaryLine = ""

        pipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            guard !data.isEmpty, let text = String(data: data, encoding: .utf8) else { return }
            lineBuffer += text
            let lines = lineBuffer.components(separatedBy: "\n")
            lineBuffer = lines.last ?? ""
            for line in lines.dropLast() {
                let trimmed = line.trimmingCharacters(in: .whitespacesAndNewlines)
                guard !trimmed.isEmpty else { continue }
                lastProgressLine = trimmed
                if trimmed.contains("new messages")
                    || trimmed.contains("Export complete")
                    || trimmed.contains("Discovery complete")
                    || trimmed.hasPrefix("Done:") {
                    summaryLine = trimmed
                }
            }
            DispatchQueue.main.async {
                self?.setProgress(String(lastProgressLine.prefix(100)), platform: platform)
            }
        }

        process.terminationHandler = { [weak self] proc in
            pipe.fileHandleForReading.readabilityHandler = nil
            let elapsed = Date().timeIntervalSince(startTime)
            let code = proc.terminationStatus
            let summary = code == 0 ? (summaryLine.isEmpty ? (lastProgressLine.isEmpty ? "Finished" : lastProgressLine) : summaryLine)
                                    : "Failed (exit \(code))"
            let result = ExportResult(summary: summary, succeeded: code == 0, elapsed: elapsed, finishedAt: Date())
            log("\(platform.rawValue) sync: exited with code \(code) in \(Int(elapsed))s")
            DispatchQueue.main.async {
                self?.setRunning(false, platform: platform)
                self?.setProgress("", platform: platform)
                self?.setProcess(nil, platform: platform)
                self?.setResult(result, platform: platform)
                let handlers = self?.completionHandlers.removeValue(forKey: platform) ?? []
                handlers.forEach { $0(result) }
            }
        }

        setProcess(process, platform: platform)
        do {
            try process.run()
            log("\(platform.rawValue) sync: launched (pid \(process.processIdentifier))")
            return true
        } catch {
            log("\(platform.rawValue) sync: launch failed: \(error)")
            setRunning(false, platform: platform)
            setProgress("", platform: platform)
            setProcess(nil, platform: platform)
            let result = ExportResult(summary: "Launch failed", succeeded: false)
            setResult(result, platform: platform)
            let handlers = completionHandlers.removeValue(forKey: platform) ?? []
            handlers.forEach { $0(result) }
            return false
        }
    }

    private func setRunning(_ running: Bool, platform: ChatPlatform) {
        switch platform {
        case .slack: slackRunning = running
        case .teams: teamsRunning = running
        }
    }

    private func setProgress(_ progress: String, platform: ChatPlatform) {
        switch platform {
        case .slack: slackProgress = progress
        case .teams: teamsProgress = progress
        }
    }

    private func setResult(_ result: ExportResult, platform: ChatPlatform) {
        switch platform {
        case .slack: slackResult = result
        case .teams: teamsResult = result
        }
    }

    private func setProcess(_ process: Process?, platform: ChatPlatform) {
        switch platform {
        case .slack: slackProcess = process
        case .teams: teamsProcess = process
        }
    }
}
