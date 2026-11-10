#!/usr/bin/env python3
"""The first-day check (scripts/launch_check.py): what is due, the job it queues, the record, the verdict and the
report. Every test builds its own small studio in a temporary folder, so none reads the real numbers."""
import contextlib
import datetime as dt
import io
import json
import pathlib
import re
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import launch_check as lc  # noqa: E402
import refill  # noqa: E402

UTC = dt.timezone.utc
LIVE = dt.datetime(2026, 11, 10, 11, 30, tzinfo=UTC)   # the video under test goes live here


def t(text: str) -> dt.datetime:
    return dt.datetime.fromisoformat(text).replace(tzinfo=UTC)


def video(vid, fmt="short", privacy="public", live="2026-11-01T11:30:00Z", views=0, title="", seconds=20):
    """One row of a daily snapshot. A private video carries its scheduled time; a public one the time it went live."""
    public = privacy == "public"
    return {"id": vid, "title": title or f"Video {vid}", "format": fmt, "privacy": privacy, "seconds": seconds,
            "publishedAt": live if public else "2026-10-01T09:00:00Z", "publishAt": None if public else live,
            "views": views}


class Fixture(unittest.TestCase):
    """A throwaway studio with two channels, `aaa` and `bbb`."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        names = {"aaa": "Channel A", "bbb": "Channel B"}
        for name, fake in (("slugs", lambda: ["aaa", "bbb"]), ("name", names.get), ("studio_port", lambda slug: "9333"),
                           ("analytics_dir", lambda slug: self.root / "numbers" / slug),
                           ("uploads_file", lambda slug: self.root / "repo" / slug / "UPLOADS.json")):
            patch = mock.patch.object(lc.channels, name, fake)
            patch.start()
            self.addCleanup(patch.stop)

    def snapshot(self, taken: str, videos: list, slug: str = "aaa"):
        folder = self.root / "numbers" / slug / "snapshots"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{taken[:10]}.json").write_text(json.dumps({"date": taken[:10], "takenAt": taken, "videos": videos}))

    def register(self, videos: dict, slug: str = "aaa"):
        path = self.root / "repo" / slug / "UPLOADS.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"version": 1, "videos": videos}))

    def studio_read(self, videos: dict, slug: str = "aaa"):
        folder = self.root / "numbers" / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "studio_ctr.json").write_text(json.dumps({"videos": videos}))

    def checked(self, vid, fmt="short", live="2026-11-10T11:30Z", title="", faults=(), **figures) -> dict:
        """Store a record with one reading at 6 h (or `hours`)."""
        hours = figures.pop("hours", 6)
        info = {"id": vid, "title": title or f"Video {vid}", "format": fmt, "at": lc.studio.parse(live), "seconds": 20}
        rec = lc.with_reading(lc.load_record("aaa", vid), "aaa", info, {"hours": hours, **figures}, faults)
        lc.save_record("aaa", rec)
        return rec

    def usual_shorts(self):
        """Three Shorts with enough views to say what is normal: 32% stay, 66% of it is watched."""
        self.studio_read({f"u{i}": {"views": 500, "stayedToWatch": s, "avgViewPct": a}
                          for i, (s, a) in enumerate(((30, 60), (32, 66), (40, 70)))})


class WhatWentLive(Fixture):
    def test_a_scheduled_video_counts_once_its_time_has_passed(self):
        self.snapshot("2026-11-10T06:40:00Z", [video("today", privacy="private", live="2026-11-10T11:30:00Z"),
                                               video("tomorrow", privacy="private", live="2026-11-11T11:30:00Z")])
        self.assertEqual([v["id"] for v in lc.went_live("aaa", t("2026-11-10T11:00"))], [])
        self.assertEqual([v["id"] for v in lc.went_live("aaa", t("2026-11-10T12:00"))], ["today"])

    def test_a_public_video_is_timed_from_when_it_really_went_live(self):
        self.snapshot("2026-11-10T06:40:00Z", [video("pub", live="2026-11-09T11:30:10Z", views=900)])
        live = lc.went_live("aaa", t("2026-11-10T12:00"))
        self.assertEqual(live[0]["at"], dt.datetime(2026, 11, 9, 11, 30, 10, tzinfo=UTC))

    def test_trailers_and_other_formats_are_left_out(self):
        self.snapshot("2026-11-10T06:40:00Z", [video("tr", fmt="trailer", live="2026-11-10T08:00:00Z")])
        self.assertEqual(lc.went_live("aaa", t("2026-11-10T12:00")), [])

    def test_a_video_scheduled_after_the_snapshot_comes_from_the_register(self):
        self.snapshot("2026-11-10T06:40:00Z", [])
        self.register({"late": {"kind": "short", "publishAt": "2026-11-10T11:30:00Z", "title": "Added at nine"}})
        live = lc.went_live("aaa", t("2026-11-10T12:00"))
        self.assertEqual([(v["id"], v["title"], v["format"]) for v in live], [("late", "Added at nine", "short")])

    def test_an_upload_taken_off_the_schedule_since_the_snapshot_is_not_checked(self):
        self.snapshot("2026-11-10T06:40:00Z", [video(v, privacy="private", live="2026-11-10T11:30:00Z")
                                               for v in ("replaced", "pulled", "back-on")])
        self.register({"replaced": {"kind": "short", "supersededBy": "new"},
                       "pulled": {"kind": "short", "unscheduledAt": "2026-11-10T09:00:00Z"},
                       "back-on": {"kind": "short", "unscheduledAt": "2026-11-01T09:00:00Z"}})   # rescheduled since
        self.assertEqual([v["id"] for v in lc.went_live("aaa", t("2026-11-10T12:00"))], ["back-on"])

    def test_a_channel_with_no_numbers_or_register_has_nothing_live(self):
        self.assertEqual(lc.went_live("bbb", t("2026-11-10T12:00")), [])


class WhatIsDue(Fixture):
    def setUp(self):
        super().setUp()
        self.snapshot("2026-11-10T06:40:00Z", [video("short1", privacy="private", live="2026-11-10T11:30:00Z"),
                                               video("long1", fmt="long", privacy="private", live="2026-11-10T11:30:00Z")])

    def due(self, when: str, queue=None):
        return [(d["id"], d["hours"]) for d in lc.due(t(when), queue)]

    def test_nothing_is_due_before_six_hours(self):
        self.assertEqual(self.due("2026-11-10T17:29"), [])

    def test_a_short_gets_one_check_and_a_long_two(self):
        self.assertEqual(self.due("2026-11-10T17:30"), [("long1", 6), ("short1", 6)])
        self.assertEqual(self.due("2026-11-12T11:30"), [("long1", 48)])

    def test_a_check_that_could_not_run_in_time_is_dropped_after_eighteen_hours(self):
        self.assertEqual(self.due("2026-11-11T11:30"), [("long1", 6), ("short1", 6)])
        self.assertEqual(self.due("2026-11-11T11:31"), [])

    def test_a_reading_at_that_age_means_it_is_done(self):
        self.checked("short1", views=4)
        self.assertEqual(self.due("2026-11-10T18:00"), [("long1", 6)])

    def test_a_job_already_asked_for_it_counts_whatever_became_of_the_job(self):
        queue = {"jobs": [{"id": "J1", "status": "done", "launch": "short1@6"}]}
        self.assertEqual(self.due("2026-11-10T18:00", queue), [("long1", 6)])

    def test_every_channel_is_looked_at(self):
        self.snapshot("2026-11-10T06:40:00Z", [video("other", privacy="private", live="2026-11-10T11:30:00Z")], slug="bbb")
        self.assertIn(("bbb", "other"), [(d["channel"], d["id"]) for d in lc.due(t("2026-11-10T18:00"))])


class TheJob(Fixture):
    def setUp(self):
        super().setUp()
        self.snapshot("2026-11-10T06:40:00Z", [video("short1", privacy="private", live="2026-11-10T11:30:00Z",
                                                     title="What Would Standing on Titan Feel Like?")])
        self.at = t("2026-11-10T17:40")

    def test_one_job_is_queued_and_never_a_second(self):
        data = {"jobs": [], "next_id": 1}
        self.assertEqual(lc.queue_due(data, self.at), ["J0001"])
        self.assertEqual(lc.queue_due(data, self.at + dt.timedelta(minutes=10)), [])
        job = data["jobs"][0]
        self.assertEqual((job["needs"], job["kind"], job["repo"], job["launch"]), ("mini", "studio", "aaa", "short1@6"))
        self.assertEqual(job["due"], "2026-11-10T19:40:00Z")   # a deadline, so it runs ahead of standing work
        self.assertIn("6 hours after it went live", job["plain"])

    def test_the_job_is_not_mistaken_for_standing_backlog_work(self):
        title = lc.job_spec(lc.due(self.at)[0])["title"]
        self.assertIsNone(re.search(r"^Backlog|weekly .*audit|QA sweep|listing check.*live", title, re.I))

    def test_the_job_reads_and_never_changes_anything(self):
        body = lc.job_spec(lc.due(self.at)[0])["body"]
        self.assertIn("Read-only: change nothing in Studio", body)
        self.assertIn("launch_check.py record short1 --hours 6", body)
        self.assertIn("launch_check.py judge short1", body)
        self.assertIn("Never: edit the video", body)
        self.assertIn("Never delete anything", body)
        self.assertIn("Channel A", body)
        self.assertIn("Tue 10 Nov 11:30 London", body)

    def test_a_short_is_asked_for_feed_figures_and_a_long_for_click_figures(self):
        short = lc.job_spec({"id": "s", "title": "S", "format": "short", "at": LIVE, "channel": "aaa", "hours": 6})["body"]
        long_ = lc.job_spec({"id": "l", "title": "L", "format": "long", "at": LIVE, "channel": "aaa", "hours": 48})["body"]
        self.assertIn("Viewed vs swiped away", short)
        self.assertIn("--typical <n> --feed-views <n> --stayed <%>", short)
        self.assertIn("than usual", short)
        self.assertIn("Leave out any flag Studio gives no figure for.", short)
        self.assertIn("--typical <n> --impressions <n>", long_)
        self.assertIn("Impressions click-through rate", long_)
        self.assertIn("--impressions <n> --ctr <%>", long_)
        self.assertNotIn("--feed-views", long_)
        self.assertNotIn("Shorts tab", long_)


class TheRefillTick(unittest.TestCase):
    def test_due_checks_ride_on_the_refill(self):
        with mock.patch.object(lc, "queue_due", return_value=["J0007"]) as queue, \
                mock.patch.object(refill, "do_refill", return_value=["J0008"]):
            self.assertEqual(refill.top_up({"jobs": []}, [], LIVE), ["J0007", "J0008"])
        queue.assert_called_once()

    def test_a_fault_in_the_check_never_stops_the_refill(self):
        with mock.patch.object(lc, "queue_due", side_effect=RuntimeError("snapshot unreadable")), \
                mock.patch.object(refill, "do_refill", return_value=["J0008"]), \
                contextlib.redirect_stderr(io.StringIO()) as said:
            self.assertEqual(refill.top_up({"jobs": []}, [], LIVE), ["J0008"])
        self.assertIn("first-day checks not queued: snapshot unreadable", said.getvalue())


class TheRecord(Fixture):
    INFO = {"id": "v1", "title": "A Short", "format": "short", "at": LIVE, "seconds": 19}

    def test_a_first_reading_makes_the_record(self):
        rec = lc.with_reading(None, "aaa", self.INFO, {"hours": 6, "views": 4, "rank": 10, "of": 10, "shown": None})
        self.assertEqual((rec["channel"], rec["format"], rec["wentLive"], rec["seconds"]), ("aaa", "short", "2026-11-10T11:30Z", 19))
        self.assertEqual(rec["readings"], [{"hours": 6, "views": 4, "rank": 10, "of": 10}])   # no figure, no key

    def test_a_second_reading_at_the_same_age_corrects_the_first(self):
        rec = lc.with_reading(None, "aaa", self.INFO, {"hours": 6, "views": 4})
        rec = lc.with_reading(rec, "aaa", self.INFO, {"hours": 48, "views": 90})
        rec = lc.with_reading(rec, "aaa", self.INFO, {"hours": 6, "views": 5})
        self.assertEqual([(r["hours"], r["views"]) for r in rec["readings"]], [(6, 5), (48, 90)])

    def test_faults_are_kept_once_each(self):
        rec = lc.with_reading(None, "aaa", self.INFO, {"hours": 6, "views": 4}, ["Made for kids is on", " "])
        rec = lc.with_reading(rec, "aaa", self.INFO, {"hours": 6, "views": 4}, ["Made for kids is on", "No Related video"])
        self.assertEqual(rec["faults"], ["Made for kids is on", "No Related video"])

    def test_it_is_saved_under_the_channels_own_numbers(self):
        path = lc.save_record("aaa", lc.with_reading(None, "aaa", self.INFO, {"hours": 6, "views": 4}))
        self.assertEqual(path, self.root / "numbers" / "aaa" / "launch" / "v1.json")
        self.assertEqual(lc.load_record("aaa", "v1")["readings"][0]["views"], 4)
        self.assertTrue(path.read_text().endswith("}\n"))


class WhereItStands(Fixture):
    def level(self, **figures):
        v = lc.verdict("aaa", self.checked("mine", **figures))
        return v["level"], v["stage"]

    def test_with_no_earlier_checks_studios_own_rank_decides(self):
        self.assertEqual(self.level(views=4, rank=10, of=10, shown=900, stayed=31)[0], "behind")
        self.assertEqual(self.level(views=4, rank=8, of=10, shown=900, stayed=31)[0], "behind")
        self.assertEqual(self.level(views=400, rank=5, of=10)[0], "usual")
        self.assertEqual(self.level(views=900, rank=2, of=10)[0], "ahead")

    def test_studios_own_usual_figure_outranks_its_rank(self):
        # 10 Nov 2026, the Titan Short at 1 h 54 min: "4 views, 36 less than usual", yet ranked 7 of 10.
        v = lc.verdict("aaa", self.checked("mine", views=4, typical=40, rank=7, of=10))
        self.assertEqual(v["level"], "behind")
        self.assertEqual(v["why"][:2], ["4 views at 6 h; Studio says the usual for us at this age is 40.",
                                        "Studio ranks it 7 of 10 against our latest videos at the same age."])
        self.assertEqual(self.level(views=30, typical=40, rank=9, of=10)[0], "usual")
        self.assertEqual(self.level(views=1046, typical=630, rank=9, of=10)[0], "ahead")

    def test_our_own_earlier_checks_outrank_studios_usual_figure(self):
        for i, views in enumerate((400, 500, 600)):
            self.checked(f"old{i}", live=f"2026-11-0{i + 1}T11:30Z", views=views)
        self.assertEqual(self.level(views=450, typical=5000)[0], "usual")

    def test_with_neither_a_rank_nor_earlier_checks_it_says_so(self):
        v = lc.verdict("aaa", self.checked("mine", views=4))
        self.assertEqual(v["level"], "unknown")
        self.assertIn("Nothing to compare it with yet", v["why"][0])

    def test_three_earlier_checks_at_the_same_age_make_the_baseline(self):
        for i, views in enumerate((400, 500, 600)):
            self.checked(f"old{i}", live=f"2026-11-0{i + 1}T11:30Z", views=views)
        self.checked("later", live="2026-11-12T11:30Z", views=5000)   # after ours: never part of our baseline
        self.assertEqual(self.level(views=100, rank=2, of=10, shown=900, stayed=31)[0], "behind")   # our own numbers beat the rank
        self.assertEqual(self.level(views=450)[0], "usual")
        self.assertEqual(self.level(views=900)[0], "ahead")
        why = lc.verdict("aaa", lc.load_record("aaa", "mine"))["why"][0]
        self.assertEqual(why, "900 views at 6 h; the last 3 checked at the same age had 500 (median).")

    def test_a_reading_at_another_age_is_not_a_baseline(self):
        for i in range(3):
            self.checked(f"old{i}", live=f"2026-11-0{i + 1}T11:30Z", views=5000, hours=48)
        self.assertEqual(self.level(views=4)[0], "unknown")

    def test_no_reading_yet(self):
        v = lc.verdict("aaa", {"id": "x", "format": "short", "wentLive": "2026-11-10T11:30Z", "readings": []})
        self.assertEqual((v["level"], v["why"]), ("unknown", ["No reading has been recorded yet."]))


class WhichStepLostTheViewers(Fixture):
    def setUp(self):
        super().setUp()
        self.usual_shorts()

    def stage(self, fmt="short", **figures):
        v = lc.verdict("aaa", self.checked("mine", fmt=fmt, rank=10, of=10, **figures))
        self.assertEqual(v["level"], "behind")
        return v

    def test_a_short_shown_to_almost_nobody_was_not_shown(self):
        v = self.stage(views=4, shown=30)
        self.assertEqual(v["stage"], "not shown")
        self.assertIn("too few people to judge it", v["now"][0])

    def test_a_short_people_swiped_away_from(self):
        v = self.stage(views=40, shown=900, stayed=12.0, avgPct=70)
        self.assertEqual(v["stage"], "swiped")
        self.assertIn("gate_shorts_open.py", " ".join(v["now"]))
        self.assertIn("only after Ben has watched it", " ".join(v["carry"]))

    def test_a_short_people_stayed_for_and_then_left(self):
        self.assertEqual(self.stage(views=40, shown=900, stayed=31.0, avgPct=40.0)["stage"], "left early")

    def test_a_short_that_did_as_usual_with_few_people(self):
        v = self.stage(views=40, shown=300, stayed=31.0, avgPct=66.0)
        self.assertEqual(v["stage"], "small pool")
        self.assertIn("Nothing to fix", v["now"][0])

    def test_without_a_shown_figure_the_feed_views_and_the_stayed_rate_give_it(self):
        # Studio had no "Shown in feed" card on 10 Nov. 2 feed views at 25% stayed: the feed showed it about 8 times.
        v = self.stage(views=4, feedViews=2, stayed=25.0)
        self.assertEqual(v["stage"], "not shown")
        self.assertEqual(lc.shown_in_feed({"feedViews": 1003, "stayed": 38.5}), 2605)
        self.assertEqual(lc.shown_in_feed({"shown": 900, "feedViews": 2, "stayed": 25.0}), 900)   # Studio's own figure wins
        self.assertEqual(lc.shown_in_feed({"feedViews": 3}), 3)        # no stayed rate: at least the views themselves
        self.assertIsNone(lc.shown_in_feed({"views": 4}))
        swiped = self.stage(views=40, feedViews=120, stayed=12.0, avgPct=70)   # shown about 1,000 times, and swiped
        self.assertEqual(swiped["stage"], "swiped")

    def test_with_no_reach_figure_it_does_not_guess(self):
        v = self.stage(views=4)
        self.assertEqual(v["stage"], "")
        self.assertEqual(v["now"], lc.NO_FIGURES)

    def test_shown_is_judged_against_our_own_earlier_checks_when_there_are_three(self):
        for i in range(3):
            self.checked(f"old{i}", live=f"2026-11-0{i + 1}T11:30Z", views=500, shown=4000, stayed=33.0)
        v = lc.verdict("aaa", self.checked("mine", views=60, shown=1200, stayed=30.0))   # over 100, under 40% of 4,000
        self.assertEqual((v["level"], v["stage"]), ("behind", "not shown"))

    def test_a_long_nobody_was_shown(self):
        v = self.stage(fmt="long", views=3, impressions=40, ctr=5.0)
        self.assertEqual(v["stage"], "not shown")
        self.assertIn("Related video", " ".join(v["now"]))

    def test_a_long_shown_and_not_clicked(self):
        v = self.stage(fmt="long", views=9, impressions=800, ctr=1.2, hours=48)
        self.assertEqual(v["stage"], "not clicked")
        self.assertIn("a set test is never replaced or deleted without Ben", " ".join(v["now"]))

    def test_a_long_with_too_few_impressions_to_judge_its_click_rate(self):
        self.assertEqual(self.stage(fmt="long", views=1, impressions=150, ctr=0.5, avgPct=30)["stage"], "small pool")

    def test_a_long_clicked_and_left_early(self):
        self.studio_read({f"l{i}": {"impressions": 900, "impressionsCtr": 2.5, "avgViewPct": a} for i, a in enumerate((20, 24, 30))})
        self.assertEqual(self.stage(fmt="long", views=30, impressions=900, ctr=3.5, avgPct=9.0, hours=48)["stage"], "left early")

    def test_every_step_it_can_name_has_advice(self):
        for fmt, stages in (("short", ("not shown", "swiped", "left early", "small pool")),
                            ("long", ("not shown", "not clicked", "left early", "small pool"))):
            for stage in stages:
                do, carry = lc.ADVICE[(fmt, stage)]
                self.assertTrue(do and carry, (fmt, stage))

    def test_no_advice_tells_anyone_to_delete_or_to_replace_a_set_test(self):
        for (fmt, stage), (do, carry) in lc.ADVICE.items():
            for line in do + carry:
                for word in re.findall(r"\b(delete[sd]?|replace[sd]?)\b", line.lower()):
                    self.assertRegex(line.lower(), rf"never (replaced or )?{word}", (fmt, stage, line))


class Faults(Fixture):
    def test_a_fault_outranks_the_numbers_and_is_fixed_today(self):
        v = lc.verdict("aaa", self.checked("mine", views=900, rank=1, of=10, faults=["Visibility is Private"]))
        self.assertEqual(v["level"], "fault")
        self.assertEqual(v["why"][0], "Fault: Visibility is Private")
        self.assertIn("Put the fault right today", v["now"][0])
        self.assertIn("visibility and schedule changes are Ben's", v["now"][0])
        self.assertNotIn("Nothing to fix.", v["now"])

    def test_a_fault_on_a_video_that_is_behind_still_says_which_step(self):
        self.usual_shorts()
        v = lc.verdict("aaa", self.checked("mine", views=4, rank=10, of=10, shown=20, faults=["No Related video"]))
        self.assertEqual((v["level"], v["stage"]), ("fault", "not shown"))


class TheNextMorning(Fixture):
    def test_the_verdict_adds_the_first_mornings_views_once_the_snapshot_has_them(self):
        day = dt.date(2026, 11, 1)
        rows = [(f"v{i}", 400 + 100 * i) for i in range(4)]   # 400, 500, 600 before it; ours is the fourth
        for i in range(len(rows)):
            seen = [video(vid, live=f"{day + dt.timedelta(days=j)}T11:30:00Z", views=views) for j, (vid, views) in enumerate(rows[:i + 1])]
            self.snapshot(f"{day + dt.timedelta(days=i + 1)}T06:40:00Z", seen)
        rec = self.checked("v3", live="2026-11-04T11:30Z", views=90, rank=6, of=10)
        self.assertIn("By the next morning it had 700 views; the 3 before it had 500 (median).", lc.verdict("aaa", rec)["why"])


class OurOwnHistory(Fixture):
    def setUp(self):
        super().setUp()
        self.snapshot("2026-11-01T06:40:00Z", [video("old", live="2026-10-01T11:30:00Z", views=5000),
                                               video("new", privacy="private", live="2026-11-01T11:30:00Z")])
        self.snapshot("2026-11-02T06:40:00Z", [video("old", live="2026-10-01T11:30:00Z", views=5001),
                                               video("new", live="2026-11-01T11:30:05Z", views=820)])
        self.snapshot("2026-11-03T06:40:00Z", [video("new", live="2026-11-01T11:30:05Z", views=830)])

    def test_the_first_snapshot_after_going_live_is_the_first_morning(self):
        by_id = {h["id"]: h for h in lc.history("aaa", "short")}
        self.assertEqual(by_id["new"]["firstMorning"], 820)

    def test_a_video_already_public_when_the_snapshots_began_has_no_first_morning(self):
        by_id = {h["id"]: h for h in lc.history("aaa", "short")}
        self.assertIsNone(by_id["old"]["firstMorning"])

    def test_history_is_per_format(self):
        self.assertEqual(lc.history("aaa", "long"), [])


class WhatIsDifferent(Fixture):
    def setUp(self):
        super().setUp()
        rows = [("a", "Why Is Venus So Hot?", 900, 20), ("b", "Why Is Mars Red?", 800, 21), ("c", "Why Is Pluto Small?", 700, 22),
                ("d", "How Thin Are Saturn's Rings?", 40, 20), ("e", "Saturn's Rings Are Falling", 50, 21),
                ("f", "Are Saturn's Rings Young?", 60, 22)]
        day = dt.date(2026, 11, 1)   # November: London is on GMT, so 11:30Z is 11:30 there
        for i, (vid, title, views, seconds) in enumerate(rows):
            live = f"{day + dt.timedelta(days=i)}T11:30:00Z"
            taken = f"{day + dt.timedelta(days=i + 1)}T06:40:00Z"
            earlier = [video(r[0], live=f"{day + dt.timedelta(days=j)}T11:30:00Z", views=r[2], title=r[1], seconds=r[3])
                       for j, r in enumerate(rows[:i])]
            self.snapshot(taken, earlier + [video(vid, live=live, views=views, title=title, seconds=seconds)])

    def differences(self, title, live="2026-11-10T11:30:00Z", seconds=21, vid="mine"):
        info = {"id": vid, "title": title, "format": "short", "at": lc.studio.parse(live), "seconds": seconds}
        return {d["key"]: d["text"] for d in lc.differences("aaa", info)}

    def test_a_subject_that_was_weak_before_is_named_with_its_numbers(self):
        found = self.differences("What Would Standing on Saturn's Moon Titan Feel Like?")
        self.assertEqual(found["subject-weak"], "\"Saturn\" was in the title of 3 earlier Shorts: they had 50 views by the "
                                                "next morning (median), against 380 for all Shorts.")

    def test_an_opener_that_was_strong_before_is_named_too(self):
        found = self.differences("Why Is Neptune Windy?")
        self.assertIn("The title starts with \"Why\", like 3 earlier Shorts: they had 800 views", found["opener-strong"])

    def test_a_subject_seen_only_twice_is_not_a_pattern(self):
        self.assertEqual(self.differences("Venus Has No Moon"), {})   # "Venus" was in one earlier title, not three

    def test_a_different_slot_and_length_are_noticed(self):
        found = self.differences("Something New", live="2026-11-10T18:00:00Z", seconds=45)
        self.assertEqual(found["slot"], "It went live at 18:00 London; the last 6 Shorts mostly at 11:30.")
        self.assertEqual(found["length"], "It is 45 s long; the last 6 Shorts were 20 to 22 s.")
        self.assertEqual(self.differences("Something New"), {})   # the usual slot and length: nothing to say

    def test_a_second_upload_is_noticed(self):
        self.register({"mine": {"kind": "short", "supersedes": "first-go"}})
        self.assertEqual(self.differences("Something New")["reupload"],
                         "It is a second upload of the same video (it replaced first-go).")

    def test_only_videos_before_this_one_count(self):
        found = self.differences("Why Is Saturn Tilted?", live="2026-11-02T11:30:00Z")   # only "a" is earlier
        self.assertEqual(found, {})


class TheWords(Fixture):
    def test_judge_reads_as_plain_lines(self):
        self.usual_shorts()
        rec = self.checked("mine", title="What Would Standing on Titan Feel Like?", views=4, rank=10, of=10, shown=30)
        text = lc.judge_text("aaa", rec)
        self.assertIn("\"What Would Standing on Titan Feel Like?\" (mine) · Channel A · Short · went live Tue 10 Nov 11:30 London", text)
        self.assertIn("At 6 h: views 4 · Studio rank 10 of 10 · shown in feed 30 · stayed to watch no figure yet · "
                      "average viewed no figure yet", text)
        self.assertIn("Usual for this channel: stayed to watch 32%, average viewed 66%", text)
        est = lc.judge_text("aaa", self.checked("est", views=4, rank=10, of=10, feedViews=2, stayed=25.0))
        self.assertIn("shown in feed about 8 (from 2 feed views) · stayed to watch 25.0%", est)
        self.assertIn("Verdict: BEHIND, not shown", text)
        self.assertIn("Do now", text)
        self.assertIn("Carry forward", text)

    def test_what_was_done_is_shown_under_the_verdict(self):
        rec = self.checked("mine", views=4, rank=10, of=10)
        rec["notes"] = [{"at": "2026-11-10T18:00Z", "by": "chief", "text": "Related video set"}]
        self.assertIn("Done (2026-11-10T18:00Z, chief): Related video set", lc.judge_text("aaa", rec))

    def test_the_report_names_what_three_weak_starts_share(self):
        self.usual_shorts()
        for i in range(3):
            self.checked(f"weak{i}", live=f"2026-11-0{i + 1}T11:30Z", views=5, rank=10, of=10, shown=900, stayed=10.0)
        self.checked("fine", live="2026-11-05T11:30Z", views=600, rank=4, of=10)
        text = lc.report_text()
        self.assertIn("Channel A: 4 checked", text)
        self.assertIn("What the 3 weak starts share", text)
        self.assertIn("- stage: swiped: 3 of 3 weak starts, 0 of 1 others", text)
        self.assertNotIn("Channel B", text)

    def test_the_report_does_not_call_two_a_pattern(self):
        self.usual_shorts()
        for i in range(2):
            self.checked(f"weak{i}", live=f"2026-11-0{i + 1}T11:30Z", views=5, rank=10, of=10, shown=900, stayed=10.0)
        self.assertIn("Nothing is shared by three weak starts yet (2 weak so far).", lc.report_text())

    def test_an_empty_studio_says_so(self):
        self.assertEqual(lc.report_text(), "No video has been checked yet.")


class TheCommands(Fixture):
    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                mock.patch.object(lc.channels, "ROOT", self.root):
            code = lc.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def setUp(self):
        super().setUp()
        self.snapshot("2026-11-10T06:40:00Z", [video("short1", privacy="private", live="2026-11-10T11:30:00Z", title="A Short")])

    def test_record_then_judge_then_note(self):
        code, out, _ = self.run_cli("record", "short1", "--hours", "6", "--views", "4", "--rank", "10", "--of", "10",
                                    "--shown", "30", "--fault", "No Related video", "--by", "gemini")
        self.assertEqual((code, out.strip()), (0, "saved numbers/aaa/launch/short1.json"))
        rec = lc.load_record("aaa", "short1")
        self.assertEqual((rec["title"], rec["readings"][0]["by"], rec["faults"]), ("A Short", "gemini", ["No Related video"]))
        code, out, _ = self.run_cli("judge", "short1")
        self.assertEqual(code, 0)
        self.assertIn("Verdict: FAULT, not shown", out)
        code, _, _ = self.run_cli("note", "short1", "Related video set by J9", "--by", "claude")
        self.assertEqual(code, 0)
        self.assertEqual(lc.load_record("aaa", "short1")["notes"][0]["text"], "Related video set by J9")

    def test_a_rank_needs_its_of(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            lc.main(["record", "short1", "--hours", "6", "--views", "4", "--rank", "10"])

    def test_an_unknown_video_is_refused(self):
        code, _, err = self.run_cli("record", "nope", "--hours", "6", "--views", "4")
        self.assertEqual(code, 1)
        self.assertIn("not in any channel's snapshot or uploads register", err)

    def test_judge_before_any_reading_says_what_to_do(self):
        code, _, err = self.run_cli("judge", "short1")
        self.assertEqual(code, 1)
        self.assertIn("use `record` first", err)


if __name__ == "__main__":
    unittest.main()
