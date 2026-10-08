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
    if bad:
        raise SystemExit(f"film_briefs.json: keys must be HOS:NNN or OWB:NNN, not {bad}")
    return films


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
        live = [dict({k: j.get(k, "") for k in ("id", "title", "needs", "status", "by", "eta", "film", "stage", "after", "ref", "result")},
                     last=(j.get("history") or [{}])[-1],  # who touched it last, when, and their note (the board shows it)
                     claimedAt=next((h["at"] for h in reversed(j.get("history") or []) if h["what"].startswith("claimed")), ""),
                     addedAt=(j.get("history") or [{}])[0].get("at", ""),
                     estMin=est_minutes(j), watch=makes_video(j))
                for j in alljobs if j["status"] in ("open", "claimed", "blocked")]
        lanes = lanes_info(alljobs)
        hb = mini_heartbeat()
        if hb:
            lanes.setdefault("mini", {})["heartbeat"] = hb
        doc = {"updatedAt": now, "films": owb, "jobs": live, "lanes": lanes,
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
        (a.db_out / "credits.json").write_text(json.dumps(credits, ensure_ascii=False))
        briefs = load_briefs()
        (a.db_out / "briefs.json").write_text(json.dumps({"updatedAt": now, "films": briefs}, ensure_ascii=False))
        print(f"store documents: {a.db_out}/briefs.json ({len(briefs)} film notes), {a.db_out}/hos.json ({len(hos['films'])} HOS films), {a.db_out}/owb.json ({len(owb)} OWB films), "
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
