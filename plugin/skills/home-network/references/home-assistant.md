# Home Assistant (http://192.168.0.2:8123)

HA Container 2026.8.2, container `homeassistant` in the main compose project on stan-lab, `network_mode: host`, plain HTTP. Config bind mount `~/docker/config/homeassistant` on the box, root-owned: read and write with `sudo -n`. Log `home-assistant.log`; registries and dashboards in `.storage/`. Plain HTTP means the browser microphone does not work against it; the iPhone app does. HTTPS is deferred.

## Integrations and devices

| Device | Integration | Notes |
|---|---|---|
| Hue Bridge 192.168.0.243 | Hue | rooms Salón, Dormitorio, Despacho (device-registry model "Room") |
| LG C2 192.168.0.133 | webOS TV + Wake-on-LAN automation | MAC 20:28:bc:80:27:1a; Quick Start+ must stay on |
| Apple TV 192.168.0.45 | Apple TV | |
| WiiM Ultra 192.168.0.99 | WiiM / LinkPlay | volume slider on the dashboard |
| Dreo DR-HPF008S fan | hass-dreo custom component (cloud polling) | four `script.fan_point_*` angle nudgers |
| Mac mini speech server 192.168.0.155:10300 | Wyoming | Assist pipeline with the built-in `conversation.home_assistant` agent; no LLM by decision |

## TV control

Switch inputs by webOS app id, never by source label: two HDMI inputs share the label "Apple OTT", so `select_source` collides. Shape: `webostv.command` with `command: system.launcher/launch`, `payload: {id: com.webos.app.hdmi1}` (hdmi3 likewise). Inputs: HDMI1 Mac mini, HDMI2 WiiM, HDMI3 Apple TV, HDMI4 unused. Scripts: `script.tv_toggle` (power), `script.tv_hdmi1`, `script.tv_hdmi3`; the HDMI scripts wake the TV first and wait for state `on` plus 2 s. In real standby the TV only answers after a WOL magic packet to its MAC (several retries).

Direct poke from the box: python3 inside the `homeassistant` container with `aiowebostv`; the client key is in the webostv config entry.

## Dashboard

Single view "Home", `type: sections`, `max_columns: 2`, theme "Catppuccin Auto Latte Mocha". Sections: Salón (all-lights card, brightness, scene chips Relax/Concentrate/Read, WiiM volume, three TV buttons), Ventilador (fan card, direction nudges, oscillation toggles), Luces (Dormitorio/Despacho/Casa toggles).

No HACS. Custom cards live in `config/www/` with a hand-written `.storage/lovelace_resources` entry: Mushroom 5.1.1 (`/local/mushroom.js?v=5.1.1`) and vertical-stack-in-card 1.0.1 (the only way to get one bordered, titled card wrapping others; it reaches into children's shadow DOM, so suspect it first after any frontend upgrade).

Edit ritual (the dashboard is stored, not YAML): write `.storage/lovelace.lovelace` (that exact key; the legacy `.storage/lovelace` is dead), validate the JSON locally, scp to the box, `sudo -n docker compose stop homeassistant` in `~/docker`, mv the file into `.storage`, `chown root:root` and `chmod 600`, start, sleep 20, then confirm `curl` returns 200 and `home-assistant.log` has nothing beyond bluetooth noise (`grep -viE "bluetooth|habluetooth|bleak|Unclosed"`). Rollbacks: `~/lovelace.lovelace.bak-*` and `~/lovelace_resources.bak-boxes` on the box. Scripts are in `config/scripts.yaml`.

## Verify before relying on it

`internal_url` was observed unset, which made HA advertise a Docker bridge address (172.19.0.1) over mDNS for first-time app onboarding. Intended fix: `internal_url: http://192.168.0.2:8123` in `configuration.yaml` and zeroconf restricted to `enp2s0`. Check `core.config` in `.storage` before onboarding a new client.

## Planned client

A sofa-side tablet (Xiaomi Pad 8 recommended) running Fully Kiosk against this dashboard, docked landscape, black screensaver at backlight 0 instead of screen-off. Not purchased as of the snapshot.
