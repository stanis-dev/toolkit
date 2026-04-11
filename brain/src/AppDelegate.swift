import AppKit
import Carbon.HIToolbox
import SwiftUI
import Combine
import UserNotifications

class AppDelegate: NSObject, NSApplicationDelegate, UNUserNotificationCenterDelegate {
    let recState: RecordingState
    let appState: AppState
    let listState: RecordingListState
    let playback: PlaybackState
    let assistantState: AssistantState
    let chatSync: ChatSyncRunner
    let chatAutoRefresh: ChatAutoRefreshCoordinator
    let todoOverlayState = TodoOverlayState()
    let dictatorState = DictatorState()
    let meetingDetector = MeetingDetector()
    var window: NSWindow!
    var statusItem: NSStatusItem!
    var todoPanel: TodoOverlayPanel!
    var dictatorPanel: DictatorPanel!
    private var dictatorEventTap: CFMachPort?
    private var lastKnownBinaryModDate: Date?
    private var pendingUpdateDate: Date?
    private var updateCheckTimer: Timer?
    private var todoHotKeyRef: EventHotKeyRef?
    private var todoHotKeyHandlerRef: EventHandlerRef?
    private let todoHotKeySignature = fourCharCode("BTDO")
    private let todoHotKeyID: UInt32 = 1

    init(recState: RecordingState, appState: AppState, listState: RecordingListState,
         playback: PlaybackState, assistantState: AssistantState,
         chatSync: ChatSyncRunner, chatAutoRefresh: ChatAutoRefreshCoordinator) {
        self.recState = recState
        self.appState = appState
        self.listState = listState
        self.playback = playback
        self.assistantState = assistantState
        self.chatSync = chatSync
        self.chatAutoRefresh = chatAutoRefresh
        super.init()
    }

    func applicationDidFinishLaunching(_ notification: Notification) {
        log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        log("App: launched (pid \(ProcessInfo.processInfo.processIdentifier))")
        logStartupDiagnostics()

        listState.refresh()
        listState.playback = playback

        setupMainMenu()
        setupStatusItem()
        setupWindow()
        setupTodoPanel()
        setupDictatorPanel()
        setupGlobalHotkey()
        setupTodoHotKey()
        setupDictatorEventTap()
        setupAutoUpdate()
        setupMeetingDetector()
        chatAutoRefresh.start()
        log("App: setup complete")

        NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            guard let self = self else { return event }

            if self.dictatorState.status == .recording && event.keyCode == 36 {
                self.dictatorState.finishDictation()
                return nil
            }
            if self.dictatorState.status == .recording && event.keyCode == 53 {
                self.dictatorState.cancelDictation()
                self.dictatorPanel.orderOut(nil)
                return nil
            }

            if event.keyCode == 53 {
                if self.appState.viewingTranscriptId != nil {
                    withAnimation(.easeInOut(duration: 0.2)) { self.appState.viewingTranscriptId = nil }
                    return nil
                }
            }
            guard event.modifierFlags.contains(.command),
                  let key = event.charactersIgnoringModifiers else { return event }
            if key == "," {
                self.showWindow()
                self.appState.selectedTab = .settings
                return nil
            }
            if key == "w" {
                if self.todoPanel.isKeyWindow {
                    self.todoPanel.orderOut(nil)
                } else {
                    self.window.orderOut(nil)
                }
                return nil
            }
            if key == "q" {
                if self.recState.isRecording { self.recState.stopRecording() }
                NSApp.terminate(nil)
                return nil
            }
            return event
        }

        observeDictatorStatus()
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(toggleTodoOverlayFromMenu),
            name: .brainToggleTodoOverlay,
            object: nil
        )
    }

    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool {
        showWindow()
        return true
    }

    private func setupMainMenu() {
        let appName = "Brain"
        let mainMenu = NSMenu()

        let appMenuItem = NSMenuItem()
        mainMenu.addItem(appMenuItem)

        let appMenu = NSMenu(title: appName)
        appMenuItem.submenu = appMenu
        appMenu.addItem(withTitle: "About \(appName)", action: #selector(NSApplication.orderFrontStandardAboutPanel(_:)), keyEquivalent: "")

        let settingsItem = NSMenuItem(title: "Settings…", action: #selector(openSettingsFromMenu), keyEquivalent: ",")
        settingsItem.target = self
        appMenu.addItem(settingsItem)
        appMenu.addItem(.separator())

        let hideItem = NSMenuItem(title: "Hide \(appName)", action: #selector(NSApplication.hide(_:)), keyEquivalent: "h")
        hideItem.target = NSApp
        appMenu.addItem(hideItem)

        let hideOthersItem = NSMenuItem(title: "Hide Others", action: #selector(NSApplication.hideOtherApplications(_:)), keyEquivalent: "h")
        hideOthersItem.target = NSApp
        hideOthersItem.keyEquivalentModifierMask = [.command, .option]
        appMenu.addItem(hideOthersItem)

        let showAllItem = NSMenuItem(title: "Show All", action: #selector(NSApplication.unhideAllApplications(_:)), keyEquivalent: "")
        showAllItem.target = NSApp
        appMenu.addItem(showAllItem)

        appMenu.addItem(.separator())

        let quitItem = NSMenuItem(title: "Quit \(appName)", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
        quitItem.target = NSApp
        appMenu.addItem(quitItem)

        let editMenuItem = NSMenuItem()
        mainMenu.addItem(editMenuItem)

        let editMenu = NSMenu(title: "Edit")
        editMenuItem.submenu = editMenu
        addEditMenuItem(to: editMenu, title: "Cut", action: #selector(NSText.cut(_:)), keyEquivalent: "x")
        addEditMenuItem(to: editMenu, title: "Copy", action: #selector(NSText.copy(_:)), keyEquivalent: "c")
        addEditMenuItem(to: editMenu, title: "Paste", action: #selector(NSText.paste(_:)), keyEquivalent: "v")
        addEditMenuItem(to: editMenu, title: "Select All", action: #selector(NSResponder.selectAll(_:)), keyEquivalent: "a")

        let windowMenuItem = NSMenuItem()
        mainMenu.addItem(windowMenuItem)

        let windowMenu = NSMenu(title: "Window")
        windowMenuItem.submenu = windowMenu
        addWindowMenuItem(to: windowMenu, title: "Minimize", action: #selector(NSWindow.performMiniaturize(_:)), keyEquivalent: "m")
        addWindowMenuItem(to: windowMenu, title: "Zoom", action: #selector(NSWindow.performZoom(_:)), keyEquivalent: "")
        windowMenu.addItem(.separator())
        addWindowMenuItem(to: windowMenu, title: "Bring All to Front", action: #selector(NSApplication.arrangeInFront(_:)), keyEquivalent: "")

        NSApp.windowsMenu = windowMenu

        NSApp.mainMenu = mainMenu
    }

    private func addEditMenuItem(to menu: NSMenu, title: String, action: Selector, keyEquivalent: String) {
        let item = NSMenuItem(title: title, action: action, keyEquivalent: keyEquivalent)
        item.target = nil
        menu.addItem(item)
    }

    private func addWindowMenuItem(to menu: NSMenu, title: String, action: Selector, keyEquivalent: String) {
        let item = NSMenuItem(title: title, action: action, keyEquivalent: keyEquivalent)
        item.target = nil
        menu.addItem(item)
    }

    private func setupStatusItem() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        if let button = statusItem.button {
            button.image = NSImage(systemSymbolName: "brain", accessibilityDescription: "Brain")
        }
        let menu = NSMenu()
        let showItem = NSMenuItem(title: "Show Brain", action: #selector(showWindow), keyEquivalent: "")
        showItem.target = self
        menu.addItem(showItem)
        let todoItem = NSMenuItem(title: "Toggle TODO", action: #selector(toggleTodoOverlayFromMenu), keyEquivalent: "")
        todoItem.target = self
        menu.addItem(todoItem)
        menu.addItem(.separator())
        let quitItem = NSMenuItem(title: "Quit Brain", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
        quitItem.target = NSApp
        menu.addItem(quitItem)
        statusItem.menu = menu
    }

    private func setupWindow() {
        let rootView = AppRootView(
            appState: appState,
            recState: recState,
            listState: listState,
            playback: playback,
            assistantState: assistantState,
            chatSync: chatSync,
            chatAutoRefresh: chatAutoRefresh
        )
        let hosting = NSHostingView(rootView: rootView)

        window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 800, height: 500),
            styleMask: [.titled, .closable, .miniaturizable, .resizable, .fullSizeContentView],
            backing: .buffered,
            defer: false
        )
        window.title = "Brain"
        window.titlebarAppearsTransparent = true
        window.setFrameAutosaveName("Brain")
        window.contentView = hosting
        window.contentMinSize = NSSize(width: 600, height: 400)
        window.isReleasedWhenClosed = false
        window.autorecalculatesKeyViewLoop = false
        window.initialFirstResponder = nil
        window.center()
        window.makeKeyAndOrderFront(nil)
    }

    private func setupTodoPanel() {
        todoPanel = TodoOverlayPanel()
        todoPanel.contentView = NSHostingView(rootView: TodoOverlayView(state: todoOverlayState))
        todoPanel.center()
    }

    private func setupDictatorPanel() {
        dictatorPanel = DictatorPanel()
        dictatorPanel.contentView = NSHostingView(rootView: DictatorOverlayView(state: dictatorState))
    }

    private func setupGlobalHotkey() {
        func isDictatorHotkey(_ event: NSEvent) -> Bool {
            let flags = event.modifierFlags
            return flags.contains(.shift) && flags.contains(.option)
                && flags.contains(.control) && flags.contains(.command)
                && event.keyCode == 2
        }

        NSEvent.addGlobalMonitorForEvents(matching: .keyDown) { [weak self] event in
            if isDictatorHotkey(event) {
                DispatchQueue.main.async { self?.toggleDictation() }
            }
        }

        NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            if isDictatorHotkey(event) {
                self?.toggleDictation()
                return nil
            }
            return event
        }
    }

    private func setupTodoHotKey() {
        var eventType = EventTypeSpec(
            eventClass: OSType(kEventClassKeyboard),
            eventKind: OSType(kEventHotKeyPressed)
        )

        let installStatus = InstallEventHandler(
            GetApplicationEventTarget(),
            { _, event, userData in
                guard let event, let userData else { return OSStatus(eventNotHandledErr) }

                var hotKeyID = EventHotKeyID()
                let status = GetEventParameter(
                    event,
                    EventParamName(kEventParamDirectObject),
                    EventParamType(typeEventHotKeyID),
                    nil,
                    MemoryLayout<EventHotKeyID>.size,
                    nil,
                    &hotKeyID
                )
                guard status == noErr else { return status }

                let delegate = Unmanaged<AppDelegate>.fromOpaque(userData).takeUnretainedValue()
                guard hotKeyID.signature == delegate.todoHotKeySignature,
                      hotKeyID.id == delegate.todoHotKeyID else {
                    return OSStatus(eventNotHandledErr)
                }

                DispatchQueue.main.async {
                    delegate.toggleTodoOverlay()
                }
                return noErr
            },
            1,
            &eventType,
            Unmanaged.passUnretained(self).toOpaque(),
            &todoHotKeyHandlerRef
        )

        guard installStatus == noErr else {
            log("todo: failed to install hotkey handler (status \(installStatus))")
            return
        }

        let hotKeyID = EventHotKeyID(signature: todoHotKeySignature, id: todoHotKeyID)
        let registerStatus = RegisterEventHotKey(
            UInt32(kVK_ANSI_T),
            UInt32(cmdKey | optionKey | shiftKey | controlKey),
            hotKeyID,
            GetApplicationEventTarget(),
            0,
            &todoHotKeyRef
        )

        if registerStatus == noErr {
            log("todo: registered global hotkey Control+Shift+Option+Command+T")
        } else {
            log("todo: failed to register global hotkey Control+Shift+Option+Command+T (status \(registerStatus))")
        }
    }

    private func setupDictatorEventTap() {
        let callback: CGEventTapCallBack = { _, type, event, userInfo in
            if type == .tapDisabledByTimeout || type == .tapDisabledByUserInput {
                if let userInfo = userInfo {
                    let d = Unmanaged<AppDelegate>.fromOpaque(userInfo).takeUnretainedValue()
                    if let tap = d.dictatorEventTap { CGEvent.tapEnable(tap: tap, enable: true) }
                }
                return Unmanaged.passRetained(event)
            }
            guard type == .keyDown, let userInfo = userInfo else {
                return Unmanaged.passRetained(event)
            }
            let d = Unmanaged<AppDelegate>.fromOpaque(userInfo).takeUnretainedValue()
            let keyCode = event.getIntegerValueField(.keyboardEventKeycode)
            let modifiers: CGEventFlags = [.maskCommand, .maskShift, .maskAlternate, .maskControl]
            if d.dictatorState.status == .recording
                && keyCode == 35
                && event.flags.intersection(modifiers).isEmpty {
                DispatchQueue.main.async { d.dictatorState.finishDictation(andPaste: true) }
                return nil
            }
            return Unmanaged.passRetained(event)
        }

        dictatorEventTap = CGEvent.tapCreate(
            tap: .cgSessionEventTap,
            place: .headInsertEventTap,
            options: .defaultTap,
            eventsOfInterest: CGEventMask(1 << CGEventType.keyDown.rawValue),
            callback: callback,
            userInfo: Unmanaged.passUnretained(self).toOpaque()
        )
        if let tap = dictatorEventTap {
            let src = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, tap, 0)
            CFRunLoopAddSource(CFRunLoopGetCurrent(), src, .commonModes)
        }
    }

    private func toggleDictation() {
        if dictatorState.status == .recording {
            dictatorState.finishDictation()
        } else if dictatorState.status == .idle {
            dictatorState.startDictation()
            dictatorPanel.showBottomLeft()
        }
    }

    private func toggleTodoOverlay() {
        log("todo: toggle requested (visible=\(todoPanel.isVisible))")
        if todoPanel.isVisible {
            todoPanel.orderOut(nil)
        } else {
            showTodoOverlay()
        }
    }

    private func showTodoOverlay() {
        todoOverlayState.requestEditorFocus()
        todoPanel.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
        log("todo: panel shown")
    }

    @objc private func toggleTodoOverlayFromMenu() {
        toggleTodoOverlay()
    }

    private func observeDictatorStatus() {
        dictatorState.$status
            .receive(on: DispatchQueue.main)
            .sink { [weak self] status in
                guard let self = self else { return }
                if status == .idle {
                    self.dictatorPanel.orderOut(nil)
                } else if !self.dictatorPanel.isVisible {
                    self.dictatorPanel.showBottomLeft()
                }
            }
            .store(in: &cancellables)
    }

    private var cancellables = Set<AnyCancellable>()

    // MARK: - Meeting detection

    private func setupMeetingDetector() {
        meetingDetector.isSuppressed = { [weak self] in
            guard let self = self else { return false }
            return self.dictatorState.status != .idle || self.recState.isRecording
        }
        meetingDetector.onMeetingDetected = { [weak self] match in
            guard let self = self, !self.recState.isRecording else { return }
            log("App: meeting match evidence → \(match.evidenceSummary)")
            self.promptToRecord(appName: match.appName)
        }
        dictatorState.$status
            .removeDuplicates { $0 == $1 }
            .dropFirst()
            .receive(on: DispatchQueue.main)
            .sink { [weak self] status in
                guard let self = self else { return }
                switch status {
                case .recording:
                    self.meetingDetector.suppress(for: 2, reason: "dictation recording start")
                case .transcribing:
                    self.meetingDetector.suppress(for: 2, reason: "dictation transcribing")
                case .idle:
                    self.meetingDetector.suppress(for: kMeetingDictationCooldownSec, reason: "dictation cooldown")
                }
            }
            .store(in: &cancellables)
        meetingDetector.startMonitoring()
    }

    private func promptToRecord(appName: String) {
        log("App: showing meeting prompt for \(appName)")
        NSApp.activate(ignoringOtherApps: true)

        let alert = NSAlert()
        alert.messageText = "Meeting Detected"
        alert.informativeText = "\(appName) call in progress. Start recording?"
        alert.alertStyle = .informational
        alert.addButton(withTitle: "Record")
        alert.addButton(withTitle: "Dismiss")

        if alert.runModal() == .alertFirstButtonReturn {
            log("App: meeting prompt → Record")
            guard !self.recState.isRecording else {
                log("App: already recording, ignoring")
                return
            }
            self.recState.startRecording()
            self.showWindow()
            self.appState.selectedTab = .recorder
            self.listState.refresh()
        } else {
            log("App: meeting prompt → Dismiss")
        }
    }

    // MARK: - Auto-update

    private func setupAutoUpdate() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound]) { granted, error in
            log("App: notification auth → granted=\(granted)\(error.map { " error=\($0)" } ?? "")")
        }
        lastKnownBinaryModDate = binaryModificationDate()
        updateCheckTimer = Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { [weak self] _ in
            self?.checkForUpdate()
        }
    }

    private func binaryModificationDate() -> Date? {
        let path = "/Applications/Brain.app/Contents/MacOS/rec"
        return (try? FileManager.default.attributesOfItem(atPath: path))?[.modificationDate] as? Date
    }

    private func checkForUpdate() {
        guard let currentModDate = binaryModificationDate(),
              let knownDate = lastKnownBinaryModDate,
              currentModDate > knownDate else { return }

        let isNewBuild = pendingUpdateDate == nil || currentModDate > pendingUpdateDate!
        let reasons = busyReasons()

        if reasons.isEmpty {
            relaunch()
        } else {
            pendingUpdateDate = currentModDate
            if isNewBuild {
                sendUpdateBlockedNotification(reasons: reasons)
            }
        }
    }

    private func busyReasons() -> [String] {
        var reasons: [String] = []
        if recState.isRecording { reasons.append("meeting recording") }
        if dictatorState.status == .recording { reasons.append("dictation recording") }
        if dictatorState.status == .transcribing { reasons.append("dictation transcription") }
        if listState.recordings.contains(where: { $0.transcribing }) { reasons.append("transcript processing") }
        return reasons
    }

    private func sendUpdateBlockedNotification(reasons: [String]) {
        let content = UNMutableNotificationContent()
        content.title = "Brain Update Pending"
        content.body = "Couldn't restart: \(reasons.joined(separator: ", ")) in progress."
        let request = UNNotificationRequest(identifier: "brain-update-blocked", content: content, trigger: nil)
        UNUserNotificationCenter.current().add(request)
        log("Auto-update blocked: \(reasons.joined(separator: ", "))")
    }

    private func relaunch() {
        log("App: auto-update relaunching")
        let task = Process()
        task.executableURL = URL(fileURLWithPath: "/bin/sh")
        task.arguments = ["-c", "sleep 0.5 && open /Applications/Brain.app"]
        try? task.run()
        NSApp.terminate(nil)
    }

    @objc private func showWindow() {
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }

    @objc private func openSettingsFromMenu() {
        showWindow()
        appState.selectedTab = .settings
    }

    private func logStartupDiagnostics() {
        let info = ProcessInfo.processInfo
        log("App: macOS \(info.operatingSystemVersionString), uptime \(Int(info.systemUptime))s")
        log("App: outputDir=\(kOutputDir)")

        let fm = FileManager.default
        let recCount = (try? fm.contentsOfDirectory(atPath: kOutputDir))?.filter { $0.hasSuffix(".wav") }.count ?? 0
        log("App: \(recCount) recording(s) on disk")

        let meetingApps = NSWorkspace.shared.runningApplications.compactMap { app -> String? in
            guard let bid = app.bundleIdentifier else { return nil }
            if let name = kMeetingAppBundleIDs[bid] { return name }
            if kMeetingBrowserBundleIDs.contains(bid) { return app.localizedName }
            return nil
        }
        log("App: meeting-relevant apps running: \(meetingApps.isEmpty ? "none" : meetingApps.joined(separator: ", "))")
    }

    func applicationWillTerminate(_ notification: Notification) {
        NotificationCenter.default.removeObserver(self, name: .brainToggleTodoOverlay, object: nil)
        if let todoHotKeyRef {
            UnregisterEventHotKey(todoHotKeyRef)
        }
        if let todoHotKeyHandlerRef {
            RemoveEventHandler(todoHotKeyHandlerRef)
        }
        chatAutoRefresh.stop()
    }
}

private func fourCharCode(_ string: String) -> FourCharCode {
    precondition(string.utf8.count == 4)
    return string.utf8.reduce(0) { ($0 << 8) | FourCharCode($1) }
}
