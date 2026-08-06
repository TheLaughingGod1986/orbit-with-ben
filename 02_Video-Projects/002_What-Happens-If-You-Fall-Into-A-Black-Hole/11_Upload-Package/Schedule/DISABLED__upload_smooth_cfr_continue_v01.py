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
"""Continue smooth CFR publish: publicize RCs6MMxF3ko, upload Shorts, demote old."""
from __future__ import annotations

import importlib.util
import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-from-chrome"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
BH = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
JWST_UP = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "004_JWST-Discoveries-That-Change-Everything/11_Upload-Package/Schedule/"
    "_upload_jwst_v03_all_v01.py"
)
FORCE = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "004_JWST-Discoveries-That-Change-Everything/11_Upload-Package/Schedule/"
    "_force_schedule_shorts_v01.py"
)
NS = BH / "11_Upload-Package/Schedule/_upload_normal_speed_and_micros_v01.py"
AUDIT = BH / "11_Upload-Package/Schedule/_studio_audit_smooth_upload"
OUT = BH / "11_Upload-Package/Schedule/smooth_cfr_upload_result.json"
CATALOG = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "vidiq_full_catalog_2026-08-06/CATALOG.json"
)

NEW_LONG = "RCs6MMxF3ko"
OLD_LONG = "3xrxdmaOwJI"

SHORTS = [
    {
        "tag": "s01",
        "old_id": "JRfhE6yWom4",
        "title": "Cross This Line and You Never Come Back",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-01_event-horizon_v04_smooth_normal.mp4",
        "schedule_iso": None,
        "needle": "v04_smooth_normal",
    },
    {
        "tag": "s02",
        "old_id": "L2OFjL4neOo",
        "title": "Falling In Wouldn't Feel Like Falling",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-02_spaghettification_v04_smooth_normal.mp4",
        "schedule_iso": "2026-08-06T12:30:00+01:00",
        "needle": "v04_smooth_normal",
    },
    {
        "tag": "nf01",
        "old_id": "tUAdhOnMW2g",
        "title": "Time Appears to Stop at a Black Hole",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_nf01_time-appears-to-stop_v03_smooth_normal.mp4",
        "schedule_iso": "2026-08-07T12:30:00+01:00",
        "needle": "v03_smooth_normal",
    },
    {
        "tag": "s04",
        "old_id": "svYOx07OrIM",
        "title": "Would You Look Back?",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-04_look-back_v04_smooth_normal.mp4",
        "schedule_iso": "2026-08-08T12:30:00+01:00",
        "needle": "v04_smooth_normal",
    },
    {
        "tag": "nf02",
        "old_id": "B2STcIAF1lY",
        "title": "What You Would See Falling Into a Black Hole",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_nf02_what-you-would-see_v03_smooth_normal.mp4",
        "schedule_iso": "2026-08-09T12:30:00+01:00",
        "needle": "v03_smooth_normal",
    },
    {
        "tag": "s06",
        "old_id": "w1ej9u0rPTA",
        "title": "The Point of No Return Explained",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-06_point-of-no-return_v04_smooth_normal.mp4",
        "schedule_iso": "2026-08-10T12:30:00+01:00",
        "needle": "v04_smooth_normal",
    },
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def catalog_ids() -> set[str]:
    ids: set[str] = set()
    if CATALOG.exists():
        data = json.loads(CATALOG.read_text())
        # flexible shapes
        if isinstance(data, list):
            for row in data:
                if isinstance(row, dict):
                    for k in ("id", "video_id", "videoId"):
                        if row.get(k):
                            ids.add(row[k])
        elif isinstance(data, dict):
            for v in data.values():
                if isinstance(v, dict) and v.get("id"):
                    ids.add(v["id"])
                if isinstance(v, list):
                    for row in v:
                        if isinstance(row, dict) and row.get("id"):
                            ids.add(row["id"])
                        elif isinstance(row, str) and len(row) >= 6:
                            ids.add(row)
    # known BH + others
    ids.update(
        {
            OLD_LONG,
            NEW_LONG,
            "n7CbJrOCnU0",
            "tfTkMdE7qqw",
            "1wxUhF3XnwI",
            "b8-X_FyJnHM",
            "Mo93x0fxB1Q",
            "JRfhE6yWom4",
            "L2OFjL4neOo",
            "tUAdhOnMW2g",
            "svYOx07OrIM",
            "B2STcIAF1lY",
            "w1ej9u0rPTA",
            "HvAKGjx4lv0",
            "icedH_gK8JE",
            "2777WlMGM8M",
            "jyzrl9ueKq4",
            "EO-44QH4glI",
            "t1hTGIH8O44",
            "nX84ileqPKw",
            "5jjJ5CHrbCs",
        }
    )
    return ids


def short_desc(long_url: str) -> str:
    return (
        "One moment from the full black hole journey.\n\n"
        f"Full film on YouTube:\n{long_url}\n\n"
        "#Space #Shorts #OrbitWithBen #Astronomy #BlackHole"
    )


def extract_fresh_vid(page, exclude: set[str], needle: str) -> str:
    """Prefer udvid; then dialog links not in exclude; require needle in dialog if present."""
    exclude = set(exclude)
    m = re.search(r"[?&]udvid=([A-Za-z0-9_-]{6,})", page.url)
    if m and m.group(1) not in exclude:
        return m.group(1)
    dialog = ""
    try:
        if page.locator("ytcp-uploads-dialog").count():
            dialog = page.locator("ytcp-uploads-dialog").inner_text()
    except Exception:
        dialog = ""
    # If needle present, only accept IDs from dialog text/hrefs
    try:
        hrefs = page.evaluate(
            """() => {
              const root=document.querySelector('ytcp-uploads-dialog')||document;
              return [...root.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')||'');
            }"""
        )
        for href in hrefs or []:
            for pat in (
                r"youtu\.be/([A-Za-z0-9_-]{6,})",
                r"youtube\.com/shorts/([A-Za-z0-9_-]{6,})",
                r"youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})",
                r"/video/([A-Za-z0-9_-]{6,})",
            ):
                m = re.search(pat, href or "")
                if m and m.group(1) not in exclude:
                    if not needle or needle in dialog or not dialog:
                        return m.group(1)
    except Exception:
        pass
    text = dialog
    for pat in (
        r"Video link\s*\n?\s*https://youtu\.be/([A-Za-z0-9_-]{6,})",
        r"Video link\s*\n?\s*https://(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]{6,})",
        r"youtu\.be/([A-Za-z0-9_-]{6,})",
    ):
        m = re.search(pat, text, re.I)
        if m and m.group(1) not in exclude:
            return m.group(1)
    return ""


def set_public(page, force) -> bool:
    force.dismiss(page)
    try:
        force.open_visibility(page)
    except Exception:
        try:
            page.locator("ytcp-video-metadata-visibility").first.click(force=True)
            page.wait_for_timeout(1000)
        except Exception:
            return False
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
    page.wait_for_timeout(600)
    for label in (r"^Done$", r"^Save$", r"^Save as public$"):
        b = page.get_by_role("button", name=re.compile(label, re.I))
        if b.count() and b.first.is_enabled():
            try:
                b.first.click(force=True)
                page.wait_for_timeout(2000)
                break
            except Exception:
                pass
    try:
        sb = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if sb.count() and sb.first.is_enabled():
            sb.first.click(force=True)
            page.wait_for_timeout(2500)
    except Exception:
        pass
    return "Public" in page.locator("body").inner_text()


def upload_short(page, ns, up, force, item: dict, long_url: str, exclude: set[str]) -> dict:
    # Monkey-patch extract during this call via local wrapper
    orig = up.extract_vid

    def patched(page, *, exclude=None):
        ex = set(exclude or ())
        vid = extract_fresh_vid(page, ex, item["needle"])
        if vid:
            return vid
        return orig(page, exclude=ex)

    up.extract_vid = patched
    try:
        r = ns.upload_file(
            page,
            up,
            path=item["file"],
            title=item["title"],
            desc=short_desc(long_url),
            tag=f"smooth_{item['tag']}",
            exclude=exclude,
        )
    finally:
        up.extract_vid = orig
    r["tag"] = item["tag"]
    r["old_id"] = item["old_id"]
    r["schedule_iso"] = item["schedule_iso"]
    vid = r.get("video_id") or ""
    if vid and vid in exclude:
        r["ok"] = False
        r["error"] = f"extracted_known_id:{vid}"
        return r
    if not vid or not r.get("ok"):
        return r
    if item["schedule_iso"]:
        try:
            day, month_num, time_str = force.parse_iso(item["schedule_iso"])
            r["schedule"] = force.schedule_one(
                page, vid, day, month_num, time_str, item["tag"]
            )
        except Exception as e:
            r["schedule_error"] = str(e)[:200]
    else:
        page.goto(
            f"https://studio.youtube.com/video/{vid}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        force.dismiss(page)
        r["public"] = set_public(page, force)
    return r


def main() -> None:
    ns = load(NS, "ns")
    up = load(JWST_UP, "up")
    force = load(FORCE, "force")
    AUDIT.mkdir(parents=True, exist_ok=True)
    exclude = catalog_ids()
    long_url = f"https://youtu.be/{NEW_LONG}"
    result: dict = {
        "ok": False,
        "long": {"video_id": NEW_LONG, "url": long_url, "file": "v06_SMOOTH"},
        "shorts": [],
        "demotions": [],
    }

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        print("=== PUBLICIZE LONG", NEW_LONG, "===", flush=True)
        page.goto(
            f"https://studio.youtube.com/video/{NEW_LONG}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        force.dismiss(page)
        # confirm filename
        body = page.locator("body").inner_text()
        assert "SMOOTH" in body, "expected smooth master on new long"
        result["long"]["public"] = set_public(page, force)
        print("long public", result["long"]["public"], flush=True)
        page.screenshot(path=str(AUDIT / "long_public.png"), full_page=True)

        for item in SHORTS:
            assert item["file"].exists(), item["file"]
            print(f"=== UPLOAD {item['tag']} ===", flush=True)
            r = upload_short(page, ns, up, force, item, long_url, exclude)
            result["shorts"].append(r)
            print(json.dumps({k: r.get(k) for k in ("tag", "ok", "video_id", "error", "public", "schedule_iso")}, indent=2), flush=True)
            if r.get("video_id"):
                exclude.add(r["video_id"])

        # Demote old juddery
        for oid in [OLD_LONG, *(s["old_id"] for s in SHORTS)]:
            print(f"=== DEMOTE {oid} ===", flush=True)
            try:
                d = ns.demote_to_private(page, force, oid, f"demote_{oid}")
            except Exception as e:
                d = {"video_id": oid, "ok": False, "error": str(e)[:200]}
            result["demotions"].append(d)
            print(json.dumps(d, indent=2)[:300], flush=True)

        ctx.close()

    result["ok"] = bool(result["long"].get("public")) and all(
        s.get("ok") for s in result["shorts"]
    )
    OUT.write_text(json.dumps(result, indent=2))
    print("Wrote", OUT, flush=True)
    print("OVERALL", result["ok"], flush=True)
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
