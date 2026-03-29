#!/usr/bin/env python3
"""
Download tracks and create a Plex playlist via SoulSync's mirrored playlist pipeline.

Runs on the homelab. Zero external dependencies (stdlib only).
Uses SoulSync's full pipeline: mirror playlist -> discover metadata -> sync
(library match + download missing + create Plex playlist).

This ensures tracks go through SoulSync's metadata discovery (iTunes/Spotify)
before any Soulseek search, producing rich metadata that leads to better
search queries, accurate quality filtering, and proper library dedup.

Usage:
    python3 sync_playlist.py --playlist-name "Evening Vibes" \
        --tracks '[{"artist":"Erykah Badu","track":"Otherside of the Game","album":"Baduizm"}]'

    python3 sync_playlist.py --playlist-name "Evening Vibes" \
        --tracks-file /tmp/tracks.json --timeout 1800
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

SOULSYNC_URL = "http://localhost:8008"
POLL_INTERVAL = 5
DEFAULT_TIMEOUT = 1200

_session_cookie = None


def _request(path, method="GET", data=None, base=None):
    url = f"{base or SOULSYNC_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    if _session_cookie:
        req.add_header("Cookie", f"session={_session_cookie}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode() if e.fp else ""
        try:
            return json.loads(body_text)
        except (json.JSONDecodeError, ValueError):
            return {"error": {"code": str(e.code), "message": body_text}}
    except Exception as e:
        return {"error": {"code": "REQUEST_FAILED", "message": str(e)}}


def get_session():
    global _session_cookie
    url = f"{SOULSYNC_URL}/api/profiles/select"
    body = json.dumps({"profile_id": 1}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            for header in resp.getheader("Set-Cookie", "").split(","):
                for part in header.split(";"):
                    part = part.strip()
                    if part.startswith("session="):
                        _session_cookie = part[len("session="):]
                        return True
    except Exception as e:
        log(f"  Failed to get session: {e}")
    return False


def log(msg):
    print(msg, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Step 1: Create mirrored playlist
# ---------------------------------------------------------------------------

def create_mirrored_playlist(name, tracks):
    playlist_tracks = []
    for t in tracks:
        playlist_tracks.append({
            "track_name": t.get("track", ""),
            "artist_name": t.get("artist", ""),
            "album_name": t.get("album", ""),
            "duration_ms": 0,
            "image_url": None,
            "source_track_id": "",
            "extra_data": None,
        })

    source_id = f"agent_{int(time.time())}"
    resp = _request("/api/mirror-playlist", method="POST", data={
        "source": "file",
        "source_playlist_id": source_id,
        "name": name,
        "tracks": playlist_tracks,
        "description": f"Agent sync: {len(tracks)} tracks",
        "owner": "agent",
        "image_url": "",
    })

    playlist_id = resp.get("playlist_id")
    if not playlist_id:
        return None, resp.get("error", str(resp))
    return playlist_id, None


# ---------------------------------------------------------------------------
# Step 2: Discovery -- resolve each track to real iTunes/Spotify metadata
# ---------------------------------------------------------------------------

def run_discovery(playlist_id, timeout):
    url_hash = f"mirrored_{playlist_id}"

    resp = _request(f"/api/mirrored-playlists/{playlist_id}/prepare-discovery", method="POST")
    if not resp.get("success"):
        return None, f"prepare-discovery failed: {resp}"

    resp = _request(f"/api/youtube/discovery/start/{url_hash}", method="POST")
    if not resp.get("success"):
        return None, f"discovery/start failed: {resp}"

    start = time.time()
    while time.time() - start < timeout:
        status = _request(f"/api/youtube/discovery/status/{url_hash}")
        phase = status.get("phase", "")
        progress = status.get("progress", 0)
        matches = status.get("spotify_matches", 0)
        results = status.get("results", [])
        total = len(results) if results else status.get("total_tracks", "?")

        log(f"  [{time.time() - start:.0f}s] phase={phase} progress={progress}% matches={matches}/{total}")

        if phase == "discovered":
            discovered = []
            not_resolved = []
            for r in results:
                label = f"{r.get('yt_artist', '?')} - {r.get('yt_track', '?')}"
                if r.get("status_class") == "found":
                    sp_label = f"{r.get('spotify_artist', '')} - {r.get('spotify_track', '')} [{r.get('spotify_album', '')}]"
                    discovered.append({"input": label, "resolved": sp_label, "confidence": r.get("confidence", 0)})
                else:
                    not_resolved.append(label)

            return {
                "discovered": len(discovered),
                "not_resolved": len(not_resolved),
                "discovered_tracks": discovered,
                "not_resolved_tracks": not_resolved,
            }, None

        if phase in ("error", "failed"):
            return None, f"Discovery failed: {status}"

        time.sleep(POLL_INTERVAL)

    return None, "Discovery timed out"


# ---------------------------------------------------------------------------
# Step 3: Sync -- library match + download missing + create Plex playlist
# ---------------------------------------------------------------------------

def run_sync(playlist_id, timeout):
    url_hash = f"mirrored_{playlist_id}"

    resp = _request(f"/api/youtube/sync/start/{url_hash}", method="POST")
    if not resp.get("success"):
        return None, f"sync/start failed: {resp}"

    start = time.time()
    last_log = ""
    while time.time() - start < timeout:
        status = _request(f"/api/youtube/sync/status/{url_hash}")
        phase = status.get("phase", "")
        sync_status = status.get("sync_status", "")
        complete = status.get("complete", False)
        progress = status.get("progress", {})

        if isinstance(progress, dict):
            matched = progress.get("matched_tracks", "?")
            failed = progress.get("failed_tracks", "?")
            downloaded = progress.get("downloaded_tracks", "?")
            total = progress.get("total_tracks", "?")
            summary = f"phase={phase} matched={matched} failed={failed} downloaded={downloaded} total={total}"
        else:
            summary = f"phase={phase} sync_status={sync_status}"

        if summary != last_log:
            log(f"  [{time.time() - start:.0f}s] {summary}")
            last_log = summary

        if complete or sync_status == "finished":
            result = progress if isinstance(progress, dict) else {}
            return {
                "status": "completed",
                "matched": result.get("matched_tracks", 0),
                "failed": result.get("failed_tracks", 0),
                "downloaded": result.get("downloaded_tracks", 0),
                "total": result.get("total_tracks", 0),
                "playlist_name": result.get("playlist_name", ""),
            }, None

        time.sleep(POLL_INTERVAL)

    return None, "Sync timed out"


# ---------------------------------------------------------------------------
# Step 4 (optional): Trigger wishlist download for tracks added during sync
# ---------------------------------------------------------------------------

def trigger_wishlist_download():
    resp = _request("/api/wishlist/download_missing", method="POST",
                     data={"force_download_all": False})
    if resp.get("success"):
        return resp.get("batch_id")
    return None


def poll_wishlist_downloads(batch_id, timeout):
    start = time.time()
    settled = 0
    last_log = ""

    while time.time() - start < timeout:
        resp = _request(f"/api/download_status/batch?batch_ids={batch_id}")
        batches = resp.get("batches", {})
        batch = batches.get(batch_id, {})

        if not batch:
            settled += 1
            if settled >= 3:
                log("  Batch cleared (completed)")
                return {"status": "completed"}
            time.sleep(POLL_INTERVAL)
            continue

        settled = 0
        phase = batch.get("phase", "unknown")
        tasks = batch.get("tasks", [])

        active = sum(1 for t in tasks if t.get("status") in
                     ("searching", "downloading", "queued", "pending", "initializing"))
        downloaded = sum(1 for t in tasks if t.get("status") in
                        ("completed", "succeeded"))
        not_found = sum(1 for t in tasks if t.get("status") == "not_found")
        failed = sum(1 for t in tasks if t.get("status") in
                     ("failed", "errored", "cancelled", "permanently_failed"))

        summary = f"phase={phase} active={active} downloaded={downloaded} not_found={not_found} failed={failed}"
        if summary != last_log:
            log(f"  [{time.time() - start:.0f}s] {summary}")
            last_log = summary

        if phase == "complete":
            nf_tracks = [_task_label(t) for t in tasks if t.get("status") == "not_found"]
            fail_tracks = [_task_label(t) for t in tasks
                           if t.get("status") in ("failed", "errored", "cancelled", "permanently_failed")]
            return {
                "status": "completed",
                "downloaded": downloaded,
                "not_found": not_found,
                "not_found_tracks": nf_tracks,
                "failed": failed,
                "failed_tracks": fail_tracks,
            }

        time.sleep(POLL_INTERVAL)

    return {"status": "timeout"}


def _task_label(task):
    info = task.get("track_info") or {}
    name = info.get("name") or info.get("track_name", "?")
    artists = info.get("artists") or info.get("artist", [])
    artist_str = artists[0] if isinstance(artists, list) and artists else str(artists)
    return f"{artist_str} - {name}"


# ---------------------------------------------------------------------------
# Cleanup: delete the mirrored playlist after use
# ---------------------------------------------------------------------------

def delete_mirrored_playlist(playlist_id):
    resp = _request(f"/api/mirrored-playlists/{playlist_id}", method="DELETE")
    return resp.get("success", False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Download tracks via SoulSync mirrored playlist pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tracks", help="JSON array of {artist, track, album} objects")
    group.add_argument("--tracks-file", help="Path to JSON file with track array")
    parser.add_argument("--playlist-name", required=True, help="Name for the Plex playlist")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"Max seconds to wait for downloads (default {DEFAULT_TIMEOUT})")
    parser.add_argument("--keep-mirrored", action="store_true",
                        help="Don't delete the mirrored playlist after completion")
    args = parser.parse_args()

    if args.tracks_file:
        with open(args.tracks_file) as f:
            tracks = json.load(f)
    else:
        tracks = json.loads(args.tracks)

    log(f"SoulSync Pipeline: {len(tracks)} tracks -> '{args.playlist_name}'\n")

    # Authenticate
    log("Step 0: Authenticating...")
    if not get_session():
        log("Failed to get session from SoulSync.")
        print(json.dumps({"status": "auth_failed"}, indent=2))
        sys.exit(1)
    log("  Session acquired\n")

    # Step 1: Create mirrored playlist
    log("Step 1: Creating mirrored playlist...")
    playlist_id, err = create_mirrored_playlist(args.playlist_name, tracks)
    if err:
        log(f"  Failed: {err}")
        print(json.dumps({"status": "mirror_failed", "error": str(err)}, indent=2))
        sys.exit(1)
    log(f"  Playlist ID: {playlist_id}\n")

    # Step 2: Discovery
    discovery_timeout = min(args.timeout // 3, 300)
    log("Step 2: Running metadata discovery (iTunes)...")
    discovery, err = run_discovery(playlist_id, discovery_timeout)
    if err:
        log(f"  Discovery failed: {err}")
        print(json.dumps({"status": "discovery_failed", "error": str(err), "playlist_id": playlist_id}, indent=2))
        sys.exit(1)

    log(f"\n  Discovered: {discovery['discovered']}/{discovery['discovered'] + discovery['not_resolved']}")
    if discovery["not_resolved_tracks"]:
        log(f"  Not resolved ({discovery['not_resolved']}):")
        for name in discovery["not_resolved_tracks"]:
            log(f"    - {name}")
    log("")

    # Step 3: Sync (library match + Plex playlist + wishlist for missing)
    sync_timeout = min(args.timeout // 3, 120)
    log("Step 3: Syncing (library match + Plex playlist)...")
    sync_result, err = run_sync(playlist_id, sync_timeout)
    if err:
        log(f"  Sync failed: {err}")
        print(json.dumps({"status": "sync_failed", "error": str(err), "discovery": discovery}, indent=2))
        sys.exit(1)

    matched = sync_result.get("matched", 0)
    missing = sync_result.get("failed", 0)
    log(f"\n  Matched in library: {matched}")
    log(f"  Missing (added to wishlist): {missing}\n")

    # Step 4: Download missing tracks via wishlist
    download_result = None
    if missing > 0:
        download_timeout = args.timeout - (args.timeout // 3)
        log("Step 4: Downloading missing tracks...")
        batch_id = trigger_wishlist_download()
        if batch_id:
            log(f"  Batch ID: {batch_id}")
            download_result = poll_wishlist_downloads(batch_id, download_timeout)

            downloaded = download_result.get("downloaded", 0)
            not_found = download_result.get("not_found", 0)
            failed = download_result.get("failed", 0)

            log(f"\n  Downloaded: {downloaded}")
            if not_found:
                log(f"  Not found on Soulseek: {not_found}")
                for name in download_result.get("not_found_tracks", []):
                    log(f"    - {name}")
            if failed:
                log(f"  Failed: {failed}")
        else:
            log("  No tracks to download (all matched or wishlist empty)")
    else:
        log("Step 4: Skipped (all tracks already in library)\n")

    # Cleanup
    if not args.keep_mirrored:
        delete_mirrored_playlist(playlist_id)

    # Final output
    output = {
        "status": "completed",
        "playlist_name": args.playlist_name,
        "tracks_requested": len(tracks),
        "discovery": {
            "resolved": discovery["discovered"],
            "not_resolved": discovery["not_resolved"],
            "not_resolved_tracks": discovery["not_resolved_tracks"],
        },
        "sync": {
            "matched_in_library": matched,
            "missing": missing,
        },
    }
    if download_result:
        output["downloads"] = {
            "downloaded": download_result.get("downloaded", 0),
            "not_found": download_result.get("not_found", 0),
            "not_found_tracks": download_result.get("not_found_tracks", []),
            "failed": download_result.get("failed", 0),
            "failed_tracks": download_result.get("failed_tracks", []),
        }

    log(f"\nDone.")
    print(json.dumps(output, indent=2))

    has_failures = (
        discovery["not_resolved"] > 0 or
        (download_result and (download_result.get("not_found", 0) > 0 or download_result.get("failed", 0) > 0))
    )
    sys.exit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
