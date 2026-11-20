#!/usr/bin/env python3
"""Machines on the Studio home page (Ben, 4 Nov 2026: "I see what job is on, MacBook Pro, and what is the mini, and
how many jobs each machine completed in the last 24 hours").

board_publish.py calls `section(queue, mini_hb, macbook_hb, at)` on every publish. For each machine it gives the jobs
claimed on it now, its own heartbeat (state and why it is idle), and the jobs it finished in the last 24 h, by agent.
Which machine a job ran on comes from the agent id that claimed or finished it:
  Mac mini   codex, gemini, cursor (the relay's workers) and the relay itself
  MacBook    macbook (every agent CLI the MacBook worker wakes claims as `macbook`)
  Cloud      claude (Claude's cloud runs)
  Grok box   chief (Grok Bot)
Reads only; never fails the publish.
"""
import datetime as dt
import re

WINDOW = dt.timedelta(hours=24)
# A plain Grok post in this window means the box is working, even with no claimed job (J3248).
GROK_POST_WORKING = dt.timedelta(hours=3)
MACHINES = [
    ("mini", "Mac mini", ("codex", "gemini", "cursor", "relay")),
    ("macbook", "MacBook Pro", ("macbook",)),
    ("cloud", "Claude (cloud)", ("claude",)),
    ("grok", "Grok box", ("chief",)),
]
OF = {a: m for m, _, agents in MACHINES for a in agents}


def _t(s):
    try:
        return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def machine_of(agent: str) -> str:
    a = str(agent or "").split("/")[0].strip().lower()
    return OF.get(re.sub(r"^macbook-\d+$", "macbook", a), "")


def finished(job: dict):
    """(when, agent) of the job's last 'done' history entry, or (None, '')."""
    for h in reversed(job.get("history") or []):
        if str(h.get("what", "")).startswith("done"):
            return _t(h.get("at")), str(h.get("by") or job.get("by") or "")
    return None, ""


def _add(row: dict, job: str, agent: str, since: str, queue: dict) -> None:
    if job and not any(n["id"] == job for n in row["now"]):
        title = next((str(j.get("title") or "")[:110] for j in queue.get("jobs") or [] if j.get("id") == job), "")
        row["now"].append({"id": job, "title": title, "agent": agent, "since": since})


def grok_activity(queue: dict, at: dt.datetime, posts) -> tuple:
    """Jobs Grok touched in the last day, the newest stamp, and whether a post landed in the last 3 hours.

    A jobs.py history line by `chief` counts, and so does a ruling post that names a job. A post that names no job
    still marks the box as working when it is inside 3 hours; it does not add a job to the count."""
    ids = set()
    last_record_at, last_record = None, ""
    for job in queue.get("jobs") or []:
        jid = str(job.get("id") or "")
        for entry in job.get("history") or []:
            if entry.get("by") != "chief":
                continue
            when = _t(entry.get("at"))
            if not when or when > at or at - when > WINDOW:
                continue
            if jid:
                ids.add(jid)
            if last_record_at is None or when > last_record_at:
                last_record_at, last_record = when, str(entry.get("at") or "")
    last_post_at, last_post = None, ""
    for post in posts or []:
        if not isinstance(post, dict):
            continue
        when = _t(post.get("at"))
        if not when or when > at or at - when > WINDOW:
            continue
        if last_post_at is None or when > last_post_at:
            last_post_at, last_post = when, str(post.get("at") or "")
        for jid in post.get("jobs") or []:
            if jid:
                ids.add(str(jid))
    seen = last_post if last_post_at and (last_record_at is None or last_post_at >= last_record_at) else last_record
    working = bool(last_post_at and at - last_post_at <= GROK_POST_WORKING)
    return ids, seen, working


def section(queue: dict, mini_hb: dict | None, macbook_hb: dict | None, at: dt.datetime, executions=None,
            grok_posts=None) -> dict:
    """`executions`: the relay's live runs on the Mini ({job, worker, startedAt}, from chief_relay.current_execution),
    which show a job the moment a worker is woken, before its claim reaches the queue."""
    rows = {m: {"id": m, "name": name, "now": [], "done24": 0, "byAgent": {}, "state": "", "why": "", "seen": ""}
            for m, name, _ in MACHINES}
    for j in queue.get("jobs") or []:
        if j.get("status") == "claimed":
            m = machine_of(j.get("by"))
            if m:
                rows[m]["now"].append({"id": j.get("id"), "title": str(j.get("title") or "")[:110],
                                       "agent": j.get("by"), "since": j.get("since") or ""})
        elif j.get("status") == "done":
            when, agent = finished(j)
            m = machine_of(agent)
            if m and when and at - when <= WINDOW:
                rows[m]["done24"] += 1
                rows[m]["byAgent"][agent] = rows[m]["byAgent"].get(agent, 0) + 1
    for ex in [e for e in (executions or []) if isinstance(e, dict)]:
        m = machine_of(ex.get("worker")) or "mini"
        _add(rows[m], str(ex.get("job") or ""), str(ex.get("worker") or ""), str(ex.get("startedAt") or ""), queue)
    if mini_hb:
        seen = _t(mini_hb.get("at"))
        note = str(mini_hb.get("note") or "")
        import re
        woke = re.match(r"woke (\w+) for (J\d+)", note)
        # A run lasts at most 25 min: a 'woke X for J…' heartbeat younger than that is still the Mini's current job.
        if woke and mini_hb.get("state") == "running" and seen and at - seen <= dt.timedelta(minutes=26):
            _add(rows["mini"], woke.group(2), woke.group(1).lower(), str(mini_hb.get("at") or ""), queue)
        rows["mini"].update(state=str(mini_hb.get("state") or ""), why=str(mini_hb.get("note") or "")[:140],
                            seen=str(mini_hb.get("at") or ""))
    if macbook_hb:
        why = macbook_hb.get("why") or []
        rows["macbook"].update(state=str(macbook_hb.get("state") or ""),
                               why="; ".join(why) if isinstance(why, list) else str(why),
                               seen=str(macbook_hb.get("at") or ""), agents=macbook_hb.get("agents") or [])
        # Each slot's own report (two jobs at once, 5 Nov 2026); a single-slot heartbeat is its own only slot.
        for hb in macbook_hb.get("slots") or [macbook_hb]:
            if hb.get("job"):
                _add(rows["macbook"], str(hb.get("job") or ""), str(hb.get("agent") or "macbook"),
                     str(hb.get("at") or ""), queue)
    # Cloud Claude has no heartbeat here: "seen" is its last entry in the queue's history.
    if not rows["cloud"]["seen"]:
        rows["cloud"]["seen"] = max((str(h.get("at") or "") for j in queue.get("jobs") or []
                                     for h in j.get("history") or [] if h.get("by") == "claude"), default="")
    # Grok's day is jobs.py lines by chief plus ruling posts that name a job. A post in the last 3 hours is work,
    # so the card says so instead of Idle (J3248).
    grok_ids, grok_seen, grok_working = grok_activity(queue, at, grok_posts)
    rows["grok"]["done24"] = len(grok_ids)
    rows["grok"]["byAgent"] = {"chief": len(grok_ids)} if grok_ids else {}
    if grok_seen:
        rows["grok"]["seen"] = grok_seen
    elif not rows["grok"]["seen"]:
        rows["grok"]["seen"] = max((str(h.get("at") or "") for j in queue.get("jobs") or []
                                    for h in j.get("history") or [] if h.get("by") == "chief"), default="")
    if grok_working:
        rows["grok"]["state"] = "rulings"
        rows["grok"]["why"] = "Working (rulings on the thread)"
    out = [rows[m] for m, _, _ in MACHINES]
    # The Grok box shows when it has a job, a day's work, or a post in the last 3 hours.
    return {"machines": [r for r in out if r["id"] != "grok" or r["now"] or r["done24"] or r.get("state") == "rulings"],
            "doneTotal": sum(r["done24"] for r in out), "at": at.strftime("%Y-%m-%dT%H:%MZ")}
