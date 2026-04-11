import SwiftUI

struct AppRootView: View {
    @ObservedObject var appState: AppState
    @ObservedObject var recState: RecordingState
    @ObservedObject var listState: RecordingListState
    @ObservedObject var playback: PlaybackState
    @ObservedObject var assistantState: AssistantState
    @ObservedObject var chatSync: ChatSyncRunner
    @ObservedObject var chatAutoRefresh: ChatAutoRefreshCoordinator

    var body: some View {
        HStack(spacing: 0) {
            VStack(alignment: .leading, spacing: 2) {
                SidebarItem(title: "Assistant", icon: "sparkles", tab: .assistant, selected: $appState.selectedTab)
                SidebarItem(title: "Recorder", icon: "waveform", tab: .recorder, selected: $appState.selectedTab)
                SidebarItem(title: "Dictator", icon: "mic.badge.plus", tab: .dictator, selected: $appState.selectedTab)
                SidebarItem(title: "macOS", icon: "desktopcomputer", tab: .macos, selected: $appState.selectedTab)
                Spacer()
                Divider().padding(.horizontal, 8)
                SidebarItem(title: "Settings", icon: "gear", tab: .settings, selected: $appState.selectedTab)
                SidebarItem(title: "Logs", icon: "doc.text.magnifyingglass", tab: .logs, selected: $appState.selectedTab)
            }
            .padding(.vertical, 8)
            .frame(width: 160)
            .frame(maxHeight: .infinity)
            .background(.windowBackground)

            Divider()

            GeometryReader { geo in
                Group {
                    switch appState.selectedTab {
                    case .assistant:
                        AssistantTabView(assistantState: assistantState)
                    case .recorder:
                        RecorderTabView(recState: recState, appState: appState, listState: listState, playback: playback)
                    case .dictator:
                        DictatorTabView()
                    case .macos:
                        MacOSTabView(exporter: chatSync, autoRefresh: chatAutoRefresh)
                    case .settings:
                        SettingsTabView()
                    case .logs:
                        LogsTabView()
                    }
                }
                .frame(width: geo.size.width, height: geo.size.height)
                .clipped()
            }
        }
        .focusEffectDisabled()
        .focusable(false)
    }
}

struct SidebarItem: View {
    let title: String
    let icon: String
    let tab: Tab
    @Binding var selected: Tab
    @State private var hovering = false

    var body: some View {
        Button(action: { selected = tab }) {
            HStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.system(size: 14))
                    .frame(width: 20)
                Text(title)
                    .font(.system(size: 13))
                Spacer()
            }
            .foregroundStyle(selected == tab ? .primary : .secondary)
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .contentShape(Rectangle())
            .background(
                selected == tab
                    ? Color.accentColor.opacity(0.15)
                    : (hovering ? Color.primary.opacity(0.05) : .clear),
                in: RoundedRectangle(cornerRadius: 6)
            )
        }
        .buttonStyle(NoFocusButtonStyle())
        .onHover { hovering = $0 }
        .padding(.horizontal, 8)
    }
}

struct NoFocusButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .opacity(configuration.isPressed ? 0.7 : 1.0)
            .focusable(false)
    }
}

struct HoverIconButton: View {
    let icon: String
    let color: Color
    let size: CGFloat
    let action: () -> Void
    @State private var hovering = false

    init(_ icon: String, color: Color = .secondary, size: CGFloat = 11, action: @escaping () -> Void) {
        self.icon = icon
        self.color = color
        self.size = size
        self.action = action
    }

    var body: some View {
        Button(action: action) {
            Image(systemName: icon)
                .font(.system(size: size))
                .foregroundStyle(hovering ? .primary : color)
                .frame(width: 24, height: 24)
                .contentShape(Rectangle())
                .background(hovering ? Color.primary.opacity(0.06) : .clear, in: RoundedRectangle(cornerRadius: 4))
        }
        .buttonStyle(NoFocusButtonStyle())
        .onHover { hovering = $0 }
    }
}

struct RecorderTabView: View {
    @ObservedObject var recState: RecordingState
    @ObservedObject var appState: AppState
    @ObservedObject var listState: RecordingListState
    @ObservedObject var playback: PlaybackState

    var body: some View {
        VStack(spacing: 0) {
            RecordingControls(recState: recState)
            Divider()

            if let tid = appState.viewingTranscriptId,
               let rec = listState.recordings.first(where: { $0.id == tid }) {
                TranscriptView(recording: rec, listState: listState, appState: appState, playback: playback)
            } else if listState.recordings.isEmpty {
                Spacer()
                Text("No recordings")
                    .font(.system(size: 13))
                    .foregroundStyle(.secondary)
                Spacer()
            } else {
                ScrollView {
                    LazyVStack(spacing: 0) {
                        ForEach(listState.recordings) { rec in
                            RecordingRow(recording: rec, listState: listState, appState: appState, playback: playback)
                            if rec.id != listState.recordings.last?.id {
                                Divider().padding(.horizontal, 12)
                            }
                        }
                    }
                }
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .focusEffectDisabled()
        .contentShape(Rectangle())
        .onTapGesture {
            if listState.deletingId != nil { withAnimation { listState.deletingId = nil } }
        }
        .onChange(of: recState.isRecording) { _, isRec in
            if isRec { playback.stop() }
            else { listState.refresh() }
        }
    }
}

struct RecordingControls: View {
    @ObservedObject var recState: RecordingState
    @State private var pulsing = false

    var body: some View {
        HStack(spacing: 10) {
            Button(action: {
                if recState.isRecording { recState.stopRecording() } else { recState.startRecording() }
            }) {
                Circle()
                    .fill(recState.isRecording ? .red : .green)
                    .frame(width: 12, height: 12)
                    .opacity(recState.isRecording && !recState.isPaused && pulsing ? 0.3 : 1.0)
                    .animation(
                        recState.isRecording && !recState.isPaused
                            ? .easeInOut(duration: 1).repeatForever(autoreverses: true)
                            : .default,
                        value: pulsing
                    )
                    .onChange(of: recState.isRecording) { _, rec in pulsing = rec }
                    .onChange(of: recState.isPaused) { _, p in pulsing = !p && recState.isRecording }
            }
            .buttonStyle(NoFocusButtonStyle())

            if recState.isRecording {
                Button(action: { recState.togglePause() }) {
                    Image(systemName: recState.isPaused ? "play.fill" : "pause.fill")
                        .font(.system(size: 10))
                        .foregroundStyle(.secondary)
                }
                .buttonStyle(NoFocusButtonStyle())

                Text(recState.formattedTime)
                    .font(.system(size: 14, weight: .medium, design: .monospaced))
                    .foregroundStyle(recState.isPaused ? .secondary : .primary)
            } else {
                Text("Ready to record")
                    .font(.system(size: 13))
                    .foregroundStyle(.secondary)
            }

            Spacer()
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 10)
    }
}
