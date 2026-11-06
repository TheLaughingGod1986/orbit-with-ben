#!/usr/bin/env python3
"""Tests for progress24.py."""
import datetime as dt, json, os, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import progress24 as p

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 11, 4, 13, 0, tzinfo=UTC)


def ms(n_done, awaiting=False):
    return [{"id": f"m{i}", "state": "done" if i < n_done else "todo", "awaitingApproval": awaiting and i == n_done - 1}
            for i in range(9)]


def board(videos, done=()):
    return {"tracker": {"videos": [{"key": k, "title": t, "production": {"milestones": m}} for k, t, m in videos]},
            "owb": {"done": list(done)}}


class Counts(unittest.TestCase):
    def test_counts_and_awaiting_approval(self):
        b = board([("OWB:030", "Thirty", ms(5)), ("HOS:008", "Franklin", ms(4, awaiting=True)), ("OWB:099", "None", [])])
        self.assertEqual(p.video_counts(b), {"OWB:030": [5, "Thirty"], "HOS:008": [3, "Franklin"]})


class History(unittest.TestCase):
    def test_samples_every_30_min_and_drops_after_48h(self):
        h = [{"at": "2026-11-02T10:00Z", "counts": {}}, {"at": "2026-11-04T12:45Z", "counts": {}}]
        h = p.record(h, NOW, {"A": [1, "a"]})
        self.assertEqual([x["at"] for x in h], ["2026-11-04T12:45Z"])     # 50 h old dropped; 15 min too soon
        h = p.record(h, NOW + dt.timedelta(minutes=20), {"A": [2, "a"]})
        self.assertEqual(len(h), 2)

    def test_baseline_nearest_24h(self):
        h = [{"at": "2026-11-03T11:00Z"}, {"at": "2026-11-03T12:30Z"}, {"at": "2026-11-03T14:00Z"}]
        self.assertEqual(p.baseline(h, NOW)["at"], "2026-11-03T12:30Z")
        self.assertEqual(p.baseline([{"at": "2026-11-04T09:00Z"}], NOW)["at"], "2026-11-04T09:00Z")


class Summary(unittest.TestCase):
    def test_moved_jobs_and_films(self):
        hist = [{"at": "2026-11-03T12:30Z", "counts": {"OWB:030": 5, "HOS:008": 4, "OWB:032": 1}}]
        counts = {"OWB:030": [7, "Thirty"], "HOS:008": [4, "Franklin"], "OWB:032": [3, "Thirty-two"], "OWB:040": [1, "New"]}
        done = [{"id": "J1", "by": "codex", "film": "OWB:030", "title": "030 picture pass", "at": "2026-11-04T10:00Z"},
                {"id": "J2", "by": "codex", "title": "032 script review", "repo": "owb", "at": "2026-11-04T09:00Z"},
                {"id": "J3", "by": "gemini", "title": "Daily Studio read", "at": "2026-11-04T07:00Z"}]
        s = p.summarise(hist, NOW, counts, done)
        self.assertEqual(s["jobsDone"], 3)
        self.assertEqual(s["byAgent"], {"codex": 2, "gemini": 1})
        self.assertEqual(s["milestones"], 4)
        self.assertEqual([(m["key"], m["from"], m["to"]) for m in s["moved"]], [("OWB:030", 56, 78), ("OWB:032", 11, 33)])
        self.assertEqual({f["film"] for f in s["films"]}, {"OWB:030", "OWB:032"})
        self.assertEqual(s["otherJobs"], 1)
        self.assertEqual(s["videoJobs"], 2)
        self.assertEqual(s["hours"], 24.5)
        # Per-film job lists (Ben, 6 Nov 2026).
        by = {f["film"]: f for f in s["films"]}
        self.assertEqual([j["id"] for j in by["OWB:030"]["items"]], ["J1"])
        self.assertEqual(by["OWB:030"]["status"], "56% → 78%")
        self.assertTrue(by["OWB:030"]["closed"])
        self.assertEqual([j["id"] for j in s["studio"]], ["J3"])

    def test_jobs_done_window(self):
        b = board([], done=[{"id": "J1", "at": "2026-11-04T10:00Z"}, {"id": "J2", "at": "2026-11-03T10:00Z"},
                            {"id": "J1", "at": "2026-11-04T10:00Z"}])
        self.assertEqual([j["id"] for j in p.jobs_done(b, NOW)], ["J1"])

    def test_section_writes_history_and_survives_bad_file(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "h.json"; f.write_text("not json")
            s = p.section(f, board([("OWB:030", "T", ms(2))]), NOW)
            self.assertEqual(s["jobsDone"], 0)
            self.assertEqual(json.loads(f.read_text())[0]["counts"], {"OWB:030": 2})

    def test_schema_correction_is_not_new_production_and_preserves_history(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'h.json'
            old = {'at': '2026-11-03T13:00Z', 'counts': {'HOS:009': 3}}
            f.write_text(json.dumps([old]))
            b = board([('HOS:009', 'Moon', ms(4))], done=[{'id': 'Jreal', 'at': '2026-11-04T12:00Z'}])
            b['tracker']['videos'][0]['production']['milestoneSchema'] = 'studio-nine-stages-hos-aliases-v2'
            s = p.section(f, b, NOW)
            self.assertEqual((s['milestones'], s['moved'], s['hours'], s['jobsDone']), (0, [], 0, 1))
            self.assertEqual(json.loads(f.read_text())[0], old, 'old history is retained unmodified')
            # An actual later completion on the same basis still counts.
            b['tracker']['videos'][0]['production']['milestones'] = ms(5)
            s = p.section(f, b, NOW + dt.timedelta(minutes=31))
            self.assertEqual(s['milestones'], 1)
            self.assertEqual((s['moved'][0]['from'], s['moved'][0]['to']), (44, 56))

    def test_legacy_producer_does_not_compare_against_new_schema_on_rollback(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'h.json'
            f.write_text(json.dumps([{'at': '2026-11-03T13:00Z', 'counts': {'HOS:009': 4}, 'basis': 'v2'}]))
            s = p.section(f, board([('HOS:009', 'Moon', ms(3))]), NOW)
            self.assertEqual((s['milestones'], s['moved'], s['hours']), (0, [], 0))

    def test_title_attribution_open_jobs_and_moved_without_films(self):
        # 031/032 closed a stage; 033 had jobs but stayed at 4/9 (picture still open).
        hist = [{"at": "2026-11-03T12:30Z", "counts": {"OWB:031": 5, "OWB:032": 5, "OWB:033": 4}}]
        counts = {
            "OWB:031": [6, "What Happens When Earths Magnetic Field Flips"],
            "OWB:032": [6, "What Would Happen If You Landed On Titan"],
            "OWB:033": [4, "Why Knocked-Sideways Uranus Has 21-Year Winters"],
        }
        done = [
            {"id": "J033", "by": "chief", "title": "Chief: resolve 033 picture orphan-review", "at": "2026-11-04T10:00Z"},
            {"id": "J032", "by": "codex", "title": "Titan Short v11 cover", "at": "2026-11-04T09:00Z"},
            {"id": "Jhouse", "by": "gemini", "title": "Daily analytics capture", "at": "2026-11-04T08:00Z"},
        ]
        open_jobs = [
            {"id": "J2141", "status": "claimed", "by": "cursor", "film": "OWB:032", "stage": "picture",
             "title": "032 picture harvest", "progress": {"step": 1, "of": 3}},
        ]
        stages = {"OWB:031": "edit", "OWB:032": "picture", "OWB:033": "picture"}
        s = p.summarise(hist, NOW, counts, done, open_jobs=open_jobs, stages=stages)
        by = {f["film"]: f for f in s["films"]}
        # 031 moved a stage but had no attributed jobs — still gets a card.
        self.assertIn("OWB:031", by)
        self.assertEqual(by["OWB:031"]["status"], "56% → 67%")
        self.assertEqual(by["OWB:031"]["items"], [])
        # Bare 033 in the title + Titan title match.
        self.assertEqual([j["id"] for j in by["OWB:033"]["items"]], ["J033"])
        self.assertIn("no stage closed", by["OWB:033"]["status"])
        self.assertIn("picture", by["OWB:033"]["status"])
        self.assertEqual({j["id"] for j in by["OWB:032"]["items"]}, {"J032", "J2141"})
        live = next(j for j in by["OWB:032"]["items"] if j["id"] == "J2141")
        self.assertEqual(live["status"], "claimed")
        self.assertEqual(live["progress"], {"step": 1, "of": 3})
        self.assertEqual([j["id"] for j in s["studio"]], ["Jhouse"])
        self.assertEqual(s["videoJobs"], 2)  # finished jobs on 032 + 033
        self.assertEqual(s["otherJobs"], 1)

    def test_film_of_mid_title_number_and_title_match(self):
        titles = {"OWB:032": "What Would Happen If You Landed On Titan",
                  "OWB:033": "Why Knocked-Sideways Uranus Has 21-Year Winters"}
        self.assertEqual(p.film_of({"title": "Chief: resolve 033 picture orphan-review"}, titles), "OWB:033")
        self.assertEqual(p.film_of({"title": "Titan Short v11 cover"}, titles), "OWB:032")
        self.assertEqual(p.film_of({"title": "Daily analytics capture"}, titles), "")
        # Bare numbers only count when that film is known — PR #180 must not invent a film card.
        self.assertEqual(p.film_of({"title": "HOS #180 comment"}, titles), "")
        self.assertEqual(p.film_of({"title": "Follow up on PR 180 review notes"}, titles), "")
        self.assertEqual(p.film_of({"title": "Chief: resolve 033 picture orphan-review"}, {}), "")

    def test_remaining_today_yesterday_leftover_and_glance(self):
        # London calendar: NOW is Wed 4 Nov 2026 13:00 UTC = 13:00 GMT.
        hist = [{"at": "2026-11-03T12:30Z", "counts": {"OWB:032": 5}}]
        counts = {"OWB:032": [6, "What Would Happen If You Landed On Titan"]}
        done_24h = [
            {"id": "J2110", "by": "codex", "film": "OWB:032", "title": "Titan Short v11 cover",
             "stage": "thumbs", "at": "2026-11-04T10:00Z"},
        ]
        all_done = done_24h + [
            {"id": "J2109", "by": "codex", "film": "OWB:032", "title": "032 spectrum stills review",
             "stage": "picture", "at": "2026-11-03T18:00Z"},
            {"id": "J2001", "by": "gemini", "film": "OWB:032", "title": "032 older picture pass",
             "stage": "picture", "at": "2026-11-01T12:00Z"},
            {"id": "Jhouse", "by": "gemini", "title": "Daily analytics capture", "at": "2026-11-04T08:00Z"},
        ]
        open_jobs = [
            {"id": "J2141", "status": "claimed", "by": "cursor", "film": "OWB:032", "stage": "picture",
             "title": "032 picture harvest", "progress": {"step": 1, "of": 3}},
            {"id": "J2142", "status": "blocked", "by": "codex", "film": "OWB:032", "stage": "edit",
             "title": "032 Shorts edit held", "after": "J2141"},
            {"id": "J2143", "status": "open", "by": "cursor", "film": "OWB:032", "stage": "edit",
             "title": "032 edit waits on picture", "after": "J2141"},
        ]
        milestones = {
            "OWB:032": [
                {"id": "topic", "state": "done"}, {"id": "script", "state": "done"},
                {"id": "sources", "state": "done"}, {"id": "vo", "state": "done"},
                {"id": "shots", "state": "done"}, {"id": "picture", "state": "doing"},
                {"id": "edit", "state": "todo"}, {"id": "thumbs", "state": "done"},
                {"id": "qa", "state": "todo"},
            ],
        }
        next_live = [
            {"key": "OWB:025", "title": "Could a Robot Survive on Mars?", "at": "2026-11-08T18:00:00.000Z",
             "atLondon": "Sun 8 Nov 2026 18:00 GMT", "type": "long"},
            {"key": "HOS:007", "title": "Why Vaccines Are Named After a Cow", "at": "2026-11-12T18:00:00Z",
             "atLondon": "Thu 12 Nov 2026 18:00 GMT", "type": "long"},
        ]
        s = p.summarise(
            hist, NOW, counts, done_24h,
            open_jobs=open_jobs, stages={"OWB:032": "picture"},
            all_done=all_done, milestones=milestones, next_live=next_live,
        )
        film = s["films"][0]
        self.assertEqual(film["film"], "OWB:032")
        self.assertEqual(film["doneToday"], 1)
        # Remaining jobs + leftover qa (edit is covered by open jobs) → left=4.
        self.assertEqual(film["left"], 4)
        self.assertEqual(film["blocked"], 2)  # J2142 blocked + J2143 waiting on J2141
        self.assertEqual(film["earlierDone"], 1)  # J2001 older than yesterday
        self.assertIn("6 of 9 stages", film["pctReason"])
        self.assertIn("picture still open", film["pctReason"])
        ids = [it.get("id") or it.get("stage") for it in film["items"]]
        self.assertEqual(ids[:3], ["J2141", "J2142", "J2143"])
        self.assertIn("qa", ids)
        self.assertNotIn("edit", ids)  # covered by remaining jobs — no invented stage row
        today = next(it for it in film["items"] if it.get("id") == "J2110")
        yday = next(it for it in film["items"] if it.get("id") == "J2109")
        self.assertEqual(today["when"], "today")
        self.assertEqual(yday["when"], "yesterday")
        qa = next(it for it in film["items"] if it.get("kind") == "stage")
        self.assertEqual(qa["stage"], "qa")
        self.assertNotIn("id", qa)
        self.assertEqual(qa["title"], "Chief QA — not started")
        g = s["glance"]
        self.assertEqual(g["doneToday"], 2)  # J2110 + Jhouse on London today
        self.assertEqual(g["left"], 4)
        self.assertEqual(g["blocked"], 2)
        self.assertEqual({j["id"] for j in g["blockedJobs"]}, {"J2142", "J2143"})
        self.assertEqual([v["key"] for v in g["nextLive"]], ["OWB:025", "HOS:007"])

    def test_next_going_live_from_scheduled_publish(self):
        b = {
            "tracker": {"videos": [
                {"key": "OWB:024", "title": "Past", "type": "long",
                 "youtube": {"state": "live", "privacy": "public", "publishAt": "2026-11-01T18:00:00Z"}},
                {"key": "OWB:025", "title": "Could a Robot Survive on Mars?", "type": "long",
                 "youtube": {"state": "scheduled", "publishAt": "2026-11-08T18:00:00.000Z",
                             "publishAtLondon": "Sun 8 Nov 2026 18:00 GMT"}},
                {"key": "OWB:025:S:a", "title": "Mars Night Short", "type": "short",
                 "youtube": {"state": "scheduled", "publishAt": "2026-11-09T11:30:00.000Z",
                             "publishAtLondon": "Mon 9 Nov 2026 11:30 GMT"}},
                {"key": "OWB:025:S:b", "title": "Rover Short", "type": "short",
                 "youtube": {"state": "scheduled", "publishAt": "2026-11-11T11:30:00.000Z"}},
                {"key": "HOS:007", "title": "Why Vaccines Are Named After a Cow", "type": "long",
                 "youtube": {"state": "scheduled", "publishAt": "2026-11-12T18:00:00Z",
                             "publishAtLondon": "Thu 12 Nov 2026 18:00 GMT"}},
                {"key": "OWB:026", "title": "Later", "type": "long",
                 "youtube": {"state": "scheduled", "publishAt": "2026-11-15T18:00:00Z"}},
                {"key": "OWB:099", "title": "No date", "type": "long",
                 "youtube": {"state": "scheduled"}},
            ]},
            "owb": {"done": [], "jobs": []},
        }
        rows = p.next_going_live(b, NOW, n=4)
        self.assertEqual([r["key"] for r in rows],
                         ["OWB:025", "OWB:025:S:a", "OWB:025:S:b", "HOS:007"])
        self.assertEqual(rows[0]["title"], "Could a Robot Survive on Mars?")
        self.assertEqual(rows[0]["atLondon"], "Sun 8 Nov 2026 18:00 GMT")
        # Never invent a fifth from nowhere — Later is 5th and stays out.
        self.assertNotIn("OWB:026", {r["key"] for r in rows})
        self.assertNotIn("OWB:099", {r["key"] for r in rows})

    def test_leftover_stages_skip_complete_and_covered(self):
        ms = [
            {"id": "picture", "state": "doing"},
            {"id": "edit", "state": "todo"},
            {"id": "qa", "state": "todo"},
            {"id": "thumbs", "state": "done"},
        ]
        remaining = [{"id": "J1", "stage": "picture", "status": "claimed", "title": "pic"}]
        left = p.leftover_stages(ms, remaining)
        self.assertEqual([x["stage"] for x in left], ["edit", "qa"])
        self.assertTrue(all("id" not in x and x["kind"] == "stage" for x in left))


if __name__ == "__main__":
    unittest.main(verbosity=1)
