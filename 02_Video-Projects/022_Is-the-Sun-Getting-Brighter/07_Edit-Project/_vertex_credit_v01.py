#!/usr/bin/env python3
"""Read the Vertex credit from Cloud Billing → Credits (Chrome CDP :9222 on the Mini): every Available promo row,
the Free Trial and the Google Developer Program premium benefit monthly grants (Ben, 5 Nov 2026: "We also still have
to use [the Cloud credit] as well as flow"; screenshot 00:18 London: £69.48 of £75.39 left on the October grant).

  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_vertex_credit_v01.py <label>

Prints `CREDIT credit_remaining_gbp=… free_trial_remaining_gbp=… (same total, old name kept) status=…` and saves a screenshot to
07_Edit-Project/_evidence/vertex_credits_<label>.png (gitignored). Appends the reading to
07_Edit-Project/VERTEX_CREDIT_LOG_v01.json. Exits 3 if the remaining credit is below the floor (FLOOR_GBP).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

EDIT = Path(__file__).resolve().parent
EVID = EDIT / "_evidence"
LOG = EDIT / "VERTEX_CREDIT_LOG_v01.json"
URL = "https://console.cloud.google.com/billing/0124D1-E6EFD6-40F6DA/credits/all?project=gen-lang-client-0538779324"
FLOOR_GBP = 5.0  # AGENTS.md Budget: spend the promo credit down to £5; billing can lag >24 h on a Paid account
LABELS = ("Free Trial", "Google Developer Program")


def read_rows(text: str) -> tuple:
    """(total remaining GBP, rows read) over every Available promo row. Each row shows its promo value and its amount
    remaining; the remaining is never above the value, so the row's smallest £ figure is its remaining."""
    rows = [ln.strip() for ln in text.splitlines() if ln.strip()]
    total, read = 0.0, []
    for i, ln in enumerate(rows):
        if any(ln.startswith(label) for label in LABELS):
            window = []
            for nxt in rows[i + 1:i + 10]:
                if any(nxt.startswith(label) for label in LABELS):
                    break
                window.append(nxt)
            joined = " ".join(window)
            amounts = [float(a.replace(",", "")) for a in re.findall(r"£([\d,]+\.\d\d)", joined)]
            if amounts and "Expired" not in joined:
                total += min(amounts)
                read.append((ln, min(amounts)))
    return round(total, 2), read


def main() -> int:
    label = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d_%H%M")
    EVID.mkdir(exist_ok=True)
    shot = EVID / f"vertex_credits_{label}.png"
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = br.contexts[0]
        page = ctx.new_page()
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            page.get_by_text("Promo", exact=False).first.wait_for(timeout=60000)
            page.wait_for_timeout(2500)
            page.screenshot(path=str(shot))
            text = page.inner_text("body")
        finally:
            page.close()
    remaining, rows_read = read_rows(text)
    status = "Available" if rows_read else None
    if not rows_read:
        print(f"STOP: could not read any Available credit row (screenshot {shot})")
        return 2
    rec = {"label": label, "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "free_trial_remaining_gbp": remaining, "credit_remaining_gbp": remaining, "rows": rows_read, "status": status, "screenshot": shot.name,
           "floor_gbp": FLOOR_GBP}
    log = json.loads(LOG.read_text()) if LOG.exists() else {"source": URL, "readings": []}
    log["readings"].append(rec)
    LOG.write_text(json.dumps(log, indent=2) + "\n")
    print(f"CREDIT credit_remaining_gbp={remaining:.2f} free_trial_remaining_gbp={remaining:.2f} status={status} floor={FLOOR_GBP:.0f} shot={shot}")
    return 3 if remaining < FLOOR_GBP else 0


if __name__ == "__main__":
    sys.exit(main())
