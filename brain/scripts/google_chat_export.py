#!/usr/bin/env python3
"""Scrape the two Sierra Google Chat spaces through the signed-in browser."""
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from process_exports import process_google_chat_workspace

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "data" / "google-chat" / "sierra"
ACCOUNT = "stan.samisco@ext.sierra.ai"
SPACE_IDS = {"AAQAkdY0pQg", "AAQAZ0v2SzU"}


def validate_capture(payload):
    if payload.get("account") != ACCOUNT:
        raise ValueError("Google Chat account did not match Sierra.")
    spaces = payload.get("spaces", [])
    if len(spaces) != 2 or {s["space"]["id"] for s in spaces} != SPACE_IDS:
        raise ValueError("Google Chat export must contain exactly the two configured spaces.")
    for space in spaces:
        if space.get("history_complete") is not True or not space.get("threads"):
            raise ValueError("Google Chat returned empty or incomplete history; previous exports were kept.")
        seen = set()
        for thread in space["threads"]:
            messages = thread["messages"]
            ids = [m["id"] for m in messages]
            if (len(ids) != len(set(ids)) or thread["id"] not in ids
                    or len(ids) != thread["reply_count"] + 1
                    or any(m["thread_id"] != thread["id"] for m in messages)
                    or thread["id"] in seen):
                raise ValueError("Google Chat returned an incomplete or duplicate thread.")
            seen.add(thread["id"])


def publish_capture(payload, output_dir=OUTPUT_DIR):
    validate_capture(payload)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "snapshot.json"
    previous = json.loads(target.read_text()) if target.exists() else {"spaces": []}
    old_ids = {(s["space"]["id"], m["id"])
               for s in previous["spaces"] for t in s["threads"] for m in t["messages"]}
    new_ids = {(s["space"]["id"], m["id"])
               for s in payload["spaces"] for t in s["threads"] for m in t["messages"]}
    # Publish only after both spaces have been fully read and validated.
    with tempfile.NamedTemporaryFile(mode="w", dir=output_dir, delete=False) as tmp:
        json.dump(payload, tmp, ensure_ascii=False, indent=2)
        pending = tmp.name
    try:
        os.replace(pending, target)
    finally:
        if os.path.exists(pending):
            os.unlink(pending)
    process_google_chat_workspace(str(output_dir))
    return len(new_ids - old_ids), len(new_ids)


def main():
    executable = shutil.which("playwriter")
    if not executable:
        raise RuntimeError("Playwriter is missing. Install it and enable its extension on Sierra Google Chat.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / ".sync.lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("A Google Chat sync is already running.")
        session_id = None
        try:
            created = subprocess.run([executable, "session", "new"], capture_output=True, text=True, timeout=30)
            match = re.search(r"Session (\d+) created", created.stdout)
            if created.returncode or not match:
                raise RuntimeError("Cannot connect to the browser. Enable Playwriter on Sierra Google Chat.")
            session_id = match.group(1)
            print("Reading Openpay and Cobranza from Google Chat…", flush=True)
            with tempfile.TemporaryDirectory(prefix="capture-", dir=OUTPUT_DIR) as scratch:
                capture_path = Path(scratch) / "capture.json"
                module_path = PROJECT_DIR / "scripts" / "google_chat_browser.mjs"
                # Playwriter's relay survives sessions and caches imported modules.
                module = f"{module_path.as_uri()}?v={module_path.stat().st_mtime_ns}"
                code = (f"const mod = await import({json.dumps(module)}); "
                        f"await mod.capture({{context,outputPath:{json.dumps(str(capture_path))}}});")
                result = subprocess.run(
                    [executable, "-s", session_id, "--timeout", "600000", "-e", code],
                    capture_output=True, text=True, timeout=630,
                )
                if result.returncode or not capture_path.exists():
                    details = result.stdout + result.stderr
                    error = next((line.strip() for line in details.splitlines()
                                  if "Error executing code:" in line), "Browser scrape failed.")
                    raise RuntimeError(error.replace("Error executing code: Error: ", ""))
                payload = json.loads(capture_path.read_text())
                new_count, total = publish_capture(payload)
                print(f"Export complete: Google Chat — {new_count} new messages, {total} total in 2 spaces", flush=True)
        finally:
            if session_id:
                try:
                    subprocess.run([executable, "session", "delete", session_id],
                                   capture_output=True, timeout=15)
                except subprocess.TimeoutExpired:
                    pass


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Google Chat: {error}", file=sys.stderr, flush=True)
        sys.exit(1)
