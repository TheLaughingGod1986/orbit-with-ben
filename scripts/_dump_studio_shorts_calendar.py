#!/usr/bin/env python3
"""Dump live Studio Shorts titles, dates, visibility from the content table via CDP."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
OUT = Path("/tmp/studio_shorts_calendar_dump.json")
URL = (
    "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/short"
    "?filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D"
)


def scrape(page) -> list[dict]:
    return page.evaluate(
        """() => {
          const rows = [];
          const walk = (root) => {
            for (const a of root.querySelectorAll('a[href*="/video/"]')) {
              const href = a.getAttribute('href') || '';
              const m = href.match(/\\/video\\/([\\w-]{11})\\//);
              if (!m) continue;
              const id = m[1];
              const row = a.closest('ytcp-video-row, ytcp-video-list-cell-video, tr, [class*="row"]') || a.parentElement;
              let t = '';
              try { t = (row && row.innerText) ? row.innerText : a.innerText; } catch (e) { t = a.innerText || ''; }
              rows.push({ id, href, text: (t || '').replace(/\\s+/g, ' ').trim().slice(0, 500) });
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(document);
          const seen = new Set();
          const out = [];
          for (const r of rows) {
            if (seen.has(r.id)) continue;
            seen.add(r.id);
            out.push(r);
          }
          return out;
        }"""
    )


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(5000)
        # Scroll to load more rows
        for _ in range(12):
            page.mouse.wheel(0, 1800)
            page.wait_for_timeout(700)
        rows = scrape(page)
        # Also try the table's innerText dump
        body = page.inner_text("body")
        page.screenshot(path="/tmp/studio_shorts_calendar.png", full_page=False)
        page.close()

    DATE = re.compile(
        r"(?:Draft|Scheduled|Private|Public|Unlisted|Premiere).*?(?:\d{1,2}\s+\w{3,9}\s+2026|\d{1,2}\s+\w{3}\s+2026)?",
        re.I,
    )
    cleaned = []
    for r in rows:
        text = r["text"]
        vis = None
        for v in ("Scheduled", "Private", "Public", "Draft", "Unlisted", "Premiere"):
            if v in text:
                vis = v
                break
        dm = re.search(r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+2026)", text, re.I)
        title = text
        for cut in ("Scheduled", "Private", "Public", "Draft", "Unlisted", "0 views", "Visibility"):
            if cut in title:
                title = title.split(cut)[0]
        title = re.sub(r"^\d+:\d+\s*", "", title).strip()
        cleaned.append(
            {
                "id": r["id"],
                "title": title[:160],
                "visibility": vis,
                "date": dm.group(1) if dm else None,
                "raw": text[:300],
            }
        )
    OUT.write_text(json.dumps({"count": len(cleaned), "rows": cleaned, "body_snip": body[:2500]}, indent=2))
    print(json.dumps({"count": len(cleaned), "rows": cleaned}, indent=2))


if __name__ == "__main__":
    main()
