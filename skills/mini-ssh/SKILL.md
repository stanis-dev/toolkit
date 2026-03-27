---
name: mini-ssh
description: Use when the user asks to perform tasks on their Mac Mini, Plex server, or media server - includes SSH connection details, Plex API reference, and macOS command patterns
---

# Mac Mini SSH

## Connection

| Field | Value |
|-------|-------|
| Host alias | `mini` (configured in `~/.ssh/config`) |
| IP | `192.168.0.155` |
| User | `stan` |
| Hostname | `mini` |
| OS | macOS 26.3 (Apple M4, 16GB RAM) |
| Disk | 228GB SSD (14% used) |
| Auth | SSH key (`~/.ssh/id_ed25519`) |

## Running Commands

```bash
ssh mini 'command'                     # Single command
ssh mini 'cd /path && command'         # Chained
```

## Storage

| Mount | Source | Path |
|-------|--------|------|
| NFS | `192.168.0.2:/mnt/storage` | `/Volumes/Media` |
| Local | Internal SSD | `/` |

Media files live on the homelab and are accessed via NFS at `/Volumes/Media/media/`.

## Plex Media Server

Running natively (not Docker), v1.43.0.

| Field | Value |
|-------|-------|
| Data dir | `~/Library/Application Support/Plex Media Server/` |
| API (local) | `http://localhost:32400` |
| API (network) | `http://192.168.0.155:32400` |
| Token | `defaults read com.plexapp.plexmediaserver PlexOnlineToken` |

### Libraries

| ID | Type | Name |
|----|------|------|
| 1 | movie | Movies |
| 2 | show | TV Shows |
| 3 | artist | Music |

### Plex API Quick Reference

All requests require `?X-Plex-Token=TOKEN` and `-H "Accept: application/json"`.

```bash
# Get token first
TOKEN=$(ssh mini 'defaults read com.plexapp.plexmediaserver PlexOnlineToken')

# Libraries
ssh mini "curl -s 'http://localhost:32400/library/sections?X-Plex-Token=$TOKEN' -H 'Accept: application/json'"

# All music artists
ssh mini "curl -s 'http://localhost:32400/library/sections/3/all?X-Plex-Token=$TOKEN' -H 'Accept: application/json'"

# Currently playing
ssh mini "curl -s 'http://localhost:32400/status/sessions?X-Plex-Token=$TOKEN' -H 'Accept: application/json'"

# Play history (all)
ssh mini "curl -s 'http://localhost:32400/status/sessions/history/all?X-Plex-Token=$TOKEN' -H 'Accept: application/json'"

# Play history (music only)
ssh mini "curl -s 'http://localhost:32400/status/sessions/history/all?librarySectionID=3&X-Plex-Token=$TOKEN' -H 'Accept: application/json'"
```

## macOS-Specific Notes

- No `apt` - use `softwareupdate` for OS updates
- No Homebrew or Docker installed - this is a lean media server
- App preferences via `defaults read/write com.app.name`
- Services via `launchctl list`, `launchctl start/stop`
- Interactive commands do NOT work via Bash tool - use non-interactive alternatives
