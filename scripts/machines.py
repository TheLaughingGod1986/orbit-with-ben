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

WINDOW = dt.timedelta(hours=24)
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
    return OF.get(a, "")


def finished(job: dict):
    """(when, agent) of the job's last 'done' history entry, or (None, '')."""
    for h in reversed(job.get("history") or []):
        if str(h.get("what", "")).startswith("done"):
            return _t(h.get("at")), str(h.get("by") or job.get("by") or "")
    return None, ""


def section(queue: dict, mini_hb: dict | None, macbook_hb: dict | None, at: dt.datetime) -> dict:
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
    if mini_hb:
        rows["mini"].update(state=str(mini_hb.get("state") or ""), why=str(mini_hb.get("note") or "")[:140],
                            seen=str(mini_hb.get("at") or ""))
    if macbook_hb:
        why = macbook_hb.get("why") or []
        rows["macbook"].update(state=str(macbook_hb.get("state") or ""),
                               why="; ".join(why) if isinstance(why, list) else str(why),
                               seen=str(macbook_hb.get("at") or ""), agents=macbook_hb.get("agents") or [])
        job = macbook_hb.get("job")
        if job and not any(n["id"] == job for n in rows["macbook"]["now"]):
            title = next((str(j.get("title") or "")[:110] for j in queue.get("jobs") or [] if j.get("id") == job), "")
            rows["macbook"]["now"].append({"id": job, "title": title, "agent": "macbook", "since": macbook_hb.get("at") or ""})
    out = [rows[m] for m, _, _ in MACHINES]
    # The Grok box only shows when it did something: it has no heartbeat of its own here.
    return {"machines": [r for r in out if r["id"] != "grok" or r["now"] or r["done24"]],
            "doneTotal": sum(r["done24"] for r in out), "at": at.strftime("%Y-%m-%dT%H:%MZ")}
