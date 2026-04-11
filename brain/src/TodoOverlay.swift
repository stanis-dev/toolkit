import AppKit
import Combine
import Darwin
import Foundation
import SwiftUI

extension Notification.Name {
    static let brainToggleTodoOverlay = Notification.Name("brain.toggleTodoOverlay")
}

final class TodoOverlayState: ObservableObject {
    @Published var rawText = ""
    @Published private(set) var statusText = "Saved"
    @Published fileprivate var focusRequestID = UUID()

    private let fileURL = URL(fileURLWithPath: kAssistantTodoFile)
    private var saveWorkItem: DispatchWorkItem?
    private var fileWatcher: DispatchSourceFileSystemObject?
    private var isApplyingExternalChange = false
    private var lastKnownDiskText = ""
    private var lastSelfWriteAt: Date?
    private var cancellables = Set<AnyCancellable>()

    init() {
        ensureFileExists()
        loadFromDisk(markStatus: "Saved")
        observeEdits()
        startWatchingFile()
    }

    deinit {
        saveWorkItem?.cancel()
        fileWatcher?.cancel()
    }

    func requestEditorFocus() {
        focusRequestID = UUID()
    }

    private func observeEdits() {
        $rawText
            .dropFirst()
            .sink { [weak self] _ in
                self?.handleTextChanged()
            }
            .store(in: &cancellables)
    }

    private func handleTextChanged() {
        guard !isApplyingExternalChange else { return }

        if rawText == lastKnownDiskText {
            saveWorkItem?.cancel()
            saveWorkItem = nil
            statusText = "Saved"
            return
        }

        statusText = "Unsaved"
        scheduleSave()
    }

    private func scheduleSave() {
        saveWorkItem?.cancel()
        let snapshot = rawText
        let workItem = DispatchWorkItem { [weak self] in
            self?.persist(snapshot)
        }
        saveWorkItem = workItem
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.4, execute: workItem)
    }

    private func persist(_ text: String) {
        guard text != lastKnownDiskText else {
            statusText = "Saved"
            return
        }

        statusText = "Saving..."

        do {
            try text.write(to: fileURL, atomically: true, encoding: .utf8)
            lastKnownDiskText = text
            lastSelfWriteAt = Date()
            statusText = rawText == text ? "Saved" : "Unsaved"
            startWatchingFile()
        } catch {
            log("todo: failed to save \(fileURL.path) - \(error)")
            statusText = "Save failed"
        }
    }

    private func ensureFileExists() {
        do {
            try FileManager.default.createDirectory(
                at: fileURL.deletingLastPathComponent(),
                withIntermediateDirectories: true,
                attributes: nil
            )
        } catch {
            log("todo: failed to create directory for \(fileURL.path) - \(error)")
        }

        guard !FileManager.default.fileExists(atPath: fileURL.path) else { return }

        if !FileManager.default.createFile(atPath: fileURL.path, contents: Data()) {
            log("todo: failed to create \(fileURL.path)")
        }
    }

    private func loadFromDisk(markStatus: String? = nil) {
        let diskText = (try? String(contentsOf: fileURL, encoding: .utf8)) ?? ""

        if diskText == lastKnownDiskText {
            if let lastSelfWriteAt, Date().timeIntervalSince(lastSelfWriteAt) < 1.0 {
                return
            }
            if let markStatus {
                statusText = markStatus
            }
            return
        }

        saveWorkItem?.cancel()
        saveWorkItem = nil
        lastKnownDiskText = diskText
        isApplyingExternalChange = true
        rawText = diskText
        isApplyingExternalChange = false
        statusText = markStatus ?? "Reloaded"
    }

    private func startWatchingFile() {
        fileWatcher?.cancel()
        fileWatcher = nil

        let fd = open(fileURL.path, O_EVTONLY)
        guard fd >= 0 else {
            log("todo: failed to watch \(fileURL.path)")
            return
        }

        let source = DispatchSource.makeFileSystemObjectSource(
            fileDescriptor: fd,
            eventMask: [.write, .delete, .rename, .attrib, .extend],
            queue: .main
        )

        source.setEventHandler { [weak self, weak source] in
            guard let self, let source else { return }
            let flags = source.data
            self.loadFromDisk()

            if flags.contains(.delete) || flags.contains(.rename) {
                self.startWatchingFile()
            }
        }

        source.setCancelHandler {
            close(fd)
        }

        fileWatcher = source
        source.resume()
    }
}

final class TodoOverlayPanel: NSPanel {
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { true }

    init() {
        super.init(
            contentRect: NSRect(x: 0, y: 0, width: 380, height: 320),
            styleMask: [.titled, .closable, .resizable, .fullSizeContentView, .utilityWindow],
            backing: .buffered,
            defer: false
        )

        title = "TODO"
        titlebarAppearsTransparent = true
        isFloatingPanel = true
        level = .floating
        collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
        isReleasedWhenClosed = false
        hidesOnDeactivate = false
        contentMinSize = NSSize(width: 320, height: 220)
        setFrameAutosaveName("BrainTodoOverlay")
    }
}

struct TodoOverlayView: View {
    @ObservedObject var state: TodoOverlayState
    @FocusState private var isEditorFocused: Bool

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Text("TODO")
                    .font(.system(size: 13, weight: .medium))
                Spacer()
                Text(state.statusText)
                    .font(.system(size: 11))
                    .foregroundStyle(.secondary)
            }
            .padding(.horizontal, 14)
            .padding(.vertical, 10)

            Divider()

            TextEditor(text: $state.rawText)
                .font(.system(size: 13))
                .focused($isEditorFocused)
                .padding(10)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color(nsColor: .windowBackgroundColor))
        .onAppear {
            isEditorFocused = true
        }
        .onChange(of: state.focusRequestID) { _, _ in
            isEditorFocused = true
        }
    }
}
