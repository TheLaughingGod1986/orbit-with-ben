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
"""Re-upload BH long + active Shorts with smooth CFR masters; demote old IDs.

Studio has no Replace for this channel (Options = Download/Delete/Promote only),
so new uploads are required to fix the setpts-judder masters live on YouTube.
"""
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
AUDIT = BH / "11_Upload-Package/Schedule/_studio_audit_smooth_upload"
OUT = BH / "11_Upload-Package/Schedule/smooth_cfr_upload_result.json"

# Import helpers from prior normal-speed uploader
NS = BH / "11_Upload-Package/Schedule/_upload_normal_speed_and_micros_v01.py"

LONG = {
    "old_id": "3xrxdmaOwJI",
    "title": "What Happens If You Fall Into a Black Hole? Orbit's Cosmic Journey",
    "file": BH / "09_Final-Export/blackhole_v06_SMOOTH_NORMAL_UPLOAD_READY_MASTER.mp4",
    "schedule_iso": None,  # publish Public immediately after upload
}

SHORTS = [
    {
        "tag": "s01",
        "old_id": "JRfhE6yWom4",
        "title": "Cross This Line and You Never Come Back",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-01_event-horizon_v04_smooth_normal.mp4",
        "schedule_iso": None,  # was live — publish now
    },
    {
        "tag": "s02",
        "old_id": "L2OFjL4neOo",
        "title": "Falling In Wouldn't Feel Like Falling",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-02_spaghettification_v04_smooth_normal.mp4",
        "schedule_iso": "2026-08-06T12:30:00+01:00",
    },
    {
        "tag": "nf01",
        "old_id": "tUAdhOnMW2g",
        "title": "Time Appears to Stop at a Black Hole",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_nf01_time-appears-to-stop_v03_smooth_normal.mp4",
        "schedule_iso": "2026-08-07T12:30:00+01:00",
    },
    {
        "tag": "s04",
        "old_id": "svYOx07OrIM",
        "title": "Would You Look Back?",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-04_look-back_v04_smooth_normal.mp4",
        "schedule_iso": "2026-08-08T12:30:00+01:00",
    },
    {
        "tag": "nf02",
        "old_id": "B2STcIAF1lY",
        "title": "What You Would See Falling Into a Black Hole",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_nf02_what-you-would-see_v03_smooth_normal.mp4",
        "schedule_iso": "2026-08-09T12:30:00+01:00",
    },
    {
        "tag": "s06",
        "old_id": "w1ej9u0rPTA",
        "title": "The Point of No Return Explained",
        "file": BH
        / "10_Shorts/06_Final-Exports/blackhole_short-06_point-of-no-return_v04_smooth_normal.mp4",
        "schedule_iso": "2026-08-10T12:30:00+01:00",
    },
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def short_desc(long_url: str) -> str:
    return (
        "One moment from the full black hole journey.\n\n"
        f"Full film on YouTube:\n{long_url}\n\n"
        "#Space #Shorts #OrbitWithBen #Astronomy #BlackHole"
    )


def long_desc() -> str:
    # Pull from Studio later if needed; keep chapters + CTA shell
    return (
        "Orbit — a small orange exploration robot — asks what really happens "
        "if you fall into a black hole.\n\n"
        "Chapters\n"
        "0:00 — Orbit's question\n"
        "0:33 — What is a black hole?\n"
        "1:31 — Black hole myths\n"
        "2:23 — How black holes are born\n"
        "4:35 — Event horizon explained\n"
        "6:22 — Approaching the event horizon\n"
        "9:13 — Time dilation\n"
        "11:00 — Spaghettification\n"
        "12:42 — Crossing — the point of no return\n"
        "14:11 — Inside a black hole — the singularity\n"
        "15:37 — Hawking radiation & black hole facts\n"
        "16:51 — Spinning holes and near misses\n"
        "17:38 — Supermassive engines\n"
        "18:14 — What we still don't know\n"
        "19:17 — Closing — more cosmic journeys\n\n"
        "#Space #BlackHole #Astronomy #OrbitWithBen #Science"
    )


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
    # Save page
    try:
        page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first.click(force=True)
        page.wait_for_timeout(2500)
    except Exception:
        pass
    return "Public" in page.locator("body").inner_text()


def main() -> None:
    for job in [LONG, *SHORTS]:
        assert Path(job["file"]).exists(), job["file"]

    ns = load(NS, "ns")
    up = load(JWST_UP, "up")
    force = load(FORCE, "force")

    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "ok": False,
        "long": None,
        "shorts": [],
        "demotions": [],
        "note": "Studio Replace unavailable; new uploads + demote old",
    }
    exclude: set[str] = {LONG["old_id"], *(s["old_id"] for s in SHORTS)}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)

        print("=== UPLOAD LONG ===", flush=True)
        long_r = ns.upload_file(
            page,
            up,
            path=LONG["file"],
            title=LONG["title"],
            desc=long_desc(),
            tag="smooth_long",
            exclude=exclude,
        )
        result["long"] = long_r
        print(json.dumps(long_r, indent=2)[:600], flush=True)
        long_id = long_r.get("video_id") or ""
        if long_id:
            exclude.add(long_id)
            # Publish Public
            page.goto(
                f"https://studio.youtube.com/video/{long_id}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3500)
            force.dismiss(page)
            result["long"]["public"] = set_public(page, force)
            print("long public", result["long"]["public"], flush=True)

        long_url = f"https://youtu.be/{long_id}" if long_id else "https://youtu.be/3xrxdmaOwJI"

        for item in SHORTS:
            print(f"=== UPLOAD {item['tag']} ===", flush=True)
            r = ns.upload_file(
                page,
                up,
                path=item["file"],
                title=item["title"],
                desc=short_desc(long_url),
                tag=f"smooth_{item['tag']}",
                exclude=exclude,
            )
            r["tag"] = item["tag"]
            r["old_id"] = item["old_id"]
            r["schedule_iso"] = item["schedule_iso"]
            result["shorts"].append(r)
            print(json.dumps(r, indent=2)[:500], flush=True)
            vid = r.get("video_id") or ""
            if not vid:
                continue
            exclude.add(vid)
            if item["schedule_iso"]:
                try:
                    day, month_num, time_str = force.parse_iso(item["schedule_iso"])
                    sched = force.schedule_one(
                        page, vid, day, month_num, time_str, item["tag"]
                    )
                    r["schedule"] = sched
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

        # Demote old juddery IDs
        for oid in [LONG["old_id"], *(s["old_id"] for s in SHORTS)]:
            print(f"=== DEMOTE {oid} ===", flush=True)
            try:
                d = ns.demote_to_private(page, force, oid, f"demote_{oid}")
            except Exception as e:
                d = {"video_id": oid, "ok": False, "error": str(e)[:200]}
            result["demotions"].append(d)
            print(json.dumps(d, indent=2)[:400], flush=True)

        ctx.close()

    result["ok"] = bool(result.get("long", {}).get("ok")) and all(
        s.get("ok") for s in result["shorts"]
    )
    OUT.write_text(json.dumps(result, indent=2))
    print("Wrote", OUT, flush=True)
    print("OVERALL", result["ok"], flush=True)
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
