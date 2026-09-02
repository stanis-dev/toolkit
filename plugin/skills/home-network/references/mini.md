# Mac mini (ssh mini, 192.168.0.155)

Apple M4, 16 GB, macOS 26.5. Ethernet `en0` 192.168.0.155 and Wi-Fi `en1` 192.168.0.163 are both up; use .155. Kept awake by Amphetamine and `pmset sleep 0`. Internal disk 228 GB with under 5 GB free. sudo needs a password. It is HDMI1 on the LG C2. Docker Desktop is installed with the daemon stopped; a NordVPN helper daemon is present.

## Plex Media Server (32400)

Login app, server name `mini`, machine id `647f42b160559c69bab9a4ceb75056c8a4c0a678`, music is library section 3. Libraries point at `/Volumes/disk2/media/{movies,shows,music}`.

## NFS mounts from stan-lab

`~/Library/LaunchAgents/com.stan.media-mount.plist` runs at login: `osascript -e 'mount volume "nfs://192.168.0.2/mnt/disk2"'` then the same for disk1, giving `/Volumes/disk2` and `/Volumes/disk1`. Nothing remounts after a drop (mini sleep, network blip, stan-lab reboot); Plex then marks movies unavailable and TV episodes fail with "transcoder has failed". Remount and rescan in [runbooks.md](runbooks.md).

`/Library/LaunchDaemons/com.user.nfs.media.plist` still tries `192.168.0.2:/mnt/storage` at `/Volumes/Media`; that export is gone, leaving an empty `/Volumes/Media`. `~/fix-media-mounts.sh` (staged, never run) replaces both mechanisms with `/etc/fstab` entries served by autofs and deletes the LaunchAgent and the stale daemon.

## jobr (LinkedIn job scout)

`~/dev/jobr`, Node/TypeScript with Playwright and the claude CLI. LaunchAgent `com.stan.jobr.daily` runs `/bin/zsh ~/dev/jobr/run-daily.sh` at 06:00; the script sets PATH for nvm node v24 and `~/.local/bin`, then `npm start`. `.env` keys: `PGHOST PGPORT PGUSER PGPASSWORD PGDATABASE LINKEDIN_USERNAME LINKEDIN_PASSWORD`; Postgres is stan-lab 5432, DB `jobr`. LinkedIn session state in `linkedin_state.json`; when it expires, `npm run auth` with a display recreates it. Pipeline per run: scrape recommended feed, one-prompt batch filter, per-job deep analysis, company research, digest; only jobs new that day are analysed, there is no catch-up. `backfill-outage.ts` (untracked) re-runs analysis for a date window. Known defect: `status=$?` in `run-daily.sh` is rejected by zsh, so the script dies before its final exit and launchd never sees the real code.

## macos-speech-server (Wyoming 10300, HTTP 8080)

Binary `~/bin/speech-server serve`, LaunchAgent `com.local.speech-server` (KeepAlive), config `~/.config/speech-server/speech-server.yaml`: STT Parakeet TDT v3, TTS Kokoro voice `af_heart`. Log `~/Library/Logs/speech-server/output.log`. Source checkout `~/dev/macos-speech-server` (dokterbob/macos-speech-server). Home Assistant consumes it as a Wyoming config entry.
