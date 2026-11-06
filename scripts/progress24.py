#!/usr/bin/env python3
"""Last-24-hours progress for the Studio home page (Ben, 4 Nov 2026: "a section on the homepage that tells us how many
jobs have progressed in the last 24 hours and what overarching task has been complete or how many percentages moved
forward").

board_publish.py calls `section(history_path, board, at)` on every publish (the Mini, every 5 min). It:
  - records each video's completed-milestone count (same rule as the page: done/skip/passed and not awaiting approval,
    out of 9) in a rolling history file, one sample per 30 min, kept 48 h;
  - compares now with the sample nearest 24 h ago (or the oldest, saying how many hours that covers);
  - counts jobs finished in the window from board.owb.done, by agent, and groups them by film;
  - lists each film's finished + in-progress jobs so Overview can show what actually happened (Ben, 6 Nov 2026).
board.json gets `progress24h`; studio_app.js draws it on Overview. Reads only; never fails the publish.
"""
import datetime as dt, json, re
from pathlib import Path

import channels

DONE_STATES = ("done", "skip", "passed")
OPEN_STATUSES = ("claimed", "blocked")  # in progress / held on a film — not merely queued
TOTAL = 9
SAMPLE_EVERY = dt.timedelta(minutes=30)
KEEP = dt.timedelta(hours=48)
WINDOW = dt.timedelta(hours=24)
FILM = channels.key_re()
# Bare episode numbers in titles ("Chief: resolve 033 picture orphan-review").
BARE_NO = re.compile(r"(?<![A-Za-z0-9:])(\d{3})\b")
STAGE_LABELS = {
    "topic": "topic", "script": "script", "sources": "fact checks", "vo": "voice",
    "shots": "shot plan", "picture": "picture", "edit": "edit", "thumbs": "packaging", "qa": "Chief QA",
}
# Ignore these when matching a job title against a film title (too generic).
_STOP = {
    "a", "an", "the", "and", "or", "of", "on", "in", "to", "for", "with", "what", "when", "why",
    "how", "would", "happen", "happens", "if", "you", "your", "has", "have", "is", "are", "does",
    "did", "could", "should", "short", "shorts", "long", "v01", "v02", "v03", "v04", "v05",
    "v06", "v07", "v08", "v09", "v10", "v11", "v12", "work", "pass", "review", "chief", "resolve",
}


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


def video_stages(board: dict) -> dict:
    """{video key: stage_id} — the film's current production stage, when known."""
    out = {}
    for v in ((board.get("tracker") or {}).get("videos") or []):
        key = v.get("key")
        if not key:
            continue
        prod = v.get("production") or {}
        ms = {m.get("id"): m for m in (prod.get("milestones") or []) if m.get("id")}
        for sid in prod.get("activeStages") or []:
            m = ms.get(sid)
            if m and not complete(m):
                out[key] = sid
                break
        if key in out:
            continue
        for sid in ("topic", "script", "sources", "vo", "shots", "picture", "edit", "thumbs", "qa"):
            m = ms.get(sid)
            if not m or complete(m):
                continue
            state = m.get("displayState") or m.get("state") or ""
            if state in ("doing", "in_progress", "blocked", "review") or m.get("awaitingApproval"):
                out[key] = sid
                break
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


def _words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]{3,}", (text or "").lower()) if w not in _STOP}


def film_of(j: dict, titles: dict | None = None) -> str:
    """Attribute a job to a film from its film field, or from the title when film is empty."""
    f = str(j.get("film") or "")
    if channels.strict_key_re().fullmatch(f):
        return f
    title = j.get("title") or ""
    m = FILM.search(title)
    if m:
        return m.group(1).upper() + ":" + m.group(2)
    # Leading episode number ("032 Titan Short v11").
    m = re.match(r"^\s*(\d{3})\b", title)
    if m:
        return ("HOS:" if j.get("repo") == "hos" else "OWB:") + m.group(1)
    # Mid-title episode number ("Chief: resolve 033 picture orphan-review").
    nums = BARE_NO.findall(title)
    if len(nums) == 1:
        return ("HOS:" if j.get("repo") == "hos" else "OWB:") + nums[0]
    # Title names the film without a number ("Titan Short v11" → OWB:032).
    if titles:
        tw = _words(title)
        if tw:
            best, best_n = "", 0
            for key, name in titles.items():
                hits = tw & _words(name)
                if len(hits) > best_n:
                    best, best_n = key, len(hits)
            if best_n >= 1 and best:
                return best
    return ""


def jobs_done(board: dict, at: dt.datetime) -> list:
    seen, out = set(), []
    for j in ((board.get("owb") or {}).get("done") or []):
        t = _t(j.get("at"))
        if t and at - t <= WINDOW and j.get("id") not in seen:
            seen.add(j.get("id")); out.append(j)
    return out


def jobs_open(board: dict) -> list:
    """Claimed/blocked jobs still on a film (multi-day work that never hit done yet)."""
    seen, out = set(), []
    for j in ((board.get("owb") or {}).get("jobs") or []):
        if j.get("status") in OPEN_STATUSES and j.get("id") and j["id"] not in seen:
            seen.add(j["id"]); out.append(j)
    return out


def _job_item(j: dict, status: str) -> dict:
    item = {
        "id": j.get("id") or "",
        "title": str(j.get("title") or "")[:120],
        "status": status,
        "by": str(j.get("by") or "") or None,
        "stage": str(j.get("stage") or "") or None,
    }
    prog = j.get("progress") or {}
    if isinstance(prog, dict) and prog.get("of"):
        try:
            item["progress"] = {"step": int(prog.get("step") or 0), "of": int(prog["of"])}
        except (TypeError, ValueError):
            pass
    return {k: v for k, v in item.items() if v is not None}


def _status_line(moved_row: dict | None, pct: int | None, stage_id: str | None) -> str:
    if moved_row and moved_row.get("milestones", 0) > 0:
        return f"{moved_row['from']}% → {moved_row['to']}%"
    if moved_row and moved_row.get("milestones", 0) < 0:
        return f"↺ reopened · {moved_row['from']}% → {moved_row['to']}%"
    stage = STAGE_LABELS.get(stage_id or "", stage_id or "")
    if stage and pct is not None:
        return f"worked on, no stage closed — still in {stage} ({pct}%)"
    if stage:
        return f"worked on, no stage closed — still in {stage}"
    if pct is not None:
        return f"worked on, no stage closed — still at {pct}%"
    return "worked on, no stage closed"


def summarise(history: list, at: dt.datetime, counts: dict, done: list,
              open_jobs: list | None = None, stages: dict | None = None) -> dict:
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
    moved_by = {m["key"]: m for m in moved}
    titles = {k: c[1] for k, c in counts.items()}
    stages = stages or {}

    by_agent, by_film, studio_items = {}, {}, []
    for j in done:
        a = str(j.get("by") or "other")
        by_agent[a] = by_agent.get(a, 0) + 1
        f = film_of(j, titles)
        item = _job_item(j, "done")
        if f:
            g = by_film.setdefault(f, {"film": f, "title": titles.get(f, f), "jobs": 0, "last": "", "items": []})
            g["jobs"] += 1
            if not g["last"]:
                g["last"] = str(j.get("title") or "")[:90]
            g["items"].append(item)
        else:
            studio_items.append(item)

    # In-progress jobs on a film stay visible even when the parent never hits done.
    seen_ids = {it["id"] for g in by_film.values() for it in g["items"]} | {it["id"] for it in studio_items}
    for j in open_jobs or []:
        if j.get("id") in seen_ids:
            continue
        f = film_of(j, titles)
        item = _job_item(j, j.get("status") or "claimed")
        if f:
            g = by_film.setdefault(f, {"film": f, "title": titles.get(f, f), "jobs": 0, "last": "", "items": []})
            if not g["last"]:
                g["last"] = str(j.get("title") or "")[:90]
            g["items"].append(item)
            seen_ids.add(item["id"])
        # Studio-wide open jobs stay on the Agents/Machines cards; only finished ones fold here.

    # Films that moved a stage but had no attributed jobs still get a card.
    for m in moved:
        g = by_film.setdefault(m["key"], {"film": m["key"], "title": m["title"], "jobs": 0, "last": "", "items": []})
        if g["title"] in (m["key"], "") or not g["title"]:
            g["title"] = m["title"]

    films = []
    for f, g in by_film.items():
        now_done, title = counts.get(f, [None, g["title"]])
        pct = round(now_done / TOTAL * 100) if now_done is not None else None
        mv = moved_by.get(f)
        stage_id = stages.get(f)
        card = {
            "film": f,
            "title": title or g["title"],
            "jobs": g["jobs"],
            "last": g["last"],
            "items": g["items"],
            "status": _status_line(mv, pct, stage_id),
            "closed": bool(mv and mv.get("milestones", 0) > 0),
        }
        if pct is not None:
            card["pct"] = pct
        if stage_id:
            card["stage"] = stage_id
            card["stageLabel"] = STAGE_LABELS.get(stage_id, stage_id)
        if mv:
            card["from"] = mv["from"]
            card["to"] = mv["to"]
            card["milestones"] = mv["milestones"]
        films.append(card)

    # Moved films first (by milestones), then films with the most finished jobs, then key.
    films.sort(key=lambda g: (
        0 if g.get("closed") else 1,
        -(g.get("milestones") or 0),
        -g["jobs"],
        -len(g.get("items") or []),
        g["film"],
    ))
    return {
        "hours": span_h, "since": base["at"] if base else "",
        "jobsDone": len(done), "byAgent": dict(sorted(by_agent.items(), key=lambda kv: -kv[1])),
        "milestones": sum(m["milestones"] for m in moved if m["milestones"] > 0),
        "moved": moved[:10], "films": films,
        "studio": studio_items,
        "otherJobs": len(studio_items),
        "videoJobs": sum(g["jobs"] for g in films),
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
    return summarise(
        comparable, at, counts, jobs_done(board, at),
        open_jobs=jobs_open(board), stages=video_stages(board),
    )
