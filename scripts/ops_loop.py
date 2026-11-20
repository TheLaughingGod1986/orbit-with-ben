#!/usr/bin/env python3
"""Weekly Studio Ops Loop (J3257 item 4, Ben 20 Nov 2026): the studio improving itself every week.

Measures six operational metrics over the trailing 7 days from jobs/queue.json and the AI spend ledger:
  1. jobs done per day per machine
  2. idle agent-hours with ready work
  3. stall and park counts
  4. Chief FIX rate
  5. time from job to Ben-watch
  6. credit spend per finished film

Names the single biggest bottleneck, optionally queues its fix job (guardrailed, £0, deduplicated),
and re-measures the following week against history.jsonl to prove whether last week's fix helped.

Commands:
    python3 scripts/ops_loop.py measure [--as-of YYYY-MM-DDTHH:MMZ]
    python3 scripts/ops_loop.py run [--write] [--queue-fix] [--as-of YYYY-MM-DDTHH:MMZ]
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import re
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import channels  # noqa: E402
import jobs  # noqa: E402
import machines  # noqa: E402
import studio  # noqa: E402

UTC = dt.timezone.utc
WINDOW_DAYS = 7
STALL_RE = re.compile(r"\b(stall(?:ed|s)?|expired|reclaimed|timed?\s*out|auto[- ]?released)\b", re.I)
FIX_RE = re.compile(r"\b(fix(?:es)?|fail(?:ed)?|reopen(?:ed)?|reject(?:ed)?|needs?\s+changes?)\b", re.I)
PASS_RE = re.compile(r"\b(pass(?:ed)?|approved|chief\s+ok|accepted)\b", re.I)
BEN_WATCH_RE = re.compile(r"\b(ben[- ]?watch|for\s+ben|uat\s+handoff|ready\s+for\s+ben)\b", re.I)


def ops_dir() -> pathlib.Path:
    return channels.studio_records("ops_loop")


def _parse_ts(value) -> dt.datetime | None:
    if not value:
        return None
    try:
        t = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return t.replace(tzinfo=UTC) if t.tzinfo is None else t.astimezone(UTC)
    except ValueError:
        return None


def _load_spend_rows(path: pathlib.Path | None = None) -> list[dict]:
    p = path or channels.studio_records("ai_spend", "ledger.jsonl")
    if not p.is_file():
        return []
    rows = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def _load_history(path: pathlib.Path | None = None) -> list[dict]:
    p = path or (ops_dir() / "history.jsonl")
    if not p.is_file():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                out.append(obj)
        except ValueError:
            continue
    return out


def _job_events(job: dict) -> list[tuple[dt.datetime, str, str]]:
    out = []
    for h in job.get("history") or []:
        t = _parse_ts(h.get("at"))
        if t:
            out.append((t, str(h.get("by") or ""), str(h.get("what") or "")))
    out.sort(key=lambda item: item[0])
    return out


def _estimate_idle_hours_with_ready_work(queue_jobs: list[dict], start: dt.datetime, end: dt.datetime) -> dict:
    """Scan hourly buckets over [start, end): count hours where ready work existed while 0 workers were active."""
    by_id = {j.get("id"): j for j in queue_jobs if isinstance(j, dict) and j.get("id")}
    # Precompute simple state transitions per job from history
    timelines: list[tuple[dict, list[tuple[dt.datetime, str]]]] = []
    for j in queue_jobs:
        if not isinstance(j, dict):
            continue
        events = _job_events(j)
        if not events:
            continue
        states = []
        for t, _by, what in events:
            low = what.lower()
            if low.startswith("added") or low.startswith("reopened") or low.startswith("released"):
                states.append((t, "open"))
            elif low.startswith("claimed"):
                states.append((t, "claimed"))
            elif low.startswith("blocked"):
                states.append((t, "blocked"))
            elif low.startswith("done"):
                states.append((t, "done"))
            elif low.startswith("cancelled"):
                states.append((t, "cancelled"))
        if states:
            timelines.append((j, states))

    def state_at(states: list[tuple[dt.datetime, str]], ts: dt.datetime) -> str:
        cur = ""
        for t, st in states:
            if t <= ts:
                cur = st
            else:
                break
        return cur

    # Pre-index done times for dependency checks
    done_times: dict[str, dt.datetime] = {}
    for j, states in timelines:
        for t, st in reversed(states):
            if st == "done":
                done_times[j["id"]] = t
                break

    hours_total = max(1, int((end - start).total_seconds() // 3600))
    idle_hours = 0
    ready_hours = 0
    for h in range(hours_total):
        ts = start + dt.timedelta(hours=h, minutes=30)
        has_ready = False
        active_workers = 0
        for j, states in timelines:
            if j.get("needs") not in ("mini", "any"):
                continue
            st = state_at(states, ts)
            if st == "claimed":
                active_workers += 1
            elif st == "open":
                after_id = j.get("after")
                if after_id and after_id in by_id:
                    dt_done = done_times.get(after_id)
                    if not dt_done or dt_done > ts:
                        continue
                has_ready = True
        if has_ready:
            ready_hours += 1
            if active_workers == 0:
                idle_hours += 1
    return {
        "idle_hours_zero_active": idle_hours,
        "ready_work_hours": ready_hours,
        "window_hours": hours_total,
    }


def measure(
    queue: dict,
    spend_rows: list[dict] | None = None,
    as_of: dt.datetime | None = None,
    window_days: int = WINDOW_DAYS,
) -> dict:
    """Compute all 6 studio operational metrics and diagnose the single biggest bottleneck."""
    now = as_of or dt.datetime.now(UTC)
    if now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    start = now - dt.timedelta(days=window_days)
    queue_jobs = [j for j in (queue.get("jobs") or []) if isinstance(j, dict)]

    # 1. Jobs done per day per machine
    done_counts = {m: 0 for m, _, _ in machines.MACHINES}
    done_total = 0
    for j in queue_jobs:
        if j.get("status") != "done":
            continue
        when, agent = machines.finished(j)
        if when and start <= when <= now:
            m = machines.machine_of(agent)
            if m in done_counts:
                done_counts[m] += 1
            done_total += 1
    jobs_per_day = {m: round(c / float(window_days), 2) for m, c in done_counts.items()}

    # 2. Idle agent-hours with ready work
    idle_info = _estimate_idle_hours_with_ready_work(queue_jobs, start, now)

    # 3. Stall and park counts
    stalls_7d = 0
    parks_7d = 0
    chief_parks_7d = 0
    currently_parked = 0
    for j in queue_jobs:
        if j.get("status") == "blocked" and "parked for chief" in str(j.get("result") or "").lower():
            currently_parked += 1
        for t, _by, what in _job_events(j):
            if not (start <= t <= now):
                continue
            if STALL_RE.search(what):
                stalls_7d += 1
            if what.lower().startswith("blocked:"):
                parks_7d += 1
                if "parked for chief" in what.lower():
                    chief_parks_7d += 1

    # 4. Chief FIX rate (passes vs fixes/reopens in review/chief decisions in window)
    chief_passes = 0
    chief_fixes = 0
    for j in queue_jobs:
        is_reviewish = j.get("kind") in ("chief", "review", "qa") or "parked for chief" in str(j.get("result") or "").lower()
        for t, _by, what in _job_events(j):
            if not (start <= t <= now):
                continue
            low = what.lower()
            if low.startswith("reopened:") and (is_reviewish or FIX_RE.search(low)):
                chief_fixes += 1
            elif low.startswith("done:") and is_reviewish:
                if FIX_RE.search(low) and not PASS_RE.search(low):
                    chief_fixes += 1
                elif PASS_RE.search(low):
                    chief_passes += 1
    chief_total = chief_passes + chief_fixes
    chief_fix_rate_pct = round(100.0 * chief_fixes / chief_total, 1) if chief_total else None

    # 5. Time from job to Ben-watch (hours from earliest job on a film to Ben-watch handoff)
    film_first_job: dict[str, dt.datetime] = {}
    film_ben_watch: dict[str, dt.datetime] = {}
    for j in queue_jobs:
        keys = channels.film_keys(f"{j.get('title') or ''} {j.get('film') or ''}")
        if not keys and j.get("film"):
            lbl = channels.label_of_repo(j.get("repo"))
            keys = {f"{lbl}:{j['film']}"}
        if not keys:
            continue
        events = _job_events(j)
        if not events:
            continue
        first_t = events[0][0]
        for fk in keys:
            if fk not in film_first_job or first_t < film_first_job[fk]:
                film_first_job[fk] = first_t
        is_ben_job = bool(j.get("awaits_ben")) or j.get("needs") == "ben" or bool(BEN_WATCH_RE.search(str(j.get("title") or "")))
        if is_ben_job:
            for fk in keys:
                if fk not in film_ben_watch or first_t > film_ben_watch[fk]:
                    film_ben_watch[fk] = first_t
        else:
            for t, _by, what in events:
                if BEN_WATCH_RE.search(what):
                    for fk in keys:
                        if fk not in film_ben_watch or t > film_ben_watch[fk]:
                            film_ben_watch[fk] = t

    watch_durations_h = []
    for fk, bw_t in film_ben_watch.items():
        if fk in film_first_job and bw_t >= film_first_job[fk]:
            # Prefer films reaching Ben-watch in the last 30 days so the metric stays current
            if now - bw_t <= dt.timedelta(days=30):
                watch_durations_h.append(round((bw_t - film_first_job[fk]).total_seconds() / 3600.0, 1))
    median_to_ben_h = round(statistics.median(watch_durations_h), 1) if watch_durations_h else None

    # 6. Credit spend per finished film
    spend_by_film: dict[str, dict[str, float]] = collections.defaultdict(lambda: collections.defaultdict(float))
    for row in spend_rows if spend_rows is not None else _load_spend_rows():
        if row.get("kind") != "spend":
            continue
        film = str(row.get("film") or "").strip()
        pool = str(row.get("pool") or "").strip()
        amount = row.get("amount")
        if not film or not pool or not isinstance(amount, (int, float)) or isinstance(amount, bool):
            continue
        spend_by_film[film][pool] += float(amount)

    finished_films = {fk for fk in film_ben_watch} | {fk for fk in spend_by_film if fk in film_first_job}
    pool_totals: dict[str, list[float]] = collections.defaultdict(list)
    for fk in sorted(finished_films):
        for pool, total in (spend_by_film.get(fk) or {}).items():
            if total > 0:
                pool_totals[pool].append(total)
    spend_per_film = {
        pool: round(statistics.mean(vals), 1)
        for pool, vals in sorted(pool_totals.items())
        if vals
    }

    metrics = {
        "window_days": window_days,
        "done_7d_total": done_total,
        "done_7d_by_machine": done_counts,
        "jobs_per_day_by_machine": jobs_per_day,
        "jobs_per_day_total": round(done_total / float(window_days), 2),
        "idle_agent_hours_with_ready_work": idle_info["idle_hours_zero_active"],
        "ready_work_hours": idle_info["ready_work_hours"],
        "stalls_7d": stalls_7d,
        "parks_7d": parks_7d,
        "chief_parks_7d": chief_parks_7d,
        "currently_parked_for_chief": currently_parked,
        "chief_fix_rate_pct": chief_fix_rate_pct,
        "chief_passes_7d": chief_passes,
        "chief_fixes_7d": chief_fixes,
        "median_job_to_ben_watch_h": median_to_ben_h,
        "ben_watch_films_30d": len(watch_durations_h),
        "credit_spend_per_finished_film": spend_per_film,
        "films_with_spend": len([fk for fk in finished_films if spend_by_film.get(fk)]),
    }

    bottleneck = diagnose_bottleneck(metrics)
    metrics_line = (
        f"{metrics['jobs_per_day_total']:.1f} jobs/day "
        f"(Mini {jobs_per_day.get('mini', 0):.1f}, MacBook {jobs_per_day.get('macbook', 0):.1f}) · "
        f"{metrics['idle_agent_hours_with_ready_work']} idle h with ready work · "
        f"{stalls_7d} stalls, {parks_7d} parks"
        + (f" · Chief FIX rate {chief_fix_rate_pct:.0f}%" if chief_fix_rate_pct is not None else "")
    )

    return {
        "schema_version": 1,
        "measured_at": studio.iso(now),
        "metrics": metrics,
        "bottleneck": bottleneck,
        "metrics_line": metrics_line,
    }


def diagnose_bottleneck(metrics: dict) -> dict:
    """Rank operational failure modes and name the single biggest bottleneck with a concrete £0 fix."""
    candidates: list[tuple[float, dict]] = []

    idle_h = int(metrics.get("idle_agent_hours_with_ready_work") or 0)
    if idle_h >= 6:
        candidates.append((
            idle_h * 2.0,
            {
                "key": "idle_dispatch",
                "title": "Agents sitting idle while ready jobs wait",
                "metric_key": "idle_agent_hours_with_ready_work",
                "metric_value": idle_h,
                "lower_is_better": True,
                "summary": f"Workers were idle for {idle_h} hours in the last {metrics.get('window_days', 7)} days while ready jobs waited in the queue.",
                "proposed_fix": "Audit relay dispatch concurrency, fallback rerouting, and worker heartbeats so ready jobs are claimed immediately.",
                "fix_kind": "assembly",
            },
        ))

    stalls = int(metrics.get("stalls_7d") or 0)
    if stalls >= 3:
        candidates.append((
            stalls * 5.0,
            {
                "key": "worker_stalls",
                "title": "Frequent job stalls and timeouts",
                "metric_key": "stalls_7d",
                "metric_value": stalls,
                "lower_is_better": True,
                "summary": f"{stalls} stalls or timeouts recorded in the last {metrics.get('window_days', 7)} days.",
                "proposed_fix": "Inspect the stalled jobs' agent/model mix and split over-sized jobs or tighten lease/retry handling.",
                "fix_kind": "assembly",
            },
        ))

    parks = int(metrics.get("currently_parked_for_chief") or 0)
    chief_parks = int(metrics.get("chief_parks_7d") or 0)
    if parks >= 5 or chief_parks >= 10:
        score = max(parks * 4.0, chief_parks * 1.5)
        candidates.append((
            score,
            {
                "key": "chief_park_backlog",
                "title": "Jobs piling up waiting for Chief review",
                "metric_key": "currently_parked_for_chief",
                "metric_value": parks,
                "lower_is_better": True,
                "summary": f"{parks} jobs are parked for Chief right now ({chief_parks} parked in the last 7 days).",
                "proposed_fix": "Tune Chief review batching, escalation cadence, and pre-flight self-checks so fewer routine jobs park.",
                "fix_kind": "review",
            },
        ))

    fix_rate = metrics.get("chief_fix_rate_pct")
    if fix_rate is not None and fix_rate >= 30.0 and (metrics.get("chief_fixes_7d") or 0) >= 2:
        candidates.append((
            fix_rate * 0.9,
            {
                "key": "high_chief_fix_rate",
                "title": "High Chief FIX rate on submitted work",
                "metric_key": "chief_fix_rate_pct",
                "metric_value": fix_rate,
                "lower_is_better": True,
                "summary": f"Chief requested fixes on {fix_rate:.1f}% of reviewed jobs ({metrics.get('chief_fixes_7d')} fixes vs {metrics.get('chief_passes_7d')} passes).",
                "proposed_fix": "Promote the top recurring Chief FIX reasons into automated pre-submission checks and generator templates.",
                "fix_kind": "review",
            },
        ))

    ben_h = metrics.get("median_job_to_ben_watch_h")
    if ben_h is not None and ben_h >= 120.0:
        candidates.append((
            ben_h / 4.0,
            {
                "key": "slow_to_ben_watch",
                "title": "Long wait from first film job to Ben's watch",
                "metric_key": "median_job_to_ben_watch_h",
                "metric_value": ben_h,
                "lower_is_better": True,
                "summary": f"Median time from first job to Ben-watch handoff is {ben_h:.0f} hours across {metrics.get('ben_watch_films_30d')} recent films.",
                "proposed_fix": "Identify the slowest stage handoff between script, VO, picture and edit and remove manual wait gaps.",
                "fix_kind": "review",
            },
        ))

    if not candidates:
        return {
            "key": "throughput_steady",
            "title": "Throughput steady — focus on higher output per day",
            "metric_key": "jobs_per_day_total",
            "metric_value": metrics.get("jobs_per_day_total", 0.0),
            "lower_is_better": False,
            "summary": f"No acute stall or idle spike ({metrics.get('jobs_per_day_total', 0):.1f} jobs/day across all machines).",
            "proposed_fix": "Review weekly job mix to shift more repeatable work to fast local/MacBook lanes.",
            "fix_kind": "review",
        }
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def compare_previous(current: dict, history: list[dict]) -> dict:
    """Compare this week's measurement against last week's named bottleneck to prove whether the fix helped."""
    if not history:
        return {
            "verdict": "first_measurement",
            "plain": "First weekly ops baseline recorded; next week will verify whether this fix helped.",
        }
    prev = history[-1]
    prev_bn = prev.get("bottleneck") or {}
    metric_key = prev_bn.get("metric_key")
    prev_val = prev_bn.get("metric_value")
    curr_val = (current.get("metrics") or {}).get(metric_key) if metric_key else None
    lower_is_better = prev_bn.get("lower_is_better", True)
    if prev_val is None or curr_val is None:
        return {
            "verdict": "inconclusive",
            "previous_bottleneck": prev_bn.get("title") or "",
            "plain": f"Last week's bottleneck ({prev_bn.get('title') or 'unknown'}) could not be re-measured this week.",
        }
    delta = round(float(curr_val) - float(prev_val), 2)
    improved = (delta < 0) if lower_is_better else (delta > 0)
    worsened = (delta > 0) if lower_is_better else (delta < 0)
    verdict = "helped" if improved else ("worse" if worsened else "unchanged")
    arrow = "down" if delta < 0 else ("up" if delta > 0 else "flat")
    plain = (
        f"Last week's bottleneck ({prev_bn.get('title')}): "
        f"{prev_val} → {curr_val} ({arrow}, {verdict})."
    )
    return {
        "verdict": verdict,
        "previous_bottleneck": prev_bn.get("title") or "",
        "metric_key": metric_key,
        "previous_value": prev_val,
        "current_value": curr_val,
        "delta": delta,
        "plain": plain,
    }


def render_markdown(report: dict) -> str:
    m = report["metrics"]
    bn = report["bottleneck"]
    cmp = report.get("previous_comparison") or {}
    lines = [
        f"# Studio Ops Loop — {report['measured_at'][:10]}",
        "",
        f"Measured at: `{report['measured_at']}` (trailing {m['window_days']} days).",
        "",
        "## Six weekly metrics",
        "",
        f"1. **Jobs done per day per machine:** total **{m['jobs_per_day_total']}/day** ({m['done_7d_total']} in 7d) — "
        + ", ".join(f"{k}: {v}/day" for k, v in m["jobs_per_day_by_machine"].items()),
        f"2. **Idle agent-hours with ready work:** **{m['idle_agent_hours_with_ready_work']} h** (out of {m['ready_work_hours']} ready-work hours)",
        f"3. **Stall and park counts:** **{m['stalls_7d']} stalls**, **{m['parks_7d']} parks** ({m['chief_parks_7d']} parked for Chief in 7d; {m['currently_parked_for_chief']} currently parked)",
        f"4. **Chief FIX rate:** **{m['chief_fix_rate_pct']}%** ({m['chief_fixes_7d']} fixes / {m['chief_passes_7d']} passes)"
        if m["chief_fix_rate_pct"] is not None else "4. **Chief FIX rate:** no Chief verdicts in window",
        f"5. **Time from job to Ben-watch:** median **{m['median_job_to_ben_watch_h']} h** ({m['ben_watch_films_30d']} recent films)"
        if m["median_job_to_ben_watch_h"] is not None else "5. **Time from job to Ben-watch:** no films reached Ben-watch in window",
        "6. **Credit spend per finished film:** "
        + (", ".join(f"{pool}: {val}" for pool, val in m["credit_spend_per_finished_film"].items())
           or "no recorded spend on finished films"),
        "",
        "## Single biggest bottleneck",
        "",
        f"- **Bottleneck:** {bn['title']}",
        f"- **Evidence:** {bn['summary']}",
        f"- **Queued fix:** {bn['proposed_fix']}",
        "",
        "## Did last week's fix help?",
        "",
        f"- {cmp.get('plain') or 'No prior measurement.'}",
        "",
    ]
    return "\n".join(lines)


def queue_bottleneck_fix(queue_data: dict, report: dict, at: dt.datetime) -> str | None:
    """Queue one deduplicated £0 fix job for the named bottleneck (never duplicates an open/claimed/blocked fix)."""
    bn = report.get("bottleneck") or {}
    key = str(bn.get("key") or "")
    if not key or key == "throughput_steady":
        return None
    tag = f"ops-fix:{key}"
    for j in queue_data.get("jobs") or []:
        if j.get("ops_bottleneck") == tag and j.get("status") in ("open", "claimed", "blocked"):
            return None
    title = f"Ops loop fix: {bn['title']}"
    body = (
        f"Weekly Studio Ops Loop ({report['measured_at'][:10]}) named this as the studio's single biggest bottleneck.\n\n"
        f"**Evidence:** {bn['summary']}\n"
        f"**Metrics:** {report['metrics_line']}\n"
        f"**Fix:** {bn['proposed_fix']}\n\n"
        f"**Guards:** £0. Never change Ben's gates, the never-list, money, or any channel's direction. "
        f"Open a PR for the Chief with tests; next week's ops loop will re-measure `{bn.get('metric_key')}` to prove it helped."
    )
    job = jobs.do_add(
        queue_data,
        title=title,
        needs="any",
        body=body,
        by="ops-loop",
        at=at,
        repo=channels.default(),
        eta_min=60,
        kind=str(bn.get("fix_kind") or "review"),
        action=f"Fix ops bottleneck: {bn['title']}"[:180],
    )
    job["ops_bottleneck"] = tag
    return job["id"]


def write_outputs(report: dict, out_dir: pathlib.Path | None = None) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    d = out_dir or ops_dir()
    d.mkdir(parents=True, exist_ok=True)
    latest = d / "latest.json"
    history = d / "history.jsonl"
    md = d / f"OPS_{report['measured_at'][:10]}.md"
    latest.write_text(json.dumps(report, indent=2) + "\n")
    with history.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(report) + "\n")
    md.write_text(render_markdown(report))
    return latest, history, md


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("measure", "run"):
        p = sub.add_parser(name)
        p.add_argument("--as-of", default="")
        if name == "run":
            p.add_argument("--write", action="store_true")
            p.add_argument("--queue-fix", action="store_true")

    a = ap.parse_args(argv)
    now = _parse_ts(a.as_of) if a.as_of else dt.datetime.now(UTC)
    queue = jobs.load()
    history = _load_history()
    report = measure(queue, as_of=now)
    report["previous_comparison"] = compare_previous(report, history)

    if a.cmd == "measure":
        print(json.dumps(report, indent=2))
        return 0

    if a.write:
        latest, _hist, md = write_outputs(report)
        print(f"Wrote {latest} and {md}")
    if a.queue_fix:
        jid = queue_bottleneck_fix(queue, report, now)
        if jid:
            jobs.save(queue)
            jobs.JOBS_MD.write_text(jobs.render(queue, now))
            print(f"Queued bottleneck fix job {jid}: {report['bottleneck']['title']}")
        else:
            print("No new bottleneck fix queued (steady or already open).")
    if not a.write and not a.queue_fix:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
