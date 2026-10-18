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
        if brace < 0 or brace > eol:          # arrow or a possibly multi-line constant array
            return src[start:eol] if ";" in src[start:eol] else src[start:src.find(";\n", start)+1]
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


PROGRESS_FUNCTIONS = ["OWB_STAGES", "taskKeysFor", "taskStageInfo", "jobOutcome", "jobFollowUps", "jobImpact", "progressUpdates"]


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
        self.assertIn("renderSource(); renderTracker(films); renderNow(); renderDone(); renderJobBoard(); ", html)
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

    def render(self, on_card=(), jobs=None, extra=None, lanes=None):
        html = page()
        names = ["esc", "AGENT", "MINUTE", "ts", "clock", "etaOf", "ago", "jobMin", "plan", "laneQuiet", "shortTitle", "jobTag",
                 "jobName", "jobLabel", "jobLine", "CHIEF_PARK", "blockWhy", "isChiefPark", "shortReason", "stepPace", "progressOf", "finishIn", "plainJob",
                 "updatedAt", "STALL_MIN", "stallOf", "hbLine", "NEEDS_BEN", "WAITS_INPUT", "cleanTitle", "WORKER", "readyAt", "jobKind", "plainTitle", "waitReason", "WAIT_WORD", "pcCol", "renderNow"]
        lib = "\n".join(js_function(html, n) for n in dict.fromkeys(names + PROGRESS_FUNCTIONS))
        board = {"jobs": self.JOBS if jobs is None else jobs,
                 "runOrder": {"mini": ["J0130", "J0126", "J0128", "J0132"], "chief": ["J0123"]},
                 "lanes": lanes or {}, "focus": [], "owbAt": "2026-10-11T19:49Z", "extra": extra or {},
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
console.log(JSON.stringify({{hidden: box.hidden, html: box.innerHTML, className: box.className}}));
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

    # Ben, 12 Oct 19:45 / 21:07: three plain lines. Now (short title) with the progress bar, Next, and one muted
    # "N jobs waiting: ..." line grouped by plain reasons; no job ids, no worker badge, red only for Ben.
    def test_one_line_now_with_worker_and_ready_time(self):
        r = self.render()
        self.assertFalse(r["hidden"])
        self.assertIn('<span class="tt"><b>Now:</b> 024 Light Speed v05 – picture fixes</span>', r["html"])
        self.assertIn('<div class="pbar" data-live>', r["html"])
        self.assertIn("33% done · finished in about 40 min", r["html"])
        self.assertIn('<div class="upd">Updated ', r["html"])
        self.assertNotIn("J0129", r["html"])
        self.assertNotIn('class="jid"', r["html"])

    def test_next_up_lists_three_and_no_dropdown(self):
        r = self.render()
        self.assertEqual(r["html"].count('<div class="nx">'), 1)
        self.assertLessEqual(r["html"].count('<li>'), 3)
        self.assertIn("<li>027 Earth Stopped Spinning rough v01f – frame-review fixes</li>", r["html"])
        self.assertNotIn("<details", r["html"])
        self.assertNotIn("jobs waiting", r["html"])

    def test_idle_box_is_plain_too(self):
        r = self.render(jobs=self.with_jobs(J0129=None))
        self.assertIn("<b>Now:</b> starting the next job", r["html"])
        self.assertNotIn('<div class="pbar"', r["html"])

    def test_stalled_queue_says_how_long_since_a_job_finished(self):
        # Ben, 14 Oct: the box read "starting the next job" for hours while nothing ran.
        lanes = {"mini": {"lastAt": "2026-10-11T19:10Z", "lastBy": "codex", "lastWhat": "blocked: parked for Chief: Studio sign-in",
                          "heartbeat": {"at": "2026-10-11T19:46Z", "state": "running"}}}
        r = self.render(jobs=self.with_jobs(J0129=None), extra={"done": [{"id": "J0100", "at": "2026-10-10T15:50Z"}]}, lanes=lanes)
        self.assertIn("nothing running · last job finished", r["html"])
        self.assertIn(">1 d ago<", r["html"])
        self.assertIn("nowbar asleep", r["className"])
        self.assertIn("Mac mini checked in <span", r["html"])
        self.assertIn("last: Codex blocked: parked for Chief: Studio sign-in (", r["html"])
        # a job finished an hour ago: still the plain idle line
        r = self.render(jobs=self.with_jobs(J0129=None), extra={"done": [{"id": "J0100", "at": "2026-10-11T18:50Z"}]})
        self.assertIn("<b>Now:</b> starting the next job", r["html"])
        # a running job: no check-in line, the bar instead
        self.assertNotIn('class="hb"', self.render(lanes=lanes)["html"])

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
        self.assertIn("Nothing to watch right now.", html)   # Ben, 15 Oct 2026: the box always shows
        self.assertIn("if(b.you) forYou.push(", html)
        # Ben, 15 Oct 2026: the standalone Shorts need the watch link, Approve and Request changes too
        self.assertIn("const extraItem = x =>", html)
        self.assertIn('data-ok="${id}">✓ Approve</button><button class="btn" data-chg="${id}">Request changes', html.split("const extraItem")[1])
        self.assertIn("▶ Watch it", html.split("const extraItem")[1])
        self.assertIn('if(ck) b = Object.assign({}, b, {you:"", youShort:"", youWhen:""});', html)


class VenusApproved(unittest.TestCase):
    def test_023_note_is_off_bens_box_and_shipping(self):
        j = json.loads((PAGE.parent / "film_briefs.json").read_text())["films"]["OWB:023"]
        self.assertEqual(j["you"], "")
        self.assertEqual(j["mood"], "watched")
        self.assertTrue(j["line"].startswith("Approved by Ben Sun 11 Oct 20:26"))
        self.assertTrue(any(s["what"].startswith("ship v05e") for s in j["steps"]))   # Claude, or the Mac mini (J0236, 14 Oct)
        self.assertTrue(all(s.get("done") for s in j["steps"] if s["who"] == "Ben"))


@unittest.skipUnless(shutil.which("node"), "node not installed")
class TaskProgress(unittest.TestCase):
    """A job outcome must not imply that a film or its review is complete."""

    def evaluate(self, expression, board=None):
        names = ["esc", "MINUTE", "ts", "WORKER", "cleanTitle", "plainTitle", "pw", "fd", "fw"] + PROGRESS_FUNCTIONS
        lib = "\n".join(js_function(page(), n) for n in dict.fromkeys(names))
        script = f"const fromDb = {json.dumps(board or {})};\n{lib}\nconsole.log(JSON.stringify({expression}));"
        out = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)

    def test_hos_job_with_numeric_film_never_links_to_owb(self):
        keys = self.evaluate('taskKeysFor({id:"J1",title:"HOS 006: edit fixes",film:"006"})')
        self.assertEqual(keys, ["HOS:006"])

    def test_generic_backlog_does_not_guess_a_film_from_result_text(self):
        job = {"id": "J1", "title": "Backlog HOS: next Short", "status": "done", "result": "Built 006 Short, needs review."}
        html = self.evaluate(f"jobImpact({json.dumps(job)})")
        self.assertIn("Built 006 Short, needs review.", html)
        self.assertIn("No individual film linked", html)
        self.assertIn("No follow-up recorded", html)
        self.assertNotIn("data-task-film", html)

    def test_brief_and_stage_job_ids_link_jobs_without_film_numbers(self):
        board = {"briefs": {"OWB:024": {"steps": [{"job": "J1"}]}},
                 "hos": {"films": [{"id": "006", "stages": {"edit": {"jobs": ["J1"]}}}]}}
        self.assertEqual(self.evaluate('taskKeysFor({id:"J1",title:"Teaching graphics"})', board), ["OWB:024", "HOS:006"])

    def test_explicit_result_can_name_the_film_selected_by_a_backlog_job(self):
        keys = self.evaluate('taskKeysFor({id:"J1",title:"Backlog HOS: next Short",result:"Short PASS (HOS 004 s07 built; gates PASS)"})')
        self.assertEqual(keys, ["HOS:004"])

    def test_finished_job_keeps_film_review_and_upload_outstanding(self):
        board = {"owb": [{"film": "024", "title": "Light Speed", "stages": {
            key: {"state": "done"} for key in ("topic", "script", "sources", "vo", "shots", "picture")}}]}
        board["owb"][0]["stages"]["edit"] = {"state": "review"}
        html = self.evaluate('jobImpact({id:"J1",title:"024 edit fixes",status:"done",result:"New cut rendered."})', board)
        self.assertIn("New cut rendered.", html)
        self.assertIn("6 of 9 stages marked complete", html)
        self.assertIn("Edit (review) → Thumbnails → Upload", html)
        self.assertNotIn("All recorded film stages complete", html)

    def test_active_steps_and_follow_up_are_recorded_separately(self):
        board = {"jobs": [{"id": "J2", "title": "Chief review", "after": "J1", "status": "open"}]}
        html = self.evaluate('jobImpact({id:"J1",status:"claimed",progress:{step:3,of:4,note:"Captions complete."}})', board)
        self.assertIn("3 of 4 job steps recorded complete", html)
        self.assertIn("Captions complete.", html)
        self.assertIn("1 of 4 steps", html)
        self.assertIn("Chief review (queued)", html)

    def test_parked_pass_keeps_review_reason_and_is_not_counted_as_done(self):
        job = {"id": "J1", "title": "HOS Short", "status": "blocked", "progress": {"step": 4, "of": 4, "at": "2026-10-18T21:30Z"},
               "result": "parked for Chief: Short PASS", "last": {"at": "2026-10-18T23:30Z", "what": "escalated"}}
        board = {"jobs": [job], "extra": {"done": []}}
        updates = self.evaluate("progressUpdates()", board)
        self.assertEqual(updates[0]["status"], "blocked")
        self.assertEqual(updates[0]["at"], "2026-10-18T21:30Z")  # not the later escalation
        html = self.evaluate(f"jobImpact({json.dumps(job)})", board)
        self.assertIn("Waiting on:", html)
        self.assertIn("parked for Chief: Short PASS", html)
        self.assertNotIn("0 of 4 steps", html)

    def test_external_worker_notes_are_escaped(self):
        html = self.evaluate('jobImpact({status:"done",result:"<img src=x onerror=alert(1)>"})')
        self.assertIn("&lt;img", html)
        self.assertNotIn("<img", html)

    def test_unknown_result_does_not_claim_a_film_is_complete(self):
        html = self.evaluate('jobImpact({status:"done",title:"Read analytics"})')
        self.assertIn("no result note recorded", html)
        self.assertNotIn("All recorded film stages complete", html)


if __name__ == "__main__":
    unittest.main()


@unittest.skipUnless(shutil.which("node"), "node not installed")
class JobBoard(unittest.TestCase):
    """Ben, 12 Oct 15:49: five columns, one-line cards, Needs-you strip only for money/irreversible, stuck alarm,
    three header numbers with a dash for any missing source."""

    NOW = "2026-10-12T15:00:00Z"
    JOBS = [
        {"id": "J0201", "title": "HOS 006 picture: Part 03 plates", "needs": "mini", "status": "claimed", "by": "cursor",
         "claimedAt": "2026-10-12T13:00Z", "workStart": "2026-10-12T13:00Z", "estMin": 30, "typMin": 30, "kindKey": "omni", "last": {}},
        {"id": "J0202", "title": "025 Mars robot rough v02", "needs": "mini", "status": "open", "estMin": 20, "last": {}},
        {"id": "J0203", "title": "024 Light Speed covers", "needs": "mini", "status": "blocked",
         "result": "parked for Chief: two covers", "last": {"at": "2026-10-12T14:30Z", "what": "blocked: parked for Chief"}},
        {"id": "J0204", "title": "025 date gate", "needs": "cloud", "status": "blocked",
         "result": "waits for input: 025 long public (publishAt Sun 8 Nov 18:00Z)", "last": {}},
    ]

    def render(self, jobs=None, extra=None, credits=None):
        html = page()
        names = ["esc", "AGENT", "MINUTE", "ts", "clock", "pd", "fd", "pw", "fw", "today", "days", "etaOf", "ago", "jobMin", "plan",
                 "laneQuiet", "shortTitle", "jobTag", "jobName", "jobLabel", "jobLine", "CHIEF_PARK", "blockWhy", "isChiefPark",
                 "shortReason", "stepPace", "progressOf", "finishIn", "NEEDS_BEN", "WAITS_INPUT", "cleanTitle", "WORKER",
                 "readyAt", "jobKind", "plainTitle", "rel", "JOB_KINDS", "jobKindOf", "jobPlan", "MONEY_IRREV", "chanOf", "AIR_RX", "airOf", "sinceMin", "dur", "isStuck", "jobCard",
                 "renderJobBoard"]
        lib = "\n".join(js_function(html, n) for n in dict.fromkeys(names + PROGRESS_FUNCTIONS))
        board = {"jobs": self.JOBS if jobs is None else jobs, "runOrder": {"mini": ["J0202"]}, "lanes": {}, "focus": [],
                 "owb": [], "extra": extra if extra is not None else {}, "credits": credits}
        script = f"""
const RealDate = Date, FIXED = RealDate.parse({json.dumps(self.NOW)});
globalThis.Date = class extends RealDate {{ constructor(...a){{ super(...(a.length?a:[FIXED])); }} static now(){{ return FIXED; }} }};
const els = {{jobboard:{{hidden:true,innerHTML:""}}, daystats:{{hidden:true,innerHTML:""}}, needsyou:{{hidden:true,innerHTML:""}}}};
const $ = id => els[id] || null;
const DAY = 86400000;
const fromDb = Object.assign({{chief:null}}, {json.dumps(board)});
const ON_CARD = new Set();
{lib}
renderJobBoard();
console.log(JSON.stringify(els));
"""
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(script)
        out = subprocess.run(["node", f.name], capture_output=True, text=True, timeout=30)
        Path(f.name).unlink()
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)

    def test_five_columns_and_one_line_cards(self):
        r = self.render()
        h = r["jobboard"]["innerHTML"]
        for col in ("Next", "Running", "Waiting for review", "Jobs done", "Scheduled"):
            self.assertIn(f"<h4>{col}", h)
        self.assertIn('<span class="jid">J0201</span><span class="cdot HOS"', h)
        self.assertIn('<span class="jid">J0202</span><span class="cdot OWB"', h)
        self.assertIn("Airs Sun 8 Nov 18:00", h)  # 18:00Z in November is 18:00 London

    def test_stuck_running_card_turns_amber(self):
        h = self.render()["jobboard"]["innerHTML"]
        self.assertIn('class="jc HOS stuck"', h)          # 120 min > 2 x 30
        self.assertNotIn('class="jc OWB stuck"', h)        # the 30-min-old review is fine (default 240)

    def test_needs_you_absent_unless_money_or_irreversible(self):
        self.assertTrue(self.render()["needsyou"]["hidden"])
        jobs = self.JOBS + [{"id": "J0205", "title": "ElevenLabs top-up?", "needs": "mini", "status": "blocked",
                             "result": "needs Ben: approve a paid top-up", "last": {}}]
        r = self.render(jobs=jobs)
        self.assertFalse(r["needsyou"]["hidden"])
        self.assertIn("J0205", r["needsyou"]["innerHTML"])

    def test_missing_sources_show_a_dash(self):
        s = self.render()["daystats"]["innerHTML"]
        self.assertEqual(s.count(">—<"), 2)
        self.assertIn("ElevenLabs — · Flow — · Vertex —", s)
        s = self.render(extra={"day": {"doneToday": 7, "idleMin": 12}},
                        credits={"pools": {"flow": {"latest": {"left": 52}}, "vertex": {"latest": {"left": 4.93}}}})["daystats"]["innerHTML"]
        self.assertIn(">7<", s)
        self.assertIn("Flow 52 · Vertex £4.93", s)

    def test_week_bars_and_low_credit_flag(self):
        week = [{"date": f"2026-10-{d:02d}", "done": n, "idleMin": i, "min": m}
                for d, n, i, m in [(6, 30, 900, 1440), (7, 20, 1000, 1440), (8, 32, 1057, 1440), (9, 27, 1009, 1440),
                                   (10, 27, 1234, 1440), (11, 8, 1331, 1440), (12, 2, 600, 900)]]
        credits = {"pools": {"elevenlabs": {"latest": {"left": 5275, "total": 209536}}, "cursor": {"unit": "%", "latest": {"left": 0, "total": 100}},
                             "flow": {"latest": {"left": 23690}}}}
        s = self.render(extra={"day": {"doneToday": 2, "idleMin": 600}, "week": week}, credits=credits)["daystats"]["innerHTML"]
        self.assertEqual(s.count('<span class="spk'), 2)
        self.assertIn("24 a day, last 6 days", s)
        self.assertIn("67% of today", s)
        self.assertIn("Flow 24k · Vertex — · Cursor 0%", s)
        self.assertIn("Low: ElevenLabs 3% left · Cursor used up", s)
        self.assertIn('data-open="foldPlans"', s)
        # no week from the Mini yet: no bars, no flag without a known pool size
        s = self.render(extra={"day": {"doneToday": 2, "idleMin": 600}}, credits={"pools": {"flow": {"latest": {"left": 10}}}})["daystats"]["innerHTML"]
        self.assertNotIn("spk", s)
        self.assertNotIn("Low:", s)

    def test_job_cards_have_a_kind_a_bar_and_a_step_plan(self):
        # Ben, 14 Oct: "updating text or improving SEO or working on thumbnails ... a percentage bar to each job and a full
        # breakdown with the ETA on when each part will be complete".
        jobs = self.JOBS + [
            {"id": "J0211", "title": "HOS standalone Shorts S1-S4: titles, descriptions, tags (listing)", "needs": "mini", "status": "claimed",
             "by": "codex", "claimedAt": "2026-10-12T14:00Z", "workStart": "2026-10-12T14:00Z", "kindKey": "listing", "estMin": 60,
             "progress": {"step": 2, "of": 4, "at": "2026-10-12T14:30Z", "note": "S1 and S2 drafted"}, "last": {}},
            {"id": "J0167", "title": "OWB compilation film: assemble 45-60 min cut", "needs": "mini", "status": "blocked", "kindKey": "assembly",
             "result": "parked for Chief: music gap", "progress": {"step": 7, "of": 8, "at": "2026-10-12T11:18Z"},
             "last": {"at": "2026-10-12T11:18Z", "what": "blocked: parked for Chief"}}]
        h = self.render(jobs=jobs)["jobboard"]["innerHTML"]
        self.assertIn('<span class="kd seo">SEO &amp; listing</span>', h)
        self.assertIn('<span class="kd edit">Edit</span><span class="pb wait"><i style="width:88%"></i></span><span class="pc">88%</span>', h)
        self.assertIn('<span class="kd picture">Picture</span><span class="pb "><i style="width:95%"></i></span><span class="pc">95%</span>', h)
        plan = h[h.index("J0211"):]
        plan = plan[plan.index('<ol class="plan">'):plan.index("</ol>")]
        self.assertEqual(plan.count('<li class="ok">'), 2)
        self.assertEqual(plan.count('<li class="now">'), 1)
        self.assertIn("S1 and S2 drafted", plan)
        self.assertIn("<span>Ready</span>", plan)
        self.assertIn("Step 4 of 4", plan)
        self.assertIn("parked for the Chief&#39;s check", h)
        self.assertIn("Mac mini line: ", h)

    def test_kind_labels_from_real_titles(self):
        html = page()
        lib = "\n".join(js_function(html, n) for n in ["JOB_KINDS", "jobKindOf"])
        titles = ["OWB compilation film: Chief review + schedule", "Daily Studio read: long films (impressions, CTR, views)",
                  "026 Nearest Star: long thumbnail v02", "HOS Atom GHZDsiH7L7A: Sources line for description",
                  "030 Apophis: Claude quote check v01 + fix rows 7/13/20", "HOS 006 picture: P3:06 on Flow after the Chief's price pass",
                  "030 Apophis Short: assembly + gate_shorts_open", "025 date gate: mark done once Js6EQJ8qDi8 is public",
                  "027 long VO take 2", "Mini disk full: move old render scratch"]
        script = f"{lib}\nconsole.log(JSON.stringify({json.dumps(titles)}.map(t=>jobKindOf({{title:t}}).label)));"
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(script)
        out = subprocess.run(["node", f.name], capture_output=True, text=True, timeout=30)
        Path(f.name).unlink()
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.loads(out.stdout), ["Review", "Analytics", "Thumbnails", "SEO & listing", "Review", "Picture", "Edit",
                                                  "Upload & schedule", "Voiceover", "Other"])

    def test_recently_done_strip_shows_the_last_five(self):
        # Ben, 14 Oct: "I'm not seeing tasks that are done."
        html = page()
        names = ["esc", "MINUTE", "ts", "ago", "WORKER", "cleanTitle", "plainTitle", "JOB_KINDS", "jobKindOf", "pw", "fd", "fw", "doneOpen", "renderDone"]
        lib = "\n".join(js_function(html, n) for n in dict.fromkeys(names + PROGRESS_FUNCTIONS))
        done = [{"id": f"J0{i}", "title": t, "by": "cursor", "at": at} for i, (t, at) in enumerate([
            ("HOS 005 Short s04 cover, set in its package manifest", "2026-10-12T14:30Z"),
            ("Upload packages for 3 Shorts: listing + manifest", "2026-10-12T14:00Z"),
            ("027 long VO take 2", "2026-10-11T09:00Z")])]
        script = f"""
const RealDate = Date, FIXED = RealDate.parse({json.dumps(self.NOW)});
globalThis.Date = class extends RealDate {{ constructor(...a){{ super(...(a.length?a:[FIXED])); }} static now(){{ return FIXED; }} }};
const box = {{hidden:true, className:"", innerHTML:"", querySelectorAll: () => []}};
const $ = id => id==="donebar" ? box : null;
const fromDb = {{extra: {{done: {json.dumps(done)}}}}};
{lib}
renderDone();
console.log(JSON.stringify(box));
"""
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(script)
        out = subprocess.run(["node", f.name], capture_output=True, text=True, timeout=30)
        Path(f.name).unlink()
        self.assertEqual(out.returncode, 0, out.stderr)
        r = json.loads(out.stdout)
        self.assertFalse(r["hidden"])
        self.assertEqual(r["className"], "donebar")   # something finished in the last day
        self.assertIn("2 jobs finished in the last 24 h", r["innerHTML"])
        self.assertIn('<span class="kd thumb">Thumbnails</span>', r["innerHTML"])
        self.assertIn('<span class="kd vo">Voiceover</span>', r["innerHTML"])
        self.assertLess(r["innerHTML"].index("HOS 005"), r["innerHTML"].index("027 long VO"))   # newest first
        self.assertIn("Cursor · job done · <span data-ago=", r["innerHTML"])

    def test_done_over_48h_goes_to_archive(self):
        done = [{"id": "J0190", "title": "OWB new", "at": "2026-10-12T10:00Z"}, {"id": "J0180", "title": "OWB old", "at": "2026-10-08T10:00Z"}]
        h = self.render(extra={"done": done})["jobboard"]["innerHTML"]
        self.assertIn("Archive (1)", h)
        self.assertLess(h.index("J0190"), h.index("Archive (1)"))
        self.assertGreater(h.index("J0180"), h.index("Archive (1)"))
