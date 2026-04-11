import EventKit

func currentMeetingName() -> String? {
    let store = EKEventStore()
    let semaphore = DispatchSemaphore(value: 0)
    var granted = false
    store.requestFullAccessToEvents { ok, err in
        granted = ok
        if let err = err { log("Calendar: access error — \(err)") }
        semaphore.signal()
    }
    semaphore.wait()
    guard granted else {
        log("Calendar: access denied")
        return nil
    }

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
