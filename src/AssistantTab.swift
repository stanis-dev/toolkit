import SwiftUI
import WebKit

struct AssistantTabView: View {
    @ObservedObject var assistantState: AssistantState

    var body: some View {
        VStack(spacing: 0) {
            AssistantSessionToolbar(assistantState: assistantState)
            Divider()

            ZStack {
                if assistantState.phase == .unavailable {
                    AssistantUnavailableView(assistantState: assistantState)
                } else {
                    AssistantWebContainer(webView: assistantState.webView)

                    if assistantState.phase == .loading {
                        ZStack {
                            Color(nsColor: .windowBackgroundColor).opacity(0.92)
                            ProgressView("Connecting to OpenCode…")
                                .controlSize(.regular)
                        }
                    }
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

private struct AssistantSessionToolbar: View {
    @ObservedObject var assistantState: AssistantState

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack(spacing: 8) {
                TextField("Paste OpenCode session URL or session ID", text: $assistantState.sessionInput)
                    .textFieldStyle(.plain)
                    .font(.system(size: 12))
                    .padding(.horizontal, 8)
                    .padding(.vertical, 6)
                    .background(Color.primary.opacity(0.06), in: RoundedRectangle(cornerRadius: 6))
                    .onSubmit {
                        assistantState.openSessionInput()
                    }
                    .onChange(of: assistantState.sessionInput) { _, _ in
                        assistantState.clearSessionError()
                    }

                Button(assistantState.isResolvingSession ? "Opening…" : "Open") {
                    assistantState.openSessionInput()
                }
                .buttonStyle(NoFocusButtonStyle())
                .disabled(assistantState.isResolvingSession)

                Button("Reset") {
                    assistantState.resetSessionTarget()
                }
                .buttonStyle(NoFocusButtonStyle())
                .disabled(!assistantState.hasSavedTarget && assistantState.sessionInput.isEmpty)
            }

            if let error = assistantState.sessionError, !error.isEmpty {
                Text(error)
                    .font(.system(size: 11))
                    .foregroundStyle(.tertiary)
                    .lineLimit(2)
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
    }
}

private struct AssistantUnavailableView: View {
    @ObservedObject var assistantState: AssistantState

    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: "globe")
                .font(.system(size: 26))
                .foregroundStyle(.secondary)

            Text("OpenCode isn't running")
                .font(.system(size: 15, weight: .medium))

            Text("Start it in a terminal, then reload this tab.")
                .font(.system(size: 12))
                .foregroundStyle(.secondary)

            Text(verbatim: kAssistantOpenCodeLaunchCommand)
                .font(.system(size: 11, design: .monospaced))
                .textSelection(.enabled)
                .padding(.horizontal, 12)
                .padding(.vertical, 10)
                .background(Color.primary.opacity(0.06), in: RoundedRectangle(cornerRadius: 8))

            if assistantState.failureMessage != "OpenCode isn't running." {
                Text(assistantState.failureMessage)
                    .font(.system(size: 11))
                    .foregroundStyle(.tertiary)
                    .multilineTextAlignment(.center)
                    .frame(maxWidth: 380)
            }

            Button("Reload") {
                assistantState.reload()
            }
            .buttonStyle(NoFocusButtonStyle())
            .padding(.top, 4)
        }
        .padding(24)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

private struct AssistantWebContainer: NSViewRepresentable {
    let webView: WKWebView

    func makeNSView(context: Context) -> NSView {
        let container = NSView()
        attachWebView(to: container)
        return container
    }

    func updateNSView(_ nsView: NSView, context: Context) {
        attachWebView(to: nsView)
    }

    private func attachWebView(to container: NSView) {
        guard webView.superview !== container else { return }
        webView.removeFromSuperview()
        webView.translatesAutoresizingMaskIntoConstraints = false
        container.addSubview(webView)
        NSLayoutConstraint.activate([
            webView.leadingAnchor.constraint(equalTo: container.leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: container.trailingAnchor),
            webView.topAnchor.constraint(equalTo: container.topAnchor),
            webView.bottomAnchor.constraint(equalTo: container.bottomAnchor),
        ])
    }
}
