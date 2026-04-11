import SwiftUI
import CoreAudio

class AudioDeviceEnforcer: ObservableObject {
    @Published var enabled: Bool {
        didSet {
            UserDefaults.standard.set(enabled, forKey: "brain.enforceAudioDevice")
            if enabled { startPolling() } else { stopPolling() }
        }
    }
    @Published var currentDevice: String = ""
    private var timer: Timer?

    init() {
        self.enabled = UserDefaults.standard.bool(forKey: "brain.enforceAudioDevice")
        refreshCurrentDevice()
        if enabled { startPolling() }
    }

    private func startPolling() {
        stopPolling()
        enforce()
        timer = Timer.scheduledTimer(withTimeInterval: 3, repeats: true) { [weak self] _ in
            self?.enforce()
        }
    }

    private func stopPolling() {
        timer?.invalidate()
        timer = nil
    }

    private func enforce() {
        refreshCurrentDevice()
        if currentDevice != kTargetAudioDevice {
            if let deviceId = findInputDevice(named: kTargetAudioDevice) {
                setDefaultInputDevice(deviceId)
                refreshCurrentDevice()
                log("Audio: set default input to \(kTargetAudioDevice)")
            }
        }
    }

    private func refreshCurrentDevice() {
        let id = getDefaultInputDevice()
        currentDevice = getDeviceName(id) ?? "Unknown"
    }
}

private func getDefaultInputDevice() -> AudioDeviceID {
    var deviceID = AudioDeviceID(0)
    var size = UInt32(MemoryLayout<AudioDeviceID>.size)
    var address = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyDefaultInputDevice,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain
    )
    AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size, &deviceID)
    return deviceID
}

private func getDeviceName(_ deviceID: AudioDeviceID) -> String? {
    var address = AudioObjectPropertyAddress(
        mSelector: kAudioObjectPropertyName,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain
    )
    var name: Unmanaged<CFString>?
    var size = UInt32(MemoryLayout<Unmanaged<CFString>?>.size)
    let status = AudioObjectGetPropertyData(deviceID, &address, 0, nil, &size, &name)
    guard status == noErr, let cfName = name?.takeRetainedValue() else { return nil }
    return cfName as String
}

private func findInputDevice(named target: String) -> AudioDeviceID? {
    var address = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyDevices,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain
    )
    var size: UInt32 = 0
    AudioObjectGetPropertyDataSize(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size)
    let count = Int(size) / MemoryLayout<AudioDeviceID>.size
    var devices = [AudioDeviceID](repeating: 0, count: count)
    AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size, &devices)

    for device in devices {
        guard getDeviceName(device) == target else { continue }
        var inputAddress = AudioObjectPropertyAddress(
            mSelector: kAudioDevicePropertyStreamConfiguration,
            mScope: kAudioDevicePropertyScopeInput,
            mElement: kAudioObjectPropertyElementMain
        )
        var bufSize: UInt32 = 0
        AudioObjectGetPropertyDataSize(device, &inputAddress, 0, nil, &bufSize)
        if bufSize > 0 { return device }
    }
    return nil
}

private func setDefaultInputDevice(_ deviceID: AudioDeviceID) {
    var id = deviceID
    var address = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyDefaultInputDevice,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain
    )
    AudioObjectSetPropertyData(
        AudioObjectID(kAudioObjectSystemObject), &address, 0, nil,
        UInt32(MemoryLayout<AudioDeviceID>.size), &id
    )
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
