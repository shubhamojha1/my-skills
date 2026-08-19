#!/usr/bin/env python3

import importlib.util
import unittest
from datetime import datetime, timezone
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("collect_github.py")
SPEC = importlib.util.spec_from_file_location("collect_github", MODULE_PATH)
assert SPEC and SPEC.loader
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


def pr(number, association, merged=False, user_type="User", created="2026-01-01T00:00:00Z"):
    return {
        "number": number,
        "author_association": association,
        "user": {"type": user_type},
        "created_at": created,
        "draft": False,
        "pull_request": {"merged_at": "2026-01-02T00:00:00Z" if merged else None},
    }


class CollectorTests(unittest.TestCase):
    def test_normalizes_supported_repository_inputs(self):
        self.assertEqual(collector.normalize_repo("owner/repo"), "owner/repo")
        self.assertEqual(
            collector.normalize_repo("https://github.com/owner/repo.git"), "owner/repo"
        )
        self.assertEqual(collector.normalize_repo("git@github.com:owner/repo.git"), "owner/repo")

    def test_rejects_non_github_urls(self):
        with self.assertRaises(collector.CollectionError):
            collector.normalize_repo("https://gitlab.com/owner/repo")

    def test_outcomes_exclude_bots_and_unknown_associations(self):
        items = [
            pr(1, "NONE", merged=True),
            pr(2, "FIRST_TIMER", merged=False),
            pr(3, "MEMBER", merged=True),
            pr(4, "MANNEQUIN", merged=False),
            pr(5, "NONE", merged=True, user_type="Bot"),
        ]
        result = collector.closed_outcomes(items)
        self.assertEqual(result["population"]["bots_excluded"], 1)
        self.assertEqual(result["outside_merged"]["numerator"], 1)
        self.assertEqual(result["outside_merged"]["denominator"], 2)
        self.assertEqual(result["unknown_count"], 1)

    def test_open_pr_age_uses_utc(self):
        now = datetime(2026, 4, 15, tzinfo=timezone.utc)
        result = collector.open_pr_metrics([pr(1, "NONE")], now)
        self.assertEqual(result["older_than_30_days"], 1)
        self.assertEqual(result["older_than_90_days"], 1)


if __name__ == "__main__":
    unittest.main()
