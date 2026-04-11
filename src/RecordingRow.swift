import SwiftUI

struct RecordingRow: View {
    let recording: Recording
    @ObservedObject var listState: RecordingListState
    @ObservedObject var appState: AppState
    @ObservedObject var playback: PlaybackState

    @State private var isDragging = false
    @State private var dragProgress: Double = 0
    private var isActive: Bool { playback.playingId == recording.id }
    private var isDeleting: Bool { listState.deletingId == recording.id }

    var body: some View {
        VStack(spacing: 0) {
            ZStack(alignment: .trailing) {
                HStack(spacing: 8) {
                    Spacer()
                    Text("Sure?")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(.secondary)
                    Button(action: { withAnimation { listState.delete(id: recording.id) } }) {
                        Image(systemName: "checkmark")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundStyle(.green)
                    }
                    .buttonStyle(NoFocusButtonStyle())
                    Button(action: { withAnimation { listState.deletingId = nil } }) {
                        Image(systemName: "xmark")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundStyle(.red)
                    }
                    .buttonStyle(NoFocusButtonStyle())
                }
                .padding(.trailing, 12)

                HStack(spacing: 8) {
                    Text(recording.displayName)
                        .font(.system(size: 12))
                        .lineLimit(1)
                    Spacer()
                    Text(recording.durationString)
                        .font(.system(size: 11, design: .monospaced))
                        .foregroundStyle(.secondary)

                    HoverIconButton(
                        isActive && playback.isPlaying ? "pause.fill" : "play.fill",
                        color: isActive ? .primary : .secondary
                    ) { playback.toggle(recording: recording) }

                    if recording.transcribing {
                        HStack(spacing: 4) {
                            ProgressView().controlSize(.mini)
                            if !recording.transcribeStatus.isEmpty {
                                Text(recording.transcribeStatus)
                                    .font(.system(size: 10))
                                    .foregroundStyle(.secondary)
                            }
                        }
                    } else if recording.hasTranscript {
                        HoverIconButton("doc.text", color: .green) {
                            withAnimation(.easeInOut(duration: 0.2)) { appState.viewingTranscriptId = recording.id }
                        }
                    } else {
                        HoverIconButton("text.bubble") { listState.transcribe(id: recording.id) }
                    }

                    HoverIconButton("trash") { withAnimation { listState.deletingId = recording.id } }
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .background(Color(nsColor: .windowBackgroundColor))
                .offset(x: isDeleting ? -100 : 0)
            }
            .frame(height: 36)
            .clipped()
            .animation(.easeInOut(duration: 0.2), value: isDeleting)

            if isActive {
                HStack(spacing: 6) {
                    Text(formatDuration(playback.currentTime))
                        .font(.system(size: 9, design: .monospaced))
                        .foregroundStyle(.secondary)
                        .frame(width: 30, alignment: .trailing)
                    Slider(
                        value: Binding(
                            get: { isDragging ? dragProgress : playback.progress },
                            set: { dragProgress = $0 }
                        ),
                        in: 0...1,
                        onEditingChanged: { editing in
                            isDragging = editing
                            if !editing { playback.seek(to: dragProgress) }
                        }
                    )
                    .controlSize(.mini)
                    Text(formatDuration(recording.duration))
                        .font(.system(size: 9, design: .monospaced))
                        .foregroundStyle(.secondary)
                        .frame(width: 30, alignment: .leading)
                }
                .padding(.horizontal, 12)
                .padding(.bottom, 6)
            }
        }
    }
}
