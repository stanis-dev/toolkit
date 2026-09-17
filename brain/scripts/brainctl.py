#!/usr/bin/env python3
"""Control the running Brain app. Commands and errors return JSON."""
import argparse
import json
import math
from pathlib import Path
import socket
import subprocess
import sys
import time

SOCKET_PATH = "/Users/stan/Library/Application Support/Brain/control.sock"
MAXIMUM_REQUEST_BYTES = 256 * 1024


class BrainUnavailable(ConnectionError):
    pass


def send_request(request, path=SOCKET_PATH):
    payload = json.dumps(request, ensure_ascii=False).encode() + b"\n"
    if len(payload) - 1 > MAXIMUM_REQUEST_BYTES:
        raise ValueError("Request exceeds 256 KiB.")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(10)
        try:
            connection.connect(path)
        except (FileNotFoundError, ConnectionRefusedError) as error:
            raise BrainUnavailable("Brain control socket is unavailable.") from error
        connection.sendall(payload)
        response = bytearray()
        while b"\n" not in response:
            chunk = connection.recv(65536)
            if not chunk:
                raise ConnectionError("Brain closed the connection without a response.")
            response.extend(chunk)
            if len(response) > 16 * 1024 * 1024:
                raise ValueError("Brain response exceeds 16 MiB.")
    decoded = json.loads(response.split(b"\n", 1)[0])
    if not isinstance(decoded, dict) or not isinstance(decoded.get("ok"), bool):
        raise ValueError("Brain returned an invalid response.")
    return decoded


def wait_for_job(response, timeout, request=send_request):
    if not response["ok"]:
        return response
    job = response["result"]
    deadline = time.monotonic() + timeout
    while job["state"] == "running":
        if time.monotonic() >= deadline:
            return {"ok": False, "error": {"code": "timeout", "message": "Job is still running.", "job_id": job["id"]}}
        time.sleep(0.5)
        response = request({"command": "job", "id": job["id"]})
        if not response["ok"]:
            return response
        job = response["result"]
    return response


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Read app state, sync progress and results.")
    sub.add_parser("launch", help="Start Brain in the background and wait until it is ready.")
    platforms = ["slack", "teams", "google-chat"]
    sync = sub.add_parser("sync", help="Start a chat export through the app.")
    sync.add_argument("platform", choices=platforms)
    job = sub.add_parser("job", help="Read the outcome of a sync job.")
    job.add_argument("id")
    for command in (sync, job):
        command.add_argument("--wait", action="store_true", help="Wait for completion; failed jobs exit nonzero.")
        command.add_argument("--timeout", type=float, default=660, help="Maximum wait in seconds (default: 660).")
    auto = sub.add_parser("auto", help="Enable or disable automatic chat refresh.")
    auto.add_argument("platform", choices=platforms)
    auto.add_argument("enabled", choices=["on", "off"])
    recording = sub.add_parser("recording", help="Control meeting recording.")
    recording.add_argument("action", choices=["start", "stop", "pause", "resume"])
    sub.add_parser("recordings", help="List recordings, their IDs and transcription status.")
    transcribe = sub.add_parser("transcribe", help="Start transcription; poll recordings for status.")
    transcribe.add_argument("id")
    dictation = sub.add_parser("dictation", help="Control dictation. Finishing copies text to the clipboard.")
    dictation.add_argument("action", choices=["start", "finish", "cancel"])
    dictation.add_argument("--paste", action="store_true", help="Also paste the result when finishing.")
    todo = sub.add_parser("todo", help="Read, replace or append to the TODO document.")
    todo.add_argument("action", choices=["get", "set", "append"])
    todo.add_argument("--file", type=Path, help="Read text from this file; otherwise pipe text on stdin.")
    navigate = sub.add_parser("navigate", help="Show an app tab or hide the window.")
    navigate.add_argument("tab", choices=["assistant", "recorder", "dictator", "macos", "settings", "logs", "hide"])
    return cli


def main():
    cli = parser()
    args = cli.parse_args()
    if not math.isfinite(getattr(args, "timeout", 1)) or getattr(args, "timeout", 1) <= 0:
        cli.error("--timeout must be a finite positive number")
    if getattr(args, "paste", False) and args.action != "finish":
        cli.error("--paste is only valid with dictation finish")
    request = {key: value for key, value in vars(args).items() if key not in ("wait", "timeout", "file")}
    try:
        if args.command == "launch":
            subprocess.run(["/usr/bin/open", "-gj", "/Applications/Brain.app"], check=True, capture_output=True)
            deadline = time.monotonic() + 15
            while True:
                try:
                    response = send_request({"command": "status"})
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError("Brain started but its control socket did not become available.")
                    time.sleep(0.25)
        else:
            if args.command == "auto":
                request["enabled"] = args.enabled == "on"
            if args.command == "todo":
                if args.action == "get" and args.file:
                    cli.error("--file is only valid with todo set or append")
                if args.action != "get":
                    if not args.file and sys.stdin.isatty():
                        cli.error("provide --file or pipe the TODO text on stdin")
                    request["text"] = args.file.read_text() if args.file else sys.stdin.read()
            response = send_request(request)
            if getattr(args, "wait", False):
                response = wait_for_job(response, args.timeout)
    except BrainUnavailable:
        response = {"ok": False, "error": {"code": "unavailable", "message": "Brain is not running or control is unavailable. Run brainctl launch."}}
    except Exception as error:
        response = {"ok": False, "error": {"code": "client_error", "message": str(error)}}
    print(json.dumps(response, ensure_ascii=False, indent=2))
    return 0 if response["ok"] and response.get("result", {}).get("state") != "failed" else 1


if __name__ == "__main__":
    sys.exit(main())
