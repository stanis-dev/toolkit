#!/usr/bin/env python3
"""Export Slack channels, conversations and DMs to local JSON files.

Extracts credentials from the local Slack desktop app, matches its web client
request signature, and downloads message history for all channels the user
participates in.
"""

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import uuid
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
SLACK_DATA_DIR = os.path.join(DATA_DIR, "slack")
SLACK_APP_SUPPORT = os.path.expanduser("~/Library/Application Support/Slack")
LOCAL_STORAGE_DIR = os.path.join(SLACK_APP_SUPPORT, "Local Storage", "leveldb")
COOKIES_DB = os.path.join(SLACK_APP_SUPPORT, "Cookies")

# ---------------------------------------------------------------------------
# Request signature constants (matches Slack web client)
# ---------------------------------------------------------------------------
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/146.0.0.0 Safari/537.36"
)
COMMON_HEADERS = {
    "user-agent": USER_AGENT,
    "origin": "https://app.slack.com",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}

RATE_LIMIT_TIER2 = 2.0   # seconds between search requests
RATE_LIMIT_TIER3 = 0.8   # seconds between history requests
HISTORY_PAGE_LIMIT = 200
SEARCH_PAGE_LIMIT = 100

# Dec 1, 2025 00:00:00 UTC — don't fetch anything older
OLDEST_TS = "1733011200.000000"
FETCH_THREADS = False


# ===================================================================
# Credential extraction
# ===================================================================

def extract_credentials():
    """Extract xoxc tokens, d cookie, and auxiliary cookies from Slack desktop app."""
    teams = _read_local_config()
    d_cookie, aux_cookies = _read_cookies()
    return teams, d_cookie, aux_cookies


def _read_local_config():
    """Copy Slack's Local Storage LevelDB and read localConfig_v2 via Node."""
    tmp = tempfile.mkdtemp(prefix="slack-ls-")
    try:
        for f in os.listdir(LOCAL_STORAGE_DIR):
            src = os.path.join(LOCAL_STORAGE_DIR, f)
            dst = os.path.join(tmp, f)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
        lock = os.path.join(tmp, "LOCK")
        if os.path.exists(lock):
            os.remove(lock)

        node_script = r"""
const { ClassicLevel } = require('classic-level');
(async () => {
  const db = new ClassicLevel(process.argv[1], {
    createIfMissing: false, keyEncoding: 'buffer', valueEncoding: 'buffer'
  });
  await db.open();
  for await (const [key, value] of db.iterator()) {
    if (key.toString('utf-8').includes('localConfig_v2')) {
      let v = value.toString('utf-8');
      const i = v.indexOf('{');
      if (i > 0) v = v.substring(i);
      process.stdout.write(v);
      break;
    }
  }
  await db.close();
})();
"""
        result = subprocess.run(
            ["node", "-e", node_script, tmp],
            capture_output=True, text=True, timeout=15,
            cwd=PROJECT_DIR,
        )
        if result.returncode != 0:
            print(f"Error reading LevelDB: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        config = json.loads(result.stdout)
        teams = {}
        for tid, team in config.get("teams", {}).items():
            if not team.get("token"):
                continue
            teams[tid] = {
                "id": tid,
                "name": team["name"],
                "domain": team["domain"],
                "url": team["url"],
                "token": team["token"],
                "user_id": team["user_id"],
                "is_enterprise": "enterprise" in team.get("url", ""),
                "enterprise_id": team.get("enterprise_id"),
            }
        return teams
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _read_cookies():
    """Decrypt the d cookie and read auxiliary cookies from Slack's Cookies SQLite."""
    tmp_db = os.path.join(tempfile.gettempdir(), "slack_cookies_copy.sqlite")
    shutil.copy2(COOKIES_DB, tmp_db)

    try:
        keychain_pw = subprocess.run(
            ["security", "find-generic-password", "-s", "Slack Safe Storage", "-w"],
            capture_output=True, text=True, timeout=60,
        ).stdout.strip()

        derived_key = pbkdf2_hmac("sha1", keychain_pw.encode(), b"saltysalt", 1003, dklen=16)
        iv = b"\x20" * 16

        conn = sqlite3.connect(tmp_db)
        cur = conn.cursor()

        def _decrypt_cookie(enc_value):
            """Decrypt a Chromium v10-encrypted cookie, stripping the 32-byte hash prefix."""
            if not enc_value or len(enc_value) < 4 or enc_value[:3] != b"v10":
                return None
            ct = enc_value[3:]
            cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            padded = decryptor.update(ct) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            raw = unpadder.update(padded) + unpadder.finalize()
            # Chromium prepends a 32-byte hash before the actual value
            return raw[32:].decode("utf-8", errors="replace") if len(raw) > 32 else raw.decode("utf-8", errors="replace")

        # Decrypt the d cookie
        cur.execute(
            "SELECT encrypted_value FROM cookies WHERE name='d' AND host_key='.slack.com'"
        )
        row = cur.fetchone()
        d_cookie = ""
        if row:
            val = _decrypt_cookie(row[0])
            if val and "xoxd-" in val:
                d_cookie = val[val.index("xoxd-"):]

        # Read auxiliary cookies (may be unencrypted or encrypted)
        aux_cookies = {}
        for name in ("b", "ssb_instance_id", "d-s", "lc", "tz", "utm", "x"):
            cur.execute(
                "SELECT value, encrypted_value FROM cookies WHERE name=? AND host_key='.slack.com'",
                (name,),
            )
            row = cur.fetchone()
            if not row:
                continue
            plain, enc = row
            if plain:
                aux_cookies[name] = plain
                continue
            try:
                val = _decrypt_cookie(enc)
                if val:
                    aux_cookies[name] = val
            except Exception:
                pass

        conn.close()
        return d_cookie, aux_cookies
    finally:
        os.unlink(tmp_db)


# ===================================================================
# HTTP session matching Slack web client
# ===================================================================

class SlackSession:
    """HTTP session that mimics the Slack web client request signature."""

    def __init__(self, team, d_cookie, aux_cookies):
        self.team = team
        self.token = team["token"]
        self.d_cookie = d_cookie
        self.aux_cookies = aux_cookies
        self.session = requests.Session()
        self.session.headers.update(COMMON_HEADERS)
        self._version_ts = str(int(time.time()))
        self._csid = hashlib.md5(uuid.uuid4().bytes).hexdigest()[:16]

        if team["is_enterprise"]:
            self.base_url = f"https://{team['domain']}.enterprise.slack.com/api"
        else:
            self.base_url = f"https://{team['domain']}.slack.com/api"

    def _cookie_string(self):
        # d cookie is already URL-encoded from the Chromium cookie store
        parts = [f"d={self.d_cookie}"]
        for k, v in self.aux_cookies.items():
            parts.append(f"{k}={v}")
        return "; ".join(parts)

    def _query_params(self):
        x_id = f"{uuid.uuid4().hex[:8]}-{time.time():.3f}"
        route = self.team["id"]
        params = {
            "_x_id": x_id,
            "slack_route": f"{route}",
            "_x_version_ts": self._version_ts,
            "_x_frontend_build_type": "current",
            "_x_desktop_ia": "4",
            "_x_gantry": "true",
            "fp": "58",
            "_x_num_retries": "0",
        }
        return params

    def _tracking_fields(self, reason="export/fetch"):
        return {
            "_x_reason": reason,
            "_x_mode": "online",
            "_x_sonic": "true",
            "_x_app_name": "client",
        }

    def api_call(self, method, params=None, reason="export/fetch", tier_delay=RATE_LIMIT_TIER3):
        """POST to a Slack API method using multipart form data."""
        url = f"{self.base_url}/{method}"
        query = self._query_params()

        form = {"token": self.token}
        if params:
            form.update(params)
        form.update(self._tracking_fields(reason))

        headers = {"Cookie": self._cookie_string()}

        for attempt in range(5):
            resp = self.session.post(url, params=query, data=form, headers=headers, timeout=30)

            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 10))
                print(f"  Rate limited, waiting {retry_after}s...", file=sys.stderr)
                time.sleep(retry_after)
                continue

            resp.raise_for_status()
            data = resp.json()

            if not data.get("ok") and data.get("error") == "ratelimited":
                time.sleep(5)
                continue

            time.sleep(tier_delay)
            return data

        return data


# ===================================================================
# Channel discovery
# ===================================================================

def discover_channels(session):
    """Find all channels/DMs the user participates in."""
    if not session.team["is_enterprise"]:
        return _discover_via_conversations_list(session)

    # Enterprise: try users.conversations first, fall back to search
    result = session.api_call(
        "users.conversations",
        {"types": "public_channel,private_channel,mpim,im", "limit": "200"},
        reason="channels/list",
    )
    if result.get("ok"):
        return _collect_conversations(session, result)

    print(f"  users.conversations blocked ({result.get('error')}), falling back to search", file=sys.stderr)
    return _discover_via_search(session)


def _discover_via_conversations_list(session):
    """List channels via users.conversations (works on non-enterprise)."""
    result = session.api_call(
        "users.conversations",
        {"types": "public_channel,private_channel,mpim,im", "limit": "200"},
        reason="channels/list",
    )
    if not result.get("ok"):
        print(f"  users.conversations failed: {result.get('error')}", file=sys.stderr)
        return {}
    return _collect_conversations(session, result)


def _collect_conversations(session, initial_result):
    """Paginate through users.conversations results."""
    channels = {}
    for ch in initial_result.get("channels", []):
        channels[ch["id"]] = _channel_meta(ch)

    cursor = initial_result.get("response_metadata", {}).get("next_cursor", "")
    while cursor:
        result = session.api_call(
            "users.conversations",
            {"types": "public_channel,private_channel,mpim,im", "limit": "200", "cursor": cursor},
            reason="channels/list",
        )
        if not result.get("ok"):
            break
        for ch in result.get("channels", []):
            channels[ch["id"]] = _channel_meta(ch)
        cursor = result.get("response_metadata", {}).get("next_cursor", "")

    print(f"  Found {len(channels)} channels via conversations list", file=sys.stderr)
    return channels


def _discover_via_search(session):
    """Discover channels by searching for messages from the current user."""
    user_id = session.team["user_id"]
    channels = {}
    page = 1

    while True:
        result = session.api_call(
            "search.messages",
            {"query": f"from:<@{user_id}> after:2025-12-01", "count": str(SEARCH_PAGE_LIMIT), "page": str(page), "sort": "timestamp", "sort_dir": "desc"},
            reason="channels/search",
            tier_delay=RATE_LIMIT_TIER2,
        )
        if not result.get("ok"):
            print(f"  search.messages failed: {result.get('error')}", file=sys.stderr)
            break

        matches = result.get("messages", {}).get("matches", [])
        if not matches:
            break

        for m in matches:
            ch = m.get("channel", {})
            cid = ch.get("id")
            if cid and cid not in channels:
                channels[cid] = {
                    "id": cid,
                    "name": ch.get("name", cid),
                    "is_im": ch.get("is_im", False),
                    "is_mpim": ch.get("is_mpim", False),
                    "is_private": ch.get("is_private", False),
                }

        paging = result.get("messages", {}).get("paging", {})
        if page >= paging.get("pages", 1):
            break
        page += 1

    # Enrich with conversations.info for any channels missing metadata
    for cid, meta in list(channels.items()):
        if meta.get("name") == cid:
            info = session.api_call(
                "conversations.info", {"channel": cid}, reason="channels/info"
            )
            if info.get("ok"):
                channels[cid] = _channel_meta(info["channel"])

    print(f"  Found {len(channels)} channels via search", file=sys.stderr)
    return channels


def _channel_meta(ch):
    return {
        "id": ch["id"],
        "name": ch.get("name", ch.get("user", ch["id"])),
        "is_im": ch.get("is_im", False),
        "is_mpim": ch.get("is_mpim", False),
        "is_private": ch.get("is_private", False),
        "is_channel": ch.get("is_channel", False),
        "is_group": ch.get("is_group", False),
        "purpose": ch.get("purpose", {}).get("value", ""),
        "topic": ch.get("topic", {}).get("value", ""),
        "num_members": ch.get("num_members"),
    }


# ===================================================================
# Message export with incremental sync
# ===================================================================

def export_channel_messages(session, channel_id, oldest="0"):
    """Fetch message history for a channel (no older than OLDEST_TS), with thread replies."""
    # Never go further back than the global floor
    oldest = str(max(float(oldest), float(OLDEST_TS)))

    all_messages = []
    cursor = None
    page = 0

    while True:
        params = {
            "channel": channel_id,
            "limit": str(HISTORY_PAGE_LIMIT),
            "inclusive": "true",
            "oldest": oldest,
        }
        if cursor:
            params["cursor"] = cursor

        result = session.api_call(
            "conversations.history", params, reason="message-pane/requestHistory"
        )

        if not result.get("ok"):
            err = result.get("error", "unknown")
            if err in ("channel_not_found", "not_in_channel", "missing_scope"):
                print(f"    Skipping {channel_id}: {err}", file=sys.stderr)
                return None
            print(f"    Error fetching {channel_id}: {err}", file=sys.stderr)
            break

        messages = result.get("messages", [])
        all_messages.extend(messages)
        page += 1

        if page % 5 == 0:
            print(f"    ... {len(all_messages)} messages so far (page {page})", file=sys.stderr)

        if not result.get("has_more"):
            break
        cursor = result.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break

    # Optionally fetch thread replies (slow — ~1s per thread due to rate limits)
    thread_parents = [m for m in all_messages if m.get("reply_count", 0) > 0]
    if FETCH_THREADS and thread_parents:
        for i, msg in enumerate(thread_parents):
            replies = _fetch_thread(session, channel_id, msg["ts"])
            if replies:
                msg["replies_full"] = replies
            if (i + 1) % 10 == 0:
                print(f"    ... fetched {i+1}/{len(thread_parents)} threads", file=sys.stderr)

    threads_note = f", {len(thread_parents)} threads fetched" if FETCH_THREADS else f", {len(thread_parents)} threads (skipped, use --threads)"
    print(f"    {len(all_messages)} messages{threads_note} ({page} pages)", file=sys.stderr)
    return all_messages


def _fetch_thread(session, channel_id, thread_ts):
    """Fetch all replies in a thread."""
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

        if not result.get("ok"):
            break

        msgs = result.get("messages", [])
        # First message is the parent, skip it
        all_replies.extend(m for m in msgs if m.get("ts") != thread_ts)

        if not result.get("has_more"):
            break
        cursor = result.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break

    return all_replies


# ===================================================================
# User resolution
# ===================================================================

def fetch_users(session):
    """Fetch user list for name resolution."""
    users = {}
    cursor = None

    while True:
        params = {"limit": "200"}
        if cursor:
            params["cursor"] = cursor

        result = session.api_call("users.list", params, reason="users/list")
        if not result.get("ok"):
            print(f"  users.list failed: {result.get('error')}", file=sys.stderr)
            break

        for u in result.get("members", []):
            users[u["id"]] = {
                "name": u.get("name", ""),
                "real_name": u.get("real_name", u.get("profile", {}).get("real_name", "")),
                "display_name": u.get("profile", {}).get("display_name", ""),
                "is_bot": u.get("is_bot", False),
            }

        cursor = result.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break

    print(f"  Fetched {len(users)} users", file=sys.stderr)
    return users


def load_users(workspace_dir):
    path = os.path.join(workspace_dir, "users.json")
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def _harvest_user_profiles(workspace_dir):
    """Scan exported channel JSON files for user_profile data not in users.json."""
    channels_dir = os.path.join(workspace_dir, "channels")
    if not os.path.isdir(channels_dir):
        return {}

    with open(os.path.join(workspace_dir, "users.json")) as f:
        existing = json.load(f)

    extra = {}
    for fname in os.listdir(channels_dir):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(channels_dir, fname)) as f:
            data = json.load(f)
        for m in data.get("messages", []):
            uid = m.get("user", "")
            if not uid or uid in existing or uid in extra:
                continue
            prof = m.get("user_profile", {})
            if prof.get("real_name") or prof.get("display_name"):
                extra[uid] = {
                    "name": prof.get("name", prof.get("display_name", "")),
                    "real_name": prof.get("real_name", ""),
                    "display_name": prof.get("display_name", ""),
                    "is_bot": False,
                }
    return extra


# ===================================================================
# Storage
# ===================================================================

def load_state(workspace_dir):
    path = os.path.join(workspace_dir, "state.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save_state(workspace_dir, state):
    path = os.path.join(workspace_dir, "state.json")
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def save_workspace_meta(workspace_dir, team):
    path = os.path.join(workspace_dir, "workspace.json")
    payload = {
        "team_id": team["id"],
        "name": team["name"],
        "domain": team["domain"],
        "dir_name": os.path.basename(workspace_dir),
        "is_enterprise": team["is_enterprise"],
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)


def load_known_channels(workspace_dir, channel_ids=None):
    channels = {}
    selected = set(channel_ids or [])
    channels_dir = os.path.join(workspace_dir, "channels")
    if os.path.isdir(channels_dir):
        for fname in os.listdir(channels_dir):
            if not fname.endswith(".json"):
                continue
            cid = fname[:-5]
            if selected and cid not in selected:
                continue
            with open(os.path.join(channels_dir, fname)) as f:
                data = json.load(f)
            meta = data.get("channel", {})
            if meta.get("id"):
                channels[cid] = meta

    state = load_state(workspace_dir)
    for cid in selected:
        if cid in channels:
            continue
        name = state.get(cid, {}).get("name", cid)
        channels[cid] = {"id": cid, "name": name}
    return channels


def fetch_channel_metadata(session, channel_id):
    info = session.api_call("conversations.info", {"channel": channel_id}, reason="channels/info")
    if info.get("ok"):
        return _channel_meta(info["channel"])
    return {"id": channel_id, "name": channel_id}


def resolve_channels(session, workspace_dir, channel_ids=None, skip_discovery=False):
    selected = set(channel_ids or [])
    if skip_discovery:
        channels = load_known_channels(workspace_dir, channel_ids=channel_ids)
        missing = selected - set(channels)
        for cid in missing:
            channels[cid] = fetch_channel_metadata(session, cid)
        return channels

    channels = discover_channels(session)
    if selected:
        missing = selected - set(channels)
        for cid in missing:
            channels[cid] = fetch_channel_metadata(session, cid)
        channels = {cid: meta for cid, meta in channels.items() if cid in selected}
    return channels


def apply_since_buffer(oldest, seconds):
    if seconds <= 0:
        return oldest
    try:
        return f"{max(0.0, float(oldest) - float(seconds)):.6f}"
    except (TypeError, ValueError):
        return oldest


def save_channel(workspace_dir, channel_meta, messages):
    channels_dir = os.path.join(workspace_dir, "channels")
    os.makedirs(channels_dir, exist_ok=True)
    path = os.path.join(channels_dir, f"{channel_meta['id']}.json")

    existing_messages = []
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
            existing_messages = data.get("messages", [])

    existing_by_ts = {m["ts"]: m for m in existing_messages if m.get("ts")}
    new_count = 0
    for msg in messages:
        ts = msg.get("ts")
        if not ts:
            continue
        if ts not in existing_by_ts:
            new_count += 1
        existing_by_ts[ts] = msg

    merged = sorted(existing_by_ts.values(), key=lambda m: float(m["ts"]), reverse=True)

    with open(path, "w") as f:
        json.dump({"channel": channel_meta, "messages": merged}, f, indent=2, ensure_ascii=False)

    return new_count


def merge_thread_replies(workspace_dir, channel_meta, thread_ts, session):
    path = os.path.join(workspace_dir, "channels", f"{channel_meta['id']}.json")
    if not os.path.exists(path):
        return False, None

    with open(path) as f:
        data = json.load(f)
    messages = data.get("messages", [])

    parent = next((m for m in messages if m.get("ts") == thread_ts), None)
    if parent is None:
        result = session.api_call(
            "conversations.history",
            {
                "channel": channel_meta["id"],
                "oldest": thread_ts,
                "latest": thread_ts,
                "inclusive": "true",
                "limit": "1",
            },
            reason="message-pane/requestHistory",
        )
        if result.get("ok"):
            fetched = result.get("messages", [])
            if fetched:
                parent = fetched[0]
                messages.append(parent)
        if parent is None:
            return False, None

    replies = _fetch_thread(session, channel_meta["id"], thread_ts)
    parent["replies_full"] = replies
    data["channel"] = channel_meta
    data["messages"] = sorted(messages, key=lambda m: float(m.get("ts", 0)), reverse=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    latest_reply = max((r.get("ts") for r in replies), default=None)
    return True, latest_reply


def save_users(workspace_dir, users):
    path = os.path.join(workspace_dir, "users.json")
    with open(path, "w") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


# ===================================================================
# Main
# ===================================================================

def export_workspace(team, d_cookie, aux_cookies, args):
    """Export a single workspace."""
    domain = team["domain"]
    dir_name = f"{domain}-enterprise" if team["is_enterprise"] else domain
    workspace_dir = os.path.join(SLACK_DATA_DIR, dir_name)
    os.makedirs(workspace_dir, exist_ok=True)
    save_workspace_meta(workspace_dir, team)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Exporting: {team['name']} ({domain})", file=sys.stderr)
    print(f"  User: {team['user_id']}", file=sys.stderr)
    print(f"  Enterprise: {team['is_enterprise']}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    session = SlackSession(team, d_cookie, aux_cookies)

    # Verify auth
    auth = session.api_call("auth.test", reason="auth/verify")
    if not auth.get("ok"):
        print(f"  Auth failed: {auth.get('error')}", file=sys.stderr)
        return
    print(f"  Authenticated as: {auth.get('user')} @ {auth.get('team')}", file=sys.stderr)

    users = load_users(workspace_dir)
    if not args.skip_users:
        print("\n  Fetching users...", file=sys.stderr)
        users = fetch_users(session)
        save_users(workspace_dir, users)

    channel_ids = args.channels or []
    if args.skip_discovery:
        print("\n  Loading known channels...", file=sys.stderr)
    else:
        print("\n  Discovering channels...", file=sys.stderr)
    channels = resolve_channels(
        session,
        workspace_dir,
        channel_ids=channel_ids,
        skip_discovery=args.skip_discovery,
    )

    # Load incremental state
    state = load_state(workspace_dir)

    # Export each channel
    total_new = 0
    touched_channels = set()
    threads_by_channel = {}
    for cid, thread_ts in args.thread_specs:
        threads_by_channel.setdefault(cid, set()).add(thread_ts)
    for i, (cid, meta) in enumerate(channels.items(), 1):
        name = meta.get("name", cid)
        # For DMs, resolve user name
        if meta.get("is_im") and name in users:
            name = users[name].get("real_name") or users[name].get("name") or name
            meta["resolved_name"] = name

        oldest = state.get(cid, {}).get("last_ts", "0")
        oldest = apply_since_buffer(oldest, args.since_buffer_sec)
        label = f"DM:{name}" if meta.get("is_im") else f"#{name}"
        print(f"\n  [{i}/{len(channels)}] {label} (since {oldest})", file=sys.stderr)

        messages = export_channel_messages(session, cid, oldest=oldest)
        if messages is None:
            continue

        if messages:
            new_count = save_channel(workspace_dir, meta, messages)
            total_new += new_count
            touched_channels.add(cid)

            latest_ts = max(m["ts"] for m in messages)
            state[cid] = {"last_ts": latest_ts, "name": name}
            save_state(workspace_dir, state)
            print(f"    Saved {new_count} new messages", file=sys.stderr)
        else:
            print(f"    No new messages", file=sys.stderr)

        for thread_ts in sorted(threads_by_channel.get(cid, [])):
            ok, latest_reply = merge_thread_replies(workspace_dir, meta, thread_ts, session)
            if ok:
                touched_channels.add(cid)
                if latest_reply:
                    prev = state.get(cid, {}).get("last_ts", "0")
                    state[cid] = {"last_ts": max(prev, latest_reply, key=float), "name": name}
                    save_state(workspace_dir, state)
                print(f"    Refreshed thread {thread_ts}", file=sys.stderr)

    # Augment users.json with names found in message user_profile fields
    extra = _harvest_user_profiles(workspace_dir)
    if extra:
        users.update(extra)
        save_users(workspace_dir, users)
        print(f"\n  Users updated: {len(users)} total ({len(extra)} from message profiles)", file=sys.stderr)

    # Generate readable markdown
    sys.path.insert(0, SCRIPT_DIR)
    from process_exports import process_slack_workspace
    clean = not args.skip_discovery and not args.channels
    channel_subset = None if clean else touched_channels
    n = process_slack_workspace(workspace_dir, channel_ids=channel_subset, clean=clean)
    print(f"\n  Generated {n} readable files", file=sys.stderr)

    print(f"\n  Done: {total_new} new messages across {len(channels)} channels", file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser(description="Export Slack conversations to local JSON.")
    parser.add_argument("--workspace", action="append", default=[],
                        help="Workspace directory name or Slack domain to export.")
    parser.add_argument("--channels", action="append", default=[],
                        help="Comma-separated channel IDs to sync.")
    parser.add_argument("--thread", action="append", default=[],
                        help="Specific thread to refresh, formatted as CHANNEL_ID:THREAD_TS.")
    parser.add_argument("--skip-discovery", action="store_true",
                        help="Use known channels from local state instead of rediscovering.")
    parser.add_argument("--skip-users", action="store_true",
                        help="Skip users.list and reuse existing users.json.")
    parser.add_argument("--since-buffer-sec", type=int, default=120,
                        help="Re-fetch a small overlap before the last saved cursor.")
    parser.add_argument("--threads", action="store_true",
                        help="Fetch full thread replies for matching channels.")
    args = parser.parse_args()
    channel_ids = []
    for value in args.channels:
        channel_ids.extend(v.strip() for v in value.split(",") if v.strip())
    args.channels = channel_ids
    thread_specs = []
    for value in args.thread:
        for item in value.split(","):
            item = item.strip()
            if not item or ":" not in item:
                continue
            cid, thread_ts = item.split(":", 1)
            cid = cid.strip()
            thread_ts = thread_ts.strip()
            if cid and thread_ts:
                thread_specs.append((cid, thread_ts))
                if cid not in channel_ids:
                    channel_ids.append(cid)
    args.channels = channel_ids
    args.thread_specs = thread_specs
    return args


def main():
    global FETCH_THREADS
    args = parse_args()
    FETCH_THREADS = args.threads

    print("Extracting Slack credentials...", file=sys.stderr)
    teams, d_cookie, aux_cookies = extract_credentials()

    if not d_cookie:
        print("Error: Could not extract d cookie from Slack desktop app", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(teams)} workspace(s): {', '.join(t['name'] for t in teams.values())}", file=sys.stderr)
    print(f"Cookie: d={d_cookie[:30]}...", file=sys.stderr)

    os.makedirs(SLACK_DATA_DIR, exist_ok=True)

    filter_domains = set(args.workspace) if args.workspace else None

    for team in teams.values():
        # Skip enterprise workspace when a non-enterprise one exists for the same domain
        # (they share the same channels and the non-enterprise has more)
        if team["is_enterprise"]:
            has_non_ent = any(
                t["domain"] == team["domain"] and not t["is_enterprise"]
                for t in teams.values()
            )
            if has_non_ent:
                print(f"Skipping {team['name']} enterprise (non-enterprise superset exists)", file=sys.stderr)
                continue

        dir_name = f"{team['domain']}-enterprise" if team["is_enterprise"] else team["domain"]
        if filter_domains and dir_name not in filter_domains and team["domain"] not in filter_domains:
            continue
        export_workspace(team, d_cookie, aux_cookies, args)

    print("\nExport complete.", file=sys.stderr)


if __name__ == "__main__":
    main()
