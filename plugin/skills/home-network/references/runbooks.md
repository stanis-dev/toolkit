# Runbooks

Each block is complete on its own. Every stan-lab docker command needs `sudo -n`.

## Plex shows media unavailable (NFS mount dropped)

```sh
ssh mini 'launchctl kickstart -k gui/501/com.stan.media-mount; sleep 8; df -h /Volumes/disk2 /Volumes/disk1'
ssh mini 'curl -s "http://localhost:32400/library/sections/all/refresh?X-Plex-Token=$(defaults read com.plexapp.plexmediaserver PlexOnlineToken)"'
```

Done when `df` lists `192.168.0.2:/mnt/disk2` on `/Volumes/disk2` and the Plex library shows items again. Run this after any stan-lab reboot too. Permanent fix, staged on the mini and not yet run (needs sudo at the keyboard): `ssh -t mini 'sudo /Users/stan/fix-media-mounts.sh'`.

## Downloads stopped after a VPN blip

```sh
ssh homelab 'sudo -n docker exec gluetun ip route show table 51820'        # expect: default dev tun0
ssh homelab 'sudo -n docker restart qbittorrent slskd'
ssh homelab 'sudo -n journalctl -u gluetun-watchdog -n 20 --no-pager'      # what the watchdog already did
```

Signature and mechanism in [media-stack.md](media-stack.md). If the route table has no tun0 line, gluetun itself is down: `sudo -n docker logs gluetun --tail 50`.

## Deploy Sayya

```sh
ssh homelab 'cd ~/dev/sayya \
  && sudo -n docker exec sayya-server-1 cat /data/sayya.db > ~/sayya-db-backup-$(date +%F).db \
  && git pull \
  && sudo -n docker compose up -d --build \
  && sleep 5 && curl -s localhost:8090/healthz'
```

`git pull` before the build is mandatory: the box has its own checkout, and building without it redeploys the old binary (new routes 404 while `/healthz` stays 200). If the build fails on a Docker Hub timeout: `sudo -n DOCKER_BUILDKIT=0 docker build -t sayya-server:local ./server && sudo -n docker compose up -d`. Confirm the public site in a browser; curl against https://saya.stan-lab.net can get 403 from Cloudflare bot protection.

## Deploy cima

```sh
scp ~/code/cima/.env homelab:dev/cima/.env      # only when .env changed
ssh homelab 'cd ~/dev/cima && git pull && sudo -n docker compose up -d --build && sudo -n docker compose ps'
```

Verify on the LAN at http://192.168.0.2:4100 and publicly at https://cima.stan-lab.net using the health path documented in `~/code/cima/CLAUDE.md`. The public route rides the Sayya `cloudflared` container, so if Sayya's compose project is down, cima is unreachable from outside too.

## After a stan-lab reboot

Every container in the three compose projects has `restart: unless-stopped`, so they return on their own. The mini's NFS mounts go stale and need the Plex remount block. The host-level `cloudflared.service` resumes its restart loop.

## Rotate the headless Claude token (yearly)

On the MacBook run `claude setup-token`, then `~/.claude/remote-auth/deploy-token.sh` and paste the token; the script deploys it to both boxes and probes each with a haiku call.

## jobr did not run or produced nothing

```sh
ssh mini 'ls -t ~/dev/jobr/logs | head -3; tail -40 ~/dev/jobr/logs/daily-$(date +%F).log'
```

Manual run: `ssh mini 'zsh ~/dev/jobr/run-daily.sh'`. The launchd exit code is always wrong because of the `status=$?` defect; read the log instead. A LinkedIn login wall in the log means `linkedin_state.json` expired; see [mini.md](mini.md).
