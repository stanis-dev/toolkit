import Foundation
import CoreAudio

func getDefaultInputDevice() -> AudioDeviceID {
    var deviceID = AudioDeviceID(0)
    var size = UInt32(MemoryLayout<AudioDeviceID>.size)
    var address = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyDefaultInputDevice,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain
    )
    AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size, &deviceID)
    return deviceID
}

func getDeviceName(_ deviceID: AudioDeviceID) -> String? {
    var address = AudioObjectPropertyAddress(
        mSelector: kAudioObjectPropertyName,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain
    )
    var name: Unmanaged<CFString>?
    var size = UInt32(MemoryLayout<Unmanaged<CFString>?>.size)
    let status = AudioObjectGetPropertyData(deviceID, &address, 0, nil, &size, &name)
    guard status == noErr, let cfName = name?.takeRetainedValue() else { return nil }
    return cfName as String
}

func findInputDevice(named target: String) -> AudioDeviceID? {
    var address = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyDevices,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain
    )
    var size: UInt32 = 0
    AudioObjectGetPropertyDataSize(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size)
    let count = Int(size) / MemoryLayout<AudioDeviceID>.size
    var devices = [AudioDeviceID](repeating: 0, count: count)
    AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size, &devices)

    for device in devices {
        guard getDeviceName(device) == target else { continue }
        var inputAddress = AudioObjectPropertyAddress(
            mSelector: kAudioDevicePropertyStreamConfiguration,
            mScope: kAudioDevicePropertyScopeInput,
            mElement: kAudioObjectPropertyElementMain
        )
        var bufSize: UInt32 = 0
        AudioObjectGetPropertyDataSize(device, &inputAddress, 0, nil, &bufSize)
        if bufSize > 0 { return device }
    }
    return nil
}

func setDefaultInputDevice(_ deviceID: AudioDeviceID) {
    var id = deviceID
    var address = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyDefaultInputDevice,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain
    )
    AudioObjectSetPropertyData(
        AudioObjectID(kAudioObjectSystemObject), &address, 0, nil,
        UInt32(MemoryLayout<AudioDeviceID>.size), &id
    )
}

/// Switch the system default input to `target` if that device is currently connected
/// and exposes an input stream. No-op when the device isn't available or already active.
/// Always logs an `Audio.ensure:` line so callers leave a verifiable trace.
@discardableResult
func ensureDefaultInputDevice(_ target: String) -> Bool {
    let currentID = getDefaultInputDevice()
    let currentName = getDeviceName(currentID) ?? "Unknown"
    if currentName == target {
        log("Audio.ensure: already on target '\(target)' — no switch needed")
        return true
    }
    guard let deviceID = findInputDevice(named: target) else {
        log("Audio.ensure: target '\(target)' not available — staying on '\(currentName)'")
        return false
    }
    setDefaultInputDevice(deviceID)
    let newName = getDeviceName(getDefaultInputDevice()) ?? "Unknown"
    let success = newName == target
    log("Audio.ensure: switched '\(currentName)' → '\(newName)' (target='\(target)', success=\(success))")
    return success
}
