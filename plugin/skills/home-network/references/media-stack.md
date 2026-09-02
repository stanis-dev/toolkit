# Media and download stack (stan-lab)

All in the main compose project `~/docker/docker-compose.yml`. Plex on the Mac mini consumes the results over NFS.

## Topology

`gluetun` (NordVPN WireGuard, Spain) owns the published ports 5030 and 50300 (slskd), 8085 and 61881 plus 6881/udp (qBittorrent), 8191 (FlareSolverr). It also runs an HTTP proxy on 8888 inside the container only; host ports 8888-8889 belong to soulsync. `qbittorrent`, `slskd` and `flaresolverr` use `network_mode: service:gluetun`, so from the LAN they answer on 192.168.0.2 at those ports and inside the compose network they are reached as `gluetun:<port>`.

`sonarr`, `radarr`, `prowlarr`, `seerr`, `soulsync` sit on the default bridge. Prowlarr's app-level proxy is `http://gluetun:8888` with bypass `localhost,127.0.0.1,192.168.0.*,10.5.5.*`; the Spanish ISP blocks public trackers (connections hang), so indexer traffic must exit via the VPN. Cloudflare-fronted indexers (1337x, EZTV, BT.etree, others) carry Prowlarr's FlareSolverr tag with URL `http://192.168.0.2:8191`. Active public indexers include Knaben, YTS, LimeTorrents; kickasstorrents.to is dead in every mirror; apibay (TPB) rate-limits after repeated tests.

## Paths

| Container | Host path | In container |
|---|---|---|
| qbittorrent, sonarr, radarr | `/mnt/disk2/media/downloads` | `/downloads` |
| sonarr | `/mnt/disk2/media/shows` | `/media/tv` |
| radarr | `/mnt/disk2/media/movies` | `/media/movies` |
| slskd | `/mnt/disk2/media/downloads/slskd`, `/mnt/disk2/media/music` | `/downloads`, `/music` |
| soulsync | `/mnt/disk2/media/downloads/slskd`, `/mnt/disk2/media/music`, `~/docker/config/soulsync/staging` | `/app/downloads`, `/app/Transfer`, `/app/Staging` |

## Failure signature: VPN self-restart strands the apps

gluetun runs `HEALTH_RESTART_VPN=on`; on a health failure it rebuilds tun0 inside the running container, and the apps sharing its namespace keep dead sockets. qBittorrent: `connection_status: firewalled`, `dht_nodes: 0`, magnets stuck in `metaDL`, udp trackers "Operation not permitted". slskd: server stuck "Disconnecting", searches error. Fresh egress tests from inside gluetun pass while the apps stay dead. gluetun takes about two minutes of retries before it reports unhealthy.

Fix: confirm the tunnel is up with `sudo -n docker exec gluetun ip route show table 51820` (expect `default dev tun0`), then `sudo -n docker restart qbittorrent slskd`.

`gluetun-watchdog.service` on the host does this automatically: gluetun `unhealthy`, `restart` or `start` docker events arm it, and the next `health_status: healthy` fires the restart. Normal boots do not trigger it. Script `/usr/local/bin/gluetun-watchdog.sh` (uses `/snap/bin/docker` absolute path), logs `journalctl -u gluetun-watchdog`.
