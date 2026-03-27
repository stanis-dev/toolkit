#!/usr/bin/env python3
"""
Sync Plex music ratings and play history into the PostgreSQL taste table.

Runs on the homelab. Zero external dependencies (stdlib only).
Talks to Plex API over the network, enriches with SoulSync MusicBrainz IDs,
and upserts into the local PostgreSQL music database via docker exec psql.

Usage:
    python3 sync_taste.py --plex-token TOKEN
    python3 sync_taste.py --plex-token TOKEN --dry-run
"""

import argparse
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

PLEX_MUSIC_SECTION = 3
PLEX_PATH_PREFIX = "/System/Volumes/Data/Volumes/Media/media/music/"
PSQL_CMD = ["sudo", "docker", "exec", "-i", "postgres", "psql", "-U", "postgres", "-d", "music"]
SOULSYNC_CMD = ["sudo", "docker", "exec", "soulsync", "python3", "-c"]


def plex_get(base_url, token, path):
    url = f"{base_url}{path}{'&' if '?' in path else '?'}X-Plex-Token={token}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def fetch_rated_tracks(base_url, token):
    """Fetch all music tracks that have a user rating."""
    tracks = {}
    page_size = 100
    offset = 0

    while True:
        data = plex_get(
            base_url, token,
            f"/library/sections/{PLEX_MUSIC_SECTION}/all"
            f"?type=10&sort=userRating:desc"
            f"&X-Plex-Container-Start={offset}&X-Plex-Container-Size={page_size}"
        )
        container = data.get("MediaContainer", {})
        items = container.get("Metadata", [])
        if not items:
            break

        for item in items:
            rating = item.get("userRating")
            if not rating:
                continue

            parts = item.get("Media", [{}])[0].get("Part", [])
            file_path = parts[0].get("file", "") if parts else ""

            key = (
                item.get("grandparentTitle", "").strip(),
                item.get("parentTitle", "").strip(),
                item.get("title", "").strip(),
            )
            if not key[0] or not key[2]:
                continue

            tracks[key] = {
                "artist": key[0],
                "album": key[1],
                "track": key[2],
                "user_rating": float(rating),
                "play_count": int(item.get("viewCount", 0)),
                "last_played_at": item.get("lastViewedAt"),
                "plex_guid": item.get("guid", ""),
                "file_path": file_path,
            }

        total = int(container.get("totalSize", 0))
        offset += page_size
        if offset >= total:
            break

    return tracks


def fetch_play_history(base_url, token):
    """Fetch play history to supplement play counts for unrated tracks."""
    history = {}
    data = plex_get(
        base_url, token,
        f"/status/sessions/history/all?librarySectionID={PLEX_MUSIC_SECTION}"
    )
    for item in data.get("MediaContainer", {}).get("Metadata", []):
        key = (
            item.get("grandparentTitle", "").strip(),
            item.get("parentTitle", "").strip(),
            item.get("title", "").strip(),
        )
        if not key[0] or not key[2]:
            continue

        if key not in history:
            history[key] = {
                "artist": key[0],
                "album": key[1],
                "track": key[2],
                "play_count": 0,
                "last_played_at": item.get("viewedAt"),
                "plex_guid": item.get("guid", ""),
            }
        history[key]["play_count"] += 1

    return history


def enrich_musicbrainz_ids(tracks):
    """Look up MusicBrainz recording IDs from SoulSync SQLite DB."""
    script = """
import sqlite3, json
c = sqlite3.connect("/app/data/music_library.db").cursor()
c.execute(
    "SELECT t.file_path, t.musicbrainz_recording_id "
    "FROM tracks t WHERE t.musicbrainz_recording_id IS NOT NULL"
)
out = {}
for path, mbid in c.fetchall():
    out[path] = mbid
print(json.dumps(out))
"""
    try:
        result = subprocess.run(
            SOULSYNC_CMD + [script],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            print(f"  Warning: SoulSync query failed: {result.stderr.strip()}", file=sys.stderr)
            return

        mb_map = json.loads(result.stdout.strip())
    except Exception as e:
        print(f"  Warning: MusicBrainz enrichment skipped: {e}", file=sys.stderr)
        return

    matched = 0
    for track_data in tracks.values():
        plex_path = track_data.get("file_path", "")
        if plex_path and plex_path in mb_map:
            track_data["musicbrainz_recording_id"] = mb_map[plex_path]
            matched += 1

    print(f"  MusicBrainz enrichment: {matched}/{len(tracks)} tracks matched")


def normalize_file_path(plex_path):
    """Strip Plex NFS prefix to get relative path matching audio_features."""
    if plex_path and plex_path.startswith(PLEX_PATH_PREFIX):
        return plex_path[len(PLEX_PATH_PREFIX):]
    return plex_path or None


def escape_sql(value):
    """Escape a string for SQL single-quote literals."""
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def generate_sql(tracks):
    """Generate the upsert SQL for all tracks."""
    lines = [
        "CREATE TABLE IF NOT EXISTS taste ("
        "  id SERIAL PRIMARY KEY,"
        "  artist TEXT NOT NULL,"
        "  album TEXT NOT NULL DEFAULT '',"
        "  track TEXT NOT NULL,"
        "  file_path TEXT,"
        "  plex_guid TEXT,"
        "  musicbrainz_recording_id TEXT,"
        "  user_rating REAL,"
        "  play_count INTEGER DEFAULT 0,"
        "  last_played_at TIMESTAMPTZ,"
        "  context_tags TEXT[] DEFAULT '{}',"
        "  anti_tags TEXT[] DEFAULT '{}',"
        "  disliked BOOLEAN DEFAULT FALSE,"
        "  notes TEXT,"
        "  first_seen_at TIMESTAMPTZ DEFAULT NOW(),"
        "  updated_at TIMESTAMPTZ DEFAULT NOW(),"
        "  synced_at TIMESTAMPTZ,"
        "  UNIQUE(artist, track, album)"
        ");",
        "",
        "BEGIN;",
    ]

    now = datetime.now(timezone.utc).isoformat()

    for t in tracks.values():
        rel_path = normalize_file_path(t.get("file_path", ""))
        last_played = None
        if t.get("last_played_at"):
            ts = int(t["last_played_at"])
            last_played = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()

        lines.append(
            f"INSERT INTO taste (artist, album, track, file_path, plex_guid, "
            f"musicbrainz_recording_id, user_rating, play_count, last_played_at, synced_at) "
            f"VALUES ({escape_sql(t['artist'])}, {escape_sql(t['album'])}, "
            f"{escape_sql(t['track'])}, {escape_sql(rel_path)}, "
            f"{escape_sql(t.get('plex_guid'))}, "
            f"{escape_sql(t.get('musicbrainz_recording_id'))}, "
            f"{t.get('user_rating', 'NULL')}, {t.get('play_count', 0)}, "
            f"{'TIMESTAMPTZ ' + escape_sql(last_played) if last_played else 'NULL'}, "
            f"TIMESTAMPTZ {escape_sql(now)}) "
            f"ON CONFLICT (artist, track, album) DO UPDATE SET "
            f"file_path = COALESCE(EXCLUDED.file_path, taste.file_path), "
            f"plex_guid = COALESCE(EXCLUDED.plex_guid, taste.plex_guid), "
            f"musicbrainz_recording_id = COALESCE(EXCLUDED.musicbrainz_recording_id, taste.musicbrainz_recording_id), "
            f"user_rating = COALESCE(EXCLUDED.user_rating, taste.user_rating), "
            f"play_count = GREATEST(EXCLUDED.play_count, taste.play_count), "
            f"last_played_at = GREATEST(EXCLUDED.last_played_at, taste.last_played_at), "
            f"updated_at = NOW(), "
            f"synced_at = EXCLUDED.synced_at;"
        )

    lines.append("COMMIT;")
    return "\n".join(lines)


def execute_sql(sql, dry_run=False):
    if dry_run:
        print(sql)
        return True

    result = subprocess.run(
        PSQL_CMD,
        input=sql, capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"SQL error: {result.stderr}", file=sys.stderr)
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Sync Plex taste data to PostgreSQL")
    parser.add_argument("--plex-url", default="http://192.168.0.155:32400")
    parser.add_argument("--plex-token", required=True)
    parser.add_argument("--dry-run", action="store_true", help="Print SQL without executing")
    args = parser.parse_args()

    print("Fetching rated tracks from Plex...")
    tracks = fetch_rated_tracks(args.plex_url, args.plex_token)
    print(f"  Found {len(tracks)} rated tracks")

    print("Fetching play history from Plex...")
    history = fetch_play_history(args.plex_url, args.plex_token)
    print(f"  Found {len(history)} tracks with play history")

    for key, hist in history.items():
        if key in tracks:
            if hist["play_count"] > tracks[key]["play_count"]:
                tracks[key]["play_count"] = hist["play_count"]
            if hist.get("last_played_at") and (
                not tracks[key].get("last_played_at")
                or int(hist["last_played_at"]) > int(tracks[key]["last_played_at"])
            ):
                tracks[key]["last_played_at"] = hist["last_played_at"]
        else:
            tracks[key] = {
                "artist": hist["artist"],
                "album": hist["album"],
                "track": hist["track"],
                "play_count": hist["play_count"],
                "last_played_at": hist.get("last_played_at"),
                "plex_guid": hist.get("plex_guid", ""),
                "file_path": "",
            }

    print(f"  Merged total: {len(tracks)} tracks")

    print("Enriching with MusicBrainz IDs from SoulSync...")
    enrich_musicbrainz_ids(tracks)

    print("Generating SQL...")
    sql = generate_sql(tracks)

    if args.dry_run:
        print("\n--- DRY RUN SQL ---")
        print(sql)
        print("--- END ---")
    else:
        print("Executing upsert...")
        if execute_sql(sql):
            rated = sum(1 for t in tracks.values() if t.get("user_rating"))
            unrated = len(tracks) - rated
            print(f"\nDone! Synced {len(tracks)} tracks ({rated} rated, {unrated} play-history only)")
        else:
            print("Sync failed!", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
