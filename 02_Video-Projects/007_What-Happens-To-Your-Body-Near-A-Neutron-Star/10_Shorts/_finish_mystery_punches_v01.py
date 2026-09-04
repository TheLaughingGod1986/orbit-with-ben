#!/usr/bin/env python3
"""Finish mystery punches: schedule+Related for 06, upload+schedule+Related for 07/08."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _upload_schedule_mystery_punches_v01 as U  # noqa: E402

CDP = "http://127.0.0.1:9222"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
LONG_ID = "Yk1tLh23rko"
PILLAR_IDS = {
    LONG_ID,
    "NbW5G1BpPY0",  # Europa — poisoned prior scrape
    "REXYxuLOBoI",
    "Mo93x0fxB1Q",
    "n7CbJrOCnU0",
    "b8-X_FyJnHM",
    "ziKBPJ6FY0U",
    "3xrxdmaOwJI",
    "upload",
    "shorts",
}
MANIFEST = Path(__file__).resolve().parent / "MYSTERY_PUNCHES_15_17_SEP.json"
OUT = Path("/tmp/orbit_neutron_mystery/finish_result.json")
AUDIT = Path("/tmp/orbit_neutron_mystery/upload_audit")
KNOWN_06 = "3QrICn9Kp00"  # Why Does Light Leave Exhausted?


def find_by_title(page, title: str, ban: set[str]) -> str:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/short"
        "?sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    found = page.evaluate(
        """(title) => {
          const as=[...document.querySelectorAll('a[href*="/video/"]')];
          for (const a of as) {
            let el=a, text='';
            for (let i=0;i<8&&el;i++){
              text=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (text.includes(title)) break;
              el=el.parentElement;
            }
            if (!text.includes(title)) continue;
            const m=(a.getAttribute('href')||'').match(/\\/video\\/([\\w-]{11})/);
            if (m) return m[1];
          }
          return '';
        }""",
        title,
    )
    if found and found not in ban:
        return found
    return ""


def open_visibility_safe(page) -> None:
    U.dismiss(page)
    try:
        page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed(
            timeout=8000
        )
        page.locator("ytcp-video-metadata-visibility").first.click(force=True)
        page.wait_for_timeout(1400)
        return
    except Exception:
        pass
    ok = page.evaluate(
        """() => {
          const walk=(root)=>{
            for (const el of root.querySelectorAll('ytcp-video-metadata-visibility')) {
              const r=el.getBoundingClientRect();
              if (r.width>40 && r.height>10) { el.click(); return true; }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
          };
          return walk(document);
        }"""
    )
    if not ok:
        raise RuntimeError("visibility_open_failed")
    page.wait_for_timeout(1400)


def schedule_safe(page, item: dict, video_id: str) -> dict:
    day = int(item["schedule_uk"][8:10])
    result: dict = {
        "id": item["id"],
        "video_id": video_id,
        "ok": False,
        "target": f"{day} Sep 2026 11:30",
    }
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    U.dismiss(page)
    open_visibility_safe(page)
    result["expand"] = U.expand_schedule(page)
    U.set_date_time(page, day, "11:30", result)
    U.click_done(page)
    result["saved"] = U.save_edit(page)
    page.wait_for_timeout(2200)
    body = page.locator("body").inner_text()
    snip = body.split("Visibility", 1)[-1][:220] if "Visibility" in body else body[:220]
    result["visibility_snip"] = snip.replace("\n", " ")
    result["ok"] = "Scheduled" in snip or "11:30" in snip
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"finish_sched_{item['id']}.png"))
    return result


def recover_id(page, item: dict, ban: set[str], claimed: str) -> str:
    if claimed and claimed not in ban:
        return claimed
    return find_by_title(page, item["title"], ban)


def main() -> int:
    AUDIT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text())
    by_id = {s["id"]: s for s in manifest["shorts"]}
    report: dict = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "related_target": LONG_ID,
        "uploads": [],
        "schedules": [],
        "related": [],
    }
    ban = set(PILLAR_IDS) | {KNOWN_06}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        U.ensure_orbit_channel(page)

        # 06 already uploaded
        item06 = by_id["06"]
        report["uploads"].append(
            {
                "id": "06",
                "title": item06["title"],
                "ok": True,
                "video_id": KNOWN_06,
                "url": f"https://youtu.be/{KNOWN_06}",
                "note": "already_uploaded",
            }
        )
        print(f"Schedule 06 {KNOWN_06}…", flush=True)
        sch = schedule_safe(page, item06, KNOWN_06)
        report["schedules"].append(sch)
        print(json.dumps(sch, indent=2), flush=True)
        print(f"Related 06 → {LONG_ID}…", flush=True)
        rel = U.set_related(page, KNOWN_06, "06")
        report["related"].append(rel)
        print(json.dumps(rel, indent=2), flush=True)
        OUT.write_text(json.dumps(report, indent=2))

        for sid in ("07", "08"):
            item = by_id[sid]
            print(f"Upload {sid} {item['title']}…", flush=True)
            up = U.upload_one(page, item)
            vid = recover_id(page, item, ban, up.get("video_id") or "")
            if not vid:
                up["ok"] = False
                up["error"] = "unrecovered_id"
            else:
                up["video_id"] = vid
                up["url"] = f"https://youtu.be/{vid}"
                up["ok"] = True
                if up.get("video_id") in PILLAR_IDS:
                    up["recovered_by_title"] = True
            report["uploads"].append(up)
            print(json.dumps(up, indent=2), flush=True)
            OUT.write_text(json.dumps(report, indent=2))
            if not up.get("ok"):
                continue
            ban.add(vid)
            print(f"Schedule {vid}…", flush=True)
            sch = schedule_safe(page, item, vid)
            report["schedules"].append(sch)
            print(json.dumps(sch, indent=2), flush=True)
            print(f"Related {vid} → {LONG_ID}…", flush=True)
            rel = U.set_related(page, vid, sid)
            report["related"].append(rel)
            print(json.dumps(rel, indent=2), flush=True)
            OUT.write_text(json.dumps(report, indent=2))

        page.close()

    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    report["all_ok"] = (
        len(report["uploads"]) == 3
        and all(u.get("ok") for u in report["uploads"])
        and len(report["schedules"]) == 3
        and all(s.get("ok") for s in report["schedules"])
        and len(report["related"]) == 3
        and all(r.get("ok") for r in report["related"])
    )
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
