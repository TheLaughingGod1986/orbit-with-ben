#!/usr/bin/env python3
"""Apply Europa Short yellow+white covers via YouTube Data API (if OAuth) + Studio CDP.

Writes /tmp/europa_thumbs_studio_apply_result.json
Exit 2 if Studio CDP blocked on Google login (BLOCKED_NEED_BEN_LOGIN).
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHORTS_ROOT = ROOT / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts"
COVERS = SHORTS_ROOT / "08_Thumbs/yellow_white_v01"
RELATED = "NbW5G1BpPY0"
CDP = "http://127.0.0.1:9222"
OUT = Path("/tmp/europa_thumbs_studio_apply_result.json")

SHORTS = [
    {"id": "FbRFvSApfOQ", "schedule": "2026-09-03T20:00 Europe/London", "cover": "cover_FbRFvSApfOQ.jpg"},
    {"id": "EcsunqhN0jQ", "schedule": "2026-09-04T11:30 Europe/London", "cover": "cover_EcsunqhN0jQ.jpg", "alt_id": "8Bym-yrYhGc"},
    {"id": "k0PjH2I0OxY", "schedule": "2026-09-05T11:30 Europe/London", "cover": "cover_k0PjH2I0OxY.jpg"},
    {"id": "0eqTVgrlU-s", "schedule": "2026-09-06T11:30 Europe/London", "cover": "cover_0eqTVgrlU-s.jpg"},
    {"id": "Fv-lSwB_Z-o", "schedule": "2026-09-07T11:30 Europe/London", "cover": "cover_Fv-lSwB_Z-o.jpg"},
    {"id": "KPO68c-U42E", "schedule": "2026-09-08T11:30 Europe/London", "cover": "cover_KPO68c-U42E.jpg"},
    {"id": "gN2qAv8m9Wc", "schedule": "2026-09-09T11:30 Europe/London", "cover": "cover_gN2qAv8m9Wc.jpg"},
    {"id": "TE_HDKAnqms", "schedule": "2026-09-10T11:30 Europe/London", "cover": "cover_TE_HDKAnqms.jpg"},
]

TOKEN_PATHS = [
    Path.home() / ".config/orbit-youtube/token.json",
    Path.home() / ".config/youtube-oauth/token.json",
    ROOT / "07_Content-Ops/.env",
    ROOT / ".env",
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


def find_oauth_token() -> str | None:
    for p in TOKEN_PATHS:
        if not p.exists():
            continue
        if p.suffix == ".json":
            try:
                data = json.loads(p.read_text())
                for key in ("access_token", "token"):
                    if data.get(key):
                        return data[key]
            except Exception:
                pass
        elif p.name == ".env":
            for line in p.read_text().splitlines():
                if line.startswith("YOUTUBE_ACCESS_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"')
                if line.startswith("GOOGLE_ACCESS_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"')
    return None


def api_set_thumbnail(token: str, video_id: str, cover_path: Path) -> dict:
    """YouTube Data API thumbnails.set — note: letterboxes 9:16 for Shorts."""
    buf = cover_path.read_bytes()
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=buf,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "image/jpeg",
            "Content-Length": str(len(buf)),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return {"ok": True, "status": r.status, "note": "API ok but Shorts may letterbox — verify in Studio"}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        return {"ok": False, "status": e.code, "error": body}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def studio_apply_thumbs() -> tuple[list[dict], bool]:
    from playwright.sync_api import sync_playwright

    results: list[dict] = []
    blocked = False
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = next((pg for pg in ctx.pages if "studio.youtube.com" in pg.url), None)
        if not page:
            page = ctx.new_page()
            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(4000)

        if "accounts.google.com" in page.url:
            blocked = True
            return results, blocked

        for s in SHORTS:
            vid = s["id"]
            cover = COVERS / s["cover"]
            row: dict = {
                "id": vid,
                "schedule_expected": s["schedule"],
                "cover": s["cover"],
                "cover_path": str(cover),
                "cover_exists": cover.exists(),
                "related_target": RELATED,
                "api_thumb": None,
                "studio_thumb_uploaded": False,
                "saved": False,
                "schedule_visible": None,
                "related_visible": None,
                "error": None,
            }
            if not cover.exists():
                row["error"] = "missing cover"
                results.append(row)
                continue

            edit_url = f"https://studio.youtube.com/video/{vid}/edit"
            page.goto(edit_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            # Thumbnail upload
            uploaded = False
            for sel in ['input[type=file][accept*="image"]', 'input[type="file"]']:
                loc = page.locator(sel)
                if loc.count():
                    try:
                        loc.first.set_input_files(str(cover))
                        uploaded = True
                        page.wait_for_timeout(2500)
                        break
                    except Exception as e:
                        row["error"] = f"upload: {e}"
            row["studio_thumb_uploaded"] = uploaded

            # Save if enabled
            for label in ["Save", "Save changes"]:
                btn = page.get_by_role("button", name=label)
                if btn.count() and btn.first.is_enabled():
                    btn.first.click()
                    page.wait_for_timeout(2000)
                    row["saved"] = True
                    break

            # Schedule text (best-effort scrape)
            try:
                body = page.inner_text("body")
                for needle in ["Sep 2026", "2026", "Scheduled", "Public", "Private"]:
                    if needle in body:
                        row["schedule_visible"] = needle
                        break
            except Exception:
                pass

            # Related video (Studio-only field)
            try:
                related_loc = page.get_by_text(RELATED, exact=False)
                if related_loc.count():
                    row["related_visible"] = RELATED
                else:
                    for txt in ["Related video", "Related", "Europa", "Could Life Exist"]:
                        if page.get_by_text(txt, exact=False).count():
                            row["related_visible"] = f"partial:{txt}"
                            break
            except Exception:
                pass

            results.append(row)
    return results, blocked


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    report: dict = {
        "task": "europa_shorts_yellow_white_thumbs",
        "started_at": started,
        "related_target": RELATED,
        "covers_dir": str(COVERS),
        "cdp": CDP,
        "covers_found": {s["id"]: (COVERS / s["cover"]).exists() for s in SHORTS},
        "oauth_token_found": False,
        "api_results": [],
        "studio_blocked": False,
        "studio_results": [],
        "exit_reason": None,
    }

    # Verify covers
    missing = [s["id"] for s in SHORTS if not (COVERS / s["cover"]).exists()]
    if missing:
        report["exit_reason"] = f"missing_covers:{missing}"
        OUT.write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        return 1

    # Early login-block detection (before polling)
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

    # Poll CDP for studio session (up to 15s)
    for _ in range(5):
        if cdp_has_studio():
            break
        time.sleep(3)


    # Try API if token available
    token = find_oauth_token()
    report["oauth_token_found"] = bool(token)
    if token:
        for s in SHORTS:
            cover = COVERS / s["cover"]
            api_res = api_set_thumbnail(token, s["id"], cover)
            report["api_results"].append({"id": s["id"], **api_res})

    # Studio CDP apply (required for Shorts vertical slot)
    if report["studio_blocked"]:
        OUT.write_text(json.dumps(report, indent=2))
        print("BLOCKED_NEED_BEN_LOGIN")
        print(json.dumps(report, indent=2))
        return 2

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

    ok = all(r.get("studio_thumb_uploaded") for r in report["studio_results"])
    report["exit_reason"] = "success" if ok else "partial_or_failed"
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
