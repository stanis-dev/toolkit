#!/usr/bin/env python3

import json
import os
import sys
import tempfile
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from process_exports import process_slack_workspace, process_teams_workspace
from slack_export import save_channel
from teams_export import save_conversation


class ChatExportTests(unittest.TestCase):
    def test_save_channel_upserts_existing_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "channels"), exist_ok=True)
            path = os.path.join(tmp, "channels", "C1.json")
            with open(path, "w") as f:
                json.dump(
                    {
                        "channel": {"id": "C1", "name": "alerts"},
                        "messages": [{"ts": "1.000000", "text": "old"}],
                    },
                    f,
                )

            new_count = save_channel(
                tmp,
                {"id": "C1", "name": "alerts"},
                [{"ts": "1.000000", "text": "new"}],
            )

            self.assertEqual(new_count, 0)
            with open(path) as f:
                payload = json.load(f)
            self.assertEqual(payload["messages"][0]["text"], "new")

    def test_process_slack_workspace_targets_single_channel(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "channels"), exist_ok=True)
            os.makedirs(os.path.join(tmp, "readable"), exist_ok=True)
            with open(os.path.join(tmp, "users.json"), "w") as f:
                json.dump({}, f)
            with open(os.path.join(tmp, "channels", "C1.json"), "w") as f:
                json.dump(
                    {
                        "channel": {"id": "C1", "name": "alerts"},
                        "messages": [{"ts": "1.000000", "text": "hello", "user": "U1"}],
                    },
                    f,
                )
            with open(os.path.join(tmp, "channels", "C2.json"), "w") as f:
                json.dump(
                    {
                        "channel": {"id": "C2", "name": "random"},
                        "messages": [{"ts": "2.000000", "text": "skip", "user": "U2"}],
                    },
                    f,
                )
            keep_path = os.path.join(tmp, "readable", "keep.md")
            with open(keep_path, "w") as f:
                f.write("keep")

            written = process_slack_workspace(tmp, channel_ids=["C1"], clean=False)

            self.assertEqual(written, 1)
            self.assertTrue(os.path.exists(os.path.join(tmp, "readable", "slack_C1.md")))
            self.assertFalse(os.path.exists(os.path.join(tmp, "readable", "slack_C2.md")))
            self.assertTrue(os.path.exists(keep_path))

    def test_save_conversation_upserts_existing_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "chats"), exist_ok=True)
            meta = {"id": "19:chat"}
            save_conversation(
                tmp,
                "chats",
                meta,
                [{"id": "m1", "content": "old", "composetime": "2026-01-01T00:00:00Z"}],
            )
            new_count = save_conversation(
                tmp,
                "chats",
                meta,
                [{"id": "m1", "content": "new", "composetime": "2026-01-01T00:00:00Z"}],
            )
            self.assertEqual(new_count, 0)
            out_path = os.path.join(tmp, "chats", "19_chat.json")
            with open(out_path) as f:
                payload = json.load(f)
            self.assertEqual(payload["messages"][0]["content"], "new")

    def test_process_teams_workspace_targets_specific_conversation(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "chats"), exist_ok=True)
            os.makedirs(os.path.join(tmp, "channels"), exist_ok=True)
            os.makedirs(os.path.join(tmp, "readable"), exist_ok=True)

            with open(os.path.join(tmp, "chats", "chat.json"), "w") as f:
                json.dump(
                    {
                        "meta": {"id": "19:chat", "topic": "Alpha"},
                        "messages": [{"id": "m1", "content": "<p>Hello</p>", "composetime": "2026-01-01T00:00:00Z"}],
                    },
                    f,
                )
            with open(os.path.join(tmp, "channels", "channel.json"), "w") as f:
                json.dump(
                    {
                        "meta": {"id": "19:channel", "team_name": "Team", "channel_name": "General"},
                        "messages": [{"id": "m2", "content": "<p>World</p>", "composetime": "2026-01-01T00:00:00Z"}],
                    },
                    f,
                )

            written = process_teams_workspace(tmp, conversations=[("chats", "19:chat")], clean=False)

            self.assertEqual(written, 1)
            self.assertTrue(os.path.exists(os.path.join(tmp, "readable", "teams_chat_19_chat.md")))
            self.assertFalse(os.path.exists(os.path.join(tmp, "readable", "teams_channel_19_channel.md")))


    def test_slack_reactions_rendered_in_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "channels"), exist_ok=True)
            users = {
                "U1": {"name": "seb", "real_name": "Seb Tranaeus", "display_name": "seb"},
                "U2": {"name": "stan", "real_name": "Stan Samisco", "display_name": "stan"},
                "U3": {"name": "andrew", "real_name": "Andrew Granoff", "display_name": "andrew"},
            }
            with open(os.path.join(tmp, "users.json"), "w") as f:
                json.dump(users, f)

            messages = [
                {
                    "ts": "1000.000000",
                    "user": "U1",
                    "text": "Thanks for pushing out meaningful changes this week!",
                    "reactions": [
                        {"name": "sierra-heart", "users": ["U1"], "count": 1},
                    ],
                },
                {
                    "ts": "2000.000000",
                    "user": "U2",
                    "text": "I think we should enable predictive keywords.",
                    "reactions": [
                        {"name": "thumbsup", "users": ["U2", "U3"], "count": 2},
                        {"name": "white_check_mark", "users": ["U1"], "count": 1},
                    ],
                },
                {
                    "ts": "3000.000000",
                    "thread_ts": "3000.000000",
                    "user": "U2",
                    "text": "Can you handle the deploy?",
                    "reply_count": 1,
                    "replies_full": [
                        {
                            "ts": "3001.000000",
                            "thread_ts": "3000.000000",
                            "user": "U3",
                            "text": "On it",
                            "reactions": [
                                {"name": "white_check_mark", "users": ["U2"], "count": 1},
                            ],
                        },
                    ],
                },
                {
                    "ts": "4000.000000",
                    "user": "U3",
                    "text": "No reactions here",
                },
            ]

            with open(os.path.join(tmp, "channels", "C1.json"), "w") as f:
                json.dump({"channel": {"id": "C1", "name": "working-team"}, "messages": messages}, f)

            process_slack_workspace(tmp, channel_ids=["C1"], clean=False)
            with open(os.path.join(tmp, "readable", "slack_C1.md")) as f:
                md = f.read()

            self.assertIn("[reactions: :sierra-heart: Seb Tranaeus]", md)
            self.assertIn("[reactions: :thumbsup: Stan Samisco, Andrew Granoff \u00b7 :white_check_mark: Seb Tranaeus]", md)
            self.assertIn("  > [reactions: :white_check_mark: Stan Samisco]", md)
            no_reaction_line = [l for l in md.splitlines() if "No reactions here" in l]
            self.assertTrue(no_reaction_line)
            idx = md.splitlines().index(no_reaction_line[0])
            next_line = md.splitlines()[idx + 1] if idx + 1 < len(md.splitlines()) else ""
            self.assertNotIn("[reactions:", next_line)

    def test_slack_reactions_unknown_user_falls_back_to_uid(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "channels"), exist_ok=True)
            with open(os.path.join(tmp, "users.json"), "w") as f:
                json.dump({"U1": {"name": "stan", "real_name": "Stan", "display_name": ""}}, f)

            messages = [
                {
                    "ts": "1000.000000",
                    "user": "U1",
                    "text": "bot reacted",
                    "reactions": [
                        {"name": "robot_face", "users": ["U1", "UBOT999"], "count": 2},
                    ],
                },
            ]
            with open(os.path.join(tmp, "channels", "C1.json"), "w") as f:
                json.dump({"channel": {"id": "C1", "name": "test"}, "messages": messages}, f)

            process_slack_workspace(tmp, channel_ids=["C1"], clean=False)
            with open(os.path.join(tmp, "readable", "slack_C1.md")) as f:
                md = f.read()

            self.assertIn("[reactions: :robot_face: Stan, UBOT999]", md)


if __name__ == "__main__":
    unittest.main()
