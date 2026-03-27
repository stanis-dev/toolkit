#!/usr/bin/env python3
"""
Download tracks via SoulSync's built-in pipeline.

Runs on the homelab. Zero external dependencies (stdlib only).
Adds tracks to the SoulSync wishlist, triggers the download pipeline
(which handles Soulseek search, quality selection, 3 concurrent downloads,
metadata tagging, and Artist/Album/Track organization), then polls
until complete.

Usage:
    python3 sync_playlist.py --tracks '[{"artist":"Erykah Badu","track":"Otherside of the Game","album":"Baduizm"}]' \
        --api-key 'sk_...'

    python3 sync_playlist.py --tracks-file /tmp/tracks.json --api-key 'sk_...' --timeout 1800
"""

import argparse
import hashlib
import json
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

SOULSYNC_URL = "http://localhost:8008"
SOULSYNC_API = f"{SOULSYNC_URL}/api/v1"
POLL_INTERVAL = 15
DEFAULT_TIMEOUT = 1200

_session_cookie = None


def api_request(path, method="GET", data=None, api_key=None, base=None, use_session=False):
    """Make an authenticated request to the SoulSync API."""
    url = f"{base or SOULSYNC_API}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    if api_key and not use_session:
        req.add_header("Authorization", f"Bearer {api_key}")
    if use_session and _session_cookie:
        req.add_header("Cookie", f"session={_session_cookie}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        try:
            return json.loads(body)
        except (json.JSONDecodeError, ValueError):
            return {"error": {"code": str(e.code), "message": body}}
    except Exception as e:
        return {"error": {"code": "REQUEST_FAILED", "message": str(e)}}


def get_session():
    """Get a Flask session cookie by selecting profile 1."""
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


def make_track_id(artist, track):
    """Generate a deterministic synthetic ID from artist + track name."""
    key = f"{artist}|{track}".lower().strip()
    return hashlib.md5(key.encode()).hexdigest()


def format_for_wishlist(track):
    """Convert {artist, track, album} to the spotify_track_data format SoulSync expects."""
    artist = track.get("artist", "").strip()
    title = track.get("track", "").strip()
    album = track.get("album", "").strip()
    synthetic_id = make_track_id(artist, title)

    return {
        "id": synthetic_id,
        "name": title,
        "artists": [artist],
        "album": {"name": album, "album_type": "single", "total_tracks": 1} if album else {},
        "duration_ms": 0,
        "popularity": 0,
        "preview_url": None,
        "external_urls": {},
    }


def add_tracks_to_wishlist(tracks, api_key):
    """Add tracks to the SoulSync wishlist. Returns (added, skipped, errors)."""
    added, skipped, errors = [], [], []
    for i, track in enumerate(tracks, 1):
        spotify_data = format_for_wishlist(track)
        label = f"{track.get('artist', '?')} - {track.get('track', '?')}"
        log(f"  [{i}/{len(tracks)}] {label}")

        resp = api_request("/wishlist", method="POST", data={
            "spotify_track_data": spotify_data,
            "failure_reason": "Added via agent sync_playlist",
            "source_type": "manual",
        }, api_key=api_key)

        if resp.get("success"):
            added.append(label)
            log(f"    Added")
        elif resp.get("error", {}).get("code") == "CONFLICT":
            skipped.append(label)
            log(f"    Already in wishlist")
        else:
            err = resp.get("error", {}).get("message", str(resp))
            errors.append({"track": label, "error": err})
            log(f"    Error: {err}")

    return added, skipped, errors


def trigger_wishlist_download(api_key):
    """Trigger SoulSync's wishlist download processing via the internal endpoint."""
    resp = api_request("/api/wishlist/download_missing", method="POST",
                       data={"force_download_all": False},
                       base=SOULSYNC_URL, use_session=True)
    if resp.get("success"):
        log(f"  batch_id: {resp.get('batch_id', 'unknown')}")
        return resp.get("batch_id")
    err = resp.get("error", str(resp))
    log(f"  Failed to trigger download: {err}")
    return None


def poll_downloads(batch_id, timeout):
    """Poll download batch status until complete or timeout."""
    start = time.time()
    last_summary = ""
    settled_count = 0

    while time.time() - start < timeout:
        resp = api_request(
            f"/api/download_status/batch?batch_ids={batch_id}",
            base=SOULSYNC_URL, use_session=True,
        )
        batches = resp.get("batches", {})
        batch = batches.get(batch_id, {})

        if not batch:
            settled_count += 1
            if settled_count >= 3:
                log("  Batch cleared (completed)")
                return {"status": "completed"}
            time.sleep(POLL_INTERVAL)
            continue

        settled_count = 0
        phase = batch.get("phase", "unknown")
        tasks = batch.get("tasks", [])

        active = sum(1 for t in tasks if t.get("status") in
                     ("searching", "downloading", "queued", "pending", "initializing"))
        done = sum(1 for t in tasks if t.get("status") in
                   ("completed", "succeeded", "not_found"))
        failed = sum(1 for t in tasks if t.get("status") in
                     ("failed", "errored", "cancelled", "permanently_failed"))

        summary = f"phase={phase} active={active} done={done} failed={failed}"
        if summary != last_summary:
            elapsed = time.time() - start
            log(f"  [{elapsed:.0f}s] {summary}")
            for t in tasks:
                status = t.get("status", "")
                info = t.get("track_info") or {}
                name = info.get("name") or info.get("track_name", "?")
                artists = info.get("artists") or info.get("artist", [])
                artist_str = artists[0] if isinstance(artists, list) and artists else str(artists)
                if status in ("searching", "downloading", "queued"):
                    log(f"    {artist_str} - {name} | {status}")
            last_summary = summary

        if phase == "complete":
            return {
                "status": "completed" if failed == 0 else "completed_with_errors",
                "completed": done,
                "failed": failed,
            }

        if phase == "error":
            return {"status": "error", "error": batch.get("error", "Unknown error")}

        time.sleep(POLL_INTERVAL)

    return {"status": "timeout", "elapsed": time.time() - start}


def get_wishlist_tracks(api_key):
    """Get current wishlist track IDs."""
    resp = api_request("/wishlist", api_key=api_key) or {}
    data = resp.get("data") or {}
    return data.get("tracks", [])


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser(description="Download tracks via SoulSync pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tracks", help="JSON array of {artist, track, album} objects")
    group.add_argument("--tracks-file", help="Path to JSON file with track array")
    parser.add_argument("--api-key", required=True, help="SoulSync API key")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"Max seconds to wait for downloads (default {DEFAULT_TIMEOUT})")
    args = parser.parse_args()

    if args.tracks_file:
        with open(args.tracks_file) as f:
            tracks = json.load(f)
    else:
        tracks = json.loads(args.tracks)

    log(f"SoulSync Pipeline: {len(tracks)} tracks\n")

    # Step 1: Get session for internal endpoints
    log("Authenticating...")
    if not get_session():
        log("Failed to get session from SoulSync.")
        print(json.dumps({"status": "auth_failed"}, indent=2))
        sys.exit(1)
    log("  Session acquired\n")

    # Step 2: Check current wishlist state
    log("Checking current wishlist...")
    existing = get_wishlist_tracks(args.api_key)
    if existing:
        log(f"  {len(existing)} tracks already in wishlist (will be included in download)\n")

    # Step 3: Add tracks to wishlist
    log("Adding tracks to wishlist...")
    added, skipped, add_errors = add_tracks_to_wishlist(tracks, args.api_key)
    log(f"\n  Added: {len(added)}, Already in wishlist: {len(skipped)}, Errors: {len(add_errors)}\n")

    if not added and not skipped and not existing:
        log("No tracks to download.")
        print(json.dumps({"status": "no_tracks", "errors": add_errors}, indent=2))
        sys.exit(1)

    # Step 4: Trigger download via internal endpoint (session-based)
    log("Triggering SoulSync download pipeline...")
    batch_id = trigger_wishlist_download(args.api_key)
    if not batch_id:
        log("Failed to trigger downloads.")
        print(json.dumps({"status": "trigger_failed", "added": len(added)}, indent=2))
        sys.exit(1)
    log("  Download pipeline started (SoulSync handles search, download, organize)\n")

    # Step 5: Poll progress
    log("Polling download progress...")
    poll_result = poll_downloads(batch_id, args.timeout)
    log(f"\nResult: {poll_result['status']}\n")

    output = {
        "status": poll_result["status"],
        "tracks_requested": len(tracks),
        "tracks_added_to_wishlist": len(added),
        "tracks_already_in_wishlist": len(skipped),
        "add_errors": add_errors,
        "download_result": {
            "completed": poll_result.get("completed", 0),
            "failed": poll_result.get("failed", 0),
        },
    }
    print(json.dumps(output, indent=2))

    if poll_result["status"] == "timeout":
        sys.exit(2)


if __name__ == "__main__":
    main()
