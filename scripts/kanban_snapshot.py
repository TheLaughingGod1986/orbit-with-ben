#!/usr/bin/env python3
"""Refresh the snapshots built into the Studio Kanban page (https://claude.ai/artifact/Hhk519dkbHMzeaZfp3efhc).

The page reads both repos live through the viewer's GitHub connector. When that link isn't available, it shows the
snapshot built into the page, so Claude rebuilds that snapshot a few times a day from:
  - HOS: 00_Brand/Channel-Setup/PIPELINE.json in history-of-science (main)
  - OWB: every 02_Video-Projects/*/status.json in this repo (main)

  python3 scripts/kanban_snapshot.py <page.html> --hos <history-of-science checkout> [--out <page.html>]
  python3 scripts/kanban_snapshot.py --hos <checkout> --db-out <dir>    # board/hos, board/owb, board/credits, board/briefs

Since 7 Oct the page also reads `board/hos` ({updatedAt, pipeline}) and `board/owb` ({updatedAt, films}) from its own
store, which Claude writes on a schedule with ArtifactData (file_path = the JSON files --db-out writes). That keeps
the board current without the viewer's GitHub connector.

Since 8 Oct (Ben: "what's the holdup, what is it waiting for, and when does that happen?") it also writes `board/briefs`:
Claude's plain note per film from 05_Analytics/kanban/film_briefs.json, and every stage in hand gets a `since` (when it
took its current state, from the file's git history) so the page can say "in this stage 2 days".

It replaces only the two `const SNAPSHOT = …;` / `const OWB_SNAPSHOT = …;` lines, fails if either is missing, and
prints "unchanged" when the data is the same (so nothing needs republishing).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def js(obj) -> str:
    # `</` escaped so no value can close the page's script tag.
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def rebuild(html: str, hos: dict, owb: list[dict]) -> str:
    for name in ("SNAPSHOT", "OWB_SNAPSHOT"):
        if len(re.findall(rf"^const {name} = .*;$", html, flags=re.M)) != 1:
            raise SystemExit(f"page has no single `const {name} = …;` line; not touching it")
    html = re.sub(r"^const SNAPSHOT = .*;$", lambda m: "const SNAPSHOT = " + js(hos) + ";", html, flags=re.M)
    return re.sub(r"^const OWB_SNAPSHOT = .*;$", lambda m: "const OWB_SNAPSHOT = " + js(owb) + ";", html, flags=re.M)


# ---- "At a glance" (Ben, 8 Oct): how long each queued job takes, and when the Mini last did anything ----
# Minutes from "ready" to "done", from the queue's own history (8 Oct: median 49, recent 024 jobs 14-41). Keyword
# estimates keep it simple; the page turns them into start/finish times from the job's place in its lane.
EST = [(("reading", "readings"), 15), (("assemble", "rough", "full rough", "final picture", "render"), 45),
       (("omni", "veo", "flow", "mint"), 60), (("vo take", "voiceover", "vo "), 25), (("thumb", "cover"), 30),
       (("package", "upload", "trailer"), 20), (("harvest", "pool", "licence", "commit "), 15)]


LEARNED: dict = {}  # kind -> median minutes from history (set by learn_estimates)


def kind_of(j: dict) -> int:
    t = (j.get("title") or "").lower()
    return next((i for i, (words, _) in enumerate(EST) if any(w in t for w in words)), -1)


def _t(s: str):
    from datetime import datetime, timezone
    s = (s or "").replace("Z", "")
    for f in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(s[:19] if len(s) > 16 else s, f).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def learn_estimates(alljobs: list[dict]) -> None:
    """Median minutes from 'ready' (added, or its --after job done) to done, per kind of job, once a kind has 3+ done
    jobs. Mini jobs only, so a Gemini or Claude job doesn't skew the Mini's line-up."""
    import statistics
    done_at = {j["id"]: _t(next((h["at"] for h in reversed(j.get("history") or []) if h["what"].startswith("done")), ""))
               for j in alljobs}
    per: dict = {}
    for j in alljobs:
        h = j.get("history") or []
        if j.get("needs") != "mini" or not h or not done_at.get(j["id"]):
            continue
        ready = _t(h[0]["at"])
        if j.get("after") and done_at.get(j["after"]):
            ready = max(ready, done_at[j["after"]])
        mins = (done_at[j["id"]] - ready).total_seconds() / 60 if ready else None
        if mins is not None and 0 < mins < 8 * 60:  # a job that sat overnight on a sleeping Mini says nothing about its length
            per.setdefault(kind_of(j), []).append(mins)
    LEARNED.clear()
    LEARNED.update({k: round(statistics.median(v)) for k, v in per.items() if len(v) >= 3})


# Ben, 12 Oct 15:49: job board numbers. All from the queue's own history; nothing estimated or made up.
def _done_at(j: dict) -> str:
    return next((h["at"] for h in reversed(j.get("history") or []) if str(h.get("what", "")).startswith("done")), "")


def completed_jobs(alljobs: list[dict], at=None) -> list[dict]:
    """Recent activity plus the last result per video/stage, so busy channels don't erase it."""
    from datetime import datetime, timezone, timedelta
    at = at or datetime.now(timezone.utc)
    rows = sorted((dict({k: j.get(k, "") for k in
                         ("id", "title", "film", "by", "repo", "stage", "model", "ref", "result")},
                        taskKeys=j.get("taskKeys", []), at=_done_at(j))
                   for j in alljobs if j.get("status") == "done" and _t(_done_at(j))),
                  key=lambda j: _t(j["at"]), reverse=True)
    kept, seen = [], set()
    for i, j in enumerate(rows):
        keys = set(j["taskKeys"] or [])
        if not keys:
            keys.update(m[0].upper() + ":" + m[1] for m in
                        re.findall(r"\b(HOS|OWB)\s*[:·-]?\s*(\d{3})\b", j["title"], re.I))
            film = str(j["film"])
            if re.fullmatch(r"(HOS|OWB):\d{3}", film):
                keys.add(film)
            elif not keys:
                no = film if re.fullmatch(r"\d{3}", film) else (re.match(r"^\s*(\d{3})\b", j["title"]) or [""])[0].strip()
                if no:
                    ch = "HOS" if j["repo"] == "hos" or re.search(r"\bHOS\b|history of science", j["title"], re.I) else "OWB"
                    keys.add(ch + ":" + no)
            keys.update(m[0].upper() + ":" + m[1] for m in
                        re.findall(r"\b(HOS|OWB)\s*[:·-]?\s*(\d{3})\b", j["result"], re.I))
        targets = {(key, j["stage"]) for key in keys if re.fullmatch(r"(HOS|OWB):\d{3}", key)}
        if i < 60 or _t(j["at"]) >= at - timedelta(days=1) or targets - seen:
            kept.append(j)
        seen.update(targets)
    return kept


def kind_key(j: dict) -> str:
    """A job's kind for typical durations: its queue kind if set, else the title keyword family."""
    k = kind_of(j)
    return (j.get("kind") or "") or (EST[k][0][0] if k >= 0 else "other")


def typical_minutes(alljobs: list[dict], default: int = 30) -> dict:
    """Median claimed->done minutes per kind_key (3+ done jobs, floor 15 min so quick jobs do not alarm), runs over 8 h ignored; others fall back to `default`."""
    import statistics
    per: dict = {}
    for j in alljobs:
        if j.get("status") != "done":
            continue
        claimed = next((h["at"] for h in reversed(j.get("history") or []) if str(h.get("what", "")).startswith("claimed")), "")
        a, b = _t(claimed), _t(_done_at(j))
        if a and b and 0 < (b - a).total_seconds() < 8 * 3600:
            per.setdefault(kind_key(j), []).append((b - a).total_seconds() / 60)
    out = {k: max(15, round(statistics.median(v))) for k, v in per.items() if len(v) >= 3}
    out["_default"] = default
    # Chief reviews: from "parked for Chief" to the next step on that job (done/reopened/claimed), floor 60 min, default 4 h.
    rev = []
    for j in alljobs:
        a = None
        for h in j.get("history") or []:
            what, at = str(h.get("what", "")).lower(), _t(h.get("at", ""))
            if what.startswith("blocked") and "chief" in what:
                a = at
            elif a and at and what.split(":")[0] in ("done", "reopened", "claimed", "open", "unblocked"):
                if 0 < (at - a).total_seconds() < 3 * 86400:
                    rev.append((at - a).total_seconds() / 60)
                a = None
    out["_review"] = max(60, round(statistics.median(rev))) if len(rev) >= 3 else 240
    return out


def _mini_numbers(alljobs: list[dict], start, end) -> tuple[int, int]:
    """Jobs done in [start, end), and minutes of that window in which no Mac mini job was claimed (the Mini idle)."""
    done = sum(1 for j in alljobs for h in j.get("history") or []
               if str(h.get("what", "")).startswith("done") and _t(h.get("at", "")) and start <= _t(h.get("at", "")) < end)
    spans = []
    for j in alljobs:
        if j.get("needs") != "mini":
            continue
        a = None
        for h in j.get("history") or []:
            what, at = str(h.get("what", "")), _t(h.get("at", ""))
            if what.startswith("claimed"):
                a = at
            elif a and at and what.split(":")[0] in ("released", "done", "blocked", "block", "reopened"):
                spans.append((a, at)); a = None
        if a and j.get("status") == "claimed":
            spans.append((a, end))
    busy, cur = 0.0, None
    for a, b in sorted((max(a, start), min(b, end)) for a, b in spans if b > start and a < end):
        if cur and a <= cur[1]:
            cur = (cur[0], max(cur[1], b))
        else:
            if cur:
                busy += (cur[1] - cur[0]).total_seconds()
            cur = (a, b)
    if cur:
        busy += (cur[1] - cur[0]).total_seconds()
    return done, max(0, round(((end - start).total_seconds() - busy) / 60))


def _london_midnight(t):
    from datetime import timezone
    from zoneinfo import ZoneInfo
    return t.astimezone(ZoneInfo("Europe/London")).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)


def day_numbers(alljobs: list[dict], now=None) -> dict:
    """Jobs done since London midnight, and minutes since then that no Mac mini job was claimed (the Mini idle)."""
    from datetime import datetime, timezone
    now = now or datetime.now(timezone.utc)
    start = _london_midnight(now)
    done, idle = _mini_numbers(alljobs, start, now)
    return {"since": start.strftime("%Y-%m-%dT%H:%MZ"), "doneToday": done, "idleMin": idle}


def week_numbers(alljobs: list[dict], now=None, days: int = 7) -> list[dict]:
    """The same two numbers for each of the last `days` London days, oldest first, today (so far) last. The board's
    tiles draw them as small bars (Ben, 14 Oct: "make it more dynamic"), so a quiet day stands out next to a busy one."""
    from datetime import datetime, timedelta, timezone
    from zoneinfo import ZoneInfo
    now = now or datetime.now(timezone.utc)
    out, start = [], _london_midnight(now)
    for _ in range(days):
        end = min(now, _london_midnight(start + timedelta(hours=36)))  # next London midnight (DST-safe)
        done, idle = _mini_numbers(alljobs, start, end)
        out.append({"date": start.astimezone(ZoneInfo("Europe/London")).strftime("%Y-%m-%d"), "done": done, "idleMin": idle,
                    "min": round((end - start).total_seconds() / 60)})
        start = _london_midnight(start - timedelta(hours=12))
    return out[::-1]


def est_minutes(j: dict) -> int:
    k = kind_of(j)
    if k in LEARNED:
        return max(5, LEARNED[k])
    return EST[k][1] if k >= 0 else 25


def makes_video(j: dict) -> bool:
    """A job whose result Ben can watch in OWB UAT (a cut), as opposed to sheets, packages or text."""
    t = (j.get("title") or "").lower()
    return j.get("stage") == "edit" and any(w in t for w in ("rough", "cut", "picture", "assemble"))


# ---- Plain progress (Ben, 11 Oct 22:09: "we're currently working on X, 20% done, finished in 30 minutes") ----
STEP_RE = re.compile(r"\bsteps?\s+(\d{1,3})\s*(?:/|of)\s*(\d{1,3})\b", re.I)


def job_progress(j: dict) -> dict | None:
    """Real step progress for a job, or None: `jobs.py progress` (job["progress"]: step k of n finished) if the worker
    reported it, else the newest "step k of n" in the job's own history notes since it was last added or reopened
    (a release note like "stopping point; step 3 of 8 done"). The page turns it into % done; without it the page uses
    the time since work started against the estimate, capped at 95%."""
    p = j.get("progress")
    if isinstance(p, dict) and isinstance(p.get("step"), int) and isinstance(p.get("of"), int) and 0 <= p["step"] <= p["of"] and p["of"] >= 1:
        return {"step": p["step"], "of": p["of"], "at": p.get("at", ""), **({"note": p["note"]} if p.get("note") else {})}
    found = None
    for h in j.get("history") or []:
        what = str(h.get("what", ""))
        if what.startswith(("added", "reopened")):
            found = None
            continue
        m = STEP_RE.search(what)
        if m and 0 <= int(m.group(1)) <= int(m.group(2)) and int(m.group(2)) >= 1:
            found = {"step": int(m.group(1)), "of": int(m.group(2)), "at": h.get("at", "")}
    return found


def work_start(j: dict) -> str:
    """When work on this job began: its first claim since it was added or last reopened (released-and-reclaimed
    stretches count as one piece of work), so % done by time covers the whole job, not just the latest run."""
    start = ""
    for h in j.get("history") or []:
        what = str(h.get("what", ""))
        if what.startswith(("added", "reopened")):
            start = ""
        elif what.startswith("claimed") and not start:
            start = h.get("at", "")
    return start


def mini_heartbeat() -> dict | None:
    """The Mini's relay heartbeat (scripts/chief_relay.py push_heartbeat) from the mini-heartbeat branch, if any."""
    import subprocess
    try:
        subprocess.run(["git", "-C", str(ROOT), "fetch", "-q", "origin", "mini-heartbeat"], capture_output=True, timeout=60, check=True)
        out = subprocess.run(["git", "-C", str(ROOT), "show", "FETCH_HEAD:heartbeat.json"], capture_output=True, text=True,
                             timeout=30, check=True).stdout
        return json.loads(out)
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def mini_work(alljobs: list[dict], since: str) -> dict:
    """What the Mac mini's agents (Cursor, Grok, Codex) actually did since a date, from the queue history: each claim
    to its release/done/block is one stretch of work (capped at 8 h, so a claim left open overnight doesn't count as
    work). Ben, 8 Oct: at the check-in, would Claude Max cover what Cursor does?"""
    jobs, minutes, by_film, by_agent = set(), 0.0, {}, {}
    for j in alljobs:
        if j.get("needs") != "mini":
            continue
        start = None
        for h in j.get("history") or []:
            what, at = h.get("what", ""), _t(h.get("at", ""))
            if what.startswith("claimed"):
                start = (at, h.get("by", ""))
            elif start and at and start[0] and what.split(":")[0] in ("released", "done", "blocked", "block"):
                if h.get("at", "") >= since:
                    m = min(8 * 60, max(0.0, (at - start[0]).total_seconds() / 60))
                    jobs.add(j["id"])
                    minutes += m
                    key = f"OWB:{j['film']}" if j.get("film") else "admin"
                    by_film[key] = by_film.get(key, 0) + m
                    who = start[1] or "?"
                    by_agent[who] = by_agent.get(who, 0) + m
                start = None
    return {"since": since, "jobs": len(jobs), "minutes": round(minutes),
            "byFilm": {k: round(v) for k, v in sorted(by_film.items())}, "byAgent": {k: round(v) for k, v in by_agent.items()}}


def lanes_info(alljobs: list[dict]) -> dict:
    out = {}
    for lane in ("mini", "gemini", "cloud", "ben"):
        acts = [(h["at"], h.get("by", ""), h["what"]) for j in alljobs if j.get("needs") == lane
                for h in j.get("history") or [] if h.get("by") and h.get("by") != "claude" or lane == "cloud"]
        if acts:
            at, by, what = max(acts)
            out[lane] = {"lastAt": at, "lastBy": by, "lastWhat": what[:160]}
    return out


# ---- Film by film (Ben, 8 Oct): how long each stage has been where it is, and Claude's plain note per film ----
BRIEFS = ROOT / "05_Analytics" / "kanban" / "film_briefs.json"


def since_from_history(snaps: list[tuple[str, dict]], truncated: bool) -> dict:
    """snaps: [(iso time, {key: state})], oldest first. When each key took the state it has now. A key that already
    had that state in the oldest snapshot of a cut-short history gets no time (we can't see when it started)."""
    if not snaps:
        return {}
    cur = snaps[-1][1]
    out = {}
    for key, state in cur.items():
        at = None
        for when, states in reversed(snaps):
            if states.get(key) != state:
                break
            at = when
        if at and not (truncated and at == snaps[0][0]):
            out[key] = at
    return out


def file_history(repo: Path, rel: str, states, limit: int = 80) -> dict:
    """since_from_history over the git history of one JSON file. states(doc) -> {key: state}."""
    import subprocess
    try:
        log = subprocess.run(["git", "-C", str(repo), "log", f"-n{limit}", "--format=%H %cI", "--", rel],
                             capture_output=True, text=True, timeout=60, check=True).stdout.split("\n")
        shallow = subprocess.run(["git", "-C", str(repo), "rev-parse", "--is-shallow-repository"],
                                 capture_output=True, text=True, timeout=30).stdout.strip() == "true"
    except (OSError, subprocess.SubprocessError):
        return {}
    commits = [line.split(" ", 1) for line in log if " " in line][::-1]
    snaps = []
    for h, at in commits:
        try:
            doc = json.loads(subprocess.run(["git", "-C", str(repo), "show", f"{h}:{rel}"], capture_output=True,
                                            text=True, timeout=30, check=True).stdout)
            snaps.append((at, states(doc)))
        except (OSError, subprocess.SubprocessError, ValueError, AttributeError, TypeError, KeyError):
            continue
    return since_from_history(snaps, truncated=shallow or len(commits) >= limit)


LIVE = ("doing", "review", "blocked")  # only stages in hand get a "since"; done and to-do stages don't need one


def add_since_owb(films: list[dict]) -> None:
    for f in films:
        d = next(iter(sorted((ROOT / "02_Video-Projects").glob(f"{f.get('film')}_*/status.json"))), None)
        if not d:
            continue
        since = file_history(ROOT, str(d.relative_to(ROOT)),
                             lambda doc: {k: v.get("state") for k, v in (doc.get("stages") or {}).items()})
        for k, st in (f.get("stages") or {}).items():
            if st.get("state") in LIVE and since.get(k) and not st.get("since"):
                st["since"] = since[k]


def add_since_hos(repo: Path, hos: dict) -> None:
    since = file_history(repo, "00_Brand/Channel-Setup/PIPELINE.json",
                         lambda doc: {f"{f['id']}/{k}": v.get("status") for f in doc["films"] for k, v in f["stages"].items()})
    for f in hos.get("films", []):
        for k, st in (f.get("stages") or {}).items():
            if st.get("status") in LIVE and since.get(f"{f['id']}/{k}") and not st.get("since"):
                st["since"] = since[f"{f['id']}/{k}"]


def load_briefs() -> dict:
    if not BRIEFS.exists():
        return {}
    films = json.loads(BRIEFS.read_text()).get("films", {})
    bad = [k for k in films if not re.fullmatch(r"(HOS|OWB):\d{3}", k)]
    urls = [u for u in [json.loads(BRIEFS.read_text()).get("uatFolderUrl", "")] + [b.get("uatUrl", "") for b in films.values()] if u]
    if any(not u.startswith("https://www.icloud.com/") for u in urls):
        raise SystemExit("film_briefs.json: UAT links must be https://www.icloud.com/ share links")
    if bad:
        raise SystemExit(f"film_briefs.json: keys must be HOS:NNN or OWB:NNN, not {bad}")
    return films


# ---- Order of work (Ben, 10 Oct: "the order of work seems to be gone") ----
# The board shows each live job's place in line, the same order scripts/jobs.py's `next` uses: what a worker holds
# first, then jobs.order() (addressed to the agent, urgent in the order named, focus film, other films, quick jobs, id),
# skipping a job until the job it waits for (`after`) is done. Two lines: the Mac mini's workers (Cursor/Codex take
# mini, gemini and any) and the Chief (jobs addressed `for: chief`, and cloud). A job held up by a blocked job or one in
# the other line has no number; it says what it waits for.
WORKER_NEEDS = {"mini", "gemini", "any"}


def _job_order():
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import jobs as _jobs  # the queue's own sort key, so the board can't drift from it
        return _jobs.order
    except Exception:  # noqa: BLE001  (fallback copy of jobs.order, 9 Oct)
        def order(job, focus=()):
            u = job.get("urgent")
            rank = u if isinstance(u, int) and not isinstance(u, bool) else 0
            return (0 if job.get("for") else 1, 0 if u else 1, rank if u else 0,
                    0 if job.get("film") and job["film"] in focus else 1, 0 if job.get("film") else 1,
                    0 if (job.get("eta_min") or 120) <= 60 else 1, job["id"])
        return order


def line_of(j: dict) -> str:
    if j.get("needs") == "ben":
        return "ben"
    if j.get("for") == "chief" or j.get("needs") == "cloud":
        return "chief"
    return "mini" if j.get("needs") in WORKER_NEEDS else "other"


# ---- Date gates (Ben, 11 Oct: "No eta" on a job that can't start before an air date) ----
# A job's not-before time: its own `not_before` field if it has one, else a date written next to gate words in its title
# or the top of its body ("mark done on/after Sun 8 Nov 18:00Z", "once ... is public (Sun 8 Nov 18:00Z)"). A trailing Z
# is UTC; otherwise London time. A job waiting (`after`) on a gated job inherits the gate.
GATE_WORDS = re.compile(r"date gate|on/after|on or after|not before|only on|go(?:es)?[- ]public|is public|shows as public", re.I)
GATE_DATE = re.compile(r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\w*\s+(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*"
                       r"(?:\s+(\d{4}))?\s+(\d{1,2}):(\d{2})\s*(Z|UTC)?")
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def gate_of(j: dict, today=None) -> str:
    """Ben, 12 Oct 2026 14:37: no fixed start times on the board. A job waiting on an input is blocked/after, not
    clocked, so there is no start gate to show."""
    return ""


def _old_gate_of(j: dict, today=None) -> str:  # kept for reference; unused
    import datetime as _dt
    from zoneinfo import ZoneInfo
    if j.get("not_before"):
        return str(j["not_before"])
    for text in (j.get("title") or "", (j.get("body") or "")[:400]):
        if not GATE_WORDS.search(text):
            continue
        m = GATE_DATE.search(text)
        if not m:
            continue
        d, mon, yr, hh, mm, z = m.groups()
        today = today or _dt.datetime.now(_dt.timezone.utc)
        year = int(yr) if yr else today.year
        tz = _dt.timezone.utc if z else ZoneInfo("Europe/London")
        t = _dt.datetime(year, MONTHS.index(mon[:3]) + 1, int(d), int(hh), int(mm), tzinfo=tz)
        if not yr and t < today - _dt.timedelta(days=60):
            t = t.replace(year=year + 1)
        return t.astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    return ""


def gates(alljobs: list[dict]) -> dict:
    """{id: not-before ISO} for live jobs, own gate or inherited along `after`."""
    byid = {j["id"]: j for j in alljobs}
    out = {}

    def g(j, seen=()):
        if j["id"] in out:
            return out[j["id"]]
        own = gate_of(j)
        dep = byid.get(j.get("after") or "")
        inh = g(dep, seen + (j["id"],)) if dep and dep["id"] not in seen and dep.get("status") != "done" else ""
        out[j["id"]] = max(own, inh)
        return out[j["id"]]
    for j in alljobs:
        if j.get("status") in ("open", "claimed", "blocked"):
            g(j)
    return {k: v for k, v in out.items() if v}


def run_order(alljobs: list[dict], focus=()) -> dict:
    """{"lines": {"mini": [ids in run order], "chief": [...]}, "pos": {id: {line, pos, waitsFor}}}. pos 0 = in hand now."""
    order = _job_order()
    live = {j["id"]: j for j in alljobs if j.get("status") in ("open", "claimed", "blocked")}
    out, lines = {}, {}
    for ln in ("mini", "chief"):
        mine = [j for j in live.values() if line_of(j) == ln]
        seq = [j["id"] for j in sorted((j for j in mine if j["status"] == "claimed"), key=lambda j: j["id"])]
        for i in seq:
            out[i] = {"line": ln, "pos": 0}
        done, n = set(seq), 0
        todo = [j for j in mine if j["status"] == "open"]
        while True:
            ready = [j for j in todo if j["id"] not in done and (not j.get("after") or j["after"] not in live or j["after"] in done)]
            if not ready:
                break
            j = min(ready, key=lambda j: order(j, tuple(focus)))
            done.add(j["id"]); seq.append(j["id"]); n += 1
            out[j["id"]] = {"line": ln, "pos": n}
        for j in mine:
            if j["id"] not in out:
                out[j["id"]] = {"line": ln, "pos": None,
                                "waitsFor": "" if j["status"] == "blocked" else j.get("after", "")}
        lines[ln] = seq
    return {"lines": lines, "pos": out}


# ---- Who reviews (Ben's studio, 9 Oct): reviews, PASSes, music checks and final OKs are the Chief's, not Claude's ----
# The film notes and status files were written while Claude was Chief. The board says "Chief" for every review step
# still to come; done steps keep who really did them. Claude's own making work (drawing, graphics) keeps its name.
REVIEW_WORDS = re.compile(r"\b(check|checks|review|reviews|pass|passes|PASS|listen|final OK|OK|approve|launch check|look at|sees stills|frame by frame)\b", re.I)
REVIEW_TEXT = [(re.compile(r"\bClaude's final OK\b"), "the Chief's final OK"),
               (re.compile(r"\bClaude launch check\b"), "Chief launch check"),
               (re.compile(r"\bClaude sees stills\b"), "The Chief sees stills"),
               (re.compile(r"\bClaude (checks|reviews|passes|listens|OKs)\b"), r"The Chief \1")]


def chief_text(s):
    if not isinstance(s, str) or "Claude" not in s:
        return s
    for rx, rep in REVIEW_TEXT:
        s = rx.sub(rep, s)
    return re.sub(r"(^|[.!?]\s+)the Chief", r"\1The Chief", s)


# ---- Who does each step still to do (Ben, 12 Oct: "Is Gemini not used at all?") ----
# From 11 Oct, scripts/routing.py decides who does each kind of job (AGENTS.md "Who does what"). Past steps keep their
# true doer (a done stage's owner, or the agent that claimed/finished the job). A step still to do shows the routed
# worker for its kind: a film-note step with `kind`, or with a `job` whose queue entry has a kind. A job that is claimed
# shows whoever holds it. HOS queue jobs ("HOS 006 ...") the note doesn't name are added to the note, as the page does
# for OWB jobs, so an HOS card moves with the queue too.
HOS_STAGE_KIND = {"topic": "review", "script": "script", "facts": "facts", "package": "listing", "vo": "vo",
                  "shorts_scripts": "script", "shorts_vo": "vo", "picture": "video", "edit": "assembly",
                  "thumbnails": "chart", "scheduled": "studio"}
HOS_JOB = re.compile(r"^HOS\s+(\d{3})\b")
# A step with no kind still routes when its words say plainly what it is: a facts check (Gemini) or code graphics (Codex).
KIND_WORDS = [("facts", re.compile(r"\bfact[- ]?checks?\b|\bsources\b|\bcheck (?:every|the|all) (?:numbers?|dates?|claims?|facts?)", re.I)),
              ("chart", re.compile(r"\bcharts?\b|\bgraphs?\b|people cards?|code graphics|\boverlays?\b|date stamps?|\bWHO cards?", re.I))]


def kind_of_step(what: str) -> str:
    return next((k for k, rx in KIND_WORDS if rx.search(what or "")), "")


def worker_name(agent: str, model: str = "") -> str:
    """Board name for a routing lane: the model's maker for model-led lanes, else the worker."""
    if model == "grok" or agent == "chief":
        return "Chief"
    if model == "cursor-claude-opus-5-5":
        return "Claude (in Cursor)"
    if model.startswith("claude"):
        return "Claude"
    if model == "gemini-agy":
        return "Gemini"
    if model.startswith("gpt-"):
        return "Codex"
    return {"cursor": "Cursor", "codex": "Codex", "gemini": "Gemini", "claude": "Claude"}.get(agent, agent.title())


def _routing():
    sys.path.insert(0, str(ROOT / "scripts"))
    import routing
    return routing


def routing_doc() -> dict:
    """{kind: {what, who, chain}} for the page: who does each kind first, then the stand-ins in order."""
    r = _routing()
    return {k: {"what": what, "who": worker_name(*ch[0]), "chain": [worker_name(a, m) for a, m in ch]}
            for k, (what, ch, _how) in r.CHAINS.items()}


def routed_who(kind: str = "", model: str = "") -> str:
    r = _routing()
    if model and model in r.RUNS_ON and not kind:
        return worker_name(r.RUNS_ON[model], model)
    ch = r.job_chain({"kind": kind, "model": model})
    if not ch:
        return ""
    if model and model in r.RUNS_ON:  # a job pinned to a model runs on that model's worker
        return worker_name(r.RUNS_ON[model], model)
    return worker_name(*ch[0])


def job_doer(j: dict) -> str:
    """The agent that holds or finished a job ("chief/gemini" is Gemini run by the Chief; "chief" alone is Grok)."""
    b = str(j.get("by") or "").lower()
    last = b.split("/")[-1]
    if last in ("gemini", "agy"):
        return "Gemini"
    if b == "chief" or b.startswith("chief/"):
        return "Grok"
    return last.title() if last else ""


def job_who(j: dict) -> str:
    """Who a queue job shows on a card: whoever holds or did it, else the routed worker for its kind."""
    if j.get("status") in ("claimed", "done") and j.get("by"):
        return job_doer(j)
    return routed_who(j.get("kind") or "", j.get("model") or "")


def hos_job_steps(briefs: dict, alljobs: list[dict]) -> dict:
    """Add live HOS queue jobs a note doesn't name yet (before Ben's own steps), each with its job id and kind."""
    out = {}
    live = [j for j in alljobs if j.get("status") in ("open", "claimed", "blocked")]
    for k, b in briefs.items():
        if not k.startswith("HOS:"):
            out[k] = b
            continue
        steps = list(b.get("steps") or [])
        named = {x for st in steps for x in (st.get("job"), st.get("afterJob")) if x}
        extra = []
        for j in live:
            m = HOS_JOB.match(j.get("title") or "")
            if (j.get("film") == k or (m and "HOS:" + m.group(1) == k)) and j["id"] not in named:
                what = re.sub(r"\s*\([^)]*\)", "", HOS_JOB.sub("", j.get("title") or "")).strip(" :·")
                extra.append({"who": job_who(j), "what": what[:90], "job": j["id"], **({"kind": j["kind"]} if j.get("kind") else {})})
        if extra:
            at = next((i for i, st in enumerate(steps) if st.get("who") == "Ben" and not st.get("done")), len(steps))
            steps[at:at] = extra
            b = dict(b, steps=steps)
        out[k] = b
    return out


def route_steps(briefs: dict, alljobs: list[dict]) -> dict:
    """A step still to do shows the routed worker for its kind (or whoever holds its job); Ben's steps and done steps
    keep their name."""
    byid = {j["id"]: j for j in alljobs}
    out = {}
    for k, b in briefs.items():
        steps = []
        for st in b.get("steps") or []:
            if not st.get("done") and st.get("who") != "Ben":
                j = byid.get(st.get("job") or "")
                kind = st.get("kind") or (j or {}).get("kind") or kind_of_step(st.get("what", ""))
                who = job_who(j) if j and (j.get("status") in ("claimed", "done") or j.get("kind")) else routed_who(kind) if kind else ""
                if who:
                    st = dict(st, who=who, **({"kind": kind} if kind else {}))
            steps.append(st)
        out[k] = dict(b, steps=steps) if "steps" in b else b
    return out


def route_hos_stages(hos: dict) -> None:
    """HOS stages still to do with no owner: the routed worker for the stage's kind (done stages keep their doer)."""
    for f in hos.get("films", []):
        for key, st in (f.get("stages") or {}).items():
            if st.get("status") == "todo" and not st.get("owner") and key in HOS_STAGE_KIND:
                st["owner"] = routed_who(HOS_STAGE_KIND[key])


# ---- Ben's handoffs (Ben, 10 Oct: the card said "Waiting for you" while the For-you box said nothing to check) ----
# "Waiting for you" only when the cut really is in Ben's For-you box: the note has `you` set and the board has a Watch
# link for it. Any other step of Ben's still to come is a future handoff and reads "Ready for you" with its date.
READY = "Ready for you"


def ben_handoffs(briefs: dict, watch: dict) -> dict:
    out = {}
    for k, b in briefs.items():
        ready_now = bool(b.get("you")) and k in watch
        if not ready_now and any(st.get("who") == "Ben" and not st.get("done") for st in b.get("steps") or []):
            b = dict(b, steps=[dict(st, who=READY) if st.get("who") == "Ben" and not st.get("done") else st
                               for st in b["steps"]])
        out[k] = b
    return out


def chief_reviews(briefs: dict) -> dict:
    out = {}
    for k, b in briefs.items():
        b = {f: (chief_text(v) if f in ("line", "holdup", "limit", "timing", "you", "youShort") else v) for f, v in b.items()}
        steps = []
        for st in b.get("steps") or []:
            if st.get("who") == "Claude" and not st.get("done") and REVIEW_WORDS.search(st.get("what", "")):
                st = dict(st, who="Chief")
            steps.append(st)
        if "steps" in b:
            b["steps"] = steps
        out[k] = b
    return out


# ---- Watch links (Ben, 9 Oct 22:51): every cut waiting for Ben gets a button that opens it on his phone ----
# One link per film, best first:
#   1. an explicit `watch` {url, version, label} on the film: OWB status.json (top level), HOS PIPELINE.json (film),
#      or film_briefs.json (film note). Set it when the link is something the board can't find by itself.
#   2. the film's long upload in 00_Brand/Channel-Setup/social/UPLOADS.json (private/scheduled YouTube video), unless a
#      newer cut sits in the UAT folder (Ben has to watch the newest one).
#   3. the newest cut in iCloud Drive (OWB UAT/NNN_*.mp4; HOS UAT/NNN_*/... ), the *_PHONE.mp4 copy when there is one,
#      as a Files-app link (shareddocuments://...): the file is already in Ben's iCloud Drive, nothing is shared.
# Read where the files are (the Mini); elsewhere step 3 finds nothing and the board falls back to the folder note.
UPLOADS = ROOT / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json"
ICLOUD = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
UAT_DIRS = {"OWB": Path(os.environ.get("OWB_UAT_DIR", str(ICLOUD / "OWB UAT"))),
            "HOS": Path(os.environ.get("HOS_UAT_DIR", str(ICLOUD / "HOS UAT")))}
PHONE_ROOT = "/private/var/mobile/Library/Mobile Documents/com~apple~CloudDocs"
WATCH_OK = ("https://studio-kanban.vercel.app/api/watch?", "https://youtu.be/", "https://www.youtube.com/", "https://studio.youtube.com/", "https://www.icloud.com/")
VIDEO_EXT = (".mp4", ".mov", ".m4v")


def version_of(name: str) -> str:
    m = re.findall(r"_v(\d+[a-z]*)(?=[_.]|$)", Path(name).stem, flags=re.I)
    return "v" + m[-1].lower() if m else ""


def version_key(v: str) -> tuple:
    m = re.fullmatch(r"v(\d+)([a-z]*)", v or "")
    return (int(m.group(1)), m.group(2)) if m else (-1, "")


def explicit_watch(w) -> dict | None:
    if not isinstance(w, dict) or not str(w.get("url", "")).startswith(WATCH_OK):
        return None
    kind = "icloud" if "icloud.com" in w["url"] else "stream" if "/api/watch?" in w["url"] else "youtube"
    return {"url": w["url"], "version": str(w.get("version", "")), "label": str(w.get("label", "")), "kind": kind,
            "source": "set by hand"}


def newest_uat(ch: str, film: str) -> dict | None:
    root = UAT_DIRS[ch]
    if not root.is_dir():
        return None
    pat = re.compile(rf"^(hos_)?{film}[_\-]", re.I)
    files = []
    try:
        for p in root.iterdir():
            if p.is_file() and pat.match(p.name) and p.suffix.lower() in VIDEO_EXT:
                files.append(p)
            elif p.is_dir() and pat.match(p.name):
                files += [q for q in p.rglob("*") if q.is_file() and q.suffix.lower() in VIDEO_EXT
                          and not any(w in part.lower() for part in q.relative_to(p).parts[:-1] for w in ("short", "stills"))]
    except OSError:
        return None
    files = [p for p in files if version_of(p.name)]
    if not files:
        return None
    top = max(version_key(version_of(p.name)) for p in files)
    same = [p for p in files if version_key(version_of(p.name)) == top]
    phone = [p for p in same if "_phone" in p.stem.lower()]
    pick = max(phone or same, key=lambda p: p.stat().st_mtime)
    rel = pick.relative_to(ICLOUD) if ICLOUD in pick.parents else pick.relative_to(root.parent)
    streamed = stream_link(ch, film, pick, rel.as_posix())
    if streamed:
        return streamed
    from urllib.parse import quote
    return {"url": "shareddocuments://" + quote(f"{PHONE_ROOT}/{rel.as_posix()}"), "version": version_of(pick.name),
            "label": "", "kind": "files", "file": rel.as_posix(), "source": "iCloud Drive"}


# Streamed watch links (Ben, 15 Oct: "Clicking watch does not play the film"). Safari can't play a Files-app link, so a
# cut is uploaded once to the Studio Kanban's Blob store and the button opens /api/watch?v=<id> (plays in the browser;
# needs Ben's board code, never public in board.json). The register maps the cut's iCloud path (relative to CloudDocs) to
# its id: WATCH_REGISTER in the repo (committed by whoever uploads by hand) plus WATCH_LOCAL_REGISTER on the Mini (written
# by the auto-upload below). Auto-upload runs only when env WATCH_UPLOAD_KEY is set and the file is at most
# WATCH_AUTO_MAX bytes (the Hobby Blob allowance is 1 GB in total; bigger cuts need a phone proxy first, e.g. 720p
# ~1.3 Mbit/s, uploaded with scripts/watch_upload.mjs and added to the register). Otherwise the Files link stays.
SITE_URL = os.environ.get("BOARD_SITE_URL", "https://studio-kanban.vercel.app").rstrip("/")
WATCH_REGISTER = ROOT / "05_Analytics" / "kanban" / "watch_uploads.json"
WATCH_LOCAL_REGISTER = Path(os.environ.get("WATCH_LOCAL_REGISTER", str(Path.home() / ".config" / "studio-kanban" / "watch_uploads.json")))
WATCH_AUTO_MAX = int(os.environ.get("WATCH_AUTO_MAX", str(120 * 1024 * 1024)))


def watch_id(ch: str, film: str, version: str) -> str:
    return re.sub(r"[^a-z0-9_-]", "-", f"{ch}-{film}-{version or 'cut'}".lower())


def watch_register() -> dict:
    reg = {}
    for p in (WATCH_REGISTER, WATCH_LOCAL_REGISTER):
        try:
            reg.update((json.loads(p.read_text()) or {}).get("files", {}))
        except (OSError, ValueError, AttributeError):
            pass
    return reg


def auto_upload(wid: str, path: Path, rel: str) -> bool:
    key = os.environ.get("WATCH_UPLOAD_KEY", "")
    try:
        if not key or path.stat().st_size > WATCH_AUTO_MAX:
            return False
    except OSError:
        return False
    import subprocess
    try:
        r = subprocess.run(["node", str(ROOT / "scripts" / "watch_upload.mjs"), wid, str(path)], capture_output=True,
                           text=True, timeout=900, cwd=str(ROOT / "05_Analytics" / "kanban" / "board_site"))
    except (OSError, subprocess.TimeoutExpired):
        return False
    if r.returncode != 0:
        print(f"watch upload {wid} failed: {r.stderr.strip()[-200:]}", file=sys.stderr)
        return False
    try:
        cur = json.loads(WATCH_LOCAL_REGISTER.read_text())
    except (OSError, ValueError):
        cur = {}
    cur.setdefault("files", {})[rel] = wid
    WATCH_LOCAL_REGISTER.parent.mkdir(parents=True, exist_ok=True)
    WATCH_LOCAL_REGISTER.write_text(json.dumps(cur, indent=2) + "\n")
    return True


def stream_link(ch: str, film: str, pick: Path, rel: str) -> dict | None:
    version = version_of(pick.name)
    wid = watch_register().get(rel)
    if not wid:
        wid = watch_id(ch, film, version)
        if not auto_upload(wid, pick, rel):
            return None
    return {"url": f"{SITE_URL}/api/watch?v={wid}", "version": version, "label": "", "kind": "stream", "file": rel,
            "source": "Studio Kanban (plays in the browser)"}


def release_record(film: str, root: Path | None = None) -> dict | None:
    """Read actual upload receipts; a manifest, dry run or due date is not an upload."""
    root = root or ROOT
    records = []
    for path in sorted((root / "02_Video-Projects").glob(f"{film}_*/11_Upload-Package/PACKAGE_UPLOAD_RESULT*.json")):
        try:
            doc = json.loads(path.read_text())
            upload = doc.get("upload") or {}
            if doc.get("ok") is not True or doc.get("dryRun") is not False or not upload.get("platformPostId"):
                continue
            response = upload.get("responseSummary") or {}
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except ValueError:
                    response = {}
            publish_at = upload.get("scheduledFor") or response.get("publishAt") or ""
            state = "live" if response.get("privacyStatus") == "public" else "scheduled" if upload.get("scheduledOnPlatform") is True and publish_at else "uploaded"
            records.append({"state": state, "videoId": upload["platformPostId"], "publishAt": publish_at,
                            "source": str(path.relative_to(root))})
        except (OSError, ValueError, TypeError, AttributeError):
            continue
    return records[-1] if records else None


def uploaded_long(film: str) -> dict | None:
    try:
        vids = json.loads(UPLOADS.read_text()).get("videos", {})
    except (OSError, ValueError):
        return None
    hits = [(vid, v) for vid, v in vids.items() if v.get("kind") == "long"
            and re.match(rf"02_Video-Projects/{film}_", str(v.get("packageDir") or v.get("file") or ""))]
    if not hits:
        return None
    vid, v = hits[-1]
    return {"url": f"https://youtu.be/{vid}", "alt": f"https://studio.youtube.com/video/{vid}/edit",
            "version": version_of(str(v.get("file", ""))), "label": "", "kind": "youtube", "source": "YouTube upload (private until it airs)"}


def watch_links(hos: dict, owb: list[dict], briefs: dict) -> dict:
    """{"OWB:026": {url, version, label, kind, source[, alt, file]}} for every film with something to watch."""
    out = {}
    films = [("OWB", str(f.get("film", "")), f.get("watch")) for f in owb] + \
            [("HOS", str(f.get("id", "")), f.get("watch")) for f in hos.get("films", [])]
    for ch, film, own in films:
        if not re.fullmatch(r"\d{3}", film):
            continue
        key = f"{ch}:{film}"
        w = explicit_watch(own) or explicit_watch((briefs.get(key) or {}).get("watch"))
        if not w:
            yt = uploaded_long(film) if ch == "OWB" else None
            uat = newest_uat(ch, film)
            if yt and uat and version_key(uat["version"]) > version_key(yt["version"]):
                yt = None  # a newer cut than the upload is waiting: that's the one to watch
            w = yt or uat
        wf = (briefs.get(key) or {}).get("watchFrom")  # e.g. "v05": no link until that version's phone copy exists
        if w and wf and w.get("version") and version_key(w["version"]) < version_key(str(wf)):
            w = None
        if w:
            if not w["label"]:
                w["label"] = f"Watch {w['version']}" if w.get("version") else "Watch it"
            out[key] = w
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", type=Path, nargs="?")
    ap.add_argument("--hos", type=Path, required=True, help="history-of-science checkout on main")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--db-out", type=Path, default=None, help="write hos.json and owb.json store documents here")
    ap.add_argument("--chief", default="", help="acting Chief from the relay's last thread line, e.g. Cursor (into owb.json)")
    ap.add_argument("--chief-since", default="", help="ISO time that agent became Chief")
    ap.add_argument("--chief-next", default="", help="comma list: next in line")
    ap.add_argument("--chief-note", default="", help="one short line, e.g. Grok Bot out of credit")
    a = ap.parse_args(argv)
    hos = json.loads((a.hos / "00_Brand/Channel-Setup/PIPELINE.json").read_text())
    if not isinstance(hos.get("films"), list):
        raise SystemExit("PIPELINE.json has no films list; not touching the page")
    owb = [json.loads(p.read_text()) for p in sorted((ROOT / "02_Video-Projects").glob("*/status.json"))]
    for film in owb:
        receipt = release_record(str(film.get("film", "")))
        if receipt:
            film["release"] = receipt
    if a.db_out:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        a.db_out.mkdir(parents=True, exist_ok=True)
        add_since_hos(a.hos, hos)
        route_hos_stages(hos)
        add_since_owb(owb)
        (a.db_out / "hos.json").write_text(json.dumps({"updatedAt": now, "pipeline": hos}, ensure_ascii=False))
        q = ROOT / "jobs" / "queue.json"
        alljobs = json.loads(q.read_text())["jobs"] if q.exists() else []
        learn_estimates(alljobs)
        focus = json.loads(q.read_text()).get("focus", []) if q.exists() else []
        ro = run_order(alljobs, focus)
        gate = gates(alljobs)
        typ = typical_minutes(alljobs)
        live = [dict({k: j.get(k, "") for k in ("id", "title", "needs", "status", "by", "eta", "eta_min", "repo", "film", "stage", "after", "ref", "result", "urgent", "for", "kind", "model")},
                     taskKeys=j.get("taskKeys", []),
                     line=ro["pos"].get(j["id"], {}).get("line", line_of(j)), pos=ro["pos"].get(j["id"], {}).get("pos"),
                     waitsFor=ro["pos"].get(j["id"], {}).get("waitsFor", ""), notBefore=gate.get(j["id"], ""),
                     gateOnly=bool(re.search(r"\bdate gate\b", j.get("title", ""), re.I)),
                     last=(j.get("history") or [{}])[-1],  # who touched it last, when, and their note (the board shows it)
                     claimedAt=next((h["at"] for h in reversed(j.get("history") or []) if h["what"].startswith("claimed")), ""),
                     addedAt=(j.get("history") or [{}])[0].get("at", ""),
                     workStart=work_start(j), progress=job_progress(j),
                     estMin=est_minutes(j), typMin=typ.get(kind_key(j), typ["_default"]), kindKey=kind_key(j),
                     watch=makes_video(j), routedTo=routed_who(j.get("kind") or "", j.get("model") or ""))
                for j in alljobs if j["status"] in ("open", "claimed", "blocked")]
        lanes = lanes_info(alljobs)
        hb = mini_heartbeat()
        if hb:
            lanes.setdefault("mini", {})["heartbeat"] = hb
        for f in owb:
            if isinstance(f.get("next"), str):
                f["next"] = chief_text(f["next"])
        recent = sorted(({"id": j["id"], "title": j.get("title", ""), "film": j.get("film", ""), "by": j.get("by", ""),
                          "at": next((h["at"] for h in reversed(j.get("history") or []) if str(h.get("what", "")).startswith("done")), "")}
                         for j in alljobs if j.get("status") == "done"), key=lambda r: r["at"], reverse=True)[:5]
        doc = {"updatedAt": now, "films": owb, "jobs": live, "lanes": lanes, "focus": focus, "runOrder": ro["lines"], "recent": recent,
               "jobStates": {j["id"]: {"status": j.get("status", ""), "by": j.get("by", ""),
                                      "at": (j.get("history") or [{}])[-1].get("at", "")} for j in alljobs},
               "estimates": {(", ".join(EST[k][0][:2]) if k >= 0 else "other"): m for k, m in sorted(LEARNED.items())},
               "routing": routing_doc(), "typical": typ, "day": day_numbers(alljobs), "week": week_numbers(alljobs),
               "done": completed_jobs(alljobs)}
        from video_progress import progress_document
        doc["videoProgress"] = progress_document(ROOT, a.hos, alljobs, a.db_out)
        if a.chief:
            doc["chief"] = {"name": a.chief, "since": a.chief_since, "note": a.chief_note,
                            "next": [x.strip() for x in a.chief_next.split(",") if x.strip()]}
        (a.db_out / "owb.json").write_text(json.dumps(doc, ensure_ascii=False))
        # board/credits (Ben, 8 Oct): the AI spend month from scripts/ai_spend.py, plus HOS's own credit checks
        sys.path.insert(0, str(ROOT / "scripts"))
        import ai_spend
        credits = ai_spend.build_doc(ai_spend.load())
        credits["hosChecks"] = hos.get("credits", [])
        credits["miniWork"] = mini_work(alljobs, (credits.get("pools", {}).get("cursor", {}) or {}).get("since")
                                        or json.loads(ai_spend.PLANS.read_text()).get("poolStarts", {}).get("cursor", "2026-10-08"))
        (a.db_out / "credits.json").write_text(json.dumps(credits, ensure_ascii=False))
        briefs = load_briefs()
        links = {k: v for k, v in json.loads(BRIEFS.read_text()).items() if k in ("uatFolderUrl", "extraWatch")} if BRIEFS.exists() else {}
        watch = watch_links(hos, owb, briefs)
        briefs = ben_handoffs(chief_reviews(route_steps(hos_job_steps(briefs, alljobs), alljobs)), watch)
        (a.db_out / "briefs.json").write_text(json.dumps({"updatedAt": now, "films": briefs, "watch": watch, **links}, ensure_ascii=False))
        print(f"store documents: {a.db_out}/briefs.json ({len(briefs)} film notes, {len(watch)} watch links), {a.db_out}/hos.json ({len(hos['films'])} HOS films), {a.db_out}/owb.json ({len(owb)} OWB films), "
              f"{a.db_out}/credits.json ({credits['lines']} spend lines since {credits['period'].get('start')})")
        if not a.page:
            return 0
    if not a.page:
        raise SystemExit("give a page file, --db-out, or both")
    old = a.page.read_text()
    new = rebuild(old, hos, owb)
    (a.out or a.page).write_text(new)
    print("unchanged" if new == old else f"updated: HOS {hos.get('updated')} ({len(hos['films'])} films), OWB {len(owb)} films")
    return 0


if __name__ == "__main__":
    sys.exit(main())
