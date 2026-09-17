import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

from brainctl import BrainUnavailable, send_request, wait_for_job


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="brain-control-")
        self.path = str(Path(self.tmp.name) / "control.sock")
        self.host = os.environ["BRAIN_CONTROL_TEST_HOST"]
        self.process = None

    def start(self):
        self.process = subprocess.Popen([self.host, self.path], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                self.fail(self.process.stderr.read().decode())
            try:
                if send_request({"command": "echo"}, self.path)["ok"]:
                    return
            except (OSError, ValueError):
                time.sleep(0.02)
        self.fail("Test control server did not become ready")

    def tearDown(self):
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
            self.process.stderr.close()
        self.tmp.cleanup()

    def test_roundtrip_fragmented_unicode_and_private_permissions(self):
        self.start()
        self.assertEqual(stat.S_IMODE(os.stat(self.path).st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(os.stat(self.tmp.name).st_mode), 0o700)
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(5)
            client.connect(self.path)
            payload = json.dumps({"command": "echo", "text": "Álvaro 🙌"}, ensure_ascii=False).encode() + b"\n"
            client.sendall(payload[:17])
            client.sendall(payload[17:])
            response = json.loads(client.makefile("rb").readline())
        self.assertEqual(response["result"]["text"], "Álvaro 🙌")

    def test_malformed_requests_and_disconnected_clients_do_not_kill_server(self):
        self.start()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(5)
            client.connect(self.path)
            client.sendall(b"not json\n")
            response = json.loads(client.makefile("rb").readline())
        self.assertEqual(response["error"]["code"], "invalid_request")
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(self.path)
            client.sendall(b'{"command":"echo"}\n')
        try:
            self.assertTrue(send_request({"command": "echo"}, self.path)["ok"])
        except Exception as error:
            code = self.process.poll()
            if code is None:
                try:
                    code = self.process.wait(timeout=0.2)
                except subprocess.TimeoutExpired:
                    self.process.terminate()
                    self.process.wait(timeout=5)
            details = self.process.stderr.read().decode()
            self.fail(f"{error}; server exit={code}; {details}")

    def test_oversized_input_is_rejected_before_connecting(self):
        with self.assertRaisesRegex(ValueError, "256 KiB"):
            send_request({"command": "echo", "text": "x" * (256 * 1024)}, self.path)

    def test_stale_socket_is_recovered(self):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as stale:
            stale.bind(self.path)
        self.start()
        self.assertTrue(send_request({"command": "echo"}, self.path)["ok"])

    def test_live_socket_and_regular_files_are_never_replaced(self):
        self.start()
        second = subprocess.run([self.host, self.path], capture_output=True, timeout=5)
        self.assertNotEqual(second.returncode, 0)
        self.assertTrue(send_request({"command": "echo"}, self.path)["ok"])
        other = str(Path(self.tmp.name) / "important.txt")
        Path(other).write_text("keep")
        third = subprocess.run([self.host, other], capture_output=True, timeout=5)
        self.assertNotEqual(third.returncode, 0)
        self.assertEqual(Path(other).read_text(), "keep")

    def test_absent_app_is_reported(self):
        with self.assertRaises(BrainUnavailable):
            send_request({"command": "status"}, self.path)

    def test_wait_surfaces_failed_job_and_retains_id_on_timeout(self):
        running = {"ok": True, "result": {"id": "job1", "state": "running"}}
        failed = {"ok": True, "result": {"id": "job1", "state": "failed", "result": {"summary": "Export failed"}}}
        with patch("brainctl.time.sleep"):
            self.assertEqual(wait_for_job(running, 5, request=lambda _: failed), failed)
        timeout = wait_for_job(running, 0)
        self.assertFalse(timeout["ok"])
        self.assertEqual(timeout["error"]["job_id"], "job1")


if __name__ == "__main__":
    unittest.main()
