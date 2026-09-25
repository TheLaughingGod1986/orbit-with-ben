#!/usr/bin/env python3
"""Delete premature FB Page reels for aliens shorts 01–03 (YT not live yet)."""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "fb_page_retry_2026-08-03"
OUT.mkdir(parents=True, exist_ok=True)
PAGE_REELS = "https://www.facebook.com/profile.php?id=61592833318203&sk=reels_tab"
CDP = "http://127.0.0.1:9222"
NEEDLES = ("everybody", "distance", "watching", "rude", "zoo")


def main() -> None:
    urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
    results: dict = {"deleted": [], "remaining": None}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next((pg for pg in ctx.pages if "facebook.com" in (pg.url or "")), None)
        if page is None:
            page = ctx.new_page()
        page.bring_to_front()
        page.goto(PAGE_REELS, wait_until="domcontentloaded", timeout=120000)
        time.sleep(4)
        page.screenshot(path=str(OUT / "v18_before_delete.png"), timeout=15000)

        for round_i in range(6):
            body = page.evaluate("() => (document.body && document.body.innerText) || ''")
            low = body.lower()
            if "haven't created any reels" in low or "no reels yet" in low:
                results["empty"] = True
                break
            # Open first reel tile if present
            opened = page.evaluate(
                """() => {
                  const tiles=[...document.querySelectorAll('a[href*="/reel/"],a[href*="reels"],div[role=link]')]
                    .filter(el => {
                      const r=el.getBoundingClientRect();
                      return r.width>80 && r.height>80 && r.y>200 && r.y<900;
                    });
                  if (!tiles.length) return false;
                  tiles[0].click();
                  return true;
                }"""
            )
            if not opened:
                # try clicking in reels grid area
                page.mouse.click(420, 520)
            time.sleep(3)
            page.screenshot(path=str(OUT / f"v18_open_{round_i}.png"), timeout=12000)

            # Menu → Delete
            clicked_menu = page.evaluate(
                """() => {
                  const btns=[...document.querySelectorAll('div[role=button],button,[aria-label]')];
                  const more=btns.find(el => {
                    const al=(el.getAttribute('aria-label')||'').toLowerCase();
                    return /more|actions|options|menu/i.test(al);
                  });
                  if (more) { more.click(); return 'aria'; }
                  const byText=btns.find(el => /^More$/i.test((el.innerText||'').trim()));
                  if (byText) { byText.click(); return 'text'; }
                  return null;
                }"""
            )
            time.sleep(1.2)
            deleted = page.evaluate(
                """() => {
                  const items=[...document.querySelectorAll('div[role=menuitem],span,div[role=button],button')]
                    .filter(el => /^(Delete|Move to trash|Remove)$/i.test((el.innerText||'').trim()));
                  if (!items.length) return {ok:false, reason:'no_delete'};
                  items[0].click();
                  return {ok:true};
                }"""
            )
            time.sleep(1.2)
            # confirm
            confirmed = page.evaluate(
                """() => {
                  const btns=[...document.querySelectorAll('div[role=button],button')]
                    .filter(el => /^(Delete|Confirm|Move to trash|OK)$/i.test((el.innerText||'').trim()));
                  const el=btns.find(e => e.getAttribute('aria-disabled')!=='true') || btns[0];
                  if (!el) return false;
                  el.click(); return true;
                }"""
            )
            entry = {
                "round": round_i,
                "menu": clicked_menu,
                "deleted": deleted,
                "confirmed": confirmed,
            }
            results["deleted"].append(entry)
            print(entry, flush=True)
            time.sleep(3)
            page.goto(PAGE_REELS, wait_until="domcontentloaded", timeout=120000)
            time.sleep(3)

        page.goto(PAGE_REELS, wait_until="domcontentloaded", timeout=120000)
        time.sleep(4)
        body = page.evaluate("() => (document.body && document.body.innerText) || ''")
        page.screenshot(path=str(OUT / "v18_after_delete.png"), timeout=15000)
        low = body.lower()
        results["remaining"] = {
            "empty": ("haven't created any reels" in low) or ("no reels yet" in low),
            "everybody": "everybody" in low,
            "distance": "rude" in low or "distance" in low,
            "watching": "watching" in low or "zoo" in low,
            "snip": re.sub(r"\s+", " ", body)[200:700],
        }
        (OUT / "V18_DELETE_PREMATURE.json").write_text(json.dumps(results, indent=2))
        print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
