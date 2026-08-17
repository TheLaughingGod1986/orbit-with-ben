#!/usr/bin/env python3
"""Ledger must treat already-synced shorts as posted so CDP does not retry them."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

AUTO = Path(__file__).resolve().parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

import ledger  # noqa: E402


class PostedStatusTests(unittest.TestCase):
    def test_posted_status_is_terminal(self):
        short = {"video_id": "1HuV8o3gOss"}
        data = {
            "posted": {
                "yt:1HuV8o3gOss": {
                    "instagram": {"status": "posted"},
                    "facebook": {"status": "posted"},
                }
            }
        }
        with patch.object(ledger, "load", return_value=data):
            self.assertTrue(ledger.is_posted(short))
            self.assertTrue(ledger.is_posted(short, platform="instagram"))
            self.assertTrue(ledger.is_posted(short, platform="facebook"))

    def test_unconfirmed_is_not_terminal(self):
        short = {"video_id": "abc"}
        data = {
            "posted": {
                "yt:abc": {
                    "instagram": {"status": "unconfirmed"},
                    "facebook": {"status": "unconfirmed"},
                }
            }
        }
        with patch.object(ledger, "load", return_value=data):
            self.assertFalse(ledger.is_posted(short))


if __name__ == "__main__":
    unittest.main()
