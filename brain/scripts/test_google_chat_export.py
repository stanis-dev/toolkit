import copy
import json
from pathlib import Path
import tempfile
import unittest

from google_chat_export import ACCOUNT, SPACE_IDS, publish_capture


def capture():
    spaces = []
    for space_id in sorted(SPACE_IDS):
        messages = [{"id": "root", "thread_id": "root", "sender": {"name": "Stan"},
                     "create_time_usec": "1789000000000000", "update_time_usec": "1789000000000000",
                     "text": "Hola", "reactions": []},
                    {"id": "reply", "thread_id": "root", "sender": {"name": "Colleague"},
                     "create_time_usec": "1789000001000000", "update_time_usec": "1789000001000000",
                     "text": "Gracias", "reactions": [{"emoji": "🙌", "count": 1}]}]
        spaces.append({"space": {"id": space_id, "name": "Voicebot"}, "history_complete": True,
                       "threads": [{"id": "root", "reply_count": 1, "messages": messages}]})
    return {"account": ACCOUNT, "captured_at": "2026-09-15T10:00:00Z", "spaces": spaces}


class GoogleChatExportTests(unittest.TestCase):
    def test_repeated_sync_updates_edits_and_removes_deleted_reply_without_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = capture()
            self.assertEqual(publish_capture(payload, tmp), (4, 4))
            self.assertEqual(publish_capture(payload, tmp), (0, 4))
            thread = payload["spaces"][0]["threads"][0]
            thread["messages"][0]["text"] = "Corrected"
            thread["messages"] = thread["messages"][:1]
            thread["reply_count"] = 0
            self.assertEqual(publish_capture(payload, tmp), (0, 3))
            stored = json.loads((Path(tmp) / "snapshot.json").read_text())
            self.assertEqual(stored["spaces"][0]["threads"][0]["messages"][0]["text"], "Corrected")
            md = (Path(tmp) / "readable" / f"google_chat_{payload['spaces'][1]['space']['id']}.md").read_text()
            self.assertIn("Colleague (Reply)", md)
            self.assertIn("🙌 ×1", md)

    def test_invalid_capture_never_overwrites_previous_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = capture()
            publish_capture(payload, tmp)
            original = (Path(tmp) / "snapshot.json").read_bytes()
            for mutation in ["account", "space", "incomplete", "empty", "missing_reply"]:
                bad = copy.deepcopy(payload)
                if mutation == "account": bad["account"] = "other@example.com"
                elif mutation == "space": bad["spaces"][0]["space"]["id"] = "other"
                elif mutation == "incomplete": bad["spaces"][0]["history_complete"] = False
                elif mutation == "empty": bad["spaces"][0]["threads"] = []
                else: bad["spaces"][0]["threads"][0]["messages"].pop()
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    publish_capture(bad, tmp)
                self.assertEqual((Path(tmp) / "snapshot.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
