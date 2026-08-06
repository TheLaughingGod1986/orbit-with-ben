#!/usr/bin/env python3
"""DISABLED — Orbit YouTube cleanup 2026-08-07.

This script caused duplicate public uploads / competing BH IDs / broken funnels.
Do NOT run. Use Content Ops API package upload instead.
ONE VIDEO = ONE UPLOAD.
"""
raise SystemExit(
    "DISABLED: smooth-CFR replace/reupload scripts are quarantined. "
    "Use 07_Content-Ops npm run youtube:package. See audits/youtube_cleanup_2026-08-07/REPORT.md"
)


# --- original quarantined source below ---
"""Replace BH long + active Shorts with smooth CFR normal-speed masters.

Live IDs from SCHEDULE_RELATED_AUDIT_2026-08-06.md.
Uses Studio Replace file (Playwright profile).
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = os.environ.get(
    "YT_PROFILE",
    "/Users/ben/code/youtube/.playwright-youtube-from-chrome",
)
CDP = os.environ.get("YT_CDP", "http://127.0.0.1:9245")
FORCE_CDP = os.environ.get("YT_FORCE_CDP", "0") == "1"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"

BH = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
AUDIT = BH / "11_Upload-Package/Schedule/_studio_audit_smooth_cfr"
OUT = BH / "11_Upload-Package/Schedule/smooth_cfr_replace_result.json"

JOBS = [
    {
        "tag": "long",
        "id": "3xrxdmaOwJI",
        "file": BH
        / "09_Final-Export/blackhole_v06_SMOOTH_NORMAL_UPLOAD_READY_MASTER.mp4",
        "needles": ["blackhole_v06_SMOOTH", "SMOOTH_NORMAL"],
        "restore_public": True,
    },
    {
        "tag": "s01",
        "id": "JRfhE6yWom4",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-01_event-horizon_v04_smooth_normal.mp4",
        "needles": ["event-horizon_v04_smooth", "v04_smooth_normal"],
        "restore_public": True,
    },
    {
        "tag": "s02",
        "id": "L2OFjL4neOo",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-02_spaghettification_v04_smooth_normal.mp4",
        "needles": ["spaghettification_v04_smooth", "v04_smooth_normal"],
        "restore_public": False,  # may be scheduled — leave visibility alone after replace
    },
    {
        "tag": "nf01",
        "id": "tUAdhOnMW2g",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_nf01_time-appears-to-stop_v03_smooth_normal.mp4",
        "needles": ["time-appears-to-stop_v03_smooth", "v03_smooth_normal"],
        "restore_public": False,
    },
    {
        "tag": "s04",
        "id": "svYOx07OrIM",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-04_look-back_v04_smooth_normal.mp4",
        "needles": ["look-back_v04_smooth", "v04_smooth_normal"],
        "restore_public": False,
    },
    {
        "tag": "nf02",
        "id": "B2STcIAF1lY",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_nf02_what-you-would-see_v03_smooth_normal.mp4",
        "needles": ["what-you-would-see_v03_smooth", "v03_smooth_normal"],
        "restore_public": False,
    },
    {
        "tag": "s06",
        "id": "w1ej9u0rPTA",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-06_point-of-no-return_v04_smooth_normal.mp4",
        "needles": ["point-of-no-return_v04_smooth", "v04_smooth_normal"],
        "restore_public": False,
    },
]


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass
    try:
        page.evaluate(
            "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
        )
    except Exception:
        pass


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=True)
    except Exception:
        pass


def open_edit(page, video_id: str) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)


def find_replace(page) -> bool:
    dismiss(page)
    for role in ("menuitem", "button", "link"):
        loc = page.get_by_role(
            role, name=re.compile(r"Replace file|Replace video|^Replace$", re.I)
        )
        if loc.count():
            try:
                if loc.first.is_visible():
                    loc.first.click(force=True)
                    return True
            except Exception:
                pass
    clicked = page.evaluate(
        """() => {
          const walk=(root)=>{
            for (const el of root.querySelectorAll('button,[role=button],ytcp-icon-button')) {
              const al=(el.getAttribute('aria-label')||'').toLowerCase();
              if (al.includes('options') || al.includes('more options') || al.includes('more actions') || al.includes('video actions')) {
                const box=el.getBoundingClientRect();
                if (box.width>8) { el.click(); return al; }
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    if clicked:
        page.wait_for_timeout(700)
        item = page.get_by_role("menuitem", name=re.compile(r"Replace", re.I))
        if item.count() and item.first.is_visible():
            item.first.click(force=True)
            return True
        hit = page.evaluate(
            """() => {
              const walk=(root)=>{
                for (const el of root.querySelectorAll('tp-yt-paper-item,[role=menuitem],yt-formatted-string,span,div')) {
                  const t=(el.innerText||'').trim();
                  if (/^Replace( file| video)?$/i.test(t)) {
                    const box=el.getBoundingClientRect();
                    if (box.width>20) { el.click(); return t; }
                  }
                }
                for (const el of root.querySelectorAll('*')) {
                  if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
                }
                return null;
              };
              return walk(document);
            }"""
        )
        return bool(hit)
    return False


def confirm(page) -> None:
    for name in (r"^Replace$", r"^Continue$", r"^Yes$", r"^Confirm$", r"^Done$"):
        try:
            b = page.get_by_role("button", name=re.compile(name, re.I))
            if b.count() and b.first.is_visible():
                txt = (b.first.inner_text() or "").lower()
                if "cancel" in txt:
                    continue
                b.first.click(force=True, timeout=2000)
                page.wait_for_timeout(800)
        except Exception:
            pass


def set_file(page, path: Path) -> bool:
    inputs = page.locator('input[type="file"]')
    if inputs.count():
        for idx in range(inputs.count() - 1, -1, -1):
            try:
                inputs.nth(idx).set_input_files(str(path))
                return True
            except Exception:
                continue
    try:
        with page.expect_file_chooser(timeout=25000) as fc:
            for label in (r"Select files?", r"Replace file", r"Upload", r"Choose file"):
                b = page.get_by_role("button", name=re.compile(label, re.I))
                if b.count() and b.first.is_visible():
                    b.first.click(force=True)
                    break
        fc.value.set_files(str(path))
        return True
    except Exception:
        return False


def wait_upload(page, needles: list[str], timeout_s: int = 1800) -> dict:
    start = time.time()
    last = ""
    while time.time() - start < timeout_s:
        dismiss(page)
        body = page.locator("body").inner_text()
        last = re.sub(r"\s+", " ", body)[:500]
        low = body.lower()
        if any(n.lower() in low for n in needles):
            if "uploading" not in low and "0%" not in low:
                page.wait_for_timeout(5000)
                return {"done": True, "signal": "filename", "head": last}
        if any(
            x in low
            for x in (
                "checks complete",
                "processing complete",
                "finished processing",
                "video replaced",
                "replaced successfully",
            )
        ):
            return {"done": True, "signal": "complete", "head": last}
        if "uploading 100%" in low or "processing 100%" in low:
            page.wait_for_timeout(10000)
        page.wait_for_timeout(5000)
    return {"done": False, "signal": "timeout", "head": last}


def save_page(page) -> bool:
    dismiss(page)
    for label in (r"^Save$", r"^Publish$", r"^Done$"):
        b = page.get_by_role("button", name=re.compile(label, re.I))
        if b.count() and b.first.is_enabled():
            try:
                b.first.click(force=True)
                page.wait_for_timeout(3000)
                return True
            except Exception:
                pass
    return False


def set_public(page) -> bool:
    dismiss(page)
    try:
        page.locator("ytcp-video-metadata-visibility").first.click(force=True, timeout=5000)
    except Exception:
        return False
    page.wait_for_timeout(1200)
    dismiss(page)
    page.evaluate(
        """() => {
          const walk=(r)=>{
            if(!r)return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])){
              const t=(el.innerText||'').toLowerCase();
              if(t.includes('public') && !t.includes('schedule')){ el.click(); return true; }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
              if(el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
          };
          return walk(document);
        }"""
    )
    page.wait_for_timeout(500)
    for label in (r"^Done$", r"^Save$", r"^Save as public$"):
        b = page.get_by_role("button", name=re.compile(label, re.I))
        if b.count() and b.first.is_enabled():
            try:
                b.first.click(force=True)
                page.wait_for_timeout(2500)
                break
            except Exception:
                pass
    body = page.locator("body").inner_text()
    return "Public" in body


def replace_one(page, job: dict) -> dict:
    path: Path = job["file"]
    r: dict = {
        "id": job["id"],
        "tag": job["tag"],
        "file": str(path),
        "ok": False,
    }
    if not path.exists():
        r["error"] = "missing_file"
        return r
    open_edit(page, job["id"])
    shot(page, f"{job['tag']}_01_edit")

    opened = find_replace(page)
    r["replace_opened"] = opened
    shot(page, f"{job['tag']}_02_replace")
    if not opened:
        r["error"] = "replace_menu_not_found"
        return r

    confirm(page)
    page.wait_for_timeout(600)
    uploaded = set_file(page, path)
    r["file_set"] = uploaded
    confirm(page)
    shot(page, f"{job['tag']}_03_file")
    if not uploaded:
        r["error"] = "file_input_failed"
        return r

    wait = wait_upload(page, job["needles"])
    r["wait"] = wait
    shot(page, f"{job['tag']}_04_wait")
    r["saved"] = save_page(page)
    if job.get("restore_public"):
        open_edit(page, job["id"])
        r["public"] = set_public(page)
        r["saved_public"] = save_page(page)
    r["ok"] = bool(wait.get("done")) and bool(r.get("file_set"))
    return r


def main() -> None:
    missing = [j for j in JOBS if not j["file"].exists()]
    if missing:
        raise SystemExit(
            "Missing files:\n" + "\n".join(str(j["file"]) for j in missing)
        )

    results: list[dict] = []
    with sync_playwright() as p:
        if FORCE_CDP:
            browser = p.chromium.connect_over_cdp(CDP)
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
        else:
            context = p.chromium.launch_persistent_context(
                PROFILE,
                headless=False,
                viewport={"width": 1440, "height": 900},
                args=["--disable-blink-features=AutomationControlled"],
            )
            page = context.pages[0] if context.pages else context.new_page()

        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/search?filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22descending%22%7D",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        dismiss(page)

        for job in JOBS:
            print(f"=== REPLACE {job['tag']} {job['id']} ===", flush=True)
            try:
                row = replace_one(page, job)
            except Exception as e:
                row = {
                    "id": job["id"],
                    "tag": job["tag"],
                    "ok": False,
                    "error": str(e),
                }
            results.append(row)
            print(json.dumps(row, indent=2)[:800], flush=True)

        if not FORCE_CDP:
            context.close()

    payload = {
        "ok": all(r.get("ok") for r in results),
        "results": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print("Wrote", OUT, flush=True)
    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
