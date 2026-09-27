#!/usr/bin/env python3
"""Catch up LIVE Meta Reels using the proven Title-label + Share flow."""
from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

AUTO = Path(__file__).resolve().parent
sys.path.insert(0, str(AUTO))
sys.path.insert(0, str(AUTO.parents[1] / "social"))

from _sib import load  # noqa: E402
import uniqueness  # noqa: E402

ledger = load("ledger")
disc = load("discover")
caption_mod = load("caption")

COMPOSER = (
    "https://business.facebook.com/latest/reels_composer"
    "?asset_id=1285932871266399&business_id=1352434763139246"
)
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-01a06770-da52-7f5e-94e8-57ef97285507/files/artifacts"
)
ART.mkdir(parents=True, exist_ok=True)


def dismiss(page) -> None:
    page.keyboard.press("Escape")
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button,[role=button]')) {
            const t=(b.innerText||'').trim();
            if (/continue editing|not now|cancel|close|skip|got it/i.test(t) && t.length<36) {
              b.click();
            }
          }
        }"""
    )


def pending_queue() -> list[dict]:
    posted = ledger.load().get("posted") or {}
    all_live = []
    for s in disc.iter_index_shorts():
        if not s.get("_live") or s.get("_posted"):
            continue
        if not Path(s.get("_abs_file") or "").exists():
            continue
        all_live.append(s)
    return uniqueness.first_unique(all_live, posted)


def post_one(page, short: dict) -> dict:
    video = Path(short["_abs_file"])
    title = (short.get("title") or "Orbit Short")[:80]
    cap = short.get("_caption") or caption_mod.meta_caption(short)
    page.goto(COMPOSER, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    dismiss(page)

    uploaded = False
    for label in ("Add video", "Upload", "Select video", "Add media"):
        try:
            with page.expect_file_chooser(timeout=4500) as fc:
                loc = page.get_by_role("button", name=label)
                if loc.count():
                    loc.first.click(force=True)
                else:
                    page.get_by_text(label, exact=False).first.click(timeout=2000)
            fc.value.set_files(str(video))
            uploaded = True
            break
        except Exception:
            continue
    if not uploaded:
        inp = page.locator("input[type=file]")
        if inp.count():
            inp.first.set_input_files(str(video))
            uploaded = True
    if not uploaded:
        return {"status": "no_upload"}

    for _ in range(90):
        txt = (page.inner_text("body") or "").lower()
        if "safe to publish" in txt or "no copyright" in txt:
            break
        page.wait_for_timeout(1000)
    page.wait_for_timeout(1500)

    try:
        page.get_by_text("Title", exact=True).first.click(force=True, timeout=2500)
        page.keyboard.press("Meta+a")
        page.keyboard.type(title, delay=3)
    except Exception:
        pass
    try:
        page.get_by_text("Text", exact=False).first.click(force=True, timeout=2000)
        page.keyboard.press("Meta+a")
        page.keyboard.type(cap[:2000], delay=1)
    except Exception:
        pass
    page.wait_for_timeout(800)

    for _ in range(8):
        share = page.get_by_role("button", name="Share")
        if share.count():
            try:
                if not share.last.is_disabled():
                    break
            except Exception:
                break
        nxt = page.get_by_role("button", name="Next")
        if nxt.count():
            try:
                if not nxt.last.is_disabled():
                    nxt.last.click(force=True)
                    page.wait_for_timeout(1200)
                    continue
            except Exception:
                pass
        page.evaluate(
            """() => {
              for (const b of [...document.querySelectorAll('button,[role=button]')].reverse()) {
                if ((b.innerText||'').trim()==='Next' && b.getAttribute('aria-disabled')!=='true' && !b.disabled) {
                  b.click(); return true;
                }
              }
              return false;
            }"""
        )
        page.wait_for_timeout(1200)

    shared = False
    for _ in range(5):
        share = page.get_by_role("button", name="Share")
        if share.count():
            try:
                if not share.last.is_disabled():
                    share.last.click(force=True)
                    shared = True
                    break
            except Exception:
                pass
        ok = page.evaluate(
            """() => {
              const vh=innerHeight;
              for (const b of document.querySelectorAll('button,[role=button]')) {
                const t=(b.innerText||'').trim();
                if (t!=='Share' && t!=='Share now') continue;
                const r=b.getBoundingClientRect();
                if (r.y < vh*0.35) continue;
                if (b.getAttribute('aria-disabled')==='true' || b.disabled) continue;
                b.click(); return true;
              }
              return false;
            }"""
        )
        if ok:
            shared = True
            break
        page.wait_for_timeout(800)

    page.wait_for_timeout(7000)
    vid = short.get("video_id") or "unknown"
    page.screenshot(path=str(ART / f"meta_batch_{vid}.png"))
    if shared:
        return {"status": "ok", "shared": True, "method": "batch_catchup"}
    return {"status": "fail", "shared": False}


def main() -> int:
    queue = pending_queue()
    print(f"queue={len(queue)}")
    for s in queue:
        print(f" - {s.get('_ledger_key')} · {s.get('title')}")

    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223", timeout=60000)
        page = browser.contexts[0].new_page()
        for i, short in enumerate(queue, 1):
            key = short.get("_ledger_key")
            title = short.get("title")
            print(f"\n=== {i}/{len(queue)} {key} · {title} ===", flush=True)
            try:
                result = post_one(page, short)
            except Exception as e:
                result = {"status": "error", "error": f"{type(e).__name__}: {e}"}
            print("result", result, flush=True)
            results.append({"key": key, "title": title, **result})
            if result.get("status") in {"ok", "partial"}:
                ledger.mark_posted(short, result)
                print("marked", key, flush=True)
            page.wait_for_timeout(4000)
        try:
            page.close()
        except Exception:
            pass

    print("\nSUMMARY")
    for r in results:
        print(r.get("status"), r.get("key"), r.get("title"))
    ok_n = sum(1 for r in results if r.get("status") in {"ok", "partial"})
    print(f"done {ok_n}/{len(results)}")
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
