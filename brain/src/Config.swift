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
let kAssistantOpenCodeURL = URL(string: "http://127.0.0.1:4096")!
let kAssistantOpenCodeLaunchCommand = "opencode web --hostname 127.0.0.1 --port 4096"
let kAssistantOpenCodeLastTargetDefaultsKey = "brain.assistant.opencode.last-target"
let kWorkRadarSkillFile = "/Users/stan/code/toolkit/skills/work-radar/SKILL.md"
let kCommunicationCopilotSkillFile = "/Users/stan/code/toolkit/skills/communication-copilot/SKILL.md"
let kGitHubSkillFile = "/Users/stan/.codex/plugins/cache/openai-curated/github/f78e3ad49297672a905eb7afb6aa0cef34edc79e/skills/github/SKILL.md"
let kCursorChatHistorySkillFile = "/Users/stan/code/toolkit/skills/cursor-chat-history/SKILL.md"
let kCodexSessionsDir = "/Users/stan/.codex/sessions"
let kCodexSessionIndexFile = "/Users/stan/.codex/session_index.jsonl"
let kCodexHistoryFile = "/Users/stan/.codex/history.jsonl"
let kCodexSessionStorageDir = "/Users/stan/Library/Application Support/Codex/Session Storage"

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

func log(_ msg: String) {
    let ts = DateFormatter.localizedString(from: Date(), dateStyle: .none, timeStyle: .medium)
    let line = "[\(ts)] \(msg)\n"
    fputs(line, stderr)
    if let data = line.data(using: .utf8),
       let fh = FileHandle(forWritingAtPath: kLogFile) {
        fh.seekToEndOfFile()
        fh.write(data)
        fh.closeFile()
    } else {
        FileManager.default.createFile(atPath: kLogFile, contents: line.data(using: .utf8))
    }
}
