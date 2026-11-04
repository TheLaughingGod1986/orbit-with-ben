#!/usr/bin/env python3
"""Last-24-hours progress for the Studio home page (Ben, 4 Nov 2026: "a section on the homepage that tells us how many
jobs have progressed in the last 24 hours and what overarching task has been complete or how many percentages moved
forward").

board_publish.py calls `section(history_path, board, at)` on every publish (the Mini, every 5 min). It:
  - records each video's completed-milestone count (same rule as the page: done/skip/passed and not awaiting approval,
    out of 9) in a rolling history file, one sample per 30 min, kept 48 h;
  - compares now with the sample nearest 24 h ago (or the oldest, saying how many hours that covers);
  - counts jobs finished in the window from board.owb.done, by agent, and groups them by film.
board.json gets `progress24h`; studio_app.js draws it on Overview. Reads only; never fails the publish.
"""
import datetime as dt, json, re
from pathlib import Path

DONE_STATES = ("done", "skip", "passed")
TOTAL = 9
SAMPLE_EVERY = dt.timedelta(minutes=30)
KEEP = dt.timedelta(hours=48)
WINDOW = dt.timedelta(hours=24)
FILM = re.compile(r"\b(HOS|OWB)\s*[:·-]?\s*(\d{3})\b", re.I)


def _t(s):
    try:
        return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def _iso(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def complete(m: dict) -> bool:
    return (m.get("displayState") or m.get("state")) in DONE_STATES and not m.get("awaitingApproval")


def video_counts(board: dict) -> dict:
    """{video key: [milestones done, title]} for every tracker video that has milestones."""
    out = {}
    for v in ((board.get("tracker") or {}).get("videos") or []):
        ms = (v.get("production") or {}).get("milestones") or []
        if v.get("key") and ms:
            out[v["key"]] = [sum(1 for m in ms if complete(m)), v.get("title") or v["key"]]
    return out


def record(history: list, at: dt.datetime, counts: dict, basis=None) -> list:
    """Add a sample if the newest is 30+ min old; drop samples older than 48 h."""
    hist = [h for h in history if _t(h.get("at")) and at - _t(h["at"]) <= KEEP]
    if not hist or hist[-1].get("basis") != basis or at - _t(hist[-1]["at"]) >= SAMPLE_EVERY:
        sample = {"at": _iso(at), "counts": {k: c[0] for k, c in counts.items()}}
        if basis is not None:
            sample["basis"] = basis
        hist.append(sample)
    return hist


def baseline(history: list, at: dt.datetime):
    """The newest sample at least 24 h old, else the oldest one."""
    old = [h for h in history if at - _t(h["at"]) >= WINDOW]
    return old[-1] if old else (history[0] if history else None)


def film_of(j: dict) -> str:
    f = str(j.get("film") or "")
    if re.fullmatch(r"(HOS|OWB):\d{3}", f):
        return f
    m = FILM.search(j.get("title") or "")
    if m:
        return m.group(1).upper() + ":" + m.group(2)
    m = re.match(r"^\s*(\d{3})\b", j.get("title") or "")
    if m:
        return ("HOS:" if j.get("repo") == "hos" else "OWB:") + m.group(1)
    return ""


def jobs_done(board: dict, at: dt.datetime) -> list:
    seen, out = set(), []
    for j in ((board.get("owb") or {}).get("done") or []):
        t = _t(j.get("at"))
        if t and at - t <= WINDOW and j.get("id") not in seen:
            seen.add(j.get("id")); out.append(j)
    return out


def summarise(history: list, at: dt.datetime, counts: dict, done: list) -> dict:
    base = baseline(history, at)
    then = (base or {}).get("counts") or {}
    span_h = round((at - _t(base["at"])).total_seconds() / 3600, 1) if base else 0
    moved = []
    for key, (now_done, title) in counts.items():
        before = then.get(key)
        if before is not None and now_done != before:
            moved.append({"key": key, "title": title, "from": round(before / TOTAL * 100), "to": round(now_done / TOTAL * 100),
                          "milestones": now_done - before})
    moved.sort(key=lambda m: (-m["milestones"], m["key"]))
    by_agent, by_film = {}, {}
    for j in done:
        a = str(j.get("by") or "other")
        by_agent[a] = by_agent.get(a, 0) + 1
        f = film_of(j)
        if f:
            g = by_film.setdefault(f, {"film": f, "title": counts.get(f, [0, f])[1], "jobs": 0, "last": ""})
            g["jobs"] += 1
            if not g["last"]:
                g["last"] = str(j.get("title") or "")[:90]
    films = sorted(by_film.values(), key=lambda g: (-g["jobs"], g["film"]))[:8]
    return {
        "hours": span_h, "since": base["at"] if base else "",
        "jobsDone": len(done), "byAgent": dict(sorted(by_agent.items(), key=lambda kv: -kv[1])),
        "milestones": sum(m["milestones"] for m in moved if m["milestones"] > 0),
        "moved": moved[:10], "films": films,
        "otherJobs": len(done) - sum(g["jobs"] for g in by_film.values()),
    }


def section(history_path: Path, board: dict, at: dt.datetime) -> dict:
    try:
        history = json.loads(Path(history_path).read_text())
    except Exception:
        history = []
    counts = video_counts(board)
    # A publisher/schema correction is not newly finished production. Retain
    # older samples, but compare only samples with the same counting basis.
    schemas = sorted({p.get("milestoneSchema") for v in ((board.get("tracker") or {}).get("videos") or [])
                      if isinstance(p := v.get("production"), dict) and isinstance(p.get("milestoneSchema"), str)})
    basis = "|".join(schemas) or None
    history = record(history, at, counts, basis)
    try:
        Path(history_path).write_text(json.dumps(history))
    except Exception:
        pass
    comparable = [h for h in history if h.get("basis") == basis]
    return summarise(comparable, at, counts, jobs_done(board, at))
