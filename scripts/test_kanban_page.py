#!/usr/bin/env python3
"""Tests for the Studio Kanban page itself (05_Analytics/kanban/studio_kanban.html).

Ben, 11 Oct 20:52: "Not sure we need this as we have the swim lanes." The Order of work list (and its Just finished
list) is gone. Card ranks are unchanged.
Ben, 11 Oct 22:09: "we're currently working on X, Y, Z. We are twenty percent of the way through, we'll be finished in
thirty minutes." The Mac mini box is plain: Working on, a % done bar with the finish time, Next, Then, Blocked, Updated.
"""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "05_Analytics/kanban/studio_kanban.html"


def page() -> str:
    return PAGE.read_text()


def js_function(src: str, name: str) -> str:
    """The source of `function name(...){...}` or a `const name = ...` arrow, by brace matching."""
    m = re.search(rf"^(function {re.escape(name)}\(|const {re.escape(name)} = )", src, re.M)
    if not m:
        raise AssertionError(f"{name} not found in studio_kanban.html")
    i, depth, start = m.start(), 0, m.start()
    if src.startswith("const", start):
        brace = src.find("{", start)
        eol = src.find("\n", start)
        if brace < 0 or brace > eol:          # one-line arrow
            return src[start:eol]
        i = brace
    else:
        i = src.find("{", start)
    while True:
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = src.find("\n", i)
                return src[start:end if end > 0 else len(src)]
        i += 1


class OrderOfWorkRemoved(unittest.TestCase):
    def test_no_order_of_work_section(self):
        html = page()
        for gone in ('id="jobsBox"', ">Order of work", "<b>Just finished</b>", "function renderJobs", "renderJobs()"):
            self.assertFalse(gone in html, f"still on the page: {gone}")

    def test_mac_mini_box_stays_at_the_top(self):
        html = page()
        self.assertIn('<div class="nowbar" id="nowbar" hidden></div>', html)
        self.assertLess(html.index('id="nowbar"'), html.index('id="tracker"'))

    def test_cards_render_before_the_box_and_rank_code_is_unchanged(self):
        html = page()
        self.assertIn("renderSource(); renderTracker(films); renderNow(); ", html)
        self.assertIn("if(fj) ON_CARD.add(fj.j.id);", html)
        # PR #122's work order across both channels: same tiers as before.
        self.assertIn("tier: !fj ? 2 : fj.p.state===\"now\"||partDone ? 0 : fj.p.state===\"gated\" ? 3 : fj.p.start ? 1 : 2", html)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class MacMiniBox(unittest.TestCase):
    """Runs the page's own renderNow() in node against a small queue."""

    NOW = "2026-10-11T19:50:00Z"
    JOBS = [
        {"id": "J0129", "title": "024 Light Speed v05: picture fixes", "needs": "mini", "line": "mini", "film": "024",
         "status": "claimed", "by": "cursor", "claimedAt": "2026-10-11T19:30Z", "estMin": 60, "last": {}},
        {"id": "J0130", "title": "027 Earth Stopped Spinning rough v01f: frame-review fixes", "needs": "mini", "line": "mini",
         "film": "027", "status": "open", "estMin": 30, "last": {}},
        {"id": "J0126", "title": "Saturn Short v03 Cka7_TVVOUQ: set Related to 55AEQwvs36g", "needs": "mini", "line": "mini",
         "film": "", "status": "open", "estMin": 15, "last": {}},
        {"id": "J0128", "title": "HOS 002 A/B day-14 read", "needs": "mini", "line": "mini", "film": "", "status": "open",
         "estMin": 20, "last": {}},
        {"id": "J0132", "title": "Spare job four", "needs": "mini", "line": "mini", "film": "", "status": "open",
         "estMin": 20, "last": {}},
        {"id": "J0123", "title": "025 date gate: mark done on/after Sun 8 Nov 18:00Z", "needs": "cloud", "line": "chief",
         "film": "", "status": "open", "notBefore": "2026-11-08T18:00Z", "gateOnly": True, "estMin": 30, "last": {}},
        {"id": "J0131", "title": "Orbit Instagram bio link -> Saturn long 55AEQwvs36g (before Mon 11:30)", "needs": "mini",
         "line": "mini", "film": "", "status": "blocked", "result": "needs Ben to sign Instagram in on the mini: the Orbit "
         "Studio Chrome is signed into historyofscienceyt; Instagram web locks the Website field.", "last": {}},
    ]

    def render(self, on_card=(), jobs=None):
        html = page()
        names = ["esc", "AGENT", "MINUTE", "ts", "clock", "etaOf", "ago", "plan", "laneQuiet", "shortTitle", "jobTag",
                 "jobName", "jobLabel", "jobLine", "CHIEF_PARK", "blockWhy", "isChiefPark", "shortReason", "stepPace", "progressOf", "finishIn", "plainJob",
                 "updatedAt", "NEEDS_BEN", "WAITS_INPUT", "cleanTitle", "WORKER", "readyAt", "jobKind", "renderNow"]
        lib = "\n".join(js_function(html, n) for n in names)
        board = {"jobs": self.JOBS if jobs is None else jobs,
                 "runOrder": {"mini": ["J0130", "J0126", "J0128", "J0132"], "chief": ["J0123"]},
                 "lanes": {}, "focus": [], "owbAt": "2026-10-11T19:49Z",
                 "owb": [{"film": "024", "title": "What Happens If You Travel Near Light Speed?"},
                         {"film": "027", "title": "What If Earth Stopped Spinning?"}]}
        script = f"""
const RealDate = Date, FIXED = RealDate.parse({json.dumps(self.NOW)});
globalThis.Date = class extends RealDate {{ constructor(...a){{ super(...(a.length?a:[FIXED])); }} static now(){{ return FIXED; }} }};
const box = {{hidden:true, className:"", innerHTML:""}};
const $ = id => id==="nowbar" ? box : null;
const fromDb = Object.assign({{chief:null}}, {json.dumps(board)});
const ON_CARD = new Set({json.dumps(list(on_card))});
{lib}
renderNow();
console.log(JSON.stringify({{hidden: box.hidden, html: box.innerHTML}}));
"""
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(script)
        out = subprocess.run(["node", f.name], capture_output=True, text=True, timeout=30)
        Path(f.name).unlink()
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)

    def with_jobs(self, **changes):
        """The queue with some jobs changed: J0129={...} updates that job; J0129=None drops it."""
        out = []
        for j in self.JOBS:
            if j["id"] in changes and changes[j["id"]] is None:
                continue
            out.append(dict(j, **(changes.get(j["id"]) or {})))
        return out

    # Ben, 12 Oct 15:05: one glance. Now (title, worker, ready time), Next, one chip; the rest behind "Show all".
    def test_one_line_now_with_worker_and_ready_time(self):
        r = self.render()
        self.assertFalse(r["hidden"])
        self.assertIn('<b>Now:</b> 024 Light Speed v05: picture fixes</span><span class="meta"><span class="run">Running</span> <span class="jid">J0129</span> <span class="who">Cursor</span>', r["html"])
        self.assertIn("ready in about 40 min", r["html"])
        self.assertIn('<div class="upd">Updated ', r["html"])
        self.assertEqual(r["html"].count("J0129"), 1)

    def test_one_next_line_only(self):
        r = self.render()
        self.assertEqual(r["html"].count('<div class="nx one">'), 1)
        self.assertIn("<b>Next:</b> 027 Earth Stopped Spinning rough v01f: frame-review fixes", r["html"])
        self.assertNotIn("Saturn Short", r["html"])

    def test_needs_ben_is_one_red_line(self):
        r = self.render()
        self.assertIn('<div class="bl">Needs Ben: Orbit Instagram bio link -&gt; Saturn long 55AEQwvs36g</div>', r["html"])

    def test_chief_parks_collapse_into_a_chip(self):
        many = {f"J09{i:02d}": None for i in range(1)}
        jobs = self.with_jobs(J0131={"result": "parked for Chief: thumbnail review"}) + [
            {"id": f"J09{i:02d}", "title": f"Backlog OWB: thing {i}", "needs": "mini", "line": "mini", "status": "blocked",
             "result": "parked for Chief: review", "last": {}} for i in range(5)]
        r = self.render(jobs=jobs)
        self.assertIn('<span class="chip">6 waiting on Chief</span><span class="sa">Show all</span>', r["html"])
        self.assertIn("<details", r["html"])
        self.assertNotIn('<div class="bl">', r["html"])
        self.assertNotIn("Backlog OWB:", r["html"])
        self.assertIn("OWB: thing 0", r["html"])

    def test_date_bound_job_is_scheduled_not_red(self):
        jobs = self.with_jobs(J0131=None) + [{"id": "J0135", "title": "025 set Related once the long is public",
            "needs": "mini", "line": "mini", "status": "blocked", "last": {},
            "result": "waits for input: 025 long Js6EQJ8qDi8 public"}]
        r = self.render(jobs=jobs)
        self.assertIn("1 scheduled", r["html"])
        self.assertIn('<div class="sh">Scheduled</div>', r["html"])
        self.assertNotIn('<div class="bl">', r["html"])

    def test_idle_box_is_plain_too(self):
        r = self.render(jobs=self.with_jobs(J0129=None))
        self.assertIn("<b>Now:</b> starting the next job", r["html"])

    def test_box_shows_on_every_channel(self):
        self.assertNotIn('chan==="HOS"', js_function(page(), "renderNow"))


@unittest.skipUnless(shutil.which("node"), "node not installed")
class TickedCardsLeaveTheBox(unittest.TestCase):
    """Ben, 11 Oct 21:39: "Been approved why is it still here". A ticked cut leaves his For-you box, handled or not;
    a "Just approved" line with Undo stays for two hours; the box says one short line when nothing is left."""

    NOW = "2026-10-11T20:40:00Z"

    def run_js(self, body):
        html = page()
        lib = "\n".join(js_function(html, n) for n in ["esc", "MINUTE", "ts", "JUST_MS", "tickStands", "justTicks", "justLine"])
        script = f"const NOW = Date.parse({json.dumps(self.NOW)});\n{lib}\nconsole.log(JSON.stringify((()=>{{ {body} }})()));"
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(script)
        out = subprocess.run(["node", f.name], capture_output=True, text=True, timeout=30)
        Path(f.name).unlink()
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)

    def test_a_tick_stands_handled_or_not(self):
        r = self.run_js("""
          const ok = {verdict:"ok", version:"v05e", at:"2026-10-11T19:26:10.800Z", handled:false};
          const brief = {updated:"2026-10-11T18:05Z"};
          return [tickStands(ok, brief, "v05e"), tickStands(Object.assign({}, ok, {handled:true}), brief, "v05e"),
                  tickStands(Object.assign({}, ok, {handled:true}), {updated:"2026-10-11T20:43Z"}, "v05e"),
                  tickStands(null, brief, "v05e")];""")
        self.assertEqual(r, [True, True, True, False])

    def test_a_newer_cut_brings_the_card_back(self):
        r = self.run_js("""
          const chg = {verdict:"change", version:"v05d", at:"2026-10-11T09:42Z", handled:true, fixes:[{t:"5:53",text:"x"}]};
          return [tickStands(chg, {updated:"2026-10-11T18:05Z"}, "v05e"),          // v05e handed over
                  tickStands(Object.assign({}, chg, {version:""}), {updated:"2026-10-11T18:05Z"}, ""),   // note rewritten
                  tickStands(Object.assign({}, chg, {handled:false}), {updated:"2026-10-11T18:05Z"}, "v05e")];""")
        self.assertEqual(r, [False, False, True])

    def test_just_approved_line_for_two_hours_with_undo(self):
        r = self.run_js("""
          const f = {key:"OWB:023", id:"023", title:"What Happened to Venus?"};
          const c = at => ({verdict:"ok", version:"v05e", at, handled:false});
          const shown = justTicks([{f, c:c("2026-10-11T19:26:10.800Z")}], NOW).map(justLine);
          const gone = justTicks([{f, c:c("2026-10-11T18:39:00Z")}], NOW).length;
          const handled = justLine({f, c:Object.assign(c("2026-10-11T19:26:10.800Z"), {handled:true})});
          const chg = justLine({f, c:{verdict:"change", version:"v05e", at:"2026-10-11T20:30Z", handled:false, fixes:[{},{}]}});
          return {shown, gone, handled, chg};""")
        self.assertEqual(len(r["shown"]), 1)
        self.assertIn("Just approved: <b>023 What Happened to Venus? v05e</b>", r["shown"][0])
        self.assertIn('data-undo="OWB-023"', r["shown"][0])
        self.assertEqual(r["gone"], 0)
        self.assertNotIn("data-undo", r["handled"])
        self.assertIn("Just sent 2 fixes", r["chg"])
        self.assertIn('data-more="OWB-023"', r["chg"])

    def test_box_has_no_ticked_card_list_and_one_empty_line(self):
        html = page()
        self.assertNotIn("All checked. Nothing else for you right now.", html)
        self.assertNotIn("You said it looks good (", html)
        self.assertIn("<b>Nothing for you right now.</b>", html)
        self.assertIn("if(b.you) forYou.push(", html)
        self.assertIn('if(ck) b = Object.assign({}, b, {you:"", youShort:"", youWhen:""});', html)


class VenusApproved(unittest.TestCase):
    def test_023_note_is_off_bens_box_and_shipping(self):
        j = json.loads((PAGE.parent / "film_briefs.json").read_text())["films"]["OWB:023"]
        self.assertEqual(j["you"], "")
        self.assertEqual(j["mood"], "watched")
        self.assertTrue(j["line"].startswith("Approved by Ben Sun 11 Oct 20:26"))
        self.assertTrue(any(s["who"] == "Claude" and s["what"].startswith("ship v05e") for s in j["steps"]))
        self.assertTrue(all(s.get("done") for s in j["steps"] if s["who"] == "Ben"))


if __name__ == "__main__":
    unittest.main()
