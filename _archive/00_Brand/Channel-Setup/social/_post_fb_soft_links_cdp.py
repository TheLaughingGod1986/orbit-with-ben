#!/usr/bin/env python3
"""Post pending YouTube long soft-links to Facebook via Meta Business Suite CDP (:9223)."""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import live_longs as longs  # noqa: E402

CDP = "http://127.0.0.1:9223"
SUITE_HOME = (
    "https://business.facebook.com/latest/home"
    "?asset_id=1285932871266399&business_id=1352434763139246"
)
AUDIT = ROOT / "social" / "_fb_softlink_audit"
LOG = ROOT / "social" / "live_longs_auto.log"


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} fb-suite {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def click_text(page, pattern: str) -> bool:
    return bool(
        page.evaluate(
            """(pat) => {
              const re = new RegExp(pat, 'i');
              const nodes = [...document.querySelectorAll('button,[role=button],a,div,span')];
              for (const n of nodes) {
                const t = (n.innerText || n.getAttribute('aria-label') || '').trim();
                if (!t || t.length > 60) continue;
                if (!re.test(t)) continue;
                const r = n.getBoundingClientRect();
                if (r.width < 20 || r.height < 10) continue;
                n.click();
                return true;
              }
              return false;
            }""",
            pattern,
        )
    )


def open_create_post(page) -> bool:
    page.goto(SUITE_HOME, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(4000)
    if not click_text(page, r"^Create Post$"):
        if not click_text(page, r"Create Post"):
            return False
    page.wait_for_timeout(3000)
    for _ in range(20):
        if page.locator('div[contenteditable="true"], textarea').count():
            return True
        page.wait_for_timeout(500)
    return False


def fill_and_post(page, caption: str) -> dict:
    box = page.locator('div[role="dialog"] div[contenteditable="true"]').first
    if not box.count():
        box = page.locator('div[contenteditable="true"]').first
    if not box.count():
        ta = page.locator("textarea").first
        if ta.count():
            ta.fill(caption)
        else:
            return {"status": "error", "detail": "no composer box"}
    else:
        box.click(timeout=5000)
        page.wait_for_timeout(200)
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(caption)
    page.wait_for_timeout(4000)
    posted = page.evaluate(
        """() => {
          const nodes=[...document.querySelectorAll('[role=button], button')];
          for (const b of nodes) {
            const t=(b.innerText||'').trim();
            if (!/^(Post|Publish|Share now)$/i.test(t)) continue;
            const r=b.getBoundingClientRect();
            if (r.width<40 || r.height<12) continue;
            if (b.getAttribute('aria-disabled')==='true' || b.hasAttribute('disabled')) continue;
            b.click();
            return 'posted';
          }
          return 'no post btn';
        }"""
    )
    page.wait_for_timeout(5000)
    return {
        "status": "posted_link_card" if posted == "posted" else "error",
        "method": "meta_suite_cdp",
        "detail": posted,
    }


def post_one(film: dict) -> dict:
    AUDIT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        try:
            if not open_create_post(page):
                page.screenshot(path=str(AUDIT / f"no_composer_{film['video_id']}.png"))
                return {"status": "error", "detail": "no composer"}
            page.screenshot(path=str(AUDIT / f"composer_{film['video_id']}.png"))
            result = fill_and_post(page, film["_caption"])
            page.screenshot(path=str(AUDIT / f"after_{film['video_id']}.png"))
            return result
        finally:
            try:
                page.close()
            except Exception:
                pass


def main() -> int:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    prio = [
        "Yk1tLh23rko",
        "NbW5G1BpPY0",
        "REXYxuLOBoI",
        "b8-X_FyJnHM",
        "3xrxdmaOwJI",
        "Mo93x0fxB1Q",
    ]
    pending = {p["video_id"]: p for p in longs.pending_live_longs(platform="facebook")}
    ordered = [pending[i] for i in prio if i in pending][:limit]
    log(f"pending={len(pending)} posting={len(ordered)}")
    n = 0
    for film in ordered:
        log(f"posting {film['video_id']} · {film['title']}")
        result = post_one(film)
        log(f"result {result}")
        if result.get("status") in {"posted_link_card", "posted", "ok", "partial"}:
            longs.mark_posted(
                film["video_id"], "facebook", result, title=film.get("title") or ""
            )
            n += 1
        time.sleep(3)
    remaining = [p["video_id"] for p in longs.pending_live_longs(platform="facebook")]
    print(json.dumps({"posted": n, "remaining": remaining}))
    return 0 if n else 1


if __name__ == "__main__":
    raise SystemExit(main())
