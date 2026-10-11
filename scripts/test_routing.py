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
            if backup:
                self.assertIn(f"`{backup[1]}`", row, kind)

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
        self.assertEqual(routing.model_for(job, "cursor"), "cursor-auto")

    def test_an_explicit_model_wins(self):
        job = {"kind": "assembly", "model": "gpt-6-astra"}
        self.assertEqual(routing.preferred_worker(job), "codex")
        self.assertEqual(routing.model_for(job, "codex"), "gpt-6-astra")

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


if __name__ == "__main__":
    unittest.main()
