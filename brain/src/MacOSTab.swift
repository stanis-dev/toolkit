import SwiftUI
import CoreAudio

class AudioDeviceEnforcer: ObservableObject {
    @Published var enabled: Bool {
        didSet {
            UserDefaults.standard.set(enabled, forKey: "brain.enforceAudioDevice")
            log("Audio.enforce: toggle \(oldValue ? "ON" : "OFF") → \(enabled ? "ON" : "OFF")")
            if enabled { startPolling() } else { stopPolling() }
        }
    }
    @Published var currentDevice: String = ""
    private var timer: Timer?
    private var lastTargetAvailable: Bool?
    private var lastHeartbeat: Date = .distantPast
    private let heartbeatInterval: TimeInterval = 300

    init() {
        self.enabled = UserDefaults.standard.bool(forKey: "brain.enforceAudioDevice")
        refreshCurrentDevice()
        let available = findInputDevice(named: kTargetAudioDevice) != nil
        lastTargetAvailable = available
        log("Audio.enforce: init enabled=\(enabled) current='\(currentDevice)' target='\(kTargetAudioDevice)' available=\(available)")
        if enabled { startPolling() }
    }

    private func startPolling() {
        stopPolling()
        log("Audio.enforce: polling started (every 3s, heartbeat every \(Int(heartbeatInterval))s)")
        lastHeartbeat = Date()
        enforce()
        timer = Timer.scheduledTimer(withTimeInterval: 3, repeats: true) { [weak self] _ in
            self?.enforce()
        }
    }

    private func stopPolling() {
        guard timer != nil else { return }
        timer?.invalidate()
        timer = nil
        log("Audio.enforce: polling stopped")
    }

    private func enforce() {
        let previousDevice = currentDevice
        refreshCurrentDevice()
        let targetID = findInputDevice(named: kTargetAudioDevice)
        let available = targetID != nil

        if available != lastTargetAvailable {
            log("Audio.enforce: target '\(kTargetAudioDevice)' \(available ? "connected" : "disconnected")")
            lastTargetAvailable = available
        }

        if previousDevice != currentDevice && !previousDevice.isEmpty {
            log("Audio.enforce: current input changed externally '\(previousDevice)' → '\(currentDevice)'")
        }

        if currentDevice != kTargetAudioDevice, let deviceId = targetID {
            setDefaultInputDevice(deviceId)
            refreshCurrentDevice()
            log("Audio.enforce: switched default input → '\(kTargetAudioDevice)'")
        }

        if Date().timeIntervalSince(lastHeartbeat) >= heartbeatInterval {
            log("Audio.enforce: heartbeat current='\(currentDevice)' target='\(kTargetAudioDevice)' available=\(available)")
            lastHeartbeat = Date()
        }
    }

    private func refreshCurrentDevice() {
        let id = getDefaultInputDevice()
        currentDevice = getDeviceName(id) ?? "Unknown"
    }
}

struct MacOSTabView: View {
    @StateObject private var enforcer = AudioDeviceEnforcer()
    @ObservedObject var exporter: ChatSyncRunner
    @ObservedObject var autoRefresh: ChatAutoRefreshCoordinator

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text("macOS")
                .font(.system(size: 15, weight: .semibold))
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
            Divider()

            VStack(alignment: .leading, spacing: 12) {
                Toggle(isOn: $enforcer.enabled) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Enforce default audio input")
                            .font(.system(size: 13))
                        Text("Always set to \(kTargetAudioDevice)")
                            .font(.system(size: 11))
                            .foregroundStyle(.secondary)
                    }
                }

                HStack(spacing: 6) {
                    Circle()
                        .fill(enforcer.currentDevice == kTargetAudioDevice ? .green : .orange)
                        .frame(width: 8, height: 8)
                    Text("Current: \(enforcer.currentDevice)")
                        .font(.system(size: 12))
                        .foregroundStyle(.secondary)
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)

            Divider()

            VStack(alignment: .leading, spacing: 12) {
                Text("Chat Sync")
                    .font(.system(size: 13, weight: .medium))

                chatSyncRow(
                    label: "Slack",
                    status: autoRefresh.slackStatus,
                    running: exporter.slackRunning,
                    progress: exporter.slackProgress,
                    result: exporter.slackResult,
                    enabled: $autoRefresh.slackEnabled
                ) {
                    exporter.runSlackExport()
                }

                chatSyncRow(
                    label: "Teams",
                    status: autoRefresh.teamsStatus,
                    running: exporter.teamsRunning,
                    progress: exporter.teamsProgress,
                    result: exporter.teamsResult,
                    enabled: $autoRefresh.teamsEnabled
                ) {
                    exporter.runTeamsExport()
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
    }

    private func chatSyncRow(label: String, status: AutoRefreshPlatformStatus, running: Bool,
                             progress: String, result: ExportResult, enabled: Binding<Bool>,
                             action: @escaping () -> Void) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack(spacing: 10) {
                Text(label)
                    .font(.system(size: 12))
                Text(status.cadence)
                    .font(.system(size: 11))
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
                Spacer()
                Text("Auto")
                    .font(.system(size: 11))
                    .foregroundStyle(.secondary)
                Toggle("", isOn: enabled)
                    .labelsHidden()
                    .toggleStyle(.switch)
                    .controlSize(.mini)
                Button(action: action) {
                    HStack(spacing: 6) {
                        if running {
                            ProgressView()
                                .controlSize(.small)
                        }
                        Text(running ? "Syncing…" : "Sync")
                            .font(.system(size: 12))
                    }
                }
                .disabled(running)
            }

            HStack(spacing: 6) {
                if let badge = stateBadge(for: status) {
                    Text(badge.text)
                        .font(.system(size: 10, weight: .medium))
                        .foregroundStyle(badge.foreground)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(badge.background, in: Capsule())
                }
                if status.queuedCount > 0 && status.headline != "Queued" {
                    Text("Queued \(status.queuedCount)")
                        .font(.system(size: 11))
                        .foregroundStyle(.secondary)
                }
                if running, !progress.isEmpty {
                    ProgressView()
                        .controlSize(.small)
                    Text(progress)
                        .font(.system(size: 11))
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                        .truncationMode(.middle)
                } else if !status.detail.isEmpty {
                    Text(status.detail)
                        .font(.system(size: 11))
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
                if !running, result.finishedAt != nil, !result.summary.isEmpty {
                    Text("•")
                        .font(.system(size: 11))
                        .foregroundStyle(.tertiary)
                    Image(systemName: result.succeeded ? "checkmark.circle.fill" : "exclamationmark.circle.fill")
                        .font(.system(size: 10))
                        .foregroundStyle(result.succeeded ? .green : .red)
                    Text(result.summary)
                        .font(.system(size: 11))
                        .foregroundColor(result.succeeded ? .secondary : .red)
                        .lineLimit(1)
                        .truncationMode(.tail)
                    if let finishedAt = result.finishedAt {
                        Text("(\(relativeTimeSince(finishedAt)))")
                            .font(.system(size: 11))
                            .foregroundStyle(.tertiary)
                    }
                }
            }
        }
    }

    private func relativeTimeSince(_ date: Date) -> String {
        let s = max(0, Int(Date().timeIntervalSince(date)))
        if s < 60 { return "\(s)s" }
        if s < 3600 { return "\(s / 60)m" }
        return "\(s / 3600)h"
    }

    private func stateBadge(for status: AutoRefreshPlatformStatus) -> (text: String, foreground: Color, background: Color)? {
        switch status.headline {
        case "Syncing":
            return ("Syncing", .green, .green.opacity(0.12))
        case "Queued":
            return ("Queued", .orange, .orange.opacity(0.12))
        case "Off":
            return ("Off", .secondary, .secondary.opacity(0.12))
        default:
            return nil
        }
    }
}
