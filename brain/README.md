# Brain

A personal macOS app for recording meetings, transcribing them with speaker attribution, and managing the recordings.

## Features

- **Meeting recording**: Captures system audio (other participants) and microphone (you) into a stereo WAV file
- **Transcription**: Speaker-attributed transcription via Whisper Large-v3 running locally on Apple Silicon GPU
- **Playback**: In-app audio playback with seeking
- **Multilingual**: Auto-detects English, Spanish, and Turkish

## Prerequisites

- macOS 14+, Apple Silicon
- [whisper-cpp](https://github.com/ggml-org/whisper.cpp) (`brew install whisper-cpp`)
- [Node.js](https://nodejs.org/) 22+ (`brew install node@22`)
- Whisper Large-v3 GGML model in `models/ggml-large-v3.bin`

## Build

```bash
./build.sh
```

This compiles all Swift sources, assembles `Brain.app`, signs it with hardened runtime, and copies it to `/Applications/Brain.app`.

## Usage

**From the app**: Open Brain.app, click the green circle to start recording, click it again to stop. Expand the list to play, transcribe, or delete recordings.

**From the terminal**:

```bash
# Record (CLI, same binary)
./brain

# Transcribe the most recent recording
./scripts/transcribe

# Transcribe a specific file
./scripts/transcribe rec-2026-03-24-143022.wav
```

## Permissions

On first launch, macOS will prompt for:

- **Screen Recording** (required by ScreenCaptureKit for system audio capture)
- **Microphone** (for recording your voice)
- **Accessibility** (for global dictation hotkey)
- **Calendar** (for detecting meeting names)

Grant all in the app's Settings tab or in System Settings > Privacy & Security.

### Code signing requirements for permissions

macOS TCC (the permission system) is sensitive to how the app is signed and installed. Three things are required for permissions to work reliably:

- **Hardened runtime** (`codesign --options runtime`): Without this, `CGPreflightScreenCaptureAccess()` always returns false on macOS 14+, even if the user granted Screen Recording in System Settings.
- **Entitlements** (`resources/Brain.entitlements`): Hardened runtime restricts capabilities by default. Each permission-gated API needs an explicit entitlement (`com.apple.security.device.audio-input` for mic, `com.apple.security.personal-information.calendars` for calendar). Missing an entitlement silently blocks the permission prompt from appearing.
- **Real copy in /Applications** (not a symlink): TCC and Launch Services resolve app identity by path. A symlink from `/Applications` into a dev directory causes icon resolution failures (folder icon in System Settings) and unreliable permission grants.

If permissions stop working after changes to the build, check `codesign -dvvv Brain.app` for `flags=0x10000(runtime)` and `codesign -d --entitlements - Brain.app` for the full entitlements list.

## Project Structure

```
src/                  Swift source files
  main.swift          App bootstrap
  Config.swift        Constants and logging
  Recorder.swift      Audio capture (ScreenCaptureKit)
  State.swift         App state, recording list, playback
  Views.swift         Main layout, sidebar, recorder tab
  TranscriptView.swift
  RecordingRow.swift
  Tabs.swift          Notes and Settings placeholder tabs
  AppDelegate.swift   Window setup and key handling
resources/            Info.plist, AppIcon.icns, Brain.entitlements
scripts/              Transcription scripts (TypeScript + shell wrapper)
data/                 Recordings, transcripts, logs (gitignored)
models/               Whisper GGML model (gitignored, ~3GB)
```
