#!/usr/bin/env python3
"""Tests for picture_qa.py's source checks (no video needed): python3 scripts/test_picture_qa.py"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import picture_qa as qa  # noqa: E402


def cut(source, t0, t1, up=1.0, row="1"):
    return dict(row=row, timeline_in=t0, timeline_out=t1, source=source, framing={}, upscale=up)


POOL = {"pia12337": "Computer Reconstruction of Spirit Predicament", "pia12102": "Spirit Photographs Her Underbelly, Sol 1925",
        "pia14839": "Curiosity Sky Crane Maneuver, Artist Concept", "pia00001": "Mars Traverse Map (Annotated)"}


class SourceChecks(unittest.TestCase):
    def test_the_2_54_computer_model_fails_at_its_film_time(self):
        r = qa.source_checks([cut("PIA12337.jpg", 170.73, 175.97, 1.84)], POOL)[0]
        self.assertEqual(r["at"], "2:53")
        self.assertTrue(any("computer reconstruction" in w for w in r["fail"]))

    def test_a_real_photo_passes_and_an_artist_concept_is_a_look(self):
        rows = qa.source_checks([cut("PIA12102.jpg", 0, 5), cut("PIA14839.jpg", 5, 10)], POOL)
        self.assertEqual((rows[0]["fail"], rows[0]["warn"]), ([], []))
        self.assertEqual(rows[1]["fail"], [])
        self.assertTrue(rows[1]["warn"][0].startswith("kind of picture"))

    def test_annotated_maps_fail_on_the_label_not_the_map(self):
        r = qa.source_checks([cut("PIA00001.jpg", 0, 5)], POOL)[0]
        self.assertTrue(any("annotated" in w for w in r["fail"]))

    def test_sharpness_and_reuse(self):
        rows = qa.source_checks([cut("PIA12102.jpg", 0, 5, 2.4), cut("PIA12102.jpg", 5, 10, 2.1),
                                 cut("PIA12102.jpg", 10, 15, 1.5)], POOL)
        self.assertTrue(any(w.startswith("sharpness: upscaled 2.40x") for w in rows[0]["fail"]))
        self.assertTrue(any(w.startswith("sharpness") for w in rows[1]["warn"]))
        self.assertFalse(any(w.startswith("reuse") for r in rows for w in r["fail"]))  # back to back: one appearance

    def test_a_still_may_appear_twice(self):
        rows = qa.source_checks([cut("PIA12102.jpg", 0, 5), cut("x.jpg", 5, 10), cut("PIA12102.jpg", 10, 15),
                                 cut("x.jpg", 15, 20), cut("PIA12102.jpg", 20, 25)], POOL)
        self.assertEqual([any(w.startswith("reuse: appears 3 times") for w in r["fail"]) for r in rows],
                         [False, False, False, False, True])

    def test_footage_counts_stretches_not_files(self):
        def clip(t0, off, row="1"):
            return dict(cut("gerst.webm", t0, t0 + 4, row=row), framing={"offset": off})
        cuts = [clip(0, 40), cut("a.jpg", 4, 8), clip(8, 120), cut("b.jpg", 12, 16), clip(16, 44), cut("c.jpg", 20, 24)]
        rows = qa.source_checks(cuts, POOL)
        self.assertFalse(any(w.startswith("reuse") for w in rows[2]["fail"]))           # a new stretch is a new picture
        self.assertTrue(any(w.startswith("reuse: same stretch as 0:02") for w in rows[4]["fail"]))
        many = []
        for i, off in enumerate((0, 20, 40, 60, 80, 100)):
            many += [clip(i * 8, off), cut(f"s{i}.jpg", i * 8 + 4, i * 8 + 8)]
        rows = qa.source_checks(many, POOL)
        self.assertFalse(any(w.startswith("reuse") for w in rows[8]["fail"]))
        self.assertTrue(any(w.startswith("reuse: 6 stretches") for w in rows[10]["fail"]))

    def test_a_ruling_on_one_stretch_leaves_the_rest_judged(self):
        cuts = [dict(cut("gerst.webm", 0, 4), framing={"offset": 250}), cut("a.jpg", 4, 8),
                dict(cut("gerst.webm", 8, 12), framing={"offset": 120})]
        rows = qa.source_checks(cuts, {"gerst": "Earth from the ISS (Annotated)", "a": "A photo"})
        qa.apply_reviewed(rows, {"gerst.webm@250": {"note": "lit", "kinds": ["kind of picture"]}})
        self.assertEqual(rows[0]["fail"], [])
        self.assertTrue(rows[2]["fail"])

    def test_a_run_that_replays_its_own_frames(self):
        cuts = [dict(cut("tides.mp4", 0, 4), framing={"offset": 0}), dict(cut("tides.mp4", 4, 8), framing={"offset": 4}),
                dict(cut("tides.mp4", 8, 12), framing={"offset": 6}), dict(cut("tides.mp4", 12, 17), framing={"offset": 10})]
        rows = qa.source_checks(cuts, POOL)
        self.assertEqual([any("replays frames" in w for w in r["fail"]) for r in rows], [False, False, True, False])
        self.assertTrue(any(w.startswith("reuse: on screen 17.0s") for w in rows[0]["warn"]))

    def test_unknown_sources_are_a_look_but_our_own_clips_are_not(self):
        rows = qa.source_checks([cut("mystery.jpg", 0, 5), cut("orbit_mars_cold_omni_v01.mp4", 5, 10)], POOL)
        self.assertTrue(rows[0]["warn"][0].startswith("kind of picture: no title"))
        self.assertEqual(rows[1]["warn"], [])

    def test_claudes_ruling_passes_only_the_kinds_named(self):
        rows = qa.source_checks([cut("PIA12337.jpg", 0, 5, 2.4)], POOL)
        qa.apply_reviewed(rows, {"PIA12337.jpg": {"note": "story needs it", "kinds": ["kind of picture"]}})
        self.assertEqual(len(rows[0]["fail"]), 1)
        self.assertTrue(rows[0]["fail"][0].startswith("sharpness"))
        self.assertEqual(rows[0]["reviewed_ok"]["note"], "story needs it")

    def test_pool_flags_labels_and_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "pool.json"
            f.write_text(json.dumps([{"id": "eso1702a", "title": "Alpha Centauri over the VLT", "labels": True},
                                     {"file_id": "PIA12102", "title": "Spirit Photographs Her Underbelly", "reject": "out-of-focus MI mosaic"}]))
            pool = qa.load_pool([f])
            rows = qa.source_checks([cut("eso1702a.jpg", 0, 5), cut("PIA12102.jpg", 5, 10)], pool)
            self.assertIn("labels", rows[0]["fail"][0])
            self.assertIn("out-of-focus", rows[1]["fail"][0])

    def test_pool_formats_and_the_report(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "a.json").write_text(json.dumps([{"file_id": "PIA12337", "title": POOL["pia12337"]}]))
            (d / "b.json").write_text(json.dumps({"items": [{"id": "eso1629g", "title": "Proxima Centauri"}]}))
            pool = qa.load_pool([d / "a.json", d / "b.json"])
            self.assertEqual(pool["eso1629g"], "Proxima Centauri")
            (d / "cuts.json").write_text(json.dumps([cut("PIA12337.jpg", 170.73, 175.97, 1.84), cut("eso1629g.jpg", 0, 5)]))
            code = qa.main(["--cuts", str(d / "cuts.json"), "--pool", str(d / "a.json"), "--pool", str(d / "b.json"),
                            "--out-dir", str(d / "out")])
            self.assertEqual(code, 1)
            md = (d / "out" / "PICTURE_QA.md").read_text()
            self.assertIn("# Picture QA: FAIL", md)
            self.assertIn("**2:53** row 1", md)


if __name__ == "__main__":
    unittest.main()
