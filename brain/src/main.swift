import AppKit

try? FileManager.default.createDirectory(atPath: kOutputDir, withIntermediateDirectories: true)

let recState = RecordingState()
let appState = AppState()
let listState = RecordingListState()
let playback = PlaybackState()
let assistantState = AssistantState()
let chatSync = ChatSyncRunner()
let chatAutoRefresh = ChatAutoRefreshCoordinator(syncRunner: chatSync)
let delegate = AppDelegate(
    recState: recState,
    appState: appState,
    listState: listState,
    playback: playback,
    assistantState: assistantState,
    chatSync: chatSync,
    chatAutoRefresh: chatAutoRefresh
)

let app = NSApplication.shared
app.setActivationPolicy(.regular)
app.delegate = delegate

signal(SIGINT, SIG_IGN)
let sigSource = DispatchSource.makeSignalSource(signal: SIGINT, queue: .main)
sigSource.setEventHandler {
    recState.stopRecording()
}
sigSource.resume()

app.run()
