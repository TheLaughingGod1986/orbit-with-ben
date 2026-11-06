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


def _hold_of(j: dict) -> dict:
    """Existing hold / blocked_reason dict on a job — never invent one."""
    for key in ("hold", "blocked_reason", "blockedReason"):
        h = j.get(key)
        if isinstance(h, dict) and (h.get("type") or h.get("condition")):
            return h
    return {}


def _short(text: str, n: int = 72) -> str:
    s = " ".join(str(text or "").split())
    if len(s) <= n:
        return s
    return s[: max(0, n - 1)].rstrip(" ,;:.") + "…"


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
    hold = _hold_of(j)
    if hold.get("type"):
        item["holdType"] = str(hold["type"])
    if hold.get("condition"):
        item["holdCondition"] = _short(hold["condition"], 160)
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


def _job_index(*groups) -> dict:
    """id → job from whatever board lists we have (open + done). Later rows win."""
    by = {}
    for group in groups:
        for j in group or []:
            jid = j.get("id")
            if jid:
                by[str(jid)] = j
    return by


def _is_finished(j: dict | None, done_ids: set) -> bool:
    if not j:
        return False
    jid = j.get("id")
    if jid and jid in done_ids:
        return True
    return j.get("status") in ("done", "cancelled")


def _job_waiting(j: dict, done_ids: set, by_id: dict | None = None) -> bool:
    """True when this job cannot run yet: unfinished after, or a real blocked hold."""
    return classify_cant_run(j, done_ids, by_id or {})[0] is not None


def unfinished_predecessors(j: dict, by_id: dict, done_ids: set) -> list:
    """Walk `after` toward the root; return unfinished predecessors earliest-first.
    Uses only edges already on the jobs — never invents a link."""
    chain, seen = [], set()
    cur = j
    while cur:
        aid = str(cur.get("after") or "").strip()
        if not aid or aid in seen:
            break
        seen.add(aid)
        pred = by_id.get(aid)
        if pred is None:
            if aid not in done_ids:
                chain.append({"id": aid, "title": ""})
            break
        if not _is_finished(pred, done_ids):
            chain.append({"id": aid, "title": _short(pred.get("title") or "", 48)})
        cur = pred
    chain.reverse()
    return chain


def _name_pred(p: dict) -> str:
    jid = p.get("id") or ""
    title = (p.get("title") or "").strip()
    if jid and title:
        return f"{jid} ({title})"
    return jid or title or "an earlier job"


def after_why(preds: list) -> str:
    """Ben: say the task will run automatically after the earlier unfinished jobs."""
    if not preds:
        return "Will run automatically after earlier work finishes"
    names = [_name_pred(p) for p in preds]
    if len(names) == 1:
        return f"Will run automatically after {names[0]}"
    if len(names) == 2:
        return f"Will run automatically after {names[0]}, then {names[1]}"
    head, last = ", ".join(names[:-1]), names[-1]
    return f"Will run automatically after {head}, then {last}"


def blocker_why(j: dict) -> str:
    """Plain needed-reason from existing hold type/condition — never dump the dict."""
    hold = _hold_of(j)
    cond = _short(hold.get("condition") or "", 110)
    typ = str(hold.get("type") or "").lower()
    if typ == "ben":
        return f"Needs Ben: {cond}" if cond else "Needs Ben"
    if typ == "public":
        return f"Needs a public video: {cond}" if cond else "Needs a public video"
    if typ == "date":
        return f"Waiting on a date: {cond}" if cond else "Waiting on a date"
    if typ == "credits":
        return f"Needs credits: {cond}" if cond else "Needs credits"
    if typ == "capability":
        reqs = hold.get("requires")
        if isinstance(reqs, list) and reqs and all(isinstance(x, str) and x for x in reqs):
            return f"Needs capability: {', '.join(reqs[:4])}"
        return f"Needs a capability check: {cond}" if cond else "Needs a capability check"
    if typ == "test":
        return f"Waiting on a running test: {cond}" if cond else "Waiting on a running test"
    if typ == "input":
        return f"Needs: {cond}" if cond else "Needs an input before it can run"
    if typ == "dependency":
        return f"Needs: {cond}" if cond else "Needs earlier work to finish"
    # Blocked with a result/note but no typed hold — use the existing text only.
    for key in ("result", "remaining_action"):
        raw = j.get(key)
        if isinstance(raw, str) and raw.strip():
            return _short(raw.strip().removeprefix("blocked: ").removeprefix("parked for Chief: "), 120)
    title = _short(j.get("title") or "", 72)
    jid = j.get("id") or ""
    if jid and title:
        return f"{jid} · {title} — can't run yet"
    return title or (f"{jid} — can't run yet" if jid else "Can't run yet")


def classify_cant_run(j: dict, done_ids: set, by_id: dict) -> tuple[str | None, str | None, list]:
    """('after'|'blocker'|None, why, unfinished predecessor list)."""
    preds = unfinished_predecessors(j, by_id, done_ids)
    hold = _hold_of(j)
    typ = str(hold.get("type") or "").lower()
    # Unfinished after (or dependency hold still pointing at unfinished work) = workflow wait.
    if preds:
        return "after", after_why(preds), preds
    after = str(j.get("after") or "").strip()
    if after and after not in done_ids and not _is_finished(by_id.get(after), done_ids):
        preds = [{"id": after, "title": _short((by_id.get(after) or {}).get("title") or "", 48)}]
        return "after", after_why(preds), preds
    if j.get("status") == "blocked" or (typ and typ != "dependency"):
        return "blocker", blocker_why(j), []
    if typ == "dependency":
        # Predecessor already finished — condition may still ask for a verify step.
        return "blocker", blocker_why(j), []
    return None, None, []


def annotate_cant_run(item: dict, src: dict, done_ids: set, by_id: dict) -> dict:
    """Attach waitKind / why / afterChain from real job fields onto a checklist item."""
    kind, why, preds = classify_cant_run(src, done_ids, by_id)
    if not kind:
        return item
    item = dict(item)
    item["waitKind"] = kind
    item["why"] = why
    if preds:
        item["afterChain"] = preds
    return item


def order_by_after(items: list) -> list:
    """Hierarchy order: prerequisites above jobs that wait on them (A, then B, then C)."""
    nodes = [it for it in items if it.get("id")]
    stages = [it for it in items if not it.get("id")]
    ids = {it["id"] for it in nodes}
    after_of = {it["id"]: (it.get("after") if it.get("after") in ids else None) for it in nodes}
    children = {i: [] for i in ids}
    roots = []
    for i, a in after_of.items():
        if a:
            children[a].append(i)
        else:
            roots.append(i)

    def sort_key(i):
        it = next(x for x in nodes if x["id"] == i)
        stage = it.get("stage") or ""
        try:
            sr = STAGE_ORDER.index(stage)
        except ValueError:
            sr = 99
        return (sr, i)

    for k in children:
        children[k].sort(key=sort_key)
    roots.sort(key=sort_key)
    out, seen = [], set()

    def visit(i):
        if i in seen:
            return
        seen.add(i)
        out.append(next(x for x in nodes if x["id"] == i))
        for c in children.get(i) or []:
            visit(c)

    for r in roots:
        visit(r)
    # Cycles / orphans not reached from a root — keep stable id order at the end.
    for it in sorted(nodes, key=lambda x: x["id"]):
        if it["id"] not in seen:
            out.append(it)
    # Leftover stage rows keep STAGE_ORDER after the job chain.
    def stage_key(it):
        try:
            return STAGE_ORDER.index(it.get("stage") or "")
        except ValueError:
            return 99
    out.extend(sorted(stages, key=stage_key))
    return out


def normalize_focus(focus) -> set[str]:
    """Queue/board focus entries → match set (bare 032 and OWB:032 / HOS:032). No titles invented."""
    out: set[str] = set()
    for raw in focus or []:
        s = str(raw or "").strip()
        if not s:
            continue
        out.add(s)
        if re.fullmatch(r"\d{3}", s):
            for lab in channels.labels():
                out.add(f"{lab}:{s}")
            continue
        m = re.fullmatch(r"([A-Za-z]+):(\d{3})", s)
        if m:
            lab, num = m.group(1).upper(), m.group(2)
            out.add(f"{lab}:{num}")
            out.add(num)
    return out


def in_focus(film_key: str, focus: set[str]) -> bool:
    """True when this Overview film card belongs to the current studio focus.
    Exact long keys only (OWB:032) — Shorts keys like OWB:032:S:… are not separate focus cards.
    Empty focus means no filter (legacy: show every earned card)."""
    if not focus:
        return True
    key = str(film_key or "")
    if key in focus:
        return True
    m = re.fullmatch(r"([A-Z]+):(\d{3})", key)
    return bool(m and (m.group(2) in focus or f"{m.group(1)}:{m.group(2)}" in focus))


def _blocked_why(blocked_items: list) -> str | None:
    """One clear workflow / needed line for the film card (prefer after-wait copy)."""
    if not blocked_items:
        return None
    # Prefer "will run after …" so the card reads as progress, not a wall.
    ordered = sorted(blocked_items, key=lambda it: 0 if it.get("waitKind") == "after" else 1)
    why = (ordered[0].get("why") or "").strip()
    return why or None


def board_focus(board: dict) -> list:
    """Focus keys from published board.owb.focus (kanban_snapshot ← queue.json)."""
    owb = board.get("owb") or {}
    raw = owb.get("focus")
    return list(raw) if isinstance(raw, list) else []


def summarise(history: list, at: dt.datetime, counts: dict, done: list,
              open_jobs: list | None = None, stages: dict | None = None,
              all_done: list | None = None, milestones: dict | None = None,
              next_live: list | None = None, focus: list | None = None) -> dict:
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
    by_id = _job_index(all_done, done, open_jobs)
    open_by_id = {str(j["id"]): j for j in (open_jobs or []) if j.get("id")}

    def _bucket(key, title=""):
        return by_film.setdefault(key, {"film": key, "title": title or titles.get(key, key), "jobs": 0, "last": "",
                                        "recent": [], "remaining": [], "earlier": 0})

    focus_set = normalize_focus(focus)
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
    # Focus films always get a card on Overview, even with no 24 h activity (Ben, 6 Nov evening).
    if focus_set:
        for key, (_n, title) in counts.items():
            if in_focus(key, focus_set) and re.fullmatch(r"[A-Z]+:\d{3}", key):
                _bucket(key, title)

    # Remaining open / claimed / blocked jobs (including Shorts attributed to the long).
    seen_ids = {it.get("id") for g in by_film.values() for it in g["recent"]} | {it.get("id") for it in studio_items}
    for j in open_jobs or []:
        if j.get("id") in seen_ids:
            continue
        f = film_of(j, titles)
        item = annotate_cant_run(_job_item(j, j.get("status") or "open"), j, done_ids, by_id)
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
    # 24 h video-job head count stays global; Overview cards + glance follow focus when set.
    video_jobs_all = sum(g["jobs"] for g in by_film.values())
    films = []
    glance_blocked = []
    for f, g in by_film.items():
        if not in_focus(f, focus_set):
            continue
        now_done, title = counts.get(f, [None, g["title"]])
        pct = round(now_done / TOTAL * 100) if now_done is not None else None
        mv = moved_by.get(f)
        stage_id = stages.get(f)
        leftovers = leftover_stages(milestones.get(f) or [], g["remaining"])
        # Hierarchy: prerequisites above waiters; then leftover stages; then today/yesterday ticks.
        today_items = [it for it in g["recent"] if it.get("when") == "today"]
        yday_items = [it for it in g["recent"] if it.get("when") == "yesterday"]
        remaining_ordered = order_by_after(list(g["remaining"]) + leftovers)
        items = remaining_ordered + today_items + yday_items
        done_today = len(today_items)
        left = len(g["remaining"]) + len(leftovers)
        blocked_items = [it for it in remaining_ordered if it.get("waitKind") or _job_waiting(
            open_by_id.get(it.get("id") or "", it), done_ids, by_id)]
        for it in blocked_items:
            row = {
                "id": it.get("id") or "",
                "film": f,
                "title": it.get("title") or "",
                "status": it.get("status") or "blocked",
            }
            if it.get("waitKind"):
                row["waitKind"] = it["waitKind"]
            if it.get("why"):
                row["why"] = it["why"]
            glance_blocked.append(row)
        reason = _pct_reason(now_done, stage_id, leftovers)
        why = _blocked_why(blocked_items)
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
        if why:
            card["blockedWhy"] = why
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

    # Focus order when set; else moved films first, then most finished jobs.
    if focus_set:
        focus_rank = {k: i for i, k in enumerate(
            [x for x in (focus or []) if re.fullmatch(r"[A-Za-z]+:\d{3}", str(x or ""))]
            or sorted(k for k in focus_set if re.fullmatch(r"[A-Z]+:\d{3}", k))
        )}
        films.sort(key=lambda g: (focus_rank.get(g["film"], 99), g["film"]))
    else:
        films.sort(key=lambda g: (
            0 if g.get("closed") else 1,
            -(g.get("milestones") or 0),
            -g["jobs"],
            -len(g.get("items") or []),
            g["film"],
        ))

    # Glance matches the cards on screen (focus-scoped when focus is set).
    glance = {
        "doneToday": sum(f.get("doneToday") or 0 for f in films),
        "left": sum(f.get("left") or 0 for f in films),
        "blocked": len(glance_blocked),
        "blockedJobs": glance_blocked[:12],
        "nextLive": list(next_live or [])[:4],
    }
    out = {
        "hours": span_h, "since": base["at"] if base else "",
        "jobsDone": len(done), "byAgent": dict(sorted(by_agent.items(), key=lambda kv: -kv[1])),
        "milestones": sum(m["milestones"] for m in moved if m["milestones"] > 0),
        "moved": moved[:10], "films": films,
        "studio": studio_items,
        "otherJobs": len(studio_items),
        "videoJobs": video_jobs_all,
        "glance": glance,
    }
    if focus_set:
        # Only the long keys that earned an Overview card (not every channel expansion of a bare 032).
        out["focus"] = [f["film"] for f in films if re.fullmatch(r"[A-Z]+:\d{3}", f["film"])]
    return out


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
        next_live=next_going_live(board, at), focus=board_focus(board),
    )
