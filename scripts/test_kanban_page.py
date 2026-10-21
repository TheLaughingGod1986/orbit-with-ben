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


PROGRESS_FUNCTIONS = ["OWB_STAGES", "taskKeysFor", "taskStageInfo", "jobOutcome", "jobFollowUps", "jobImpact", "progressUpdates", "JOB_KINDS", "jobKindOf", "dailyWorkSummary", "videoTotals", "runningJob", "linkedJobsFor", "jobTargetHtml"]


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
                 "updatedAt", "STALL_MIN", "latestWorkActivity", "activityLine", "stallOf", "workLane", "jobQueueInfo", "hbLine", "NEEDS_BEN", "WAITS_INPUT", "cleanTitle", "WORKER", "readyAt", "jobKind", "plainTitle", "waitReason", "WAIT_WORD", "pcCol", "renderNow"]
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
        self.assertNotIn("J0129", re.sub(r"<[^>]*>", "", r["html"]))
        self.assertNotIn('class="jid"', r["html"])

    def test_next_up_stays_visible_with_progress_in_closed_dropdown(self):
        r = self.render()
        self.assertEqual(r["html"].count('<div class="nx">'), 1)
        self.assertLessEqual(r["html"].count('<li>'), 3)
        self.assertIn("<li>027 Earth Stopped Spinning rough v01f – frame-review fixes</li>", r["html"])
        self.assertIn('<details id="now-progress-J0129" class="progress-fold"><summary>Progress details</summary>', r["html"])
        self.assertNotIn('<details id="now-progress-J0129" class="progress-fold" open', r["html"])
        self.assertNotIn("jobs waiting", r["html"])

    def test_idle_box_is_plain_too(self):
        r = self.render(jobs=self.with_jobs(J0129=None))
        self.assertIn("<b>Now:</b> next job queued", r["html"])
        self.assertNotIn('<div class="pbar"', r["html"])

    def test_recent_review_hand_off_is_activity_even_if_last_fully_done_job_was_yesterday(self):
        lanes = {"mini": {"lastAt": "2026-10-11T19:10Z", "lastBy": "codex", "lastWhat": "blocked: parked for Chief: Studio sign-in",
                          "heartbeat": {"at": "2026-10-11T19:46Z", "state": "idle"}}}
        r=self.render(jobs=self.with_jobs(J0129=None),extra={"done":[{"id":"J0100","at":"2026-10-10T15:50Z"}]},lanes=lanes)
        self.assertIn("Last work sent for review",r["html"])
        self.assertNotIn("last job finished",r["html"])
        self.assertNotIn("nowbar asleep",r["className"])
        self.assertIn("Mac mini checked in <span",r["html"])
        # A fresh relay check-in alone must not mask genuinely old worker activity.
        lanes["mini"].update(lastAt="2026-10-10T15:50Z",lastWhat="done: delivered")
        r=self.render(jobs=self.with_jobs(J0129=None),extra={"done":[{"id":"J0100","at":"2026-10-10T15:50Z"}]},lanes=lanes)
        self.assertIn("no worker activity for",r["html"])
        self.assertIn(">1 d ago<",r["html"])
        self.assertIn("nowbar asleep",r["className"])
        self.assertNotIn('class="hb"',self.render(lanes=lanes)["html"])

    def test_review_work_is_not_described_as_finished(self):
        jobs=self.with_jobs(J0129=None)
        jobs.append({"id":"JREVIEW","title":"Short cut","needs":"mini","status":"blocked","result":"parked for Chief: Short PASS","by":"gemini","last":{"at":"2026-10-11T19:48Z","what":"blocked: parked for Chief: Short PASS"},"progress":{"step":4,"of":4,"at":"2026-10-11T19:47Z"}})
        r=self.render(jobs=jobs,extra={"done":[{"id":"J0100","at":"2026-10-11T12:50Z"}]})
        self.assertIn("Last work sent for review",r["html"])
        self.assertIn("JREVIEW",r["html"])
        self.assertNotIn("7 h ago",r["html"])
        self.assertNotIn("asleep",r["className"])

    def test_automatic_review_escalation_does_not_mask_old_worker_activity(self):
        jobs=self.with_jobs(J0129=None)
        jobs.append({"id":"JSTALE","title":"Old review","needs":"mini","status":"blocked","result":"parked for Chief: review","last":{"at":"2026-10-11T19:49Z","by":"refill","what":"escalated to Chief: parked 2 h"},"progress":{"step":4,"of":4,"at":"2026-10-10T19:47Z"}})
        r=self.render(jobs=jobs,extra={"done":[{"id":"J0100","at":"2026-10-11T12:50Z"}]})
        self.assertIn("no worker activity for",r["html"])
        self.assertIn("7 h ago",r["html"])
        self.assertIn("nowbar asleep",r["className"])

    def test_review_hold_without_ready_jobs_is_waiting_not_a_worker_stall(self):
        jobs=[{"id":"JREVIEW","title":"Awaiting review","needs":"mini","status":"blocked","result":"parked for Chief: Short PASS","last":{"at":"2026-10-11T12:50Z","by":"gemini","what":"blocked: parked for Chief: Short PASS"}}]
        r=self.render(jobs=jobs)
        self.assertIn("<b>Now:</b> waiting for review",r["html"])
        self.assertIn("Last work sent for review",r["html"])
        self.assertNotIn("asleep",r["className"])

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
        self.assertIn('data-ok="${id}">✓ Approve</button><button class="btn" data-chg="${id}">Comment / request changes', html.split("const extraItem")[1])
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
        names = ["esc", "MINUTE", "ts", "WORKER", "cleanTitle", "plainTitle", "pw", "fd", "fw", "filmJobs", "jobRollup", "jobRollupHtml", "ago"] + PROGRESS_FUNCTIONS
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

    def test_eight_audit_jobs_do_not_claim_eight_finished_videos(self):
        done = [{"id": f"J{i}", "title": "Backlog OWB: listing check on the last 10 live videos", "at": "2026-10-18T10:00Z"} for i in range(7)]
        done.append({"id": "J7", "title": "Daily Studio read: analytics", "at": "2026-10-18T10:00Z"})
        board = {"extra": {"day": {"since": "2026-10-17T23:00Z", "doneToday": 8}, "done": done}}
        html = self.evaluate('(()=>{Date.now=()=>Date.parse("2026-10-18T22:00Z"); return dailyWorkSummary()})()', board)
        self.assertIn("7 listing checks · 1 analytics read", html)
        self.assertIn("0 of 8 completed jobs linked to an individual video", html)

    def test_today_breakdown_uses_london_midnight_and_discloses_truncation(self):
        board = {"extra": {"day": {"since": "2026-10-17T23:00Z", "doneToday": 10}, "done": [
            {"id": "J1", "title": "Analytics", "at": "2026-10-17T23:30Z"},
            {"id": "J2", "title": "Analytics", "at": "2026-10-17T22:30Z"}]}}
        html = self.evaluate('(()=>{Date.now=()=>Date.parse("2026-10-18T22:00Z"); return dailyWorkSummary()})()', board)
        self.assertIn("Showing 1 of 10 job completions today", html)
        self.assertIn("1 analytics read", html)

    def test_video_totals_exclude_scheduled_and_live_from_unfinished(self):
        summary = self.evaluate('videoTotals({wait:Array(19),sched:Array(2),live:Array(1)})')
        self.assertEqual(summary, "19 unfinished videos · 2 scheduled · 1 live")

    def test_finished_subtask_changes_its_video_job_counts_without_finishing_the_video(self):
        board = {"jobs": [{"id":"J1", "title":"OWB 024: diagram fixes", "status":"claimed", "progress":{"step":2,"of":4}},
                          {"id":"J2", "title":"OWB 024: final review", "status":"blocked"}]}
        expression = """(()=>{const before=jobRollup('OWB:024'); const j=fromDb.jobs.shift();
          j.status='done';j.at=new Date().toISOString();j.result='New diagrams delivered';fromDb.extra={done:[j]};
          const after=jobRollup('OWB:024');return {before:[before.active,before.waiting,before.done],
            after:[after.active,after.waiting,after.done],html:jobRollupHtml('OWB:024')};})()"""
        result = self.evaluate(expression, board)
        self.assertEqual(result["before"], [1,1,0])
        self.assertEqual(result["after"], [0,1,1])
        self.assertIn("J1 done", result["html"])
        self.assertIn("1 waiting", result["html"])

    def test_now_box_discloses_work_outside_the_video_plan(self):
        board = {"owb":[{"film":"024"}]}
        html = self.evaluate('jobTargetHtml({id:"J1",title:"OWB ideas",taskKeys:["OWB:051"]})', board)
        self.assertIn("OWB:051", html)
        self.assertIn("outside the recorded video plan", html)

    def test_repo_disambiguates_numeric_video_ids_and_structured_links_are_used(self):
        self.assertEqual(self.evaluate('taskKeysFor({id:"J1",title:"Edit fixes",repo:"hos",film:"006"})'), ["HOS:006"])
        self.assertEqual(self.evaluate('taskKeysFor({id:"J1",title:"Shared overlays",taskKeys:["OWB:028","OWB:029"]})'), ["OWB:028", "OWB:029"])

    def test_live_job_wins_over_older_blocked_job_for_same_video(self):
        board = {"jobs": [
            {"id": "J1", "title": "HOS 006: older review", "status": "blocked", "last": {"at": "2026-10-17T10:00Z"}},
            {"id": "J2", "title": "HOS 006: fixes", "status": "claimed", "eta": "2099-10-18T23:00Z"}]}
        jobs = self.evaluate('linkedJobsFor("HOS:006")', board)
        self.assertEqual([j["id"] for j in jobs], ["J2", "J1"])

    def test_missing_and_cancelled_jobs_are_not_assumed_complete(self):
        self.assertIn("stepWhen", page())
        # Run the actual step resolver with an empty queue and a known terminal-state index.
        source = js_function(page(), "stepWhen")
        lib = "\n".join(js_function(page(), n) for n in ["esc", "ts"])
        script = f'''const fromDb={{jobs:[],extra:{{done:[]}},jobStates:{{J2:{{status:"done"}},J3:{{status:"cancelled"}}}}}};
{lib}
{source}
console.log(JSON.stringify([stepWhen({{job:"J1"}},{{}}),stepWhen({{job:"J2"}},{{}}),stepWhen({{job:"J3"}},{{}})]));'''
        out = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        unknown, done, cancelled = json.loads(out.stdout)
        self.assertFalse(unknown.get("ok", False))
        self.assertTrue(done["ok"])
        self.assertFalse(cancelled.get("ok", False))

    def test_refreshing_old_plan_keeps_recorded_scheduled_or_watched_status(self):
        source = js_function(page(), "currentFilmBrief")
        script = f'''const fromDb={{briefs:{{"OWB:025":{{updated:"2020-01-01T00:00Z",mood:"ready",line:"old work plan"}}}}}};
const ts=s=>Date.parse(s); const autoBrief=()=>({{mood:"good",steps:[]}});
{source}
console.log(JSON.stringify(currentFilmBrief({{key:"OWB:025"}})));'''
        out = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        brief = json.loads(out.stdout)
        self.assertEqual(brief["mood"], "ready")
        self.assertNotIn("line", brief)





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


@unittest.skipUnless(shutil.which("node"), "node not installed")
class ReleaseReadiness(unittest.TestCase):
    def evaluate(self, expression, board=None):
        names = ["RELEASE_RECORDS", "filmRelease", "releaseBlockers", "supportingJob", "ts", "stOf", "whoOf", "OWB_OWNER", "AGENT",
                 "CHIEF_PARK", "blockWhy", "isChiefPark", "linkedJobsFor", "runningJob", "taskKeysFor", "MINUTE"]
        lib = "\n".join(js_function(page(), n) for n in names)
        script = f"const fromDb={json.dumps(board or {})};\n{lib}\nconsole.log(JSON.stringify({expression}));"
        out = subprocess.run(["node", "-e", script], text=True, capture_output=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)

    def test_target_date_all_done_or_ready_note_never_proves_scheduled_or_live(self):
        film = {"key":"OWB:099", "_ch":"OWB", "air":"2020-01-01", "stages":{"upload":{"status":"done"}}}
        self.assertEqual(self.evaluate(f"filmRelease({json.dumps(film)})")["state"], "unscheduled")

    def test_actual_future_upload_receipt_is_scheduled(self):
        film = {"key":"OWB:025", "release":{"state":"scheduled", "publishAt":"2099-11-08T18:00:00Z", "videoId":"Js6EQJ8qDi8"}}
        self.assertEqual(self.evaluate(f"filmRelease({json.dumps(film)})")["state"], "scheduled")

    def test_post_release_jobs_do_not_block_a_recorded_schedule(self):
        row = {"f":{"key":"OWB:023"}, "isSched":True}
        board = {"jobs":[{"id":"J0324", "film":"023", "status":"blocked", "result":"waits for long public"}]}
        self.assertEqual(self.evaluate(f"releaseBlockers({json.dumps(row)})", board), [])

    def test_100_percent_without_schedule_gets_an_owner_and_verification_action(self):
        row = {"f":{"key":"OWB:099", "_stages":[]}, "pct":100}
        holds = self.evaluate(f"releaseBlockers({json.dumps(row)})")
        self.assertIn("no scheduled upload", holds[0]["reason"])
        self.assertIn("Chief", holds[0]["owner"])
        self.assertIn("publishAt", holds[0]["action"])

    def test_unhandled_change_notes_remain_a_blocker(self):
        row = {"f":{"key":"OWB:024", "_stages":[]}, "pct":100}
        board = {"checks":{"OWB-024":{"verdict":"change", "handled":False, "fixes":[{"text":"Explain the diagrams more clearly"}]}}}
        hold = self.evaluate(f"releaseBlockers({json.dumps(row)})", board)[0]
        self.assertIn("Explain the diagrams", hold["reason"])
        self.assertIn("revised cut", hold["action"])

    def test_complete_dependency_does_not_silently_unblock_job(self):
        row = {"f":{"key":"OWB:024", "_stages":[]}, "pct":80}
        board = {"jobStates":{"J1":{"status":"done"}}, "jobs":[{"id":"J2", "film":"024", "status":"blocked", "after":"J1", "result":"waiting on input"}]}
        holds = self.evaluate(f"releaseBlockers({json.dumps(row)})", board)
        self.assertIn("J1 is complete", holds[0]["action"])
        self.assertEqual(holds[0]["job"], "J2")


@unittest.skipUnless(shutil.which("node"), "node not installed")
class VideoWorkSchedule(unittest.TestCase):
    def evaluate(self, expression, board):
        names = ["MINUTE", "ts", "jobLine", "CHIEF_PARK", "blockWhy", "isChiefPark", "shortReason", "runningJob", "stepPace", "jobMin", "plan", "progressOf", "taskKeysFor", "linkedJobsFor", "progressUpdates", "filmJobs", "supportingJob", "workLane", "jobQueueInfo", "jobPriority", "videoPriority", "stOf", "videoWorkPlan"]
        lib = "\n".join(js_function(page(), n) for n in names)
        script = f"const fromDb={json.dumps(board)};\n{lib}\nconsole.log(JSON.stringify({expression}));"
        out = subprocess.run(["node", "-e", script], text=True, capture_output=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)

    def board(self):
        def job(jid, **fields):
            return dict(id=jid, title=jid, needs="mini", line="mini", status="open", typMin=10, **fields)
        a=job("J1", film="024", stage="picture"); a["status"]="claimed"
        fillers=[job(f"F{i}") for i in range(7)]
        b=job("J2", film="024", stage="edit", pos=6)
        c=job("J3", film="024", stage="upload", pos=9)
        jobs=[a,*fillers[:5],b,*fillers[5:],c]
        return {"jobs":jobs,"runOrder":{"mini":[j["id"] for j in jobs],"chief":[]},"extra":{"done":[]}}

    ROW = {"f":{"key":"OWB:024","_stages":[{"key":k,"label":k} for k in ("picture","edit","upload")],"stages":{}},"steps":[],"pct":89}

    def test_badges_follow_worker_queue_and_skip_held_or_gated_jobs(self):
        b=self.board()
        badges=self.evaluate("(()=>{const P=plan();return fromDb.jobs.slice(0,4).map(j=>jobPriority(j,P).text)})()",b)
        self.assertEqual(badges,["Working now","Next","#3","#4"])
        b["jobs"][1].update(status="blocked",result="parked for Chief: review")
        b["jobs"][2].update(notBefore="2099-01-01T10:00:00Z")
        badges=self.evaluate("(()=>{const P=plan();return fromDb.jobs.slice(1,5).map(j=>jobPriority(j,P).text)})()",b)
        self.assertEqual(badges,["Review","Date gated","Next","#3"])

    def test_held_video_priority_is_not_advertised_as_the_next_executable_job(self):
        b=self.board()
        for j in b["jobs"]:
            if j.get("film")=="024":j.update(status="blocked",result="parked for Chief: review")
        badge=self.evaluate(f"videoPriority({json.dumps(self.ROW)},plan(),{{'OWB:024':3}})",b)
        self.assertEqual(badge["text"],"Priority #3 · Review")
        self.assertIn("not an executable job queue position",badge["title"])

    def test_three_video_jobs_use_global_worker_queue_positions_six_and_nine(self):
        row=json.dumps(self.ROW)
        r=self.evaluate(f"(()=>{{const P=plan(),w=videoWorkPlan({row},P);return {{ids:w.remaining.map(x=>x.j.id),positions:w.remaining.map(x=>x.q.pos||0),finish:w.finish,last:P.J3.done,active:w.active[0].j.id}};}})()",self.board())
        self.assertEqual(r["ids"],["J1","J2","J3"])
        self.assertEqual(r["positions"],[0,6,9])
        self.assertEqual(r["finish"],r["last"])
        self.assertEqual(r["active"],"J1")

    def test_review_hold_prevents_a_whole_video_finish_estimate(self):
        b=self.board();j=next(j for j in b["jobs"] if j["id"]=="J2");j.update(status="blocked",result="parked for Chief: review")
        w=self.evaluate(f"videoWorkPlan({json.dumps(self.ROW)},plan())",b)
        self.assertEqual(w["finish"],0)
        self.assertIn("Chief review",w["finishReason"])
        self.assertEqual(w["held"][0]["q"]["state"],"review")

    def test_old_stage_dates_do_not_fill_in_an_unqueued_stage(self):
        row=json.loads(json.dumps(self.ROW));row["f"]["_stages"].append({"key":"thumbs","label":"Thumbnails"});row["f"]["stages"]["thumbs"]={"status":"todo","due":"2020-01-01"}
        w=self.evaluate(f"videoWorkPlan({json.dumps(row)},plan())",self.board())
        self.assertEqual(w["finish"],0)
        self.assertEqual(w["gaps"],[{"key":"thumbs","label":"Thumbnails"}])

    def test_channel_audits_do_not_inflate_remaining_production_jobs(self):
        b=self.board();b["jobs"].append({"id":"AUDIT","title":"Weekly OWB audit: channel review","taskKeys":["OWB:024"],"status":"blocked","result":"parked for Chief: audit"})
        w=self.evaluate(f"videoWorkPlan({json.dumps(self.ROW)},plan())",b)
        self.assertEqual(len(w["remaining"]),3)
        self.assertEqual(len(w["related"]),1)
        self.assertGreater(w["finish"],0)

    def test_completed_job_decrements_count_but_does_not_approve_the_stage(self):
        b=self.board();j=b["jobs"].pop(0);j.update(status="done",at="2026-10-19T10:00Z");b["extra"]["done"]=[j]
        w=self.evaluate(f"videoWorkPlan({json.dumps(self.ROW)},plan())",b)
        self.assertEqual(len(w["remaining"]),2)
        self.assertEqual(len(w["completed"]),1)
        self.assertEqual(w["gaps"],[])
        self.assertEqual(w["stageUpdates"][0]["key"],"picture")
        self.assertEqual(w["finish"],0)

    def test_cancelled_dependency_never_gets_a_start_time(self):
        b=self.board();j=next(j for j in b["jobs"] if j["id"]=="J2");j["after"]="CANCEL";b["jobStates"]={"CANCEL":{"status":"cancelled"}}
        w=self.evaluate(f"videoWorkPlan({json.dumps(self.ROW)},plan())",b)
        q=next(x["q"] for x in w["remaining"] if x["j"]["id"]=="J2")
        self.assertNotIn("start",q)
        self.assertEqual(w["finish"],0)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class VisibleJobResults(unittest.TestCase):
    def evaluate(self, code):
        names = ["esc", "MINUTE", "ts", "ago", "OWB_STAGES", "taskKeysFor", "jobOutcome", "progressUpdates",
                 "supportingJob", "cleanTitle", "plainTitle", "CHIEF_PARK", "blockWhy", "isChiefPark",
                 "stOf", "resultNote", "resultState", "videoResultHtml"]
        lib = "\n".join(js_function(page(), name) for name in names)
        script = "const fromDb={jobs:[],extra:{done:[]}};\n" + lib + "\n" + code
        out = subprocess.run(["node", "--input-type=commonjs"], input=script, text=True, capture_output=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)

    def test_completed_result_names_video_and_explains_pending_stage(self):
        r = self.evaluate('''
fromDb.extra.done=[{id:"J1",title:"HOS 006: picture fixes",taskKeys:["HOS:006"],stage:"picture",at:new Date().toISOString(),result:"Two picture fixes delivered."}];
const row={f:{key:"HOS:006",_stages:[{key:"picture",label:"Picture"}],stages:{picture:{status:"doing"}}}};
console.log(JSON.stringify(videoResultHtml(row)));
''')
        self.assertIn("Finished: HOS 006", r)
        self.assertIn("Two picture fixes delivered.", r)
        self.assertIn("Picture still needs confirmation", r)
        self.assertIn('data-result-job="J1"', r)

    def test_four_of_four_parked_job_stays_in_review_with_its_result(self):
        r = self.evaluate('''
const j={id:"J2",title:"HOS 006: script",taskKeys:["HOS:006"],status:"blocked",result:"parked for Chief: script review",progress:{step:4,of:4,at:new Date().toISOString()}};
fromDb.jobs=[j]; const row={f:{key:"HOS:006",_stages:[],stages:{}}};
console.log(JSON.stringify({html:videoResultHtml(row),note:resultNote(j)}));
''')
        self.assertIn("Ready for review", r["html"])
        self.assertNotIn("Finished:", r["html"])
        self.assertEqual(r["note"], "parked for Chief: script review")

    def test_reopened_job_drops_its_old_finished_receipt(self):
        r = self.evaluate('''
fromDb.jobs=[{id:"J3",status:"open"}];fromDb.extra.done=[{id:"J3",at:new Date().toISOString()}];
console.log(JSON.stringify(progressUpdates()));
''')
        self.assertEqual(r, [])

    def test_result_card_is_visible_before_the_video_lanes_and_history_is_folded(self):
        html = page()
        self.assertLess(html.index('id="latestResult"'), html.index('id="videos"'))
        self.assertIn('id="recentActivity" class="more fold"', html)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class DailyVideoProgress(unittest.TestCase):
    def evaluate(self, code):
        names=["WORD","OWB_STAGES","AGENT","owbFilm","filmPct","progress","stOf","progressWindow","videoMovement",
               "supportingJob","taskKeysFor","chanOf","periodWork"]
        lib="\n".join(js_function(page(),name) for name in names)
        script='''const fromDb={jobs:[],videoProgress:{periods:{day:{channels:{HOS:{available:true,definitions:[{key:"picture",weight:100}],films:{"HOS:006":{stages:{picture:{status:"doing",progress:0.4}}}}}},work:[]}}}};
let progressPeriod="day",chan="all";const videoScheduleRows=new Map();
'''+lib+'''
const row={f:{key:"HOS:006",_ch:"HOS",_stages:[{key:"picture",label:"Picture",weight:100}],stages:{picture:{status:"doing",progress:0.6}}}};
'''+code
        out=subprocess.run(["node"],input=script,text=True,capture_output=True,timeout=30)
        self.assertEqual(out.returncode,0,out.stderr)
        return json.loads(out.stdout)

    def test_comparison_uses_historical_stage_progress_and_completed_job_does_not_fill_bar(self):
        r=self.evaluate('''fromDb.videoProgress.periods.day.work=[{id:"J1",done:true}];console.log(JSON.stringify(videoMovement(row)));''')
        self.assertEqual((r['previous'],r['current'],r['delta']),(40,60,20))
        self.assertEqual(r['kind'],'advanced')
        self.assertEqual(r['changes'][0],{'stage':'Picture','from':'in progress 40%','to':'in progress 60%'})

    def test_unchanged_regression_new_and_missing_history_are_distinct(self):
        r=self.evaluate('''const h=fromDb.videoProgress.periods.day.channels.HOS;const out=[];
h.films["HOS:006"].stages.picture.progress=0.6;out.push(videoMovement(row).kind);
h.films["HOS:006"].stages.picture.progress=0.8;out.push(videoMovement(row).kind);
delete h.films["HOS:006"];out.push(videoMovement(row).kind);
h.available=false;out.push(videoMovement(row).kind);console.log(JSON.stringify(out));''')
        self.assertEqual(r,['unchanged','reduced','new','unavailable'])

    def test_changed_weights_are_not_called_video_progress(self):
        r=self.evaluate('''fromDb.videoProgress.periods.day.channels.HOS.definitions[0].weight=35;console.log(JSON.stringify(videoMovement(row)));''')
        self.assertEqual(r['kind'],'unavailable')
        self.assertIn('not comparable',r['reason'])

    def test_work_categories_do_not_double_count_channel_qa_or_outside_plan(self):
        r=self.evaluate('''videoScheduleRows.set("HOS:006",row);
fromDb.videoProgress.periods.day.work=[{id:"QA",title:"Backlog: QA sweep of newest packs on both channels",taskKeys:["HOS:006"],status:"blocked"},{id:"VIDEO",title:"HOS 006 picture fixes",taskKeys:["HOS:006"],done:true},{id:"OTHER",title:"HOS new script",taskKeys:["HOS:099"]}];
const w=periodWork([row]);console.log(JSON.stringify({video:w.video.map(j=>j.id),outside:w.outside.map(j=>j.id),checks:w.checks.map(j=>j.id),done:w.finished}));''')
        self.assertEqual(r,{'video':['VIDEO'],'outside':['OTHER'],'checks':['QA'],'done':1})


if __name__ == "__main__":
    unittest.main()
