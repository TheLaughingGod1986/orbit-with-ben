#!/usr/bin/env python3
"""Keep the Mini busy 24/7 (Ben, 12 Oct 2026: "it should always be picking up jobs, completing jobs").

Two rules, run by chief_relay.py on every 10-minute tick (and by hand):

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
import studio  # noqa: E402

BACKLOG = jobs.ROOT / "jobs" / "backlog.json"
MIN_READY = 3
STALE_H = 2.0
# One live copy per key (Chief J0811, 21 Oct 2026): a key counted as busy only while open or claimed, so every copy
# the workers parked freed it, and 16-21 Oct added 28-30 copies of each of 15 keys (406 jobs). A parked job still
# holds only itself among the other keys' work (Ben, 12 Oct); it holds the next copy of its own key until it is done.
ESCALATE_EVERY_H = 24
LIVE = ("open", "claimed", "blocked")


def load_backlog(path: pathlib.Path = BACKLOG) -> list:
    return json.loads(path.read_text())["items"]


def ready(data: dict, at: dt.datetime) -> list:
    """Jobs a Mini worker could claim right now."""
    return [j for j in data["jobs"] if not j.get("for") and jobs.claimable(data, j, jobs.MINI_NEEDS, at)]


def parked_for_chief(job: dict) -> bool:
    return job["status"] == "blocked" and "parked for chief" in (job.get("result") or "").lower()


def do_refill(data: dict, items: list, at: dt.datetime, min_ready: int = MIN_READY) -> list:
    """Top up to min_ready claimable Mini jobs. A key is skipped while a job from it is open, claimed or blocked
    (whatever the reason), while the item is "paused", and for every_h hours after its last one. Never empty: if after
    that nothing at all is ready, the key whose last job is oldest is added anyway (still not a busy or paused one)."""
    added = []
    have = len(ready(data, at))
    last = data.setdefault("backlog_last", {})

    def busy(key):
        return any(j.get("backlog") == key and j["status"] in LIVE for j in data["jobs"])

    items = [it for it in items if not it.get("paused")]

    def add(it):
        nonlocal have
        j = jobs.do_add(data, title=it["title"], needs=it["needs"], body=it["body"], by="refill", at=at,
                        repo=it.get("repo", "owb"), eta_min=it.get("eta", jobs.DEFAULT_ETA), kind=it.get("kind", ""))
        j["backlog"] = it["key"]
        last[it["key"]] = studio.iso(at)
        added.append(j["id"])
        have += 1

    # Daily items (Ben, 12 Oct 22:19): an item with "daily_at": "HH:MM" (London) is added once per London day as soon
    # as that time has passed, whatever the ready count, and put first in line (urgent), so it runs before 09:00.
    for it in items:
        if not it.get("daily_at") or busy(it["key"]):
            continue
        ln = at.astimezone(jobs.LONDON)
        hh, mm = (int(x) for x in it["daily_at"].split(":"))
        prev = last.get(it["key"])
        if (ln.hour, ln.minute) < (hh, mm) or (prev and studio.parse(prev).astimezone(jobs.LONDON).date() == ln.date()):
            continue
        add(it)
        data["jobs"][-1]["urgent"] = 0
    for it in items:
        if it.get("daily_at"):
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
        free = [it for it in items if not busy(it["key"]) and not it.get("daily_at")]
        if free:
            add(min(free, key=lambda it: last.get(it["key"], "")))
    return added


def parked_since(job: dict):
    for h in reversed(job.get("history", [])):
        if h["what"].startswith("blocked"):
            return studio.parse(h["at"])
    return None


def do_escalate(data: dict, at: dt.datetime, hours: float = STALE_H) -> list:
    out = []
    recent = studio.iso(at - dt.timedelta(hours=ESCALATE_EVERY_H))
    posted = {j["backlog"] for j in data["jobs"] if j.get("backlog") and j.get("escalated_at", "") > recent}
    for j in data["jobs"]:
        if not parked_for_chief(j):
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


def run(cmd: str, git: bool, min_ready: int = MIN_READY, hours: float = STALE_H) -> list:
    at = jobs.now()
    if cmd == "refill":
        items = load_backlog()
        apply = lambda d: (do_refill(d, items, at, min_ready), None, [])  # noqa: E731
        msg = "jobs: refill from backlog by relay"
    else:
        apply = lambda d: ([j["id"] + " " + j["title"][:80] for j in do_escalate(d, at, hours)], None, [])  # noqa: E731
        msg = "jobs: escalate stale Chief reviews by relay"
    if git:
        out, err = jobs.with_git(apply, msg)
        if err:
            print(err, file=sys.stderr)
            return []
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
    for line in run(a.cmd, a.git, a.min, a.hours):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
