#!/usr/bin/env python3
"""Tests for cdp_tabs.py (pure logic; no Chrome)."""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdp_tabs as c

NOW = 100_000.0
OLD = NOW - 3600
S = "https://studio.youtube.com/channel/x/videos"


def tab(i, url):
    return {"id": i, "url": url}


class Plan(unittest.TestCase):
    def test_keeps_newest_studio_closes_old_duplicates(self):
        tabs = [tab("a", S), tab("b", S), tab("c", S)]
        seen = {"a": OLD - 20, "b": OLD - 10, "c": OLD}
        self.assertEqual(c.plan_closes(tabs, seen, NOW), ["a", "b"])

    def test_fresh_duplicate_is_left_alone(self):
        tabs = [tab("a", S), tab("b", S)]
        seen = {"a": NOW - 60, "b": NOW - 30}            # both under 20 min
        self.assertEqual(c.plan_closes(tabs, seen, NOW), [])

    def test_newest_kept_even_if_older_is_idle(self):
        tabs = [tab("old", S), tab("new", S)]
        seen = {"old": OLD, "new": NOW - 30}
        self.assertEqual(c.plan_closes(tabs, seen, NOW), ["old"])

    def test_different_sites_kept(self):
        tabs = [tab("a", S), tab("b", "https://labs.google/fx/tools/flow"), tab("c", "https://claude.ai/settings/usage")]
        seen = {k: OLD for k in "abc"}
        self.assertEqual(c.plan_closes(tabs, seen, NOW), [])

    def test_blank_tabs_count_as_one_site(self):
        tabs = [tab("a", "about:blank"), tab("b", "chrome://newtab/"), tab("c", S)]
        seen = {"a": OLD - 5, "b": OLD, "c": OLD}
        self.assertEqual(c.plan_closes(tabs, seen, NOW), ["a"])

    def test_sign_in_page_never_closed(self):
        g = "https://accounts.google.com/signin"
        tabs = [tab("a", g), tab("b", g)]
        seen = {"a": OLD - 5, "b": OLD}
        self.assertEqual(c.plan_closes(tabs, seen, NOW), [])

    def test_cap_closes_oldest(self):
        tabs = [tab(str(i), f"https://site{i}.example/") for i in range(9)]
        seen = {str(i): OLD + i for i in range(9)}
        self.assertEqual(c.plan_closes(tabs, seen, NOW, max_tabs=6), ["0", "1", "2"])

    def test_never_closes_last_tab(self):
        tabs = [tab("a", S)]
        self.assertEqual(c.plan_closes(tabs, {"a": OLD}, NOW, max_tabs=0), [])

    def test_unknown_tab_counts_as_new(self):
        tabs = [tab("a", S), tab("b", S)]
        self.assertEqual(c.plan_closes(tabs, {}, NOW), [])


class Busy(unittest.TestCase):
    def test_claimed_studio_job_detected(self):
        import json, tempfile
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump({"jobs": [{"status": "claimed", "kind": "studio"}]}, f); f.close()
        self.assertTrue(c.studio_job_running(f.name))
        json.dump({"jobs": [{"status": "claimed", "kind": "video"}, {"status": "open", "kind": "studio"}]}, open(f.name, "w"))
        self.assertFalse(c.studio_job_running(f.name))
        self.assertTrue(c.studio_job_running("/nonexistent.json"))


class Reuse(unittest.TestCase):
    class P:
        def __init__(self, url): self.url, self.front = url, False
        def is_closed(self): return False
        def bring_to_front(self): self.front = True

    class Ctx:
        def __init__(self, urls): self.pages, self.made = [Reuse.P(u) for u in urls], 0
        def new_page(self):
            self.made += 1; p = Reuse.P("about:blank"); self.pages.append(p); return p

    def test_reuses_existing_studio(self):
        ctx = self.Ctx(["https://claude.ai/", S])
        p = c.reuse_page(ctx, "studio.youtube.com")
        self.assertIs(p, ctx.pages[1]); self.assertEqual(ctx.made, 0); self.assertTrue(p.front)

    def test_reuses_blank_before_opening(self):
        ctx = self.Ctx(["https://claude.ai/", "about:blank"])
        self.assertIs(c.reuse_page(ctx, "studio.youtube.com"), ctx.pages[1]); self.assertEqual(ctx.made, 0)

    def test_opens_one_when_nothing_fits(self):
        ctx = self.Ctx(["https://claude.ai/"])
        c.reuse_page(ctx, "studio.youtube.com"); self.assertEqual(ctx.made, 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
