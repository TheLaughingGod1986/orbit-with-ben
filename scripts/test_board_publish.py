#!/usr/bin/env python3
"""Tests for board_publish.py (self-updating Studio Kanban data) and the board_site build."""
import datetime as dt
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board_publish as bp  # noqa: E402


def docs(job_status="open", heartbeat="2026-10-09T20:00:00Z"):
    return {"hos": {"updatedAt": "x", "pipeline": {"films": [{"id": "005"}]}},
            "owb": {"updatedAt": "x", "films": [{"film": "027"}], "jobs": [{"id": "J1", "status": job_status}],
                    "lanes": {"mini": {"busy": 1, "heartbeat": {"at": heartbeat}}}},
            "briefs": {"updatedAt": "x", "films": {"027": "note"}},
            "credits": {"pools": {"flow": {}}}}


T0 = dt.datetime(2026, 10, 9, 20, 0, tzinfo=dt.timezone.utc)
T1 = T0 + dt.timedelta(minutes=5)


class ChangeTimes(unittest.TestCase):
    def test_first_run_stamps_every_section(self):
        board, hashes = bp.assemble(docs(), {}, {}, T0)
        self.assertEqual(set(board["changedAt"]), set(bp.SECTIONS))
        self.assertEqual(board["dataChangedAt"], "2026-10-09T20:00:00Z")
        self.assertEqual(board["owb"]["updatedAt"], "2026-10-09T20:00:00Z")

    def test_only_the_changed_section_moves(self):
        b0, h0 = bp.assemble(docs(), {}, {}, T0)
        prev = {"hashes": h0, "changedAt": b0["changedAt"]}
        b1, _ = bp.assemble(docs(job_status="claimed"), prev, {}, T1)
        self.assertEqual(b1["changedAt"]["owb"], "2026-10-09T20:05:00Z")
        self.assertEqual(b1["changedAt"]["hos"], "2026-10-09T20:00:00Z")
        self.assertEqual(b1["dataChangedAt"], "2026-10-09T20:05:00Z")

    def test_heartbeat_alone_is_not_a_data_change_but_is_published(self):
        b0, h0 = bp.assemble(docs(), {}, {}, T0)
        b1, h1 = bp.assemble(docs(heartbeat="2026-10-09T20:10:00Z"), {"hashes": h0, "changedAt": b0["changedAt"]}, {}, T1)
        self.assertEqual(h0, h1)
        self.assertEqual(b1["dataChangedAt"], "2026-10-09T20:00:00Z")
        self.assertNotEqual(bp.digest(b0), bp.digest(b1))  # so the push still happens and "Mini last seen" moves

    def test_checks_ride_along(self):
        board, _ = bp.assemble(docs(), {}, {"OWB-022": {"verdict": "ok"}}, T0)
        self.assertEqual(board["checks"]["OWB-022"]["verdict"], "ok")


class Lock(unittest.TestCase):
    def test_a_busy_publish_queues_one_more_round_and_never_fails(self):
        with tempfile.TemporaryDirectory() as d:
            old = bp.STATE
            bp.STATE = Path(d)
            try:
                import fcntl
                with open(Path(d) / "publish.lock", "w") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.assertEqual(bp.main(["--quiet"]), 0)
                self.assertTrue((Path(d) / "again").exists())
            finally:
                bp.STATE = old


class JobsHook(unittest.TestCase):
    def test_hook_is_off_when_disabled(self):
        import jobs
        os.environ["BOARD_PUBLISH"] = "0"
        try:
            called = []
            real = jobs.subprocess.Popen
            jobs.subprocess.Popen = lambda *a, **k: called.append(a)
            try:
                jobs.publish_board()
            finally:
                jobs.subprocess.Popen = real
            self.assertEqual(called, [])
        finally:
            os.environ.pop("BOARD_PUBLISH")


class SiteBuild(unittest.TestCase):
    def test_build_patches_the_artifact_page(self):
        spec = importlib.util.spec_from_file_location("board_build", HERE.parent / "05_Analytics/kanban/board_site/build.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            mod.build(Path(d) / "dist")
            html = (Path(d) / "dist" / "index.html").read_text()
            self.assertIn("window.claude = { use:", html)
            self.assertIn("dbApi = db.canWrite===false ? null : db;", html)
            self.assertIn("board-data/board.json", html)
            self.assertTrue((HERE.parent / "05_Analytics/kanban/board_site/api/checks.js").exists())
            self.assertIn('href="/tracker"', html)
            version=json.loads((Path(d)/"dist/version.json").read_text())["version"]
            self.assertIn(f'<meta name="studio-version" content="{version}">',html)
            self.assertIn('src="/updater.js"',html)
            self.assertTrue((Path(d)/"dist/updater.js").exists())
            tracker=(Path(d)/"dist/tracker.html").read_text()
            self.assertIn(f'<meta name="studio-version" content="{version}">',tracker)

    def test_build_makes_the_tracker_web_app(self):
        spec = importlib.util.spec_from_file_location("board_build", HERE.parent / "05_Analytics/kanban/board_site/build.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            mod.build(Path(d) / "dist")
            dist = Path(d) / "dist"
            html = (dist / "tracker.html").read_text()
            self.assertNotIn("__TRACKER_DATA__", html)
            self.assertIn("window.__trackerStart = (DATA) => {", html)
            self.assertIn("board-data/tracker.json", html)
            self.assertIn('<link rel="manifest" href="/tracker.webmanifest">', html)
            self.assertIn('<link rel="apple-touch-icon" href="/static/tracker-180.png">', html)
            self.assertIn('<a href="/">Studio board</a>', html)
            man = json.loads((dist / "tracker.webmanifest").read_text())
            self.assertEqual((man["start_url"], man["display"]), ("/tracker", "standalone"))
            for icon in man["icons"]:
                self.assertTrue((dist / icon["src"].lstrip("/")).exists(), icon["src"])
            self.assertTrue((dist / "static/tracker-180.png").exists())
        vercel = json.loads((HERE.parent / "05_Analytics/kanban/board_site/vercel.json").read_text())
        self.assertIn({"source": "/tracker", "destination": "/tracker.html"}, vercel["rewrites"])

    def test_daily_data_changes_do_not_trigger_code_update_loops(self):
        spec=importlib.util.spec_from_file_location("board_version_build",HERE.parent/"05_Analytics/kanban/board_site/build.py")
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);mod.TRACKER_DATA=root/"data.json"
            mod.TRACKER_DATA.write_text(json.dumps({"channels":[],"generatedAt":"first"}))
            mod.build(root/"dist")
            first=json.loads((root/"dist/version.json").read_text())["version"]
            first_html=(root/"dist/tracker.html").read_text()
            mod.TRACKER_DATA.write_text(json.dumps({"channels":[],"generatedAt":"second"}))
            mod.build(root/"dist")
            self.assertEqual(first,json.loads((root/"dist/version.json").read_text())["version"])
            self.assertNotEqual(first_html,(root/"dist/tracker.html").read_text())


class Tracker(unittest.TestCase):
    def test_tree_lists_tracker_json_in_git_order(self):
        rows = bp.tree_listing("b" * 40, "n" * 40, "s" * 40, "t" * 40).splitlines()
        self.assertEqual([r.split("\t")[1] for r in rows], ["07_Content-Ops", "board.json", "tracker.json", "vercel.json"])
        self.assertNotIn("tracker.json", bp.tree_listing("b" * 40, "n" * 40, "s" * 40, None))

    def test_tracker_text_keeps_the_last_good_copy(self):
        with tempfile.TemporaryDirectory() as d:
            old_state, old_wt = bp.STATE, bp.WT
            bp.STATE, bp.WT = Path(d) / "state", Path(d) / "wt"
            bp.STATE.mkdir()
            src = bp.WT / "owb" / bp.TRACKER_SRC
            src.parent.mkdir(parents=True)
            try:
                self.assertIsNone(bp.tracker_text())
                good = '{"generatedAt":"2026-10-09T05:40:00Z","channels":[]}\n'
                src.write_text(good)
                self.assertEqual(bp.tracker_text(), good)
                src.write_text("{broken")
                self.assertEqual(bp.tracker_text(), good)
            finally:
                bp.STATE, bp.WT = old_state, old_wt


class ButtonStamp(unittest.TestCase):
    """Ben's board buttons reach board.json on the next run via the cheap change stamp (11 Oct)."""
    URL = "https://x.public.blob.vercel-storage.com/board/checks/stamp.json"

    def setUp(self):  # keep the Mini's real publish.log clean when the suite runs there
        self._tmp = tempfile.TemporaryDirectory()
        self._state = bp.STATE
        bp.STATE = Path(self._tmp.name)

    def tearDown(self):
        bp.STATE = self._state
        self._tmp.cleanup()

    def prev(self, mins_ago=10, version="v1", **kw):
        p = {"checks": {"OWB-023": {"verdict": "ok"}}, "checksAt": bp.iso(T0 - dt.timedelta(minutes=mins_ago)),
             "checksVersion": version, "stampUrl": self.URL}
        p.update(kw)
        return p

    def stamp(self, v, calls=None):
        def f(url):
            if calls is not None:
                calls.append(url)
            return v
        return f

    def test_unchanged_stamp_means_no_reread(self):
        self.assertFalse(bp.checks_due(self.prev(), T0, False, self.stamp("v1")))

    def test_moved_stamp_means_reread_on_this_run(self):
        self.assertTrue(bp.checks_due(self.prev(), T0, False, self.stamp("v2")))

    def test_unreadable_stamp_falls_back_to_hourly(self):
        self.assertFalse(bp.checks_due(self.prev(), T0, False, self.stamp(None)))
        self.assertTrue(bp.checks_due(self.prev(mins_ago=61), T0, False, self.stamp(None)))

    def test_hourly_force_and_first_run_still_reread(self):
        self.assertTrue(bp.checks_due(self.prev(mins_ago=60), T0, False, self.stamp("v1")))
        self.assertTrue(bp.checks_due(self.prev(), T0, True, self.stamp("v1")))
        self.assertTrue(bp.checks_due({}, T0, False, self.stamp("v1")))

    def test_old_state_learns_the_stamp_url_once(self):
        p = self.prev()
        del p["stampUrl"]
        self.assertTrue(bp.checks_due(p, T0, False, self.stamp("v1")))

    def test_an_older_site_without_a_stamp_stays_hourly(self):
        calls = []
        self.assertFalse(bp.checks_due(self.prev(stampUrl=""), T0, False, self.stamp("v2", calls)))
        self.assertEqual(calls, [])

    def test_at_most_one_stamp_reread_a_minute(self):
        calls = []
        self.assertFalse(bp.checks_due(self.prev(mins_ago=0.5), T0, False, self.stamp("v2", calls)))
        self.assertEqual(calls, [])

    def test_fetch_keeps_the_previous_copy_when_unchanged(self):
        prev = self.prev()
        checks, at, meta = bp.fetch_checks(prev, T0, False, self.stamp("v1"))
        self.assertEqual((checks, at), (prev["checks"], prev["checksAt"]))
        self.assertEqual(meta, {"checksVersion": "v1", "stampUrl": self.URL})

    def test_fetch_rereads_and_records_the_new_version(self):
        body = {"checks": {"OWB-023": {"verdict": "change"}}, "version": "v2", "stampUrl": self.URL}

        class R:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return json.dumps(body).encode()

        real = bp.urllib.request.urlopen
        bp.urllib.request.urlopen = lambda *a, **k: R()
        try:
            checks, at, meta = bp.fetch_checks(self.prev(), T0, False, self.stamp("v2"))
        finally:
            bp.urllib.request.urlopen = real
        self.assertEqual(checks["OWB-023"]["verdict"], "change")
        self.assertEqual(at, bp.iso(T0))
        self.assertEqual(meta, {"checksVersion": "v2", "stampUrl": self.URL})

    def test_site_down_keeps_the_previous_copy_and_retries(self):
        def boom(*a, **k):
            raise OSError("down")
        real = bp.urllib.request.urlopen
        bp.urllib.request.urlopen = boom
        try:
            checks, at, meta = bp.fetch_checks(self.prev(), T0, False, self.stamp("v2"))
        finally:
            bp.urllib.request.urlopen = real
        self.assertEqual(meta["checksVersion"], "v1")  # so the next run sees the moved stamp again

    def test_site_stores_ticks_in_the_github_issue_and_posting_is_unchanged(self):
        js = (HERE.parent / "05_Analytics/kanban/board_site/api/checks.js").read_text()
        # 15 Oct 2026: the store is orbit-with-ben #219's body, not the suspended Vercel Blob store
        self.assertIn('const STORE = ["TheLaughingGod1986/orbit-with-ben", 219];', js)
        self.assertNotIn("@vercel/blob", js)
        self.assertIn("version, stampUrl", js)
        self.assertIn("/api/checks?stamp=1", js)
        # one post per real change, exactly as before, and only after the tick is saved
        self.assertIn("const line = doc && prev && prev.at === doc.at && prev.verdict === doc.verdict ? null : benLine(b.id, doc, prev);", js)
        self.assertEqual(js.count("postToChief(b.id, saved ?"), 1)
        self.assertLess(js.index("await save(state)"), js.index("postToChief(b.id, saved ?"))

    def test_the_mini_never_posts(self):
        src = (HERE / "board_publish.py").read_text()
        self.assertNotIn("api.github.com", src)
        self.assertNotIn("issues/", src)


class QuickNoOp(unittest.TestCase):
    """Every-minute runs (Ben, 11 Oct 22:09) stop early when nothing moved."""

    def test_same_refs_recent_build_and_no_ticks_skip(self):
        prev = {"key": "k1", "built": bp.iso(T0 - dt.timedelta(minutes=2))}
        self.assertTrue(bp.skip_quick(prev, "k1", T0, False))

    def test_a_moved_ref_a_tap_an_old_build_or_no_key_rebuild(self):
        prev = {"key": "k1", "built": bp.iso(T0 - dt.timedelta(minutes=2))}
        self.assertFalse(bp.skip_quick(prev, "k2", T0, False))
        self.assertFalse(bp.skip_quick(prev, "k1", T0, True))
        self.assertFalse(bp.skip_quick(dict(prev, built=bp.iso(T0 - dt.timedelta(seconds=bp.FULL_EVERY_S))), "k1", T0, False))
        self.assertFalse(bp.skip_quick(prev, None, T0, False))
        self.assertFalse(bp.skip_quick({}, "k1", T0, False))

    def test_quick_key_follows_the_refs_and_fails_open(self):
        refs = {"main": "a"}
        remote = lambda repo, *r: f"{repo}:{refs['main']}:{','.join(r)}"
        k1 = bp.quick_key(remote)
        self.assertEqual(k1, bp.quick_key(remote))
        refs["main"] = "b"
        self.assertNotEqual(k1, bp.quick_key(remote))

        def broken(repo, *r):
            raise RuntimeError("offline")
        with tempfile.TemporaryDirectory() as d:
            old = bp.STATE
            bp.STATE = Path(d)
            try:
                self.assertIsNone(bp.quick_key(broken))
            finally:
                bp.STATE = old

    def test_launchd_runs_every_minute(self):
        plist = (HERE / "mini" / "com.owb.board-publish.plist").read_text()
        self.assertIn("<key>StartInterval</key><integer>60</integer>", plist)

    def test_page_polls_board_data_every_minute(self):
        shim = (HERE.parent / "05_Analytics/kanban/board_site/shim.js").read_text()
        self.assertIn("const PERIOD = 60 * 1000;", shim)   # re-read a minute after the last read (Refresh restarts it)
        self.assertIn("timer = setTimeout(() => { pollData().then(schedule); }", shim)
        self.assertIn("publishedAt: j.publishedAt", shim)


if __name__ == "__main__":
    unittest.main()
