"""Upload and daily sweeps must use current gates, not cached PASS labels."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess as sp
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publishing_gates as g  # noqa: E402
import scheduled_gates as sg  # noqa: E402

try:
    import numpy as np
    import test_music_gate as tmg
except ImportError:
    np = tmg = None

REAL_MEDIA_OK = np is not None and shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


class Publishing(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "studio").mkdir()
        (self.root / "studio/channel.json").write_text("{}")
        self.video = self.root / "short.mp4"
        self.video.write_bytes(b"cut")
        self.meta = self.video.with_name("short_meta.json")
        self.meta.write_text(json.dumps(dict(
            sha256=hashlib.sha256(b"cut").hexdigest(),
            publishing_gates={k: k for k in ["film", "bed", "cuts", "vo", "sfx"]},
        )))

    def check(self, fmt="short", **kwargs):
        return g.evaluate(self.video, self.root, fmt, "2026-12-01", short_run=lambda c: (0, "PASS"), **kwargs)

    def test_reused_bed_blocks_upload_even_with_recorded_pass(self):
        def run(c, **_kw):
            return (1, "FAIL reused: same bed (0.830)") if "music_gate.py" in c[1] else (0, "PASS")
        with patch.object(g, "run", side_effect=run):
            result = self.check()
        self.assertFalse(result["ok"])
        self.assertTrue(result["needs_watch"])
        self.assertIn("music", result["failed_gates"])
        self.assertIn("0.830", result["checks"][1]["output"])

    def test_gate_applied_waiver_passes_both_formats(self):
        with patch.object(g, "run", return_value=(0, "WAIVED reused: Chief waiver\nPASS")):
            for fmt in ["short", "long"]:
                res = self.check(fmt)
                self.assertTrue(res["ok"])
                self.assertTrue(res["waived"])

    def test_shorts_chief_waiver_passes_exact_fail_but_never_tool_error(self):
        fail_out = "FAIL  short.mp4\n   FAIL  Orbit in frame at 0 s (visor 0.0048 >= 0.003)\n"
        (self.root / "short_gate.json").write_text(json.dumps({
            "waivers": [{"fail": "Orbit in frame at 0 s (visor 0.0048 >= 0.003)", "waived_by": "Chief J3291"}]
        }))
        with patch.object(g, "run", return_value=(0, "PASS")):
            res = g.evaluate(self.video, self.root, "short", "2026-12-01", short_run=lambda c: (1, fail_out))
            self.assertTrue(res["ok"])
            self.assertTrue(res["waived"])
            # Tool errors (exit 2) can never be waived.
            res_err = g.evaluate(self.video, self.root, "short", "2026-12-01", short_run=lambda c: (2, fail_out))
            self.assertFalse(res_err["ok"])

    def test_missing_inputs_and_tool_errors_block(self):
        self.meta.write_text("{}")
        with patch.object(g, "run", return_value=(2, "unavailable")):
            res = self.check()
        self.assertFalse(res["ok"])
        self.assertFalse(res["needs_watch"])

    def test_changed_export_blocks_even_when_gates_pass(self):
        self.video.write_bytes(b"new cut")
        with patch.object(g, "run", return_value=(0, "PASS")):
            res = self.check()
        self.assertFalse(res["ok"])
        self.assertIn("identity", res["failed_gates"])

    def test_new_unknown_required_gate_cannot_silently_pass(self):
        (self.root / "studio/channel.json").write_text('{"publishing_gates":{"required":["new_gate"]}}')
        with patch.object(g, "run", return_value=(0, "PASS")):
            res = self.check()
        self.assertFalse(res["ok"])
        self.assertIn("new_gate", res["failed_gates"])

    def test_derives_film_bed_and_stems_for_legacy_exports_without_publishing_gates_block(self):
        film = self.root / "02_Video-Projects" / "031_Magnetic-Flip"
        (film / "05_Music").mkdir(parents=True)
        bed = film / "05_Music" / "flip_score_bed_v01.mp3"
        bed.write_bytes(b"bed")
        (film / "05_Music" / "flip_score_bed_v01_plan.json").write_text('{"prompt":"Pace: 60-80 BPM. NOT other."}')
        out_dir = film / "10_Shorts" / "s1" / "06_Final-Exports"
        out_dir.mkdir(parents=True)
        vid = out_dir / "s1_v01.mp4"
        vid.write_bytes(b"mp4")
        (out_dir / "s1_v01_vo.wav").write_bytes(b"vo")
        (out_dir / "s1_v01_sfx.wav").write_bytes(b"sfx")
        (self.root / "studio/channel.json").write_text('{"slug":"owb","analytics":{"open_gate_library":true}}')
        calls = []
        def fake_run(cmd, **_kw):
            calls.append(cmd)
            return (0, "PASS")
        with patch.object(g, "run", side_effect=fake_run):
            res = g.evaluate(vid, self.root, "short", "2026-12-01", short_run=lambda c: (0, "PASS"))
        self.assertTrue(res["ok"], res)
        self.assertTrue(any("music_gate.py" in c[1] and str(bed) in c for c in calls))
        self.assertTrue(any("sfx_kit.py" in c[1] for c in calls))

    def test_channel_specific_gates_for_hos_and_ww2(self):
        # WW2 long requires music + archive_provenance (and does NOT require OWB picture_qa).
        ww2 = self.root / "ww2"
        (ww2 / "studio").mkdir(parents=True)
        (ww2 / "studio/channel.json").write_text('{"slug":"ww2","shorts":{"planned_per_long":0}}')
        film = ww2 / "02_Video-Projects" / "001_Mulberry"
        (film / "05_Music").mkdir(parents=True)
        (film / "05_Music/score_v01.mp3").write_bytes(b"bed")
        (film / "05_Music/score_v01_plan.json").write_text('{"prompt":"Pace: 70-90 BPM. NOT other."}')
        (film / "09_Final-Export").mkdir(parents=True)
        vid = film / "09_Final-Export/mulberry_v01.mp4"
        vid.write_bytes(b"long")
        with patch.object(g, "run", return_value=(0, "PASS")):
            fail_res = g.evaluate(vid, ww2, "long", "2026-12-01")
        self.assertFalse(fail_res["ok"])
        self.assertEqual(fail_res["failed_gates"], ["archive_provenance"])
        self.assertFalse(fail_res["needs_watch"])
        (film / "03_Picture").mkdir(parents=True)
        (film / "03_Picture/ARCHIVE_PROVENANCE.md").write_text("# Provenance\nNARA RG-111 public domain.\n")
        with patch.object(g, "run", return_value=(0, "PASS")):
            pass_res = g.evaluate(vid, ww2, "long", "2026-12-01")
        self.assertTrue(pass_res["ok"], pass_res)

        # HOS requires lint_package in addition to music/sfx.
        hos = self.root / "hos"
        (hos / "studio").mkdir(parents=True)
        (hos / "studio/channel.json").write_text('{"slug":"hos"}')
        (hos / "07_Content-Ops/scripts").mkdir(parents=True)
        (hos / "07_Content-Ops/scripts/package-lint.ts").write_text("// stub\n")
        hfilm = hos / "02_Video-Projects" / "007_Vaccine"
        (hfilm / "05_Music").mkdir(parents=True)
        (hfilm / "05_Music/vac_bed.mp3").write_bytes(b"bed")
        (hfilm / "05_Music/vac_bed_plan.json").write_text('{"prompt":"Pace: 60-80 BPM. NOT other."}')
        (hfilm / "09_Final-Export").mkdir(parents=True)
        hvid = hfilm / "09_Final-Export/vac_v01.mp4"
        hvid.write_bytes(b"long")
        (hfilm / "09_Final-Export/vac_v01_vo.wav").write_bytes(b"vo")
        (hfilm / "09_Final-Export/vac_v01_sfx.wav").write_bytes(b"sfx")
        seen = []
        def fake_hos(cmd, **_kw):
            seen.append(cmd)
            return (0, "PASS")
        with patch.object(g, "run", side_effect=fake_hos):
            hres = g.evaluate(hvid, hos, "long", "2026-12-01")
        self.assertTrue(hres["ok"], hres)
        self.assertTrue(any("package-lint.ts" in " ".join(c) and "007" in c for c in seen))

    @unittest.skipUnless(REAL_MEDIA_OK, "needs numpy, ffmpeg and ffprobe")
    def test_real_music_gate_refuses_reused_bed_and_passes_with_chief_waiver(self):
        """End-to-end with real synthetic audio + real music_gate.py: reused bed FAILs, Chief waiver PASSes."""
        ch = self.root / "owb_real"
        (ch / "studio").mkdir(parents=True)
        (ch / "studio/channel.json").write_text('{"slug":"owb","analytics":{"open_gate_library":true}}')
        film_a = ch / "02_Video-Projects" / "024_Light"
        film_b = ch / "02_Video-Projects" / "023_Venus"
        (film_a / "05_Music").mkdir(parents=True)
        (film_b / "05_Music").mkdir(parents=True)
        track = tmg.piece(7, secs=40, bpm=72)
        bed_a = film_a / "05_Music" / "muons_bed_v01.mp3"
        bed_b = film_b / "05_Music" / "venus_bed_v01.mp3"
        tmg.save(track, bed_a)
        tmg.save(track[4 * tmg.SR:], bed_b, "96k")  # reused bed, offset & re-encoded
        (film_a / "05_Music" / "muons_bed_v01_plan.json").write_text(json.dumps({"prompt": tmg.PROMPT}))
        exp_dir = film_a / "10_Shorts" / "muons" / "06_Final-Exports"
        exp_dir.mkdir(parents=True)
        vid = exp_dir / "muons_v05.mp4"
        sp.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=64x36:d=25", str(vid)], check=True)
        (exp_dir / "muons_v05_vo.wav").write_bytes(b"vo")
        (exp_dir / "muons_v05_sfx.wav").write_bytes(b"sfx")

        real_run = g.run
        def run_music_real_only(cmd, **kw):
            if "music_gate.py" in str(cmd[1]):
                return real_run(cmd, **kw)
            return (0, "PASS")

        with patch.object(g, "run", side_effect=run_music_real_only):
            blocked = g.evaluate(vid, ch, "short", "2026-12-01", short_run=lambda c: (0, "PASS"))
        self.assertFalse(blocked["ok"])
        self.assertEqual(blocked["failed_gates"], ["music"])
        self.assertTrue(blocked["needs_watch"])
        music_chk = next(c for c in blocked["checks"] if c["gate"] == "music")
        self.assertIn("reused: sounds like venus_bed_v01.mp3", music_chk["output"])

        # Add Chief waiver in the existing music_gate_*_chief_waiver.json format -> PASSes!
        waiver = film_a / "05_Music" / "music_gate_v01_chief_waiver.json"
        waiver.write_text(json.dumps({"accept": True, "by": "chief", "bed": bed_a.name, "waive": ["reused"]}))
        with patch.object(g, "run", side_effect=run_music_real_only):
            allowed = g.evaluate(vid, ch, "short", "2026-12-01", short_run=lambda c: (0, "PASS"))
        self.assertTrue(allowed["ok"], allowed)
        self.assertTrue(allowed["waived"])

    def test_daily_flags_failing_bed_ten_days_ahead_for_short_and_long_and_merges_uploads(self):
        spec = importlib.util.spec_from_file_location("upcoming_test", g.ROOT / "00_Brand/Channel-Setup/tools/gate_upcoming.py")
        upcoming = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(upcoming)
        at_short = datetime.now(timezone.utc) + timedelta(days=10)
        at_long = datetime.now(timezone.utc) + timedelta(days=11)
        long_vid = self.root / "long.mp4"
        long_vid.write_bytes(b"longcut")
        long_vid.with_name("long_meta.json").write_text(json.dumps(dict(
            sha256=hashlib.sha256(b"longcut").hexdigest(),
            publishing_gates={k: k for k in ["film", "bed", "cuts", "vo", "sfx"]},
        )))
        (self.root / "snap.json").write_text(json.dumps({"videos": [
            dict(id="short1", format="short", privacy="private", publishAt=at_short.isoformat(), title="Muons"),
            dict(id="long1", format="long", privacy="private", publishAt=at_long.isoformat(), title="Long Film"),
        ]}))
        # Split across two UPLOADS files (as HOS keeps Shorts in studio social/hos/UPLOADS.json).
        (self.root / "uploads_main.json").write_text(json.dumps({"videos": {"long1": {"file": "long.mp4"}}}))
        (self.root / "uploads_extra.json").write_text(json.dumps({"videos": {"short1": {"file": "short.mp4"}}}))
        def run(c, **_kw):
            return (1, "FAIL reused: 0.830") if "music_gate.py" in c[1] else (0, "PASS")
        with patch.object(g, "run", side_effect=run), patch.object(upcoming, "run", return_value=(0, "PASS")):
            upcoming.main([
                "--snapshot", str(self.root / "snap.json"),
                "--uploads", str(self.root / "uploads_main.json"),
                "--extra-uploads", str(self.root / "uploads_extra.json"),
                "--media-root", str(self.root),
                "--out", str(self.root / "report.md"),
            ])
        rows = json.loads((self.root / "report.json").read_text())
        self.assertEqual([r["id"] for r in rows], ["short1", "long1"])
        for row in rows:
            self.assertFalse(row["ok"])
            self.assertTrue(row["needs_watch"])
            self.assertIn("0.830", row["output"])

    def test_only_near_term_fails_queue_one_chief_fix_and_alert_ben_only_if_watch_needed(self):
        now = datetime.now(timezone.utc)
        rows = [
            dict(channel="owb", id="near_meta", title="Meta", ok=False, needs_watch=False, failed_gates=["inputs"],
                 publishAt=(now + timedelta(days=3)).isoformat(), output="inputs missing"),
            dict(channel="owb", id="near_cut", title="Muons Short", ok=False, needs_watch=True, failed_gates=["music"],
                 publishAt=(now + timedelta(hours=18)).isoformat(), output="music FAIL 0.830"),
            dict(channel="hos", id="far_cut", title="Far", ok=False, needs_watch=True, failed_gates=["music"],
                 publishAt=(now + timedelta(days=10)).isoformat(), output="music FAIL"),
        ]
        data = {"jobs": [], "next": 1}
        delivered = []
        import jobs
        counter = [0]
        def add(d, **kwargs):
            counter[0] += 1
            job = dict(kwargs, id=f"J-test-{counter[0]}", status="open")
            d["jobs"].append(job)
            return job
        state_file = self.root / "alerts.json"
        with patch.object(jobs, "do_add", side_effect=add):
            added = sg.queue_fixes(data, rows, now, root=self.root, alert_state_path=state_file,
                                   deliver_fn=lambda ev, _r: (delivered.append(ev) or {"status": "ok"}))
            self.assertEqual(added, ["J-test-1", "J-test-2"])
            # Second run deduplicates both jobs and alerts.
            self.assertEqual(sg.queue_fixes(data, rows, now, root=self.root, alert_state_path=state_file,
                                            deliver_fn=lambda ev, _r: (delivered.append(ev) or {"status": "ok"})), [])
        by_key = {j["scheduled_gate_fix"]: j for j in data["jobs"]}
        self.assertEqual(by_key["owb:near_meta"]["kind"], "chief")
        self.assertFalse(by_key["owb:near_meta"]["needs_ben_watch"])
        self.assertNotIn("ben_alert_required", by_key["owb:near_meta"])
        self.assertTrue(by_key["owb:near_cut"]["needs_ben_watch"])
        self.assertTrue(by_key["owb:near_cut"]["ben_alert_required"])
        self.assertEqual(len(delivered), 1)
        self.assertEqual(delivered[0]["videoId"], "near_cut")

    def test_sweep_isolates_channel_errors_and_skips_prelaunch(self):
        now = datetime(2026, 11, 21, 13, 0, tzinfo=timezone.utc)
        for slug in ("good", "stale", "pre"):
            (self.root / slug / "studio").mkdir(parents=True)
            (self.root / slug / "studio/channel.json").write_text(json.dumps({"slug": slug}))
            (self.root / "analytics" / slug / "snapshots").mkdir(parents=True)
        # good: fresh snapshot, empty upcoming
        (self.root / "analytics/good/snapshots/2026-11-21.json").write_text(json.dumps({"takenAt": (now - timedelta(hours=2)).isoformat(), "videos": []}))
        good_up = self.root / "good/UPLOADS.json"
        good_up.write_text('{"videos":{}}')
        # stale: 50h old snapshot
        (self.root / "analytics/stale/snapshots/2026-11-19.json").write_text(json.dumps({"takenAt": (now - timedelta(hours=50)).isoformat(), "videos": []}))
        stale_up = self.root / "stale/UPLOADS.json"
        stale_up.write_text('{"videos":{}}')
        # pre: no snapshot and no uploads (prelaunch)
        with patch.object(sg.channels, "slugs", return_value=["stale", "pre", "good"]), \
             patch.object(sg.channels, "get", side_effect=lambda s: {"slug": s, "launch_state": "prelaunch" if s == "pre" else "live"}), \
             patch.object(sg.channels, "checkout", side_effect=lambda s: self.root / s), \
             patch.object(sg.channels, "analytics_dir", side_effect=lambda s: self.root / "analytics" / s), \
             patch.object(sg, "_uploads_files_for", side_effect=lambda s: {"good": [good_up], "stale": [stale_up], "pre": []}[s]):
            outcome = sg.sweep(now=now)
        self.assertEqual(outcome["channels"]["good"]["status"], "checked")
        self.assertEqual(outcome["channels"]["pre"]["status"], "skipped")
        self.assertEqual(outcome["channels"]["stale"]["status"], "error")
        self.assertEqual(len(outcome["errors"]), 1)
        self.assertTrue((self.root / "analytics/good/UPCOMING_PUBLISHING_GATES.md").is_file())

    def test_refill_daily_sweep_deduplicates(self):
        import jobs
        data = {"jobs": []}
        now = datetime.now(timezone.utc)
        def add(d, **kwargs):
            job = dict(kwargs, id="J-daily", status="open")
            d["jobs"].append(job)
            return job
        with patch.object(jobs, "do_add", side_effect=add):
            self.assertEqual(sg.queue_daily(data, now), ["J-daily"])
            self.assertEqual(sg.queue_daily(data, now + timedelta(days=1)), [])


if __name__ == "__main__":
    unittest.main()
