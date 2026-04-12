---
name: local-infra
description: >-
  Reference for Stan's home network machines. Use when asked to perform tasks on the
  homelab, Linux server, Mac Mini, Plex server, or media server — includes SSH details,
  Docker stack, storage layout, Plex API, and command patterns for both machines.
---

# Local Infrastructure

Two machines on the local network. Both accessible via SSH key (`~/.ssh/id_ed25519`).

## Homelab (Ubuntu)

### Connection

| Field | Value |
|-------|-------|
| Host alias | `homelab` (configured in `~/.ssh/config`) |
| IP | `192.168.0.2` |
| User | `stan` |
| Hostname | `stan-lab` |
| OS | Ubuntu 24.04 LTS (x86_64) |
| Docker | 28.4.0 with Compose v2.39.1 (requires `sudo`) |

### Storage

Two physical disks merged via **mergerfs** into a single `/mnt/storage` pool:

| Mount | Size | Used | Type |
|-------|------|------|------|
| `/mnt/disk1` | 3.6T | 2.0T | ext4 (HDD) |
| `/mnt/disk2` | 11T | 6.4T | ext4 (HDD) |
| `/mnt/storage` | 15T | 8.4T | mergerfs (disk1 + disk2) |
| `/` | 466G | 108G | ext4 (NVMe) |

**Network share:** NFS - `/mnt/storage` exported to `192.168.0.0/16` (rw, all_squash to uid/gid 1000)

**Media directory:** `/mnt/storage/media/`
- `downloads/` - qBittorrent download destination
- `movies/` - Radarr-managed movie library
- `shows/` - Sonarr-managed TV library
- `music/` - Lidarr-managed music library
- `transcode/` - Transcoding workspace

### Docker Stack

Compose file: `/home/stan/docker/docker-compose.yml`
Config dir: `/home/stan/docker/config/`

#### Media Acquisition

| Container | Port | Purpose |
|-----------|------|---------|
| prowlarr | 9696 | Indexer manager (feeds Sonarr/Radarr) |
| qbittorrent | 8085 | Torrent client (WebUI) |
| slskd | 5030 | Soulseek P2P client (WebUI), peer port 50300 |
| flaresolverr | 8191 | Cloudflare bypass for Prowlarr |
| overseerr | 5055 | Media request UI |

#### Media Management

| Container | Port | Purpose |
|-----------|------|---------|
| sonarr | 8989 | TV show automation |
| radarr | 7878 | Movie automation |
| lidarr | 8686 | Music automation |
| soularr | - | Lidarr↔Slskd bridge (polls every 5min) |

#### Infrastructure

| Container | Port | Purpose |
|-----------|------|---------|
| homepage | 3000 | Dashboard |
| file-browser | 8080 | Web file manager (serves `/mnt/`) |
| postgres | 5432 | PostgreSQL 17 with pgvector (data on disk2) |
| cloudbeaver | 3011 | DB web admin (connects to postgres) |

### Quick Reference

```bash
ssh homelab 'sudo docker ps --format "table {{.Names}}\t{{.Status}}"'
ssh homelab 'cd /home/stan/docker && sudo docker compose up -d'
ssh homelab 'cd /home/stan/docker && sudo docker compose restart sonarr'
ssh homelab 'cd /home/stan/docker && sudo docker compose logs --tail 50 radarr'
ssh homelab 'df -h /mnt/storage /mnt/disk1 /mnt/disk2'
ssh homelab 'ls /home/stan/docker/config/'
```

## Mac Mini (macOS)

### Connection

| Field | Value |
|-------|-------|
| Host alias | `mini` (configured in `~/.ssh/config`) |
| IP | `192.168.0.155` |
| User | `stan` |
| Hostname | `mini` |
| OS | macOS 26.3 (Apple M4, 16GB RAM) |
| Disk | 228GB SSD (14% used) |

### Storage

| Mount | Source | Path |
|-------|--------|------|
| NFS | `192.168.0.2:/mnt/storage` | `/Volumes/Media` |
| Local | Internal SSD | `/` |

Media files live on the homelab and are accessed via NFS at `/Volumes/Media/media/`.

### Plex Media Server

Running natively (not Docker), v1.43.0.

| Field | Value |
|-------|-------|
| Data dir | `~/Library/Application Support/Plex Media Server/` |
| API (local) | `http://localhost:32400` |
| API (network) | `http://192.168.0.155:32400` |
| Token | `defaults read com.plexapp.plexmediaserver PlexOnlineToken` |

#### Libraries

| ID | Type | Name |
|----|------|------|
| 1 | movie | Movies |
| 2 | show | TV Shows |
| 3 | artist | Music |

#### Plex API Quick Reference

All requests require `?X-Plex-Token=TOKEN` and `-H "Accept: application/json"`.

```bash
TOKEN=$(ssh mini 'defaults read com.plexapp.plexmediaserver PlexOnlineToken')

ssh mini "curl -s 'http://localhost:32400/library/sections?X-Plex-Token=$TOKEN' -H 'Accept: application/json'"
ssh mini "curl -s 'http://localhost:32400/library/sections/3/all?X-Plex-Token=$TOKEN' -H 'Accept: application/json'"
ssh mini "curl -s 'http://localhost:32400/status/sessions?X-Plex-Token=$TOKEN' -H 'Accept: application/json'"
ssh mini "curl -s 'http://localhost:32400/status/sessions/history/all?X-Plex-Token=$TOKEN' -H 'Accept: application/json'"
ssh mini "curl -s 'http://localhost:32400/status/sessions/history/all?librarySectionID=3&X-Plex-Token=$TOKEN' -H 'Accept: application/json'"
```

### macOS Notes

- No `apt` — use `softwareupdate` for OS updates
- No Homebrew or Docker installed — lean media server
- App preferences via `defaults read/write com.app.name`
- Services via `launchctl list`, `launchctl start/stop`

## Shared Notes

**Running commands:** Use the Bash tool with `ssh <alias>` prefix. All commands run non-interactively.

```bash
ssh homelab 'command'                         # Single command
ssh mini 'cd /path && command'                # Chained
ssh homelab 'docker logs app 2>&1 | tail -50' # Pipes
```

**File transfer:**

```bash
scp /local/file homelab:/remote/path          # Upload
scp mini:/remote/file /local/path             # Download
scp -r homelab:/remote/dir /local/dir         # Directory
```

**Limitations:**
- Docker on homelab requires `sudo` (stan is not in docker group)
- Interactive commands (vim, top, htop) do NOT work — use non-interactive alternatives
- For `top`: `ssh homelab 'top -b -n1 | head -20'`
- Long-running commands: use `run_in_background` on the Bash tool
- Web UIs accessible at `192.168.0.2:<port>` (homelab) or `192.168.0.155:<port>` (mini) from the local network
