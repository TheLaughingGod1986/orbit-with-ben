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
"""Replace BH masters via Studio file input (filename / hidden input)."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-from-chrome"
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
        "old_name": "blackhole_v05",
        "new_name": "blackhole_v06_SMOOTH",
    },
    {
        "tag": "s01",
        "id": "JRfhE6yWom4",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-01_event-horizon_v04_smooth_normal.mp4",
        "old_name": "event-horizon",
        "new_name": "v04_smooth_normal",
    },
    {
        "tag": "s02",
        "id": "L2OFjL4neOo",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-02_spaghettification_v04_smooth_normal.mp4",
        "old_name": "spaghettification",
        "new_name": "v04_smooth_normal",
    },
    {
        "tag": "nf01",
        "id": "tUAdhOnMW2g",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_nf01_time-appears-to-stop_v03_smooth_normal.mp4",
        "old_name": "time-appears",
        "new_name": "v03_smooth_normal",
    },
    {
        "tag": "s04",
        "id": "svYOx07OrIM",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-04_look-back_v04_smooth_normal.mp4",
        "old_name": "look-back",
        "new_name": "v04_smooth_normal",
    },
    {
        "tag": "nf02",
        "id": "B2STcIAF1lY",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_nf02_what-you-would-see_v03_smooth_normal.mp4",
        "old_name": "what-you-would-see",
        "new_name": "v03_smooth_normal",
    },
    {
        "tag": "s06",
        "id": "w1ej9u0rPTA",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-06_point-of-no-return_v04_smooth_normal.mp4",
        "old_name": "point-of-no-return",
        "new_name": "v04_smooth_normal",
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


def confirm(page) -> None:
    for name in (
        r"^Replace$",
        r"^Continue$",
        r"^Yes$",
        r"^Confirm$",
        r"^Upload$",
        r"^Done$",
        r"^Save$",
    ):
        try:
            b = page.get_by_role("button", name=re.compile(name, re.I))
            if b.count() and b.first.is_visible() and b.first.is_enabled():
                txt = (b.first.inner_text() or "").lower()
                if "cancel" in txt or "undo" in txt:
                    continue
                b.first.click(force=True, timeout=2000)
                page.wait_for_timeout(900)
        except Exception:
            pass


def wait_done(page, needle: str, timeout_s: int = 1800) -> dict:
    t0 = time.time()
    last = ""
    while time.time() - t0 < timeout_s:
        dismiss(page)
        body = page.locator("body").inner_text()
        last = re.sub(r"\s+", " ", body)[:400]
        low = body.lower()
        if needle.lower() in low and "uploading" not in low:
            page.wait_for_timeout(4000)
            return {"done": True, "signal": "filename", "head": last}
        if any(
            x in low
            for x in (
                "checks complete",
                "processing complete",
                "video replaced",
                "replaced successfully",
                "finished processing",
            )
        ):
            return {"done": True, "signal": "complete", "head": last}
        if "uploading 100%" in low or "processing 100%" in low:
            page.wait_for_timeout(8000)
        page.wait_for_timeout(5000)
    return {"done": False, "signal": "timeout", "head": last}


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        for job in JOBS:
            print(f"=== {job['tag']} {job['id']} ===", flush=True)
            r: dict = {
                "id": job["id"],
                "tag": job["tag"],
                "file": str(job["file"]),
                "ok": False,
            }
            assert job["file"].exists(), job["file"]
            page.goto(
                f"https://studio.youtube.com/video/{job['id']}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3500)
            dismiss(page)
            page.screenshot(path=str(AUDIT / f"{job['tag']}_fn_01.png"), full_page=True)

            clicked = False
            for sel in (
                page.get_by_text(re.compile(r"Filename", re.I)),
                page.locator("text=/blackhole_/"),
                page.get_by_text(re.compile(job["old_name"], re.I)),
            ):
                try:
                    if sel.count() and sel.first.is_visible():
                        sel.first.click(force=True)
                        clicked = True
                        break
                except Exception:
                    pass
            r["filename_clicked"] = clicked
            page.wait_for_timeout(800)

            page.evaluate(
                """() => {
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('button,[role=button],ytcp-icon-button')) {
                      const al=(el.getAttribute('aria-label')||'').toLowerCase();
                      if (al==='options' || al.includes('video actions')) {
                        const box=el.getBoundingClientRect();
                        if (box.width>8 && box.x>900 && box.y<500) { el.click(); return al+':'+box.x; }
                      }
                    }
                    for (const el of root.querySelectorAll('*')) if(el.shadowRoot){ const x=walk(el.shadowRoot); if(x) return x;}
                    return null;
                  };
                  return walk(document);
                }"""
            )
            page.wait_for_timeout(700)
            try:
                item = page.get_by_role("menuitem", name=re.compile(r"Replace", re.I))
                if item.count() and item.first.is_visible():
                    item.first.click(force=True)
                    r["replace_menu"] = True
                else:
                    r["replace_menu"] = False
            except Exception:
                r["replace_menu"] = False

            confirm(page)
            inputs = page.locator('input[type="file"]')
            r["file_inputs"] = inputs.count()
            uploaded = False
            if inputs.count():
                for idx in range(inputs.count() - 1, -1, -1):
                    try:
                        inputs.nth(idx).set_input_files(str(job["file"]))
                        uploaded = True
                        break
                    except Exception as e:
                        r.setdefault("input_errs", []).append(str(e)[:120])
            r["file_set"] = uploaded
            confirm(page)
            page.screenshot(path=str(AUDIT / f"{job['tag']}_fn_02.png"), full_page=True)
            if not uploaded:
                r["error"] = "file_input_failed"
                results.append(r)
                print(json.dumps(r)[:500], flush=True)
                continue

            timeout = 1500 if job["file"].stat().st_size > 80_000_000 else 600
            wait = wait_done(page, job["new_name"], timeout_s=timeout)
            r["wait"] = wait
            try:
                b = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
                if b.count() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(2500)
                    r["saved"] = True
            except Exception:
                pass
            page.screenshot(path=str(AUDIT / f"{job['tag']}_fn_03.png"), full_page=True)
            body = page.locator("body").inner_text()
            r["filename_on_page"] = (
                job["new_name"] in body or job["file"].name[:20] in body
            )
            r["ok"] = bool(uploaded and (wait.get("done") or r.get("filename_on_page")))
            results.append(r)
            summary = {k: r[k] for k in r if k != "wait"}
            summary["wait"] = wait.get("signal")
            print(json.dumps(summary), flush=True)

        ctx.close()

    payload = {"ok": all(x.get("ok") for x in results), "results": results}
    OUT.write_text(json.dumps(payload, indent=2))
    print("Wrote", OUT, flush=True)
    print("OVERALL", payload["ok"], flush=True)
    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
