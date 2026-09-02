---
name: home-network
description: Map of Stan's home LAN. Use when a task touches the homelab (stan-lab, 192.168.0.2), the Mac mini, Home Assistant, Plex, the arr media stack, jobr, a Sayya or cima deploy, any 192.168.0.x address, or a *.stan-lab.net hostname.
---

Snapshot taken 2026-09-02. Facts below are what was observed on that date; verify anything that decides an action.

## Network

One flat subnet, 192.168.0.0/24. Router 192.168.0.1 is a TP-Link and is the DHCP server and DNS resolver. Every host below is on DHCP. Whether the router reserves the addresses for stan-lab and the mini is unverified.

| Host | IP | Hardware / OS | Reach |
|---|---|---|---|
| stan-lab ("homelab") | 192.168.0.2 | Intel N97 mini PC, Ubuntu 24.04, 16 GB, 466 GB NVMe, disk1 4 TB, disk2 11 TB | `ssh homelab` (user stan, passwordless sudo) |
| Mac mini | 192.168.0.155 ethernet, 192.168.0.163 wifi | Apple M4, 16 GB, macOS 26.5, 228 GB disk at 98 % | `ssh mini` (user stan, sudo needs a password) |
| MacBook Pro (sierra-mac) | 192.168.0.198 | Sierra work laptop | local; inbound LAN connections are reset by SentinelOne, so nothing on the LAN can reach a server on it |
| Apple TV "Living Room" | 192.168.0.45 | | HA integration |
| WiiM Ultra | 192.168.0.99 | streamer | HA integration |
| LG C2 TV | 192.168.0.133 | MAC 20:28:bc:80:27:1a (Wake-on-LAN) | HA webOS integration |
| Hue Bridge C81240 | 192.168.0.243 | | HA integration |
| iPad | 192.168.0.168 | HA dashboard client | |

The Windows PC in `~/.ssh/config` (`win`, 192.168.1.64) is powered off and out of scope.

Docker on stan-lab is the snap package: `sudo -n docker ...` always. `docker cp` to host paths fails under snap confinement; pipe through `docker exec ... cat`.

## stan-lab services

Main compose project at `~/docker/docker-compose.yml`, configs under `~/docker/config/<service>`. Details in [references/homelab.md](references/homelab.md); the download stack in [references/media-stack.md](references/media-stack.md).

| Service | Port on 192.168.0.2 | Notes |
|---|---|---|
| Home Assistant 2026.8.2 | 8123 (http) | container `homeassistant`, host network; see [references/home-assistant.md](references/home-assistant.md) |
| homepage | 3000 | dashboard; `~/docker/homepage-config/services.yaml` lists every service with its API key |
| Sonarr / Radarr / Prowlarr | 8989 / 7878 / 9696 | |
| Seerr | 5055 | requests |
| qBittorrent | 8085 | runs inside gluetun's network namespace |
| slskd (Soulseek) | 5030 | inside gluetun |
| soulsync | 8008 | music discovery; also holds host ports 8888-8889 |
| FlareSolverr | 8191 | inside gluetun |
| Postgres 17 + pgvector | 5432 | data at `/mnt/disk2/jobs-db`; holds the `jobr` DB written from the mini |
| CloudBeaver | 3011 | DB web UI |
| File Browser | 8080 | serves `/mnt` |
| Sayya (Go server) | 8090, loopback only | compose at `~/dev/sayya`; public at https://saya.stan-lab.net via its `cloudflared` sidecar |
| cima | 4100 | compose at `~/dev/cima`; Postgres on 5433; public at https://cima.stan-lab.net through the Sayya tunnel (joins network `sayya_default`) |
| NFS | 2049 | exports `/mnt/disk1` and `/mnt/disk2` to 192.168.0.0/16 |

## Mac mini services

No containers (Docker Desktop installed, not running). Details in [references/mini.md](references/mini.md).

| Service | Port on 192.168.0.155 | Notes |
|---|---|---|
| Plex Media Server | 32400 | libraries on `/Volumes/disk2/media/{movies,shows,music}`, an NFS mount from stan-lab |
| macos-speech-server | 10300 Wyoming, 8080 http | Parakeet STT + Kokoro TTS; HA's voice pipeline |
| Ollama | 11434, loopback | small local models; `ollama list` |
| jobr | launchd 06:00 daily | LinkedIn scrape + Claude analysis, writes to stan-lab Postgres |
| Screen Sharing / SSH | 5900 / 22 | |

## Cross-machine dependencies

- Plex on the mini reads media over NFS from stan-lab disk2. The mount is created at login only and drops after sleep or network blips; Plex then shows items as unavailable. Remount with `ssh mini 'launchctl kickstart -k gui/501/com.stan.media-mount'`; full block with rescan in [references/runbooks.md](references/runbooks.md).
- jobr on the mini writes to Postgres on stan-lab (5432, DB `jobr`).
- Home Assistant on stan-lab sends voice to the mini's speech server on 10300.
- Both public hostnames (saya, cima) depend on the Sayya `cloudflared` container. Tunnel hostnames are managed in the Cloudflare dashboard, zone stan-lab.net.
- qBittorrent, slskd and FlareSolverr share gluetun's NordVPN network namespace; a VPN restart strands their sockets. `gluetun-watchdog.service` on the host restarts them automatically.

## Scheduled jobs

| Where | When | What |
|---|---|---|
| stan-lab cron | 06:00 UTC daily | `~/.local/bin/sayya-grow-feed.sh` writes Sayya articles; log `~/.local/state/sayya-grow-feed.log` |
| mini launchd `com.stan.jobr.daily` | 06:00 local daily | `~/dev/jobr/run-daily.sh`; logs `~/dev/jobr/logs/daily-YYYY-MM-DD.log` |
| mini launchd `com.stan.media-mount` | at login | mounts the two NFS shares |
| mini launchd `com.local.speech-server` | always (KeepAlive) | speech server |
| stan-lab systemd `gluetun-watchdog.service` | always | restarts qbittorrent + slskd when gluetun recovers |
| MacBook launchd `com.stan.claude-token-watchdog` | Mondays 10:00 | warns 30 days before the headless Claude token expires |

## Headless Claude on the boxes

Both boxes are `sshConfigs` entries in `~/.claude/settings.json`. Scheduled jobs call `~/.local/bin/claude-job`, which exports `CLAUDE_CODE_OAUTH_TOKEN` from `~/.claude/oauth-token` and execs claude; `~/.zprofile` on each box exports the same variable for interactive logins. Never pass `--bare` (it ignores the env var). Token expires 2027-08-31; rotation is in [references/runbooks.md](references/runbooks.md).

## Broken or stale right now

- stan-lab host-level `cloudflared.service` (`/etc/systemd/system/cloudflared.service`, token inline) is in a restart loop with "control stream encountered a failure". Purpose undocumented; neither public hostname uses it.
- Mini disk is 98 % full.
- Mini `/Library/LaunchDaemons/com.user.nfs.media.plist` mounts a share that no longer exists (`/mnt/storage`) and fails every boot. `~/fix-media-mounts.sh` on the mini (autofs switchover) is staged and has never been run; it needs sudo at the keyboard.
- `run-daily.sh` on the mini uses `status=$?`, which zsh rejects, so launchd never sees a real exit code.
- homepage lists Whisparr on 6969 and Prowlarr syncs to 6969 and 8686; nothing listens there. `~/docker/config/{whisparr,lidarr,soularr}`, `~/etc-pihole` and `~/etc-dnsmasq.d` on stan-lab are leftovers with no container.
- Sayya's `HEALTHCHECK_URL` is unset in `~/dev/sayya/.env`, so the cron's dead-man ping is inert.

## Where secrets live

None are in this skill. qBittorrent and every arr API key: `~/docker/homepage-config/services.yaml` on stan-lab. Sayya `TUNNEL_TOKEN` and `READER_TOKEN`: `~/dev/sayya/.env`. Plex token: `defaults read com.plexapp.plexmediaserver PlexOnlineToken` on the mini. jobr Postgres and LinkedIn credentials: `~/dev/jobr/.env` on the mini. Claude OAuth token: `~/.claude/oauth-token` on each box, deploy script `~/.claude/remote-auth/deploy-token.sh` on the MacBook.
