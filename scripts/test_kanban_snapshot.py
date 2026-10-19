#!/usr/bin/env python3
"""Tests for kanban_snapshot.py: stage 'since' times and the film notes (board/briefs)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kanban_snapshot as ks  # noqa: E402


class Since(unittest.TestCase):
    snaps = [("2026-10-05T10:00:00Z", {"picture": "todo", "edit": "todo"}),
             ("2026-10-06T10:00:00Z", {"picture": "doing", "edit": "todo"}),
             ("2026-10-07T10:00:00Z", {"picture": "doing", "edit": "todo"}),
             ("2026-10-08T10:00:00Z", {"picture": "done", "edit": "review"})]

    def test_since_is_when_the_current_state_began(self):
        s = ks.since_from_history(self.snaps[:3], truncated=False)
        self.assertEqual(s["picture"], "2026-10-06T10:00:00Z")  # not the 7 Oct commit that left it unchanged
        self.assertEqual(ks.since_from_history(self.snaps, truncated=False)["edit"], "2026-10-08T10:00:00Z")

    def test_cut_short_history_gives_no_time_for_a_state_older_than_it(self):
        s = ks.since_from_history(self.snaps[:3], truncated=True)
        self.assertNotIn("edit", s)  # 'todo' since before the oldest commit we can see
        self.assertEqual(s["picture"], "2026-10-06T10:00:00Z")
        self.assertEqual(ks.since_from_history([], truncated=True), {})


class MiniWork(unittest.TestCase):
    def test_claim_to_release_is_work_and_overnight_is_capped(self):
        jobs = [{"id": "J1", "needs": "mini", "film": "025", "history": [
                    {"at": "2026-10-08T10:00Z", "by": "claude", "what": "added"},
                    {"at": "2026-10-08T10:10Z", "by": "cursor", "what": "claimed"},
                    {"at": "2026-10-08T10:40Z", "by": "cursor", "what": "released: step 1"},
                    {"at": "2026-10-08T11:00Z", "by": "cursor", "what": "claimed"},
                    {"at": "2026-10-08T11:15Z", "by": "cursor", "what": "done: ok"}]},
                {"id": "J2", "needs": "mini", "history": [
                    {"at": "2026-10-07T20:00Z", "by": "cursor", "what": "claimed"},
                    {"at": "2026-10-08T09:00Z", "by": "cursor", "what": "done: ok"}]},
                {"id": "J3", "needs": "cloud", "history": [
                    {"at": "2026-10-08T10:00Z", "by": "claude", "what": "claimed"},
                    {"at": "2026-10-08T11:00Z", "by": "claude", "what": "done: ok"}]}]
        w = ks.mini_work(jobs, "2026-10-08")
        self.assertEqual(w["byFilm"], {"OWB:025": 45, "admin": 480})  # J2's 13 h claim counts as 8 h
        self.assertEqual((w["jobs"], w["minutes"]), (2, 525))
        self.assertNotIn("claude", w["byAgent"])


class Briefs(unittest.TestCase):
    def test_real_file_loads_and_every_step_says_when(self):
        films = ks.load_briefs()
        self.assertTrue(films)
        for key, b in films.items():
            for k in ("updated", "mood", "line", "done", "holdup", "steps"):
                self.assertIn(k, b, key)
            self.assertIn(b["mood"], ("good", "waiting", "held", "finished", "watched", "fixing", "ready"), key)
            for st in b["steps"]:
                self.assertTrue((st.get("who") or st.get("kind") in ks.routing_doc()) and st.get("what"), key)  # kind: routed (12 Oct)
                self.assertTrue(st.get("done") or st.get("job") or st.get("afterJob") or st.get("when") or st.get("whenText"), f"{key}: {st}")

    def test_bad_key_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "b.json"
            p.write_text(json.dumps({"films": {"022": {}}}))
            old, ks.BRIEFS = ks.BRIEFS, p
            try:
                with self.assertRaises(SystemExit):
                    ks.load_briefs()
            finally:
                ks.BRIEFS = old


class JobProgress(unittest.TestCase):
    """The board's % done (Ben, 11 Oct 22:09): real step data from the queue, else nothing (the page uses time)."""

    def test_reported_progress_wins(self):
        j = {"progress": {"step": 2, "of": 6, "at": "2026-10-11T21:00Z", "by": "cursor"},
             "history": [{"at": "2026-10-11T20:00Z", "what": "released: step 1 of 3 done"}]}
        self.assertEqual(ks.job_progress(j), {"step": 2, "of": 6, "at": "2026-10-11T21:00Z"})

    def test_step_k_of_n_in_a_release_note(self):
        j = {"history": [{"at": "2026-10-11T19:00Z", "what": "added"}, {"at": "2026-10-11T19:10Z", "what": "claimed"},
                         {"at": "2026-10-11T19:40Z", "what": "released: stopping point, step 3 of 8 done"}]}
        self.assertEqual(ks.job_progress(j), {"step": 3, "of": 8, "at": "2026-10-11T19:40Z"})

    def test_no_numbers_no_progress_and_reopen_resets(self):
        self.assertIsNone(ks.job_progress({"history": [{"at": "t", "what": "released: Step 1 of v01f done"}]}))
        j = {"history": [{"at": "a", "what": "released: step 2 of 4"}, {"at": "b", "what": "reopened: redo"}]}
        self.assertIsNone(ks.job_progress(j))
        self.assertIsNone(ks.job_progress({"progress": {"step": 5, "of": 4}, "history": []}))

    def test_work_start_is_the_first_claim_since_added_or_reopened(self):
        h = [{"at": "1", "what": "added"}, {"at": "2", "what": "claimed"}, {"at": "3", "what": "released"},
             {"at": "4", "what": "claimed"}]
        self.assertEqual(ks.work_start({"history": h}), "2")
        self.assertEqual(ks.work_start({"history": h + [{"at": "5", "what": "reopened"}, {"at": "6", "what": "claimed"}]}), "6")
        self.assertEqual(ks.work_start({"history": [{"at": "1", "what": "added"}]}), "")


if __name__ == "__main__":
    unittest.main()


class OrderAndHandoffs(unittest.TestCase):
    def test_run_order_matches_jobs_py(self):
        J = lambda i, **k: dict({"id": i, "needs": "mini", "status": "open", "film": "", "after": "", "eta_min": 120}, **k)
        jobs = [J("J1"), J("J2", urgent=2), J("J3", urgent=1, after="J9"), J("J4", status="claimed"), J("J5", film="026"),
                J("J9", status="blocked"), J("J6", needs="any", **{"for": "chief"})]
        r = ks.run_order(jobs, ["026"])
        self.assertEqual(r["lines"]["mini"], ["J4", "J2", "J5", "J1"])
        self.assertEqual(r["pos"]["J4"]["pos"], 0)
        self.assertEqual(r["pos"]["J2"]["pos"], 1)
        self.assertIsNone(r["pos"]["J3"]["pos"])
        self.assertEqual(r["pos"]["J3"]["waitsFor"], "J9")
        self.assertEqual(r["lines"]["chief"], ["J6"])

    def test_reviews_say_chief_and_future_handoffs_say_ready(self):
        b = {"OWB:024": {"steps": [{"who": "Claude", "what": "final OK", "done": True},
                                   {"who": "Claude", "what": "listen to the music and check v04"},
                                   {"who": "Claude", "what": "redraw the diagram"},
                                   {"who": "Ben", "what": "watch v05"}], "you": "",
                         "limit": "If not, Claude's final OK goes ahead."}}
        out = ks.ben_handoffs(ks.chief_reviews(b), {"OWB:024": {"url": "https://x"}})["OWB:024"]
        self.assertEqual([s["who"] for s in out["steps"]], ["Claude", "Chief", "Claude", "Ready for you"])
        self.assertIn("the Chief's final OK", out["limit"])
        b["OWB:024"]["you"] = "Watch v05"
        out = ks.ben_handoffs(b, {"OWB:024": {"url": "https://x"}})["OWB:024"]
        self.assertEqual(out["steps"][-1]["who"], "Ben")


class DateGates(unittest.TestCase):
    def test_no_start_gates_on_the_board(self):  # Ben, 12 Oct 2026 14:37
        jobs = [{"id": "J1", "status": "open", "title": "025 date gate: mark done on/after Sun 8 Nov 18:00Z", "body": ""},
                {"id": "J2", "status": "open", "title": "x", "body": "", "not_before": "2026-10-12T14:00Z"}]
        self.assertEqual(ks.gates(jobs), {})


class RoutedSteps(unittest.TestCase):
    """Ben, 12 Oct ("Is Gemini not used at all?"): steps still to do show the routed worker by kind; done steps keep
    their doer; HOS queue jobs join the HOS film note like OWB jobs do."""
    jobs = [{"id": "J1", "status": "open", "title": "HOS 006 Part 03 rough v01 (P3:06 held)", "kind": "assembly", "needs": "mini"},
            {"id": "J2", "status": "claimed", "by": "codex", "title": "HOS 006 graphics", "kind": "chart"},
            {"id": "J3", "status": "done", "by": "cursor", "title": "HOS 006 Part 03 picture", "kind": "video"},
            {"id": "J4", "status": "open", "title": "025 Mars Short", "kind": "chart"}]

    def test_names_by_kind(self):
        self.assertEqual(ks.routed_who("facts"), "Gemini")
        self.assertEqual(ks.routed_who("chart"), "Codex")
        self.assertEqual(ks.routed_who("script"), "Claude")
        self.assertEqual(ks.routed_who("chief"), "Chief")
        self.assertEqual(ks.routed_who("", "cursor-claude-opus-5-5"), "Claude (in Cursor)")
        self.assertEqual(ks.routing_doc()["facts"]["who"], "Gemini")

    def test_todo_steps_route_done_steps_keep_their_doer(self):
        b = {"HOS:006": {"steps": [
            {"who": "Grok", "what": "Fact check", "done": True},
            {"who": "Grok", "what": "check every number and date on the graphics"},
            {"who": "Cursor", "what": "graphics", "job": "J2"},
            {"what": "picture", "job": "J3"},
            {"kind": "script", "who": "Grok", "what": "script for the Short"},
            {"who": "Ben", "what": "final OK", "kind": "qa"}]}}
        out = [s["who"] for s in ks.route_steps(b, self.jobs)["HOS:006"]["steps"]]
        self.assertEqual(out, ["Grok", "Gemini", "Codex", "Cursor", "Claude", "Ben"])

    def test_hos_queue_jobs_join_the_note_before_ben(self):
        b = {"HOS:006": {"steps": [{"who": "Cursor", "what": "x", "job": "J2"}, {"who": "Ben", "what": "final OK"}]},
             "OWB:025": {"steps": []}}
        out = ks.hos_job_steps(b, self.jobs)
        self.assertEqual([s.get("job") for s in out["HOS:006"]["steps"]], ["J2", "J1", None])
        self.assertEqual(out["HOS:006"]["steps"][1]["who"], "Cursor")
        self.assertEqual(out["HOS:006"]["steps"][1]["what"], "Part 03 rough v01")
        self.assertEqual(out["OWB:025"]["steps"], [])  # OWB jobs: the page adds them

    def test_todo_hos_stages_get_the_routed_owner(self):
        hos = {"films": [{"id": "006", "stages": {"facts": {"status": "done"}, "thumbnails": {"status": "todo"},
                                                  "edit": {"status": "todo", "owner": "Cursor"}}}]}
        ks.route_hos_stages(hos)
        st = hos["films"][0]["stages"]
        self.assertNotIn("owner", st["facts"])
        self.assertEqual(st["thumbnails"]["owner"], "Codex")
        self.assertEqual(st["edit"]["owner"], "Cursor")


class WeekNumbers(unittest.TestCase):
    """Ben, 14 Oct: the board's tiles show seven days of jobs done and Mini idle, today last."""

    def test_seven_london_days_today_last(self):
        from datetime import datetime, timezone
        now = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)   # 11:00 London (BST)
        jobs = [{"id": "J1", "needs": "mini", "status": "done", "history": [
                    {"what": "claimed", "at": "2026-10-13T09:00Z"}, {"what": "done: ok", "at": "2026-10-13T11:00Z"}]},
                {"id": "J2", "needs": "mini", "status": "claimed", "history": [{"what": "claimed", "at": "2026-10-14T09:00Z"}]},
                {"id": "J3", "needs": "cloud", "status": "done", "history": [{"what": "done", "at": "2026-10-13T22:30Z"}]}]  # 23:30 London, 13th
        w = ks.week_numbers(jobs, now)
        self.assertEqual([d["date"] for d in w], [f"2026-10-{d:02d}" for d in range(8, 15)])
        self.assertEqual([d["done"] for d in w], [0, 0, 0, 0, 0, 2, 0])
        self.assertEqual(w[-2], {"date": "2026-10-13", "done": 2, "idleMin": 1440 - 120, "min": 1440})
        self.assertEqual(w[-1], {"date": "2026-10-14", "done": 0, "idleMin": 660 - 60, "min": 660})
        self.assertEqual(ks.day_numbers(jobs, now), {"since": "2026-10-13T23:00Z", "doneToday": 0, "idleMin": 600})

    def test_clock_change_day_is_25_hours(self):
        from datetime import datetime, timezone
        w = ks.week_numbers([], datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc))
        self.assertEqual(next(d for d in w if d["date"] == "2026-10-25")["min"], 25 * 60)


class ReleaseReceipts(unittest.TestCase):
    def receipt(self, root, name, **updates):
        doc = {"ok": True, "dryRun": False, "upload": {"published": True, "scheduledOnPlatform": True,
               "platformPostId": "abc12345678", "scheduledFor": "2026-11-08T18:00:00Z",
               "responseSummary": '{"privacyStatus":"private"}'}}
        doc.update(updates)
        path = root / "02_Video-Projects/025_Mars/11_Upload-Package" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc))

    def test_actual_schedule_is_distinct_from_uploaded_and_live(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.receipt(root, "PACKAGE_UPLOAD_RESULT_2026-10-09.json")
            record = ks.release_record("025", root)
            self.assertEqual(record["state"], "scheduled")  # upload.published means uploaded, not public
            self.assertEqual(record["videoId"], "abc12345678")
            self.assertEqual(record["publishAt"], "2026-11-08T18:00:00Z")
            self.assertTrue(record["source"].endswith("2026-10-09.json"))

    def test_dry_run_failure_and_other_films_are_not_release_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.receipt(root, "PACKAGE_UPLOAD_RESULT_2026-10-09.json", dryRun=True)
            self.receipt(root, "PACKAGE_UPLOAD_RESULT_2026-10-10.json", ok=False)
            self.assertIsNone(ks.release_record("025", root))
            self.assertIsNone(ks.release_record("024", root))

    def test_newer_actual_upload_without_schedule_replaces_old_schedule(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.receipt(root, "PACKAGE_UPLOAD_RESULT_2026-10-09.json")
            self.receipt(root, "PACKAGE_UPLOAD_RESULT_2026-10-10.json", upload={"platformPostId":"new12345678", "published":True})
            self.assertEqual(ks.release_record("025", root)["state"], "uploaded")
            self.receipt(root, "PACKAGE_UPLOAD_RESULT_2026-10-11.json", upload={"platformPostId":"new12345678", "published":True, "responseSummary":'{"privacyStatus":"public"}'})
            self.assertEqual(ks.release_record("025", root)["state"], "live")
