#!/usr/bin/env python3
"""Tests for board_publish.py (self-updating Studio Kanban data) and the board_site build."""
import datetime as dt
import importlib.util
import json
import os
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board_publish as bp  # noqa: E402


def docs(job_status="open", heartbeat="2026-10-09T20:00:00Z"):
    return {"hos": {"updatedAt": "x", "pipeline": {"films": [{"id": "005"}]}},
            "owb": {"updatedAt": "x", "films": [{"film": "027"}], "jobs": [{"id": "J1", "status": job_status}],
                    "lanes": {"mini": {"busy": 1, "heartbeat": {"at": heartbeat}}}},
            "briefs": {"updatedAt": "x", "films": {"027": "note"}},
            "credits": {"pools": {"flow": {}}},
            "tracker": {"updatedAt": "x", "lanes": [], "videos": []}}


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
            home = (Path(d) / "dist" / "index.html").read_text()
            ai = (Path(d) / "dist" / "ai.html").read_text()
            # Home page is the studio app (Ben, 28 Oct 2026)
            self.assertIn("STUDIO_APP_TEST_HOOK", home)
            self.assertIn("board-data/board.json", home)
            # The per-video column board (/board) is retired (Ben, 10 Nov 2026: "This seems legacy. I think we can
            # remove this section"): not built, not linked, its address sent to the Studio app. The Studio app keeps
            # the old /#k= key itself now instead of handing it to that page.
            self.assertFalse((Path(d) / "dist" / "board.html").exists())
            self.assertNotIn('href="/board"', home + ai)
            self.assertNotIn('location.replace("/board"', home)
            self.assertIn('localStorage.setItem("studio-board-key", m[1])', home)
            self.assertIn('href="/#videos">Videos</a>', ai)
            # The October swim-lane board (/classic) is retired (Ben, 28 Oct 2026): not built, not linked
            self.assertFalse((Path(d) / "dist" / "classic.html").exists())
            self.assertNotIn('href="/classic"', home + ai)
            self.assertTrue((HERE.parent / "05_Analytics/kanban/board_site/api/checks.js").exists())
            version=json.loads((Path(d)/"dist/version.json").read_text())["version"]
            self.assertIn(f'<meta name="studio-version" content="{version}">', home)
            self.assertIn('src="/updater.js"', home)
            self.assertTrue((Path(d)/"dist/updater.js").exists())
            tracker=(Path(d)/"dist/tracker.html").read_text()
            self.assertIn(f'<meta name="studio-version" content="{version}">',tracker)

    def test_retired_addresses_go_to_the_studio_app(self):
        site = json.loads((HERE.parent / "05_Analytics/kanban/board_site/vercel.json").read_text())
        gone = {r["source"]: r["destination"] for r in site["redirects"]}
        for source in ("/board", "/board/", "/board.html", "/classic", "/classic/", "/classic.html"):
            # No fragment in the destination: the browser then carries an old link's own #v=<video> or #k=<key> over.
            self.assertEqual(gone.get(source), "/", source)
        self.assertEqual([r for r in site["rewrites"] + site["headers"] if "board" in r["source"]], [])

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
            # 10 Nov 2026 (phone): a real back button, and the Studio's dark colours instead of a white page.
            self.assertIn('<a class="studio-back" href="/">', html)
            self.assertIn('<html lang="en" data-theme="dark">', html)
            self.assertIn('<meta name="theme-color" content="#0B111B">', html)
            self.assertIn(':root[data-theme="dark"]', html)   # the template still carries the dark theme this relies on
            man = json.loads((dist / "tracker.webmanifest").read_text())
            self.assertEqual((man["start_url"], man["display"]), ("/tracker", "standalone"))
            for icon in man["icons"]:
                self.assertTrue((dist / icon["src"].lstrip("/")).exists(), icon["src"])
            self.assertTrue((dist / "static/tracker-180.png").exists())
        vercel = json.loads((HERE.parent / "05_Analytics/kanban/board_site/vercel.json").read_text())
        self.assertIn({"source": "/tracker", "destination": "/tracker.html"}, vercel["rewrites"])
        self.assertIn({"source": "/classic", "destination": "/", "permanent": False}, vercel["redirects"])

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
            src = bp.wt() / bp.TRACKER_SRC            # the studio's own copy, whichever repo carries the studio
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
        # Ben's ticks go on the thread scripts/thread.json names (10 Nov 2026: this line still said #264 six days
        # after the November thread opened, so his words went where no agent was reading). A rollover must change both.
        thread = json.loads((HERE / "thread.json").read_text())
        self.assertIn(f'OWB: ["{thread["repo"]}", {thread["number"]}]', js)
        self.assertNotIn(', 264]', js)
        self.assertIn('HOS: ["TheLaughingGod1986/history-of-science", 180]', js)
        self.assertNotIn(', 99]', js)
        # one post per real change, exactly as before, and only after the tick is saved
        # 25 Oct 2026: `via` adds "new device: …" to the tail for open taps (test_board_benauth.py); the prefix is unchanged
        self.assertIn("const line = doc && prev && prev.at === doc.at && prev.verdict === doc.verdict ? null : benLine(b.id, doc, prev, via);", js)
        self.assertEqual(js.count("postToChief(b.id, saved ?"), 1)
        self.assertLess(js.index("await save(state)"), js.index("postToChief(b.id, saved ?"))

    def test_the_mini_never_posts(self):
        src = (HERE / "board_publish.py").read_text()
        self.assertNotIn("api.github.com", src)
        self.assertNotIn("issues/", src)


class QuickNoOp(unittest.TestCase):
    """Every-minute runs (Ben, 11 Oct 22:09) stop early when nothing moved."""

    def test_same_refs_recent_build_and_no_ticks_skip(self):
        prev = {"key": "k1", "built": bp.iso(T0 - dt.timedelta(seconds=bp.FULL_EVERY_S - 1))}
        self.assertTrue(bp.skip_quick(prev, "k1", T0, False))

    def test_a_moved_ref_a_tap_an_old_build_or_no_key_rebuild(self):
        prev = {"key": "k1", "built": bp.iso(T0 - dt.timedelta(seconds=bp.FULL_EVERY_S - 1))}
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

    def test_quick_key_changes_when_valid_execution_ends_without_a_queue_commit(self):
        import chief_relay as relay
        from unittest.mock import patch
        remote = lambda repo, *refs: "unchanged-ref"
        lease = {"job":"J1", "worker":"codex", "expiresAt":"2026-11-03T16:00:00Z"}
        with patch.object(relay, "current_execution", return_value=lease):
            launched = bp.quick_key(remote)
        with patch.object(relay, "current_execution", return_value=None):
            stopped = bp.quick_key(remote)
        self.assertNotEqual(launched, stopped)

    def test_launchd_runs_every_minute(self):
        plist = (HERE / "mini" / "com.owb.board-publish.plist").read_text()
        self.assertIn("<key>StartInterval</key><integer>60</integer>", plist)

    def test_page_polls_board_data_every_minute(self):
        studio = (HERE.parent / "05_Analytics/kanban/board_site/studio_app.js").read_text()
        self.assertIn("setInterval(poll, 60 * 1000);", studio)


class AsksTheLoader(unittest.TestCase):
    """J2615: board_publish.py names no channel. These pin what it did by name on 11 Nov 2026, and show a made-up
    third channel plugging in."""

    def setUp(self):
        # Pin the layout these tests are about, whichever one they run in: one channel's repo carries the studio.
        import channels
        own = channels.default()
        base = tuple(dict(c, home=c["slug"] == own) for c in channels._load())
        for patch in (unittest.mock.patch.object(channels, "_load", lambda directory=None: base),
                      unittest.mock.patch.object(bp, "STUDIO", own),
                      unittest.mock.patch.object(bp, "STUDIO_REPO", bp.REPOS[own])):
            patch.start()
            self.addCleanup(patch.stop)

    def sky(self):
        import channels
        base = channels._load()
        sky = dict(base[0], slug="sky", label="SKY", name="Night Sky", short="Sky", home=False, order=3,
                   title_match=r"\bSKY\b", repo={"env": "SKY_REPO", "checkouts": ["night-sky"]},
                   pipeline={"kind": "pipeline_json", "path": "PIPELINE.json"})
        return unittest.mock.patch.object(channels, "_load", lambda directory=None: base + (sky,))

    def test_nothing_changed_for_the_two_channels(self):
        import channels
        self.assertEqual(bp.SECTIONS, ("hos", "owb", "briefs", "credits", "tracker"))
        self.assertEqual((bp.STUDIO, bp.QUEUE), ("owb", "owb"))
        self.assertEqual(bp.STUDIO_REPO, channels.repo_path("owb", bp.HOME))
        if not os.environ.get("OWB_REPO"):
            self.assertEqual(bp.STUDIO_REPO, bp.HOME / "YouTube" / "orbit-with-ben")
        self.assertEqual(bp.REPOS["hos"], channels.repo_path("hos", bp.HOME))
        self.assertEqual(bp.wt(), bp.WT / "owb")
        self.assertEqual(bp.wt("hos"), bp.WT / "hos")
        shared = ["/STATUS.md", "/00_Brand/Channel-Setup/kanban/index.html", "/studio-core/CORE_FILES.json"]
        self.assertEqual(sorted(bp.sparse("owb")), sorted([
            "/scripts/", "/channels/", "/studio/", "/jobs/", "/05_Analytics/kanban/", "/05_Analytics/ai_spend/",
            "/02_Video-Projects/*/status.json", "/02_Video-Projects/*/11_Upload-Package/PACKAGE_UPLOAD_RESULT*.json",
            "/02_Video-Projects/*/10_Shorts/*/11_Upload-Package/PACKAGE_UPLOAD_RESULT*.json",
            "/00_Brand/Channel-Setup/social/UPLOADS.json", "/05_Analytics/dashboard/data.json", *shared]))
        import channel_pins
        with channel_pins.one_file("hos"):       # a channel that keeps every film in one file
            self.assertEqual(sorted(bp.sparse("hos")), sorted([
                "/studio/", "/00_Brand/Channel-Setup/PIPELINE.json", "/00_Brand/Channel-Setup/social/UPLOADS.json",
                *shared]))
        # and whichever way the real one keeps them this week, the copy holds its film state and its settings
        self.assertIn("/" + channels.pipeline("hos")["path"], bp.sparse("hos"))
        self.assertIn("/studio/", bp.sparse("hos"))

    def test_the_snapshot_is_called_as_before(self):
        out = Path("/tmp/out")
        with unittest.mock.patch.object(bp, "chief_args", lambda: []):
            self.assertEqual(bp.snapshot_command(out),
                             [sys.executable, str(bp.WT / "owb" / "scripts" / "kanban_snapshot.py"),
                              "--hos", str(bp.WT / "hos"), "--db-out", str(out)])

    def test_the_summary_reads_as_before(self):
        self.assertEqual(bp.films_summary(docs()), "1 HOS films, 1 OWB films")

    def test_the_quick_check_asks_each_repo_as_before(self):
        asked = []
        bp.quick_key(lambda repo, *refs: asked.append((repo, refs)) or "x")
        self.assertEqual(asked, [
            (bp.STUDIO_REPO, ("refs/heads/main", "refs/heads/mini-heartbeat", "refs/heads/macbook-heartbeat",
                              "refs/heads/macbook-heartbeat-2")),
            (bp.REPOS["hos"], ("refs/heads/main",))])

    def test_once_the_studio_has_its_own_repo_it_gets_its_own_copy_and_every_channel_is_beside_it(self):
        # J2621 (plan decision 1: no home channel). No channel's repo carries the studio: its files are read from a
        # copy of the studio's own repo, and each channel's copy holds only that channel's files.
        import channels
        apart = tuple(dict(c, home=False) for c in channels._load())
        studio_repo = Path("/Users/x/YouTube/studio")
        made, asked = [], []
        with unittest.mock.patch.object(channels, "_load", lambda directory=None: apart), \
                unittest.mock.patch.object(bp, "STUDIO", None), unittest.mock.patch.object(bp, "STUDIO_REPO", studio_repo), \
                unittest.mock.patch.object(bp, "chief_args", lambda: []):
            self.assertEqual(bp.wt(), bp.WT / "studio")
            self.assertEqual((bp.wt("owb"), bp.wt("hos")), (bp.WT / "owb", bp.WT / "hos"))
            self.assertFalse(set(bp.STUDIO_SPARSE) & set(bp.sparse("owb")))          # no studio file in a channel's copy
            self.assertIn("/02_Video-Projects/*/status.json", bp.sparse("owb"))
            self.assertEqual(bp.snapshot_command(Path("/tmp/out")),
                             [sys.executable, str(bp.WT / "studio" / "scripts" / "kanban_snapshot.py"),
                              "--owb", str(bp.WT / "owb"), "--hos", str(bp.WT / "hos"), "--db-out", "/tmp/out"])
            bp.quick_key(lambda repo, *refs: asked.append((repo, refs)) or "x")
            with tempfile.TemporaryDirectory() as d, \
                    unittest.mock.patch.object(bp, "worktree", lambda repo, path, sparse: made.append((repo, path, sparse))), \
                    unittest.mock.patch.object(bp.subprocess, "run", lambda *a, **k: None):
                bp.build(Path(d) / "out")
        self.assertEqual(asked[0][0], studio_repo)
        # Set when the module loads, so the line is held here; the dry run of the move loads it with no home channel.
        self.assertIn("\nSTUDIO_REPO = REPOS[STUDIO] if STUDIO else channels.studio_checkout(HOME)\n", Path(bp.__file__).read_text())
        self.assertEqual([repo for repo, _ in asked[1:]], [bp.REPOS["owb"], bp.REPOS["hos"]])
        self.assertEqual([(repo, path) for repo, path, _ in made],
                         [(bp.REPOS["owb"], bp.WT / "owb"), (bp.REPOS["hos"], bp.WT / "hos"), (studio_repo, bp.WT / "studio")])
        self.assertEqual(made[-1][2], bp.STUDIO_SPARSE)

    def test_the_heartbeat_is_left_out_of_the_queue_sections_change_check_only(self):
        d = docs()
        self.assertNotIn("heartbeat", bp.stable("owb", d["owb"])["lanes"]["mini"])
        self.assertIn("heartbeat", bp.stable("hos", d["owb"])["lanes"]["mini"])

    def test_a_third_channel_is_on_the_board_with_its_own_section(self):
        with self.sky():
            self.assertEqual(bp.sections(), ("hos", "owb", "sky", "briefs", "credits", "tracker"))
            self.assertEqual(bp.sparse("sky"), ["/studio/", "/PIPELINE.json",
                                                "/00_Brand/Channel-Setup/social/UPLOADS.json", *bp.CHANNEL_SPARSE])
            with unittest.mock.patch.object(bp, "chief_args", lambda: []):
                cmd = bp.snapshot_command(Path("/tmp/out"))
            self.assertEqual(cmd[cmd.index("--sky") + 1], str(bp.WT / "sky"))
            d = dict(docs(), sky={"pipeline": {"films": [{"id": "001"}, {"id": "002"}]}})
            self.assertEqual(bp.films_summary(d), "1 HOS films, 1 OWB films, 2 SKY films")
            board = {}
            bp.add_channels(board)
        self.assertEqual([c["slug"] for c in board["channels"]], ["owb", "hos", "sky"])
        self.assertEqual(board["channels"][-1]["name"], "Night Sky")


if __name__ == "__main__":
    unittest.main()
