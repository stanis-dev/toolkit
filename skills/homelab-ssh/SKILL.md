---
name: homelab-ssh
description: Use when the user asks to perform tasks on their homelab, Linux server, or remote machine - includes SSH connection details, media stack, storage layout, and command patterns
---

# Homelab SSH

## Connection

| Field | Value |
|-------|-------|
| Host alias | `homelab` (configured in `~/.ssh/config`) |
| IP | `192.168.0.2` |
| User | `stan` |
| Hostname | `stan-lab` |
| OS | Ubuntu 24.04 LTS (x86_64) |
| Auth | SSH key (`~/.ssh/id_ed25519`) |
| Docker | 28.4.0 with Compose v2.39.1 (requires `sudo`) |

## Running Commands

Use the Bash tool with `ssh homelab` prefix. All commands run non-interactively.

```bash
ssh homelab 'command'                        # Single command
ssh homelab 'cd /path && command'            # Chained
ssh homelab 'docker logs app 2>&1 | tail -50' # Pipes
```

## Storage

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

## Docker Stack

Compose file: `/home/stan/docker/docker-compose.yml`
Config dir: `/home/stan/docker/config/`

### Media Acquisition
| Container | Port | Purpose |
|-----------|------|---------|
| prowlarr | 9696 | Indexer manager (feeds Sonarr/Radarr) |
| qbittorrent | 8085 | Torrent client (WebUI) |
| slskd | 5030 | Soulseek P2P client (WebUI), peer port 50300 |
| flaresolverr | 8191 | Cloudflare bypass for Prowlarr |
| overseerr | 5055 | Media request UI |

### Media Management
| Container | Port | Purpose |
|-----------|------|---------|
| sonarr | 8989 | TV show automation |
| radarr | 7878 | Movie automation |
| lidarr | 8686 | Music automation |
| soularr | - | Lidarr↔Slskd bridge (polls every 5min) |

### Infrastructure
| Container | Port | Purpose |
|-----------|------|---------|
| homepage | 3000 | Dashboard |
| file-browser | 8080 | Web file manager (serves `/mnt/`) |
| postgres | 5432 | PostgreSQL 17 with pgvector (data on disk2) |
| cloudbeaver | 3011 | DB web admin (connects to postgres) |

### Quick Reference
```bash
# All containers
ssh homelab 'sudo docker ps --format "table {{.Names}}\t{{.Status}}"'

# Compose operations (from compose dir)
ssh homelab 'cd /home/stan/docker && sudo docker compose up -d'
ssh homelab 'cd /home/stan/docker && sudo docker compose restart sonarr'
ssh homelab 'cd /home/stan/docker && sudo docker compose logs --tail 50 radarr'

# Storage check
ssh homelab 'df -h /mnt/storage /mnt/disk1 /mnt/disk2'

# Container config
ssh homelab 'ls /home/stan/docker/config/'
```

## File Transfer

```bash
scp /local/file homelab:/remote/path           # Upload
scp homelab:/remote/file /local/path           # Download
scp -r homelab:/remote/dir /local/dir          # Directory
```

## Important Notes

- Docker requires `sudo` (stan is not in docker group)
- Interactive commands (vim, top, htop) do NOT work - use non-interactive alternatives
- For `top`: `ssh homelab 'top -b -n1 | head -20'`
- Long-running commands: use `run_in_background` on the Bash tool
- Web UIs accessible at `192.168.0.2:<port>` from the local network
