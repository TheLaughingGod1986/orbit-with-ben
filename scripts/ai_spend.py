#!/usr/bin/env python3
"""AI spend ledger for both channels (Ben, 8 Oct 2026): how much credit we have, how much we use, and on what.

Each subscription plan is measured across its own billing cycle (05_Analytics/ai_spend/plans.json), with weekly
usage history retained across weeks so weekly-limit plans (Claude, Codex, Cursor/Grok, Gemini) can be judged on
how often they hit their weekly limit and their average weekly use across the billing month (J2985, 17 Nov 2026).

  python3 scripts/ai_spend.py record --pool flow --left 12500 --total 12500 --by cursor --note "12 Oct refill"
  python3 scripts/ai_spend.py record --pool vertex --left 25.59 --by cursor --note "Cloud Billing > Credits"
  python3 scripts/ai_spend.py spend --pool flow --amount 100 --film HOS:006 --what "P3:04 Quality take 1" --by cursor
  python3 scripts/ai_spend.py spend --pool vertex --amount 1.60 --film OWB:025 --what "orbit_mars_cold_omni_v01" --by cursor
  python3 scripts/ai_spend.py report            # each pool's current cycle and spend per film
  python3 scripts/ai_spend.py doc               # the board/credits document (JSON) the Kanban page reads
"""
from __future__ import annotations

import argparse
import calendar
import fcntl
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channels  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DIR = channels.studio_records("ai_spend")
LEDGER = DIR / "ledger.jsonl"
PLANS = DIR / "plans.json"
POOLS = {"cursor": "%", "flow": "credits", "vertex": "GBP", "elevenlabs": "credits", "claude": "%",
         "codex": "%", "codex-macbook": "%", "gemini": "%"}
WEEKLY_POOLS = {"cursor", "claude", "codex", "codex-macbook", "gemini"}
RESET_NOTE_RE = re.compile(
    r"(?:weekly[^;]*?resets?|resets?)\s+(?:on\s+|at\s+)?"
    r"((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*\s+\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"|(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*\s+[\d:]+(?:\s*[AP]M|Z)?"
    r"|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})",
    re.I,
)
SPLIT_NOTE_RE = re.compile(r"Weekly included usage\s+\d{1,3}%\s+used\s*\(([^)]+)\)", re.I)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_iso(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _clamp_day(year: int, month: int, day: int) -> date:
    return date(year, month, min(day, calendar.monthrange(year, month)[1]))


def _shift_month(year: int, month: int, delta: int) -> tuple[int, int]:
    total = (year * 12 + (month - 1)) + delta
    return total // 12, (total % 12) + 1


def rolling_cycle(billing_day: int, ref: date) -> tuple[str, str]:
    """(cycleStart YYYY-MM-DD, renews YYYY-MM-DD) around `ref` for a plan that bills on `billing_day`."""
    this_month_start = _clamp_day(ref.year, ref.month, billing_day)
    if ref >= this_month_start:
        ny, nm = _shift_month(ref.year, ref.month, 1)
        return this_month_start.isoformat(), _clamp_day(ny, nm, billing_day).isoformat()
    py, pm = _shift_month(ref.year, ref.month, -1)
    return _clamp_day(py, pm, billing_day).isoformat(), this_month_start.isoformat()


def plan_cycles(plans: dict, ref: date) -> dict[str, dict]:
    """Map each pool id to its subscription metadata and active cycle around `ref`."""
    out: dict[str, dict] = {}
    subs = plans.get("subscriptions") or []
    legacy_starts = plans.get("poolStarts") or {}
    legacy_start = (plans.get("period") or {}).get("start") or "2026-10-08"
    for sub in subs:
        pools = sub.get("pools") or []
        bday = sub.get("billingDay") if sub.get("billingVerified") is not False else None
        c_start = (sub.get("cycleStart") or "") if sub.get("billingVerified") is not False else ""
        c_renews = (sub.get("renews") or "") if sub.get("billingVerified") is not False else ""
        if bday:
            # Use explicit cycleStart/renews when `ref` sits inside them; otherwise roll cleanly by billingDay.
            try:
                if c_start and c_renews and date.fromisoformat(c_start) <= ref < date.fromisoformat(c_renews):
                    start_s, renews_s = c_start, c_renews
                else:
                    start_s, renews_s = rolling_cycle(int(bday), ref)
            except ValueError:
                start_s, renews_s = rolling_cycle(int(bday), ref)
        elif c_start and c_renews:
            start_s, renews_s = c_start, c_renews
        else:
            # No billing renewal date on file (e.g. ChatGPT Pro on Mini): keep 30 days of readings in window,
            # while leaving `renews` empty so the board states honestly that the billing renewal date is unread.
            start_s = (ref - timedelta(days=int(plans.get("cycleDays") or 30))).isoformat()
            renews_s = ""
        for p in pools:
            out[p] = {
                "planId": sub.get("id") or p,
                "planName": sub.get("name") or p,
                "gbp": sub.get("gbp"),
                "currentGbp": sub.get("currentGbp"),
                "currentTier": sub.get("currentTier") or "",
                "start": start_s,
                "renews": renews_s,
                "billingDay": bday,
                "historyScope": "billing cycle" if renews_s else "rolling 30 days",
                "billingNote": sub.get("billingNote") or "",
                "usageNote": sub.get("usageNote") or "",
                "next": sub.get("next") or "",
            }
    if "codex" in out and "codex-macbook" not in out:
        out["codex-macbook"] = dict(out["codex"])
    for p in POOLS:
        if p not in out:
            s = legacy_starts.get(p) or legacy_start
            out[p] = {"planId": p, "planName": p, "gbp": None, "start": s, "renews": "", "billingDay": None,
                      "billingNote": "", "usageNote": "", "next": ""}
    return out


def _refill_cutoff(pool_rows: list[dict], cycle_start_iso: str, unit: str = "credits") -> str:
    """When a monthly credit refill lands hours after midnight on/after `cycleStart` (e.g. Flow or Vertex refilling
    on 12–13 Nov, read 13 Nov 08:30Z), start the new cycle at that refill so pre-refill tail spend stays in the old cycle."""
    start_dt = _parse_iso(cycle_start_iso + "T00:00:00Z")
    if not start_dt:
        return cycle_start_iso
    window_end = start_dt + timedelta(hours=48)
    min_jump = 20.0 if unit == "GBP" else 1000.0
    bal = [r for r in pool_rows if r.get("kind") == "record" and r.get("left") is not None]
    in_early = [r for r in bal if (dt := _parse_iso(r.get("at", ""))) and start_dt <= dt <= window_end]
    for i in range(1, len(in_early)):
        prev_left = float(in_early[i - 1]["left"])
        cur_left = float(in_early[i]["left"])
        if cur_left - prev_left > max(min_jump, prev_left * 0.5):
            return in_early[i]["at"]
    return cycle_start_iso


def _past_cycle_max_used(pool: str, unit: str, all_rows: list[dict], cutoff_at: str, billing_day: int | None, cur_start_iso: str = "") -> float | None:
    """Highest credit consumption observed in any completed cycle before `cutoff_at`."""
    if unit == "%" or not billing_day:
        return None
    prior = [r for r in all_rows if r.get("pool") == pool and r.get("kind") == "record"
             and r.get("left") is not None and r.get("at", "") < cutoff_at]
    if not prior:
        return None
    cur_start_date = date.fromisoformat(cur_start_iso) if len(cur_start_iso) == 10 else None
    by_cycle: dict[str, list[dict]] = defaultdict(list)
    for r in prior:
        dt = _parse_iso(r.get("at", ""))
        if not dt:
            continue
        d_key = (cur_start_date - timedelta(days=1)) if (cur_start_date and dt.date() >= cur_start_date) else dt.date()
        c_start, _ = rolling_cycle(billing_day, d_key)
        by_cycle[c_start].append(r)
    best = 0.0
    jump = 20.0 if unit == "GBP" else 1000.0
    for c_rows in by_cycle.values():
        # Handle late refill inside an older cycle too: measure from peak balance in that cycle
        # (or explicit `total`) down to minimum subsequent balance before the next refill.
        peak = 0.0
        cycle_used = 0.0
        for r in c_rows:
            left = float(r["left"])
            tot = float(r["total"]) if r.get("total") is not None else None
            if left > peak + jump:
                peak = max(left, tot or 0.0)
            else:
                peak = max(peak, left, tot or 0.0)
            used_here = (tot - left) if tot is not None else (peak - left)
            if used_here > cycle_used:
                cycle_used = used_here
        if cycle_used > best:
            best = cycle_used
    return round(best, 2) if best > 0 else None


MONTH_NUM = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
             "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}


def _norm_reset_tag(raw: str) -> str:
    """Canonicalize 'Nov 12', '12 Nov', and 'Thu 12 Nov' to '12-11' so format changes don't split one week."""
    s = re.sub(r"\s+", " ", raw.strip())
    m1 = re.search(r"\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", s, re.I)
    if m1:
        return f"{int(m1.group(1)):02d}-{MONTH_NUM[m1.group(2).lower()]}"
    m2 = re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})\b", s, re.I)
    if m2:
        return f"{int(m2.group(2)):02d}-{MONTH_NUM[m2.group(1).lower()]}"
    return s.lower()


def _weekly_reset(note: str, at: datetime) -> datetime | None:
    """Resolve provider wall time against the reading, never against today's date."""
    m = re.search(r"(?:weekly[^;]*?resets?|resets?)\s+(?:on\s+|at\s+)?([^;()]+)", note, re.I)
    if not m:
        return None
    raw = m.group(1).strip()
    zone = timezone.utc if re.search(r"Z\b|UTC|GMT", raw) else ZoneInfo("Europe/London")
    ref = at.astimezone(zone)
    clock = re.search(r"(\d{1,2}):(\d{2})\s*([AP]M)?", raw, re.I)
    h, minute = (int(clock[1]), int(clock[2])) if clock else (0, 0)
    if clock and clock[3]:
        h = h % 12 + (12 if clock[3].upper() == "PM" else 0)
    dm = re.search(r"(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:\s+(20\d{2}))?", raw, re.I)
    md = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2})(?:\s+(20\d{2}))?", raw, re.I)
    if dm or md:
        day, mon, year = (int(dm[1]), MONTH_NUM[dm[2].lower()[:3]], dm[3]) if dm else (int(md[2]), MONTH_NUM[md[1].lower()[:3]], md[3])
        years = [int(year)] if year else [ref.year - 1, ref.year, ref.year + 1]
        candidates = [datetime(y, mon, day, h, minute, tzinfo=zone) for y in years]
        return min(candidates, key=lambda d: abs((d-ref).total_seconds())).astimezone(timezone.utc)
    wd = re.match(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*", raw, re.I)
    if wd and clock:
        target = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].index(wd[1].lower())
        end = ref.replace(hour=h, minute=minute, second=0, microsecond=0) + timedelta(days=(target-ref.weekday()) % 7)
        if end < ref:
            end += timedelta(days=7)
        return end.astimezone(timezone.utc)
    return None


def _weekly_history(pool: str, all_rows: list[dict], cycle_start_iso: str) -> list[dict]:
    """Observed weekly peaks, with absolute reset boundaries and explicitly partial coverage."""
    if pool not in WEEKLY_POOLS:
        return []
    weeks = {}
    for r in sorted(all_rows, key=lambda r: r.get("at", "")):
        if r.get("pool") != pool or r.get("kind") != "record":
            continue
        dt = _parse_iso(r.get("at", ""))
        if not dt:
            continue
        note = str(r.get("note") or "")
        exhausted = bool(re.search(r"(?:hit (?:the |its )?weekly limit|weekly (?:limit )?exhausted)", note, re.I))
        if r.get("left") is None and not exhausted:
            continue
        used = 100.0 if exhausted else round(max(0.0, 100.0-float(r["left"])), 1)
        end = _weekly_reset(note, dt)
        # Unknown resets are separate observations, never claimed to be complete weeks.
        key = end.isoformat() if end else dt.isoformat()
        quota = r.get("quotaId")
        key = (key, quota)
        w = weeks.setdefault(key, {"firstAt": r["at"], "peakUsed": 0, "hitLimit": False,
                                  "partial": True, "quotaId": quota, "historyBasis": "verified" if quota else "unknown"})
        w.update(at=r["at"])
        w["peakUsed"] = max(w["peakUsed"], used)
        w["hitLimit"] |= used >= 100 or exhausted
        w["nearLimit"] = 94 <= w["peakUsed"] < 100
        if end:
            start = end - timedelta(days=7)
            w.update(windowStart=start.isoformat(), windowEnd=end.isoformat(), reset=key[0])
            w["inCycle"] = end.date().isoformat() > cycle_start_iso
            w["overlapsCycleStart"] = start.date().isoformat() < cycle_start_iso < end.date().isoformat()
        else:
            w["inCycle"] = r["at"][:10] >= cycle_start_iso
            w["windowUnknown"] = True
        split = SPLIT_NOTE_RE.search(note)
        if split:
            w["split"] = split[1].strip()
        if re.search(r"\bfable\s+100%\s+used\b", note, re.I):
            w["sublimitHit"] = "Fable 100%"
    return list(weeks.values())[-8:]


def load() -> list[dict]:
    if not LEDGER.exists():
        return []
    return [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]


def append(row: dict, git: bool) -> None:
    # Same destination lock as SharedFlowAccounting.export_ai_spend. Resolve
    # aliases before choosing the lock so symlinks cannot create two writers.
    target = LEDGER.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.with_name(target.name + ".lock").open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        data = target.read_bytes() if target.exists() else b""
        if data and not data.endswith(b"\n"):
            raise ValueError("torn ai_spend ledger; reconcile before append")
        existing = [json.loads(line) for line in data.splitlines() if line.strip()]
        if any(not isinstance(item, dict) for item in existing):
            raise ValueError("ai_spend ledger contains a non-object row")
        ids = [item["id"] for item in existing if "id" in item]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate ai_spend receipt identity")
        if "id" in row and row["id"] in ids:
            raise ValueError("ai_spend receipt identity already exists")
        with target.open("ab") as handle:
            handle.write((json.dumps(row, ensure_ascii=False) + "\n").encode())
            handle.flush()
            os.fsync(handle.fileno())
        directory = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    print(json.dumps(row, ensure_ascii=False))
    if git:
        msg = f"ai_spend: {row['kind']} {row['pool']} by {row.get('by') or '?'}"
        subprocess.run(["git", "-C", str(ROOT), "add", str(LEDGER)], check=True)
        subprocess.run(["git", "-C", str(ROOT), "commit", "-q", "-m", msg], check=True)
        for _ in range(3):
            if subprocess.run(["git", "-C", str(ROOT), "push", "-q", "origin", "HEAD:main"]).returncode == 0:
                return
            subprocess.run(["git", "-C", str(ROOT), "pull", "-q", "--rebase", "origin", "main"], check=True)
        sys.exit("ai_spend: push failed three times; the line is committed locally")


def build_doc(rows: list[dict], as_of: str | None = None, plans: dict | None = None) -> dict:
    if plans is None:
        plans = json.loads(PLANS.read_text()) if PLANS.exists() else {}
    all_sorted = sorted((r for r in rows if r.get("pool") in POOLS), key=lambda r: r.get("at", ""))
    ref_dt = _parse_iso(as_of) if as_of else (_parse_iso(all_sorted[-1].get("at", "")) if all_sorted else None)
    ref_date = (ref_dt or datetime.now(timezone.utc)).date()
    cycles = plan_cycles(plans, ref_date)

    monthly: dict = {}
    for row in all_sorted:
        month, pool = row.get("at", "")[:7], row.get("pool")
        if not month or pool not in POOLS:
            continue
        entry = monthly.setdefault(month, {}).setdefault(pool, {"logged": 0, "entries": 0, "unit": POOLS[pool], "latest": None})
        if row.get("kind") == "spend":
            entry["logged"] = round(entry["logged"] + float(row.get("amount") or 0), 2)
            entry["entries"] += 1
        elif row.get("kind") == "record" and row.get("left") is not None:
            entry["latest"] = {k: row.get(k) for k in ("at", "left", "total")}

    cutoffs: dict[str, str] = {}
    for pool, unit in POOLS.items():
        c = cycles[pool]
        p_rows = [r for r in all_sorted if r["pool"] == pool]
        cutoffs[pool] = _refill_cutoff(p_rows, c["start"], unit) if unit != "%" else c["start"]

    in_cycle_rows = [r for r in all_sorted if r.get("at", "") >= cutoffs[r["pool"]]]
    pools = {}
    for pool, unit in POOLS.items():
        c = cycles[pool]
        reads = [r for r in in_cycle_rows if r["pool"] == pool and r["kind"] == "record"]
        spends = [r for r in in_cycle_rows if r["pool"] == pool and r["kind"] == "spend"]
        all_pool_reads = [r for r in all_sorted if r["pool"] == pool and r["kind"] == "record"]
        # Keep latest balance even if a weekly pool hasn't been read since a brand-new cycle date rolled today.
        if not reads and not spends and not all_pool_reads:
            continue
        bal = [r for r in reads if r.get("left") is not None] or [r for r in all_pool_reads if r.get("left") is not None][-1:]
        first, last = (bal[0], bal[-1]) if bal else (None, None)
        past_max = _past_cycle_max_used(pool, unit, all_sorted, cutoffs[pool], c.get("billingDay"), c["start"])
        wk_hist = _weekly_history(pool, all_sorted, c["start"])
        entry_doc = {
            "unit": unit,
            "latest": last and {k: last.get(k) for k in ("left", "total", "at", "by", "note")},
            "first": first and {k: first.get(k) for k in ("left", "total", "at")},
            "spent_logged": round(sum(float(r.get("amount") or 0) for r in spends), 2),
            "series": [[r["at"], r.get("left")] for r in (reads or all_pool_reads[-10:]) if r.get("left") is not None][-120:],
            "notes": [{"at": r["at"], "note": r.get("note", ""), "by": r.get("by", "")} for r in (reads or all_pool_reads) if pool == "claude"][-20:],
            "since": c["start"],
            "renews": c.get("renews") or "",
        }
        if past_max is not None:
            entry_doc["pastCycleMaxUsed"] = past_max
        if wk_hist:
            entry_doc["weeklyHistory"] = wk_hist
        pools[pool] = entry_doc

    by_film: dict = defaultdict(lambda: defaultdict(float))
    for r in in_cycle_rows:
        if r["kind"] == "spend":
            by_film[r.get("film") or "(none)"][r["pool"]] += float(r.get("amount") or 0)

    return {
        "updatedAt": now(),
        "cycles": cycles,
        "plans": plans.get("subscriptions", []),
        "target": plans.get("target", {}),
        "fx": plans.get("fx", {}),
        "tiers": {k: v for k, v in plans.get("tiers", {}).items() if not k.startswith("_")},
        "cycleDays": plans.get("cycleDays", 30),
        "pricesNote": plans.get("note", ""),
        "pools": pools,
        "monthly": monthly,
        "byFilm": {f: {p: round(v, 2) for p, v in d.items()} for f, d in sorted(by_film.items())},
        "lines": len(in_cycle_rows),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record", help="a balance reading")
    r.add_argument("--pool", choices=POOLS, required=True)
    r.add_argument("--left", type=float)
    r.add_argument("--total", type=float, help="the pool's size this period, if known (e.g. the monthly refill)")
    r.add_argument("--note", default="")
    r.add_argument("--by", required=True)
    r.add_argument("--git", action="store_true")
    s = sub.add_parser("spend", help="one use of credit")
    s.add_argument("--pool", choices=POOLS, required=True)
    s.add_argument("--amount", type=float, required=True)
    s.add_argument("--film", default="", help="the film key: the channel's label, a colon, three digits (CHANNEL:NNN)")
    s.add_argument("--what", default="")
    s.add_argument("--by", required=True)
    s.add_argument("--git", action="store_true")
    sub.add_parser("report")
    sub.add_parser("doc")
    a = ap.parse_args(argv)

    if a.cmd == "record":
        if a.pool != "claude" and a.left is None:
            ap.error("--left is required for a balance reading")
        row = {"at": now(), "kind": "record", "pool": a.pool, "left": a.left, "total": a.total, "note": a.note, "by": a.by}
        append({k: v for k, v in row.items() if v not in (None, "")}, a.git)
    elif a.cmd == "spend":
        if a.film and ":" not in a.film:
            ap.error("--film is CHANNEL:NNN: the channel's label, a colon, three digits")
        append({"at": now(), "kind": "spend", "pool": a.pool, "amount": a.amount, "film": a.film, "what": a.what, "by": a.by}, a.git)
    elif a.cmd == "doc":
        print(json.dumps(build_doc(load()), ensure_ascii=False, indent=1))
    else:
        d = build_doc(load())
        print(f"Per-plan cycles · {d['lines']} in-cycle ledger lines")
        for pool, p in d["pools"].items():
            lt = p["latest"] or {}
            cyc = (d.get("cycles") or {}).get(pool) or {}
            ren = f" -> {cyc['renews']}" if cyc.get("renews") else ""
            print(f"  {pool:<10} cycle {p.get('since')}{ren} · left {lt.get('left')} {p['unit']} (of {lt.get('total')}) at {lt.get('at')} · logged spend {p['spent_logged']}")
        for film, d2 in d["byFilm"].items():
            print(f"  {film:<9} " + ", ".join(f"{p} {v}" for p, v in d2.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
