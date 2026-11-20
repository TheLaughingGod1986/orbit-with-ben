#!/usr/bin/env python3
"""Tests for the registry-driven Recursive Self-Improvement (RSI) loop (J3257):
- Experiment register validation, <=3 live cap per channel, guardrails, min_sample
- Autopsy -> hypothesis candidate ingestion (Test & Compare vs next-N-films)
- Readout lifecycle (pass, fail, inconclusive extend-once-then-drop)
- Registry-driven weekly improvement cycle replacing monthly-improvement items
- Newly registered dummy channel gets a cycle, autopsy ingestion, and dashboard row with NO code change
- Weekly Studio Ops Loop (6 metrics, bottleneck diagnosis, deduplicated fix job, week-over-week proof)
- Dashboard 'What the studio is learning' block and board_publish integration
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import board_publish  # noqa: E402
import channels  # noqa: E402
import jobs  # noqa: E402
import ops_loop  # noqa: E402
import refill  # noqa: E402
import rsi  # noqa: E402
import test_channel_ratchet as ratchet  # noqa: E402

NOW = dt.datetime(2026, 11, 20, 23, 0, tzinfo=dt.timezone.utc)


def _sample_exp(eid="EXP-TST-001", channel="owb", status="candidate", **extra):
    base = {
        "id": eid,
        "channel": channel,
        "status": status,
        "result": "pending",
        "hypothesis": "Payoff number spoken in the first 5 s raises 0:30 retention from 40% to 50%.",
        "change": "Speak the headline payoff number before 0:05 in the opening line.",
        "applies_to": ["next 4 longs"],
        "test_type": "next_n_films",
        "metric": "0:30 retention (%)",
        "expected_effect": "raise 0:30 retention from 40% to 50%",
        "min_sample": 4,
        "sample_unit": "longs",
        "sample_observed": 0,
        "readout_date": "2026-12-15" if status == "running" else "",
        "started_at": "2026-11-20" if status == "running" else "",
        "extended_once": False,
        "source": "test",
        "evidence": "Baseline 0:30 retention is 40%.",
        "revert_plan": "Restore previous opening prompt in script template.",
        "guardrail_scope": "production",
        "decided_at": "",
        "changelog": "",
    }
    base.update(extra)
    return base


class RealRegisterAndRatchetTest(unittest.TestCase):
    def test_real_experiments_register_is_valid_and_respects_cap(self):
        doc = rsi.load_register()
        self.assertEqual(rsi.validate_register(doc), [])
        for slug in channels.slugs():
            live = [e for e in doc["experiments"] if e["channel"] == slug and e["status"] == "running"]
            self.assertLessEqual(len(live), rsi.MAX_LIVE_PER_CHANNEL, slug)
        # Seeded from LEARNINGS + plan.json across registered channels
        ch_set = {e["channel"] for e in doc["experiments"]}
        self.assertTrue(set(channels.slugs()).issubset(ch_set))

    def test_backlog_replaces_monthly_improvement_with_registry_weekly_cycles_and_ops_loop(self):
        raw_items = json.loads((ROOT / "jobs" / "backlog.json").read_text())["items"]
        raw_keys = [it["key"] for it in raw_items]
        self.assertFalse(any(k.startswith("monthly-improvement-") for k in raw_keys))
        self.assertIn("weekly-improvement-{slug}", raw_keys)
        self.assertIn("studio-ops-loop", raw_keys)

        expanded = refill.load_backlog()
        exp_keys = {it["key"]: it for it in expanded}
        for slug in channels.slugs():
            key = f"weekly-improvement-{slug}"
            self.assertIn(key, exp_keys)
            self.assertEqual(exp_keys[key]["every_h"], 168)
            self.assertEqual(exp_keys[key]["repo"], slug)
        self.assertEqual(exp_keys["studio-ops-loop"]["every_h"], 168)

    def test_new_engine_scripts_have_zero_channel_ratchet_hits(self):
        c = ratchet.counts()
        h = ratchet.home_counts()
        for name in ("rsi.py", "ops_loop.py"):
            self.assertEqual(c.get(name, 0), 0, f"{name} named a channel")
            self.assertEqual(h.get(name, 0), 0, f"{name} assumed a home channel")


class ExperimentLifecycleAndGuardrailsTest(unittest.TestCase):
    def test_max_three_live_per_channel_enforced(self):
        doc = {
            "max_live_per_channel": 3,
            "experiments": [
                _sample_exp(f"EXP-1", status="running"),
                _sample_exp(f"EXP-2", status="running"),
                _sample_exp(f"EXP-3", status="running"),
                _sample_exp(f"EXP-4", status="candidate"),
            ],
        }
        self.assertEqual(rsi.validate_register(doc, valid_slugs=["owb"]), [])
        with self.assertRaisesRegex(rsi.RsiError, "already has 3/3"):
            rsi.start_experiment(doc, "EXP-4", now=NOW)

    def test_min_sample_blocks_premature_pass_and_allows_full_sample(self):
        doc = {"max_live_per_channel": 3, "experiments": [_sample_exp("EXP-1", status="running", min_sample=4)]}
        with self.assertRaisesRegex(rsi.RsiError, "below|min_sample|<"):
            rsi.record_readout(doc, "EXP-1", "pass", sample=2, evidence="2 longs hit 52%", now=NOW)
        exp = rsi.record_readout(
            doc, "EXP-1", "pass", sample=4, evidence="4 longs averaged 52% at 0:30", changelog="Kept opening rule", now=NOW
        )
        self.assertEqual((exp["status"], exp["result"]), ("decided", "pass"))
        self.assertEqual(exp["decided_at"], "2026-11-20")

    def test_inconclusive_extends_once_then_drops(self):
        doc = {"max_live_per_channel": 3, "experiments": [_sample_exp("EXP-1", status="running", readout_date="2026-11-20")]}
        e1 = rsi.record_readout(doc, "EXP-1", "inconclusive", sample=2, evidence="Only 2 longs aired so far", now=NOW)
        self.assertEqual(e1["status"], "running")
        self.assertTrue(e1["extended_once"])
        self.assertEqual(e1["readout_date"], "2026-12-04")
        e2 = rsi.record_readout(doc, "EXP-1", "inconclusive", sample=3, evidence="Still noisy after extension", now=NOW)
        self.assertEqual(e2["status"], "dropped")
        self.assertEqual(e2["result"], "inconclusive")

    def test_fail_reverts_and_records_evidence(self):
        doc = {"max_live_per_channel": 3, "experiments": [_sample_exp("EXP-1", status="running")]}
        e = rsi.record_readout(doc, "EXP-1", "fail", sample=4, evidence="0:30 retention fell from 40% to 34%", now=NOW)
        self.assertEqual((e["status"], e["result"]), ("decided", "fail"))

    def test_guardrails_block_ben_gates_never_list_money_and_direction(self):
        forbidden = [
            "Skip Ben's final UAT watch to publish faster",
            "Lift TikTok pause and delete a video that underperforms",
            "Buy credits and upgrade plan for faster video mints",
            "Override Ben's plan and change channel direction without asking",
        ]
        for idx, text in enumerate(forbidden):
            exp = _sample_exp(f"EXP-BAD-{idx}", status="candidate", change=text)
            self.assertTrue(rsi.check_guardrails(exp), text)
            doc = {"max_live_per_channel": 3, "experiments": [exp]}
            with self.assertRaisesRegex(rsi.RsiError, "guardrails"):
                rsi.start_experiment(doc, exp["id"], now=NOW)


class DummyChannelRegistryDrivenTest(unittest.TestCase):
    """Explicit requirement: a newly registered dummy channel gets a weekly improvement cycle,
    autopsy-to-hypothesis ingestion, experiment register support, and a dashboard row with NO code change."""

    def test_newly_registered_dummy_channel_gets_full_rsi_loop_with_no_code_change(self):
        dummy = {
            "slug": "astro",
            "label": "AST",
            "name": "Astro Chronicles",
            "short": "Astro",
            "home": False,
            "order": 9,
            "repo": {"url": "https://github.com/example/astro-chronicles.git", "env": "ASTRO_REPO", "checkouts": ["astro-chronicles"]},
            "title_match": r"\bAST\b|astro chronicles",
            "wip": {"limit": 2, "line": "next_astro"},
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            astro_analytics = tmp_path / "05_Analytics" / "astro"
            (astro_analytics / "snapshots").mkdir(parents=True)
            (astro_analytics / "launch").mkdir(parents=True)
            (astro_analytics / "autopsy").mkdir(parents=True)

            # Patch only the channel registry + analytics_dir for the dummy channel (zero engine code change).
            real_all = channels.all_channels()
            extended = tuple(real_all + [dummy])
            real_adir = channels.analytics_dir

            def fake_adir(slug):
                return astro_analytics if slug == "astro" else real_adir(slug)

            with mock.patch.object(channels, "_load", return_value=extended), \
                 mock.patch.object(channels, "analytics_dir", side_effect=fake_adir):
                # 1. Backlog expansion generates weekly-improvement-astro automatically.
                expanded = refill.load_backlog()
                astro_item = next((it for it in expanded if it["key"] == "weekly-improvement-astro"), None)
                self.assertIsNotNone(astro_item)
                self.assertEqual(astro_item["repo"], "astro")
                self.assertEqual(astro_item["every_h"], 168)
                self.assertIn("Astro Chronicles", astro_item["title"])
                self.assertIn("astro-chronicles", astro_item["body"])

                # 2. Before analytics sign-in / first 48h read, the dummy channel waits cleanly (does not queue yet).
                reg_doc = {"max_live_per_channel": 3, "experiments": []}
                self.assertFalse(rsi.channel_cycle_ready("astro", reg_doc))
                q = {"next_id": 1, "jobs": []}
                with mock.patch.object(rsi, "load_register", return_value=reg_doc):
                    refill.do_refill(q, [astro_item], NOW)
                self.assertEqual(q["jobs"], [])

                # 3. Once the dummy channel gets its first 48-hour launch read, refill queues its cycle automatically!
                (astro_analytics / "launch" / "vidAstro001.json").write_text(json.dumps({
                    "id": "vidAstro001", "channel": "astro", "format": "long",
                    "readings": [{"hours": 48, "views": 180, "impressions": 4200, "ctr": 4.2}],
                }))
                self.assertTrue(rsi.channel_cycle_ready("astro", reg_doc))
                # Even with a full ready queue (4 pipeline jobs), the guaranteed weekly cycle still queues.
                for i in range(4):
                    jobs.do_add(q, title=f"pipeline {i}", needs="mini", body="", by="chief", at=NOW)
                with mock.patch.object(rsi, "load_register", return_value=reg_doc):
                    added = refill.do_refill(q, [astro_item], NOW)
                self.assertEqual(len(added), 1)
                self.assertEqual(q["jobs"][-1]["backlog"], "weekly-improvement-astro")
                self.assertEqual(q["jobs"][-1]["repo"], "astro")

                # 4. Autopsy -> Hypothesis ingestion automatically picks up the dummy channel's autopsy.
                (astro_analytics / "autopsy" / "vidAstro001_48h.md").write_text(
                    "# Retention Autopsy: vidAstro001 (48h)\n\n"
                    "## Concrete Fixes\n"
                    "- [this video] Test a brighter spacecraft thumbnail via Test & Compare to raise CTR from 2.1% to 4.0%\n"
                    "- [next film] Payoff number spoken in the first 5 s raises 0:30 retention from 40% to 50% over the next 4 longs\n"
                )
                cands = rsi.ingest_autopsies(reg_doc, slugs=["astro"])
                self.assertEqual(len(cands), 2)
                by_type = {c["test_type"]: c for c in cands}
                self.assertEqual(by_type["test_and_compare"]["applies_to"], ["vidAstro001"])
                self.assertEqual(by_type["next_n_films"]["applies_to"], ["next 4 AST longs"])
                self.assertEqual(by_type["next_n_films"]["min_sample"], 4)
                # Idempotent re-ingest
                self.assertEqual(rsi.ingest_autopsies(reg_doc, slugs=["astro"]), [])

                # 5. Start one candidate & confirm dashboard block automatically includes the dummy channel row!
                rsi.start_experiment(reg_doc, by_type["next_n_films"]["id"], readout_date="2026-12-10", now=NOW)
                self.assertEqual(rsi.validate_register(reg_doc), [])
                block = rsi.board_section(reg_doc, None, "2026-11-20T23:00:00Z", now=NOW)
                astro_row = next((r for r in block["channels"] if r["slug"] == "astro"), None)
                self.assertIsNotNone(astro_row)
                self.assertEqual(astro_row["name"], "Astro Chronicles")
                self.assertEqual(astro_row["runningCount"], 1)
                self.assertEqual(astro_row["autopsyCount"], 1)
                self.assertEqual(astro_row["running"][0]["readoutDate"], "2026-12-10")


class OpsLoopTest(unittest.TestCase):
    def test_measures_all_six_metrics_names_bottleneck_queues_fix_and_compares_next_week(self):
        t0 = dt.datetime(2026, 11, 14, 0, 0, tzinfo=dt.timezone.utc)
        q = {"next_id": 100, "jobs": [
            {
                "id": "J1", "title": "OWB 030 script", "repo": "owb", "film": "030", "needs": "mini", "kind": "script",
                "status": "done", "by": "cursor",
                "history": [
                    {"at": "2026-11-15T00:00:00Z", "by": "chief", "what": "added"},
                    {"at": "2026-11-15T10:00:00Z", "by": "cursor", "what": "claimed"},
                    {"at": "2026-11-15T11:00:00Z", "by": "cursor", "what": "done: PASS"},
                ],
            },
            {
                "id": "J2", "title": "OWB 030 QA review", "repo": "owb", "film": "030", "needs": "mini", "kind": "review",
                "status": "done", "by": "macbook-2",
                "history": [
                    {"at": "2026-11-16T00:00:00Z", "by": "chief", "what": "added"},
                    {"at": "2026-11-16T01:00:00Z", "by": "gemini", "what": "claimed"},
                    {"at": "2026-11-16T02:00:00Z", "by": "relay", "what": "reclaimed: stalled after 25m"},
                    {"at": "2026-11-16T03:00:00Z", "by": "chief", "what": "reopened: needs fixes"},
                    {"at": "2026-11-16T04:00:00Z", "by": "macbook-2", "what": "done: PASS"},
                ],
            },
            {
                "id": "J3", "title": "OWB 030 Ben watch handoff", "repo": "owb", "film": "030", "needs": "ben",
                "awaits_ben": True, "status": "open",
                "history": [{"at": "2026-11-17T00:00:00Z", "by": "chief", "what": "added"}],
            },
            {
                "id": "J4", "title": "Parked review", "repo": "owb", "needs": "mini", "kind": "review",
                "status": "blocked", "result": "parked for Chief: check",
                "history": [
                    {"at": "2026-11-18T00:00:00Z", "by": "cursor", "what": "added"},
                    {"at": "2026-11-18T01:00:00Z", "by": "cursor", "what": "blocked: parked for Chief: check"},
                ],
            },
        ]}
        spend = [
            {"kind": "spend", "pool": "elevenlabs", "amount": 12000, "film": "OWB:030"},
            {"kind": "spend", "pool": "flow", "amount": 250, "film": "OWB:030"},
        ]
        rep = ops_loop.measure(q, spend_rows=spend, as_of=NOW)
        m = rep["metrics"]
        self.assertEqual(m["done_7d_total"], 2)
        self.assertGreater(m["jobs_per_day_by_machine"]["mini"], 0)
        self.assertGreater(m["jobs_per_day_by_machine"]["macbook"], 0)
        self.assertGreater(m["idle_agent_hours_with_ready_work"], 0)
        self.assertEqual(m["stalls_7d"], 1)
        self.assertEqual(m["parks_7d"], 1)
        self.assertEqual(m["currently_parked_for_chief"], 1)
        self.assertEqual(m["chief_fix_rate_pct"], 50.0)
        self.assertEqual(m["median_job_to_ben_watch_h"], 48.0)
        self.assertEqual(m["credit_spend_per_finished_film"]["elevenlabs"], 12000.0)
        self.assertEqual(m["credit_spend_per_finished_film"]["flow"], 250.0)
        self.assertEqual(rep["bottleneck"]["key"], "idle_dispatch")

        # Queue fix once; second call deduplicates.
        jid = ops_loop.queue_bottleneck_fix(q, rep, NOW)
        self.assertIsNotNone(jid)
        self.assertIsNone(ops_loop.queue_bottleneck_fix(q, rep, NOW))

        # Week-over-week comparison proves improvement when idle hours drop.
        next_week = json.loads(json.dumps(rep))
        next_week["metrics"]["idle_agent_hours_with_ready_work"] = 2
        cmp = ops_loop.compare_previous(next_week, [rep])
        self.assertEqual(cmp["verdict"], "helped")
        self.assertIn("helped", cmp["plain"])

    def test_board_publish_add_learning_and_quiet_updated_at(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp)
            (p / "05_Analytics" / "ops_loop").mkdir(parents=True)
            (p / "05_Analytics" / "EXPERIMENTS.json").write_text((ROOT / "05_Analytics" / "EXPERIMENTS.json").read_text())
            (p / "05_Analytics" / "ops_loop" / "latest.json").write_text(json.dumps({
                "measured_at": "2026-11-20T23:00:00Z",
                "metrics_line": "10.0 jobs/day · 4 idle h",
                "bottleneck": {"title": "One agent at a time on the Mini", "summary": "Serial lock slows throughput.", "proposed_fix": "Allow parallel slots."},
                "previous_comparison": {"plain": "First weekly baseline."},
            }))
            board = {}
            with mock.patch.object(board_publish, "wt", return_value=p), \
                 mock.patch.object(board_publish, "STATE", p):
                board_publish.add_learning(board, NOW)
            self.assertIn("learning", board)
            self.assertEqual(board["learning"]["title"], "What the studio is learning")
            self.assertEqual(board["learning"]["ops"]["bottleneck"], "One agent at a time on the Mini")

            # Quiet publish keeps updatedAt stable when nothing changes.
            first = board["learning"]
            second = rsi.board_section(
                json.loads((p / "05_Analytics" / "EXPERIMENTS.json").read_text()),
                json.loads((p / "05_Analytics" / "ops_loop" / "latest.json").read_text()),
                "2026-11-20T23:05:00Z",
                previous=first,
                now=NOW,
            )
            self.assertEqual(second["updatedAt"], first["updatedAt"])


if __name__ == "__main__":
    unittest.main()
