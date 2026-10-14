#!/usr/bin/env python3
"""Read the Vertex Free Trial credit from Cloud Billing → Credits (Chrome CDP :9222 on the Mini).

  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_vertex_credit_v01.py <label>

Prints `CREDIT free_trial_remaining_gbp=… status=…` and saves a screenshot to
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
FLOOR_GBP = 0.0  # J0012 / AGENTS.md Budget: Vertex trial credit may run to £0, never AI Studio prepaid


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
            page.get_by_text("Free Trial").first.wait_for(timeout=60000)
            page.wait_for_timeout(2500)
            page.screenshot(path=str(shot))
            text = page.inner_text("body")
        finally:
            page.close()
    rows = [ln for ln in text.splitlines() if ln.strip()]
    remaining, status = None, None
    for i, ln in enumerate(rows):
        if ln.strip() == "Free Trial":
            window = " ".join(rows[i:i + 8])
            if "Available" in window:
                m = re.search(r"£([\d,]+\.\d\d)", window)
                if m:
                    remaining, status = float(m.group(1).replace(",", "")), "Available"
                    break
    if remaining is None:
        print(f"STOP: could not read the Free Trial row (screenshot {shot})")
        return 2
    rec = {"label": label, "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "free_trial_remaining_gbp": remaining, "status": status, "screenshot": shot.name,
           "floor_gbp": FLOOR_GBP}
    log = json.loads(LOG.read_text()) if LOG.exists() else {"source": URL, "readings": []}
    log["readings"].append(rec)
    LOG.write_text(json.dumps(log, indent=2) + "\n")
    print(f"CREDIT free_trial_remaining_gbp={remaining:.2f} status={status} floor={FLOOR_GBP:.0f} shot={shot}")
    return 3 if remaining < FLOOR_GBP else 0


if __name__ == "__main__":
    sys.exit(main())
