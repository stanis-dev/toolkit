import SwiftUI
import AppKit

struct DictatorTabView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text("Dictator")
                .font(.system(size: 15, weight: .semibold))
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
            Divider()

            VStack(alignment: .leading, spacing: 16) {
                VStack(alignment: .leading, spacing: 4) {
                    Text("Voice-to-clipboard dictation")
                        .font(.system(size: 13))
                    Text("Press **Shift+Option+Ctrl+Cmd+D** anywhere to toggle dictation. The transcription is copied to your clipboard.")
                        .font(.system(size: 12))
                        .foregroundStyle(.secondary)
                        .fixedSize(horizontal: false, vertical: true)
                }

                VStack(alignment: .leading, spacing: 4) {
                    Text("Model")
                        .font(.system(size: 12, weight: .medium))
                        .foregroundStyle(.secondary)
                    Text("parakeet-tdt-0.6b-v3 (25 langs, 0.6B params)")
                        .font(.system(size: 12))
                }

                VStack(alignment: .leading, spacing: 4) {
                    Text("Note")
                        .font(.system(size: 12, weight: .medium))
                        .foregroundStyle(.secondary)
                    Text("Requires Accessibility permission for the global hotkey. Grant in System Settings > Privacy & Security > Accessibility.")
                        .font(.system(size: 12))
                        .foregroundStyle(.secondary)
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
    }
}

class DictatorPanel: NSPanel {
    init() {
        super.init(
            contentRect: NSRect(x: 0, y: 0, width: 160, height: 60),
            styleMask: [.nonactivatingPanel],
            backing: .buffered,
            defer: false
        )
        level = .floating
        isFloatingPanel = true
        collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
        isReleasedWhenClosed = false
        backgroundColor = .clear
        isOpaque = false
        hasShadow = false
    }

    func showBottomLeft() {
        if let screen = NSScreen.main {
            let sf = screen.visibleFrame
            let x = sf.origin.x + 16
            let y = sf.origin.y + 16
            setFrameOrigin(NSPoint(x: x, y: y))
        }
        orderFront(nil)
    }
}

struct DictatorOverlayView: View {
    @ObservedObject var state: DictatorState

    var body: some View {
        HStack(spacing: 10) {
            if state.status == .recording {
                let dotScale = (10 + 6 * state.audioLevel) / 16
                ZStack {
                    Circle().fill(.primary.opacity(0.35))
                    Circle().fill(Color.red.opacity(0.7))
                        .scaleEffect(max(0.001, state.audioLevel))
                }
                .frame(width: 16, height: 16)
                .scaleEffect(dotScale)
                .animation(.easeOut(duration: 0.08), value: state.audioLevel)
                Text("Dictating...")
                    .font(.system(size: 13, weight: .medium))
            } else if state.status == .transcribing {
                ProgressView()
                    .controlSize(.small)
                Text("Transcribing...")
                    .font(.system(size: 13, weight: .medium))
                    .foregroundStyle(.secondary)
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        .frame(width: 160)
        .background(.thickMaterial, in: RoundedRectangle(cornerRadius: 12))
        .overlay(RoundedRectangle(cornerRadius: 12).stroke(.primary.opacity(0.2), lineWidth: 1.5))
        .shadow(color: .black.opacity(0.2), radius: 10, y: 4)
        .padding(8)
    }
}
