# Brain

A personal macOS app for recording meetings, transcribing them locally with speaker attribution, dictating text anywhere, detecting meetings, and keeping Slack/Teams history synced for an assistant to read.

## Features

- **Meeting recording**: Captures system audio (other participants) and microphone (you) via ScreenCaptureKit, mixed into a mono 16-bit WAV in `data/`.
- **Transcription**: Local Whisper Large-v3 (`whispermlx`) on Apple Silicon, word alignment, and pyannote speaker diarization. Auto-detects the spoken language and never translates. Known speakers are matched by voice embedding against `data/speakers.json`.
- **Polish + summary**: An `agent` (cursor-agent) pass corrects obvious transcription errors and writes a structured summary with to-dos.
- **Dictation**: Global hotkey (Ctrl+Shift+Option+Cmd+D) records and transcribes speech with `parakeet-mlx`, then copies (or pastes) the result.
- **Meeting detection**: Watches camera/mic use and Slack/Teams/browser windows, and offers to start recording when a call is detected.
- **Chat sync**: Background exporters pull Slack, Teams, and two Google Chat spaces to `data/` as readable Markdown for the assistant (opencode) to consume.
- **Assistant tab**: Embeds the local opencode web UI (`127.0.0.1:4096`).
- **TODO overlay**: A floating panel two-way-synced with `data/assistant-todo.md`.

## Prerequisites

- macOS 14+, Apple Silicon
- Python 3.13 (`brew install python@3.13`) — `whispermlx` requires Python < 3.14
- [Node.js](https://nodejs.org/) 22+ (`brew install node`) — for the chat exporters' LevelDB bridge
- [ffmpeg](https://ffmpeg.org/) (`brew install ffmpeg`) — pyannote audio decoding
- `agent` (cursor-agent) on `PATH` — transcript polish/summary
- [opencode](https://opencode.ai/) — the assistant tab (`opencode web --hostname 127.0.0.1 --port 4096`)

## Setup

```bash
# Python environment (whispermlx needs Python < 3.14)
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Node dependency for chat exporters
npm install

# HuggingFace token for pyannote diarization (gated models)
echo "HF_TOKEN=hf_xxx" > .env
```

The `.env` token needs access to `pyannote/speaker-diarization-community-1` (accept its terms once on huggingface.co).

## Build

```bash
./build.sh
```

Runs the test suite (`scripts/test.sh`, skip with `--skip-tests`), compiles all Swift sources, assembles `Brain.app`, signs it with hardened runtime, and installs it to `/Applications/Brain.app`.

## Usage

**From the app**: Open Brain.app. The recorder tab's circle starts/stops a recording; expand a recording to transcribe, play, rename speakers, or delete. Dictation, meeting detection, and chat sync run in the background.

**Transcribe from the terminal**:

```bash
# Most recent recording
.venv/bin/python3 scripts/transcribe.py

# A specific file
.venv/bin/python3 scripts/transcribe.py rec-2026-03-24-143022.wav
```

## Programmatic control

`brainctl` controls the running app and returns JSON. It uses a private Unix
socket accessible only to the current macOS user; there is no network port.
Launch the app with `brainctl launch` if it is not running.

```bash
brainctl status
brainctl sync google-chat --wait
brainctl sync slack
brainctl job <job-id> --wait
brainctl auto google-chat on
brainctl recording start
brainctl recording pause
brainctl recording resume
brainctl recording stop
brainctl recordings
brainctl transcribe <recording-id>
brainctl dictation start
brainctl dictation finish
brainctl dictation cancel
brainctl todo get
brainctl todo set --file /absolute/path/todo.md
brainctl todo append --file /absolute/path/additions.md
brainctl navigate macos
brainctl navigate hide
```

- Sync platforms: `slack`, `teams`, `google-chat`. `sync` returns a job ID;
  `--wait` waits for completion and exits nonzero on failure. Jobs are kept in
  memory until restart, with up to 100 completed jobs retained.
- `auto` accepts `on` or `off`. Navigation accepts `assistant`, `recorder`,
  `dictator`, `macos`, `settings`, `logs`, or `hide`.
- Recording start is asynchronous. Poll `status` for `recording.starting`,
  `recording.active`, and `recording.error`. CLI start errors do not open a modal.
- Dictation finish transcribes and copies text to the clipboard. `--paste` also
  pastes it. Poll `status` for `dictation.state`, `dictation.text`, and
  `dictation.error`. Transcription progress is available through `recordings`.
- TODO set/append also accept piped stdin. Append adds the supplied text verbatim.

The client is `scripts/brainctl.py`, linked at `/Users/stan/.local/bin/brainctl`.
Other programs can send one newline-delimited JSON object to
`/Users/stan/Library/Application Support/Brain/control.sock`; replies use
`{"ok":true,"result":...}` or `{"ok":false,"error":{"code":...,"message":...}}`.
The client's `--help` lists commands and arguments.

## Google Chat

Google Chat uses the signed-in browser through the Playwriter extension, without
a Cloud project or OAuth setup. Keep the browser connected to Playwriter and
signed into Google Chat as `stan.samisco@ext.sierra.ai`.
Install the `playwriter` CLI if it is not already on PATH.

The macOS tab has a **Google Chat** Sync button and Auto toggle. Auto refresh runs
every five minutes after launch or the preceding sync. Only these spaces are read:

- **Voicebot - Openpay** (`AAQAkdY0pQg`)
- **VoiceBot- Cobranza** (`AAQAZ0v2SzU`)

The first sync briefly opens a temporary background tab to obtain browser
authentication, then closes that tab before reading history through direct HTTP
requests. Authentication is reused across spaces and later syncs in Playwriter's
relay memory. It is refreshed only when Google rejects it, with one refresh/retry
per run. Network failures and rate limits do not trigger a browser refresh.

Cookies and anti-CSRF tokens are never written to disk. Restarting the relay or
updating the exporter clears the cache. Chat does not need to remain open: when
authentication is needed, the helper opens a temporary Chat tab in the connected
browser. It uses the account index of an existing verified Sierra tab, or the
known account-2 URL, and verifies the Sierra account before reading credentials.
If sign-in expires or the account index changes, open Sierra Chat in the connected
browser and press Sync.

The exporter checks the account, space IDs, pagination and reply counts before
replacing either space's export. The previous snapshot remains available after a
failed scrape.

Outputs are in `data/google-chat/sierra/snapshot.json` and
`data/google-chat/sierra/readable/google_chat_<space-id>.md`. Each refresh rereads
the accessible history so edits, replies and reactions are reflected. Timestamps,
sender names, threads, canonical links and attachment names are retained;
attachment files are not downloaded. History Google no longer exposes cannot be
recovered. Google's undocumented browser format may change; unrecognized or
incomplete responses fail instead of silently replacing the export.

```bash
/Users/stan/code/toolkit/brain/.venv/bin/python3 /Users/stan/code/toolkit/brain/scripts/google_chat_export.py
```

## Tests

```bash
./scripts/test.sh
```

Runs the Swift meeting-detection and Slack-parser tests, the export-helper unit tests, and the chat-export storage/rendering tests. `build.sh` runs this and refuses to install on failure.

## Permissions

On first launch, macOS will prompt for:

- **Screen Recording** (ScreenCaptureKit system-audio capture)
- **Microphone** (your voice)
- **Accessibility** (global dictation hotkey and paste)
- **Calendar** (meeting names for recordings)
- **Automation** (inspecting the front browser tab for Google Meet calls)

Grant them in the app's Settings tab or in System Settings › Privacy & Security.

### Code signing requirements for permissions

macOS TCC is sensitive to how the app is signed and installed. Three things are required for permissions to work reliably:

- **Hardened runtime** (`codesign --options runtime`): Without this, `CGPreflightScreenCaptureAccess()` always returns false on macOS 14+, even after granting Screen Recording.
- **Entitlements** (`resources/Brain.entitlements`): Hardened runtime restricts capabilities by default. Each permission-gated API needs an explicit entitlement (`com.apple.security.device.audio-input`, `com.apple.security.personal-information.calendars`, `com.apple.security.automation.apple-events`). A missing entitlement silently blocks the permission prompt.
- **Real copy in /Applications** (not a symlink): TCC and Launch Services resolve app identity by path. A symlink into a dev directory causes icon-resolution failures and unreliable grants.

If permissions stop working after a build change, check `codesign -dvvv Brain.app` for `flags=0x10000(runtime)` and `codesign -d --entitlements - Brain.app` for the full list.

## Project structure

```
src/                  Swift sources (app, recorder, tabs, meeting detection, chat sync)
resources/            Info.plist, AppIcon.icns, Brain.entitlements
scripts/              transcribe.py, dictate.py, chat exporters, tests, test.sh
prompts/              polish.md (transcript correction + summary contract)
requirements.txt      Python environment (rebuildable with python3.13)
data/                 Recordings, transcripts, chat exports, logs (gitignored)
```
