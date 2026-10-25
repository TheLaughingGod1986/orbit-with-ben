#!/usr/bin/env python3
"""HOS longs read back from HOS UPLOADS.json (Ben, 25 Oct 2026 22:54: "Why is it in progress on the board").
HOS 005 was Private + scheduled with only a go-public-gated job left, yet its card sat in In progress because the board
had no YouTube state for any HOS long until it went public."""
from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board_check  # noqa: E402
import kanban_snapshot as ks  # noqa: E402
import video_tracker as vt  # noqa: E402

NOW = dt.datetime(2026, 10, 25, 23, 0, tzinfo=dt.timezone.utc)
GATED = {"id": "J0241", "status": "blocked", "title": "HOS 005 s04: Related once the long is public", "body": "",
         "result": "waits for input: HOS 005 long wwcjcFfC-5M public (publishAt Thu 29 Oct 18:00 London); reopen then",
         "taskKeys": ["HOS:005"], "history": []}


def film(upload=None):
    f = {"id": "005", "title": "The Tied Arm That Proved Your Blood Circulates", "air": "2026-10-29",
         "stages": {"scheduled": {"status": "done"}}}
    if upload:
        f["upload"] = upload
    return f


def build(f):
    return {v["key"]: v for v in vt.build_videos(
        hos={"films": [f]}, owb=[], briefs={}, jobs=[GATED], checks={}, uploads={}, overrides={"jobFilms": {"J0241": ["HOS:005"]}},
        now=NOW, public={}, titles={})["videos"]}


class HosLongReadBack(unittest.TestCase):
    def test_snapshot_attaches_the_long_row(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "00_Brand/Channel-Setup/social/UPLOADS.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({"videos": {
                "wwcjcFfC-5M": {"kind": "long", "film": "005", "privacyStatus": "private", "publishAt": "2026-10-29T18:00:00Z"},
                "Rl2uZ-KOTl8": {"kind": "short", "film": "005", "publishAt": "2026-10-30T11:30:00Z"},
                "OLDv1xxxxxx": {"kind": "long", "film": "005", "retired": True},
            }}))
            hos = {"films": [film(), {"id": "011"}]}
            ks.attach_hos_uploads(Path(d), hos)
        self.assertEqual(hos["films"][0]["upload"]["videoId"], "wwcjcFfC-5M")
        self.assertNotIn("upload", hos["films"][1])

    def test_scheduled_long_with_only_a_go_public_job_is_done_not_progress(self):
        v = build(film({"videoId": "wwcjcFfC-5M", "privacyStatus": "private", "publishAt": "2026-10-29T18:00:00Z"}))["HOS:005"]
        self.assertEqual((v["lane"], v["youtube"]["state"], v["youtube"]["videoId"]), ("done", "scheduled", "wwcjcFfC-5M"))
        self.assertIn("Private, scheduled", v["line"])

    def test_without_read_back_board_check_flags_it(self):
        v = build(film())["HOS:005"]
        self.assertEqual(v["lane"], "progress")
        board = {"hos": {"pipeline": {"films": [film()]}}, "tracker": {"videos": [v]}, "checks": {}}
        res = board_check.check([], board, site_status=lambda url, follow=True: 200)
        self.assertFalse(res["ok"])
        self.assertTrue(any("HOS:005: scheduled in PIPELINE" in p for p in res["problems"]))


if __name__ == "__main__":
    unittest.main()
