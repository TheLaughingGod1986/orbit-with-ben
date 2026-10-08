#!/usr/bin/env python3
"""AI spend ledger for both channels (Ben, 8 Oct 2026): how much credit we have, how much we use, and on what.

Ben's question for the 8 Nov check-in: can Orbit With Ben and History of Science run on a ~£90 Claude plan, a ~£90
Google plan and ElevenLabs (£20), without Cursor, Grok Bot or Codex? The month we measure starts when the Google
AI Ultra credits refill on Mon 12 Oct. Every agent that reads a balance or spends credit records it here.

  python3 scripts/ai_spend.py record --pool flow --left 12500 --total 12500 --by cursor --note "12 Oct refill"
  python3 scripts/ai_spend.py record --pool vertex --left 25.59 --by cursor --note "Cloud Billing > Credits"
  python3 scripts/ai_spend.py spend --pool flow --amount 100 --film HOS:006 --what "P3:04 Quality take 1" --by cursor
  python3 scripts/ai_spend.py spend --pool vertex --amount 1.60 --film OWB:025 --what "orbit_mars_cold_omni_v01" --by cursor
  python3 scripts/ai_spend.py report            # the month so far, per pool and per film
  python3 scripts/ai_spend.py doc               # the board/credits document (JSON) the Kanban page reads

Pools and units: flow (Flow credits), vertex (GBP of Google Cloud credit), elevenlabs (characters/credits),
claude (notes only, e.g. "hit the 5-hour limit"). `record` is a balance reading; `spend` is one use. Add --git to
commit the ledger line and push to main. Subscriptions and their prices live in 05_Analytics/ai_spend/plans.json.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "05_Analytics" / "ai_spend"
LEDGER = DIR / "ledger.jsonl"
PLANS = DIR / "plans.json"
POOLS = {"flow": "credits", "vertex": "GBP", "elevenlabs": "credits", "claude": "note"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load() -> list[dict]:
    if not LEDGER.exists():
        return []
    return [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]


def append(row: dict, git: bool) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
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


def build_doc(rows: list[dict]) -> dict:
    plans = json.loads(PLANS.read_text()) if PLANS.exists() else {}
    start = plans.get("period", {}).get("start", "2026-10-12")
    rows = [r for r in rows if r.get("at", "") >= start]
    pools = {}
    for pool, unit in POOLS.items():
        reads = [r for r in rows if r["pool"] == pool and r["kind"] == "record"]
        spends = [r for r in rows if r["pool"] == pool and r["kind"] == "spend"]
        if not reads and not spends:
            continue
        first, last = (reads[0], reads[-1]) if reads else (None, None)
        pools[pool] = {
            "unit": unit,
            "latest": last and {k: last.get(k) for k in ("left", "total", "at", "by", "note")},
            "first": first and {k: first.get(k) for k in ("left", "total", "at")},
            # Spent = what the balance readings show went down (refills counted as new totals), plus nothing double-counted:
            # spend lines are the per-film breakdown, the readings are the truth for the total.
            "spent_logged": round(sum(float(r.get("amount") or 0) for r in spends), 2),
            "series": [[r["at"], r.get("left")] for r in reads if r.get("left") is not None][-120:],
            "notes": [{"at": r["at"], "note": r.get("note", ""), "by": r.get("by", "")} for r in reads if pool == "claude"][-20:],
        }
    by_film: dict = defaultdict(lambda: defaultdict(float))
    for r in rows:
        if r["kind"] == "spend":
            by_film[r.get("film") or "(none)"][r["pool"]] += float(r.get("amount") or 0)
    return {
        "updatedAt": now(),
        "period": plans.get("period", {"start": start}),
        "plans": plans.get("subscriptions", []),
        "target": plans.get("target", {}),
        "fx": plans.get("fx", {}),
        "pricesNote": plans.get("note", ""),
        "pools": pools,
        "byFilm": {f: {p: round(v, 2) for p, v in d.items()} for f, d in sorted(by_film.items())},
        "lines": len(rows),
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
    s.add_argument("--film", default="", help="CHANNEL:NNN, e.g. HOS:006 or OWB:025")
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
            ap.error("--film is CHANNEL:NNN, e.g. HOS:006")
        append({"at": now(), "kind": "spend", "pool": a.pool, "amount": a.amount, "film": a.film, "what": a.what, "by": a.by}, a.git)
    elif a.cmd == "doc":
        print(json.dumps(build_doc(load()), ensure_ascii=False, indent=1))
    else:
        d = build_doc(load())
        print(f"Period from {d['period'].get('start')} · {d['lines']} ledger lines")
        for pool, p in d["pools"].items():
            lt = p["latest"] or {}
            print(f"  {pool:<10} left {lt.get('left')} {p['unit']} (of {lt.get('total')}) at {lt.get('at')} · logged spend {p['spent_logged']}")
        for film, d2 in d["byFilm"].items():
            print(f"  {film:<9} " + ", ".join(f"{p} {v}" for p, v in d2.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
