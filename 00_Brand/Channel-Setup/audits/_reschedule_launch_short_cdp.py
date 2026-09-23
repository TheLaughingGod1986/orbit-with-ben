#!/usr/bin/env python3
"""Reschedule an Orbit Short to a new publishAt in YouTube Studio (CDP :9222).

Usage:
  python3 _reschedule_launch_short_cdp.py --video-id keXe1GNxWSU --when 2026-09-03T20:00:00+01:00
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
LONDON = ZoneInfo("Europe/London")
OUT = Path(__file__).resolve().parent / "RESCHEDULE_LAUNCH_SHORT.json"


def parse_when(raw: str) -> datetime:
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LONDON)
    return dt.astimezone(LONDON)


def reschedule(page, video_id: str, when: datetime) -> dict:
    out: dict = {"video_id": video_id, "target_iso": when.isoformat()}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)

    # Open Schedule visibility option.
    clicked = page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('tp-yt-paper-radio-button, [role="radio"], label, div, button')) {
            const t = (el.innerText || '').trim();
            if (/^Schedule$/i.test(t) || t.startsWith('Schedule\\n')) {
              const r = el.getBoundingClientRect();
              if (r.width > 20 && r.height > 10 && r.height < 90) {
                el.click();
                return t.slice(0, 40);
              }
            }
          }
          return null;
        }"""
    )
    out["schedule_click"] = clicked
    page.wait_for_timeout(1200)

    # Date field — try common Studio selectors.
    date_str = when.strftime("%d %b %Y")
    time_str = when.strftime("%H:%M")
    out["date_str"] = date_str
    out["time_str"] = time_str

    date_set = page.evaluate(
        """(dateStr) => {
          const inputs = [...document.querySelectorAll('input, textarea, tp-yt-iron-input input')];
          for (const inp of inputs) {
            const ph = (inp.placeholder || '').toLowerCase();
            const al = (inp.getAttribute('aria-label') || '').toLowerCase();
            if (ph.includes('date') || al.includes('date')) {
              inp.focus();
              inp.value = '';
              inp.dispatchEvent(new Event('input', { bubbles: true }));
              return 'found_date_input';
            }
          }
          // Click visible date picker trigger
          for (const el of document.querySelectorAll('button, ytcp-text-dropdown-trigger, div')) {
            const t = (el.innerText || '').trim();
            if (/\\d{1,2}\\s+[A-Za-z]{3}\\s+\\d{4}/.test(t) || /date/i.test(t)) {
              const r = el.getBoundingClientRect();
              if (r.width > 40 && r.height > 20 && r.height < 80) {
                el.click();
                return 'clicked_date_trigger:' + t.slice(0, 30);
              }
            }
          }
          return null;
        }""",
        date_str,
    )
    out["date_set"] = date_set
    page.wait_for_timeout(800)

    # Type date via keyboard into focused field when possible.
    page.keyboard.press("Meta+a")
    page.keyboard.type(when.strftime("%d/%m/%Y"), delay=30)
    page.wait_for_timeout(400)
    page.keyboard.press("Tab")
    page.wait_for_timeout(300)
    page.keyboard.press("Meta+a")
    page.keyboard.type(time_str, delay=30)
    page.wait_for_timeout(600)

    saved = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button, ytcp-button')) {
            const t = (b.innerText || '').trim();
            if (/^Save$/i.test(t) || /^Schedule$/i.test(t) || /^Done$/i.test(t)) {
              if (!b.disabled) { b.click(); return t; }
            }
          }
          return null;
        }"""
    )
    out["save"] = saved
    page.wait_for_timeout(3500)

    body = page.locator("body").inner_text()
    out["body_snippet"] = body[:1200]
    out["mentions_target_date"] = when.strftime("%d %b").replace(" 0", " ") in body or date_str in body
    out["ok"] = bool(saved)
    page.screenshot(path=str(OUT.with_suffix(f"_{video_id}.png")), full_page=False)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-id", required=True)
    ap.add_argument("--when", required=True, help="Europe/London ISO, e.g. 2026-09-03T20:00:00+01:00")
    args = ap.parse_args()
    when = parse_when(args.when)

    report = {"ran_at": datetime.now(LONDON).isoformat(), "results": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        try:
            row = reschedule(page, args.video_id, when)
            report["results"].append(row)
            print(json.dumps(row, indent=2))
        finally:
            try:
                page.close()
            except Exception:
                pass
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
