#!/usr/bin/env python3
"""Jobs waiting on Ben (awaits_ben) always reach Ready for OK, and board_check.py notices when one doesn't
(Ben, 25 Oct 2026: "the ones needed from me I can't see them on the board")."""
from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import board_check  # noqa: E402
import jobs as J  # noqa: E402
import video_tracker as vt  # noqa: E402

NOW = dt.datetime(2026, 10, 25, 9, 0, tzinfo=dt.timezone.utc)


def job(jid, status="blocked", **kw):
    return {"id": jid, "status": status, "title": "x", "body": "", "repo": "owb", "history": [], **kw}


def held_short():
    j = job("J0940")
    J.do_awaits(j, "chief", NOW, what="swap the 027 Short to v05", file="OWB UAT/earth/earth_v05.mp4", version="v05",
                due="2026-10-25 20:00", title="Earth Short v05", number="027", vtype="short")
    return j


class Awaits(unittest.TestCase):
    def test_jobs_awaits_sets_and_clears(self):
        j = held_short()
        self.assertEqual(j["awaits_ben"]["due"], "2026-10-25T20:00Z")
        J.do_awaits(j, "chief", NOW, what="b", file="f2.mp4", add=True)
        self.assertEqual(len(j["awaits_ben"]), 2)
        J.do_awaits(j, "chief", NOW, clear=True)
        self.assertNotIn("awaits_ben", j)
        with self.assertRaises(ValueError):
            J.do_awaits(j, "chief", NOW, what="no file")

    def test_unuploaded_short_gets_a_ready_card(self):
        asks = vt.ask_entries([held_short()])
        asks[0]["watch"] = {"url": "https://studio-kanban.vercel.app/api/watch?v=x&e=1&s=y", "version": "v05"}
        doc = vt.build_videos(hos={"films": []}, owb=[], briefs={}, jobs=[], checks={}, uploads={}, overrides={},
                              now=NOW, public={}, titles={}, asks=asks)
        card = next(v for v in doc["videos"] if v.get("ask"))
        self.assertEqual((card["lane"], card["readyFor"], card["type"], card["checkId"]), ("ready", "Ben", "short", "OWB-J0940"))
        self.assertIn("Needed by Sun 25 Oct 20:00", card["line"])
        self.assertTrue(card["watch"]["url"])

    def test_old_version_change_tick_does_not_hide_new_cut(self):
        j = job("J0925", status="done", repo="hos")
        J.do_awaits(j, "chief", NOW, what="watch HOS 007 v04", file="HOS UAT/007/v04.mp4", version="v04", card="HOS:007")
        card = {"key": "HOS:007", "lane": "changes", "flags": []}
        e = vt.ask_entries([j])[0]
        vt.apply_ask(card, e, {"HOS-007": {"verdict": "change", "version": "v03", "handled": False}}, NOW)
        self.assertEqual((card["lane"], card["readyFor"], card["version"]), ("ready", "Ben", "v04"))
        # once the Chief has handled Ben's tick on v04, a done job's card stops asking
        self.assertFalse(vt.ask_live(e, {"HOS-007": {"verdict": "ok", "version": "v04", "handled": True}}))
        self.assertTrue(vt.ask_live(e, {"HOS-007": {"verdict": "ok", "version": "v04", "handled": False}}))

    def test_board_check_flags_missing_card_and_site(self):
        board = {"checks": {}, "tracker": {"videos": []}}
        res = board_check.check([held_short()], board, site_status=lambda url, follow=True: 500)
        self.assertFalse(res["ok"])
        self.assertTrue(any("no card" in p for p in res["problems"]))
        self.assertTrue(any("answers 500" in p for p in res["problems"]))
        self.assertTrue(board_check.note_text(res).startswith("[Chief] board-check"))

    def test_board_check_passes_with_card(self):
        e = vt.ask_entries([held_short()])[0]
        card = {"key": "OWB:ASK:J0940", "lane": "ready", "readyFor": "Ben", "ask": {"id": "J0940"},
                "watch": {"url": "https://studio-kanban.vercel.app/api/watch?v=x&e=1&s=y"}}
        orig = board_check.file_on_mini
        board_check.file_on_mini = lambda rel: True
        try:
            res = board_check.check([held_short()], {"checks": {}, "tracker": {"videos": [card]}},
                                    site_status=lambda url, follow=True: 302 if not follow else 200)
        finally:
            board_check.file_on_mini = orig
        self.assertTrue(res["ok"], res["problems"])
        self.assertEqual(e["id"], "J0940")


if __name__ == "__main__":
    unittest.main()
