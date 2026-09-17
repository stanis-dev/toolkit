import AppKit
import Foundation

/// Routes local commands through the same state objects used by the UI.
final class BrainControl {
    private weak var app: AppDelegate?
    private var jobs: [String: [String: Any]] = [:]
    private var jobOrder: [String] = []

    init(app: AppDelegate) { self.app = app }

    func handle(_ request: [String: Any]) -> [String: Any] {
        guard let app else { return ControlServer.error("unavailable", "Brain is shutting down.") }
        do {
            let command = try string(request, "command")
            let result: [String: Any]
            switch command {
            case "status":
                result = status(app)
            case "sync":
                let platform = try platform(request)
                guard !app.chatSync.isRunning(platform) else { throw problem("busy", "\(platform.rawValue) is already syncing.") }
                let id = UUID().uuidString
                jobs[id] = ["id": id, "platform": platformName(platform), "state": "running", "started_at": now()]
                jobOrder.append(id)
                pruneJobs()
                let completion: (ExportResult) -> Void = { [weak self] export in
                    guard let self else { return }
                    self.jobs[id]?["state"] = export.succeeded ? "succeeded" : "failed"
                    self.jobs[id]?["result"] = self.exportResult(export)
                }
                switch platform {
                case .slack: app.chatSync.runSlackExport(reason: "programmatic", completion: completion)
                case .teams: app.chatSync.runTeamsExport(reason: "programmatic", completion: completion)
                case .googleChat: app.chatAutoRefresh.syncGoogleChat(reason: "programmatic", completion: completion)
                }
                result = jobs[id]!
            case "job":
                let id = try string(request, "id")
                guard let job = jobs[id] else { throw problem("not_found", "Job not found. Jobs are retained until Brain restarts, up to 100 completed jobs.") }
                result = job
            case "auto":
                let platform = try platform(request)
                guard let enabled = request["enabled"] as? Bool else { throw problem("invalid_request", "enabled must be a boolean.") }
                switch platform {
                case .slack: app.chatAutoRefresh.slackEnabled = enabled
                case .teams: app.chatAutoRefresh.teamsEnabled = enabled
                case .googleChat: app.chatAutoRefresh.googleChatEnabled = enabled
                }
                result = chatStatus(app)[platformName(platform)] as! [String: Any]
            case "recording":
                let action = try string(request, "action")
                switch action {
                case "start":
                    guard !app.recState.isRecording else { throw problem("busy", "A recording is already in progress.") }
                    app.recState.startRecording(showErrors: false)
                case "stop": app.recState.stopRecording(); app.listState.refresh()
                case "pause", "resume":
                    guard app.recState.isRecording else { throw problem("not_recording", "No recording is in progress.") }
                    if app.recState.isPaused != (action == "pause") { app.recState.togglePause() }
                default: throw problem("invalid_request", "Unknown recording action.")
                }
                result = recordingStatus(app)
            case "recordings":
                app.listState.refresh()
                result = ["recordings": app.listState.recordings.map { recording in
                    ["id": recording.id, "name": recording.displayName, "path": recording.url.path,
                     "duration_seconds": recording.duration, "has_transcript": recording.hasTranscript,
                     "transcribing": recording.transcribing] as [String: Any]
                }]
            case "transcribe":
                let id = try string(request, "id")
                app.listState.refresh()
                guard let recording = app.listState.recordings.first(where: { $0.id == id }) else {
                    throw problem("not_found", "Recording not found.")
                }
                guard !recording.transcribing else { throw problem("busy", "This recording is already being transcribed.") }
                app.listState.transcribe(id: id)
                result = ["id": id, "accepted": true]
            case "dictation":
                let action = try string(request, "action")
                switch action {
                case "start":
                    guard app.dictatorState.status == .idle else { throw problem("busy", "Dictation is already active.") }
                    app.dictatorState.startDictation()
                    guard app.dictatorState.status == .recording else { throw problem("failed", "Dictation could not start. Check microphone permissions.") }
                case "finish":
                    guard app.dictatorState.status == .recording else { throw problem("not_recording", "Dictation is not recording.") }
                    app.dictatorState.finishDictation(andPaste: request["paste"] as? Bool ?? false)
                case "cancel":
                    guard app.dictatorState.status != .transcribing else { throw problem("busy", "Wait for dictation transcription to finish.") }
                    app.dictatorState.cancelDictation()
                default: throw problem("invalid_request", "Unknown dictation action.")
                }
                result = dictationStatus(app)
            case "todo":
                let action = try string(request, "action")
                if action == "set" || action == "append" {
                    let text = try string(request, "text", allowEmpty: true)
                    let content = action == "set" ? text : app.todoOverlayState.rawText + text
                    guard app.todoOverlayState.setText(content) else { throw problem("save_failed", "TODO could not be saved.") }
                } else if action != "get" { throw problem("invalid_request", "Unknown TODO action.") }
                result = ["text": app.todoOverlayState.rawText, "save_state": app.todoOverlayState.statusText,
                          "path": kAssistantTodoFile]
            case "navigate":
                let destination = try string(request, "tab")
                let tabs: [String: Tab] = ["assistant": .assistant, "recorder": .recorder, "dictator": .dictator,
                                           "macos": .macos, "settings": .settings, "logs": .logs]
                if destination == "hide" { app.window.orderOut(nil) }
                else {
                    guard let tab = tabs[destination] else { throw problem("invalid_request", "Unknown tab.") }
                    app.appState.selectedTab = tab
                    app.appState.viewingTranscriptId = nil
                    app.showWindow()
                }
                result = ["tab": String(describing: app.appState.selectedTab), "visible": app.window.isVisible]
            default: throw problem("unknown_command", "Unknown command: \(command)")
            }
            return ["ok": true, "result": result]
        } catch let error as CommandError {
            return ControlServer.error(error.code, error.message)
        } catch {
            return ControlServer.error("internal_error", error.localizedDescription)
        }
    }

    private func status(_ app: AppDelegate) -> [String: Any] {
        ["pid": ProcessInfo.processInfo.processIdentifier, "api_version": 1,
         "tab": String(describing: app.appState.selectedTab), "visible": app.window.isVisible,
         "chat": chatStatus(app), "recording": recordingStatus(app),
         "dictation": dictationStatus(app),
         "todo": ["save_state": app.todoOverlayState.statusText, "path": kAssistantTodoFile],
         "transcribing": app.listState.recordings.filter(\.transcribing).map(\.id)]
    }

    private func recordingStatus(_ app: AppDelegate) -> [String: Any] {
        ["active": app.recState.isRecording, "starting": app.recState.isStarting,
         "paused": app.recState.isPaused, "elapsed_seconds": app.recState.elapsed,
         "error": app.recState.startError as Any? ?? NSNull()]
    }

    private func dictationStatus(_ app: AppDelegate) -> [String: Any] {
        ["state": String(describing: app.dictatorState.status),
         "text": app.dictatorState.lastText as Any? ?? NSNull(),
         "error": app.dictatorState.lastError as Any? ?? NSNull()]
    }

    private func chatStatus(_ app: AppDelegate) -> [String: Any] {
        ["slack": ["running": app.chatSync.slackRunning, "auto": app.chatAutoRefresh.slackEnabled,
                   "progress": app.chatSync.slackProgress, "last_result": exportResult(app.chatSync.slackResult)],
         "teams": ["running": app.chatSync.teamsRunning, "auto": app.chatAutoRefresh.teamsEnabled,
                   "progress": app.chatSync.teamsProgress, "last_result": exportResult(app.chatSync.teamsResult)],
         "google-chat": ["running": app.chatSync.googleChatRunning, "auto": app.chatAutoRefresh.googleChatEnabled,
                         "progress": app.chatSync.googleChatProgress, "last_result": exportResult(app.chatSync.googleChatResult)]]
    }

    private func exportResult(_ result: ExportResult) -> [String: Any] {
        ["succeeded": result.succeeded, "summary": result.summary, "elapsed_seconds": result.elapsed,
         "finished_at": result.finishedAt.map { ISO8601DateFormatter().string(from: $0) } as Any? ?? NSNull()]
    }

    private func platform(_ request: [String: Any]) throws -> ChatPlatform {
        switch try string(request, "platform") {
        case "slack": return .slack
        case "teams": return .teams
        case "google-chat": return .googleChat
        default: throw problem("invalid_request", "platform must be slack, teams, or google-chat.")
        }
    }

    private func platformName(_ platform: ChatPlatform) -> String {
        platform == .googleChat ? "google-chat" : platform.rawValue.lowercased()
    }

    private func string(_ request: [String: Any], _ key: String, allowEmpty: Bool = false) throws -> String {
        guard let value = request[key] as? String, allowEmpty || !value.isEmpty else {
            throw problem("invalid_request", "\(key) must be a \(allowEmpty ? "" : "nonempty ")string.")
        }
        return value
    }

    private func pruneJobs() {
        while jobOrder.count > 100, let index = jobOrder.firstIndex(where: { jobs[$0]?["state"] as? String != "running" }) {
            jobs.removeValue(forKey: jobOrder.remove(at: index))
        }
    }

    private func now() -> String { ISO8601DateFormatter().string(from: Date()) }
    private struct CommandError: Error { let code: String; let message: String }
    private func problem(_ code: String, _ message: String) -> CommandError { CommandError(code: code, message: message) }
}
