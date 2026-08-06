raise SystemExit("DISABLED: smooth-canon shelf mutators quarantined — use FINAL_SHELF_VERIFY canonicals (3xrxdmaOwJI / JRfhE6yWom4 / L2OFjL4neOo).")

#!/usr/bin/env python3
"""Make smooth-CFR BH masters the ONLY public/scheduled YouTube shelf.

Canonical KEEP (smooth):
  long:  RCs6MMxF3ko
  shorts: IwpO33AJaPQ (public), IqII5mVGdrs, 2C-eiSMsBLc,
          lIHb_tyxQSM, wOlnj7nZWJM, 2uT3wXJLybw (keep schedule / public as appropriate)

FORCE PRIVATE (old slow / superseded):
  3xrxdmaOwJI, n7CbJrOCnU0,
  JRfhE6yWom4, L2OFjL4neOo, tUAdhOnMW2g, svYOx07OrIM, B2STcIAF1lY, w1ej9u0rPTA,
  2777WlMGM8M, jyzrl9ueKq4, EO-44QH4glI, t1hTGIH8O44, nX84ileqPKw, 5jjJ5CHrbCs
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-from-chrome"
CDP = "http://127.0.0.1:9222"
FORCE_CDP = False  # prefer persistent profile; set True if CDP already open

HELPER = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "004_JWST-Discoveries-That-Change-Everything/11_Upload-Package/Schedule/"
    "_force_schedule_shorts_v01.py"
)
CLEANUP = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_cleanup_2026-08-07/_cleanup_visibility_cdp.py"
)
OUT = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_smooth_canon_2026-08-07/CANON_RESULT.json"
)
AUDIT = OUT.parent / "shots"

PUBLICIZE = [
    "RCs6MMxF3ko",  # smooth long
    "IwpO33AJaPQ",  # smooth launch short
    "IqII5mVGdrs",  # past schedule → public
]

# Keep these scheduled (smooth files already on them)
KEEP_SCHEDULED = [
    "2C-eiSMsBLc",
    "lIHb_tyxQSM",
    "wOlnj7nZWJM",
    "2uT3wXJLybw",
]

FORCE_PRIVATE = [
    "3xrxdmaOwJI",
    "n7CbJrOCnU0",
    "JRfhE6yWom4",
    "L2OFjL4neOo",
    "tUAdhOnMW2g",
    "svYOx07OrIM",
    "B2STcIAF1lY",
    "w1ej9u0rPTA",
    "2777WlMGM8M",
    "jyzrl9ueKq4",
    "EO-44QH4glI",
    "t1hTGIH8O44",
    "nX84ileqPKw",
    "5jjJ5CHrbCs",
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def click_continue(page) -> bool:
    for name in (r"^Continue$", r"^Stop test$", r"^Yes$", r"^OK$"):
        try:
            b = page.get_by_role("button", name=re.compile(name, re.I))
            if b.count() and b.first.is_visible():
                b.first.click(force=True)
                page.wait_for_timeout(1500)
                return True
        except Exception:
            pass
    try:
        page.get_by_text("Continue", exact=True).first.click(force=True, timeout=1500)
        page.wait_for_timeout(1500)
        return True
    except Exception:
        return False


def set_vis(clean, force, page, video_id: str, target: str) -> dict:
    """Wrap cleanup set_visibility + ABC Continue + re-save."""
    AUDIT.mkdir(parents=True, exist_ok=True)
    r = clean.set_visibility(force, page, video_id, target)
    # If still wrong, try Continue path
    page.wait_for_timeout(500)
    if click_continue(page):
        r["abc_continue"] = True
        try:
            force.click_done(page)
        except Exception:
            pass
        r["saved2"] = clean.save_all(force, page)
        page.wait_for_timeout(2000)
        page.goto(
            f"https://studio.youtube.com/video/{video_id}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        chip = clean.visibility_chip(page)
        r["after2"] = {"chip": chip[:160], "vis": clean.classify(chip)}
        r["ok"] = r["after2"]["vis"] == target
    return r


def main() -> None:
    force = load(HELPER, "force")
    clean = load(CLEANUP, "clean")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    result: dict = {"publicize": [], "private": [], "scheduled_ok": []}

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

        for vid in PUBLICIZE:
            print(f"=== PUBLIC {vid} ===", flush=True)
            row = set_vis(clean, force, page, vid, "public")
            result["publicize"].append(row)
            print(json.dumps({k: row.get(k) for k in ("id", "ok", "before", "after", "after2", "abc_continue")}, indent=2), flush=True)

        for vid in FORCE_PRIVATE:
            print(f"=== PRIVATE {vid} ===", flush=True)
            try:
                row = set_vis(clean, force, page, vid, "private")
            except Exception as e:
                row = {"id": vid, "ok": False, "error": str(e)[:200]}
            result["private"].append(row)
            print(json.dumps({k: row.get(k) for k in ("id", "ok", "before", "after", "after2", "error", "abc_continue")}, indent=2), flush=True)

        for vid in KEEP_SCHEDULED:
            page.goto(
                f"https://studio.youtube.com/video/{vid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(2500)
            chip = clean.visibility_chip(page)
            body = page.locator("body").inner_text()
            result["scheduled_ok"].append(
                {
                    "id": vid,
                    "vis": clean.classify(chip),
                    "chip": chip[:120],
                    "smooth_file": "smooth_normal" in body or "SMOOTH" in body,
                }
            )

        if not FORCE_CDP:
            context.close()

    result["ok"] = all(x.get("ok") for x in result["publicize"]) and any(
        x.get("id") == "3xrxdmaOwJI" and x.get("ok") for x in result["private"]
    )
    OUT.write_text(json.dumps(result, indent=2))
    print("Wrote", OUT, "ok=", result["ok"], flush=True)


if __name__ == "__main__":
    main()
