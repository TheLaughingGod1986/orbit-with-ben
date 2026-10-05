import pathlib, subprocess, sys, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import vo_take  # noqa: E402

SCRIPT = """# Title

Open line one.
Open line two.

[VISUAL MUST: not spoken]
[TEACH: not spoken]

[CHAPTER CARD: First Act]

Para one.

Para two continues
on a second line.

[SUBSCRIBE BEAT]
We make one of these every week.

<!-- HOOK ESCALATION -->
"""


class Chapters(unittest.TestCase):
    def test_prose_only_split_at_cards(self):
        ch = vo_take.spoken_chapters(SCRIPT)
        self.assertEqual([c["title"] for c in ch], ["open", "First Act"])
        self.assertEqual(ch[0]["text"], "Open line one. Open line two.")
        self.assertEqual(ch[1]["text"], "Para one.\n\nPara two continues on a second line.\n\nWe make one of these every week.")

    def test_matches_hand_built_026_parts(self):
        root = pathlib.Path(__file__).resolve().parents[2]
        try:
            md = subprocess.check_output(["git", "-C", str(root), "show",
                "c7ced8c:02_Video-Projects/026_How-Far-Is-The-Nearest-Star/01_Script/nearest_star_script_master_v01.md"],
                text=True, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.skipTest("026 LOCK commit not in this checkout")
        parts = root / "02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/parts"
        ch = vo_take.spoken_chapters(md)
        self.assertEqual(len(ch), 6)
        for i, c in enumerate(ch):
            ref = sorted(parts.glob(f"nearest_star_vo_v01_ch{i:02d}_*.txt"))[0].read_text().strip()
            self.assertEqual(c["text"], ref)


class Checks(unittest.TestCase):
    def test_diff_ignores_punctuation(self):
        d = vo_take.script_diff("Next week: what if Earth stopped spinning?", "Next week, what if Earth stopped spinning?")
        self.assertTrue(d["exact_match"])
        self.assertEqual(d["match_rate_pct"], 100.0)

    def test_diff_reports_mismatch(self):
        d = vo_take.script_diff("a cherry far away", "a grapefruit far away")
        self.assertFalse(d["exact_match"])
        self.assertEqual(d["mismatches"], [{"op": "replace", "script": ["cherry"], "scribe": ["grapefruit"]}])

    def test_verdict(self):
        good = {"exact_match": False, "match_rate_pct": 98.6}
        self.assertEqual(vo_take.verdict(good, -20.6), "PASS")
        self.assertEqual(vo_take.verdict({"exact_match": False, "match_rate_pct": 90.0}, -20.0), "REVIEW")
        self.assertTrue(vo_take.verdict(good, -50.0).startswith("FAIL"))
        self.assertTrue(vo_take.verdict(good, None).startswith("FAIL"))

    def test_floor(self):
        self.assertIsNone(vo_take.spend_check(77_155, 6_300, 50_000))
        self.assertIn("STOP", vo_take.spend_check(52_000, 6_300, 50_000))
        self.assertIsNone(vo_take.spend_check(None, 6_300, 50_000))

    def test_cli_needs_order_and_refuses_existing_stem(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(vo_take.main(["--text", "hi", "--out", d, "--stem", "x", "--dry-run"]), 2)
            self.assertEqual(vo_take.main(["--text", "hi", "--out", d, "--stem", "x", "--order", "1", "--dry-run"]), 0)
            (pathlib.Path(d) / "x.mp3").write_bytes(b"")
            self.assertEqual(vo_take.main(["--text", "hi", "--out", d, "--stem", "x", "--order", "1", "--dry-run"]), 2)


if __name__ == "__main__":
    unittest.main()
