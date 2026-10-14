#!/usr/bin/env python3
"""Daily AI credit readings for the AI spend month (J0052, Ben 8 Oct 2026). Runs on the Mini at 08:30 London.

  python3 scripts/ai_spend_daily.py --dry-run          # read every pool, print, record nothing
  python3 scripts/ai_spend_daily.py --git              # read and record one `ai_spend.py record` per pool, push
  python3 scripts/ai_spend_daily.py --pools elevenlabs,vertex --git

Pools:
- elevenlabs: API `/v1/user/subscription` (character_count / character_limit). Key via el_client; never printed.
- flow:       the Flow page in the Mini's CDP Chrome (:9222), "N credits" text, as the HOS mint scripts read it.
- vertex:     Cloud Billing > Credits (all) in the same Chrome. Free Trial is `--left`; every credit line goes in --note.
- cursor:     cursor.com/dashboard/spending in the same Chrome: percent of the Cursor Models pool left this cycle
              (the page shows % used per pool and no $ since 12 Oct); Cursor Models and Grok Bot weekly go in --note.

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
CURSOR_URL = "https://cursor.com/dashboard/spending"
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


def _page_text(url: str, wait_text: str | None, settle_ms: int = 3000, then=None) -> str:
    """Body text of `url` in the CDP Chrome. `then(page, text)` may click and return new text."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp(CDP)
        page = br.contexts[0].new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            if wait_text:
                page.get_by_text(wait_text).first.wait_for(timeout=45000)
            page.wait_for_timeout(settle_ms)
            text = page.inner_text("body")
            return then(page, text) if then else text
        finally:
            page.close()


FLOW_ACCOUNT = "benoats@googlemail.com"
# The account chip that opens the picker with the credit count, as the HOS Flow minters click it.
FLOW_PICKER = ('[aria-label*="Account details" i]', '[aria-label*="Google Account" i]',
               'button:has-text("ULTRA")', "text=ULTRA")
CREDITS_RE = re.compile(r"([\d,]{1,7})\s*(?:Google\s+Flow\s+|AI\s+)?credits", re.I)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", re.I)


def parse_flow(text: str) -> int:
    hits = [int(m.group(1).replace(",", "")) for m in CREDITS_RE.finditer(text)]
    if not hits:
        raise RuntimeError("no 'N credits' text on the Flow page or its account picker (signed out, or the picker moved)")
    return hits[0]


def _flow_picker(page, text: str) -> str:
    """Open the account picker so the credit count and signed-in account are on the page."""
    if CREDITS_RE.search(text) and FLOW_ACCOUNT in text.lower():
        return text
    for sel in FLOW_PICKER:
        loc = page.locator(sel).first
        try:
            if loc.count() == 0:
                continue
            loc.click(timeout=2500)
        except Exception:  # noqa: BLE001
            continue
        page.wait_for_timeout(1500)
        aria = page.evaluate("() => [...document.querySelectorAll('[aria-label]')]"
                             ".map(e => e.getAttribute('aria-label') || '').join('\\n')") or ""
        text = page.inner_text("body") + "\n" + aria
        page.keyboard.press("Escape")
        break
    return text


def read_flow() -> dict:
    text = _page_text(FLOW_URL, None, settle_ms=8000, then=_flow_picker)
    if re.search(r"sign in to continue|you.?re not signed in", text, re.I):
        raise RuntimeError("Flow is signed out in the CDP Chrome")
    emails = {e.lower() for e in EMAIL_RE.findall(text)}
    if emails and FLOW_ACCOUNT not in emails:
        raise RuntimeError(f"Flow is signed in as another account ({len(emails)} seen, not the Ultra one)")
    who = FLOW_ACCOUNT if FLOW_ACCOUNT in emails else "account not shown"
    return {"left": parse_flow(text), "note": f"Flow account picker credits ({who}, CDP :9222)"}


def _credit_status(cell: str) -> str:
    """The row's own status cell. Since 12 Oct 2026 an active credit near its end date reads "Expiring in N days"."""
    for word, status in (("Expired", "Expired"), ("Used", "Used"), ("Available", "Available")):
        if re.search(rf"\b{word}\b", cell):
            return status
    m = re.search(r"Expiring in \d+ days?", cell, re.I)
    return f"Available ({m.group(0).lower()})" if m else "?"


def parse_billing(text: str) -> tuple[float, str]:
    rows = [ln.strip() for ln in text.splitlines() if ln.strip()]
    lines, trial = [], None
    for i, ln in enumerate(rows):
        if re.fullmatch(r"(Free Trial|.*Developer Program.*|.*credit.*)", ln, re.I) and len(ln) < 90:
            window = " ".join(rows[i:i + 8])
            m = re.search(r"£([\d,]+\.\d\d)", window)
            if not m or ln.lower().startswith("credit application type") or re.search(r"CreditId|Credit-", ln):
                continue
            amt = float(m.group(1).replace(",", ""))
            status = _credit_status(" ".join(rows[i + 1:i + 3]))
            lines.append(f"{ln}: £{amt:.2f} {status}")
            if status.startswith("Available"):
                # Ben, 12 Oct 2026 23:51: the pool is every active promo credit (Free Trial + Developer Program
                # monthly), all scoped to Vertex on billing account 0124D1. Used/Expired rows count nothing.
                trial = (trial or 0.0) + amt
    if trial is None:
        raise RuntimeError("could not read an Available credit row on Cloud Billing > Credits")
    return round(trial, 2), "; ".join(dict.fromkeys(lines))


def read_vertex() -> dict:
    trial, lines = parse_billing(_page_text(BILLING_URL, "Free Trial", settle_ms=2500))
    return {"left": trial, "note": f"promo pool (all Available credits; jobs stop at £1 margin) · Cloud Billing > Credits: {lines}"}


CURSOR_POOLS = {"cursor models": "Cursor Models", "other models": "Other Models", "weekly usage": "Grok Bot weekly"}


def parse_cursor(text: str) -> dict:
    """The /dashboard/spending page (12 Oct 2026): a percent used per pool, no $ figure.

    `left` is the percent left of Cursor Models, the pool the Mini's Cursor runs on (Auto, Composer): when it fills,
    usage overflows into Other Models, which also carries Claude-in-Cursor. Until 14 Oct `left` was Other Models, so the
    board read "Cursor 0%" while Cursor's own models were 86% free (Ben, 14 Oct 2026: "plenty left in cursor").
    Other Models (Claude-in-Cursor, flagged in scripts/credit_flags.json when used up) and the reset dates go in the note."""
    rows = [ln.strip() for ln in text.splitlines() if ln.strip()]
    used: dict[str, int] = {}
    label = None
    for ln in rows:
        key = next((k for k in CURSOR_POOLS if ln.lower().startswith(k)), None)
        if key:
            label = key
            continue
        m = re.fullmatch(r"(\d{1,3})%\s+used", ln, re.I)
        if m and label and label not in used:
            used[label] = int(m.group(1))
            label = None
    if "other models" not in used and "cursor models" not in used:
        raise RuntimeError("no 'Cursor Models' or 'Other Models · N% used' line on the Cursor spending page (signed out, or the page changed)")
    reset = re.search(r"Usage limits reset on ([^\n(]+?)\s*(?:\(|\n|$)", text)
    weekly = re.search(r"Weekly usage\s+\d{1,3}%\s+used\s+Resets ([^\n(]+?)\s*(?:\(|\n|$)", text)
    bits = [f"{CURSOR_POOLS[k]} {used[k]}% used" for k in CURSOR_POOLS if k in used]
    if reset:
        bits.append(f"limits reset {reset.group(1).strip()}")
    if weekly:
        bits.append(f"weekly resets {weekly.group(1).strip()}")
    return {"left": 100 - used.get("cursor models", used.get("other models", 0)), "total": 100, "used": used,
            "note": "; ".join(bits)}


def read_cursor() -> dict:
    text = _page_text(CURSOR_URL, None, settle_ms=8000)
    if re.search(r"\bsign in\b|\blog in\b", text[:2000], re.I) and "% used" not in text:
        raise RuntimeError("Cursor dashboard is signed out in the CDP Chrome")
    r = parse_cursor(text)
    return {"left": r["left"], "total": r["total"],
            "note": f"Cursor spending page, % of Cursor Models left: {r['note']} (CDP :9222)"}


def flow_refill(r: dict, last_left: float | None) -> dict:
    """A Flow balance above the last recorded one is the monthly refill: record it as --total (J0052 step 2)."""
    if last_left is not None and r.get("total") is None and r["left"] > last_left:
        return {**r, "total": r["left"], "note": f"{r['note']}; refill from {last_left:g} (monthly allotment)"}
    return r


def last_left(pool: str) -> float | None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from ai_spend import load  # noqa: E402
    rows = [x for x in load() if x.get("kind") == "record" and x.get("pool") == pool and x.get("left") is not None]
    return float(rows[-1]["left"]) if rows else None


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
            if pool == "flow":
                r = flow_refill(r, last_left("flow"))
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
