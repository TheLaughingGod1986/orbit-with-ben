import datetime as dt, json, pathlib, sys, tempfile, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import studio  # noqa: E402
import sync_rules  # noqa: E402

T0 = dt.datetime(2026, 10, 5, 15, 0, tzinfo=dt.timezone.utc)


def blank():
    return {"film": "027", "title": "", "air": "", "stages": {}, "claims": [], "next": ""}


class Parse(unittest.TestCase):
    def test_minute_and_second_stamps(self):
        self.assertEqual(studio.parse("2026-10-26T08:47Z"), dt.datetime(2026, 10, 26, 8, 47, tzinfo=dt.timezone.utc))
        self.assertEqual(studio.parse("2026-10-26T08:47:15Z"), dt.datetime(2026, 10, 26, 8, 47, 15, tzinfo=dt.timezone.utc))


class FilmDir(unittest.TestCase):
    def test_a_channel_prefixed_film_id_finds_the_same_folder(self):
        # 8 Nov 2026: jobs naming "OWB:026" stopped every MacBook claim ("no single film folder").
        with tempfile.TemporaryDirectory() as t:
            films = pathlib.Path(t)
            (films / "026_How-Far-Is-The-Nearest-Star").mkdir()
            self.assertEqual(studio.film_dir(films, "OWB:026").name, "026_How-Far-Is-The-Nearest-Star")
            self.assertEqual(studio.film_dir(films, "026").name, "026_How-Far-Is-The-Nearest-Star")


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

    def test_stale_seen_reports_each_stall_once(self):
        seen = self.films / "seen.txt"
        late = T0 + dt.timedelta(minutes=31)
        self.assertEqual(len(studio.stale_list(self.films, late, seen)), 1)
        self.assertEqual(studio.stale_list(self.films, late + dt.timedelta(minutes=15), seen), [])
        self.assertEqual(len(studio.stale_list(self.films, late)), 1)  # without --seen it always lists

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
        import channels
        if not channels.home():
            # The studio in a repo of its own keeps no STATUS.md: the page is built on every run (the move's table,
            # scripts/studio_split.py ROUTES), so there is no committed copy to be out of date.
            self.skipTest("no channel is the studio's home: STATUS.md is built, not kept")
        self.assertEqual(studio.main(["status", "--check"]), 0)


class SyncRules(unittest.TestCase):
    SRC = "# A\n\n## Never\n- one\n- two\n\n## Other\nx\n"
    CHANNEL = "# Channel\n\n## Teach on screen\n- show it\n\n## Never (this channel's additions)\n- three\n"
    BOTH = {"AGENTS.md": SRC, "studio/RULES.md": CHANNEL}

    def test_section_body(self):
        self.assertEqual(sync_rules.find_section(self.SRC, "Never"), "- one\n- two\n")
        self.assertEqual(sync_rules.section(self.BOTH, "AGENTS.md", "Never"), "- one\n- two\n")
        self.assertIsNone(sync_rules.find_section(self.SRC, "Missing"))

    def test_block_rewritten_from_source(self):
        doc = "top\n<!-- SYNC: AGENTS.md#Never -->\n- stale\n<!-- /SYNC -->\nend\n"
        self.assertEqual(sync_rules.sync(doc, self.SRC),
                         "top\n<!-- SYNC: AGENTS.md#Never -->\n- one\n- two\n<!-- /SYNC -->\nend\n")

    def test_a_block_is_filled_from_the_rule_file_its_marker_names(self):
        """J2527, 11 Nov 2026: the studio's rules are in AGENTS.md and the channel's own in studio/RULES.md."""
        doc = ("<!-- SYNC: AGENTS.md#Never -->\nold\n<!-- /SYNC -->\n"
               "<!-- SYNC: studio/RULES.md#Teach on screen -->\nold\n<!-- /SYNC -->\n"
               "<!-- SYNC: studio/RULES.md#Never (this channel's additions) -->\n<!-- /SYNC -->\n")
        self.assertEqual(sync_rules.sync(doc, self.BOTH),
                         "<!-- SYNC: AGENTS.md#Never -->\n- one\n- two\n<!-- /SYNC -->\n"
                         "<!-- SYNC: studio/RULES.md#Teach on screen -->\n- show it\n<!-- /SYNC -->\n"
                         "<!-- SYNC: studio/RULES.md#Never (this channel's additions) -->\n- three\n<!-- /SYNC -->\n")

    def test_the_two_never_lists_do_not_shadow_each_other(self):
        self.assertEqual(sync_rules.section(self.BOTH, "studio/RULES.md", "Never (this channel's additions)"), "- three\n")
        self.assertEqual(sync_rules.section(self.BOTH, "AGENTS.md", "Never"), "- one\n- two\n")

    def test_a_marker_naming_the_wrong_file_says_where_the_section_is(self):
        with self.assertRaises(SystemExit) as cm:
            sync_rules.sync("<!-- SYNC: AGENTS.md#Teach on screen -->\n<!-- /SYNC -->\n", self.BOTH)
        self.assertIn("AGENTS.md has no '## Teach on screen' section", str(cm.exception))
        self.assertIn("it is in studio/RULES.md", str(cm.exception))
        with self.assertRaises(SystemExit) as cm:
            sync_rules.sync("<!-- SYNC: AGENTS.md#Nowhere -->\n<!-- /SYNC -->\n", self.BOTH)
        self.assertNotIn("it is in", str(cm.exception))

    def test_repo_rules_are_in_sync(self):
        self.assertEqual(sync_rules.main.__name__, "main")
        src = {name: path.read_text() for name, path in sync_rules.SOURCES.items()}
        for rel in sync_rules.TARGETS:
            text = (sync_rules.ROOT / rel).read_text()
            self.assertEqual(sync_rules.sync(text, src), text, rel)
        self.assertEqual(sync_rules.stale_hits(), [])

    def test_the_studio_file_points_at_the_channel_file_and_the_channel_file_back(self):
        studio = sync_rules.SOURCE.read_text()
        channel = sync_rules.CHANNEL_SOURCE.read_text()
        self.assertIn("**Then read `studio/RULES.md`.**", studio[:1500])     # in the first screen, before any rule
        self.assertIn("Read `AGENTS.md` first.", channel[:400])
        self.assertIn("can never remove a studio rule", studio)
        self.assertIn("Nothing here removes a studio rule", channel)

    def test_no_section_sits_in_both_rule_files(self):
        import re
        heads = lambda text: set(re.findall(r"^## (.+)$", text, re.M))
        both = heads(sync_rules.SOURCE.read_text()) & heads(sync_rules.CHANNEL_SOURCE.read_text())
        self.assertEqual(both, set(), "a heading in both files makes it unclear which one a copy is filled from")

    def test_the_safety_lines_stay_in_the_studio_file(self):
        """A channel can add a rule and can never remove a studio one: these must not move to a channel's file."""
        import re
        never = re.search(r"^## Never\n(.*?)(?=^## )", sync_rules.SOURCE.read_text(), re.S | re.M).group(1)
        for line in ("Swap the file on an existing YouTube id.", "Delete a video.", "Air more than one Short a day.",
                     "Ship a Short of 40 s or more.", "Ship a silent or near-silent file.", "Run a new test? Your current test will be deleted",
                     "Generate anything on the ElevenLabs website", "Use a video model's speech as VO.", "**Security (both repos are public",
                     "Commit a token, cookie, bearer, password", "email address into a tracked file", "private-network address",
                     "**Repo:** merge, close or push to a studio thread", "**Secrets:** commit or print them."):
            self.assertIn(line, never, line)


if __name__ == "__main__":
    unittest.main()
