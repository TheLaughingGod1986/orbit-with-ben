#!/usr/bin/env python3
"""A film already on YouTube with a job claimed or open shows in In progress (Ben, 26 Oct 2026 00:15: "Can't see these
jobs in the in progress lane"), says what is being done, and goes back to Done when the jobs finish. Blocked jobs (a
date, an input or an OK) never pull it back (HOS 005, #281). Jobs that name only a video id still find their card."""
from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board_check  # noqa: E402
import video_tracker as vt  # noqa: E402

NOW = dt.datetime(2026, 10, 26, 0, 15, tzinfo=dt.timezone.utc)
SUN = {"h8HGfyShEHI": {"channel": "OWB", "title": "Is the Sun Getting Brighter?", "format": "long",
                       "publishedAt": "2026-10-18T17:00:37Z"}}
OWB = [{"film": "022", "title": "Is the Sun Getting Brighter?"},
       {"film": "023", "title": "What Happened to Venus?",
        "release": {"videoId": "VBaYRPp85Sw", "state": "scheduled", "publishAt": "2026-10-25T18:00:00.000Z"}},
       {"film": "028", "title": "What Happens When a Star Passes Through",
        "release": {"videoId": "F-jImX5h7ws", "state": "scheduled", "publishAt": "2026-11-29T18:00:00.000Z"}}]


def job(jid, status, title, **kw):
    return {"id": jid, "status": status, "title": title, "body": "", "by": kw.pop("by", ""), "history": [], **kw}


def build(jobs):
    return {v["key"]: v for v in vt.build_videos(
        hos={"films": []}, owb=OWB, briefs={}, jobs=jobs, checks={}, uploads={}, overrides={}, now=NOW,
        public=SUN, titles={}, alljobs=jobs)["videos"]}


class ProgressWhileJobsOpen(unittest.TestCase):
    def test_claimed_and_open_jobs_put_live_and_scheduled_films_in_progress(self):
        cards = build([
            job("J0962", "claimed", "Venus VBaYRPp85Sw: arm thumbnail-only Test & Compare A (live MELTS LEAD) vs B "
                "EARTH'S TWIN, read back, ledger", by="cursor"),
            job("J0963", "open", "022 Sun h8HGfyShEHI: Test & Compare B v02 '10% BRIGHTER' (fix of J0908 B), park for Chief"),
            job("J0964", "open", "028 Oort marbles Short v02: end card without YouTube id, free slot, park for Chief"),
        ])
        v23, v22, v28 = cards["OWB:023"], cards["OWB:022"], cards["OWB:028"]
        self.assertEqual([v["lane"] for v in (v22, v23, v28)], ["progress"] * 3)
        self.assertEqual(v23["line"], "Live on YouTube · now: arm thumbnail-only Test & Compare A vs B EARTH'S TWIN (cursor).")
        self.assertEqual(v23["waitingOn"], "cursor")
        self.assertEqual(v22["line"], "Live on YouTube · next: Test & Compare B v02 '10% BRIGHTER'.")
        self.assertTrue(v28["line"].startswith("Private, scheduled Sun 29 Nov 2026 18:00 GMT · next: Oort marbles Short v02"))
        self.assertEqual([j["id"] for j in v23["jobs"]], ["J0962"])  # found by its video id alone

    def test_back_to_done_when_jobs_finish_and_blocked_jobs_never_pull_it_back(self):
        cards = build([
            job("J0962", "done", "023 Venus VBaYRPp85Sw: thumbnail test"),
            job("J0910", "blocked", "028 Shorts: set Related video -> F-jImX5h7ws after Sun 29 Nov 18:00Z"),
            job("J0999", "open", "028 Buffer posts once the long is public", after="J0910"),
        ])
        self.assertEqual((cards["OWB:023"]["lane"], cards["OWB:028"]["lane"]), ("done", "done"))
        self.assertIn("Private, scheduled Sun 29 Nov", cards["OWB:028"]["line"])

    def test_past_publish_time_reads_public(self):
        v = build([])["OWB:023"]
        self.assertEqual((v["lane"], v["youtube"]["state"], v["youtube"]["privacy"]), ("done", "live", "public"))
        self.assertTrue(v["line"].startswith("Public on YouTube since Sun 25 Oct 2026"))

    def test_board_check_flags_a_claimed_job_on_a_done_card(self):
        v = build([job("J0962", "claimed", "023 Venus VBaYRPp85Sw: thumbnail test", by="cursor")])["OWB:023"]
        ok = board_check.check([], {"tracker": {"videos": [v]}}, site_status=lambda url, follow=True: 200)
        self.assertTrue(ok["ok"], ok["problems"])
        bad = board_check.check([], {"tracker": {"videos": [{**v, "lane": "done"}]}}, site_status=lambda url, follow=True: 200)
        self.assertTrue(any("J0962 claimed but the card is in Done" in p for p in bad["problems"]))


if __name__ == "__main__":
    unittest.main()
