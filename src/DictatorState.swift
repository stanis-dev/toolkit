import Foundation
import AVFoundation
import AppKit

class DictatorState: ObservableObject {
    enum Status { case idle, recording, transcribing }

    @Published var status: Status = .idle
    @Published var audioLevel: CGFloat = 0
    private var audioRecorder: AVAudioRecorder?
    private var meterTimer: Timer?
    private var tempURL: URL {
        URL(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("brain-dictation.wav")
    }

    // Warm process launched at recording start so the model loads while the user speaks
    private var warmProcess: Process?
    private var warmStdin: FileHandle?
    private var warmStdout: FileHandle?

    func startDictation() {
        guard status == .idle else { return }

        let settings: [String: Any] = [
            AVFormatIDKey: kAudioFormatLinearPCM,
            AVSampleRateKey: 16000,
            AVNumberOfChannelsKey: 1,
            AVLinearPCMBitDepthKey: 16,
            AVLinearPCMIsFloatKey: false
        ]

        do {
            audioRecorder = try AVAudioRecorder(url: tempURL, settings: settings)
            audioRecorder?.isMeteringEnabled = true
            audioRecorder?.record()
            status = .recording
            startMeterTimer()
            launchWarmProcess()
            log("Dictator: recording started")
        } catch {
            log("Dictator: failed to start recording — \(error)")
        }
    }

    func finishDictation(andPaste: Bool = false) {
        guard status == .recording else { return }
        stopMeterTimer()
        audioRecorder?.stop()
        audioRecorder = nil
        status = .transcribing
        log("Dictator: recording stopped, transcribing")

        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            guard let self = self else { return }
            let text = self.transcribe(url: self.tempURL)
            DispatchQueue.main.async {
                if let text = text, !text.isEmpty {
                    NSPasteboard.general.clearContents()
                    NSPasteboard.general.setString(text, forType: .string)
                    log("Dictator: copied to clipboard (\(text.count) chars)")
                    if andPaste { self.simulatePaste() }
                }
                self.status = .idle
            }
        }
    }

    private func simulatePaste() {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.05) {
            let src = CGEventSource(stateID: .combinedSessionState)
            let vDown = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: true)
            vDown?.flags = .maskCommand
            let vUp = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: false)
            vUp?.flags = .maskCommand
            vDown?.post(tap: .cghidEventTap)
            vUp?.post(tap: .cghidEventTap)
        }
    }

    func cancelDictation() {
        stopMeterTimer()
        audioRecorder?.stop()
        audioRecorder = nil
        tearDownWarmProcess()
        status = .idle
        log("Dictator: cancelled")
    }

    private func startMeterTimer() {
        meterTimer = Timer.scheduledTimer(withTimeInterval: 1.0 / 12.0, repeats: true) { [weak self] _ in
            guard let self = self, let recorder = self.audioRecorder else { return }
            recorder.updateMeters()
            let db = recorder.averagePower(forChannel: 0) // -160 .. 0
            let clamped = min(1.0, max(0, (db + 50) / 35)) // map -50..-15 → 0..1, hits full at ~70% threshold
            self.audioLevel = CGFloat(clamped)
        }
    }

    private func stopMeterTimer() {
        meterTimer?.invalidate()
        meterTimer = nil
        audioLevel = 0
    }

    // MARK: - Warm process management

    private func launchWarmProcess() {
        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: kPython)
        proc.arguments = [kDictateScript]

        var env = ProcessInfo.processInfo.environment
        let brew = "/opt/homebrew/bin"
        if let path = env["PATH"], !path.contains(brew) {
            env["PATH"] = brew + ":" + path
        } else if env["PATH"] == nil {
            env["PATH"] = brew + ":/usr/bin:/bin"
        }
        proc.environment = env

        let stdinPipe = Pipe()
        let stdoutPipe = Pipe()
        proc.standardInput = stdinPipe
        proc.standardOutput = stdoutPipe
        proc.standardError = FileHandle.nullDevice

        do {
            try proc.run()
            warmProcess = proc
            warmStdin = stdinPipe.fileHandleForWriting
            warmStdout = stdoutPipe.fileHandleForReading
            log("Dictator: warm process launched")
        } catch {
            log("Dictator: failed to launch warm process — \(error)")
        }
    }

    private func tearDownWarmProcess() {
        warmStdin?.closeFile()
        warmStdin = nil
        warmStdout = nil
        if let proc = warmProcess, proc.isRunning { proc.terminate() }
        warmProcess = nil
    }

    private func readLine(from handle: FileHandle) -> String? {
        var buf = Data()
        while true {
            let chunk = handle.readData(ofLength: 1)
            if chunk.isEmpty { return buf.isEmpty ? nil : String(data: buf, encoding: .utf8) }
            if chunk[0] == 0x0A { return String(data: buf, encoding: .utf8) }
            buf.append(chunk)
        }
    }

    private func transcribe(url: URL) -> String? {
        guard let stdin = warmStdin, let stdout = warmStdout else {
            log("Dictator: no warm process, falling back to cold start")
            return transcribeCold(url: url)
        }

        // Wait for "ready" from the warm process
        guard let readyLine = readLine(from: stdout), readyLine.hasPrefix("ready") else {
            log("Dictator: warm process did not become ready, falling back")
            tearDownWarmProcess()
            return transcribeCold(url: url)
        }

        // Send audio path
        let pathLine = url.path + "\n"
        stdin.write(pathLine.data(using: .utf8)!)
        stdin.closeFile()

        // Read transcription result
        let text = readLine(from: stdout)?
            .trimmingCharacters(in: .whitespacesAndNewlines)

        warmProcess?.waitUntilExit()
        let exitCode = warmProcess?.terminationStatus ?? -1
        tearDownWarmProcess()

        if exitCode != 0 {
            log("Dictator: process exited with code \(exitCode), output: \(text ?? "nil")")
            return nil
        }

        return text
    }

    private func transcribeCold(url: URL) -> String? {
        let proc = Process()
        let stdinPipe = Pipe()
        let stdoutPipe = Pipe()
        proc.executableURL = URL(fileURLWithPath: kPython)
        proc.arguments = [kDictateScript]
        proc.standardInput = stdinPipe
        proc.standardOutput = stdoutPipe
        proc.standardError = FileHandle.nullDevice

        var env = ProcessInfo.processInfo.environment
        let brew = "/opt/homebrew/bin"
        if let path = env["PATH"], !path.contains(brew) {
            env["PATH"] = brew + ":" + path
        } else if env["PATH"] == nil {
            env["PATH"] = brew + ":/usr/bin:/bin"
        }
        proc.environment = env

        do {
            try proc.run()
        } catch {
            log("Dictator: cold transcribe failed — \(error)")
            return nil
        }

        let stdinH = stdinPipe.fileHandleForWriting
        let stdoutH = stdoutPipe.fileHandleForReading

        guard let _ = readLine(from: stdoutH) else {
            log("Dictator: cold process did not become ready")
            return nil
        }

        let pathLine = url.path + "\n"
        stdinH.write(pathLine.data(using: .utf8)!)
        stdinH.closeFile()

        let text = readLine(from: stdoutH)?
            .trimmingCharacters(in: .whitespacesAndNewlines)

        proc.waitUntilExit()
        return text
    }
}
