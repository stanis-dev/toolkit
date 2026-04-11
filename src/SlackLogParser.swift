import Foundation

struct SlackLogEvent: Equatable {
    var teamId: String?
    var channel: String?
    var threadTS: String?
    var source: String
}

final class SlackLogParser {
    private var pendingJSON = ""
    private var pendingBraceDepth = 0

    func feed(line rawLine: String) -> [SlackLogEvent] {
        let line = rawLine.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !line.isEmpty else { return [] }

        if pendingBraceDepth > 0 {
            pendingJSON += "\n" + line
            pendingBraceDepth += braceDelta(in: line)
            if pendingBraceDepth <= 0 {
                let payload = pendingJSON
                pendingJSON = ""
                pendingBraceDepth = 0
                if let event = parseNotificationPayload(payload) {
                    return [event]
                }
            }
            return []
        }

        if let start = line.range(of: "Store: NEW_NOTIFICATION") {
            let suffix = String(line[start.upperBound...]).trimmingCharacters(in: .whitespaces)
            if let braceIndex = suffix.firstIndex(of: "{") {
                let json = String(suffix[braceIndex...])
                pendingJSON = json
                pendingBraceDepth = braceDelta(in: json)
                if pendingBraceDepth <= 0 {
                    let payload = pendingJSON
                    pendingJSON = ""
                    pendingBraceDepth = 0
                    if let event = parseNotificationPayload(payload) {
                        return [event]
                    }
                }
            }
            return []
        }

        if line.contains("[RTM-ACTIVITY]") || line.contains("[RTM-THREADS]") {
            return [SlackLogEvent(
                teamId: captureFirst(in: line, pattern: #"\(([A-Z0-9]+)\)"#),
                channel: nil,
                threadTS: nil,
                source: "rtm"
            )]
        }

        return []
    }

    private func parseNotificationPayload(_ payload: String) -> SlackLogEvent? {
        guard let data = payload.data(using: .utf8),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            return nil
        }
        return SlackLogEvent(
            teamId: json["teamId"] as? String,
            channel: json["channel"] as? String,
            threadTS: json["thread_ts"] as? String,
            source: "notification"
        )
    }

    private func braceDelta(in text: String) -> Int {
        var delta = 0
        for char in text {
            if char == "{" { delta += 1 }
            if char == "}" { delta -= 1 }
        }
        return delta
    }

    private func captureFirst(in text: String, pattern: String) -> String? {
        guard let regex = try? NSRegularExpression(pattern: pattern),
              let match = regex.firstMatch(in: text, range: NSRange(text.startIndex..., in: text)),
              let range = Range(match.range(at: 1), in: text) else {
            return nil
        }
        return String(text[range])
    }
}
