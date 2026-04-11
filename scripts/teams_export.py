#!/usr/bin/env python3
"""Export Microsoft Teams chats, channels and messages to local JSON files.

Extracts MSAL access tokens from Brave's local storage and uses Teams'
internal APIs (CSA for discovery, IC3 for messages) to download history.
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
TEAMS_DATA_DIR = os.path.join(DATA_DIR, "teams")
BRAVE_LS_DIR = os.path.expanduser(
    "~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Local Storage/leveldb"
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TENANT_ID = "19f2cb54-1b2f-4f42-837c-4abec52940ec"
CSA_BASE = "https://teams.microsoft.com/api/csa/api/v2/teams"
MSG_BASE = "https://emea.ng.msg.teams.microsoft.com/v1/users/ME/conversations"
PAGE_SIZE = 50
REQUEST_DELAY = 0.3
OLDEST_DT = "2025-12-01T00:00:00.0000000Z"


# ===================================================================
# Token extraction from Brave
# ===================================================================

def _decode_jwt_payload(jwt):
    parts = jwt.split(".")
    if len(parts) < 2:
        return {}
    pad = parts[1] + "=" * (4 - len(parts[1]) % 4)
    return json.loads(base64.b64decode(pad))


def extract_tokens():
    """Extract Teams access tokens from Brave's Local Storage LevelDB.

    Returns dict mapping audience to JWT for tokens that are still valid.
    """
    tmp = tempfile.mkdtemp(prefix="brave-ls-")
    try:
        for f in os.listdir(BRAVE_LS_DIR):
            src = os.path.join(BRAVE_LS_DIR, f)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(tmp, f))
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
  const tokens = {};
  for await (const [key, value] of db.iterator()) {
    const k = key.toString('utf-8');
    if (!k.includes('teams.microsoft.com') && !k.includes('teams.cloud.microsoft')) continue;
    if (!k.includes('accesstoken')) continue;
    const raw = value.toString('utf-8');
    const i = raw.indexOf('{');
    if (i < 0) continue;
    try {
      const tok = JSON.parse(raw.substring(i));
      if (!tok.secret || !tok.secret.includes('.')) continue;
      // Decode audience from JWT
      const parts = tok.secret.split('.');
      const payload = JSON.parse(Buffer.from(parts[1] + '='.repeat(4 - parts[1].length % 4), 'base64').toString());
      const aud = payload.aud || '';
      const exp = payload.exp || 0;
      // Keep the token with latest expiry per audience
      if (!tokens[aud] || exp > tokens[aud].exp) {
        tokens[aud] = { secret: tok.secret, exp };
      }
    } catch {}
  }
  await db.close();
  process.stdout.write(JSON.stringify(tokens));
})();
"""
        proc = subprocess.run(
            ["node", "-e", node_script, tmp],
            capture_output=True, text=True, timeout=15, cwd=PROJECT_DIR,
        )
        if proc.returncode != 0:
            print(f"Error reading LevelDB: {proc.stderr}", file=sys.stderr)
            return {}

        raw_tokens = json.loads(proc.stdout)
        now = time.time()
        valid = {}
        for aud, info in raw_tokens.items():
            if info["exp"] > now:
                valid[aud] = info["secret"]
        return valid
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def get_required_tokens(all_tokens):
    """Pick the CSA and IC3 tokens from the extracted set."""
    csa_token = None
    ic3_token = None

    for aud, jwt in all_tokens.items():
        if "chatsvcagg" in aud:
            csa_token = jwt
        elif "ic3.teams.office" in aud:
            ic3_token = jwt

    return csa_token, ic3_token


# ===================================================================
# CSA API — discovery
# ===================================================================

def csa_fetch_all(csa_token):
    """Fetch teams, channels, and chats via the CSA cold-boot endpoint."""
    resp = requests.get(
        f"{CSA_BASE}/users/me",
        headers={"Authorization": f"Bearer {csa_token}", "Accept": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def parse_chats(csa_data):
    """Extract chat metadata from CSA response."""
    chats = {}
    for ch in csa_data.get("chats", []):
        cid = ch["id"]
        members = []
        for m in ch.get("members", []):
            name = m.get("displayName") or m.get("objectId", "")
            if name:
                members.append(name)
        chats[cid] = {
            "id": cid,
            "chatType": ch.get("chatType", ch.get("threadType", "")),
            "topic": ch.get("title") or "",
            "members": members,
            "isOneOnOne": ch.get("isOneOnOne", False),
            "createdAt": ch.get("createdAt"),
        }
    return chats


def parse_channels(csa_data):
    """Extract team/channel metadata from CSA response."""
    channels = {}
    for team in csa_data.get("teams", []):
        team_name = team.get("displayName", "")
        team_id_raw = team.get("id", "")
        for ch in team.get("channels", []):
            cid = ch["id"]
            channels[cid] = {
                "id": cid,
                "team_name": team_name,
                "team_thread_id": team_id_raw,
                "channel_name": ch.get("displayName", ""),
                "description": ch.get("description", ""),
                "isGeneral": ch.get("isGeneral", False),
            }
    return channels


# ===================================================================
# IC3 API — messages
# ===================================================================

def fetch_messages(ic3_token, conversation_id, since_dt=None, max_pages=200):
    """Fetch message history for a conversation via the IC3 messaging backend."""
    headers = {"Authorization": f"Bearer {ic3_token}", "Accept": "application/json"}
    all_messages = []
    url = f"{MSG_BASE}/{conversation_id}/messages"
    params = {"pageSize": str(PAGE_SIZE), "view": "superchat"}
    page = 0

    while url and page < max_pages:
        resp = requests.get(url, headers=headers, params=params if page == 0 else None, timeout=30)

        if resp.status_code == 429:
            retry = int(resp.headers.get("Retry-After", 10))
            print(f"    Rate limited, waiting {retry}s...", file=sys.stderr)
            time.sleep(retry)
            continue

        if resp.status_code in (403, 404):
            if page == 0:
                return None
            break

        if not resp.ok:
            print(f"    HTTP {resp.status_code}: {resp.text[:150]}", file=sys.stderr)
            break

        data = resp.json()
        messages = data.get("messages", [])
        if not messages:
            break

        hit_cutoff = False
        for msg in messages:
            dt = msg.get("composetime") or msg.get("originalarrivaltime", "")
            if dt < OLDEST_DT:
                hit_cutoff = True
                break
            if since_dt and dt <= since_dt:
                hit_cutoff = True
                break
            # Skip system messages (member adds/removes/topic changes)
            mtype = msg.get("messagetype", "")
            if mtype in ("ThreadActivity/AddMember", "ThreadActivity/MemberJoined",
                         "ThreadActivity/MemberLeft", "ThreadActivity/DeleteMember",
                         "ThreadActivity/TopicUpdate", "ThreadActivity/HistoryDisclosedUpdate",
                         "Event/Call"):
                continue
            all_messages.append(msg)

        page += 1
        if page % 5 == 0:
            print(f"    ... {len(all_messages)} messages so far (page {page})", file=sys.stderr)

        if hit_cutoff:
            break

        time.sleep(REQUEST_DELAY)
        url = data.get("_metadata", {}).get("backwardLink")

    print(f"    {len(all_messages)} messages ({page} pages)", file=sys.stderr)
    return all_messages


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
    with open(os.path.join(workspace_dir, "state.json"), "w") as f:
        json.dump(state, f, indent=2)


def load_manifest(workspace_dir):
    path = os.path.join(workspace_dir, "manifest.json")
    if not os.path.exists(path):
        return {"chats": {}, "channels": {}}
    with open(path) as f:
        return json.load(f)


def save_manifest(workspace_dir, chats, channels):
    payload = {
        "chats": chats,
        "channels": channels,
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(os.path.join(workspace_dir, "manifest.json"), "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def save_conversation(workspace_dir, subdir, meta, messages):
    out_dir = os.path.join(workspace_dir, subdir)
    os.makedirs(out_dir, exist_ok=True)
    safe_id = meta["id"].replace(":", "_").replace("/", "_").replace("@", "_")[:100]
    path = os.path.join(out_dir, f"{safe_id}.json")

    existing = []
    if os.path.exists(path):
        with open(path) as f:
            existing = json.load(f).get("messages", [])

    existing_by_id = {}
    for m in existing:
        mid = m.get("id") or m.get("clientmessageid") or m.get("originalarrivaltime", "")
        if mid:
            existing_by_id[mid] = m

    new_count = 0
    for m in messages:
        mid = m.get("id") or m.get("clientmessageid") or m.get("originalarrivaltime", "")
        if not mid:
            continue
        if mid not in existing_by_id:
            new_count += 1
        existing_by_id[mid] = m

    merged = sorted(existing_by_id.values(),
                    key=lambda m: m.get("composetime") or m.get("originalarrivaltime", ""),
                    reverse=True)

    with open(path, "w") as f:
        json.dump({"meta": meta, "messages": merged}, f, indent=2, ensure_ascii=False)

    return new_count


# ===================================================================
# Sync helpers
# ===================================================================

def discover_workspace(csa_token, workspace_dir):
    print("\nFetching conversation list...", file=sys.stderr)
    csa_data = csa_fetch_all(csa_token)
    chats = parse_chats(csa_data)
    channels = parse_channels(csa_data)
    save_manifest(workspace_dir, chats, channels)
    print(f"  {len(chats)} chats, {len(channels)} channels", file=sys.stderr)
    return chats, channels


def iter_manifest_conversations(manifest, conversation_ids=None):
    selected = set(conversation_ids or [])
    for cid, meta in manifest.get("chats", {}).items():
        if selected and cid not in selected:
            continue
        yield "chats", cid, meta
    for cid, meta in manifest.get("channels", {}).items():
        if selected and cid not in selected:
            continue
        yield "channels", cid, meta


def sync_manifest_conversations(ic3_token, workspace_dir, manifest, state, conversation_ids=None):
    touched = []
    totals = {"chats": 0, "channels": 0}
    items = list(iter_manifest_conversations(manifest, conversation_ids=conversation_ids))
    chats_total = sum(1 for subdir, _, _ in items if subdir == "chats")
    channels_total = len(items) - chats_total

    if chats_total:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Syncing {chats_total} chats", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
    chat_index = 0
    channel_index = 0

    for subdir, cid, meta in items:
        if subdir == "chats":
            chat_index += 1
            label = meta.get("topic") or ", ".join(meta.get("members", [])[:3]) or cid[:30]
            index = chat_index
            total = chats_total
            kind = meta.get("chatType", "chat")
            prefix = f"{kind}: "
        else:
            if channel_index == 0 and channels_total:
                print(f"\n{'='*60}", file=sys.stderr)
                print(f"Syncing {channels_total} channels", file=sys.stderr)
                print(f"{'='*60}", file=sys.stderr)
            channel_index += 1
            label = f"{meta.get('team_name', '')}/#{meta.get('channel_name', '')}"
            index = channel_index
            total = channels_total
            prefix = ""

        since = state.get(cid, {}).get("last_dt")
        print(f"\n  [{index}/{total}] {prefix}{label} (since {since or 'beginning'})", file=sys.stderr)

        messages = fetch_messages(ic3_token, cid, since_dt=since)
        if messages is None:
            print(f"    Skipped (no access)", file=sys.stderr)
            continue

        if messages:
            new_count = save_conversation(workspace_dir, subdir, meta, messages)
            totals[subdir] += new_count
            latest = max(m.get("composetime") or m.get("originalarrivaltime", "") for m in messages)
            state[cid] = {"last_dt": latest}
            save_state(workspace_dir, state)
            touched.append((subdir, cid))
            print(f"    Saved {new_count} new messages", file=sys.stderr)
        else:
            print(f"    No new messages", file=sys.stderr)

    return touched, totals


def parse_args():
    parser = argparse.ArgumentParser(description="Export Teams conversations to local JSON.")
    parser.add_argument("--discover-only", action="store_true",
                        help="Refresh the CSA manifest and exit without syncing message history.")
    parser.add_argument("--sync-known", action="store_true",
                        help="Sync only conversations already present in manifest.json.")
    parser.add_argument("--conversation-ids", action="append", default=[],
                        help="Comma-separated Teams conversation IDs to sync from the manifest.")
    args = parser.parse_args()
    convo_ids = []
    for value in args.conversation_ids:
        convo_ids.extend(v.strip() for v in value.split(",") if v.strip())
    args.conversation_ids = convo_ids
    return args


# ===================================================================
# Main
# ===================================================================

def main():
    args = parse_args()
    workspace_dir = os.path.join(TEAMS_DATA_DIR, "sierra")
    os.makedirs(workspace_dir, exist_ok=True)
    manifest = load_manifest(workspace_dir)

    print("Extracting tokens from Brave...", file=sys.stderr)
    all_tokens = extract_tokens()
    print(f"  Found {len(all_tokens)} valid tokens", file=sys.stderr)

    csa_token, ic3_token = get_required_tokens(all_tokens)
    needs_discovery = args.discover_only or not args.sync_known or (not manifest.get("chats") and not manifest.get("channels"))
    needs_ic3 = not args.discover_only
    missing = []
    if needs_discovery and not csa_token:
        missing.append("chatsvcagg (CSA)")
    if needs_ic3 and not ic3_token:
        missing.append("ic3.teams.office.com (messaging)")
    if missing:
        missing = []
        if needs_discovery and not csa_token:
            missing.append("chatsvcagg (CSA)")
        if needs_ic3 and not ic3_token:
            missing.append("ic3.teams.office.com (messaging)")
        print(
            f"\nError: Missing required token(s): {', '.join(missing)}\n"
            "  1. Open teams.microsoft.com in Brave and wait for it to fully load\n"
            "  2. Re-run this script (tokens are valid for ~1 hour)\n",
            file=sys.stderr,
        )
        sys.exit(1)

    # Show token TTLs
    for aud in ("chatsvcagg", "ic3.teams.office"):
        for a, jwt in all_tokens.items():
            if aud in a:
                payload = _decode_jwt_payload(jwt)
                ttl = int(payload.get("exp", 0) - time.time())
                print(f"  {aud}: {ttl // 60}m remaining", file=sys.stderr)

    if needs_discovery:
        chats, channels = discover_workspace(csa_token, workspace_dir)
        manifest = {"chats": chats, "channels": channels}
        if args.discover_only:
            print("\nDiscovery complete.", file=sys.stderr)
            return

    if args.sync_known and not manifest.get("chats") and not manifest.get("channels"):
        print("\nManifest is empty; nothing to sync.", file=sys.stderr)
        return

    state = load_state(workspace_dir)
    touched, totals = sync_manifest_conversations(
        ic3_token,
        workspace_dir,
        manifest,
        state,
        conversation_ids=args.conversation_ids,
    )

    # Generate readable markdown
    sys.path.insert(0, SCRIPT_DIR)
    from process_exports import process_teams_workspace
    clean = not args.sync_known and not args.conversation_ids
    conversation_subset = None if clean else touched
    n = process_teams_workspace(workspace_dir, conversations=conversation_subset, clean=clean)
    print(f"\n  Generated {n} readable files", file=sys.stderr)

    total = totals["chats"] + totals["channels"]
    print(f"\nExport complete. {total} new messages ({totals['chats']} from chats, {totals['channels']} from channels).", file=sys.stderr)


if __name__ == "__main__":
    main()
