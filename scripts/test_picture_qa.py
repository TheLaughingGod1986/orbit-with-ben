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
        self.assertTrue(all(any(w.startswith("reuse: used 3 times") for w in r["fail"]) for r in rows))

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
