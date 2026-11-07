#!/usr/bin/env python3
"""Listing package readiness + Passed upload/social handoff (Ben, 7 Nov 2026).

Safety: empty UPLOADS stubs must not allow a second Studio upload or a double-booked cadence day.
"""
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

NOW = dt.datetime(2026, 11, 7, 12, 0, tzinfo=dt.timezone.utc)  # Sat 12:00 UTC → Sat midday London


def ready_listing(**over):
    base = {"missing": [], "complete": True, "destination": "youtube", "status": "Ready to upload", "title": "Titan"}
    base.update(over)
    return base


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

    def test_short_with_two_packages_does_not_use_long_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            film = root / "02_Video-Projects" / "032_Titan"
            long_pkg = film / "11_Upload-Package"
            long_pkg.mkdir(parents=True)
            (long_pkg / "PACKAGE_MANIFEST.json").write_text(json.dumps({
                "title": "Long title", "thumbnail": "t.jpg", "description": "d", "tags": ["a"],
            }))
            for name in ("A", "B"):
                sp = film / "10_Shorts" / name / "11_Upload-Package"
                sp.mkdir(parents=True)
                (sp / "PACKAGE_MANIFEST.json").write_text(json.dumps({
                    "title": f"Short {name}", "thumbnail": "t.jpg", "description": "d", "tags": ["a"],
                }))
            self.assertIsNone(lp.find_manifest(root, number="032", vtype="short"))
            # Without packageDir, for_video must not become complete via the long manifest.
            out = lp.for_video({"number": "032", "type": "short", "youtube": {}}, root=root)
            self.assertFalse(out["complete"])
            self.assertIn("title", out["missing"])

    def test_short_with_one_package_uses_that_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            film = root / "02_Video-Projects" / "032_Titan"
            sp = film / "10_Shorts" / "Only" / "11_Upload-Package"
            sp.mkdir(parents=True)
            (sp / "PACKAGE_MANIFEST.json").write_text(json.dumps({
                "title": "Only Short", "thumbnail": "t.jpg", "description": "d", "tags": ["a"],
            }))
            # thumbnail path missing on disk → still incomplete on file check; title present proves right file.
            hit = lp.find_manifest(root, number="032", vtype="short")
            self.assertEqual(hit, sp / "PACKAGE_MANIFEST.json")


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
            "listing": ready_listing(),
            "approved": {},
        }
        empty = Path(tempfile.mkdtemp())
        with mock.patch.object(ad.lp, "for_video", side_effect=lambda v, root=None: v.get("listing") or {}):
            actions = ad.plan_actions([incomplete, banned], [], now=NOW, root=empty)
        by_key = {a["key"]: a for a in actions}
        self.assertEqual(by_key["OWB:032"]["op"], "wait")
        self.assertIn("thumbnail", by_key["OWB:032"]["reason"])
        self.assertEqual(by_key["OWB:033"]["op"], "skip")
        self.assertIn("Banned reuse", by_key["OWB:033"]["reason"])

    def test_plan_creates_private_upload_with_cadence_slot(self):
        v = {
            "key": "OWB:032", "lane": "approved", "channel": "OWB", "number": "032", "type": "long",
            "title": "Could a Robot Survive on Titan?", "version": "v03",
            "listing": ready_listing(),
            "approved": {"job": "", "version": "v03"},
        }
        empty = Path(tempfile.mkdtemp())
        with mock.patch.object(ad.lp, "for_video", return_value=v["listing"]):
            actions = ad.plan_actions([v], [], now=NOW, root=empty)
        self.assertEqual(len(actions), 1)
        a = actions[0]
        self.assertEqual(a["op"], "create")
        self.assertEqual(a["destination"], "youtube")
        self.assertIn("Private", a["title"])
        self.assertTrue(a["airs"].endswith("Z"))
        self.assertIn("Do not reuse TtgHNLXfDSs or k9pXeeJvLpc", a["body"])
        self.assertNotIn("videoId", a)

    def test_social_hos_mentions_buffer_only_tiktok(self):
        v = {
            "key": "HOS:010:S", "lane": "approved", "channel": "HOS", "number": "010", "type": "short",
            "title": "Herschel Short", "parent": "HOS:010",
            "listing": ready_listing(destination="social", status="Ready to post"),
            "approved": {"version": "v01"},
        }
        parent = {"key": "HOS:010", "youtube": {"state": "live", "privacy": "public"}}
        empty = Path(tempfile.mkdtemp())
        with mock.patch.object(ad.lp, "for_video", return_value=v["listing"]):
            actions = ad.plan_actions([v, parent], [], now=NOW, root=empty)
        self.assertEqual(actions[0]["op"], "create")
        self.assertEqual(actions[0]["destination"], "social")
        self.assertIn("HOS TikTok stays Buffer-only", actions[0]["body"])

    def test_next_cadence_never_two_shorts_same_day(self):
        taken = {"2026-11-07"}  # Sat
        slot = ad.next_cadence_slot("OWB", "short", now=NOW, taken_days=taken)
        when = dt.datetime.fromisoformat(slot.replace("Z", "+00:00")).astimezone(ad.LONDON)
        self.assertNotEqual(when.date().isoformat(), "2026-11-07")
        self.assertEqual((when.hour, when.minute), (11, 30))

    def test_already_scheduled_sibling_skips_second_upload(self):
        """OK card with no youtube must not create an upload when the film card is already scheduled."""
        ok = {
            "key": "OWB:OK:J9", "lane": "approved", "channel": "OWB", "number": "032", "type": "long",
            "title": "Titan", "version": "v03", "youtube": None,
            "listing": ready_listing(), "approved": {"job": "", "version": "v03"},
        }
        scheduled = {
            "key": "OWB:032", "lane": "done", "channel": "OWB", "number": "032", "type": "long",
            "youtube": {"videoId": "abcdefghijk", "state": "scheduled",
                        "publishAt": "2026-11-08T18:00:00Z", "privacy": "private"},
        }
        empty = Path(tempfile.mkdtemp())
        with mock.patch.object(ad.lp, "for_video", return_value=ok["listing"]):
            actions = ad.plan_actions([ok, scheduled], [], now=NOW, root=empty)
        self.assertEqual(actions, [{"op": "skip", "key": "OWB:OK:J9",
                                    "reason": "Already on YouTube as OWB:032"}])

    def test_already_public_sibling_skips_second_upload(self):
        ok = {
            "key": "OWB:OK:J9", "lane": "approved", "channel": "OWB", "number": "031", "type": "long",
            "title": "Mag", "version": "v02", "youtube": None,
            "listing": ready_listing(), "approved": {},
        }
        live = {
            "key": "OWB:031", "lane": "done", "channel": "OWB", "number": "031", "type": "long",
            "youtube": {"videoId": "bcdefghijkl", "state": "live", "privacy": "public",
                        "publishAt": "2026-11-01T18:00:00Z"},
        }
        empty = Path(tempfile.mkdtemp())
        with mock.patch.object(ad.lp, "for_video", return_value=ok["listing"]):
            actions = ad.plan_actions([ok, live], [], now=NOW, root=empty)
        self.assertEqual(actions[0]["op"], "skip")
        self.assertIn("Already on YouTube", actions[0]["reason"])

    def test_two_shorts_do_not_land_on_same_channel_day(self):
        """Once an existing Short occupies Mon 11:30, a new Passed Short takes the next free day."""
        existing = {
            "key": "OWB:030:S:oldshort01", "channel": "OWB", "number": "030", "type": "short",
            "lane": "done",
            "youtube": {"videoId": "oldshort01x", "state": "scheduled",
                        "publishAt": "2026-11-09T11:30:00Z", "privacy": "private"},  # Mon
        }
        a = {
            "key": "OWB:OK:JA", "lane": "approved", "channel": "OWB", "number": "032", "type": "short",
            "title": "A", "listing": ready_listing(), "approved": {"version": "v01"},
        }
        b = {
            "key": "OWB:OK:JB", "lane": "approved", "channel": "OWB", "number": "033", "type": "short",
            "title": "B", "listing": ready_listing(), "approved": {"version": "v01"},
        }
        empty = Path(tempfile.mkdtemp())
        with mock.patch.object(ad.lp, "for_video", side_effect=lambda v, root=None: v.get("listing") or ready_listing()):
            actions = ad.plan_actions([existing, a, b], [], now=NOW, root=empty)
        creates = [x for x in actions if x["op"] == "create"]
        self.assertEqual(len(creates), 2)
        days = []
        for c in creates:
            when = dt.datetime.fromisoformat(c["airs"].replace("Z", "+00:00")).astimezone(ad.LONDON)
            days.append(when.date().isoformat())
            self.assertEqual((when.hour, when.minute), (11, 30))
        self.assertNotIn("2026-11-09", days)
        self.assertEqual(len(set(days)), 2, "the two new Shorts must not share a London day")

    def test_long_skips_day_that_already_has_a_long(self):
        """Sunday 18:00 already booked → next free long slot (Wed), never invent an id."""
        existing = {
            "key": "OWB:030", "channel": "OWB", "number": "030", "type": "long", "lane": "done",
            "youtube": {"videoId": "longbooked1", "state": "scheduled",
                        "publishAt": "2026-11-08T18:00:00Z", "privacy": "private"},  # Sun
        }
        passed = {
            "key": "OWB:OK:J9", "lane": "approved", "channel": "OWB", "number": "032", "type": "long",
            "title": "Titan", "listing": ready_listing(), "approved": {"version": "v03"},
        }
        empty = Path(tempfile.mkdtemp())
        with mock.patch.object(ad.lp, "for_video", return_value=passed["listing"]):
            actions = ad.plan_actions([existing, passed], [], now=NOW, root=empty)
        self.assertEqual(actions[0]["op"], "create")
        when = dt.datetime.fromisoformat(actions[0]["airs"].replace("Z", "+00:00")).astimezone(ad.LONDON)
        self.assertNotEqual(when.date().isoformat(), "2026-11-08")
        self.assertEqual((when.weekday(), when.hour, when.minute), (2, 18, 0))  # Wed

    def test_uploads_json_blocks_short_day_even_without_tracker_card(self):
        """Cadence must read UPLOADS.json so empty video stubs cannot hide a booked Short day."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            up = root / "00_Brand" / "Channel-Setup" / "social"
            up.mkdir(parents=True)
            (up / "UPLOADS.json").write_text(json.dumps({"videos": {
                "alreadyshort1": {
                    "kind": "short", "film": "028", "channel": "OWB",
                    "packageDir": "02_Video-Projects/028_X/10_Shorts/A",
                    "publishAt": "2026-11-09T11:30:00Z", "privacyStatus": "private",
                },
            }}))
            taken = ad.taken_cadence_days([], "OWB", "short", NOW.astimezone(ad.LONDON).date(), root=root)
            self.assertIn("2026-11-09", taken)
            slot = ad.next_cadence_slot("OWB", "short", now=NOW, taken_days=taken)
            when = dt.datetime.fromisoformat(slot.replace("Z", "+00:00")).astimezone(ad.LONDON)
            self.assertNotEqual(when.date().isoformat(), "2026-11-09")

    def test_load_delivery_videos_uses_uploads_not_empty_stub(self):
        """run()/load_delivery_videos must not pass uploads={} — scheduled films stay visible."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "jobs").mkdir()
            (root / "jobs" / "queue.json").write_text(json.dumps({"next_id": 1, "jobs": []}))
            (root / "02_Video-Projects" / "032_Titan").mkdir(parents=True)
            (root / "02_Video-Projects" / "032_Titan" / "status.json").write_text(json.dumps({
                "film": "032", "title": "Titan", "air": "2026-11-08",
            }))
            up = root / "00_Brand" / "Channel-Setup" / "social"
            up.mkdir(parents=True)
            (up / "UPLOADS.json").write_text(json.dumps({"videos": {
                "schedlong001": {
                    "kind": "long", "film": "032",
                    "packageDir": "02_Video-Projects/032_Titan/11_Upload-Package",
                    "file": "02_Video-Projects/032_Titan/11_Upload-Package/cut.mp4",
                    "publishAt": "2026-11-08T18:00:00Z", "privacyStatus": "private",
                },
            }}))
            (root / "05_Analytics" / "kanban").mkdir(parents=True)
            (root / "05_Analytics" / "kanban" / "film_briefs.json").write_text(json.dumps({"films": {}}))
            # No public dashboard file → public_index empty; UPLOADS still attaches scheduled state.
            videos = ad.load_delivery_videos(root, [], now=NOW)
            by_key = {v["key"]: v for v in videos}
            self.assertIn("OWB:032", by_key)
            yt = by_key["OWB:032"].get("youtube") or {}
            self.assertEqual(yt.get("videoId"), "schedlong001")
            self.assertEqual(yt.get("state"), "scheduled")
            # An approved OK twin must not create another upload once UPLOADS is loaded into the plan.
            ok = {
                "key": "OWB:OK:J9", "lane": "approved", "channel": "OWB", "number": "032", "type": "long",
                "title": "Titan", "listing": ready_listing(), "approved": {},
            }
            with mock.patch.object(ad.lp, "for_video", return_value=ok["listing"]):
                actions = ad.plan_actions([ok] + videos, [], now=NOW, root=root)
            self.assertTrue(actions and actions[0]["op"] == "skip")
            self.assertIn("Already on YouTube", actions[0]["reason"])

    def test_airs_on_taken_day_falls_through_to_next_free_slot(self):
        taken = {"2026-11-08"}  # preferred airs day (Sun) already has a long
        slot = ad.next_cadence_slot(
            "OWB", "long", now=NOW, taken_days=taken, airs="2026-11-08T18:00Z",
        )
        when = dt.datetime.fromisoformat(slot.replace("Z", "+00:00")).astimezone(ad.LONDON)
        self.assertNotEqual(when.date().isoformat(), "2026-11-08")


if __name__ == "__main__":
    unittest.main()
