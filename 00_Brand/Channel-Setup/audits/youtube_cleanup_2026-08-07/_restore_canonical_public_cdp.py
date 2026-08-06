#!/usr/bin/env python3
"""Restore approved BH canonicals to PUBLIC via Studio CDP.

Canonicals: 3xrxdmaOwJI, JRfhE6yWom4, L2OFjL4neOo
Never deletes. Requires CDP :9222.
"""
from __future__ import annotations

import importlib.util
import json
import re
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
HELPER = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole/"
    "11_Upload-Package/Schedule/_force_schedule_shorts_v01.py"
)
OUT = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_cleanup_2026-08-07/CANONICAL_RESTORE_PUBLIC.json"
)

RESTORE = ["3xrxdmaOwJI", "JRfhE6yWom4", "L2OFjL4neOo"]


def load_helper():
    spec = importlib.util.spec_from_file_location("force_sched", HELPER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def oembed_public(video_id: str) -> bool:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


def chip(page) -> str:
    try:
        return page.locator("ytcp-video-metadata-visibility").first.inner_text(timeout=5000)
    except Exception as e:
        return f"err:{e}"[:80]


def restore_public(mod, page, vid: str) -> dict:
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    try:
        page.evaluate("()=>{window.onbeforeunload=null}")
    except Exception:
        pass
    mod.skip(page)
    mod.dismiss(page)
    before = chip(page)
    if "public" in before.lower() and "scheduled" not in before.lower():
        return {
            "id": vid,
            "ok": True,
            "skipped": "already_public",
            "before": before.replace("\n", " ")[:120],
            "after": before.replace("\n", " ")[:120],
            "oembed_public": oembed_public(vid),
        }

    try:
        mod.open_visibility(page)
    except Exception:
        page.locator("ytcp-video-metadata-visibility").first.click(force=True, timeout=5000)
        page.wait_for_timeout(1000)

    try:
        page.locator("#first-container-expand-button").click(force=True, timeout=1500)
        page.wait_for_timeout(600)
    except Exception:
        pass

    clicked = False
    try:
        page.get_by_role("radio", name=re.compile(r"^Public$", re.I)).first.click(
            force=True, timeout=3000
        )
        clicked = True
    except Exception:
        pass
    if not clicked:
        try:
            page.locator("tp-yt-paper-dialog").get_by_text("Public", exact=True).first.click(
                force=True, timeout=3000
            )
            clicked = True
        except Exception:
            pass
    if not clicked:
        page.evaluate(
            """() => {
              const walk=(root)=>{
                for (const el of root.querySelectorAll('*')) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (t==='Public' || t.startsWith('Public\\n') || t.startsWith('Public ')) {
                    const r=el.getBoundingClientRect();
                    if (r.width>20 && r.height>10 && r.height<120) { el.click(); return true; }
                  }
                  if (el.shadowRoot && walk(el.shadowRoot)) return true;
                }
                return false;
              };
              return walk(document.querySelector('tp-yt-paper-dialog')||document);
            }"""
        )
        clicked = True

    page.wait_for_timeout(800)
    mod.click_done(page)
    page.wait_for_timeout(800)
    mod.save_edit(page)
    page.wait_for_timeout(2500)

    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    after = chip(page)
    oe = oembed_public(vid)
    ok = ("public" in after.lower() and "scheduled" not in after.lower()) or oe
    return {
        "id": vid,
        "ok": bool(ok),
        "clicked": clicked,
        "before": before.replace("\n", " ")[:120],
        "after": after.replace("\n", " ")[:120],
        "oembed_public": oe,
    }


def main() -> int:
    mod = load_helper()
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1440, "height": 1100})
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())
        for vid in RESTORE:
            print(f"PUBLIC {vid}", flush=True)
            try:
                r = restore_public(mod, page, vid)
            except Exception as e:
                r = {"id": vid, "ok": False, "error": str(e)[:300]}
            results.append(r)
            print(json.dumps(r, ensure_ascii=False), flush=True)
            time.sleep(0.5)
        page.close()

    payload = {
        "ok": all(r.get("ok") for r in results),
        "executedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "items": results,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"ok": payload["ok"], "out": str(OUT)}, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
