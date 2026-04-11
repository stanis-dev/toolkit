#!/usr/bin/env python3
"""Backfill thread replies and download image attachments for existing Slack exports.

Reads already-exported channel JSON files, fetches missing thread replies via
the Slack API, downloads image attachments, and regenerates readable markdown.
Does NOT re-run the main export (no channel discovery or message history fetch).
"""

import json
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from slack_export import (
    extract_credentials,
    SlackSession,
    SLACK_DATA_DIR,
    RATE_LIMIT_TIER3,
    HISTORY_PAGE_LIMIT,
)


def _fetch_thread(session, channel_id, thread_ts):
    all_replies = []
    cursor = None
    while True:
        params = {
            "channel": channel_id,
            "ts": thread_ts,
            "limit": str(HISTORY_PAGE_LIMIT),
            "inclusive": "true",
        }
        if cursor:
            params["cursor"] = cursor
        result = session.api_call(
            "conversations.replies", params, reason="message-pane/requestReplies"
        )
        if not result or not result.get("ok"):
            break
        msgs = result.get("messages", [])
        all_replies.extend(m for m in msgs if m.get("ts") != thread_ts)
        if not result.get("has_more"):
            break
        cursor = result.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break
    return all_replies


def _download_file(session, url, dest_path):
    """Download a file from Slack's CDN using the session auth."""
    headers = {"Cookie": session._cookie_string()}
    resp = session.session.get(url, headers=headers, timeout=60, stream=True)
    if resp.status_code != 200:
        return False
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=65536):
            f.write(chunk)
    return True


def backfill_workspace(workspace_dir, session):
    channels_dir = os.path.join(workspace_dir, "channels")
    files_dir = os.path.join(workspace_dir, "files")
    if not os.path.isdir(channels_dir):
        print(f"  No channels directory", file=sys.stderr)
        return

    channel_files = sorted(f for f in os.listdir(channels_dir) if f.endswith(".json"))
    total_threads_fetched = 0
    total_images_downloaded = 0

    for ci, fname in enumerate(channel_files, 1):
        path = os.path.join(channels_dir, fname)
        with open(path) as f:
            data = json.load(f)

        channel = data.get("channel", {})
        messages = data.get("messages", [])
        cid = channel.get("id", fname.replace(".json", ""))
        ch_name = channel.get("resolved_name") or channel.get("name", cid)

        # Find threads needing backfill
        needs_replies = [
            m for m in messages
            if m.get("reply_count", 0) > 0 and not m.get("replies_full")
        ]

        # Find images needing download
        needs_download = []
        for m in messages:
            for fl in m.get("files", []):
                mime = fl.get("mimetype", "")
                if not mime.startswith("image/"):
                    continue
                fid = fl.get("id", "")
                ext = fl.get("filetype", "png")
                local_name = f"{fid}.{ext}"
                local_path = os.path.join(files_dir, local_name)
                if not os.path.exists(local_path):
                    url = fl.get("url_private_download") or fl.get("url_private", "")
                    if url:
                        needs_download.append((url, local_path, local_name, fl))

        if not needs_replies and not needs_download:
            continue

        label = f"DM:{ch_name}" if channel.get("is_im") else f"#{ch_name}"
        print(f"\n  [{ci}/{len(channel_files)}] {label}: {len(needs_replies)} threads, {len(needs_download)} images", file=sys.stderr)

        # Fetch threads
        modified = False
        for i, msg in enumerate(needs_replies):
            replies = _fetch_thread(session, cid, msg["ts"])
            if replies:
                msg["replies_full"] = replies
                modified = True
                total_threads_fetched += 1
            if (i + 1) % 10 == 0:
                print(f"    ... {i+1}/{len(needs_replies)} threads", file=sys.stderr)

        if needs_replies:
            print(f"    Fetched {total_threads_fetched} threads", file=sys.stderr)

        # Download images
        if needs_download:
            os.makedirs(files_dir, exist_ok=True)
            for url, local_path, local_name, fl in needs_download:
                ok = _download_file(session, url, local_path)
                if ok:
                    fl["local_path"] = os.path.relpath(local_path, workspace_dir)
                    modified = True
                    total_images_downloaded += 1
                else:
                    print(f"    Failed to download {local_name}", file=sys.stderr)
                time.sleep(0.2)
            print(f"    Downloaded {total_images_downloaded} images", file=sys.stderr)

        if modified:
            with open(path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    return total_threads_fetched, total_images_downloaded


def main():
    print("Extracting Slack credentials...", file=sys.stderr)
    teams, d_cookie, aux_cookies = extract_credentials()
    if not d_cookie:
        print("Error: Could not extract d cookie", file=sys.stderr)
        sys.exit(1)

    filter_dirs = set(sys.argv[1:]) if len(sys.argv) > 1 else None

    for name in sorted(os.listdir(SLACK_DATA_DIR)):
        ws_dir = os.path.join(SLACK_DATA_DIR, name)
        if not os.path.isdir(ws_dir) or not os.path.exists(os.path.join(ws_dir, "channels")):
            continue
        if filter_dirs and name not in filter_dirs:
            continue

        # Find the matching team config
        team = None
        for t in teams.values():
            d = f"{t['domain']}-enterprise" if t["is_enterprise"] else t["domain"]
            if d == name:
                team = t
                break
        if not team:
            # Try non-enterprise match
            for t in teams.values():
                if t["domain"] == name and not t["is_enterprise"]:
                    team = t
                    break
        if not team:
            print(f"Skipping {name}: no matching team config", file=sys.stderr)
            continue

        session = SlackSession(team, d_cookie, aux_cookies)
        auth = session.api_call("auth.test", reason="auth/verify")
        if not auth or not auth.get("ok"):
            print(f"Skipping {name}: auth failed", file=sys.stderr)
            continue

        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Backfilling: {name} (as {auth.get('user')})", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)

        threads, images = backfill_workspace(ws_dir, session)
        print(f"\n  Totals: {threads} threads fetched, {images} images downloaded", file=sys.stderr)

    # Regenerate readable files
    print("\nRegenerating readable files...", file=sys.stderr)
    from process_exports import process_all
    process_all()

    print("\nBackfill complete.", file=sys.stderr)


if __name__ == "__main__":
    main()
