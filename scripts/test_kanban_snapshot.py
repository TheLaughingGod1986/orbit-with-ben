#!/usr/bin/env python3
"""Tests for kanban_snapshot.py: stage 'since' times and the film notes (board/briefs)."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channels  # noqa: E402
import kanban_snapshot as ks  # noqa: E402


class CompletedResults(unittest.TestCase):
    def job(self, n, at="2026-10-19T10:00Z", **fields):
        return {"id": f"J{n}", "title": "Channel check", "status": "done",
                "history": [{"at": at, "what": "done: passed"}], **fields}

    def test_last_video_result_survives_more_than_sixty_channel_checks(self):
        from datetime import datetime, timezone
        jobs = [self.job(i) for i in range(70)] + [
            self.job(100, "2026-10-18T10:00Z", taskKeys=["HOS:006"], stage="picture", result="Picture fixes delivered"),
            self.job(101, "2026-10-17T10:00Z", taskKeys=["HOS:006"], stage="picture", result="Older fix"),
            self.job(102, "2026-10-16T10:00Z", film="024", stage="edit", result="Master delivered")]
        rows = ks.completed_jobs(jobs, datetime(2026, 10, 21, tzinfo=timezone.utc))
        ids = {j["id"] for j in rows}
        self.assertIn("J100", ids)
        self.assertIn("J102", ids)
        self.assertNotIn("J101", ids)
        self.assertEqual(len(rows), 62)
        self.assertEqual(next(j for j in rows if j["id"] == "J100")["result"], "Picture fixes delivered")

    def test_every_completion_in_last_twenty_four_hours_is_retained(self):
        from datetime import datetime, timezone
        jobs = [self.job(i) for i in range(90)]
        self.assertEqual(len(ks.completed_jobs(jobs, datetime(2026, 10, 19, 12, tzinfo=timezone.utc))), 90)

    def test_explicit_target_wins_over_old_title_and_review_is_not_done(self):
        from datetime import datetime, timezone
        jobs = [self.job(i) for i in range(60)] + [
            self.job(100, "2026-10-18T10:00Z", title="HOS 007 draft", taskKeys=["HOS:006"]),
            self.job(101, "2026-10-17T10:00Z", title="HOS 007 draft"),
            self.job(102, status="blocked", taskKeys=["HOS:008"])]
        rows = ks.completed_jobs(jobs, datetime(2026, 10, 21, tzinfo=timezone.utc))
        self.assertTrue({"J100", "J101"}.issubset({j["id"] for j in rows}))
        self.assertNotIn("J102", {j["id"] for j in rows})


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

    def test_work_is_filed_under_the_jobs_own_channel(self):
        # Until 11 Nov 2026 every film was filed under the first channel's label, so another channel's film 013 was
        # added to the first channel's 013.
        other = next(c for c in channels.slugs() if c != channels.default())
        stretch = [{"at": "2026-10-08T10:00Z", "by": "cursor", "what": "claimed"},
                   {"at": "2026-10-08T10:30Z", "by": "cursor", "what": "done: ok"}]
        whole = f"{channels.label(other)}:standalone"  # a film field that is already a whole key stays as it is
        jobs = [{"id": "J1", "needs": "mini", "film": "013", "repo": channels.default(), "history": stretch},
                {"id": "J2", "needs": "mini", "film": "013", "repo": other, "history": stretch},
                {"id": "J3", "needs": "mini", "film": whole, "repo": other, "history": stretch}]
        self.assertEqual(ks.mini_work(jobs, "2026-10-08")["byFilm"],
                         {f"{channels.label(channels.default())}:013": 30, f"{channels.label(other)}:013": 30, whole: 30})


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
        out = ks.queue_job_steps(b, self.jobs)
        self.assertEqual([s.get("job") for s in out["HOS:006"]["steps"]], ["J2", "J1", None])
        self.assertEqual(out["HOS:006"]["steps"][1]["who"], "Cursor")
        self.assertEqual(out["HOS:006"]["steps"][1]["what"], "Part 03 rough v01")
        self.assertEqual(out["OWB:025"]["steps"], [])  # OWB jobs: the page adds them

    def test_todo_hos_stages_get_the_routed_owner(self):
        hos = {"films": [{"id": "006", "stages": {"facts": {"status": "done"}, "thumbnails": {"status": "todo"},
                                                  "edit": {"status": "todo", "owner": "Cursor"}}}]}
        ks.route_pipeline_stages(hos)
        st = hos["films"][0]["stages"]
        self.assertNotIn("owner", st["facts"])
        self.assertEqual(st["thumbnails"]["owner"], "Codex")
        self.assertEqual(st["edit"]["owner"], "Cursor")

    def test_a_channel_with_one_status_file_per_film_is_routed_from_its_own_stage_kinds(self):
        # J2622: the same rule for the other shape of stage record (`state`), with the kinds the channel itself names.
        films = [{"film": "006", "stages": {"facts": {"state": "done"}, "thumbnails": {"state": "todo"},
                                            "edit": {"state": "todo", "owner": "Cursor"}, "ben_ok": {"state": "todo"}}}]
        ks.route_stages(films, {"facts": "facts", "thumbnails": "chart", "edit": "assembly"})
        st = films[0]["stages"]
        self.assertNotIn("owner", st["facts"])                       # done: keeps its doer, gets no owner
        self.assertEqual(st["thumbnails"]["owner"], "Codex")         # to do, nobody has it: the routed worker
        self.assertEqual(st["edit"]["owner"], "Cursor")              # someone has it: left alone
        self.assertNotIn("owner", st["ben_ok"])                      # a stage whose kind the channel does not name

    def test_a_channel_that_names_no_kinds_keeps_its_cards_as_they_are(self):
        films = [{"film": "033", "stages": {"script": {"state": "todo"}, "edit": {"state": "todo"}}}]
        before = json.dumps(films)
        ks.route_stages(films, {})
        self.assertEqual(json.dumps(films), before)
        ks.route_stages(None, {"script": "script"})                  # a channel with no films yet

    def test_the_one_file_channel_takes_its_kinds_from_its_settings_once_it_names_them(self):
        hos = {"films": [{"id": "006", "stages": {"thumbnails": {"status": "todo"}, "edit": {"status": "todo"}}}]}
        ks.route_pipeline_stages(hos, {"edit": "assembly"})          # its own kinds: only `edit` is named
        st = hos["films"][0]["stages"]
        self.assertIn("owner", st["edit"])
        self.assertNotIn("owner", st["thumbnails"])


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


def made_up(slug, label, **pipeline):
    """A channel that is in no registry: an existing one's settings under another name, keeping its films as given."""
    return dict(channels.get(channels.default()), slug=slug, label=label, name=f"Made Up {label}", short=label.title(),
                home=False, order=9, title_match=rf"\b{label}\b", pipeline=pipeline,
                repo={"env": f"{label}_REPO", "checkouts": [f"made-up-{slug}"]},
                uat_dir={"env": f"{label}_UAT_DIR", "icloud": f"{label} UAT"})


def plugged(*more):
    base = channels._load()
    return mock.patch.object(channels, "_load", lambda directory=None: base + tuple(more))


def checkout_of(slug: str, base: Path, films=()) -> Path:
    """A folder that holds a channel's film state the way that channel keeps it, with these film numbers."""
    root, kept = base / slug, channels.pipeline(slug)
    if kept["kind"] == "pipeline_json":
        (root / kept["path"]).parent.mkdir(parents=True, exist_ok=True)
        (root / kept["path"]).write_text(json.dumps({"films": [
            {"id": n, "title": f"Film {n}", "stages": {"edit": {"status": "todo"}}} for n in films]}))
    else:
        root.mkdir(parents=True, exist_ok=True)
        for n in films:
            file = root / kept["path"].replace("*", f"{n}_Made-Up")
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(json.dumps({"film": n, "title": f"Film {n}", "next": "edit it",
                                        "stages": {"edit": {"state": "todo"}}}))
    return root


class AnyChannel(unittest.TestCase):
    """J2617 (11 Nov 2026): the card builder takes its channels from the registry. Two channels that exist nowhere,
    one keeping its films each way, get documents, queue steps and a store file. No line of kanban_snapshot.py names a
    channel: scripts/test_channel_ratchet.py holds that at 0."""
    SKY = made_up("sky", "SKY", kind="film_status", path="films/*/status.json")
    SEA = made_up("deep-sea", "SEA", kind="pipeline_json", path="plan/PIPELINE.json")

    def test_documents_are_read_the_way_each_channel_keeps_its_films(self):
        with tempfile.TemporaryDirectory() as tmp, plugged(self.SKY, self.SEA):
            roots = {"sky": checkout_of("sky", Path(tmp), ["001", "002"]),
                     "deep-sea": checkout_of("deep-sea", Path(tmp), ["007"])}
            got = ks.read_documents(roots)
            self.assertEqual([f["film"] for f in got["sky"]], ["001", "002"])
            self.assertEqual([f["id"] for f in got["deep-sea"]["films"]], ["007"])
            self.assertEqual(ks.film_rows("sky", got["sky"])[0][0], "001")
            self.assertEqual(ks.film_rows("deep-sea", got["deep-sea"])[0][0], "007")

    def test_a_pipeline_file_with_no_films_list_stops_the_run(self):
        with tempfile.TemporaryDirectory() as tmp, plugged(self.SEA):
            root = checkout_of("deep-sea", Path(tmp))
            (root / "plan/PIPELINE.json").write_text("{}")
            with self.assertRaises(SystemExit):
                ks.read_documents({"deep-sea": root})

    def test_queue_jobs_join_any_channels_note_except_the_queue_documents_own(self):
        own = channels.label(channels.queue_key())
        jobs = [{"id": "J1", "status": "open", "title": "SEA 007 Part 03 rough v01 (after J9)", "kind": "video"},
                {"id": "J2", "status": "open", "title": f"{own} 025 Part 03 rough v01", "kind": "video"},
                {"id": "J3", "status": "done", "title": "SEA 007 old job"},
                {"id": "J4", "status": "claimed", "title": "no film in the title", "film": "SKY:001"}]
        notes = {"SEA:007": {"steps": [{"who": "Ben", "what": "final OK"}]}, "SKY:001": {"steps": []},
                 f"{own}:025": {"steps": []}, "XYZ:001": {"steps": []}}
        with plugged(self.SKY, self.SEA):
            out = ks.queue_job_steps(notes, jobs)
        self.assertEqual([s.get("job") for s in out["SEA:007"]["steps"]], ["J1", None])  # before Ben's own step
        self.assertEqual(out["SEA:007"]["steps"][0]["what"], "Part 03 rough v01")
        self.assertEqual([s.get("job") for s in out["SKY:001"]["steps"]], ["J4"])
        self.assertEqual(out[f"{own}:025"]["steps"], [])   # the page adds these itself
        self.assertEqual(out["XYZ:001"]["steps"], [])      # no such channel: left as it is

    def test_the_bad_key_message_lists_the_registrys_labels(self):
        with tempfile.TemporaryDirectory() as tmp, plugged(self.SKY):
            file = Path(tmp) / "briefs.json"
            file.write_text(json.dumps({"films": {"NOPE:001": {"steps": []}}}))
            with mock.patch.object(ks, "BRIEFS", file), self.assertRaises(SystemExit) as stop:
                ks.load_briefs()
        self.assertIn("SKY:NNN", str(stop.exception))

    def test_the_whole_builder_with_two_made_up_channels_beside_todays(self):
        """One real run on this checkout, with a made folder for every channel that is not this checkout."""
        import board_publish
        films = {"sky": ["001"], "deep-sea": ["007"]}
        with tempfile.TemporaryDirectory() as tmp, plugged(self.SKY, self.SEA), contextlib.ExitStack() as quiet:
            # Never touch the world from a test (25 Oct 2026: a test run on the Mini sent fixtures to the video
            # store). No watch folder, no upload, no register outside the temp folder, no fetch.
            for name, value in (("ICLOUD", Path(tmp) / "icloud"), ("WATCH_LOCAL_REGISTER", Path(tmp) / "register.json"),
                                ("UAT_DIRS", {c: Path(tmp) / "icloud" / c for c in channels.labels()}),
                                ("r2_ready", lambda *a, **k: False), ("mini_heartbeat", lambda: None)):
                quiet.enter_context(mock.patch.object(ks, name, value))
            args, out = [], Path(tmp) / "out"
            for slug in channels.slugs():
                if channels.checkout(slug) != ks.ROOT:
                    args += [f"--{slug}", str(checkout_of(slug, Path(tmp), films.get(slug, ())))]
            with contextlib.redirect_stdout(io.StringIO()) as said:
                self.assertEqual(ks.main([*args, "--db-out", str(out)]), 0)
            docs = {p.stem: json.loads(p.read_text()) for p in out.glob("*.json")}
            slugs = channels.slugs()
            one_file = {slug: ks.one_file(slug) for slug in slugs}   # each channel's own way, whatever it is this week
        # what the publisher reads is all there, and every channel has its own file in its own shape
        self.assertLessEqual(set(board_publish.SECTIONS), set(docs))
        for slug in slugs:
            self.assertIn(f"/{slug}.json", said.getvalue())
        queue = docs[channels.queue_key()]
        for key in ("films", "jobs", "lanes", "focus", "runOrder", "recent", "jobStates", "routing", "done", "videoProgress"):
            self.assertIn(key, queue)
        for slug in slugs:   # only the queue's document carries the queue
            if slug != channels.queue_key():
                self.assertEqual(set(docs[slug]), {"updatedAt", "pipeline" if one_file[slug] else "films"}, slug)
        # the made-up channels came through like any other
        self.assertEqual([f["film"] for f in docs["sky"]["films"]], ["001"])
        self.assertEqual([f["id"] for f in docs["deep-sea"]["pipeline"]["films"]], ["007"])
        self.assertTrue(docs["deep-sea"]["pipeline"]["films"][0]["stages"]["edit"].get("owner"))  # routed like any other
        keys = {v.get("key") for v in docs["tracker"]["videos"]}
        self.assertTrue({"SKY:001", "SEA:007"} <= keys, sorted(k for k in keys if k and k[:3] in ("SKY", "SEA")))

    def test_a_channel_that_is_not_this_checkout_must_be_given_its_folder(self):
        with tempfile.TemporaryDirectory() as tmp, plugged(self.SKY), contextlib.redirect_stderr(io.StringIO()) as said:
            with self.assertRaises(SystemExit) as stop:
                ks.main(["--db-out", tmp])
        self.assertEqual(stop.exception.code, 2)
        self.assertIn("--sky", said.getvalue())


if __name__ == "__main__":
    unittest.main()
