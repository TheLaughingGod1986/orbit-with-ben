#!/usr/bin/env python3
"""The plan block (scripts/plan_board.py): dates, job ids, stands, the 14-day verdict, missing figures, a quiet publish."""
import datetime as dt
import json
import pathlib
import unittest

import plan_board

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOW = dt.datetime(2026, 11, 14, 23, 0, tzinfo=dt.timezone.utc)
PUBLISHED = "2026-12-08T18:00:00Z"


def job(job_id, status="open", kind="studio", **extra):
    row = {"id": job_id, "status": status, "kind": kind, "title": job_id, "remaining_action": ""}
    row.update(extra)
    return row


def video(key, **youtube):
    return {"key": key, "number": key.split(":")[-1], "jobs": [], "youtube": youtube or None}


def every_job(plans, overrides=()):
    """A queue holding every job the plans name, with the given jobs' states."""
    given = {item["id"]: item for item in overrides}
    names = [job_id for plan in plans for step in plan.get("steps") or [] for job_id in step.get("jobs") or []]
    return list(given.values()) + [job(job_id) for job_id in dict.fromkeys(names) if job_id not in given]


class PlanBoardTest(unittest.TestCase):
    def test_real_plan_jobs_exist_and_dates_parse(self):
        plans = json.loads((ROOT / "studio" / "plan.json").read_text())
        queue = json.loads((ROOT / "jobs" / "queue.json").read_text())
        plan_board.validate(plans, {row["id"] for row in queue["jobs"]})
        block = plan_board.section(plans, queue["jobs"], [], None, "2026-11-14T23:00:00Z", now=NOW)
        card = block["plans"][0]["card"]
        self.assertEqual(card["title"], "Plan: getting our long videos seen")
        self.assertEqual(card["next"], "Next: Journey film, Tue 8 Dec")
        # Ben locked the every-planet film on 17 Nov, so the plan asks him for nothing.
        self.assertEqual(card["needs"], "")
        self.assertEqual(card["score"], "No test film is public yet. Best long so far: 230 views")
        self.assertEqual(block["plans"][0]["baseline"]["showings"],
                         "All 16 longs: about 4,050 showings (read 12 Nov)")
        texts = [row["text"] for row in block["plans"][0]["decisions"]]
        self.assertTrue(texts[0].startswith("Lock the every-planet film"))
        self.assertTrue(texts[1].startswith("Pause"))
        self.assertTrue(texts[-1].startswith("Titles"))
        jan = block["plans"][1]
        self.assertEqual(jan["id"], "orbit-search-2027-01")
        self.assertEqual(jan["channel"], "owb")
        self.assertEqual(jan["card"]["title"], "Plan: orbit from January: films people search for")
        self.assertEqual(jan["card"]["next"], "Next: First weekly search research, Mon 7 Dec")
        self.assertEqual(jan["card"]["needs"], "")
        self.assertEqual(jan["card"]["score"], "No test film is public yet. Best long so far: 230 views")
        self.assertEqual(len(jan["steps"]), 6)
        self.assertEqual(jan["baseline"]["showings"],
                         "All 16 longs: about 4,050 showings (read 12 Nov)")
        ww2 = block["plans"][2]
        self.assertEqual(ww2["id"], "ww2-launch-2026-11")
        self.assertEqual(ww2["card"]["title"], "Plan: starting our WW2 documentary channel")
        # Ben, 17 Nov 2026: on this channel he is asked only to watch finished films, so its plan asks him for nothing.
        self.assertEqual(ww2["card"]["needs"], "")
        self.assertEqual(len(ww2["steps"]), 12)
        self.assertFalse(any(s["needsYou"] for s in ww2["steps"]))
        self.assertEqual(ww2["card"]["score"], "No film is public yet.")
        self.assertEqual(ww2["baseline"]["best"], "No long film yet")

    def test_stands_from_jobs_and_the_tracker(self):
        plans = json.loads((ROOT / "studio" / "plan.json").read_text())
        jobs = [
            job("J2859", "done", "listing"),
            job("J2857", "open", "studio"),
            job("J2860", "claimed", "studio", progress={"step": 1, "of": 5},
                title="Repair the sleep opening", remaining_action="Repair the first minute"),
            job("J2861", "open", "listing"),
            job("J2863", "done", "review"),
            job("J2864", "open", "studio"),
            job("J2989", "done", "studio"),
        ]
        jobs = every_job(plans, jobs)
        videos = [
            {"key": "OWB:064", "jobs": [{"id": "J2863"}], "youtube": {}},
        ]
        block = plan_board.section(plans, jobs, videos, None, "2026-11-14T23:00:00Z", now=NOW)
        stands = {step["id"]: step["stand"] for step in block["plans"][0]["steps"]}
        self.assertEqual(stands["journey"], "Listing ready")
        self.assertEqual(stands["sleep"], "Being repaired, step 1 of 5")
        self.assertEqual(stands["planets"], "Waiting its turn")
        self.assertEqual(stands["pause"], "Waiting its turn")
        planets = next(step for step in block["plans"][0]["steps"] if step["id"] == "planets")
        self.assertFalse(planets["needsYou"])
        self.assertEqual(planets["videoKey"], "OWB:064")
        # A step that still needs Ben's lock, with no date yet, says so and counts on the card.
        waiting = json.loads(json.dumps(plans))
        step = next(step for step in waiting[0]["steps"] if step["id"] == "planets")
        step["needsBen"], step["when"] = "Lock or decline this film on its card", ""
        block = plan_board.section(waiting, jobs, videos, None, "2026-11-14T23:00:00Z", now=NOW)
        planets = next(step for step in block["plans"][0]["steps"] if step["id"] == "planets")
        self.assertEqual(planets["stand"], "Waiting for your lock")
        self.assertTrue(planets["needsYou"])
        self.assertEqual(block["plans"][0]["card"]["needs"], "1 thing needs you: lock the every-planet film")

    def test_youtube_states_and_the_fourteen_day_verdict(self):
        step = {
            "id": "journey", "name": "Journey film (58 minutes)", "what": "A calm film.",
            "when": "2026-12-08T18:00Z", "film": "J01", "jobs": ["J2857"],
            "test": {"days": 14, "keep": 500, "drop": 230},
        }
        plan = {"id": "t", "title": "Getting our long videos seen", "agreed": "2026-11-14",
                "goal": "Long videos to thousands of views each.", "why": ["Because."],
                "baseline": {"bestLongViews": 230, "longShowingsTotal": 4050, "longs": 16, "readAt": "2026-11-12"},
                "steps": [step], "decisions": []}
        jobs = [job("J2857", "done", "studio")]

        def row(state, privacy, views, extra=None, day_shift=5):
            now = dt.datetime(2026, 12, 8, 18, 0, tzinfo=dt.timezone.utc) + dt.timedelta(days=day_shift)
            analytics = {"channels": [{"videos": [{"id": "aaaaaaaaaaa", "views": views, **(extra or {})}]}]}
            videos = [video("OWB:J01", state=state, privacy=privacy, publishAt=PUBLISHED, videoId="aaaaaaaaaaa")]
            block = plan_board.section([plan], jobs, videos, analytics, "2026-12-14T18:00:00Z", now=now)
            return block["plans"][0]

        early = row("live", "public", 120, {}, day_shift=5)
        self.assertEqual(early["steps"][0]["stand"], "Live, day 6 of 14")
        result = early["results"][0]
        self.assertEqual(result["verdict"], "reading on")
        self.assertEqual(result["until"], "Mon 21 Dec")
        self.assertEqual(result["showings"], "no figure yet")
        self.assertEqual(result["clickRate"], "no figure yet")
        self.assertEqual(result["share"], "no figure yet")
        self.assertNotIn("0", result["showings"])

        later = row("live", "public", 500, {"impressions": 900, "impressionsCtr": 1.96, "studioAvgViewPct": 25.2}, day_shift=13)
        self.assertEqual(later["results"][0]["verdict"], "Keep")
        self.assertEqual(later["results"][0]["showings"], "900")
        self.assertEqual(later["results"][0]["clickRate"], "1.96%")
        self.assertEqual(later["results"][0]["share"], "25.2%")
        self.assertEqual(row("live", "public", 230, {}, day_shift=13)["results"][0]["verdict"], "One more")
        self.assertEqual(row("live", "public", 499, {}, day_shift=13)["results"][0]["verdict"], "One more")
        self.assertEqual(row("live", "public", 229, {}, day_shift=13)["results"][0]["verdict"], "Drop or change")
        self.assertIn("500 views", row("live", "public", 500, {}, day_shift=13)["card"]["score"])

        scheduled = plan_board.section(
            [plan], jobs, [video("OWB:J01", state="scheduled", privacy="private", publishAt="2026-12-08T18:00Z", videoId="aaaaaaaaaaa")],
            None, "t", now=NOW)["plans"][0]
        self.assertEqual(scheduled["steps"][0]["stand"], "Scheduled")
        self.assertEqual(scheduled["results"], [])
        private = plan_board.section(
            [plan], jobs, [video("OWB:J01", state="uploaded", privacy="private", videoId="aaaaaaaaaaa")],
            None, "t", now=NOW)["plans"][0]
        self.assertEqual(private["steps"][0]["stand"], "Uploaded, private")

    def test_a_quiet_publish_keeps_the_same_block(self):
        plans = json.loads((ROOT / "studio" / "plan.json").read_text())
        jobs = every_job(plans)
        first = plan_board.section(plans, jobs, [], None, "2026-11-14T23:00:00Z", now=NOW)
        second = plan_board.section(plans, jobs, [], None, "2026-11-14T23:05:00Z", previous=first, now=NOW)
        self.assertEqual(first, second)
        self.assertEqual(second["updatedAt"], "2026-11-14T23:00:00Z")
        moved = plan_board.section(plans, [dict(job, status="claimed", progress={"step": 2, "of": 4}) for job in jobs],
                                   [], None, "2026-11-14T23:05:00Z", previous=first, now=NOW)
        self.assertNotEqual(moved["updatedAt"], first["updatedAt"])

    def test_a_second_plan_needs_no_new_code(self):
        plans = json.loads((ROOT / "studio" / "plan.json").read_text())
        other = json.loads(json.dumps(plans[0]))
        other["id"] = "later"
        other["title"] = "A second plan"
        jobs = every_job([plans[0], other])
        block = plan_board.section([plans[0], other], jobs, [], None, "2026-11-14T23:00:00Z", now=NOW)
        self.assertEqual([plan["card"]["title"] for plan in block["plans"]],
                         ["Plan: getting our long videos seen", "Plan: a second plan"])

    def test_a_missing_job_or_a_bad_date_is_an_error(self):
        plans = json.loads((ROOT / "studio" / "plan.json").read_text())
        with self.assertRaises(plan_board.PlanError):
            plan_board.validate(plans, set())
        broken = json.loads(json.dumps(plans))
        broken[0]["steps"][0]["when"] = "next tuesday"
        with self.assertRaises(plan_board.PlanError):
            plan_board.validate(broken, {item["id"] for item in every_job(plans)})


if __name__ == "__main__":
    unittest.main()
