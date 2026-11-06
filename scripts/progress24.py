#!/usr/bin/env python3
"""Last-24-hours progress for the Studio home page (Ben, 4 Nov 2026: "a section on the homepage that tells us how many
jobs have progressed in the last 24 hours and what overarching task has been complete or how many percentages moved
forward").

board_publish.py calls `section(history_path, board, at)` on every publish (the Mini, every 5 min). It:
  - records each video's completed-milestone count (same rule as the page: done/skip/passed and not awaiting approval,
    out of 9) in a rolling history file, one sample per 30 min, kept 48 h;
  - compares now with the sample nearest 24 h ago (or the oldest, saying how many hours that covers);
  - counts jobs finished in the window from board.owb.done, by agent, and groups them by film;
  - lists each film's remaining-to-go-live work plus today/yesterday finished jobs (Ben, 6 Nov 2026), so the %
    matches the checklist instead of looking finished while a stage is still open.
board.json gets `progress24h`; studio_app.js draws it on Overview. Reads only; never fails the publish.
"""
import datetime as dt, json, re
from pathlib import Path
from zoneinfo import ZoneInfo

import channels

DONE_STATES = ("done", "skip", "passed")
# Remaining work on a film: queued, in progress, or held (Ben, 6 Nov 2026).
OPEN_STATUSES = ("open", "claimed", "blocked")
TOTAL = 9
SAMPLE_EVERY = dt.timedelta(minutes=30)
KEEP = dt.timedelta(hours=48)
WINDOW = dt.timedelta(hours=24)
LONDON = ZoneInfo("Europe/London")
FILM = channels.key_re()
# Bare episode numbers in titles ("Chief: resolve 033 picture orphan-review").
BARE_NO = re.compile(r"(?<![A-Za-z0-9:])(\d{3})\b")
STAGE_ORDER = ("topic", "script", "sources", "vo", "shots", "picture", "edit", "thumbs", "qa", "upload")
STAGE_LABELS = {
    "topic": "topic", "script": "script", "sources": "fact checks", "vo": "voice",
    "shots": "shot plan", "picture": "picture", "edit": "edit", "thumbs": "packaging",
    "qa": "Chief QA", "upload": "upload",
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


def _london_date(t: dt.datetime):
    return t.astimezone(LONDON).date()


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
        for sid in STAGE_ORDER:
            m = ms.get(sid)
            if not m or complete(m):
                continue
            state = m.get("displayState") or m.get("state") or ""
            if state in ("doing", "in_progress", "blocked", "review") or m.get("awaitingApproval"):
                out[key] = sid
                break
    return out


def video_milestones(board: dict) -> dict:
    """{video key: milestone list} from tracker production — used for leftover stage rows."""
    out = {}
    for v in ((board.get("tracker") or {}).get("videos") or []):
        key = v.get("key")
        ms = (v.get("production") or {}).get("milestones") or []
        if key and ms:
            out[key] = ms
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


def _bare_film_key(num: str, j: dict, titles: dict | None) -> str:
    """Map a bare episode number to a known film key only — never invent OWB:180 from a PR number."""
    if not titles or not num:
        return ""
    preferred = ("HOS:" if j.get("repo") == "hos" else "OWB:") + num
    alt = ("OWB:" if preferred.startswith("HOS:") else "HOS:") + num
    if preferred in titles:
        return preferred
    if alt in titles:
        return alt
    return ""


def film_of(j: dict, titles: dict | None = None) -> str:
    """Attribute a job to a film from its film field, or from the title when film is empty."""
    f = str(j.get("film") or "")
    if channels.strict_key_re().fullmatch(f):
        return f
    # Bare episode number in the film field ("032") — only when that film is known.
    if re.fullmatch(r"\d{3}", f):
        key = _bare_film_key(f, j, titles)
        if key:
            return key
    title = j.get("title") or ""
    m = FILM.search(title)
    if m:
        return m.group(1).upper() + ":" + m.group(2)
    # Leading episode number ("032 Titan Short v11") — only if that film is known.
    m = re.match(r"^\s*(\d{3})\b", title)
    if m:
        key = _bare_film_key(m.group(1), j, titles)
        if key:
            return key
    # Mid-title episode number ("Chief: resolve 033 picture orphan-review") — known films only.
    nums = BARE_NO.findall(title)
    if len(nums) == 1:
        key = _bare_film_key(nums[0], j, titles)
        if key:
            return key
    # Explicit taskKeys win over fuzzy title matching.
    for k in j.get("taskKeys") or []:
        if channels.strict_key_re().fullmatch(str(k)):
            return str(k)
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


def jobs_done_all(board: dict) -> list:
    """Every finished job the board still carries (for today / yesterday / earlier split)."""
    seen, out = set(), []
    for j in ((board.get("owb") or {}).get("done") or []):
        if j.get("id") and j["id"] not in seen:
            seen.add(j["id"]); out.append(j)
    return out


def jobs_open(board: dict) -> list:
    """Open / claimed / blocked jobs still on a film (remaining work to go live)."""
    seen, out = set(), []
    for j in ((board.get("owb") or {}).get("jobs") or []):
        if j.get("status") in OPEN_STATUSES and j.get("id") and j["id"] not in seen:
            seen.add(j["id"]); out.append(j)
    return out


def done_when(j: dict, at: dt.datetime):
    """'today' / 'yesterday' on the Europe/London calendar, else None (older or unknown)."""
    t = _t(j.get("at"))
    if not t:
        return None
    day, today = _london_date(t), _london_date(at)
    if day == today:
        return "today"
    if day == today - dt.timedelta(days=1):
        return "yesterday"
    return None


def _job_item(j: dict, status: str, when: str | None = None) -> dict:
    item = {
        "id": j.get("id") or "",
        "title": str(j.get("title") or "")[:120],
        "status": status,
        "by": str(j.get("by") or "") or None,
        "stage": str(j.get("stage") or "") or None,
    }
    if when:
        item["when"] = when
    if j.get("after"):
        item["after"] = str(j["after"])
    prog = j.get("progress") or {}
    if isinstance(prog, dict) and prog.get("of"):
        try:
            item["progress"] = {"step": int(prog.get("step") or 0), "of": int(prog["of"])}
        except (TypeError, ValueError):
            pass
    return {k: v for k, v in item.items() if v is not None}


def _stage_item(stage_id: str, state: str) -> dict:
    label = STAGE_LABELS.get(stage_id, stage_id)
    if state in ("doing", "in_progress", "blocked", "review"):
        title = f"{label} — still open"
    else:
        title = f"{label} — not started"
    return {"kind": "stage", "stage": stage_id, "status": "todo", "title": title, "state": state or "todo"}


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


def _pct_reason(done_count: int | None, stage_id: str | None, leftovers: list) -> str:
    """Quiet one-liner so 67% makes sense next to remaining work."""
    bits = []
    if done_count is not None:
        bits.append(f"{done_count} of {TOTAL} stages")
    open_stage = None
    for it in leftovers:
        st = it.get("state") or ""
        if st in ("doing", "in_progress", "blocked", "review"):
            open_stage = it.get("stage")
            break
    open_stage = open_stage or stage_id
    if open_stage:
        bits.append(f"{STAGE_LABELS.get(open_stage, open_stage)} still open")
    return " · ".join(bits)


def leftover_stages(milestones: list, remaining_jobs: list) -> list:
    """Incomplete pipeline stages that have no open/claimed/blocked job yet — no invented job ids."""
    covered = {str(j.get("stage") or "") for j in remaining_jobs if j.get("stage")}
    out = []
    for m in milestones or []:
        sid = m.get("id")
        if not sid or complete(m) or sid in covered:
            continue
        state = m.get("displayState") or m.get("state") or "todo"
        out.append(_stage_item(sid, state))
    return out


def next_going_live(board: dict, at: dt.datetime, n: int = 4) -> list:
    """Next n not-yet-live videos by existing YouTube publishAt — never invent titles or dates."""
    rows = []
    for v in ((board.get("tracker") or {}).get("videos") or []):
        yt = v.get("youtube") or {}
        if yt.get("state") != "scheduled":
            continue
        if yt.get("privacy") == "public" or yt.get("state") == "live":
            continue
        pub = yt.get("publishAt") or ""
        t = _t(pub)
        if not t or t < at:
            continue
        key = v.get("key") or ""
        title = v.get("title") or ""
        if not key or not title:
            continue
        rows.append({
            "key": key,
            "title": title,
            "type": v.get("type") or "",
            "at": pub,
            "atLondon": yt.get("publishAtLondon") or "",
        })
    rows.sort(key=lambda r: (_t(r["at"]) or at, r["key"]))
    return rows[:n]


def _job_waiting(j: dict, done_ids: set) -> bool:
    """Blocked, or open/claimed but still waiting on another unfinished job."""
    if j.get("status") == "blocked":
        return True
    after = j.get("after")
    return bool(after and after not in done_ids)


def summarise(history: list, at: dt.datetime, counts: dict, done: list,
              open_jobs: list | None = None, stages: dict | None = None,
              all_done: list | None = None, milestones: dict | None = None,
              next_live: list | None = None) -> dict:
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
    milestones = milestones or {}
    all_done = all_done if all_done is not None else done
    done_ids = {j.get("id") for j in all_done if j.get("id")} | {
        j.get("id") for j in ((open_jobs or [])) if j.get("status") == "done" and j.get("id")
    }

    def _bucket(key, title=""):
        return by_film.setdefault(key, {"film": key, "title": title or titles.get(key, key), "jobs": 0, "last": "",
                                        "recent": [], "remaining": [], "earlier": 0})

    by_agent, by_film, studio_items = {}, {}, []
    # 24 h finished jobs drive the headline counts and which films earn a card.
    for j in done:
        a = str(j.get("by") or "other")
        by_agent[a] = by_agent.get(a, 0) + 1
        f = film_of(j, titles)
        when = done_when(j, at)
        item = _job_item(j, "done", when)
        if f:
            g = _bucket(f, titles.get(f, f))
            g["jobs"] += 1
            if not g["last"]:
                g["last"] = str(j.get("title") or "")[:90]
            if when in ("today", "yesterday"):
                g["recent"].append(item)
            else:
                g["earlier"] += 1
        else:
            studio_items.append(item)

    # Remaining open / claimed / blocked jobs (including Shorts attributed to the long).
    seen_ids = {it.get("id") for g in by_film.values() for it in g["recent"]} | {it.get("id") for it in studio_items}
    for j in open_jobs or []:
        if j.get("id") in seen_ids:
            continue
        f = film_of(j, titles)
        item = _job_item(j, j.get("status") or "open")
        if f:
            g = _bucket(f, titles.get(f, f))
            if not g["last"]:
                g["last"] = str(j.get("title") or "")[:90]
            g["remaining"].append(item)
            seen_ids.add(item["id"])

    # Films that moved a stage but had no attributed jobs still get a card.
    for m in moved:
        g = _bucket(m["key"], m["title"])
        if g["title"] in (m["key"], "") or not g["title"]:
            g["title"] = m["title"]

    # Today / yesterday / earlier finished jobs only enrich films that already earned a card
    # (moved, 24 h activity, or remaining work) — never invent a card from old backlog alone.
    card_films = set(by_film)
    for j in all_done:
        if not j.get("id") or j["id"] in seen_ids:
            continue
        f = film_of(j, titles)
        if not f or f not in card_films:
            continue
        when = done_when(j, at)
        g = by_film[f]
        if when in ("today", "yesterday"):
            g["recent"].append(_job_item(j, "done", when))
        else:
            # No usable timestamp, or older than yesterday → fold into the muted earlier note.
            g["earlier"] += 1
        seen_ids.add(j["id"])
    films = []
    glance_blocked = []
    for f, g in by_film.items():
        now_done, title = counts.get(f, [None, g["title"]])
        pct = round(now_done / TOTAL * 100) if now_done is not None else None
        mv = moved_by.get(f)
        stage_id = stages.get(f)
        leftovers = leftover_stages(milestones.get(f) or [], g["remaining"])
        # Checklist order: remaining jobs, leftover stages, today done, yesterday done.
        today_items = [it for it in g["recent"] if it.get("when") == "today"]
        yday_items = [it for it in g["recent"] if it.get("when") == "yesterday"]
        items = list(g["remaining"]) + leftovers + today_items + yday_items
        done_today = len(today_items)
        left = len(g["remaining"]) + len(leftovers)
        blocked_items = [it for it in g["remaining"] if it.get("status") == "blocked"
                         or _job_waiting(it, done_ids)]
        for it in blocked_items:
            glance_blocked.append({
                "id": it.get("id") or "",
                "film": f,
                "title": it.get("title") or "",
                "status": it.get("status") or "blocked",
            })
        reason = _pct_reason(now_done, stage_id, leftovers)
        card = {
            "film": f,
            "title": title or g["title"],
            "jobs": g["jobs"],
            "last": g["last"],
            "items": items,
            "status": _status_line(mv, pct, stage_id),
            "closed": bool(mv and mv.get("milestones", 0) > 0),
            "doneToday": done_today,
            "left": left,
            "blocked": len(blocked_items),
            "earlierDone": g["earlier"],
        }
        if reason:
            card["pctReason"] = reason
        if now_done is not None:
            card["doneCount"] = now_done
            card["total"] = TOTAL
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

    done_today_total = sum(1 for j in all_done if done_when(j, at) == "today")
    left_total = sum(f.get("left") or 0 for f in films)
    glance = {
        "doneToday": done_today_total,
        "left": left_total,
        "blocked": len(glance_blocked),
        "blockedJobs": glance_blocked[:12],
        "nextLive": list(next_live or [])[:4],
    }
    return {
        "hours": span_h, "since": base["at"] if base else "",
        "jobsDone": len(done), "byAgent": dict(sorted(by_agent.items(), key=lambda kv: -kv[1])),
        "milestones": sum(m["milestones"] for m in moved if m["milestones"] > 0),
        "moved": moved[:10], "films": films,
        "studio": studio_items,
        "otherJobs": len(studio_items),
        "videoJobs": sum(g["jobs"] for g in films),
        "glance": glance,
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
        all_done=jobs_done_all(board), milestones=video_milestones(board),
        next_live=next_going_live(board, at),
    )
