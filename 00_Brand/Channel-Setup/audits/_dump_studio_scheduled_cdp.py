#!/usr/bin/env python3
"""List scheduled Orbit Studio videos via CDP :9222."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
OUT = Path(__file__).resolve().parent / "STUDIO_SCHEDULED_DUMP.json"
LONDON = ZoneInfo("Europe/London")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.goto(
            "https://studio.youtube.com/channel/UC/content?filter=%5B%22SCHEDULED%22%5D&sort=%7B%22columnType%22%3A%22SCHEDULED%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(8000)
        text = page.locator("body").inner_text()
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        rows = []
        for i, ln in enumerate(lines):
            if re.search(r"Sep \d+, 2026", ln) or re.search(r"\d{1,2}:\d{2}:\d{2}", ln):
                ctx_lines = lines[max(0, i - 3) : i + 2]
                rows.append({"schedule_line": ln, "context": ctx_lines})
        payload = {
            "ran_at": datetime.now(LONDON).isoformat(),
            "rows": rows[:80],
            "body_head": text[:4000],
        }
        OUT.write_text(json.dumps(payload, indent=2) + "\n")
        print("WROTE", OUT, "rows", len(rows))
        page.screenshot(path=str(OUT.with_suffix(".png")), full_page=True)
        page.close()


if __name__ == "__main__":
    main()
