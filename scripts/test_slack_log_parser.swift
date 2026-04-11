import Foundation

func expect(_ condition: @autoclosure () -> Bool, _ message: String) {
    if !condition() {
        fputs("FAIL: \(message)\n", stderr)
        exit(1)
    }
}

@main
struct SlackLogParserTests {
    static func main() {
        testNotificationParsing()
        testRTMParsing()
        print("Slack log parser tests passed.")
    }

    static func testNotificationParsing() {
        let parser = SlackLogParser()
        expect(parser.feed(line: "Store: NEW_NOTIFICATION {").isEmpty, "multiline notification should not emit early")
        expect(parser.feed(line: #"  "teamId": "T024QJSEN","#).isEmpty, "team line should remain buffered")
        expect(parser.feed(line: #"  "channel": "C096PSTHJTH","#).isEmpty, "channel line should remain buffered")
        expect(parser.feed(line: #"  "thread_ts": "1773767754.637419","#).isEmpty, "thread line should remain buffered")
        let events = parser.feed(line: "}")
        expect(events.count == 1, "notification should emit exactly one event")
        expect(events[0] == SlackLogEvent(
            teamId: "T024QJSEN",
            channel: "C096PSTHJTH",
            threadTS: "1773767754.637419",
            source: "notification"
        ), "notification payload should match expected fields")
    }

    static func testRTMParsing() {
        let parser = SlackLogParser()
        let events = parser.feed(line: "[03/30/26, 15:52:42:288] info: [RTM-THREADS] (T024QJSEN) update_global_thread_state")
        expect(events.count == 1, "RTM line should emit one event")
        expect(events[0] == SlackLogEvent(teamId: "T024QJSEN", channel: nil, threadTS: nil, source: "rtm"),
               "RTM event should capture team id only")
    }
}
