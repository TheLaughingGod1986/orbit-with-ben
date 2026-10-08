#!/usr/bin/env python3
"""Daily AI credit readings for the AI spend month (J0052, Ben 8 Oct 2026). Runs on the Mini at 08:30 London.

  python3 scripts/ai_spend_daily.py --dry-run          # read every pool, print, record nothing
  python3 scripts/ai_spend_daily.py --git              # read and record one `ai_spend.py record` per pool, push
  python3 scripts/ai_spend_daily.py --pools elevenlabs,vertex --git

Pools:
- elevenlabs: API `/v1/user/subscription` (character_count / character_limit). Key via el_client; never printed.
- flow:       the Flow page in the Mini's CDP Chrome (:9222), "N credits" text, as the HOS mint scripts read it.
- vertex:     Cloud Billing > Credits (all) in the same Chrome. Free Trial is `--left`; every credit line goes in --note.
- cursor:     cursor.com dashboard usage page in the same Chrome: included usage left this cycle, in USD.

A pool whose read fails records nothing; the reason goes to the log (and stdout). Never guess a number.
Log: ~/Library/Logs/owb-ai-spend.log (launchd). Exit 0 if every pool read, 1 if any failed.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "04_Audio" / "tools"
CDP = "http://127.0.0.1:9222"
BILLING_URL = "https://console.cloud.google.com/billing/0124D1-E6EFD6-40F6DA/credits/all?project=gen-lang-client-0538779324"
FLOW_URL = "https://flow.google.com/"
CURSOR_URL = "https://cursor.com/dashboard?tab=usage"
ALL = ("elevenlabs", "flow", "vertex", "cursor")


def read_elevenlabs() -> dict:
    sys.path.insert(0, str(TOOLS))
    from el_auth import load_token  # noqa: E402
    from vo_take import credits  # noqa: E402
    token, mode = load_token(prefer_api_key=True)
    c = credits(token, mode)
    if c["remaining"] is None:
        raise RuntimeError("subscription response had no character_count/character_limit")
    return {"left": c["remaining"], "total": c["limit"], "note": f"API subscription: used {c['used']} of {c['limit']}"}


def _page_text(url: str, wait_text: str | None, settle_ms: int = 3000) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp(CDP)
        page = br.contexts[0].new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            if wait_text:
                page.get_by_text(wait_text).first.wait_for(timeout=45000)
            page.wait_for_timeout(settle_ms)
            return page.inner_text("body")
        finally:
            page.close()


def parse_flow(text: str) -> int:
    hits = [int(m.group(1).replace(",", "")) for m in re.finditer(r"([\d,]{1,7})\s*(?:Google\s+Flow\s+|AI\s+)?credits", text, re.I)]
    if not hits:
        raise RuntimeError("no 'N credits' text on the Flow page (signed out, or the picker moved)")
    return hits[0]


def read_flow() -> dict:
    text = _page_text(FLOW_URL, None, settle_ms=8000)
    if re.search(r"sign in to continue|you.?re not signed in", text, re.I):
        raise RuntimeError("Flow is signed out in the CDP Chrome")
    return {"left": parse_flow(text), "note": "Flow page credits (CDP :9222)"}


def parse_billing(text: str) -> tuple[float, str]:
    rows = [ln.strip() for ln in text.splitlines() if ln.strip()]
    lines, trial = [], None
    for i, ln in enumerate(rows):
        if re.fullmatch(r"(Free Trial|.*Developer Program.*|.*credit.*)", ln, re.I) and len(ln) < 60:
            window = " ".join(rows[i:i + 8])
            m = re.search(r"£([\d,]+\.\d\d)", window)
            if not m or ln.lower().startswith("credit application type"):
                continue
            amt = float(m.group(1).replace(",", ""))
            status = "Available" if "Available" in window else ("Expired" if "Expired" in window else "?")
            lines.append(f"{ln}: £{amt:.2f} {status}")
            if ln == "Free Trial" and status == "Available" and trial is None:
                trial = amt
    if trial is None:
        raise RuntimeError("could not read an Available Free Trial row on Cloud Billing > Credits")
    return trial, "; ".join(dict.fromkeys(lines))


def read_vertex() -> dict:
    trial, lines = parse_billing(_page_text(BILLING_URL, "Free Trial", settle_ms=2500))
    return {"left": trial, "note": f"Cloud Billing > Credits: {lines}"}


def parse_cursor(text: str) -> tuple[float, float | None]:
    # e.g. "$12.34 of $20 included usage used" / "Included usage ... $7.66 remaining"
    m = re.search(r"\$([\d,]+(?:\.\d+)?)\s*(?:/|of)\s*\$([\d,]+(?:\.\d+)?)", text)
    if m:
        used, total = float(m.group(1).replace(",", "")), float(m.group(2).replace(",", ""))
        return round(total - used, 2), total
    m = re.search(r"\$([\d,]+(?:\.\d+)?)\s*(?:left|remaining)", text, re.I)
    if m:
        return float(m.group(1).replace(",", "")), None
    raise RuntimeError("no included-usage dollar figure on the Cursor dashboard (signed out, or the page changed)")


def read_cursor() -> dict:
    text = _page_text(CURSOR_URL, None, settle_ms=8000)
    if re.search(r"\bsign in\b|\blog in\b", text[:2000], re.I) and "$" not in text:
        raise RuntimeError("Cursor dashboard is signed out in the CDP Chrome")
    left, total = parse_cursor(text)
    return {"left": left, "total": total, "note": "Cursor dashboard included usage (CDP :9222)"}


READERS = {"elevenlabs": read_elevenlabs, "flow": read_flow, "vertex": read_vertex, "cursor": read_cursor}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pools", default=",".join(ALL))
    ap.add_argument("--by", default="mini-daily")
    ap.add_argument("--git", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    failed = 0
    for pool in [p.strip() for p in a.pools.split(",") if p.strip()]:
        try:
            r = READERS[pool]()
        except Exception as e:  # one pool failing never blocks the others
            failed += 1
            print(f"FAIL {pool}: {type(e).__name__}: {str(e)[:300]}", flush=True)
            continue
        print(f"READ {pool}: left={r['left']} total={r.get('total')} · {r['note']}", flush=True)
        if a.dry_run:
            continue
        cmd = [sys.executable, str(ROOT / "scripts" / "ai_spend.py"), "record", "--pool", pool,
               "--left", str(r["left"]), "--note", r["note"], "--by", a.by]
        if r.get("total") is not None:
            cmd += ["--total", str(r["total"])]
        if a.git:
            cmd.append("--git")
        if subprocess.run(cmd, cwd=ROOT).returncode != 0:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
