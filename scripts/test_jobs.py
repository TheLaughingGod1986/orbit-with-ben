"""jobs.py: any able agent claims the oldest job it can do; stalled claims are taken over; the board follows."""
import datetime as dt, json, pathlib, sys, tempfile, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs  # noqa: E402
import studio  # noqa: E402

T0 = dt.datetime(2026, 10, 7, 12, 0, tzinfo=dt.timezone.utc)
MIN = dt.timedelta(minutes=1)


def queue(*specs):
    d = {"next_id": 1, "jobs": []}
    for needs, title, kw in specs:
        jobs.do_add(d, title=title, needs=needs, body="", by="claude", at=T0, **kw)
    return d


class Next(unittest.TestCase):
    def test_takes_the_oldest_job_it_can_do(self):
        d = queue(("cloud", "review", {}), ("mini", "cut", {}), ("mini", "thumbs", {}))
        j = jobs.do_next(d, "cursor", {"mini", "any"}, T0)
        self.assertEqual((j["id"], j["status"], j["by"]), ("J0002", "claimed", "cursor"))
        self.assertEqual(j["eta"], "2026-10-07T14:00Z")  # default 120 min

    def test_whoever_is_up_gets_the_job_not_whoever_was_meant_to(self):
        d = queue(("mini", "cut", {}))
        self.assertIsNone(jobs.do_next(d, "claude", {"cloud", "any"}, T0))  # Claude can't do Mini work
        self.assertEqual(jobs.do_next(d, "cursor", {"mini"}, T0)["by"], "cursor")  # Grok is down; Cursor takes it

    def test_a_live_claim_is_not_taken_but_a_stalled_one_is(self):
        d = queue(("mini", "cut", {"eta_min": 30}))
        jobs.do_next(d, "chief", {"mini"}, T0)
        self.assertIsNone(jobs.do_next(d, "cursor", {"mini"}, T0 + 10 * MIN))
        j = jobs.do_next(d, "cursor", {"mini"}, T0 + 31 * MIN)
        self.assertEqual(j["by"], "cursor")
        self.assertIn("took over a stalled claim by chief", j["history"][-1]["what"])

    def test_quick_jobs_go_before_a_long_released_one(self):
        d = queue(("mini", "first cut", {"eta_min": 720}), ("mini", "pickup", {"eta_min": 30}))
        j = jobs.do_next(d, "cursor", {"mini"}, T0)
        self.assertEqual(j["title"], "pickup")
        jobs.do_done(j, "cursor", "ok", T0)
        self.assertEqual(jobs.do_next(d, "cursor", {"mini"}, T0)["title"], "first cut")

    def test_the_focus_films_jobs_go_first(self):
        d = queue(("mini", "disk move", {"eta_min": 30}), ("mini", "025 rough v02", {"film": "025", "stage": "edit", "eta_min": 240}),
                  ("mini", "022 covers", {"film": "022", "stage": "thumbs", "eta_min": 30}))
        d["focus"] = ["025"]
        self.assertEqual(jobs.do_next(d, "cursor", {"mini"}, T0)["title"], "025 rough v02")  # long, but the focus film
        self.assertEqual(jobs.order({"id": "J9", "film": "022", "eta_min": 30}, ["025"])[0], 1)
        jobs.do_done(d["jobs"][1], "cursor", "ok", T0)
        self.assertEqual(jobs.do_next(d, "cursor", {"mini"}, T0)["title"], "022 covers")  # a film's job before admin

    def test_a_job_for_one_agent_is_only_that_agents(self):
        d = queue(("any", "ideas from Codex", {}), ("mini", "cut", {}))
        jobs.find(d, "J0001")["for"] = "codex"
        self.assertEqual(jobs.do_next(d, "cursor", {"mini", "any"}, T0)["id"], "J0002")
        jobs.find(d, "J0002")["status"] = "open"; jobs.find(d, "J0002")["by"] = ""
        jobs.find(d, "J0002")["urgent"] = True
        self.assertEqual(jobs.do_next(d, "codex", {"mini", "any"}, T0)["id"], "J0001")  # its own job before an urgent one

    def test_urgent_jobs_run_in_the_order_named(self):
        d = queue(*[("mini", f"j{i}", {"film": "026", "stage": "edit"} if i == 2 else {}) for i in range(1, 6)])
        d["focus"] = ["026"]
        jobs.find(d, "J0004")["urgent"] = True  # an older plain true stays ahead of newly named ones
        self.assertEqual(jobs.do_urgent(d, [jobs.find(d, "J0003"), jobs.find(d, "J0001")]), ["J0004", "J0003", "J0001"])
        self.assertEqual(jobs.do_urgent(d, [jobs.find(d, "J0004")]), ["J0003", "J0001", "J0004"])  # re-named: moves back
        got = []
        for _ in range(5):
            j = jobs.do_next(d, "cursor", {"mini"}, T0)
            got.append(j["id"])
            jobs.do_done(j, "cursor", "ok", T0)
        self.assertEqual(got, ["J0003", "J0001", "J0004", "J0002", "J0005"])  # urgent by rank, then the focus film
        self.assertEqual(jobs.do_urgent(d, [jobs.find(d, "J0001")], off=True), [])  # all done: none live

    def test_an_urgent_job_goes_ahead_of_the_focus_film(self):
        d = queue(("mini", "025 rough v02", {"film": "025", "stage": "edit", "eta_min": 240}), ("mini", "disk move", {"eta_min": 240}))
        d["focus"] = ["025"]
        jobs.find(d, "J0002")["urgent"] = True
        self.assertEqual(jobs.do_next(d, "cursor", {"mini"}, T0)["title"], "disk move")

    def test_watch_flags_a_quiet_mini_and_what_waits_on_ben(self):
        d = queue(("mini", "cut", {}), ("ben", "sign in", {}))
        self.assertTrue(jobs.do_watch(d, T0 + 4 * 60 * MIN)["quiet"])  # Mini work waiting, nobody touched it for 4 h
        self.assertEqual([b["id"] for b in jobs.do_watch(d, T0)["ben"]], ["J0002"])
        j = jobs.do_next(d, "cursor", {"mini"}, T0 + 4 * 60 * MIN)
        self.assertFalse(jobs.do_watch(d, T0 + 5 * 60 * MIN)["quiet"])  # a live claim: someone is on it
        jobs.do_release(j, "cursor", "stopping point", T0 + 5 * 60 * MIN)
        self.assertFalse(jobs.do_watch(d, T0 + 6 * 60 * MIN)["quiet"])  # touched an hour ago
        self.assertTrue(jobs.do_watch(d, T0 + 9 * 60 * MIN)["quiet"])

    def test_finish_what_you_hold_first(self):
        d = queue(("mini", "a", {}), ("mini", "b", {}))
        jobs.do_next(d, "cursor", {"mini"}, T0)
        self.assertEqual(jobs.do_next(d, "cursor", {"mini"}, T0 + MIN)["id"], "J0001")

    def test_after_waits_for_the_other_job(self):
        d = queue(("mini", "cut", {}), ("cloud", "review the cut", {"after": "J0001"}))
        self.assertIsNone(jobs.do_next(d, "claude", {"cloud"}, T0))
        jobs.do_next(d, "cursor", {"mini"}, T0)
        jobs.do_done(jobs.find(d, "J0001"), "cursor", "cut up", T0 + MIN)
        self.assertEqual(jobs.do_next(d, "claude", {"cloud"}, T0 + 2 * MIN)["id"], "J0002")


class Lifecycle(unittest.TestCase):
    def test_only_the_holder_can_finish_and_release_reopens(self):
        d = queue(("mini", "cut", {}))
        j = jobs.do_next(d, "cursor", {"mini"}, T0)
        with self.assertRaises(ValueError):
            jobs.do_done(j, "chief", "x", T0)
        jobs.do_release(j, "cursor", "stopping point", T0 + MIN)
        self.assertEqual((j["status"], j["by"]), ("open", ""))
        self.assertEqual(jobs.do_next(d, "chief", {"mini"}, T0 + 2 * MIN)["by"], "chief")

    def test_blocked_jobs_wait_for_reopen(self):
        d = queue(("mini", "cut", {}))
        j = jobs.do_next(d, "cursor", {"mini"}, T0)
        jobs.do_block(j, "cursor", "needs Ben: credit", T0)
        self.assertIsNone(jobs.do_next(d, "chief", {"mini"}, T0 + MIN))
        jobs.do_reopen(j, "claude", "credit topped by Ben", T0 + 2 * MIN)
        self.assertEqual(jobs.do_next(d, "chief", {"mini"}, T0 + 3 * MIN)["id"], "J0001")

    def test_bad_input_is_refused(self):
        d = queue()
        with self.assertRaises(ValueError):
            jobs.do_add(d, title="x", needs="robot", body="", by="claude", at=T0)
        with self.assertRaises(ValueError):
            jobs.do_add(d, title="x", needs="mini", body="", by="claude", at=T0, film="022")

    def test_render_shows_stalled_and_live_jobs_only(self):
        d = queue(("mini", "cut", {"eta_min": 10}), ("cloud", "old", {}))
        jobs.do_next(d, "cursor", {"mini"}, T0)
        jobs.do_cancel(jobs.find(d, "J0002"), "claude", "", T0)
        md = jobs.render(d, T0 + 20 * MIN)
        self.assertIn("| J0001 | mini | **stalled** | cursor |", md)
        self.assertNotIn("| J0002 |", md)


class BoardLink(unittest.TestCase):
    def test_a_film_job_claims_and_releases_its_board_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            films = pathlib.Path(tmp)
            (films / "022_Sun").mkdir()
            old = studio.FILMS
            studio.FILMS = films
            try:
                d = queue(("mini", "first cut", {"film": "022", "stage": "edit"}))
                j = jobs.do_next(d, "cursor", {"mini"}, T0)
                self.assertIsNone(jobs.board_claim(j, "cursor", T0))
                st = json.loads((films / "022_Sun" / "status.json").read_text())
                self.assertEqual(st["claims"][0]["by"], "cursor")
                self.assertIn("J0001", st["claims"][0]["note"])
                jobs.do_done(j, "cursor", "up", T0 + MIN)
                jobs.board_release(j, "cursor", "review")
                st = json.loads((films / "022_Sun" / "status.json").read_text())
                self.assertEqual((st["claims"], st["stages"]["edit"]["state"]), ([], "review"))
            finally:
                studio.FILMS = old


class Progress(unittest.TestCase):
    """Ben, 11 Oct 22:09: % done on the board comes from `jobs.py progress <id> --step k --of n`."""

    def test_records_steps_and_logs_them(self):
        d = queue(("mini", "027 fixes", {}))
        j = jobs.do_next(d, "cursor", {"mini"}, T0)
        jobs.do_progress(j, "cursor", 3, 8, T0 + 10 * MIN, note="grade done")
        self.assertEqual(j["progress"], {"step": 3, "of": 8, "at": "2026-10-07T12:10Z", "by": "cursor", "note": "grade done"})
        self.assertEqual(j["history"][-1]["what"], "step 3 of 8 done: grade done")

    def test_kept_across_a_release_and_cleared_on_reopen(self):
        d = queue(("mini", "027 fixes", {}))
        j = jobs.do_next(d, "cursor", {"mini"}, T0)
        jobs.do_progress(j, "cursor", 1, 4, T0 + MIN)
        jobs.do_release(j, "cursor", "stopping point", T0 + 2 * MIN)
        self.assertEqual(j["progress"]["step"], 1)
        jobs.do_progress(j, "cursor", 2, 4, T0 + 3 * MIN)   # between steps, the job is open: still allowed
        self.assertEqual(j["progress"]["step"], 2)
        j2 = jobs.do_next(d, "chief", {"mini"}, T0 + 4 * MIN)
        jobs.do_done(j2, "chief", "ok", T0 + 5 * MIN)
        jobs.do_reopen(j2, "claude", "again", T0 + 6 * MIN)
        self.assertNotIn("progress", j2)

    def test_rejects_bad_steps_and_someone_elses_claim(self):
        d = queue(("mini", "027 fixes", {}))
        j = jobs.do_next(d, "cursor", {"mini"}, T0)
        for step, of in ((5, 4), (-1, 4), (0, 0)):
            with self.assertRaises(ValueError):
                jobs.do_progress(j, "cursor", step, of, T0)
        with self.assertRaises(ValueError):
            jobs.do_progress(j, "chief", 1, 4, T0)
        with self.assertRaises(ValueError):
            jobs.do_progress(j, "", 1, 4, T0)
        jobs.do_done(j, "cursor", "ok", T0)
        with self.assertRaises(ValueError):
            jobs.do_progress(j, "cursor", 4, 4, T0)

    def test_cli_progress(self):
        d = queue(("mini", "027 fixes", {}))
        jobs.do_next(d, "cursor", {"mini"}, T0)
        saved = []
        with tempfile.TemporaryDirectory() as tmp:
            old = (jobs.load, jobs.save, jobs.JOBS_MD, jobs.publish_board, jobs.heartbeat)
            jobs.load, jobs.save = (lambda *a: d), (lambda data, *a: saved.append(data))
            jobs.JOBS_MD, jobs.publish_board, jobs.heartbeat = pathlib.Path(tmp) / "JOBS.md", (lambda: None), (lambda a: None)
            try:
                rc = jobs.main(["progress", "J0001", "--agent", "cursor", "--step", "2", "--of", "5"])
            finally:
                jobs.load, jobs.save, jobs.JOBS_MD, jobs.publish_board, jobs.heartbeat = old
        self.assertEqual(rc, 0)
        self.assertEqual(saved[0]["jobs"][0]["progress"]["step"], 2)


class NotBefore(unittest.TestCase):
    """--not-before (Chief, 12 Oct 2026): London time in, UTC stored; nobody is handed the job early, relay included."""
    def test_london_time_is_stored_as_utc(self):
        self.assertEqual(jobs.parse_not_before("2026-10-12 09:00"), "2026-10-12T08:00Z")  # BST
        self.assertEqual(jobs.parse_not_before("2026-12-01 09:00"), "2026-12-01T09:00Z")  # GMT
        self.assertEqual(jobs.parse_not_before(""), "")
        with self.assertRaises(ValueError):
            jobs.parse_not_before("12 Oct 09:00")

    def test_next_and_peek_skip_it_until_its_time(self):
        d = queue(("mini", "flow balance", {"not_before": "2026-10-07 14:00"}), ("mini", "later job", {}))
        self.assertEqual(d["jobs"][0]["not_before"], "2026-10-07T13:00Z")
        self.assertFalse(jobs.claimable(d, d["jobs"][0], jobs.MINI_NEEDS, T0, "cursor"))
        self.assertEqual(jobs.do_next(d, "cursor", {"mini"}, T0)["id"], "J0002")  # the gated job doesn't hold up the line
        self.assertIsNone(jobs.do_next(d, "codex", {"mini"}, T0 + 59 * MIN))
        self.assertEqual(jobs.do_next(d, "codex", {"mini"}, T0 + 60 * MIN)["id"], "J0001")

    def test_schedule_sets_and_clears_and_the_board_shows_it(self):
        d = queue(("mini", "flow balance", {}))
        j = d["jobs"][0]
        jobs.do_schedule(j, "chief", "2026-10-07 14:00", T0)
        self.assertEqual(j["not_before"], "2026-10-07T13:00Z")
        self.assertIn("not before 2026-10-07 14:00 London", j["history"][-1]["what"])
        self.assertIn("starts", jobs.render(d, T0))
        self.assertIn("not before: 2026-10-07 14:00 London", jobs.show(j))
        jobs.do_schedule(j, "chief", "", T0)
        self.assertNotIn("not_before", j)
        self.assertTrue(jobs.claimable(d, j, {"mini"}, T0, "cursor"))

    def test_relay_next_job_respects_it(self):
        import chief_relay
        d = queue(("mini", "flow balance", {"not_before": "2099-01-01 09:00"}))
        old = (jobs.load,)
        jobs.load = lambda *a: d
        try:
            self.assertIsNone(chief_relay.next_job("cursor"))
        finally:
            jobs.load, = old

    def test_cli_schedule(self):
        d = queue(("mini", "flow balance", {}))
        saved = []
        with tempfile.TemporaryDirectory() as tmp:
            old = (jobs.load, jobs.save, jobs.JOBS_MD, jobs.publish_board, jobs.heartbeat)
            jobs.load, jobs.save = (lambda *a: d), (lambda data, *a: saved.append(data))
            jobs.JOBS_MD, jobs.publish_board, jobs.heartbeat = pathlib.Path(tmp) / "JOBS.md", (lambda: None), (lambda a: None)
            try:
                rc = jobs.main(["schedule", "J0001", "--agent", "chief", "--not-before", "2026-10-12 09:00"])
            finally:
                jobs.load, jobs.save, jobs.JOBS_MD, jobs.publish_board, jobs.heartbeat = old
        self.assertEqual(rc, 0)
        self.assertEqual(saved[0]["jobs"][0]["not_before"], "2026-10-12T08:00Z")


if __name__ == "__main__":
    unittest.main()
