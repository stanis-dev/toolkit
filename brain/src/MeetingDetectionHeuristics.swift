import Foundation

enum MeetingEvidenceKind: String, Equatable {
    case micActive
    case cameraActive
    case frontTabURL
    case focusedWindowTitle
    case recentActivation
}

struct MeetingEvidence: Equatable {
    let kind: MeetingEvidenceKind
    let detail: String?
}

struct MeetingMatch: Equatable {
    let appName: String
    let evidence: [MeetingEvidence]

    var evidenceSummary: String {
        evidence.map { item in
            if let detail = item.detail, !detail.isEmpty {
                return "\(item.kind.rawValue)=\(detail)"
            }
            return item.kind.rawValue
        }.joined(separator: ", ")
    }
}

enum MeetingProbeKind: Equatable {
    case googleMeet
    case focusedWindowTitle(keywords: [String], allowCameraFallback: Bool)
}

struct MeetingProbeObservation: Equatable {
    let appName: String
    let micActive: Bool
    let cameraActive: Bool
    let recentActivationAppName: String?
    let frontTabURL: String?
    let focusedWindowTitle: String?
}

struct MeetingSignalTransitionTracker {
    private(set) var lastMicActive: Bool?
    private(set) var lastCameraActive: Bool?

    mutating func consumeMicState(_ active: Bool) -> Bool {
        if lastMicActive == active { return false }
        lastMicActive = active
        return true
    }

    mutating func consumeCameraState(_ active: Bool) -> Bool {
        if lastCameraActive == active { return false }
        lastCameraActive = active
        return true
    }
}

struct MeetingSuppressionState {
    private(set) var suppressedUntil: Date = .distantPast
    private(set) var reason: String?

    mutating func suppress(for duration: TimeInterval, reason: String, now: Date = Date()) {
        guard duration > 0 else { return }
        let until = now.addingTimeInterval(duration)
        if until > suppressedUntil {
            suppressedUntil = until
            self.reason = reason
        }
    }

    mutating func currentReason(now: Date = Date(), externalSuppressed: Bool) -> String? {
        if externalSuppressed {
            return "external state"
        }
        if now < suppressedUntil {
            return reason ?? "manual suppression"
        }
        reason = nil
        return nil
    }
}

enum MeetingDetectionHeuristics {
    static func match(kind: MeetingProbeKind, observation: MeetingProbeObservation) -> MeetingMatch? {
        guard observation.micActive || observation.cameraActive else { return nil }

        switch kind {
        case .googleMeet:
            guard let url = observation.frontTabURL?.trimmingCharacters(in: .whitespacesAndNewlines),
                  url.lowercased().hasPrefix("https://meet.google.com/") else {
                return nil
            }
            var evidence = activityEvidence(for: observation)
            evidence.append(MeetingEvidence(kind: .frontTabURL, detail: url))
            appendRecentActivation(to: &evidence, observation: observation)
            return MeetingMatch(appName: observation.appName, evidence: evidence)

        case .focusedWindowTitle(let keywords, let allowCameraFallback):
            guard let title = observation.focusedWindowTitle?.trimmingCharacters(in: .whitespacesAndNewlines),
                  !title.isEmpty else {
                return nil
            }
            let normalizedTitle = title.lowercased()
            let matchesKeyword = keywords.contains(where: { normalizedTitle.contains($0.lowercased()) })
            let matchesCameraFallback = allowCameraFallback
                && observation.cameraActive
                && titleLooksSpecific(title, appName: observation.appName)
            guard matchesKeyword || matchesCameraFallback else {
                return nil
            }
            var evidence = activityEvidence(for: observation)
            evidence.append(MeetingEvidence(kind: .focusedWindowTitle, detail: title))
            appendRecentActivation(to: &evidence, observation: observation)
            return MeetingMatch(appName: observation.appName, evidence: evidence)
        }
    }

    private static func activityEvidence(for observation: MeetingProbeObservation) -> [MeetingEvidence] {
        var evidence: [MeetingEvidence] = []
        if observation.micActive {
            evidence.append(MeetingEvidence(kind: .micActive, detail: nil))
        }
        if observation.cameraActive {
            evidence.append(MeetingEvidence(kind: .cameraActive, detail: nil))
        }
        return evidence
    }

    private static func appendRecentActivation(
        to evidence: inout [MeetingEvidence],
        observation: MeetingProbeObservation
    ) {
        guard observation.recentActivationAppName == observation.appName else { return }
        evidence.append(MeetingEvidence(kind: .recentActivation, detail: observation.appName))
    }

    private static func titleLooksSpecific(_ title: String, appName: String) -> Bool {
        let normalized = title.lowercased().trimmingCharacters(in: .whitespacesAndNewlines)
        let app = appName.lowercased()
        let genericTitles: Set<String> = [
            app,
            "microsoft teams",
            "slack",
            "google meet",
        ]
        guard !genericTitles.contains(normalized) else { return false }
        return normalized.contains("|") || normalized.split(separator: " ").count >= 2
    }
}
