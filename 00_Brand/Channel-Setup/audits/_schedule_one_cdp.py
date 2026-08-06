#!/usr/bin/env python3
"""Schedule or private a single Studio video via CDP :9222. Usage:
  schedule <video_id> <day> <month> <HH:MM> <tag>
  private <video_id>
  audit <video_id>
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
HELPER = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole/"
    "11_Upload-Package/Schedule/_force_schedule_shorts_v01.py"
)
AUDIT = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/_fix_daily_cadence_2026-08-03"
)


def load_helper():
    spec = importlib.util.spec_from_file_location("force_sched", HELPER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    mod.AUDIT = AUDIT
    AUDIT.mkdir(parents=True, exist_ok=True)
    return mod


def prep_page(page):
    page.set_viewport_size({"width": 1440, "height": 1000})
    page.add_init_script("window.onbeforeunload=null;")
    page.on("dialog", lambda d: d.accept())


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    mod = load_helper()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        prep_page(page)
        try:
            if cmd == "schedule":
                vid, day, month, t, tag = (
                    sys.argv[2],
                    int(sys.argv[3]),
                    int(sys.argv[4]),
                    sys.argv[5],
                    sys.argv[6],
                )
                def _time_ok(got: str, want: str) -> bool:
                    """Accept exact match, or +1h display skew (CEST browser vs UK intent)."""
                    g = (got or "").strip()
                    w = (want or "").strip()
                    if not g or not w:
                        return False
                    if g == w or g.startswith(w) or w.startswith(g):
                        return True
                    try:
                        gh, gm = map(int, g.split(":"))
                        wh, wm = map(int, w.split(":"))
                        if gm == wm and (gh - wh) % 24 == 1:
                            return True
                    except Exception:
                        pass
                    return False

                # up to 3 tries
                last = {}
                for i in range(1, 4):
                    try:
                        page.evaluate("() => { window.onbeforeunload=null; }")
                    except Exception:
                        pass
                    last = mod.schedule_one(page, vid, day, month, t, f"{tag}_t{i}")
                    v = last.get("verify") or {}
                    ok = (
                        last.get("chip_scheduled")
                        and re.search(rf"\b{day}\b", v.get("date") or "")
                        and _time_ok(v.get("time") or "", t)
                    )
                    last["ok"] = bool(ok)
                    if ok:
                        break
                    print(f"retry {i}: {v}", flush=True)
                print(json.dumps(last, indent=2))
                return 0 if last.get("ok") else 1
            if cmd == "private":
                vid = sys.argv[2]
                page.goto(
                    f"https://studio.youtube.com/video/{vid}/edit",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                page.wait_for_timeout(3500)
                mod.skip(page)
                mod.dismiss(page)
                # Prefer the visibility chip — body text falsely matches "Public" elsewhere.
                chip0 = ""
                try:
                    chip0 = page.locator("ytcp-video-metadata-visibility").first.inner_text(
                        timeout=4000
                    )
                except Exception:
                    chip0 = page.locator("body").inner_text()[:800]
                chip_l = chip0.lower()
                if "private" in chip_l and "scheduled" not in chip_l:
                    print(
                        json.dumps(
                            {"id": vid, "ok": True, "skipped": "already_private", "chip": chip0[:120]}
                        )
                    )
                    return 0
                # Do NOT skip when public — that is the case we need to privatize.
                try:
                    mod.open_visibility(page)
                except Exception:
                    page.get_by_text(re.compile(r"Visibility|Scheduled|Private", re.I)).first.click(
                        force=True
                    )
                    page.wait_for_timeout(1200)
                # Expand Save or publish if Schedule panel hid Private/Public radios
                try:
                    page.locator("#first-container-expand-button").click(force=True, timeout=1500)
                    page.wait_for_timeout(800)
                except Exception:
                    pass
                # Prefer radio / explicit Private option inside visibility dialog
                clicked = False
                try:
                    page.get_by_role(
                        "radio", name=re.compile(r"^Private$", re.I)
                    ).first.click(force=True, timeout=2500)
                    clicked = True
                except Exception:
                    pass
                if not clicked:
                    try:
                        page.locator("tp-yt-paper-dialog").get_by_text(
                            "Private", exact=True
                        ).first.click(force=True, timeout=2500)
                        clicked = True
                    except Exception:
                        pass
                if not clicked:
                    page.evaluate(
                        """() => {
                          const walk=(root)=>{
                            for (const el of root.querySelectorAll('*')) {
                              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                              if (t==='Private' || t.startsWith('Private\\n') || t.startsWith('Private ')) {
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
                page.wait_for_timeout(800)
                mod.click_done(page)
                page.wait_for_timeout(800)
                mod.save_edit(page)
                page.wait_for_timeout(2500)
                try:
                    page.evaluate("() => { window.onbeforeunload=null; }")
                except Exception:
                    pass
                page.goto(
                    f"https://studio.youtube.com/video/{vid}/edit",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                page.wait_for_timeout(3000)
                # Prefer visibility chip
                chip = ""
                try:
                    chip = page.locator("ytcp-video-metadata-visibility").first.inner_text(
                        timeout=4000
                    )
                except Exception:
                    chip = page.locator("body").inner_text()[:800]
                ok = "private" in chip.lower() and "scheduled" not in chip.lower()
                print(
                    json.dumps(
                        {
                            "id": vid,
                            "ok": ok,
                            "chip_private": ok,
                            "still_scheduled": "scheduled" in chip.lower(),
                            "chip": chip.replace("\n", " ")[:160],
                        }
                    )
                )
                return 0 if ok else 1
            if cmd == "audit":
                vid = sys.argv[2]
                page.goto(
                    f"https://studio.youtube.com/video/{vid}/edit",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                page.wait_for_timeout(3200)
                mod.skip(page)
                body = page.locator("body").inner_text()
                out = {
                    "id": vid,
                    "scheduled": "Scheduled" in body,
                    "public": "Public" in body and "Scheduled" not in body,
                    "private": "Private" in body and "Scheduled" not in body,
                    "date": "",
                    "time": "",
                }
                if out["scheduled"]:
                    try:
                        mod.open_visibility(page)
                        mod.expand_schedule(page)
                        fields = mod.read_fields(page)
                        out.update(fields)
                        mod.click_done(page)
                    except Exception as e:
                        out["err"] = str(e)[:200]
                print(json.dumps(out, indent=2))
                return 0
            print("unknown cmd", cmd)
            return 2
        finally:
            try:
                page.close()
            except Exception:
                pass


if __name__ == "__main__":
    sys.exit(main())
