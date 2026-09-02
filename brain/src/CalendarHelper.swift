import EventKit

/// Non-blocking current-meeting lookup. Returns a title only when calendar
/// access is already granted; never waits on the TCC dialog, so recording can
/// start instantly. On first-ever launch this triggers the permission request
/// in the background (the name attaches on the next recording) and returns nil.
func currentMeetingName() -> String? {
    let status = EKEventStore.authorizationStatus(for: .event)
    switch status {
    case .fullAccess:
        return fetchCurrentMeetingTitle(EKEventStore())
    case .notDetermined:
        EKEventStore().requestFullAccessToEvents { ok, err in
            if let err = err { log("Calendar: access error — \(err)") }
            log("Calendar: access \(ok ? "granted" : "denied") (async, no name this recording)")
        }
        return nil
    default:
        log("Calendar: access unavailable (status \(status.rawValue))")
        return nil
    }
}

private func fetchCurrentMeetingTitle(_ store: EKEventStore) -> String? {
    let now = Date()
    let predicate = store.predicateForEvents(
        withStart: now.addingTimeInterval(-300),
        end: now.addingTimeInterval(300),
        calendars: nil
    )
    let events = store.events(matching: predicate)
    let current = events.first { $0.startDate <= now && $0.endDate >= now }
    log("Calendar: \(events.count) events in window, current=\(current?.title ?? "none")")
    return current?.title
}

func sanitizeForFilename(_ name: String) -> String {
    let allowed = CharacterSet.alphanumerics.union(CharacterSet(charactersIn: "-_ "))
    return name.unicodeScalars
        .filter { allowed.contains($0) }
        .map { String($0) }
        .joined()
        .trimmingCharacters(in: .whitespaces)
        .replacingOccurrences(of: " ", with: "-")
        .prefix(60)
        .description
}
