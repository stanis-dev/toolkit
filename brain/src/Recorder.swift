import Foundation
import ScreenCaptureKit
import AVFoundation
import CoreAudio
import CoreMedia

enum RecorderError: Error, Equatable {
    case noDisplay
}

class Recorder: NSObject, SCStreamOutput {
    private var stream: SCStream?
    private var audioFile: AVAudioFile?
    private var systemSamples: [Float] = []
    private var micSamples: [Float] = []
    private let lock = NSLock()
    var paused = false
    private let writeQueue = DispatchQueue(label: "rec.write")
    private var writeTimer: DispatchSourceTimer?
    private let startTime = Date()
    private var loggedSystemFormat = false
    private var loggedMicFormat = false
    private var systemConverter: AVAudioConverter?
    private var micConverter: AVAudioConverter?
    private let sampleQueue = DispatchQueue(label: "rec.samples")
    private var firstSystemTime: Double?
    private var firstMicTime: Double?
    private var alignedStarts = false
    private var previousInputDevice: AudioDeviceID?
    private let targetFormat = AVAudioFormat(
        commonFormat: .pcmFormatFloat32, sampleRate: kSampleRate, channels: 1, interleaved: false
    )!
    let filename: String

    init(meetingName: String? = nil) {
        let df = DateFormatter()
        df.dateFormat = "yyyy-MM-dd-HHmmss"
        let ts = df.string(from: Date())
        if let name = meetingName, !name.isEmpty {
            filename = "rec-\(ts)-\(sanitizeForFilename(name)).wav"
        } else {
            filename = "rec-\(ts).wav"
        }
        super.init()
        log("Recorder: init → \(filename)\(meetingName.map { " (meeting: \($0))" } ?? "")")
    }

    func start() async throws {
        let inputBefore = getDefaultInputDevice()
        ensureDefaultInputDevice(kTargetAudioDevice)
        if getDefaultInputDevice() != inputBefore {
            previousInputDevice = inputBefore
        }

        let content = try await SCShareableContent.excludingDesktopWindows(
            false, onScreenWindowsOnly: false
        )
        guard let display = content.displays.first else {
            log("Recorder: no display found")
            throw RecorderError.noDisplay
        }

        let excludedBundleIDs: Set<String> = ["tv.plex.plexamp", "tv.plex.desktop"]
        let excludedApps = content.applications.filter { excludedBundleIDs.contains($0.bundleIdentifier) }
        if !excludedApps.isEmpty {
            log("Excluding from capture: \(excludedApps.map { $0.bundleIdentifier }.joined(separator: ", "))")
        }
        let filter = SCContentFilter(display: display, excludingApplications: excludedApps, exceptingWindows: [])
        let config = SCStreamConfiguration()
        config.capturesAudio = true
        config.captureMicrophone = true
        config.sampleRate = Int(kSampleRate)
        config.channelCount = 1
        config.width = 2
        config.height = 2

        let url = URL(fileURLWithPath: "\(kOutputDir)/\(filename)")
        audioFile = try AVAudioFile(
            forWriting: url,
            settings: [
                AVFormatIDKey: kAudioFormatLinearPCM,
                AVSampleRateKey: kSampleRate,
                AVNumberOfChannelsKey: 1,
                AVLinearPCMBitDepthKey: 16,
                AVLinearPCMIsFloatKey: false,
                AVLinearPCMIsBigEndianKey: false
            ],
            commonFormat: .pcmFormatFloat32,
            interleaved: false
        )

        log("Recorder: display \(display.displayID) (\(display.width)x\(display.height)), sampleRate=\(kSampleRate)")
        stream = SCStream(filter: filter, configuration: config, delegate: nil)
        try stream!.addStreamOutput(self, type: .audio, sampleHandlerQueue: sampleQueue)
        try stream!.addStreamOutput(self, type: .microphone, sampleHandlerQueue: sampleQueue)
        try await stream!.startCapture()

        startWriteTimer()
        log("Recorder: capture started → \(kOutputDir)/\(filename)")
    }

    func stop() {
        writeTimer?.cancel()
        writeTimer = nil
        if let stream {
            try? stream.removeStreamOutput(self, type: .audio)
            try? stream.removeStreamOutput(self, type: .microphone)
            stream.stopCapture { error in
                if let error { log("Recorder: stopCapture failed — \(error)") }
            }
        }
        stream = nil
        writeQueue.sync { self.mixAndWrite() }
        audioFile = nil
        if let previous = previousInputDevice {
            setDefaultInputDevice(previous)
            log("Recorder: restored default input → '\(getDeviceName(previous) ?? "Unknown")'")
            previousInputDevice = nil
        }

        let elapsed = Date().timeIntervalSince(startTime)
        let filePath = "\(kOutputDir)/\(filename)"
        let fileSize = (try? FileManager.default.attributesOfItem(atPath: filePath))?[.size] as? UInt64 ?? 0
        let sizeMB = String(format: "%.1f", Double(fileSize) / 1_048_576)
        log("Recorder: stopped — \(formatDuration(elapsed)), \(sizeMB) MB → \(filename)")
    }

    func stream(
        _ stream: SCStream,
        didOutputSampleBuffer sampleBuffer: CMSampleBuffer,
        of type: SCStreamOutputType
    ) {
        guard sampleBuffer.isValid, CMSampleBufferDataIsReady(sampleBuffer) else { return }

        if type == .audio && !loggedSystemFormat {
            loggedSystemFormat = true
            logAudioFormat(sampleBuffer, label: "System")
        } else if type == .microphone && !loggedMicFormat {
            loggedMicFormat = true
            logAudioFormat(sampleBuffer, label: "Mic")
        }

        guard let floats = extractFloats(from: sampleBuffer, type: type) else { return }

        let pts = CMSampleBufferGetPresentationTimeStamp(sampleBuffer).seconds
        lock.lock()
        switch type {
        case .audio:
            if firstSystemTime == nil { firstSystemTime = pts }
            systemSamples.append(contentsOf: floats)
        case .microphone:
            if firstMicTime == nil { firstMicTime = pts }
            micSamples.append(contentsOf: floats)
        default:
            break
        }
        if !alignedStarts, let sysStart = firstSystemTime, let micStart = firstMicTime {
            alignedStarts = true
            let delta = micStart - sysStart
            let pad = Int((abs(delta) * kSampleRate).rounded())
            if pad > 0, pad < Int(kSampleRate) * 5 {
                let zeros = [Float](repeating: 0, count: pad)
                if delta > 0 { micSamples.insert(contentsOf: zeros, at: 0) }
                else { systemSamples.insert(contentsOf: zeros, at: 0) }
                log("Recorder: aligned stream starts — padded \(delta > 0 ? "mic" : "system") by \(pad) samples")
            }
        }
        lock.unlock()
    }

    private func startWriteTimer() {
        let timer = DispatchSource.makeTimerSource(queue: writeQueue)
        timer.schedule(deadline: .now() + 0.1, repeating: 0.1)
        timer.setEventHandler { [weak self] in self?.mixAndWrite() }
        timer.resume()
        writeTimer = timer
    }

    private func mixAndWrite() {
        lock.lock()
        if paused {
            systemSamples.removeAll(keepingCapacity: true)
            micSamples.removeAll(keepingCapacity: true)
            lock.unlock()
            return
        }
        let sysCount = systemSamples.count
        let micCount = micSamples.count
        guard sysCount > 0 || micCount > 0 else { lock.unlock(); return }

        let count: Int
        var mixed: [Float]

        if sysCount > 0 && micCount > 0 {
            count = min(sysCount, micCount)
            mixed = [Float](repeating: 0, count: count)
            for i in 0..<count {
                mixed[i] = max(-1.0, min(1.0, (systemSamples[i] + micSamples[i]) * 0.5))
            }
            systemSamples.removeFirst(count)
            micSamples.removeFirst(count)
        } else if sysCount > 0 {
            mixed = systemSamples.map { $0 * 0.5 }
            count = sysCount
            systemSamples.removeAll(keepingCapacity: true)
        } else {
            mixed = micSamples.map { $0 * 0.5 }
            count = micCount
            micSamples.removeAll(keepingCapacity: true)
        }
        lock.unlock()

        guard let audioFile = audioFile,
              let format = AVAudioFormat(
                  commonFormat: .pcmFormatFloat32,
                  sampleRate: kSampleRate,
                  channels: 1,
                  interleaved: false
              ),
              let buffer = AVAudioPCMBuffer(
                  pcmFormat: format,
                  frameCapacity: AVAudioFrameCount(count)
              )
        else { return }

        buffer.frameLength = AVAudioFrameCount(count)
        let dst = buffer.floatChannelData![0]
        for i in 0..<count { dst[i] = mixed[i] }

        do {
            try audioFile.write(from: buffer)
        } catch {
            fputs("Write error: \(error)\n", stderr)
        }
    }

    private func logAudioFormat(_ buf: CMSampleBuffer, label: String) {
        guard let fd = CMSampleBufferGetFormatDescription(buf),
              let asbd = CMAudioFormatDescriptionGetStreamBasicDescription(fd)?.pointee
        else { return }
        let flags = String(asbd.mFormatFlags, radix: 16)
        fputs("\(label): \(asbd.mSampleRate)Hz \(asbd.mChannelsPerFrame)ch \(asbd.mBitsPerChannel)bit flags=0x\(flags)\n", stderr)
    }

    private func extractFloats(from sampleBuffer: CMSampleBuffer, type: SCStreamOutputType) -> [Float]? {
        let frameCount = CMSampleBufferGetNumSamples(sampleBuffer)
        guard frameCount > 0,
              let fd = CMSampleBufferGetFormatDescription(sampleBuffer),
              let asbdPtr = CMAudioFormatDescriptionGetStreamBasicDescription(fd),
              let srcFormat = AVAudioFormat(streamDescription: asbdPtr),
              let srcBuf = AVAudioPCMBuffer(pcmFormat: srcFormat, frameCapacity: AVAudioFrameCount(frameCount))
        else { return nil }

        srcBuf.frameLength = AVAudioFrameCount(frameCount)
        guard CMSampleBufferCopyPCMDataIntoAudioBufferList(
            sampleBuffer, at: 0, frameCount: Int32(frameCount),
            into: srcBuf.mutableAudioBufferList
        ) == noErr else { return nil }

        if srcFormat.commonFormat == .pcmFormatFloat32 && srcFormat.channelCount == 1
            && srcFormat.sampleRate == kSampleRate {
            return Array(UnsafeBufferPointer(start: srcBuf.floatChannelData![0], count: frameCount))
        }

        if type == .audio && systemConverter == nil {
            systemConverter = AVAudioConverter(from: srcFormat, to: targetFormat)
        } else if type == .microphone && micConverter == nil {
            micConverter = AVAudioConverter(from: srcFormat, to: targetFormat)
        }
        let conv = (type == .audio ? systemConverter : micConverter)
        let ratio = kSampleRate / srcFormat.sampleRate
        let outputCapacity = AVAudioFrameCount(ceil(Double(frameCount) * ratio))
        guard let converter = conv,
              let dstBuf = AVAudioPCMBuffer(pcmFormat: targetFormat, frameCapacity: outputCapacity)
        else { return nil }

        var consumed = false
        let status = converter.convert(to: dstBuf, error: nil) { _, outStatus in
            if consumed { outStatus.pointee = .noDataNow; return nil }
            consumed = true
            outStatus.pointee = .haveData
            return srcBuf
        }
        guard status != .error, let floatData = dstBuf.floatChannelData else { return nil }
        return Array(UnsafeBufferPointer(start: floatData[0], count: Int(dstBuf.frameLength)))
    }
}
