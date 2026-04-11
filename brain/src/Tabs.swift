import SwiftUI
import AppKit
import AVFoundation
import ScreenCaptureKit
import ApplicationServices
import CoreServices
import EventKit

class PermissionsState: ObservableObject {
    @Published var microphone: Bool = false
    @Published var screenRecording: Bool = false
    @Published var accessibility: Bool = false
    @Published var calendar: Bool = false
    @Published var browserAutomation: Bool = false
    private var timer: Timer?
    private let calendarStore = EKEventStore()
    private let automationQueue = DispatchQueue(label: "brain.permissions.automation")
    private let browserAutomationCacheKey = "brain.permissions.browserAutomation.brave"
    private var automationRefreshInFlight = false

    init() {
        browserAutomation = UserDefaults.standard.bool(forKey: browserAutomationCacheKey)
        refresh()
    }

    func startPolling() {
        refresh()
        timer = Timer.scheduledTimer(withTimeInterval: 2, repeats: true) { [weak self] _ in
            self?.refresh()
        }
    }

    func stopPolling() {
        timer?.invalidate()
        timer = nil
    }

    func refresh() {
        microphone = AVCaptureDevice.authorizationStatus(for: .audio) == .authorized
        calendar = EKEventStore.authorizationStatus(for: .event) == .fullAccess
        screenRecording = CGPreflightScreenCaptureAccess()
        let opts = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: false] as CFDictionary
        accessibility = AXIsProcessTrustedWithOptions(opts)
        browserAutomation = UserDefaults.standard.bool(forKey: browserAutomationCacheKey)
        refreshBrowserAutomation(promptIfNeeded: false)
    }

    func requestMicrophone() {
        AVCaptureDevice.requestAccess(for: .audio) { _ in
            DispatchQueue.main.async { self.refresh() }
        }
    }

    func requestScreenRecording() {
        CGRequestScreenCaptureAccess()
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) { self.refresh() }
    }

    func requestAccessibility() {
        let opts = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true] as CFDictionary
        _ = AXIsProcessTrustedWithOptions(opts)
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) { self.refresh() }
    }

    func requestCalendar() {
        calendarStore.requestFullAccessToEvents { _, _ in
            DispatchQueue.main.async { self.refresh() }
        }
    }

    func requestBrowserAutomation() {
        ensureAutomationTargetRunning { [weak self] running in
            guard let self = self else { return }
            guard running else {
                log("Permissions: could not launch \(kMeetingAutomationBrowserName) for automation permission")
                return
            }
            self.refreshBrowserAutomation(promptIfNeeded: true)
        }
    }

    func openSystemSettings() {
        NSWorkspace.shared.open(URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy")!)
    }

    private func refreshBrowserAutomation(promptIfNeeded: Bool) {
        guard !automationRefreshInFlight else { return }
        automationRefreshInFlight = true
        let bundleID = kMeetingAutomationBrowserBundleID

        automationQueue.async { [weak self] in
            guard let self = self else { return }
            let status = self.browserAutomationStatus(
                bundleID: bundleID,
                askUserIfNeeded: promptIfNeeded
            )
            DispatchQueue.main.async {
                self.automationRefreshInFlight = false
                self.applyBrowserAutomationStatus(status)
            }
        }
    }

    private func applyBrowserAutomationStatus(_ status: OSStatus?) {
        let cached = UserDefaults.standard.bool(forKey: browserAutomationCacheKey)
        let granted: Bool

        switch status {
        case noErr:
            granted = true
        case OSStatus(errAEEventWouldRequireUserConsent), OSStatus(errAEEventNotPermitted), OSStatus(errAETargetAddressNotPermitted):
            granted = false
        case OSStatus(procNotFound), nil:
            granted = cached
        default:
            granted = false
        }

        browserAutomation = granted
        UserDefaults.standard.set(granted, forKey: browserAutomationCacheKey)

        if let status, status != noErr, status != OSStatus(procNotFound), status != OSStatus(errAEEventWouldRequireUserConsent) {
            log("Permissions: browser automation status → \(status)")
        }
    }

    private func ensureAutomationTargetRunning(completion: @escaping (Bool) -> Void) {
        if isAutomationTargetRunning() {
            completion(true)
            return
        }

        guard let url = NSWorkspace.shared.urlForApplication(withBundleIdentifier: kMeetingAutomationBrowserBundleID) else {
            completion(false)
            return
        }

        let config = NSWorkspace.OpenConfiguration()
        config.activates = false
        NSWorkspace.shared.openApplication(at: url, configuration: config) { _, error in
            if let error {
                log("Permissions: failed to launch \(kMeetingAutomationBrowserName) — \(error)")
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
                completion(self.isAutomationTargetRunning())
            }
        }
    }

    private func isAutomationTargetRunning() -> Bool {
        !NSRunningApplication.runningApplications(withBundleIdentifier: kMeetingAutomationBrowserBundleID).isEmpty
    }

    private func browserAutomationStatus(bundleID: String, askUserIfNeeded: Bool) -> OSStatus? {
        guard isAutomationTargetRunning() else { return OSStatus(procNotFound) }

        var desc = AEAddressDesc()
        let createStatus: OSErr = bundleID.withCString { ptr in
            AECreateDesc(DescType(typeApplicationBundleID), ptr, bundleID.utf8.count, &desc)
        }
        guard createStatus == noErr else { return OSStatus(createStatus) }
        defer { AEDisposeDesc(&desc) }

        return AEDeterminePermissionToAutomateTarget(
            &desc,
            AEEventClass(typeWildCard),
            AEEventID(typeWildCard),
            askUserIfNeeded
        )
    }
}

struct SettingsTabView: View {
    @StateObject private var perms = PermissionsState()

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text("Settings")
                .font(.system(size: 15, weight: .semibold))
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
            Divider()

            VStack(alignment: .leading, spacing: 4) {
                Text("Permissions")
                    .font(.system(size: 13, weight: .medium))
                    .padding(.bottom, 4)

                PermissionRow(name: "Microphone", icon: "mic.fill",
                              granted: perms.microphone, action: perms.requestMicrophone)
                PermissionRow(name: "Screen Recording", icon: "rectangle.dashed.badge.record",
                              granted: perms.screenRecording, action: perms.requestScreenRecording)
                PermissionRow(name: "Accessibility", icon: "accessibility",
                              granted: perms.accessibility, action: perms.requestAccessibility)
                PermissionRow(name: "Calendar", icon: "calendar",
                              granted: perms.calendar, action: perms.requestCalendar)
                PermissionRow(name: "Automation (\(kMeetingAutomationBrowserName.replacingOccurrences(of: " Browser", with: "")))", icon: "globe",
                              granted: perms.browserAutomation, action: perms.requestBrowserAutomation)

                Button(action: { perms.openSystemSettings() }) {
                    Text("Open System Settings")
                        .font(.system(size: 11))
                        .foregroundStyle(.secondary)
                }
                .buttonStyle(NoFocusButtonStyle())
                .padding(.top, 8)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        .onAppear { perms.startPolling() }
        .onDisappear { perms.stopPolling() }
    }
}

struct LogsTabView: View {
    @State private var lines: [String] = []
    @State private var timer: Timer?
    @State private var lastSize: UInt64 = 0

    private let maxLines = 200

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Text("Logs")
                    .font(.system(size: 15, weight: .semibold))
                Spacer()
                HoverIconButton("arrow.counterclockwise", size: 12) { loadLog(force: true) }
                HoverIconButton("trash", size: 12) { clearLog() }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
            Divider()

            if lines.isEmpty {
                Spacer()
                Text("No logs yet")
                    .font(.system(size: 13))
                    .foregroundStyle(.secondary)
                    .frame(maxWidth: .infinity)
                Spacer()
            } else {
                ScrollViewReader { proxy in
                    List {
                        ForEach(Array(lines.enumerated()), id: \.offset) { i, line in
                            Text(line)
                                .font(.system(size: 11, design: .monospaced))
                                .listRowSeparator(.hidden)
                                .listRowInsets(EdgeInsets(top: 1, leading: 12, bottom: 1, trailing: 12))
                                .textSelection(.enabled)
                                .id(i)
                        }
                    }
                    .listStyle(.plain)
                    .onChange(of: lines.count) { _, _ in
                        proxy.scrollTo(lines.count - 1, anchor: .bottom)
                    }
                    .onAppear {
                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                            if !lines.isEmpty { proxy.scrollTo(lines.count - 1, anchor: .bottom) }
                        }
                    }
                }
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        .onAppear {
            loadLog(force: true)
            timer = Timer.scheduledTimer(withTimeInterval: 2, repeats: true) { _ in loadLog() }
        }
        .onDisappear {
            timer?.invalidate()
            timer = nil
        }
    }

    private func loadLog(force: Bool = false) {
        let fm = FileManager.default
        guard let attrs = try? fm.attributesOfItem(atPath: kLogFile),
              let size = attrs[.size] as? UInt64 else {
            if force { lines = []; lastSize = 0 }
            return
        }
        guard force || size != lastSize else { return }
        lastSize = size

        guard let fh = FileHandle(forReadingAtPath: kLogFile) else { return }
        defer { fh.closeFile() }

        let tailBytes: UInt64 = 32_768
        if size > tailBytes { fh.seek(toFileOffset: size - tailBytes) }
        let data = fh.readDataToEndOfFile()
        guard let text = String(data: data, encoding: .utf8) else { return }

        var all = text.split(separator: "\n", omittingEmptySubsequences: false).map(String.init)
        if size > tailBytes { all.removeFirst() }
        lines = Array(all.suffix(maxLines))
    }

    private func clearLog() {
        try? "".write(toFile: kLogFile, atomically: true, encoding: .utf8)
        lines = []
        lastSize = 0
    }
}

struct PermissionRow: View {
    let name: String
    let icon: String
    let granted: Bool
    let action: () -> Void
    @State private var hovering = false

    var body: some View {
        HStack(spacing: 10) {
            Image(systemName: icon)
                .font(.system(size: 12))
                .frame(width: 18)
                .foregroundStyle(.secondary)
            Text(name)
                .font(.system(size: 12))
            Spacer()
            if granted {
                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 13))
                    .foregroundStyle(.green)
            } else {
                Button(action: action) {
                    Text("Grant")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(.white)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(hovering ? .red.opacity(0.8) : .red, in: RoundedRectangle(cornerRadius: 4))
                        .contentShape(Rectangle())
                }
                .buttonStyle(NoFocusButtonStyle())
                .onHover { hovering = $0 }
            }
        }
        .padding(.vertical, 4)
    }
}
