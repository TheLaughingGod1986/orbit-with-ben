#!/usr/bin/env python3
"""Listing package readiness + Passed upload/social handoff (Ben, 7 Nov 2026)."""
from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import approved_deliver as ad  # noqa: E402
import listing_package as lp  # noqa: E402

NOW = dt.datetime(2026, 11, 7, 12, 0, tzinfo=dt.timezone.utc)


class ListingPackage(unittest.TestCase):
    def test_missing_fields_and_ready_status(self):
        self.assertEqual(lp.missing_fields(None), ["title", "thumbnail", "description", "tags"])
        incomplete = {"title": "Titan", "tags": ["space"]}
        self.assertEqual(lp.missing_fields(incomplete), ["thumbnail", "description"])
        self.assertEqual(
            lp.status_line(missing=["thumbnail", "description"]),
            "Needs thumbnail, description",
        )
        self.assertEqual(lp.status_line(missing=[], destination="youtube"), "Ready to upload")
        self.assertEqual(lp.status_line(missing=[], destination="social"), "Ready to post")

    def test_schedule_status_never_invents(self):
        self.assertEqual(lp.schedule_status({}), "")
        self.assertEqual(lp.schedule_status({"state": "scheduled"}), "")
        self.assertEqual(
            lp.schedule_status({"state": "scheduled", "publishAtLondon": "Wed 12 Nov 18:00"}),
            "Scheduled for Wed 12 Nov 18:00 London",
        )

    def test_for_video_uses_inline_listing_when_no_manifest(self):
        v = {
            "key": "OWB:032",
            "number": "032",
            "type": "long",
            "lane": "approved",
            "listing": {"missing": ["tags"], "complete": False},
        }
        out = lp.for_video(v, root=Path("/tmp/no-such-owb-root"))
        self.assertEqual(out["status"], "Needs tags")
        self.assertFalse(out["complete"])


class ApprovedDeliver(unittest.TestCase):
    def test_passed_candidates_exclude_scheduled_and_public(self):
        vids = [
            {"key": "a", "lane": "approved", "youtube": None},
            {"key": "b", "lane": "approved", "youtube": {"state": "scheduled", "publishAt": "2026-11-12T18:00:00Z"}},
            {"key": "c", "lane": "approved", "youtube": {"state": "live", "privacy": "public"}},
            {"key": "d", "lane": "ready", "readyFor": "Ben"},
        ]
        self.assertEqual([v["key"] for v in ad.passed_candidates(vids)], ["a"])

    def test_plan_waits_on_incomplete_listing_and_skips_banned_ids(self):
        incomplete = {
            "key": "OWB:032", "lane": "approved", "channel": "OWB", "number": "032", "type": "long",
            "title": "Titan", "version": "v03",
            "listing": {"missing": ["thumbnail"], "complete": False, "status": "Needs thumbnail"},
            "approved": {"job": "J1", "version": "v03"},
        }
        banned = {
            "key": "OWB:033", "lane": "approved", "channel": "OWB", "number": "033", "type": "long",
            "title": "X", "youtube": {"videoId": "TtgHNLXfDSs", "state": "uploaded"},
            "listing": {"missing": [], "complete": True, "destination": "youtube"},
            "approved": {},
        }
        with mock.patch.object(ad.lp, "for_video", side_effect=lambda v, root=None: v.get("listing") or {}):
            actions = ad.plan_actions([incomplete, banned], [], now=NOW, root=Path("."))
        by_key = {a["key"]: a for a in actions}
        self.assertEqual(by_key["OWB:032"]["op"], "wait")
        self.assertIn("thumbnail", by_key["OWB:032"]["reason"])
        self.assertEqual(by_key["OWB:033"]["op"], "skip")
        self.assertIn("Banned reuse", by_key["OWB:033"]["reason"])

    def test_plan_creates_private_upload_with_cadence_slot(self):
        v = {
            "key": "OWB:032", "lane": "approved", "channel": "OWB", "number": "032", "type": "long",
            "title": "Could a Robot Survive on Titan?", "version": "v03",
            "listing": {"missing": [], "complete": True, "destination": "youtube", "title": "Titan"},
            "approved": {"job": "", "version": "v03"},
        }
        with mock.patch.object(ad.lp, "for_video", return_value=v["listing"]):
            actions = ad.plan_actions([v], [], now=NOW, root=Path("."))
        self.assertEqual(len(actions), 1)
        a = actions[0]
        self.assertEqual(a["op"], "create")
        self.assertEqual(a["destination"], "youtube")
        self.assertIn("Private", a["title"])
        self.assertTrue(a["airs"].endswith("Z"))
        # Body names banned ids as do-not-reuse destinations (never as targets).
        self.assertIn("Do not reuse TtgHNLXfDSs or k9pXeeJvLpc", a["body"])
        self.assertNotIn("videoId", a)

    def test_social_hos_mentions_buffer_only_tiktok(self):
        v = {
            "key": "HOS:010:S", "lane": "approved", "channel": "HOS", "number": "010", "type": "short",
            "title": "Herschel Short", "parent": "HOS:010",
            "listing": {"missing": [], "complete": True, "destination": "social"},
            "approved": {"version": "v01"},
        }
        parent = {"key": "HOS:010", "youtube": {"state": "live", "privacy": "public"}}
        with mock.patch.object(ad.lp, "for_video", return_value=v["listing"]):
            actions = ad.plan_actions([v, parent], [], now=NOW, root=Path("."))
        self.assertEqual(actions[0]["op"], "create")
        self.assertEqual(actions[0]["destination"], "social")
        self.assertIn("HOS TikTok stays Buffer-only", actions[0]["body"])

    def test_next_cadence_never_two_shorts_same_day(self):
        taken = {"2026-11-07"}  # Sat
        slot = ad.next_cadence_slot("OWB", "short", now=NOW, taken_days=taken)
        when = dt.datetime.fromisoformat(slot.replace("Z", "+00:00")).astimezone(ad.LONDON)
        self.assertNotEqual(when.date().isoformat(), "2026-11-07")
        self.assertEqual((when.hour, when.minute), (11, 30))


if __name__ == "__main__":
    unittest.main()
