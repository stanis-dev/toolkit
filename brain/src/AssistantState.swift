import AppKit
import Combine
import Foundation
import WebKit

enum AssistantPhase: Equatable {
    case loading
    case ready
    case unavailable
}

struct AssistantSessionTarget: Codable, Equatable {
    let sessionID: String
    let directory: String

    var url: URL {
        kAssistantOpenCodeURL
            .appendingPathComponent(Self.encodeDirectorySlug(directory))
            .appendingPathComponent("session")
            .appendingPathComponent(sessionID)
    }

    static func encodeDirectorySlug(_ directory: String) -> String {
        Data(directory.utf8)
            .base64EncodedString()
            .replacingOccurrences(of: "+", with: "-")
            .replacingOccurrences(of: "/", with: "_")
            .replacingOccurrences(of: "=", with: "")
    }

    static func decodeDirectorySlug(_ slug: String) -> String? {
        let remainder = slug.count % 4
        let padding = remainder == 0 ? "" : String(repeating: "=", count: 4 - remainder)
        let value = slug
            .replacingOccurrences(of: "-", with: "+")
            .replacingOccurrences(of: "_", with: "/") + padding
        guard let data = Data(base64Encoded: value) else { return nil }
        return String(data: data, encoding: .utf8)
    }
}

private struct AssistantSessionLookupResponse: Decodable {
    let id: String
    let directory: String
}

private enum AssistantSessionInput {
    case sessionID(String)
    case localURL(URL)
}

private enum AssistantSessionResolutionError: LocalizedError {
    case emptyInput
    case invalidSessionURL
    case unsupportedShareURL
    case unsupportedExternalURL
    case invalidSessionID
    case sessionNotFound
    case serverUnavailable
    case requestFailed(String)

    var errorDescription: String? {
        switch self {
        case .emptyInput:
            return "Paste a local OpenCode session URL or a raw session ID."
        case .invalidSessionURL:
            return "That URL isn't a valid OpenCode session link."
        case .unsupportedShareURL:
            return "Share URLs aren't supported here yet."
        case .unsupportedExternalURL:
            return "Only local OpenCode URLs from 127.0.0.1:4096 or localhost:4096 are supported."
        case .invalidSessionID:
            return "That doesn't look like a valid OpenCode session ID."
        case .sessionNotFound:
            return "That session wasn't found on the current OpenCode server."
        case .serverUnavailable:
            return "OpenCode isn't running at \(kAssistantOpenCodeURL.absoluteString)."
        case .requestFailed(let message):
            return message
        }
    }
}

class AssistantState: NSObject, ObservableObject {
    @Published private(set) var phase: AssistantPhase = .loading
    @Published private(set) var failureMessage = "OpenCode isn't running."
    @Published var sessionInput = ""
    @Published private(set) var sessionError: String?
    @Published private(set) var isResolvingSession = false
    @Published private(set) var activeTarget: AssistantSessionTarget?

    let webView: WKWebView

    private let navigationProxy = AssistantNavigationProxy()
    private var resolveTask: Task<Void, Never>?

    var hasSavedTarget: Bool {
        activeTarget != nil
    }

    override init() {
        let configuration = WKWebViewConfiguration()
        configuration.defaultWebpagePreferences.allowsContentJavaScript = true
        webView = WKWebView(frame: .zero, configuration: configuration)
        let persistedTarget = Self.loadPersistedTarget()
        activeTarget = persistedTarget
        sessionInput = persistedTarget?.sessionID ?? ""
        super.init()

        navigationProxy.owner = self
        webView.navigationDelegate = navigationProxy
        webView.uiDelegate = navigationProxy
        reload()
    }

    deinit {
        resolveTask?.cancel()
    }

    func reload() {
        sessionError = nil
        load(url: activeTarget?.url ?? kAssistantOpenCodeURL)
    }

    func openSessionInput() {
        let raw = sessionInput.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !raw.isEmpty else {
            sessionError = AssistantSessionResolutionError.emptyInput.errorDescription
            return
        }

        sessionError = nil
        isResolvingSession = true
        resolveTask?.cancel()

        resolveTask = Task { [weak self] in
            guard let self else { return }
            do {
                let input = try Self.parseSessionInput(raw)
                let target = try await Self.resolveCanonicalTarget(from: input)
                guard !Task.isCancelled else { return }
                await MainActor.run {
                    self.isResolvingSession = false
                    self.applyResolvedTarget(target, loadImmediately: true)
                }
            } catch {
                guard !Task.isCancelled else { return }
                let message = Self.errorMessage(from: error)
                await MainActor.run {
                    self.isResolvingSession = false
                    self.sessionError = message
                }
            }
        }
    }

    func resetSessionTarget() {
        resolveTask?.cancel()
        isResolvingSession = false
        sessionError = nil
        activeTarget = nil
        sessionInput = ""
        Self.persistTarget(nil)
        load(url: kAssistantOpenCodeURL)
    }

    func clearSessionError() {
        sessionError = nil
    }

    fileprivate func didStartNavigation(to url: URL?) {
        guard isEmbeddedURL(url) else { return }
        phase = .loading
    }

    fileprivate func didFinishNavigation(to url: URL?) {
        guard isEmbeddedURL(url) else { return }
        phase = .ready
        log("assistant: OpenCode web UI ready")
        trackSessionFromNavigation(url)
    }

    fileprivate func didFailNavigation(_ error: Error) {
        let nsError = error as NSError
        failureMessage = unavailableMessage(for: nsError)
        phase = .unavailable
        log("assistant: failed to load OpenCode web UI — \(nsError.localizedDescription)")
    }

    fileprivate func openExternal(_ url: URL) {
        log("assistant: opening external URL \(url.absoluteString)")
        NSWorkspace.shared.open(url)
    }

    fileprivate func isEmbeddedURL(_ url: URL?) -> Bool {
        guard let url else { return false }
        if url.scheme == "about" { return true }
        guard let host = url.host?.lowercased(), let port = url.port else { return false }
        return (host == "127.0.0.1" || host == "localhost") && port == 4096
    }

    private func load(url: URL) {
        phase = .loading
        failureMessage = "OpenCode isn't running."
        log("assistant: loading OpenCode web UI at \(url.absoluteString)")
        let request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: 5)
        webView.load(request)
    }

    private func applyResolvedTarget(_ target: AssistantSessionTarget, loadImmediately: Bool) {
        activeTarget = target
        sessionInput = target.sessionID
        sessionError = nil
        Self.persistTarget(target)
        if loadImmediately {
            load(url: target.url)
        }
    }

    private func trackSessionFromNavigation(_ url: URL?) {
        guard let url, let sessionID = Self.sessionID(from: url) else { return }
        if activeTarget?.sessionID == sessionID { return }

        Task { [weak self] in
            guard let self else { return }
            do {
                let target = try await Self.fetchSessionTarget(sessionID: sessionID)
                await MainActor.run {
                    self.applyResolvedTarget(target, loadImmediately: false)
                }
            } catch {
                log("assistant: failed to track session \(sessionID) — \(Self.errorMessage(from: error))")
            }
        }
    }

    private func unavailableMessage(for error: NSError) -> String {
        guard error.domain == NSURLErrorDomain else {
            return "OpenCode failed to load: \(error.localizedDescription)"
        }

        switch error.code {
        case NSURLErrorCannotConnectToHost,
             NSURLErrorCannotFindHost,
             NSURLErrorTimedOut,
             NSURLErrorNetworkConnectionLost,
             NSURLErrorNotConnectedToInternet:
            return "OpenCode isn't running at \(kAssistantOpenCodeURL.absoluteString)."
        default:
            return "OpenCode failed to load: \(error.localizedDescription)"
        }
    }

    private static func parseSessionInput(_ raw: String) throws -> AssistantSessionInput {
        if let url = URL(string: raw), let scheme = url.scheme?.lowercased(), !scheme.isEmpty {
            if let host = url.host?.lowercased(), host == "opncd.ai" || host.hasSuffix(".opncd.ai") {
                throw AssistantSessionResolutionError.unsupportedShareURL
            }
            return .localURL(url)
        }
        return .sessionID(raw)
    }

    private static func resolveCanonicalTarget(from input: AssistantSessionInput) async throws -> AssistantSessionTarget {
        switch input {
        case .sessionID(let value):
            return try await fetchSessionTarget(sessionID: value)
        case .localURL(let url):
            let sessionID = try parseLocalSessionURL(url)
            return try await fetchSessionTarget(sessionID: sessionID)
        }
    }

    private static func parseLocalSessionURL(_ url: URL) throws -> String {
        guard isSupportedLocalURL(url) else {
            throw AssistantSessionResolutionError.unsupportedExternalURL
        }

        let components = url.path.split(separator: "/").map(String.init)
        guard components.count >= 3,
              !components[0].isEmpty,
              components[1] == "session",
              !components[2].isEmpty
        else {
            throw AssistantSessionResolutionError.invalidSessionURL
        }

        guard AssistantSessionTarget.decodeDirectorySlug(components[0]) != nil else {
            throw AssistantSessionResolutionError.invalidSessionURL
        }

        return components[2]
    }

    private static func sessionID(from url: URL) -> String? {
        guard isSupportedLocalURL(url) else { return nil }
        let components = url.path.split(separator: "/").map(String.init)
        guard components.count >= 3, components[1] == "session", !components[2].isEmpty else { return nil }
        return components[2]
    }

    private static func isSupportedLocalURL(_ url: URL) -> Bool {
        guard let host = url.host?.lowercased(), let port = url.port else { return false }
        return (host == "127.0.0.1" || host == "localhost") && port == 4096
    }

    private static func fetchSessionTarget(sessionID: String) async throws -> AssistantSessionTarget {
        let url = kAssistantOpenCodeURL
            .appendingPathComponent("session")
            .appendingPathComponent(sessionID)
        var request = URLRequest(url: url)
        request.timeoutInterval = 5

        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse else {
                throw AssistantSessionResolutionError.requestFailed("OpenCode returned an invalid response.")
            }

            switch http.statusCode {
            case 200:
                let session = try JSONDecoder().decode(AssistantSessionLookupResponse.self, from: data)
                return AssistantSessionTarget(sessionID: session.id, directory: session.directory)
            case 400:
                throw AssistantSessionResolutionError.invalidSessionID
            case 404:
                throw AssistantSessionResolutionError.sessionNotFound
            default:
                throw AssistantSessionResolutionError.requestFailed("OpenCode returned HTTP \(http.statusCode).")
            }
        } catch let error as AssistantSessionResolutionError {
            throw error
        } catch let error as DecodingError {
            throw AssistantSessionResolutionError.requestFailed("OpenCode returned malformed session data: \(error.localizedDescription)")
        } catch let error as URLError {
            switch error.code {
            case .cannotConnectToHost, .cannotFindHost, .timedOut, .networkConnectionLost, .notConnectedToInternet:
                throw AssistantSessionResolutionError.serverUnavailable
            default:
                throw AssistantSessionResolutionError.requestFailed("OpenCode request failed: \(error.localizedDescription)")
            }
        } catch {
            throw AssistantSessionResolutionError.requestFailed("OpenCode request failed: \(error.localizedDescription)")
        }
    }

    private static func persistTarget(_ target: AssistantSessionTarget?) {
        if let target, let data = try? JSONEncoder().encode(target) {
            UserDefaults.standard.set(data, forKey: kAssistantOpenCodeLastTargetDefaultsKey)
        } else {
            UserDefaults.standard.removeObject(forKey: kAssistantOpenCodeLastTargetDefaultsKey)
        }
    }

    private static func loadPersistedTarget() -> AssistantSessionTarget? {
        guard let data = UserDefaults.standard.data(forKey: kAssistantOpenCodeLastTargetDefaultsKey) else { return nil }
        return try? JSONDecoder().decode(AssistantSessionTarget.self, from: data)
    }

    private static func errorMessage(from error: Error) -> String {
        if let resolution = error as? AssistantSessionResolutionError {
            return resolution.errorDescription ?? "Failed to resolve that OpenCode session."
        }
        if let localized = error as? LocalizedError, let description = localized.errorDescription {
            return description
        }
        return error.localizedDescription
    }
}

private final class AssistantNavigationProxy: NSObject, WKNavigationDelegate, WKUIDelegate {
    weak var owner: AssistantState?

    func webView(
        _ webView: WKWebView,
        decidePolicyFor navigationAction: WKNavigationAction,
        decisionHandler: @escaping (WKNavigationActionPolicy) -> Void
    ) {
        guard let owner, let url = navigationAction.request.url else {
            decisionHandler(.allow)
            return
        }

        if navigationAction.targetFrame?.isMainFrame == false {
            decisionHandler(.allow)
            return
        }

        if owner.isEmbeddedURL(url) {
            decisionHandler(.allow)
            return
        }

        owner.openExternal(url)
        decisionHandler(.cancel)
    }

    func webView(_ webView: WKWebView, didStartProvisionalNavigation navigation: WKNavigation!) {
        owner?.didStartNavigation(to: webView.url)
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        owner?.didFinishNavigation(to: webView.url)
    }

    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        owner?.didFailNavigation(error)
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        owner?.didFailNavigation(error)
    }

    func webViewWebContentProcessDidTerminate(_ webView: WKWebView) {
        owner?.reload()
    }

    func webView(
        _ webView: WKWebView,
        createWebViewWith configuration: WKWebViewConfiguration,
        for navigationAction: WKNavigationAction,
        windowFeatures: WKWindowFeatures
    ) -> WKWebView? {
        guard let owner, let url = navigationAction.request.url else { return nil }

        if owner.isEmbeddedURL(url) {
            webView.load(navigationAction.request)
        } else {
            owner.openExternal(url)
        }
        return nil
    }
}
