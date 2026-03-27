#!/usr/bin/env python3
"""
Create a Plex playlist from an ordered list of tracks.

Runs on the homelab. Zero external dependencies (stdlib only).
Searches Plex for each track by title+artist, creates the playlist,
and adds tracks in the specified order.

Usage:
    python3 create_playlist.py --plex-token TOKEN --playlist-name "Work Flow" \
        --tracks '[{"artist":"Mac Miller","track":"Surf"},{"artist":"Kiasmos","track":"Looped"}]'
    python3 create_playlist.py --plex-token TOKEN --playlist-name "Work Flow" \
        --tracks '[...]' --retry-missing
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse

PLEX_MUSIC_SECTION = 3


def plex_get(base_url, token, path):
    url = f"{base_url}{path}{'&' if '?' in path else '?'}X-Plex-Token={token}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def plex_post(base_url, token, path):
    url = f"{base_url}{path}{'&' if '?' in path else '?'}X-Plex-Token={token}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def plex_put(base_url, token, path):
    url = f"{base_url}{path}{'&' if '?' in path else '?'}X-Plex-Token={token}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"}, method="PUT")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def get_machine_id(base_url, token):
    data = plex_get(base_url, token, "/identity")
    return data["MediaContainer"]["machineIdentifier"]


def search_track(base_url, token, artist, track_title):
    """Search Plex for a track, return best match ratingKey or None."""
    query = urllib.parse.quote(track_title)
    data = plex_get(
        base_url, token,
        f"/library/sections/{PLEX_MUSIC_SECTION}/search?type=10&query={query}"
    )
    items = data.get("MediaContainer", {}).get("Metadata", [])
    if not items:
        return None, None

    artist_lower = artist.lower()
    for item in items:
        item_artist = item.get("grandparentTitle", "").lower()
        item_title = item.get("title", "").lower()
        if artist_lower in item_artist and track_title.lower() in item_title:
            return item.get("ratingKey"), f"{item.get('grandparentTitle', '')} - {item.get('title', '')}"

    for item in items:
        item_artist = item.get("grandparentTitle", "").lower()
        if artist_lower in item_artist or item_artist in artist_lower:
            return item.get("ratingKey"), f"{item.get('grandparentTitle', '')} - {item.get('title', '')}"

    first = items[0]
    return first.get("ratingKey"), f"{first.get('grandparentTitle', '')} - {first.get('title', '')} (best guess)"


def create_playlist(base_url, token, machine_id, name, first_rating_key):
    uri = f"server://{machine_id}/com.plexapp.plugins.library/library/metadata/{first_rating_key}"
    encoded_name = urllib.parse.quote(name)
    data = plex_post(
        base_url, token,
        f"/playlists?type=audio&title={encoded_name}&smart=0&uri={uri}"
    )
    playlist_id = data.get("MediaContainer", {}).get("Metadata", [{}])[0].get("ratingKey")
    return playlist_id


def add_to_playlist(base_url, token, machine_id, playlist_id, rating_key):
    uri = f"server://{machine_id}/com.plexapp.plugins.library/library/metadata/{rating_key}"
    plex_put(base_url, token, f"/playlists/{playlist_id}/items?uri={uri}")


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def resolve_tracks(base_url, token, tracks):
    """Search Plex for each track, return (found, missing) lists."""
    found = []
    missing = []

    for i, t in enumerate(tracks, 1):
        artist = t.get("artist", "")
        track_title = t.get("track", "")
        log(f"  [{i}/{len(tracks)}] {artist} - {track_title}")

        rating_key, matched_name = search_track(base_url, token, artist, track_title)
        if rating_key:
            log(f"    Found: {matched_name} (key={rating_key})")
            found.append({"artist": artist, "track": track_title, "rating_key": rating_key, "matched": matched_name})
        else:
            log(f"    NOT FOUND")
            missing.append({"artist": artist, "track": track_title})

    return found, missing


def main():
    parser = argparse.ArgumentParser(description="Create a Plex playlist from track list")
    parser.add_argument("--plex-url", default="http://192.168.0.155:32400")
    parser.add_argument("--plex-token", required=True)
    parser.add_argument("--playlist-name", required=True)
    parser.add_argument("--tracks", required=True, help="JSON array of ordered {artist, track} objects")
    parser.add_argument("--retry-missing", action="store_true", help="Wait 30s and retry tracks not found on first pass")
    args = parser.parse_args()

    tracks = json.loads(args.tracks)
    log(f"Creating playlist '{args.playlist_name}' with {len(tracks)} tracks\n")

    log("Getting Plex machine identifier...")
    machine_id = get_machine_id(args.plex_url, args.plex_token)
    log(f"  Machine: {machine_id}\n")

    log("Searching for tracks in Plex...")
    found, missing = resolve_tracks(args.plex_url, args.plex_token, tracks)

    if missing and args.retry_missing:
        log(f"\n{len(missing)} tracks not found. Waiting 30s for Plex scan, then retrying...")
        time.sleep(30)
        retry_found, still_missing = resolve_tracks(args.plex_url, args.plex_token, missing)
        found.extend(retry_found)
        missing = still_missing

    if not found:
        log("\nNo tracks found in Plex. Cannot create playlist.")
        print(json.dumps({"status": "no_tracks_found", "missing": missing}, indent=2))
        sys.exit(1)

    log(f"\nCreating playlist with {len(found)} tracks...")
    first = found[0]
    playlist_id = create_playlist(
        args.plex_url, args.plex_token, machine_id,
        args.playlist_name, first["rating_key"]
    )
    log(f"  Playlist created: ID={playlist_id}")

    for track in found[1:]:
        try:
            add_to_playlist(
                args.plex_url, args.plex_token, machine_id,
                playlist_id, track["rating_key"]
            )
        except Exception as e:
            log(f"  Warning: failed to add {track['artist']} - {track['track']}: {e}")
            missing.append({"artist": track["artist"], "track": track["track"], "error": str(e)})

    output = {
        "status": "created",
        "playlist_id": playlist_id,
        "playlist_name": args.playlist_name,
        "tracks_added": len(found) - len([m for m in missing if "error" in m]),
        "tracks_missing": len(missing),
        "added": [{"artist": t["artist"], "track": t["track"], "matched": t["matched"]} for t in found],
        "missing": missing,
    }

    log(f"\nDone! {output['tracks_added']} tracks added, {output['tracks_missing']} missing")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
