# stan-lab (ssh homelab, 192.168.0.2)

Ubuntu 24.04 on an Intel N97 with 16 GB RAM, wired on `enp2s0`. Docker is the snap package: `sudo -n docker ...` always.

## Disks

| Mount | Size | Holds |
|---|---|---|
| `/` | 466 GB NVMe | OS, docker root, configs |
| `/mnt/disk1` | 4 TB | `Downloads/`, shared storage |
| `/mnt/disk2` | 11 TB | `media/{movies,shows,music,downloads}`, `jobs-db/` (Postgres data) |

`/etc/exports` shares both data disks to 192.168.0.0/16 with `all_squash` to uid/gid 1000, so files written from the mini land as stan. The mini mounts them at `/Volumes/disk2` and `/Volumes/disk1`.

## Compose projects

| Project | Path | Services |
|---|---|---|
| `docker` (main) | `~/docker/docker-compose.yml` | homeassistant, homepage, gluetun, qbittorrent, slskd, flaresolverr, soulsync, sonarr, radarr, prowlarr, seerr (service name `overseerr`), postgres, cloudbeaver, file-browser |
| sayya | `~/dev/sayya/docker-compose.yml` | `server` (image `sayya-server:local`, 127.0.0.1:8090) + `cloudflared` sidecar |
| cima | `~/dev/cima/compose.yml` | `cima` (4100) + `db` (pgvector pg17 on 5433); joins external network `sayya_default` so the Sayya tunnel routes `http://cima:4100` |

Main-project config paths: `~/docker/config/<service>` for gluetun, qbittorrent, sonarr, radarr, prowlarr, slskd, soulsync, homeassistant. Exceptions: homepage `~/docker/homepage-config`, seerr `~/docker/overseerconfig`, file-browser `~/docker/file-browser`, cloudbeaver `~/docker/cloudbeaver-data`, postgres init `~/docker/workflows/init.sql`. Media bind mounts are tabled in [media-stack.md](media-stack.md). File Browser serves `/mnt` as `/srv`.

## Postgres (5432)

Data at `/mnt/disk2/jobs-db`. DB `jobr` is written by the mini's jobr pipeline: live tables `raw_jobs`, `job_analysis`, `companies`; `filtered_jobs` and `good_fits` are dead. Credentials are the `PG*` keys in `~/dev/jobr/.env` on the mini. CloudBeaver on 3011 is the web UI. The cima project has its own Postgres on 5433.

## Sayya

Go server on 8090, loopback only; public at https://saya.stan-lab.net through the `cloudflared` sidecar (dashboard-managed token `TUNNEL_TOKEN` in gitignored `.env`). Stateful: SQLite in named volume `sayya_sayya-data`, holding articles and reader state. `.env` also carries `READER_TOKEN`, which the iOS client hardcodes. The Cloudflare zone runs bot protection, so curl can get 403 on public paths that a browser gets 200 on; check health on the box with `curl -s localhost:8090/healthz`. The daily writer cron's source of truth is `ops/sayya-grow-feed.sh` in the repo, installed to `~/.local/bin`; its state is in `~/.local/state/sayya/`. Deploy steps in [runbooks.md](runbooks.md).

## cima

Public at https://cima.stan-lab.net. `.env` carries `CLAUDE_CODE_OAUTH_TOKEN` (the server calls Claude). Volumes `cima-pg`, `cima-logs`. Repo checkout on the box is `~/dev/cima`; the MacBook checkout is `~/code/cima`, whose CLAUDE.md documents the deployment contract.

## Host services outside Docker

- `gluetun-watchdog.service`: script `/usr/local/bin/gluetun-watchdog.sh`, logs `journalctl -u gluetun-watchdog`. Behaviour in [media-stack.md](media-stack.md).
- `cloudflared.service` (host level, `/etc/systemd/system/cloudflared.service`, token inline): restart loop, purpose undocumented, unused by the two public hostnames.

## Home directory landmarks

`~/dev/` holds `sayya`, `cima`, `jobr` (old checkout; the runner is on the mini), `dotfiles`, `lab` (2025 mount notes), `subtitle-translator`. Dated backups of the docker root, Postgres dumps, the Sayya SQLite and Home Assistant dashboards sit in `~`, some root-owned.
