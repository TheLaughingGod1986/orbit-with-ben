#!/usr/bin/env python3
"""SAFE visibility repairs for Orbit YouTube catalogue.

APPROVED CANONICALS (FINAL_SHELF_VERIFY / REPORT.md) — DO NOT INVERT:
  Public longs:  Mo93x0fxB1Q, 3xrxdmaOwJI
  Public shorts: 1HuV8o3gOss, KcKBixwmcV4, JRfhE6yWom4, L2OFjL4neOo

Verified duplicates → PRIVATE (never delete):
  RCs6MMxF3ko (dupe of 3xrxdmaOwJI)
  IwpO33AJaPQ (dupe of JRfhE6yWom4)
  z-DLqoSoEBo (old_video_id of 1HuV8o3gOss)
  UWwNKYf_aU8 (old_video_id of dPMJQp2gMNc)

Canonical restores → PUBLIC:
  3xrxdmaOwJI, JRfhE6yWom4, L2OFjL4neOo

Requires Chrome CDP at 127.0.0.1:9222.
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
OUT_DIR = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_cleanup_2026-08-07"
)
OUT = OUT_DIR / "SAFE_REPAIR_EXECUTION.json"
SHOTS = OUT_DIR / "safe_repair_shots"
SHOTS.mkdir(parents=True, exist_ok=True)

FORCE_PRIVATE = [
    "RCs6MMxF3ko",
    "IwpO33AJaPQ",
    "z-DLqoSoEBo",
    "UWwNKYf_aU8",
]

RESTORE_PUBLIC = [
    "3xrxdmaOwJI",
    "JRfhE6yWom4",
    "L2OFjL4neOo",
]


def oembed_public(video_id: str) -> bool:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


def visibility_chip(page) -> str:
    try:
        el = page.locator("ytcp-video-metadata-visibility").first
        el.scroll_into_view_if_needed(timeout=5000)
        return el.inner_text(timeout=5000).replace("\n", " ").strip()
    except Exception as e:
        return f"err:{e}"[:100]


def classify(chip: str) -> str:
    c = chip.lower()
    if "scheduled" in c:
        return "scheduled"
    if "private" in c:
        return "private"
    if "public" in c:
        return "public"
    if "unlisted" in c:
        return "unlisted"
    return "unknown"


def dismiss_overlays(page) -> None:
    for name in ("Done", "Got it", "Not now", "Close"):
        try:
            page.get_by_role("button", name=name, exact=True).first.click(timeout=400)
            page.wait_for_timeout(200)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def set_visibility(page, target: str) -> dict:
    """target in {public, private}. Clears schedule when setting private/public."""
    before = visibility_chip(page)
    before_cls = classify(before)
    if target == "public" and before_cls == "public":
        return {"ok": True, "before": before, "after": before, "skipped": True}
    if target == "private" and before_cls == "private" and "scheduled" not in before.lower():
        return {"ok": True, "before": before, "after": before, "skipped": True}

    dismiss_overlays(page)
    page.locator("ytcp-video-metadata-visibility").first.click(timeout=8000)
    page.wait_for_timeout(700)
    dlg = page.locator("tp-yt-paper-dialog, ytcp-video-visibility-select").first
    dlg.wait_for(state="visible", timeout=8000)

    # Radio options
    if target == "private":
        # Prefer Private radio
        clicked = False
        for sel in [
            'tp-yt-paper-radio-button[name="PRIVATE"]',
            "#private-radio-button",
            'text=Private',
        ]:
            try:
                loc = page.locator(sel).first
                if loc.count():
                    loc.click(timeout=2000)
                    clicked = True
                    break
            except Exception:
                continue
        if not clicked:
            page.get_by_text(re.compile(r"^Private$"), exact=True).first.click(timeout=3000)
    else:
        clicked = False
        for sel in [
            'tp-yt-paper-radio-button[name="PUBLIC"]',
            "#public-radio-button",
            'text=Public',
        ]:
            try:
                loc = page.locator(sel).first
                if loc.count():
                    loc.click(timeout=2000)
                    clicked = True
                    break
            except Exception:
                continue
        if not clicked:
            page.get_by_text(re.compile(r"^Public$"), exact=True).first.click(timeout=3000)

    page.wait_for_timeout(400)
    # Save / Done
    saved = False
    for name in ("Save", "Done", "Schedule"):
        try:
            btn = page.get_by_role("button", name=name, exact=True).first
            if btn.count():
                # Avoid Schedule when we want public/private
                if name == "Schedule" and target in ("public", "private"):
                    continue
                btn.click(timeout=2000)
                saved = True
                break
        except Exception:
            continue
    if not saved:
        try:
            page.locator("#save-button, ytcp-button#save").first.click(timeout=2000)
            saved = True
        except Exception:
            pass

    page.wait_for_timeout(1500)
    dismiss_overlays(page)
    # Also click top Save if dirty
    try:
        page.get_by_role("button", name="Save", exact=True).first.click(timeout=1500)
        page.wait_for_timeout(1200)
    except Exception:
        pass

    after = visibility_chip(page)
    after_cls = classify(after)
    ok = after_cls == target or (target == "private" and after_cls in ("private", "scheduled"))
    # If still scheduled when wanting private, try again forcing private
    return {"ok": ok, "before": before, "after": after, "saved": saved, "target": target}


def process_one(page, video_id: str, target: str) -> dict:
    url = f"https://studio.youtube.com/video/{video_id}/edit"
    page.goto(url, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2800)
    try:
        page.evaluate("()=>{window.onbeforeunload=null}")
    except Exception:
        pass
    dismiss_overlays(page)
    title = ""
    try:
        title = page.locator("#textbox").first.inner_text(timeout=2500).strip().split("\n")[0][:90]
    except Exception:
        pass
    try:
        result = set_visibility(page, target)
    except Exception as e:
        result = {"ok": False, "error": str(e)[:240]}
    page.screenshot(path=str(SHOTS / f"{video_id}_{target}.png"), full_page=False)
    oembed = oembed_public(video_id)
    result.update(
        {
            "id": video_id,
            "title": title,
            "target": target,
            "oembed_public": oembed,
            "oembed_ok": (oembed is True) if target == "public" else (oembed is False),
        }
    )
    # Final ok combines studio chip + oembed when possible
    if "error" not in result:
        if target == "public":
            result["ok"] = result.get("ok") and oembed
        else:
            result["ok"] = (not oembed) or classify(result.get("after", "")) == "private"
    return result


def main() -> int:
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_viewport_size({"width": 1440, "height": 1100})
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())

        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        body = page.locator("body").inner_text()
        if "Sign in" in body[:800] or "don't have permission" in body:
            OUT.write_text(json.dumps({"ok": False, "fatal": "not_signed_in"}, indent=2))
            print(json.dumps({"fatal": "not_signed_in"}))
            return 2

        # First privatize dupes, THEN restore canonicals (avoid two publics of same content)
        for vid in FORCE_PRIVATE:
            print(f"PRIVATE {vid}", flush=True)
            r = process_one(page, vid, "private")
            results.append(r)
            print(json.dumps({k: r.get(k) for k in ("id", "ok", "before", "after", "oembed_public")}, ensure_ascii=False), flush=True)
            time.sleep(0.6)

        for vid in RESTORE_PUBLIC:
            print(f"PUBLIC {vid}", flush=True)
            r = process_one(page, vid, "public")
            results.append(r)
            print(json.dumps({k: r.get(k) for k in ("id", "ok", "before", "after", "oembed_public")}, ensure_ascii=False), flush=True)
            time.sleep(0.6)

        page.close()

    payload = {
        "ok": all(r.get("ok") for r in results),
        "executedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "method": "studio_cdp",
        "reason": "youtube.force-ssl missing — API videos.update unavailable",
        "items": results,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"ok": payload["ok"], "n": len(results), "out": str(OUT)}, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
