import Foundation
import AVFoundation
import SwiftUI

enum Tab { case assistant, recorder, dictator, macos, settings, logs }

class AppState: ObservableObject {
    @Published var selectedTab: Tab = .assistant
    @Published var viewingTranscriptId: String?
}

struct Recording: Identifiable {
    let id: String
    let filename: String
    let url: URL
    let duration: TimeInterval
    var hasTranscript: Bool
    var transcribing: Bool = false
    var transcribeStatus: String = ""
    var customName: String?

    var dateString: String {
        let base = filename.replacingOccurrences(of: "rec-", with: "").replacingOccurrences(of: ".wav", with: "")
        let parts = base.split(separator: "-", maxSplits: 4)
        let tsString = parts.prefix(4).joined(separator: "-")
        let parse = DateFormatter()
        parse.dateFormat = "yyyy-MM-dd-HHmmss"
        let fmt = DateFormatter()
        fmt.dateFormat = "MMM d, HH:mm"
        return parse.date(from: tsString).map { fmt.string(from: $0) } ?? tsString
    }

    var displayName: String {
        if let custom = customName, !custom.isEmpty {
            return "\(custom) (\(dateString))"
        }
        let base = filename.replacingOccurrences(of: "rec-", with: "").replacingOccurrences(of: ".wav", with: "")
        let parts = base.split(separator: "-", maxSplits: 4)
        let meetingPart = parts.count > 4 ? String(parts[4]).replacingOccurrences(of: "-", with: " ") : nil
        if let meeting = meetingPart {
            return "\(meeting) (\(dateString))"
        }
        return dateString
    }

    var durationString: String { formatDuration(duration) }
}

class RecordingListState: ObservableObject {
    @Published var recordings: [Recording] = []
    @Published var deletingId: String?
    weak var playback: PlaybackState?
    private var runningProcesses: [String: Process] = [:]

    private func loadCustomNames() -> [String: String] {
        guard let data = FileManager.default.contents(atPath: kNamesFile),
              let dict = try? JSONSerialization.jsonObject(with: data) as? [String: String]
        else { return [:] }
        return dict
    }

    func saveCustomName(id: String, name: String) {
        var names = loadCustomNames()
        names[id] = name
        guard let data = try? JSONSerialization.data(withJSONObject: names, options: [.prettyPrinted, .sortedKeys]) else { return }
        FileManager.default.createFile(atPath: kNamesFile, contents: data)
        if let idx = recordings.firstIndex(where: { $0.id == id }) {
            recordings[idx].customName = name
        }
    }

    func refresh() {
        let fm = FileManager.default
        let dir = URL(fileURLWithPath: kOutputDir)
        guard let files = try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: nil) else { return }

        let customNames = loadCustomNames()
        var recs: [Recording] = []
        for url in files where url.pathExtension == "wav" && url.lastPathComponent.hasPrefix("rec-") {
            let name = url.lastPathComponent
            let rid = url.deletingPathExtension().lastPathComponent
            var dur: TimeInterval = 0
            if let af = try? AVAudioFile(forReading: url) {
                dur = Double(af.length) / af.processingFormat.sampleRate
            }
            let txtExists = fm.fileExists(atPath: url.path.replacingOccurrences(of: ".wav", with: ".txt"))
            let stillTranscribing = runningProcesses[rid] != nil

            let summaryPath = url.path.replacingOccurrences(of: ".wav", with: ".summary.md")
            var agentName: String? = nil
            if let summary = try? String(contentsOfFile: summaryPath, encoding: .utf8) {
                for line in summary.split(separator: "\n") {
                    let l = line.trimmingCharacters(in: .whitespaces)
                    if l.hasPrefix("## Title:") {
                        agentName = String(l.dropFirst("## Title:".count)).trimmingCharacters(in: .whitespaces)
                        break
                    }
                }
            }

            var rec = Recording(id: rid, filename: name, url: url,
                                duration: dur, hasTranscript: txtExists, transcribing: stillTranscribing)
            rec.customName = customNames[rid] ?? agentName
            recs.append(rec)
        }
        recordings = recs.sorted { $0.filename > $1.filename }
        let transcribingCount = recordings.filter { $0.transcribing }.count
        log("Recordings: refreshed — \(recordings.count) total, \(transcribingCount) transcribing")
    }

    func delete(id: String) {
        if playback?.playingId == id { playback?.stop() }
        guard let rec = recordings.first(where: { $0.id == id }) else { return }
        log("Recordings: deleting \(rec.filename)")
        let base = rec.url.path.replacingOccurrences(of: ".wav", with: "")
        for ext in [".wav", ".json", ".txt", ".polished.txt", ".reasoning.jsonl", ".summary.md", ".summary-reasoning.jsonl"] {
            let url = URL(fileURLWithPath: base + ext)
            guard FileManager.default.fileExists(atPath: url.path) else { continue }
            try? FileManager.default.trashItem(at: url, resultingItemURL: nil)
        }
        deletingId = nil
        refresh()
    }

    private func updateStatus(id: String, _ status: String) {
        if let idx = recordings.firstIndex(where: { $0.id == id }) {
            recordings[idx].transcribeStatus = status
        }
    }

    private func parseStatus(_ line: String) -> String? {
        let t = line.trimmingCharacters(in: .whitespaces)
        if t.hasPrefix("Transcribing ") { return "Transcribing…" }
        if t.hasPrefix("Loading model") { return "Loading model…" }
        if t == "Transcribing..." { return "Transcribing audio…" }
        if t.hasPrefix("Aligning") { return "Aligning words…" }
        if t.hasPrefix("Diarizing") { return "Identifying speakers…" }
        if t.hasPrefix("Correcting") { return "Correcting + summarizing…" }
        if t.hasPrefix("Polished") || t.hasPrefix("Summary saved") { return "Finishing…" }
        return nil
    }

    func transcribe(id: String) {
        guard let idx = recordings.firstIndex(where: { $0.id == id }),
              runningProcesses[id] == nil else {
            log("transcribe(\(id)): skipped — already running or not found")
            return
        }
        recordings[idx].transcribing = true
        recordings[idx].transcribeStatus = "Starting…"
        let fname = recordings[idx].filename
        log("transcribe(\(id)): starting for \(fname)")

        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: kPython)
        proc.arguments = ["-u", kTranscribeScript, fname]
        proc.currentDirectoryURL = URL(fileURLWithPath: kOutputDir)
        var env = ProcessInfo.processInfo.environment
        env["PATH"] = "/Users/stan/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:" + (env["PATH"] ?? "")
        proc.environment = env

        let pipe = Pipe()
        proc.standardOutput = pipe
        proc.standardError = pipe

        pipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            guard !data.isEmpty, let text = String(data: data, encoding: .utf8) else { return }
            log("transcribe(\(id)): \(text.trimmingCharacters(in: .whitespacesAndNewlines))")
            for line in text.split(separator: "\n") {
                if let status = self?.parseStatus(String(line)) {
                    DispatchQueue.main.async { self?.updateStatus(id: id, status) }
                }
            }
        }

        proc.terminationHandler = { [weak self] p in
            pipe.fileHandleForReading.readabilityHandler = nil
            log("transcribe(\(id)): exited with code \(p.terminationStatus)")
            DispatchQueue.main.async {
                self?.runningProcesses.removeValue(forKey: id)
                self?.refresh()
            }
        }
        runningProcesses[id] = proc
        do {
            try proc.run()
            log("transcribe(\(id)): process launched (pid \(proc.processIdentifier))")
        } catch {
            log("transcribe(\(id)): launch failed — \(error)")
            runningProcesses.removeValue(forKey: id)
            recordings[idx].transcribing = false
        }
    }
}

class PlaybackState: NSObject, ObservableObject, AVAudioPlayerDelegate {
    @Published var playingId: String?
    @Published var progress: Double = 0
    @Published var currentTime: TimeInterval = 0
    @Published var isPlaying = false
    private var player: AVAudioPlayer?
    private var timer: Timer?

    func toggle(recording: Recording) {
        if playingId == recording.id {
            if isPlaying { player?.pause(); isPlaying = false }
            else { player?.play(); isPlaying = true }
        } else {
            stop()
            guard let p = try? AVAudioPlayer(contentsOf: recording.url) else { return }
            player = p
            p.delegate = self
            playingId = recording.id
            p.play()
            isPlaying = true
            timer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { [weak self] _ in
                guard let self = self, let p = self.player else { return }
                self.currentTime = p.currentTime
                self.progress = p.duration > 0 ? p.currentTime / p.duration : 0
            }
        }
    }

    func seek(to fraction: Double) {
        guard let p = player else { return }
        p.currentTime = p.duration * fraction
        currentTime = p.currentTime
        progress = fraction
    }

    func playFrom(recording: Recording, time: TimeInterval) {
        if playingId != recording.id {
            stop()
            guard let p = try? AVAudioPlayer(contentsOf: recording.url) else { return }
            player = p
            p.delegate = self
            playingId = recording.id
            timer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { [weak self] _ in
                guard let self = self, let p = self.player else { return }
                self.currentTime = p.currentTime
                self.progress = p.duration > 0 ? p.currentTime / p.duration : 0
            }
        }
        player?.currentTime = time
        player?.play()
        isPlaying = true
        currentTime = time
        if let p = player, p.duration > 0 { progress = time / p.duration }
    }

    func stop() {
        timer?.invalidate()
        timer = nil
        player?.stop()
        player = nil
        playingId = nil
        isPlaying = false
        progress = 0
        currentTime = 0
    }

    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        DispatchQueue.main.async { self.stop() }
    }
}

class RecordingState: ObservableObject {
    @Published var isRecording = false
    @Published var isPaused = false
    @Published var elapsed: TimeInterval = 0
    private var timer: Timer?
    private var recordingStart: Date?
    private var recorder: Recorder?

    func startRecording() {
        log("Recording: starting…")
        let meeting = currentMeetingName()
        log("Recording: calendar lookup → \(meeting ?? "no meeting")")
        let rec = Recorder(meetingName: meeting)
        recorder = rec
        isRecording = true
        isPaused = false
        elapsed = 0
        recordingStart = Date()
        startTimer()
        Task {
            do { try await rec.start() } catch {
                log("Recording: start failed — \(error)")
                await MainActor.run { NSApp.terminate(nil) }
            }
        }
    }

    func stopRecording() {
        guard isRecording else { return }
        log("Recording: stopping (elapsed \(formattedTime))")
        timer?.invalidate()
        timer = nil
        isRecording = false
        isPaused = false
        recorder?.stop()
        recorder = nil
    }

    func togglePause() {
        guard isRecording else { return }
        isPaused.toggle()
        recorder?.paused = isPaused
        log("Recording: \(isPaused ? "paused" : "resumed") at \(formattedTime)")
        if isPaused {
            timer?.invalidate()
            timer = nil
        } else {
            recordingStart = Date().addingTimeInterval(-elapsed)
            startTimer()
        }
    }

    private func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { [weak self] _ in
            guard let self = self, let start = self.recordingStart else { return }
            self.elapsed = Date().timeIntervalSince(start)
        }
    }

    var formattedTime: String { formatDuration(elapsed) }
}
