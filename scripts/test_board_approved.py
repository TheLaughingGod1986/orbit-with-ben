#!/usr/bin/env python3
"""Approved, on its way (Ben, 25 Oct 2026 14:13: "Ones I approve can they go into a waiting for deployment lane or
something? Need to know the ones I approve are still in the pipeline"). jobs.py records `approved_from` on the job
that delivers what Ben OK'd; video_tracker shows it in the "approved" lane until the upload reads back; board_check.py
flags an approved job with no card there."""
from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board_check  # noqa: E402
import jobs as J  # noqa: E402
import video_tracker as vt  # noqa: E402

NOW = dt.datetime(2026, 10, 25, 14, 30, tzinfo=dt.timezone.utc)
URL = "https://studio-kanban.vercel.app/api/watch?v=x&e=1&s=y"


def job(jid, status="open", **kw):
    return {"id": jid, "status": status, "title": "x", "body": "", "repo": "owb", "needs": "mini", "history": [], **kw}


def held_short(jid="J0940", status="blocked"):
    j = job(jid, status=status)
    J.do_awaits(j, "chief", NOW, what="swap the 027 Short to v05", file="OWB UAT/earth/earth_v05.mp4", version="v05",
                due="2026-10-25 20:00", airs="2026-10-26 11:30", title="Earth Short v05", number="027", vtype="short")
    return j


def build(jobs, checks=None, videos_extra=None, hos=None, briefs=None, watch=None):
    for e in (appr := vt.approved_entries(jobs)):
        e["watch"] = {"url": URL, "version": e.get("version")}
    asks = vt.ask_entries(jobs)
    for e in asks:
        e["watch"] = {"url": URL}
    return vt.build_videos(hos=hos or {"films": []}, owb=[], briefs=briefs or {}, jobs=[j for j in jobs if j["status"] in vt.LIVE_STATUSES],
                           checks=checks or {}, uploads={}, overrides={}, now=NOW, public={}, titles={}, asks=asks,
                           approved=appr, alljobs=jobs, watch=watch or {})


def lane_of(doc, key):
    return next(v for v in doc["videos"] if v["key"] == key)


class JobsApproved(unittest.TestCase):
    def test_reopened_held_job_takes_its_own_ask(self):
        j = held_short()
        J.do_approved(j, j, "chief", NOW, ok_at="2026-10-25 11:11", ref="6396903361")
        self.assertNotIn("awaits_ben", j)
        a = j["approved_from"]
        self.assertEqual((a["version"], a["airs"], a["job"], a["okAt"], a["okRef"], a["channel"]),
                         ("v05", "2026-10-26T11:30Z", "J0940", "2026-10-25T11:11Z", "6396903361", "OWB"))

    def test_follow_on_job_links_to_the_asking_job_even_after_clear(self):
        src = job("J0924", status="done", repo="hos", film="006")
        J.do_awaits(src, "chief", NOW, what="watch HOS 006 v06", file="HOS UAT/006/v06.mp4", version="v06", card="HOS:006")
        J.do_awaits(src, "chief", NOW, clear=True)
        self.assertIn("awaits_was", src)          # kept so the follow-on can still link it
        new = job("J0945", repo="hos", film="006")
        J.do_approved(new, src, "chief", NOW, over={"airs": "2026-11-05 18:00"})
        self.assertEqual((new["approved_from"]["card"], new["approved_from"]["job"], new["approved_from"]["channel"],
                          new["approved_from"]["airs"]), ("HOS:006", "J0924", "HOS", "2026-11-05T18:00Z"))

    def test_several_cuts_need_entry_and_leave_the_rest_waiting(self):
        src = held_short("J0914")
        J.do_awaits(src, "chief", NOW, what="swap ISS to v04", file="OWB UAT/iss_v04.mp4", version="v04", add=True)
        new = job("J0942")
        with self.assertRaises(ValueError):
            J.do_approved(new, src, "chief", NOW)
        J.do_approved(new, src, "chief", NOW, entry=2)
        self.assertEqual((new["approved_from"]["what"], new["approved_from"]["askId"]), ("swap ISS to v04", "J0914.2"))
        self.assertEqual(src["awaits_ben"]["version"], "v05")   # the Earth cut still waits on Ben

    def test_nothing_to_link_is_an_error(self):
        with self.assertRaises(ValueError):
            J.do_approved(job("J1"), job("J1"), "chief", NOW)

    def test_clear_on_a_live_job_records_the_ok_unless_dropped(self):
        import io, json, tempfile, contextlib
        with tempfile.TemporaryDirectory() as d:
            q = Path(d) / "queue.json"
            orig = (J.load, J.save, J.JOBS_MD, J.publish_board, J.heartbeat)
            ld, sv = J.load, J.save
            J.load, J.save = (lambda path=None: ld(q)), (lambda data, path=None: sv(data, q))
            J.JOBS_MD = Path(d) / "JOBS.md"
            J.publish_board = lambda *a, **k: None
            J.heartbeat = lambda *a, **k: None
            try:
                for jid, extra in (("J0940", []), ("J0941", ["--dropped"])):
                    q.write_text(json.dumps({"next_id": 2, "jobs": [held_short(jid, status="open")]}))
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(J.main(["awaits", jid, "--clear", "--agent", "chief", *extra]), 0)
                    got = json.loads(q.read_text())["jobs"][0]
                    self.assertNotIn("awaits_ben", got)
                    self.assertEqual("approved_from" in got, not extra, jid)
            finally:
                J.load, J.save, J.JOBS_MD, J.publish_board, J.heartbeat = orig

    def test_cli_has_the_commands(self):
        src = (HERE / "jobs.py").read_text()
        for bit in ('sub.add_parser("approved"', '"--approved-from"', '"--dropped"'):
            self.assertIn(bit, src)


class Lane(unittest.TestCase):
    def ok_short(self, status="open", **kw):
        j = held_short(status="blocked")
        J.do_approved(j, j, "chief", NOW, ok_at="2026-10-25 11:11")
        j.update(status=status, **kw)
        return j

    def test_queued_job_is_on_its_way_with_status_air_and_play(self):
        doc = build([self.ok_short()])
        v = lane_of(doc, "OWB:OK:J0940")
        self.assertEqual(v["lane"], "approved")
        a = v["approved"]
        self.assertEqual((a["job"], a["state"], a["version"], a["airsText"]), ("J0940", "queued", "v05", "Mon 26 Oct 11:30"))
        self.assertTrue(v["watch"]["url"])
        self.assertFalse(a["warn"])
        self.assertEqual(doc["lanes"][4], {"id": "approved", "label": "Approved, on its way", "count": 1})

    def test_working_shows_progress(self):
        v = lane_of(build([self.ok_short("claimed", by="cursor", progress={"step": 2, "of": 4})]), "OWB:OK:J0940")
        self.assertEqual((v["approved"]["state"], v["approved"]["step"], v["approved"]["of"]), ("working", 2, 4))
        self.assertIn("cursor is on it, step 2 of 4", v["line"])

    def test_blocked_and_late_warn(self):
        v = lane_of(build([self.ok_short("blocked", history=[{"at": "2026-10-25T14:00Z", "what": "blocked: YouTube quota"}])]), "OWB:OK:J0940")
        self.assertIn("YouTube quota", v["approved"]["warn"])
        self.assertTrue(any(f["kind"] == "approved" for f in v["flags"]))
        late = self.ok_short()
        late["approved_from"]["airs"] = "2026-10-25T15:00Z"
        v = lane_of(build([late]), "OWB:OK:J0940")
        self.assertIn("Will miss its air time", v["approved"]["warn"])

    def test_done_waits_for_read_back_then_moves_to_done(self):
        d = self.ok_short("done", history=[{"at": "2026-10-25T14:20Z", "what": "done: uploaded"}], result="uploaded abc")
        v = lane_of(build([d]), "OWB:OK:J0940")
        self.assertEqual((v["lane"], v["approved"]["state"]), ("approved", "uploaded"))
        d["result"] = "New video XyZ12345678 read back: privacyStatus private, publishAt 2026-10-26T11:30:00Z (scheduled)"
        v = lane_of(build([d]), "OWB:OK:J0940")
        self.assertEqual(v["lane"], "done")
        self.assertIn("Private, scheduled", v["line"])

    def test_cancelled_shows_warning_then_drops(self):
        c = self.ok_short("cancelled", history=[{"at": "2026-10-25T14:00Z", "what": "cancelled: no"}])
        v = lane_of(build([c]), "OWB:OK:J0940")
        self.assertIn("cancelled", v["approved"]["warn"])
        c["history"][0]["at"] = "2026-10-20T14:00Z"
        self.assertFalse(any(x["key"] == "OWB:OK:J0940" for x in build([c])["videos"]))

    def test_existing_long_card_moves_and_ready_keeps_only_bens_asks(self):
        hos = {"films": [{"id": "006", "title": "Trees"}, {"id": "007", "title": "Vaccine"}]}
        briefs = {"HOS:006": {"you": "Final OK on v06"}, "HOS:007": {"you": "Final OK on v04"}}
        watch = {"HOS:006": {"url": URL, "version": "v06"}, "HOS:007": {"url": URL, "version": "v04"}}
        src = job("J0924", status="done", repo="hos", film="006")
        J.do_awaits(src, "chief", NOW, what="watch 006 v06", file="f.mp4", version="v06", card="HOS:006")
        new = job("J0945", repo="hos", film="006")
        J.do_approved(new, src, "chief", NOW, over={"airs": "2026-11-05 18:00"})
        checks = {"HOS-006": {"verdict": "ok", "version": "v06", "at": "2026-10-25T14:10Z", "handled": False}}
        doc = build([src, new], checks=checks, hos=hos, briefs=briefs, watch=watch)
        self.assertEqual((lane_of(doc, "HOS:006")["lane"], lane_of(doc, "HOS:006")["approved"]["job"]), ("approved", "J0945"))
        ready = [v["key"] for v in doc["videos"] if v["lane"] == "ready"]
        self.assertEqual(ready, ["HOS:007"])
        self.assertTrue(all(v["readyFor"] == "Ben" for v in doc["videos"] if v["lane"] == "ready"))

    def test_ok_tick_on_an_ask_leaves_ready_at_once(self):
        j = held_short()
        doc = build([j], checks={"OWB-J0940": {"verdict": "ok", "version": "v05", "at": "2026-10-25T14:00Z"}})
        v = next(x for x in doc["videos"] if (x.get("ask") or {}).get("id") == "J0940")
        self.assertEqual((v["lane"], v["approved"]["state"]), ("approved", "waiting"))
        self.assertIn("Waiting for the Chief to start J0940", v["line"])

    def test_parked_for_chief_without_ben_ok_is_in_progress(self):
        v = {"key": "OWB:028", "lane": "ready", "readyFor": "Chief", "check": None, "jobs": [], "flags": []}
        vt.settle_ready([v], NOW)
        self.assertEqual(v["lane"], "progress")


class Check(unittest.TestCase):
    def setUp(self):
        self.orig = board_check.file_on_mini
        board_check.file_on_mini = lambda rel: True

    def tearDown(self):
        board_check.file_on_mini = self.orig

    def approved_job(self):
        j = held_short()
        J.do_approved(j, j, "chief", NOW)
        j["status"] = "open"
        return j

    def test_missing_approved_card_is_flagged(self):
        res = board_check.check([self.approved_job()], {"checks": {}, "tracker": {"videos": []}},
                                site_status=lambda url, follow=True: 200)
        self.assertFalse(res["ok"])
        self.assertTrue(any("no card in Approved, on its way" in p for p in res["problems"]))

    def test_card_in_lane_passes(self):
        card = {"key": "OWB:OK:J0940", "lane": "approved", "approved": {"job": "J0940", "state": "queued"}, "watch": {"url": URL}}
        res = board_check.check([self.approved_job()], {"checks": {}, "tracker": {"videos": [card]}},
                                site_status=lambda url, follow=True: 200)
        self.assertTrue(res["ok"], res["problems"])
        self.assertEqual(res["approved"], 1)


class Page(unittest.TestCase):
    def test_phone_page_has_the_lane(self):
        site = HERE.parent / "05_Analytics/kanban"
        js = (site / "board_site/tracker_app.js").read_text()
        self.assertIn('["approved", "Approved, on its way"]', js)
        self.assertLess(js.index('["ready", "Ready for OK"]'), js.index('["approved", "Approved, on its way"]'))
        self.assertLess(js.index('["approved", "Approved, on its way"]'), js.index('["done", "Done on YouTube"]'))
        self.assertIn("function approvedHtml", js)
        html = (site / "video_tracker.html").read_text()
        self.assertIn('.lane[data-lane="approved"]', html)
        self.assertIn("repeat(6, 1fr)", html)


if __name__ == "__main__":
    unittest.main()
