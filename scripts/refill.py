#!/usr/bin/env python3
"""Keep the Mini busy 24/7 (Ben, 12 Oct 2026: "it should always be picking up jobs, completing jobs").

Two rules, run by chief_relay.py on every 10-minute tick (and by hand). The same tick also queues the first-day
check of every video that went live about six hours ago (`first_day_checks`, scripts/launch_check.py):

  refill    When fewer than MIN_READY Mini jobs are ready to claim, add the next items from jobs/backlog.json
            (lowest tier: `jobs.order` runs them only when no pipeline job is ready; weekly audits and idea/script
            drafts for both channels come first in the file, then polish)
            (no-spend standing work for both channels: Shorts cut from locked longs, thumb B variants, teaching
            overlays, listing fixes, next scripts, HOS plate prep, QA sweeps). A key is skipped while a job from it is
            open, claimed or blocked (parked for Chief or anything else), while it has "paused" set, and for every_h
            hours after its last one. Each backlog job routes by its kind
            (scripts/routing.py), so the fallback chain (Claude Code -> Cursor on Claude -> Gemini -> Codex) applies.
  escalate  A job parked for Chief ("parked for Chief: ...") longer than STALE_H hours is posted once on #99 for the
            Chief, and a backlog key at most once per ESCALATE_EVERY_H. Parking never blocks other work: a parked job holds only itself (and jobs --after it).

  python3 scripts/refill.py refill [--min 3] [--git]
  python3 scripts/refill.py escalate [--hours 2] [--git]

Never: real money, deleting, public uploads without PASS. Backlog bodies say so and end parked for Chief.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs  # noqa: E402
import channels  # noqa: E402
import studio  # noqa: E402
import workflow_state as workflow  # noqa: E402

BACKLOG = jobs.ROOT / "jobs" / "backlog.json"
MIN_READY = 3
STALE_H = 2.0
CAPABILITY_TRAP_H = 24.0
# One live copy per key (Chief J0811, 21 Oct 2026): a key counted as busy only while open or claimed, so every copy
# the workers parked freed it, and 16-21 Oct added 28-30 copies of each of 15 keys (406 jobs). A parked job still
# holds only itself among the other keys' work (Ben, 12 Oct); it holds the next copy of its own key until it is done.
ESCALATE_EVERY_H = 24
# The never-empty fallback skips items on a weekly-ish cadence: it picked the key added longest ago, which was always a
# weekly audit, so the "weekly" OWB/HOS audits ran every 1-2 days (40+ HOS copies 15-28 Oct, J1099 two days after J0984).
STRICT_EVERY_H = 72
# ...and it still waits a little after a key's last copy: with only a few free keys it re-added the same listing check
# every few minutes once each was done (8 copies of "Backlog OWB: listing check" in 2 h, 31 Oct-1 Nov), each one a
# worker's time and credits spent re-checking nothing new. The floor is min(FALLBACK_MIN_H, every_h / 4).
FALLBACK_MIN_H = 6.0
LIVE = ("open", "claimed", "blocked")


def load_backlog(path: pathlib.Path = BACKLOG) -> list:
    return json.loads(path.read_text())["items"]


def ready(data: dict, at: dt.datetime) -> list:
    """Jobs a Mini worker could claim right now."""
    return [j for j in data["jobs"] if not j.get("for") and jobs.can_any_mini_claim(data, j, at)]


def parked_for_chief(job: dict) -> bool:
    return job["status"] == "blocked" and "parked for chief" in (job.get("result") or "").lower()


def do_refill(data: dict, items: list, at: dt.datetime, min_ready: int = MIN_READY) -> list:
    """Top up to min_ready claimable Mini jobs. A key is skipped while a job from it is open, claimed or blocked
    (whatever the reason), while the item is "paused", and for every_h hours after its last one. Never empty: if after
    that nothing at all is ready, the key whose last job is oldest is added anyway (still not a busy or paused one, and
    never one with every_h of STRICT_EVERY_H or more: weekly audits keep their week)."""
    added = []
    have = len(ready(data, at))
    last = data.setdefault("backlog_last", {})

    def busy(key):
        return any(j.get("backlog") == key and j["status"] in LIVE for j in data["jobs"])

    items = [it for it in items if not it.get("paused")]

    def add(it):
        nonlocal have
        j = jobs.do_add(data, title=it["title"], needs=it["needs"], body=it["body"], by="refill", at=at,
                        repo=it.get("repo") or channels.default(), eta_min=it.get("eta", jobs.DEFAULT_ETA), kind=it.get("kind", ""), action=it.get("remaining_action") or it["title"][:180])
        j["backlog"] = it["key"]
        last[it["key"]] = studio.iso(at)
        added.append(j["id"])
        have += 1

    # Calendar reviews are due even when production already fills the ready queue.
    # Queue once per London month; a missed first-day tick catches up on recovery.
    for it in items:
        if not it.get("monthly_on"):
            continue
        ln = at.astimezone(jobs.LONDON)
        hh, mm = (int(x) for x in it.get("monthly_at", "09:00").split(":"))
        due = ln.replace(day=int(it["monthly_on"]), hour=hh, minute=mm, second=0, microsecond=0)
        prev = last.get(it["key"])
        if ln < due or ln.strftime("%Y-%m") < it.get("start_month", "0000-00"):
            continue
        period = (ln.replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")
        if prev and studio.parse(prev).astimezone(jobs.LONDON).strftime("%Y-%m") == ln.strftime("%Y-%m"):
            continue
        if any(j.get("backlog") == it["key"] and j.get("report_month") == period for j in data["jobs"]):
            continue
        monthly = {**it, "title": it["title"] + " — " + period,
                   "body": "Report month: " + period + ". " + it["body"]}
        add(monthly)
        data["jobs"][-1].update(report_month=period, due=studio.iso(due + dt.timedelta(days=2)), due_kind="monthly-audit")

    # Daily items (Ben, 12 Oct 22:19): an item with "daily_at": "HH:MM" (London) is added once per London day as soon
    # as that time has passed, whatever the ready count, and put first in line (urgent), so it runs before 09:00.
    for it in items:
        if it.get("monthly_on") or not it.get("daily_at") or busy(it["key"]):
            continue
        ln = at.astimezone(jobs.LONDON)
        hh, mm = (int(x) for x in it["daily_at"].split(":"))
        prev = last.get(it["key"])
        if (ln.hour, ln.minute) < (hh, mm) or (prev and studio.parse(prev).astimezone(jobs.LONDON).date() == ln.date()):
            continue
        add(it)
        data["jobs"][-1]["urgent"] = 0
    for it in items:
        if it.get("daily_at") or it.get("monthly_on"):
            continue
        if have >= min_ready:
            break
        key = it["key"]
        if busy(key):
            continue
        if key in last and at - studio.parse(last[key]) < dt.timedelta(hours=it.get("every_h", 24)):
            continue
        add(it)
    if have == 0:
        def rested(it):
            prev = last.get(it["key"])
            floor = min(FALLBACK_MIN_H, it.get("every_h", 24) / 4)
            return not prev or at - studio.parse(prev) >= dt.timedelta(hours=floor)
        free = [it for it in items if not busy(it["key"]) and not it.get("daily_at") and not it.get("monthly_on")
                and it.get("every_h", 24) < STRICT_EVERY_H and rested(it)]
        if free:
            add(min(free, key=lambda it: last.get(it["key"], "")))
    return added


def parked_since(job: dict):
    for h in reversed(job.get("history", [])):
        if h["what"].startswith("blocked"):
            return studio.parse(h["at"])
    return None


def capability_waiting_since(job: dict, by_id: dict):
    stamps = [workflow.timestamp(job.get("created_at") or job.get("addedAt"))]
    if not stamps[0]:
        stamps = [workflow.timestamp(h.get("at")) for h in (job.get("history") or []) if h.get("at")][:1]
    base = next((t for t in stamps if t), None)
    if not base:
        return None
    for h in job.get("history") or []:
        t = workflow.timestamp(h.get("at"))
        if t and str(h.get("what") or "").startswith("reopened") and t > base:
            base = t
    if job.get("after"):
        parent = by_id.get(job["after"]) or {}
        for h in parent.get("history") or []:
            t = workflow.timestamp(h.get("at"))
            if t and str(h.get("what") or "").startswith("done") and t > base:
                base = t
    return base


def park_unshown_capabilities(data: dict, at: dt.datetime, capabilities: dict | None = None,
                              hours: float = CAPABILITY_TRAP_H) -> list:
    """A job needing a capability no worker has demonstrated in `hours` (24 h) goes to the Chief instead of sitting open."""
    by_id = {j["id"]: j for j in data["jobs"]}
    limit = dt.timedelta(hours=hours)
    out = []
    for j in data["jobs"]:
        if j.get("status") not in ("open", "blocked") or j.get("recheck_of"):
            continue
        if parked_for_chief(j) or j.get("capability_escalated"):
            continue
        if j.get("needs") == "ben" or j.get("awaits_ben") or workflow.dependency_problem(j, by_id):
            continue
        if j.get("after") and by_id.get(j["after"], {}).get("status") != "done":
            continue
        hold = j.get("hold") or {}
        if hold and hold.get("type") != "capability":
            continue
        if not hold and workflow.external_hold(j, at):
            continue
        reqs = workflow.capability_names(j.get("required_capabilities") or hold.get("requires") or [])
        if not reqs:
            continue
        since = capability_waiting_since(j, by_id)
        if not since or at - since < limit:
            continue
        missing = [c for c in reqs
                   if (last := workflow.capability_last_shown(c, capabilities)) is None or at - last >= limit]
        if not missing:
            continue
        if hold.get("type") == "capability":
            j.pop("hold", None)
            for x in data["jobs"]:
                if x.get("recheck_of") == j["id"] and x.get("status") in ("open", "blocked"):
                    x.update(status="cancelled",
                             result=f"superseded: {j['id']} parked for Chief after {int(hours)} h without {', '.join(missing)}",
                             eta="")
                    jobs.log(x, at, "refill", "cancelled: parent parked for Chief")
        j["required_capabilities"] = reqs
        waited_h = int((at - since).total_seconds() // 3600)
        reason = (f"parked for Chief: no worker has shown {', '.join(missing)} in {int(hours)} h "
                  f"(waiting {waited_h} h); route or re-scope")
        j.update(status="blocked", by="", since="", eta="", result=reason,
                 capability_escalated={"missing": missing, "at": studio.iso(at)},
                 escalated_at=studio.iso(at))
        jobs.log(j, at, "refill", "blocked: " + reason)
        out.append(j)
    return out


def do_escalate(data: dict, at: dt.datetime, hours: float = STALE_H,
                capabilities: dict | None = None, capability_hours: float = CAPABILITY_TRAP_H) -> list:
    out = list(park_unshown_capabilities(data, at, capabilities, capability_hours))
    recent = studio.iso(at - dt.timedelta(hours=ESCALATE_EVERY_H))
    posted = {j["backlog"] for j in data["jobs"] if j.get("backlog") and j.get("escalated_at", "") > recent}
    for j in data["jobs"]:
        if j in out or not parked_for_chief(j):
            continue
        since = parked_since(j)
        if not since or at - since < dt.timedelta(hours=hours) or j.get("escalated_at", "") >= studio.iso(since):
            continue
        if j.get("backlog") in posted:
            continue  # that key was posted for the Chief in the last day (it re-posted the same items for five days)
        if j.get("backlog"):
            posted.add(j["backlog"])
        j["escalated_at"] = studio.iso(at)
        jobs.log(j, at, "refill", f"escalated to Chief: parked {int((at - since).total_seconds() // 3600)} h")
        out.append(j)
    return out


def first_day_checks(data: dict, at: dt.datetime) -> list:
    """Queue the first-day check of every video that went live about six hours ago (scripts/launch_check.py; Ben,
    10 Nov 2026). It rides on this tick because the tick already runs every 10 minutes on the Mini. A fault in it
    must never stop the refill, so it is caught and said, not raised."""
    try:
        import launch_check
        return launch_check.queue_due(data, at)
    except Exception as e:  # noqa: BLE001
        print(f"first-day checks not queued: {e}", file=sys.stderr)
        return []


def top_up(data: dict, items: list, at: dt.datetime, min_ready: int = MIN_READY) -> list:
    """One refill tick: the first-day checks that are due, then the standing backlog."""
    return first_day_checks(data, at) + do_refill(data, items, at, min_ready)


def run(cmd: str, git: bool, min_ready: int = MIN_READY, hours: float = STALE_H) -> list:
    at = jobs.now()
    if cmd == "refill":
        items = load_backlog()
        apply = lambda d: (top_up(d, items, at, min_ready), None, [])  # noqa: E731
        msg = "jobs: refill from backlog by relay"
    else:
        caps = jobs.chief_relay.worker_capabilities()
        apply = lambda d: ([j["id"] + " " + j["title"][:80] for j in do_escalate(d, at, hours, capabilities=caps)], None, [])  # noqa: E731
        msg = "jobs: escalate stale Chief reviews by relay"
    if git:
        out, err = jobs.with_git(apply, msg)
        if err:
            raise RuntimeError(err)
        return out or []
    data = jobs.load()
    out, _, _ = apply(data)
    if out:
        jobs.save(data)
        jobs.JOBS_MD.write_text(jobs.render(data, at))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["refill", "escalate"])
    ap.add_argument("--min", type=int, default=MIN_READY)
    ap.add_argument("--hours", type=float, default=STALE_H)
    ap.add_argument("--git", action="store_true")
    a = ap.parse_args(argv)
    try:
        lines = run(a.cmd, a.git, a.min, a.hours)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
