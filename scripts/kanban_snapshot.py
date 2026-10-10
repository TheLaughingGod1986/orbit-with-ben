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


def est_minutes(j: dict) -> int:
    k = kind_of(j)
    if k in LEARNED:
        return max(5, LEARNED[k])
    return EST[k][1] if k >= 0 else 25


def makes_video(j: dict) -> bool:
    """A job whose result Ben can watch in OWB UAT (a cut), as opposed to sheets, packages or text."""
    t = (j.get("title") or "").lower()
    return j.get("stage") == "edit" and any(w in t for w in ("rough", "cut", "picture", "assemble"))


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
WATCH_OK = ("https://youtu.be/", "https://www.youtube.com/", "https://studio.youtube.com/", "https://www.icloud.com/")
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
    kind = "icloud" if "icloud.com" in w["url"] else "youtube"
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
    from urllib.parse import quote
    return {"url": "shareddocuments://" + quote(f"{PHONE_ROOT}/{rel.as_posix()}"), "version": version_of(pick.name),
            "label": "", "kind": "files", "file": rel.as_posix(), "source": "iCloud Drive"}


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
    if a.db_out:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        a.db_out.mkdir(parents=True, exist_ok=True)
        add_since_hos(a.hos, hos)
        add_since_owb(owb)
        (a.db_out / "hos.json").write_text(json.dumps({"updatedAt": now, "pipeline": hos}, ensure_ascii=False))
        q = ROOT / "jobs" / "queue.json"
        alljobs = json.loads(q.read_text())["jobs"] if q.exists() else []
        learn_estimates(alljobs)
        focus = json.loads(q.read_text()).get("focus", []) if q.exists() else []
        ro = run_order(alljobs, focus)
        live = [dict({k: j.get(k, "") for k in ("id", "title", "needs", "status", "by", "eta", "eta_min", "film", "stage", "after", "ref", "result", "urgent", "for")},
                     line=ro["pos"].get(j["id"], {}).get("line", line_of(j)), pos=ro["pos"].get(j["id"], {}).get("pos"),
                     waitsFor=ro["pos"].get(j["id"], {}).get("waitsFor", ""),
                     last=(j.get("history") or [{}])[-1],  # who touched it last, when, and their note (the board shows it)
                     claimedAt=next((h["at"] for h in reversed(j.get("history") or []) if h["what"].startswith("claimed")), ""),
                     addedAt=(j.get("history") or [{}])[0].get("at", ""),
                     estMin=est_minutes(j), watch=makes_video(j))
                for j in alljobs if j["status"] in ("open", "claimed", "blocked")]
        lanes = lanes_info(alljobs)
        hb = mini_heartbeat()
        if hb:
            lanes.setdefault("mini", {})["heartbeat"] = hb
        for f in owb:
            if isinstance(f.get("next"), str):
                f["next"] = chief_text(f["next"])
        doc = {"updatedAt": now, "films": owb, "jobs": live, "lanes": lanes, "focus": focus, "runOrder": ro["lines"],
               "estimates": {(", ".join(EST[k][0][:2]) if k >= 0 else "other"): m for k, m in sorted(LEARNED.items())}}
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
        links = {k: v for k, v in json.loads(BRIEFS.read_text()).items() if k == "uatFolderUrl"} if BRIEFS.exists() else {}
        watch = watch_links(hos, owb, briefs)
        briefs = ben_handoffs(chief_reviews(briefs), watch)
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
