#!/usr/bin/env python3
"""Apply yellow_white_v03 covers in desktop Studio via CDP.

Winner overlay style (lowercase rounded punch). new_page per listing.
Wait until the video id is in the URL before upload.
Image-only file inputs. Never Replace / video file. Never thumbnails.set.
Do not open visibility / change dates.
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CDP = "http://127.0.0.1:9222"
OUT = Path("/tmp/orbit_thumbs_v03_apply_result.json")
SHOTS = Path("/tmp/orbit_thumbs_v03_apply")

EU = ROOT / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v03"
NS = ROOT / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/yellow_white_v03"
LS = ROOT / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/08_Thumbs/yellow_white_v03"

SHORTS = [
    {"id": "FbRFvSApfOQ", "cover": EU / "cover_FbRFvSApfOQ.jpg", "related": "NbW5G1BpPY0"},
    {"id": "eVp9a7f4rWg", "cover": EU / "cover_eVp9a7f4rWg.jpg", "related": "NbW5G1BpPY0"},
    {"id": "8Bym-yrYhGc", "cover": EU / "cover_8Bym-yrYhGc.jpg", "related": "NbW5G1BpPY0"},
    {"id": "1glQuYFSaYQ", "cover": EU / "cover_1glQuYFSaYQ.jpg", "related": "NbW5G1BpPY0"},
    {"id": "Xza_jSHD4qw", "cover": EU / "cover_Xza_jSHD4qw.jpg", "related": "NbW5G1BpPY0"},
    {"id": "VE0f186WQZo", "cover": EU / "cover_VE0f186WQZo.jpg", "related": "NbW5G1BpPY0"},
    {"id": "D3KSYrqip5A", "cover": EU / "cover_D3KSYrqip5A.jpg", "related": "NbW5G1BpPY0"},
    {"id": "TE_HDKAnqms", "cover": EU / "cover_TE_HDKAnqms.jpg", "related": "NbW5G1BpPY0"},
    {"id": "92vmMxSNmlk", "cover": NS / "cover_92vmMxSNmlk.jpg", "related": "Yk1tLh23rko"},
    {"id": "vCxXTYXSSqY", "cover": NS / "cover_vCxXTYXSSqY.jpg", "related": "Yk1tLh23rko"},
    {"id": "va5ATScn3rs", "cover": NS / "cover_va5ATScn3rs.jpg", "related": "Yk1tLh23rko"},
    {"id": "o7ykyTDZKiE", "cover": NS / "cover_o7ykyTDZKiE.jpg", "related": "Yk1tLh23rko"},
    {"id": "Rp_8J6_6IIk", "cover": NS / "cover_Rp_8J6_6IIk.jpg", "related": "Yk1tLh23rko"},
    {"id": "0j_pgYbCe5E", "cover": LS / "cover_0j_pgYbCe5E.jpg", "related": "REXYxuLOBoI"},
]


def cdp_list() -> list[dict]:
    try:
        with urllib.request.urlopen(f"{CDP}/json/list", timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        return []


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


def click_upload_thumbnail(page) -> str | None:
    return page.evaluate(
        """() => {
          const skip = /replace|video file|upload video/i;
          const hit = (el) => {
            const t = ((el.innerText || '') + ' ' + (el.getAttribute('aria-label') || '')).replace(/\\s+/g, ' ').trim();
            if (skip.test(t)) return null;
            if (/upload thumbnail|custom thumbnail/i.test(t)) {
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


def upload_cover(page, cover: Path) -> tuple[bool, str]:
    click_upload_thumbnail(page)
    page.wait_for_timeout(600)
    loc = page.locator('input[type="file"][accept*="image"]')
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
        return False, f"{last}; chooser: {e}"


def click_save(page) -> bool:
    for label in ("Save", "Save changes"):
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{label}$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=3000)
                page.wait_for_timeout(2500)
                return True
        except Exception:
            continue
    return False


def apply_one(ctx, s: dict, i: int) -> dict:
    vid = s["id"]
    cover: Path = s["cover"]
    row = {
        "id": vid,
        "cover": str(cover),
        "related_target": s["related"],
        "studio_thumb_uploaded": False,
        "saved": False,
        "url": None,
        "error": None,
    }
    if not cover.exists():
        row["error"] = "missing cover"
        return row
    page = ctx.new_page()
    try:
        page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(2800)
        if "accounts.google.com" in page.url:
            row["error"] = "BLOCKED_NEED_BEN_LOGIN"
            return row
        if f"/video/{vid}/" not in page.url:
            row["error"] = f"url_mismatch:{page.url[:180]}"
            return row
        dismiss(page)
        ok, how = upload_cover(page, cover)
        row["studio_thumb_uploaded"] = ok
        row["upload_how"] = how
        if not ok:
            row["error"] = how
        else:
            page.wait_for_timeout(1800)
            row["saved"] = click_save(page)
        row["url"] = page.url
        shot = SHOTS / f"{i:02d}_{vid}.png"
        page.screenshot(path=str(shot), full_page=False)
        row["screenshot"] = str(shot)
    except Exception as e:
        row["error"] = str(e)[:400]
    finally:
        page.close()
    return row


def main() -> int:
    SHOTS.mkdir(parents=True, exist_ok=True)
    report = {
        "task": "yellow_white_v03_thumbs",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "cdp_tabs": [t.get("url", "")[:180] for t in cdp_list() if t.get("type") == "page"],
        "studio_results": [],
    }
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        for i, s in enumerate(SHORTS, start=1):
            print(f"{i:02d} {s['id']}", flush=True)
            row = apply_one(ctx, s, i)
            report["studio_results"].append(row)
            print(json.dumps({k: row.get(k) for k in ("id", "studio_thumb_uploaded", "saved", "error")}, indent=2), flush=True)
            if row.get("error") == "BLOCKED_NEED_BEN_LOGIN":
                break
            time.sleep(0.4)
    ok = bool(report["studio_results"]) and all(
        r.get("studio_thumb_uploaded") and r.get("saved") for r in report["studio_results"]
    )
    report["exit_reason"] = "success" if ok else "partial_or_failed"
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps({"exit": report["exit_reason"], "n": len(report["studio_results"])}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
