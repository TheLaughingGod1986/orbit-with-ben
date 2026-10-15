"""routing.py: each job kind goes to the model that does it best; AGENTS.md's table and the code agree (Ben, 11 Oct 2026)."""
import datetime as dt, pathlib, re, sys, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs  # noqa: E402
import routing  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
T0 = dt.datetime(2026, 10, 11, 21, 0, tzinfo=dt.timezone.utc)


def agents_section():
    text = (ROOT / "AGENTS.md").read_text()
    m = re.search(r"^## Who does what.*?\n(.*?)(?=^## )", text, re.S | re.M)
    return m.group(1)


class Routing(unittest.TestCase):
    def test_every_kind_and_its_models_are_in_agents_md(self):
        sec = agents_section()
        for kind, (what, primary, backup, _) in routing.KINDS.items():
            row = next((l for l in sec.splitlines() if f"`{kind}`" in l), None)
            self.assertIsNotNone(row, f"AGENTS.md 'Who does what' has no row for kind {kind}")
            self.assertIn(f"`{primary[1]}`", row, kind)
            for _, model in routing.fallbacks(kind):
                self.assertIn(f"`{model}`", row, kind)

    def test_only_configured_models(self):
        for kind, (_, p, b, _) in routing.KINDS.items():
            for lane in (p, b):
                if lane:
                    self.assertIn(lane[1], routing.MODELS, kind)
        self.assertNotIn("gpt-astra", routing.MODELS)  # Ben's "GPT-Astra" is gpt-6-astra
        self.assertNotIn("claude-opus-5.5", routing.MODELS)  # the id is claude-opus-5-5

    def test_chart_work_goes_to_codex_on_astra(self):
        job = {"kind": "chart"}
        self.assertEqual(routing.preferred_worker(job), "codex")
        self.assertEqual(routing.model_for(job, "codex"), "gpt-6-astra")
        self.assertEqual(routing.model_for(job, "cursor"), "cursor-grok-4-7")

    def test_thumbnails_go_to_codex(self):
        """Ben, 14 Oct 2026: Codex built the new thumbnails; Codex builds them from now on."""
        self.assertEqual(routing.preferred_worker({"kind": "thumb"}), "codex")
        self.assertEqual(routing.model_for({"kind": "thumb"}, "codex"), "gpt-6-astra")
        self.assertEqual(routing.chain("thumb")[1:], [("cursor", "cursor-grok-4-7"), ("cursor", "cursor-auto"),
                                                      ("gemini", "gemini-agy")])

    def test_an_explicit_model_wins(self):
        job = {"kind": "assembly", "model": "gpt-6-astra"}
        self.assertEqual(routing.preferred_worker(job), "codex")
        self.assertEqual(routing.model_for(job, "codex"), "gpt-6-astra")

    def test_claude_jobs_walk_claude_cursor_on_claude_gemini_then_codex(self):
        """Ben, 11 Oct 2026 23:40 ("a Claude model in Cursor") and 23:47 ("we also have Gemini and Codex")."""
        for kind in ("script", "review", "qa", "listing"):
            self.assertEqual(routing.chain(kind), [("claude", "claude-opus-5-5"), ("cursor", "cursor-claude-opus-5-5"),
                                                   ("gemini", "gemini-argon"), ("codex", "gpt-6-astra")], kind)
            self.assertEqual(routing.model_for({"kind": kind}, "cursor"), "cursor-claude-opus-5-5")
            self.assertEqual(routing.model_for({"kind": kind}, "gemini"), "gemini-argon")
            self.assertEqual(routing.model_for({"kind": kind}, "codex"), "gpt-6-astra")
        self.assertEqual(routing.model_for({"kind": "facts"}, "cursor"), "")  # Cursor drives agy there, not Claude
        self.assertEqual(routing.chain("chart")[0], ("codex", "gpt-6-astra"))  # code and graphics: Codex first
        self.assertEqual(routing.cli_model("cursor-claude-opus-5-5"), routing.CURSOR_CLAUDE_MODEL)
        self.assertEqual(routing.CURSOR_CLAUDE_MODEL, "claude-opus-5-5")  # Cursor's Opus 5.5 id on the Mini
        self.assertEqual(routing.cli_model("cursor-auto"), "")
        self.assertTrue(routing.claude_owned({"kind": "script"}))
        self.assertFalse(routing.claude_owned({"kind": "script", "model": "gpt-6-astra"}))
        self.assertFalse(routing.claude_owned({"kind": "chart"}))

    def test_every_chain_ends_somewhere_on_the_mini_except_chief(self):
        for kind in routing.CHAINS:
            minis = [a for a, _ in routing.chain(kind) if a in routing.MINI_WORKERS]
            if kind == "chief":
                self.assertEqual(minis, [])
            else:
                self.assertGreaterEqual(len(minis), 2, kind)  # one worker out never parks the job

    def test_next_lane_skips_workers_that_are_down(self):
        job = {"kind": "script"}
        self.assertEqual(routing.next_lane(job, "claude", {"cursor", "gemini", "codex"}), ("cursor", "cursor-claude-opus-5-5"))
        self.assertEqual(routing.next_lane(job, "claude", {"gemini", "codex"}), ("gemini", "gemini-argon"))
        self.assertEqual(routing.next_lane(job, "gemini", {"cursor", "codex"}), ("codex", "gpt-6-astra"))
        self.assertIsNone(routing.next_lane(job, "codex", {"cursor", "gemini", "codex"}))
        self.assertEqual(routing.next_lane({"kind": "chart"}, "codex", {"cursor"}), ("cursor", "cursor-grok-4-7"))
        self.assertEqual(routing.preferred_worker({"kind": "chart"}, {"cursor", "gemini"}), "cursor")
        self.assertEqual(routing.preferred_worker({"kind": "chart"}, {"gemini"}), "gemini")

    def test_reroute_hands_a_claude_job_to_cursor_and_remembers_where_it_was(self):
        d = {"next_id": 1, "jobs": []}
        j = jobs.do_add(d, title="028 listing", needs="cloud", body="", by="chief", at=T0, kind="listing")
        jobs.do_reroute(j, "relay", "cursor", "cursor-claude-opus-5-5", "Claude out of usage", T0)
        self.assertEqual((j["status"], j["for"], j["needs"], j["model"]), ("open", "cursor", "mini", "cursor-claude-opus-5-5"))
        self.assertEqual(j["rerouted_from"]["needs"], "cloud")
        self.assertTrue(jobs.claimable(d, j, jobs.MINI_NEEDS, T0, "cursor"))
        self.assertFalse(jobs.claimable(d, j, jobs.MINI_NEEDS, T0, "codex"))
        with self.assertRaises(ValueError):
            jobs.do_reroute(j, "relay", "codex", "cursor-claude-opus-5-5", "", T0)  # that model doesn't run on Codex
        c = jobs.do_add(d, title="merge", needs="cloud", body="", by="chief", at=T0, kind="chief")
        with self.assertRaises(ValueError):
            jobs.do_reroute(c, "relay", "cursor", "", "", T0)

    def test_protected_calls_have_no_stand_in(self):
        self.assertIsNone(routing.KINDS["chief"][2])

    def test_jobs_add_carries_kind_and_model_and_refuses_invented_ones(self):
        d = {"next_id": 1, "jobs": []}
        j = jobs.do_add(d, title="025 DATA chart", needs="mini", body="", by="chief", at=T0, kind="chart")
        self.assertEqual(j["kind"], "chart")
        with self.assertRaises(ValueError):
            jobs.do_add(d, title="x", needs="mini", body="", by="chief", at=T0, kind="paint")
        with self.assertRaises(ValueError):
            jobs.do_add(d, title="x", needs="mini", body="", by="chief", at=T0, model="gpt-astra")
        self.assertIn("chart · ", jobs.render(d, T0))



class HosPictureOnFlow(unittest.TestCase):
    def test_hos_video_and_image_chains_use_flow_models(self):
        for kind, flow in (("video", "flow-veo-3.1"), ("image", "flow-nano-banana-2")):
            ch = routing.job_chain({"kind": kind, "repo": "hos"})
            self.assertTrue(ch and all(m == flow for _, m in ch), ch)
        self.assertEqual(routing.job_chain({"kind": "video"})[0][1], "veo-3.1-fast-generate-001")  # OWB keeps Vertex


if __name__ == "__main__":
    unittest.main()
