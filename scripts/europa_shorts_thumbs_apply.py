#!/usr/bin/env python3
"""Apply Europa Short yellow+white covers in desktop Studio via CDP.

Never uses Data API thumbnails.set (letterboxes 9:16). Never touches Replace.
Writes /tmp/europa_thumbs_studio_apply_result.json and screenshots under
/tmp/europa_thumbs_apply/.
Exit 2 if Studio CDP is on Google login (BLOCKED_NEED_BEN_LOGIN).
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHORTS_ROOT = ROOT / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts"
COVERS = SHORTS_ROOT / "08_Thumbs/yellow_white_v01"
RELATED = "NbW5G1BpPY0"
CDP = "http://127.0.0.1:9222"
OUT = Path("/tmp/europa_thumbs_studio_apply_result.json")
SHOTS = Path("/tmp/europa_thumbs_apply")

# Live Studio cluster resolved 2 Sep 2026. Leftover private ids stay off this list.
SHORTS = [
    {"id": "FbRFvSApfOQ", "schedule": "2026-09-03T20:00 Europe/London", "cover": "cover_FbRFvSApfOQ.jpg"},
    {"id": "8Bym-yrYhGc", "schedule": "2026-09-04T11:30 Europe/London", "cover": "cover_8Bym-yrYhGc.jpg"},
    {"id": "1glQuYFSaYQ", "schedule": "2026-09-05T11:30 Europe/London", "cover": "cover_1glQuYFSaYQ.jpg"},
    {"id": "Xza_jSHD4qw", "schedule": "2026-09-06T11:30 Europe/London", "cover": "cover_Xza_jSHD4qw.jpg"},
    {"id": "VE0f186WQZo", "schedule": "2026-09-07T11:30 Europe/London", "cover": "cover_VE0f186WQZo.jpg"},
    {"id": "D3KSYrqip5A", "schedule": "2026-09-08T11:30 Europe/London", "cover": "cover_D3KSYrqip5A.jpg"},
    {"id": "eVp9a7f4rWg", "schedule": "2026-09-09T11:30 Europe/London", "cover": "cover_eVp9a7f4rWg.jpg"},
    {"id": "TE_HDKAnqms", "schedule": "2026-09-10T11:30 Europe/London", "cover": "cover_TE_HDKAnqms.jpg"},
]


def cdp_list() -> list[dict]:
    try:
        with urllib.request.urlopen(f"{CDP}/json/list", timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        return []


def _page_urls() -> list[str]:
    return [t.get("url", "") for t in cdp_list() if t.get("type") == "page"]


def cdp_has_studio() -> bool:
    return any(u.startswith("https://studio.youtube.com") for u in _page_urls())


def cdp_only_login() -> bool:
    urls = _page_urls()
    if not urls:
        return False
    has_studio = any(u.startswith("https://studio.youtube.com") for u in urls)
    has_login = any("accounts.google.com" in u for u in urls)
    return has_login and not has_studio


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


def click_upload_thumbnail(page) -> str | None:
    """Open Studio's custom thumbnail picker. Never click Replace."""
    found = page.evaluate(
        """() => {
          const skip = /replace|video file|upload video/i;
          const hit = (el) => {
            const t = ((el.innerText || '') + ' ' + (el.getAttribute('aria-label') || '')).replace(/\\s+/g, ' ').trim();
            if (skip.test(t)) return null;
            if (/upload thumbnail|custom thumbnail|upload file/i.test(t) && /thumb/i.test(t + ' ' + (el.closest('[id],[class]')?.className || ''))) {
              const r = el.getBoundingClientRect();
              if (r.width > 8 && r.height > 8) { el.click(); return t.slice(0, 80); }
            }
            if (/^upload thumbnail$/i.test(t) || /upload thumbnail/i.test(t)) {
              const r = el.getBoundingClientRect();
              if (r.width > 8 && r.height > 8) { el.click(); return t.slice(0, 80); }
            }
            return null;
          };
          const walk = (root) => {
            for (const el of root.querySelectorAll('button,ytcp-button,[role=button],ytcp-icon-button,a,span,div,ytcp-thumbnails-compact-editor-uploader-old')) {
              const t = hit(el);
              if (t) return t;
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) {
                const t = walk(el.shadowRoot);
                if (t) return t;
              }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    return found


def image_file_inputs(page):
    loc = page.locator('input[type="file"][accept*="image"]')
    if loc.count():
        return loc
    # Some Studio builds omit accept=; still refuse video-only inputs.
    all_files = page.locator('input[type="file"]')
    return all_files


def upload_cover(page, cover: Path) -> tuple[bool, str]:
    click_upload_thumbnail(page)
    page.wait_for_timeout(600)

    loc = image_file_inputs(page)
    n = loc.count()
    last = "no usable image input"
    if n:
        for i in range(n):
            accept = (loc.nth(i).get_attribute("accept") or "").lower()
            if "video" in accept and "image" not in accept:
                continue
            try:
                loc.nth(i).set_input_files(str(cover))
                return True, f"input[{i}] accept={accept!r}"
            except Exception as e:
                last = f"input[{i}]: {e}"

    try:
        with page.expect_file_chooser(timeout=8000) as fc:
            clicked = click_upload_thumbnail(page)
            if not clicked:
                raise RuntimeError("no Upload thumbnail control")
        fc.value.set_files(str(cover))
        return True, f"file_chooser:{clicked}"
    except Exception as e:
        return False, f"chooser: {e}"


def click_save(page) -> bool:
    for label in ("Save", "Save changes", "Publish"):
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{label}$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=3000)
                page.wait_for_timeout(2500)
                return True
        except Exception:
            continue
    return False


def scrape_state(page) -> dict:
    try:
        body = page.inner_text("body")
    except Exception:
        body = ""
    schedule = None
    for needle in (
        "3 Sept 2026",
        "3 Sep 2026",
        "4 Sept 2026",
        "4 Sep 2026",
        "5 Sept 2026",
        "5 Sep 2026",
        "6 Sept 2026",
        "6 Sep 2026",
        "7 Sept 2026",
        "7 Sep 2026",
        "8 Sept 2026",
        "8 Sep 2026",
        "9 Sept 2026",
        "9 Sep 2026",
        "10 Sept 2026",
        "10 Sep 2026",
        "Scheduled",
        "Premiere",
        "Public",
        "Private",
    ):
        if needle in body:
            schedule = needle
            break
    related = RELATED if RELATED in body else None
    if not related:
        for txt in ("Could Life Exist Under The Ice Of Europa", "Related video"):
            if txt in body:
                related = f"partial:{txt}"
                break
    return {"schedule_visible": schedule, "related_visible": related, "url": page.url}


def open_edit(page, vid: str, alt_id: str | None) -> tuple[str, bool]:
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(2800)
    dismiss(page)
    if "/video/" + vid + "/" in page.url and "accounts.google.com" not in page.url:
        # 404 / missing still lands on an edit URL sometimes — look for error copy.
        try:
            body = page.inner_text("body")
        except Exception:
            body = ""
        if "isn't available" in body or "Video not found" in body or "couldn't find" in body.lower():
            if alt_id:
                page.goto(
                    f"https://studio.youtube.com/video/{alt_id}/edit",
                    wait_until="domcontentloaded",
                    timeout=90000,
                )
                page.wait_for_timeout(2800)
                dismiss(page)
                return alt_id, True
        return vid, False
    if alt_id:
        page.goto(f"https://studio.youtube.com/video/{alt_id}/edit", wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(2800)
        dismiss(page)
        return alt_id, True
    return vid, False


def studio_apply_thumbs() -> tuple[list[dict], bool]:
    from playwright.sync_api import sync_playwright

    SHOTS.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = next((pg for pg in ctx.pages if "studio.youtube.com" in pg.url), None)
        if not page:
            page = ctx.new_page()
            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(4000)

        if "accounts.google.com" in page.url:
            return results, True

        for i, s in enumerate(SHORTS, start=1):
            cover = COVERS / s["cover"]
            row: dict = {
                "id": s["id"],
                "applied_id": s["id"],
                "used_alt_id": False,
                "schedule_expected": s["schedule"],
                "cover": s["cover"],
                "cover_exists": cover.exists(),
                "related_target": RELATED,
                "studio_thumb_uploaded": False,
                "upload_how": None,
                "saved": False,
                "schedule_visible": None,
                "related_visible": None,
                "screenshot": None,
                "error": None,
            }
            if not cover.exists():
                row["error"] = "missing cover"
                results.append(row)
                continue

            try:
                applied, used_alt = open_edit(page, s["id"], s.get("alt_id"))
                row["applied_id"] = applied
                row["used_alt_id"] = used_alt
                if "accounts.google.com" in page.url:
                    row["error"] = "BLOCKED_NEED_BEN_LOGIN"
                    results.append(row)
                    return results, True

                ok, how = upload_cover(page, cover)
                row["studio_thumb_uploaded"] = ok
                row["upload_how"] = how
                if not ok:
                    row["error"] = how
                page.wait_for_timeout(2200)
                row["saved"] = click_save(page)
                state = scrape_state(page)
                row["schedule_visible"] = state["schedule_visible"]
                row["related_visible"] = state["related_visible"]
                shot = SHOTS / f"{i:02d}_{applied}.png"
                page.screenshot(path=str(shot), full_page=False)
                row["screenshot"] = str(shot)
            except Exception as e:
                row["error"] = str(e)[:400]
            results.append(row)
    return results, False


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    report: dict = {
        "task": "europa_shorts_yellow_white_thumbs",
        "started_at": started,
        "related_target": RELATED,
        "covers_dir": str(COVERS),
        "cdp": CDP,
        "covers_found": {s["id"]: (COVERS / s["cover"]).exists() for s in SHORTS},
        "studio_blocked": False,
        "studio_results": [],
        "exit_reason": None,
        "note": "Studio CDP only — no thumbnails.set (letterboxes Shorts).",
    }

    missing = [s["id"] for s in SHORTS if not (COVERS / s["cover"]).exists()]
    if missing:
        report["exit_reason"] = f"missing_covers:{missing}"
        OUT.write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        return 1

    report["cdp_tabs"] = [u[:200] for u in _page_urls()]
    if cdp_only_login():
        report["studio_blocked"] = True
        report["exit_reason"] = "BLOCKED_NEED_BEN_LOGIN"
        report["next_step"] = (
            "On Mac: bash 00_Brand/Channel-Setup/audits/start_studio_chrome_cdp.sh "
            "— complete Google login + 2FA — then re-run this script."
        )
        OUT.write_text(json.dumps(report, indent=2))
        print("BLOCKED_NEED_BEN_LOGIN")
        print(json.dumps(report, indent=2))
        return 2

    for _ in range(5):
        if cdp_has_studio():
            break
        time.sleep(3)

    if not cdp_list():
        report["exit_reason"] = "CDP_NOT_RUNNING"
        OUT.write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        return 1

    try:
        studio_results, blocked = studio_apply_thumbs()
        report["studio_results"] = studio_results
        if blocked:
            report["studio_blocked"] = True
            report["exit_reason"] = "BLOCKED_NEED_BEN_LOGIN"
            OUT.write_text(json.dumps(report, indent=2))
            print("BLOCKED_NEED_BEN_LOGIN")
            print(json.dumps(report, indent=2))
            return 2
    except Exception as e:
        report["exit_reason"] = f"studio_error:{e}"
        OUT.write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        return 1

    ok = bool(report["studio_results"]) and all(r.get("studio_thumb_uploaded") for r in report["studio_results"])
    report["exit_reason"] = "success" if ok else "partial_or_failed"
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
