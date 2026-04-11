#!/usr/bin/env python3
"""Post-process Slack and Teams raw JSON exports into agent-readable markdown.

Resolves user IDs, strips platform markup, inlines thread replies, groups by
date, and writes one .md file per conversation under a `readable/` directory.
"""

import glob
import html
import json
import os
import re
import sys
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")


# ===================================================================
# User lookup
# ===================================================================

def load_slack_users(workspace_dir):
    """Load users.json and also harvest user_profile from message files."""
    users = {}
    users_path = os.path.join(workspace_dir, "users.json")
    if os.path.exists(users_path):
        with open(users_path) as f:
            users = json.load(f)

    channels_dir = os.path.join(workspace_dir, "channels")
    if os.path.isdir(channels_dir):
        for fname in os.listdir(channels_dir):
            if not fname.endswith(".json"):
                continue
            with open(os.path.join(channels_dir, fname)) as f:
                data = json.load(f)
            for m in data.get("messages", []):
                uid = m.get("user", "")
                if uid and uid not in users:
                    prof = m.get("user_profile", {})
                    if prof.get("real_name") or prof.get("display_name"):
                        users[uid] = {
                            "name": prof.get("name", ""),
                            "real_name": prof.get("real_name", ""),
                            "display_name": prof.get("display_name", ""),
                        }

    return users


def _resolve_name(users, uid):
    u = users.get(uid, {})
    return u.get("real_name") or u.get("display_name") or u.get("name") or uid


# ===================================================================
# Slack processing
# ===================================================================

def _slack_ts_to_dt(ts_str):
    try:
        return datetime.fromtimestamp(float(ts_str), tz=timezone.utc)
    except (ValueError, OSError):
        return None


def _clean_slack_text(text, users):
    """Resolve Slack markup to plain text."""
    # <@U123> -> @Name
    def replace_user(m):
        uid = m.group(1)
        return f"@{_resolve_name(users, uid)}"
    text = re.sub(r"<@(U[A-Z0-9]+)(?:\|[^>]*)?>", replace_user, text)

    # <#C123|channel-name> -> #channel-name
    text = re.sub(r"<#[A-Z0-9]+\|([^>]+)>", r"#\1", text)

    # <URL|label> -> label
    text = re.sub(r"<(https?://[^|>]+)\|([^>]+)>", r"\2", text)

    # <URL> -> URL
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)

    # <!subteam^...|@group> -> @group
    text = re.sub(r"<!subteam\^[A-Z0-9]+\|(@[^>]+)>", r"\1", text)
    text = re.sub(r"<!(?:here|channel|everyone)(?:\|@([^>]+))?>",
                  lambda m: f"@{m.group(1)}" if m.group(1) else "@here", text)

    return text


def _format_reactions(reactions, users):
    """Format a message's reactions list as a bracketed inline annotation."""
    parts = []
    for r in reactions:
        names = ", ".join(_resolve_name(users, uid) for uid in r.get("users", []))
        parts.append(f":{r['name']}: {names}")
    return "[reactions: " + " \u00b7 ".join(parts) + "]"


def process_slack_workspace(workspace_dir, channel_ids=None, clean=True):
    """Process Slack channel JSON files into readable markdown."""
    channels_dir = os.path.join(workspace_dir, "channels")
    if not os.path.isdir(channels_dir):
        return 0

    users = load_slack_users(workspace_dir)
    readable_dir = os.path.join(workspace_dir, "readable")
    if clean and os.path.isdir(readable_dir):
        for f in os.listdir(readable_dir):
            if f.endswith(".md"):
                os.remove(os.path.join(readable_dir, f))
    os.makedirs(readable_dir, exist_ok=True)

    selected = set(channel_ids or [])
    count = 0
    for fname in sorted(os.listdir(channels_dir)):
        if not fname.endswith(".json"):
            continue
        cid = fname[:-5]
        if selected and cid not in selected:
            continue
        with open(os.path.join(channels_dir, fname)) as f:
            data = json.load(f)

        channel = data.get("channel", {})
        messages = data.get("messages", [])
        if not messages:
            continue

        ch_name = channel.get("resolved_name") or channel.get("name", fname.replace(".json", ""))
        is_im = channel.get("is_im", False)
        if is_im and ch_name.startswith("U"):
            ch_name = _resolve_name(users, ch_name)
        title = f"DM: {ch_name}" if is_im else f"#{ch_name}"

        md = _slack_messages_to_md(title, messages, users)

        out_path = os.path.join(readable_dir, f"slack_{channel.get('id', cid)}.md")
        with open(out_path, "w") as f:
            f.write(md)
        count += 1

    return count


def _slack_messages_to_md(title, messages, users):
    # Sort oldest-first for output
    messages = sorted(messages, key=lambda m: float(m.get("ts", 0)))

    # Group thread replies under their parent
    threads = {}
    top_level = []
    for m in messages:
        thread_ts = m.get("thread_ts")
        ts = m.get("ts")
        if thread_ts and thread_ts != ts:
            threads.setdefault(thread_ts, []).append(m)
        else:
            top_level.append(m)

    lines = [f"# {title}\n"]
    current_date = None

    for m in top_level:
        dt = _slack_ts_to_dt(m.get("ts", "0"))
        if not dt:
            continue

        date_str = dt.strftime("%Y-%m-%d")
        if date_str != current_date:
            current_date = date_str
            lines.append(f"\n## {date_str}\n")

        user_name = _resolve_name(users, m.get("user", ""))
        time_str = dt.strftime("%H:%M")
        text = _clean_slack_text(m.get("text", ""), users)

        # Attached files
        files = m.get("files", [])
        file_notes = []
        for f in files:
            file_notes.append(f"[file: {f.get('title') or f.get('name', 'attachment')}]")

        lines.append(f"**{user_name}** ({time_str}):")
        lines.append(text)
        for fn in file_notes:
            lines.append(f"> {fn}")

        reactions = m.get("reactions")
        if reactions:
            lines.append(_format_reactions(reactions, users))

        # Thread replies
        reply_list = threads.get(m.get("ts"), [])
        replies_full = m.get("replies_full", [])
        all_replies = reply_list + replies_full
        if all_replies:
            all_replies.sort(key=lambda r: r.get("ts", r.get("composetime", "0")))
            for r in all_replies:
                rdt = _slack_ts_to_dt(r.get("ts", "0"))
                rtime = rdt.strftime("%H:%M") if rdt else "?"
                rname = _resolve_name(users, r.get("user", ""))
                rtext = _clean_slack_text(r.get("text", ""), users)
                lines.append(f"  > **{rname}** ({rtime}): {rtext}")
                rreactions = r.get("reactions")
                if rreactions:
                    lines.append(f"  > {_format_reactions(rreactions, users)}")
        elif m.get("reply_count", 0) > 0:
            lines.append(f"  > [{m['reply_count']} replies not fetched]")

        lines.append("")

    return "\n".join(lines)


# ===================================================================
# Teams processing
# ===================================================================

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_TEAMS_MENTION_RE = re.compile(
    r'<span[^>]*itemtype="http://schema\.skype\.com/Mention"[^>]*>([^<]*)</span>'
)


def _clean_teams_html(content):
    """Strip Teams HTML to plain text, preserving @mentions."""
    if not content:
        return ""
    # Replace mention spans with @Name
    text = _TEAMS_MENTION_RE.sub(r"@\1", content)
    # <br> / <br/> -> newline
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    # <p>...</p> -> paragraph
    text = re.sub(r"</p>\s*<p>", "\n\n", text, flags=re.IGNORECASE)
    # <li> -> bullet
    text = re.sub(r"<li[^>]*>", "- ", text, flags=re.IGNORECASE)
    # Strip remaining tags
    text = _HTML_TAG_RE.sub("", text)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up excess whitespace
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def _teams_dt(dt_str):
    if not dt_str:
        return None
    try:
        clean = dt_str.replace("Z", "+00:00")
        if "." in clean:
            # Truncate fractional seconds to 6 digits max
            parts = clean.split(".")
            frac_and_tz = parts[1]
            frac = re.match(r"(\d+)", frac_and_tz).group(1)[:6]
            rest = frac_and_tz[len(re.match(r"\d+", frac_and_tz).group(0)):]
            clean = f"{parts[0]}.{frac}{rest}"
        return datetime.fromisoformat(clean)
    except (ValueError, AttributeError):
        return None


def process_teams_workspace(workspace_dir, conversations=None, clean=True):
    """Process Teams chat/channel JSON files into readable markdown."""
    readable_dir = os.path.join(workspace_dir, "readable")
    if clean and os.path.isdir(readable_dir):
        for f in os.listdir(readable_dir):
            if f.endswith(".md"):
                os.remove(os.path.join(readable_dir, f))
    os.makedirs(readable_dir, exist_ok=True)
    count = 0
    selected = None
    if conversations:
        selected = {(subdir, cid) for subdir, cid in conversations}

    for subdir in ("chats", "channels"):
        src_dir = os.path.join(workspace_dir, subdir)
        if not os.path.isdir(src_dir):
            continue

        for fname in sorted(os.listdir(src_dir)):
            if not fname.endswith(".json"):
                continue
            with open(os.path.join(src_dir, fname)) as f:
                data = json.load(f)

            meta = data.get("meta", {})
            cid = meta.get("id")
            if selected and (subdir, cid) not in selected:
                continue
            messages = data.get("messages", [])
            if not messages:
                continue

            if subdir == "chats":
                title = meta.get("topic") or f"Chat: {', '.join(meta.get('members', [])[:3])}"
            else:
                title = f"{meta.get('team_name', '')}/#{meta.get('channel_name', '')}"

            md = _teams_messages_to_md(title, messages)

            safe_id = (cid or fname[:-5]).replace(":", "_").replace("/", "_").replace("@", "_")[:100]
            prefix = "teams_chat" if subdir == "chats" else "teams_channel"
            out_path = os.path.join(readable_dir, f"{prefix}_{safe_id}.md")
            with open(out_path, "w") as f:
                f.write(md)
            count += 1

    return count


def _teams_messages_to_md(title, messages):
    # Sort oldest-first
    messages = sorted(messages, key=lambda m: m.get("composetime") or m.get("originalarrivaltime", ""))

    lines = [f"# {title}\n"]
    current_date = None

    for m in messages:
        dt = _teams_dt(m.get("composetime") or m.get("originalarrivaltime", ""))
        if not dt:
            continue

        date_str = dt.strftime("%Y-%m-%d")
        if date_str != current_date:
            current_date = date_str
            lines.append(f"\n## {date_str}\n")

        sender = m.get("imdisplayname") or m.get("fromDisplayNameInToken") or "?"
        time_str = dt.strftime("%H:%M")
        text = _clean_teams_html(m.get("content", ""))

        if not text.strip():
            continue

        lines.append(f"**{sender}** ({time_str}):")
        lines.append(text)
        lines.append("")

    return "\n".join(lines)


# ===================================================================
# Main
# ===================================================================

def process_all():
    """Process all Slack and Teams exports."""
    total = 0

    # Slack workspaces
    slack_dir = os.path.join(DATA_DIR, "slack")
    if os.path.isdir(slack_dir):
        for name in sorted(os.listdir(slack_dir)):
            ws = os.path.join(slack_dir, name)
            if not os.path.isdir(ws) or not os.path.exists(os.path.join(ws, "channels")):
                continue
            print(f"Processing Slack/{name}...", file=sys.stderr)
            n = process_slack_workspace(ws)
            print(f"  {n} files written to readable/", file=sys.stderr)
            total += n

    # Teams workspaces
    teams_dir = os.path.join(DATA_DIR, "teams")
    if os.path.isdir(teams_dir):
        for name in sorted(os.listdir(teams_dir)):
            ws = os.path.join(teams_dir, name)
            if not os.path.isdir(ws):
                continue
            print(f"Processing Teams/{name}...", file=sys.stderr)
            n = process_teams_workspace(ws)
            print(f"  {n} files written to readable/", file=sys.stderr)
            total += n

    print(f"\nDone: {total} readable files generated.", file=sys.stderr)
    return total


if __name__ == "__main__":
    process_all()
