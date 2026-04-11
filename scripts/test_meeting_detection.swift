import Foundation

func expect(_ condition: @autoclosure () -> Bool, _ message: String) {
    if !condition() {
        fputs("FAIL: \(message)\n", stderr)
        exit(1)
    }
}

func expectNil(_ value: MeetingMatch?, _ message: String) {
    expect(value == nil, message)
}

func evidenceKinds(_ match: MeetingMatch) -> [MeetingEvidenceKind] {
    match.evidence.map(\.kind)
}

@main
struct MeetingDetectionTests {
    static func main() {
        testBackgroundSlackDoesNotMatch()
        testDictationCooldownSuppressesLingeringMic()
        testGoogleMeetMatchesWithFrontTabProof()
        testBackgroundBrowserWithoutFrontTabDoesNotMatch()
        testNativeAppsRequireWindowKeywords()
        testTeamsCameraFallbackMatchesSpecificWindow()
        testTransitionTrackerDedupesCallbacks()
        print("Meeting detection tests passed.")
    }

    static func testBackgroundSlackDoesNotMatch() {
        let observation = MeetingProbeObservation(
            appName: "Slack",
            micActive: true,
            cameraActive: false,
            recentActivationAppName: nil,
            frontTabURL: nil,
            focusedWindowTitle: nil
        )
        let match = MeetingDetectionHeuristics.match(
            kind: .focusedWindowTitle(keywords: ["huddle", "call"], allowCameraFallback: false),
            observation: observation
        )
        expectNil(match, "background Slack without focused call title should not match")
    }

    static func testDictationCooldownSuppressesLingeringMic() {
        var suppression = MeetingSuppressionState()
        let start = Date(timeIntervalSince1970: 1_000)
        suppression.suppress(for: 12, reason: "dictation cooldown", now: start)
        expect(
            suppression.currentReason(now: start.addingTimeInterval(5), externalSuppressed: false) == "dictation cooldown",
            "dictation cooldown should suppress lingering mic activity"
        )
        expect(
            suppression.currentReason(now: start.addingTimeInterval(13), externalSuppressed: false) == nil,
            "suppression should expire after the cooldown window"
        )
    }

    static func testGoogleMeetMatchesWithFrontTabProof() {
        let observation = MeetingProbeObservation(
            appName: "Google Meet",
            micActive: true,
            cameraActive: false,
            recentActivationAppName: "Google Meet",
            frontTabURL: "https://meet.google.com/abc-defg-hij",
            focusedWindowTitle: nil
        )
        guard let match = MeetingDetectionHeuristics.match(kind: .googleMeet, observation: observation) else {
            fputs("FAIL: Google Meet should match with a front tab URL\n", stderr)
            exit(1)
        }
        expect(match.appName == "Google Meet", "Google Meet match should preserve app name")
        expect(evidenceKinds(match).contains(.micActive), "Google Meet match should include mic evidence")
        expect(evidenceKinds(match).contains(.frontTabURL), "Google Meet match should include tab URL evidence")
        expect(evidenceKinds(match).contains(.recentActivation), "Google Meet match should include recent activation evidence")
    }

    static func testBackgroundBrowserWithoutFrontTabDoesNotMatch() {
        let observation = MeetingProbeObservation(
            appName: "Google Meet",
            micActive: true,
            cameraActive: false,
            recentActivationAppName: nil,
            frontTabURL: nil,
            focusedWindowTitle: nil
        )
        let match = MeetingDetectionHeuristics.match(kind: .googleMeet, observation: observation)
        expectNil(match, "browser activity without a front Meet tab should not match")
    }

    static func testNativeAppsRequireWindowKeywords() {
        let slackObservation = MeetingProbeObservation(
            appName: "Slack",
            micActive: true,
            cameraActive: false,
            recentActivationAppName: "Slack",
            frontTabURL: nil,
            focusedWindowTitle: "Slack | Stanis"
        )
        let teamsObservation = MeetingProbeObservation(
            appName: "Teams",
            micActive: true,
            cameraActive: false,
            recentActivationAppName: "Teams",
            frontTabURL: nil,
            focusedWindowTitle: "Microsoft Teams"
        )
        expectNil(
            MeetingDetectionHeuristics.match(
                kind: .focusedWindowTitle(keywords: ["huddle", "call"], allowCameraFallback: false),
                observation: slackObservation
            ),
            "Slack should not match without huddle/call keywords"
        )
        expectNil(
            MeetingDetectionHeuristics.match(
                kind: .focusedWindowTitle(keywords: ["meeting", "call"], allowCameraFallback: true),
                observation: teamsObservation
            ),
            "Teams should not match without meeting/call keywords"
        )
    }

    static func testTeamsCameraFallbackMatchesSpecificWindow() {
        let teamsObservation = MeetingProbeObservation(
            appName: "Teams",
            micActive: true,
            cameraActive: true,
            recentActivationAppName: "Teams",
            frontTabURL: nil,
            focusedWindowTitle: "Pronet + Sierra Standup | Microsoft Teams"
        )
        guard let match = MeetingDetectionHeuristics.match(
            kind: .focusedWindowTitle(keywords: ["meeting", "call"], allowCameraFallback: true),
            observation: teamsObservation
        ) else {
            fputs("FAIL: Teams should match when camera is active and the window title is meeting-specific\n", stderr)
            exit(1)
        }
        expect(match.appName == "Teams", "Teams camera fallback should preserve app name")
        expect(evidenceKinds(match).contains(.cameraActive), "Teams camera fallback should include camera evidence")
        expect(evidenceKinds(match).contains(.focusedWindowTitle), "Teams camera fallback should include title evidence")
    }

    static func testTransitionTrackerDedupesCallbacks() {
        var tracker = MeetingSignalTransitionTracker()
        expect(tracker.consumeMicState(true), "first mic-on transition should be consumed")
        expect(!tracker.consumeMicState(true), "duplicate mic-on callback should be ignored")
        expect(tracker.consumeMicState(false), "mic-off transition should be consumed")
        expect(!tracker.consumeMicState(false), "duplicate mic-off callback should be ignored")
        expect(tracker.consumeCameraState(true), "first camera-on transition should be consumed")
        expect(!tracker.consumeCameraState(true), "duplicate camera-on callback should be ignored")
    }
}
