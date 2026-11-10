"""AI & credits page (/ai) and the studio app (/): the browser logic runs in node, and the built site serves both."""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "05_Analytics" / "kanban" / "board_site"


class AIPage(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'node is required for browser logic checks')
    def test_page_logic(self):
        result = subprocess.run(['node', str(Path(__file__).with_name('test_ai_page.cjs'))],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @unittest.skipUnless(shutil.which('node'), 'node is required for browser logic checks')
    def test_studio_app_logic(self):
        result = subprocess.run(['node', str(Path(__file__).with_name('test_studio_app.cjs'))],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_built_page_and_tabs(self):
        sys.path.insert(0, str(SITE))
        import build
        with tempfile.TemporaryDirectory() as t:
            out = pathlib.Path(t)
            build.build_ai(out)
            html = (out / "ai.html").read_text()
        self.assertIn('id="ai"', html)
        self.assertIn("renderAI", html)
        self.assertNotIn("AI_APP_BOOT", html)
        self.assertIn('<a class="on" href="/ai">', html)
        self.assertIn('href="/ai">AI & credits</a>', (ROOT / "05_Analytics" / "kanban" / "video_tracker.html").read_text())
        self.assertIn('"/ai"', (SITE / "vercel.json").read_text())
        self.assertIn('"/board"', (SITE / "vercel.json").read_text())


if __name__ == "__main__":
    unittest.main()
