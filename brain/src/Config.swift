import Foundation

let kSampleRate: Double = 48000
let kOutputDir = "/Users/stan/code/toolkit/brain/data"
let kLogFile = "\(kOutputDir)/brain.log"
let kModelsDir = "/Users/stan/code/toolkit/brain/models"
let kTranscribeScript = "/Users/stan/code/toolkit/brain/scripts/transcribe.py"
let kPython = "/Users/stan/code/toolkit/brain/.venv/bin/python3"
let kDictateScript = "/Users/stan/code/toolkit/brain/scripts/dictate.py"
let kSlackExportScript = "/Users/stan/code/toolkit/brain/scripts/slack_export.py"
let kTeamsExportScript = "/Users/stan/code/toolkit/brain/scripts/teams_export.py"
let kGoogleChatExportScript = "/Users/stan/code/toolkit/brain/scripts/google_chat_export.py"
let kSlackLogDir = NSString(string: "~/Library/Application Support/Slack/logs/default").expandingTildeInPath
let kSlackDataDir = "\(kOutputDir)/slack"
let kTeamsDataDir = "\(kOutputDir)/teams"
let kBraveBundleID = "com.brave.Browser"
let kTeamsStorageDirs: [String] = [
    NSString(string: "~/Library/Application Support/BraveSoftware/Brave-Browser/Default/IndexedDB/https_teams.microsoft.com_0.indexeddb.leveldb").expandingTildeInPath,
    NSString(string: "~/Library/Application Support/BraveSoftware/Brave-Browser/Default/IndexedDB/https_teams.cloud.microsoft_0.indexeddb.leveldb").expandingTildeInPath,
]
let kTargetAudioDevice = "Scarlett Solo USB"
let kSpeakersFile = "\(kOutputDir)/speakers.json"
let kNamesFile = "\(kOutputDir)/names.json"
let kAssistantTodoFile = "\(kOutputDir)/assistant-todo.md"
let kControlSocket = "/Users/stan/Library/Application Support/Brain/control.sock"
let kAssistantOpenCodeURL = URL(string: "http://127.0.0.1:4096")!
let kAssistantOpenCodeLaunchCommand = "opencode web --hostname 127.0.0.1 --port 4096"
let kAssistantOpenCodeLastTargetDefaultsKey = "brain.assistant.opencode.last-target"

/// Extensions of the derived transcript artifacts for a `rec-*.wav`, relative to
/// the shared base path. Excludes `.wav` itself so callers choose whether to also
/// remove the source recording.
let kTranscriptArtifactExtensions = [
    ".json", ".txt", ".polished.txt", ".reasoning.jsonl", ".summary.md", ".summary-reasoning.jsonl"
]

let kMeetingAppBundleIDs: [String: String] = [
    "com.microsoft.teams2": "Teams",
    "com.microsoft.teams": "Teams",
    "com.tinyspeck.slackmacgap": "Slack",
]
let kMeetingBrowserBundleIDs: Set<String> = [
    "com.google.Chrome",
    "com.apple.Safari",
    kBraveBundleID,
    "company.thebrowser.Browser",
]
let kMeetingNotificationCategory = "MEETING_DETECTED"
let kMeetingRecordAction = "RECORD_MEETING"
let kMeetingDebounceSec: TimeInterval = 60
let kMicSettleDelaySec: TimeInterval = 5
let kMeetingRecentActivationWindowSec: TimeInterval = 15
let kMeetingDictationCooldownSec: TimeInterval = 12
let kMeetingSlackWindowKeywords = ["huddle", "call"]
let kMeetingTeamsWindowKeywords = ["meeting", "call"]
let kMeetingBrowserScriptNames: [String: String] = [
    "com.google.Chrome": "Google Chrome",
    "com.apple.Safari": "Safari",
    kBraveBundleID: "Brave Browser",
    "company.thebrowser.Browser": "Arc",
]
let kMeetingAutomationBrowserBundleID = kBraveBundleID
let kMeetingAutomationBrowserName = "Brave Browser"
let kMeetingRelevantBundleIDs = Set(kMeetingAppBundleIDs.keys).union(kMeetingBrowserBundleIDs)

func formatDuration(_ t: TimeInterval) -> String {
    let s = Int(t)
    let h = s / 3600, m = (s % 3600) / 60, sec = s % 60
    return h > 0 ? String(format: "%d:%02d:%02d", h, m, sec) : String(format: "%d:%02d", m, sec)
}

private let kLogMaxBytes: UInt64 = 5 * 1024 * 1024
private let logQueue = DispatchQueue(label: "brain.log")

func log(_ msg: String) {
    let ts = DateFormatter.localizedString(from: Date(), dateStyle: .none, timeStyle: .medium)
    let line = "[\(ts)] \(msg)\n"
    fputs(line, stderr)
    guard let data = line.data(using: .utf8) else { return }
    logQueue.async {
        let fm = FileManager.default
        if let size = (try? fm.attributesOfItem(atPath: kLogFile))?[.size] as? UInt64,
           size > kLogMaxBytes {
            let rotated = kLogFile + ".old"
            try? fm.removeItem(atPath: rotated)
            try? fm.moveItem(atPath: kLogFile, toPath: rotated)
        }
        if let fh = FileHandle(forWritingAtPath: kLogFile) {
            fh.seekToEndOfFile()
            fh.write(data)
            fh.closeFile()
        } else {
            fm.createFile(atPath: kLogFile, contents: data)
        }
    }
}
