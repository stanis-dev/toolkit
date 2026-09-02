#!/usr/bin/env python3
"""Unit tests for export helpers: Teams timestamp normalization and Slack host routing."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from teams_export import _teams_dt
from slack_export import _host_of


class TeamsTimestampTests(unittest.TestCase):
    def test_equal_instant_across_fractional_forms(self):
        # The audit case: "...00Z" and "...00.0000000Z" are the same instant.
        # Lexically "...00Z" > "...00.0000000Z" ('Z' > '.'); chronologically equal.
        self.assertEqual(
            _teams_dt("2025-12-01T00:00:00Z"),
            _teams_dt("2025-12-01T00:00:00.0000000Z"),
        )

    def test_ordering_is_chronological(self):
        self.assertGreater(
            _teams_dt("2025-12-01T00:00:01Z"),
            _teams_dt("2025-12-01T00:00:00.9999999Z"),
        )

    def test_offset_and_zulu_equivalent(self):
        self.assertEqual(
            _teams_dt("2025-12-01T10:00:00+00:00"),
            _teams_dt("2025-12-01T10:00:00Z"),
        )

    def test_junk_and_empty_sort_as_minimum(self):
        floor = _teams_dt("")
        self.assertEqual(floor, _teams_dt("not-a-date"))
        self.assertLess(floor, _teams_dt("2025-12-01T00:00:00Z"))

    def test_max_picks_latest_across_heterogeneous_fields(self):
        msgs = [
            {"composetime": "2025-12-05T09:00:00.1230000Z"},
            {"originalarrivaltime": "2025-12-05T09:00:00Z"},
            {"composetime": "2025-12-05T08:59:59.9999999Z"},
        ]
        latest = max(msgs, key=lambda m: _teams_dt(
            m.get("composetime") or m.get("originalarrivaltime", "")))
        self.assertIs(latest, msgs[0])


class SlackHostTests(unittest.TestCase):
    def test_name_containing_enterprise_is_not_enterprise_host(self):
        host = _host_of("https://enterprise-team.slack.com/")
        self.assertEqual(host, "enterprise-team.slack.com")
        self.assertFalse(host.endswith(".enterprise.slack.com"))

    def test_real_enterprise_host(self):
        self.assertTrue(_host_of("https://acme.enterprise.slack.com/").endswith(".enterprise.slack.com"))

    def test_scheme_less_url_tolerated(self):
        self.assertEqual(_host_of("acme.slack.com"), "acme.slack.com")


if __name__ == "__main__":
    unittest.main()
