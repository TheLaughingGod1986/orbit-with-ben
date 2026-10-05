import datetime as dt, json, pathlib, sys, tempfile, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import studio  # noqa: E402
import sync_rules  # noqa: E402

T0 = dt.datetime(2026, 10, 5, 15, 0, tzinfo=dt.timezone.utc)


def blank():
    return {"film": "027", "title": "", "air": "", "stages": {}, "claims": [], "next": ""}


class Claims(unittest.TestCase):
    def test_claim_marks_doing(self):
        d = blank()
        self.assertIsNone(studio.do_claim(d, "sources", "chief/gemini", 60, "draft", T0))
        self.assertEqual(d["stages"]["sources"]["state"], "doing")
        self.assertEqual(d["claims"][0]["eta"], "2026-10-05T16:00Z")

    def test_live_claim_blocks_other_agent(self):
        d = blank()
        studio.do_claim(d, "vo", "hos-desk", 60, "", T0)
        err = studio.do_claim(d, "vo", "chief", 60, "", T0 + dt.timedelta(minutes=30))
        self.assertTrue(err.startswith("held by hos-desk"))
        self.assertEqual(len(d["claims"]), 1)

    def test_same_agent_can_renew(self):
        d = blank()
        studio.do_claim(d, "vo", "chief", 30, "", T0)
        self.assertIsNone(studio.do_claim(d, "vo", "chief", 30, "", T0 + dt.timedelta(minutes=10)))
        self.assertEqual(len(d["claims"]), 1)

    def test_stalled_claim_can_be_taken_over_and_is_noted(self):
        d = blank()
        studio.do_claim(d, "sources", "chief/gemini", 15, "", T0)
        self.assertIsNone(studio.do_claim(d, "sources", "chief/gemini-2", 60, "retry", T0 + dt.timedelta(minutes=20)))
        self.assertEqual(d["claims"][0]["by"], "chief/gemini-2")
        self.assertIn("took over stalled claim by chief/gemini", d["claims"][0]["note"])

    def test_other_stages_do_not_conflict(self):
        d = blank()
        studio.do_claim(d, "vo", "chief", 60, "", T0)
        self.assertIsNone(studio.do_claim(d, "shots", "claude", 60, "", T0))
        self.assertEqual(len(d["claims"]), 2)

    def test_release_needs_own_claim(self):
        d = blank()
        studio.do_claim(d, "vo", "chief", 60, "", T0)
        self.assertIsNotNone(studio.do_release(d, "vo", "claude", "done", None))
        self.assertIsNone(studio.do_release(d, "vo", "chief", "review", "abc123"))
        self.assertEqual(d["claims"], [])
        self.assertEqual(d["stages"]["vo"], {"state": "review", "ref": "abc123"})


class BoardAndStale(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.films = pathlib.Path(self.tmp.name)
        f = self.films / "027_What-If"
        f.mkdir()
        d = blank()
        d["air"] = "2026-11-22"
        d["next"] = "Claude: Locked VO"
        studio.do_set(d, "script", "done", "e55a5ea", None)
        studio.do_claim(d, "sources", "chief/gemini", 30, "SOURCES", T0)
        (f / "status.json").write_text(json.dumps(d))
        (self.films / "026_No-Status").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_board_shows_marks_and_claims(self):
        out = studio.board(self.films, T0 + dt.timedelta(minutes=5))
        self.assertIn("027   2026-11-22", out)
        self.assertIn("Claude: Locked VO", out)
        self.assertIn("live", out)
        self.assertNotIn("\n026 ", out)

    def test_stale_after_eta(self):
        self.assertEqual(studio.stale_list(self.films, T0 + dt.timedelta(minutes=29)), [])
        hits = studio.stale_list(self.films, T0 + dt.timedelta(minutes=31))
        self.assertEqual(len(hits), 1)
        self.assertIn("027 sources by chief/gemini", hits[0])

    def test_cli_claim_exit_code_when_held(self):
        path = self.films / "027_What-If" / "status.json"
        d = json.loads(path.read_text())
        studio.do_claim(d, "vo", "chief", 60, "", studio.now())  # live against the real clock the CLI uses
        path.write_text(json.dumps(d))
        argv = ["--films", str(self.films), "claim", "027", "vo", "--by", "other"]
        self.assertEqual(studio.main(argv), studio.EX_HELD)

    def test_cli_set_writes_file(self):
        self.assertEqual(studio.main(["--films", str(self.films), "set", "027", "vo", "todo", "--next", "x"]), 0)
        d = json.loads((self.films / "027_What-If" / "status.json").read_text())
        self.assertEqual(d["stages"]["vo"]["state"], "todo")
        self.assertEqual(d["next"], "x")


class StatusPage(unittest.TestCase):
    def test_render_and_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            films = pathlib.Path(tmp) / "02_Video-Projects"
            (films / "027_X").mkdir(parents=True)
            d = blank()
            d.update(title="What If Earth Stopped Spinning?", air="2026-11-22", next="Locked VO")
            studio.do_set(d, "topic", "done", None, None)
            studio.do_set(d, "script", "review", None, None)
            studio.do_claim(d, "sources", "chief/gemini", 30, "", T0)
            (films / "027_X" / "status.json").write_text(json.dumps(d))
            md = studio.render_md(films)
            self.assertIn("| 027 What If Earth Stopped Spinning? | 2026-11-22 | 1/9 | script (review), sources (doing) | Locked VO |", md)
            self.assertIn("| 027 | sources | chief/gemini | 2026-10-05T15:00Z | 2026-10-05T15:30Z | - |", md)
            self.assertEqual(studio.main(["--films", str(films), "status", "--check"]), 1)
            self.assertEqual(studio.main(["--films", str(films), "status"]), 0)
            self.assertEqual(studio.main(["--films", str(films), "status", "--check"]), 0)
            studio.main(["--films", str(films), "set", "027", "vo", "todo"])  # writes keep STATUS.md current
            self.assertEqual(studio.main(["--films", str(films), "status", "--check"]), 0)

    def test_repo_status_page_is_current(self):
        self.assertEqual(studio.main(["status", "--check"]), 0)


class SyncRules(unittest.TestCase):
    SRC = "# A\n\n## Never\n- one\n- two\n\n## Other\nx\n"

    def test_section_body(self):
        self.assertEqual(sync_rules.section(self.SRC, "Never"), "- one\n- two\n")

    def test_block_rewritten_from_source(self):
        doc = "top\n<!-- SYNC: AGENTS.md#Never -->\n- stale\n<!-- /SYNC -->\nend\n"
        self.assertEqual(sync_rules.sync(doc, self.SRC),
                         "top\n<!-- SYNC: AGENTS.md#Never -->\n- one\n- two\n<!-- /SYNC -->\nend\n")

    def test_repo_rules_are_in_sync(self):
        self.assertEqual(sync_rules.main.__name__, "main")
        src = sync_rules.SOURCE.read_text()
        for rel in sync_rules.TARGETS:
            text = (sync_rules.ROOT / rel).read_text()
            self.assertEqual(sync_rules.sync(text, src), text, rel)
        self.assertEqual(sync_rules.stale_hits(), [])


if __name__ == "__main__":
    unittest.main()
