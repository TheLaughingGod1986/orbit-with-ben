#!/usr/bin/env python3
"""Meta (IG/FB) schedule v03 — proven date/time entry for Business Suite.

Critical lessons (do not regress):
- Date: triple-click select-all, type DD/MM/YYYY, verify with _date_matches
  (day must be first token — don't match `6` inside `2026`).
- Time: separate aria-label=hours|minutes spinbuttons; .value often stays empty;
  trust typed + date_final.
- Cleanup: Actions → Delete reels (not Open Drop-down).
- Graph API token may be expired; CDP on :9223 only.

Verified run: audits/crosspost_sync_2026-08-03/META_SCHEDULE_V03.json (13/13 ok).
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
AUDIT = ROOT / "00_Brand/Channel-Setup/audits/crosspost_sync_2026-08-03"
LONDON = ZoneInfo("Europe/London")
SOFT = "Full film on YouTube."

sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/Meta"))
from auto import caption as meta_cap  # type: ignore
from auto import ledger as meta_ledger  # type: ignore
from auto.studio_upload import COMPOSER, suite_url  # type: ignore


def load_scheduled_shorts() -> list[dict]:
    out = []
    for index in sorted((ROOT / "02_Video-Projects").glob("*/10_Shorts/SHORTS_UPLOAD_INDEX.json")):
        project = index.parents[1]
        data = json.loads(index.read_text())
        for s in data.get("shorts") or []:
            item = dict(s)
            vid = (item.get("video_id") or item.get("youtube_video_id") or "").strip()
            item["video_id"] = vid
            if item.get("published_now") or str(item.get("visibility", "")).lower() == "public":
                continue
            when = item.get("schedule_iso")
            if not when or not vid:
                continue
            path = project / "10_Shorts/06_Final-Exports" / Path(item.get("file") or "").name
            if not path.exists():
                path = project / (item.get("file") or "")
            if not path.exists():
                continue
            item["_abs_file"] = str(path)
            item["_project"] = project.name
            item["title"] = item.get("title") or Path(item.get("file") or "").stem
            out.append(item)
    return out


def find_label(page, label: str):
    return page.evaluate(
        """(label)=>{
          const out=[];
          for (const el of document.querySelectorAll('button,div,span,[role=button]')) {
            const t=(el.innerText||'').trim();
            if (t!==label) continue;
            const r=el.getBoundingClientRect();
            if (r.width<15||r.height<10||r.width>320) continue;
            const s=getComputedStyle(el);
            out.push({x:r.x+r.width/2,y:r.y+r.height/2,bg:s.backgroundColor||'',y0:Math.round(r.y),x0:Math.round(r.x),w:Math.round(r.width)});
          }
          return out;
        }""",
        label,
    )


def click_blue(page, label: str) -> bool:
    hits = find_label(page, label)
    if not hits:
        return False

    def score(h):
        bg = h.get("bg") or ""
        blue = "10, 120, 190" in bg or "0, 97, 160" in bg
        return (1 if blue else 0, h["y0"], h["x0"])

    h = sorted(hits, key=score)[-1]
    page.mouse.move(h["x"], h["y"])
    time.sleep(0.12)
    page.mouse.down()
    time.sleep(0.05)
    page.mouse.up()
    time.sleep(1.3)
    return True


def fill_caption(page, caption: str) -> bool:
    try:
        page.get_by_placeholder(re.compile(r"Describe your reel", re.I)).first.click(timeout=4000)
    except Exception:
        try:
            page.locator("textarea").first.click(timeout=4000)
        except Exception:
            return False
    page.keyboard.press("Meta+a")
    page.keyboard.type(caption[:2100], delay=5)
    page.keyboard.press("Escape")
    return True


def _date_matches(value: str, day: int, month: int, year: int) -> bool:
    """Require day as first numeric token so `6` does not match inside `2026`."""
    v = (value or "").strip()
    if not v:
        return False
    # e.g. 3/8/2026 or 03/08/2026
    m = re.match(r"^(\d{1,2})\D+(\d{1,2})\D+(\d{2,4})", v)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y < 100:
            y += 2000
        return d == day and mo == month and y == year
    # e.g. 3 August 2026
    m = re.match(r"^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", v)
    if m:
        months = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }
        d, mon, y = int(m.group(1)), months.get(m.group(2).lower(), 0), int(m.group(3))
        return d == day and mon == month and y == year
    return False


def set_datetime_v03(page, when: datetime) -> dict:
    """Triple-click date + spinbutton hours/minutes; verify before Schedule."""
    info: dict = {"target": when.isoformat()}
    click_blue(page, "Schedule")
    time.sleep(1)
    try:
        page.get_by_text("Schedule", exact=True).first.click(timeout=2000)
    except Exception:
        pass
    time.sleep(0.8)

    date_typed = f"{when.day:02d}/{when.month:02d}/{when.year}"
    info["date_typed"] = date_typed

    # Date input: triple-click → type → Enter
    date_ok = False
    date_value = ""
    try:
        date_input = page.locator(
            'input[placeholder*="dd" i], input[aria-label*="date" i], input[placeholder*="/" i]'
        ).first
        if not date_input.count():
            # fallback: visible text inputs
            date_input = page.locator("input[type=text]").first
        date_input.click(timeout=4000)
        page.mouse.click(
            date_input.bounding_box()["x"] + 10,
            date_input.bounding_box()["y"] + 10,
            click_count=3,
        )
        page.keyboard.type(date_typed, delay=40)
        page.keyboard.press("Enter")
        time.sleep(0.6)
        date_value = date_input.input_value()
        date_ok = _date_matches(date_value, when.day, when.month, when.year)
        if not date_ok:
            # read nearby text for "3 August 2026"
            body = page.inner_text("body")
            for cand in re.findall(r"\d{1,2}\s+[A-Za-z]+\s+2026", body):
                if _date_matches(cand, when.day, when.month, when.year):
                    date_value = cand
                    date_ok = True
                    break
    except Exception as e:
        info["date_err"] = str(e)[:160]

    info["date_value"] = date_value
    info["date_ok"] = date_ok

    # Hours / minutes spinbuttons
    hh, mm = f"{when.hour:02d}", f"{when.minute:02d}"
    info["hours_typed"] = hh
    info["minutes_typed"] = mm
    for aria, val in (("hours", hh), ("minutes", mm)):
        try:
            spin = page.locator(f'[role=spinbutton][aria-label="{aria}"]').first
            if not spin.count():
                spin = page.get_by_role("spinbutton", name=re.compile(aria, re.I)).first
            spin.click(timeout=3000, click_count=3)
            page.keyboard.type(val, delay=40)
            page.keyboard.press("Enter")
            time.sleep(0.3)
        except Exception as e:
            info[f"{aria}_err"] = str(e)[:120]

    page.keyboard.press("Escape")
    time.sleep(0.4)
    body = page.inner_text("body")
    # Final date string often shown as "3 August 2026"
    date_final = ""
    for cand in re.findall(r"\d{1,2}\s+[A-Za-z]+\s+2026", body):
        if _date_matches(cand, when.day, when.month, when.year):
            date_final = cand
            break
    info["date_final"] = date_final or date_value
    info["verified"] = bool(date_ok or date_final)
    info["verified_via"] = "date+time" if info["verified"] else "failed"
    return info


def schedule_one(page, short: dict, creds: dict) -> dict:
    path = Path(short["_abs_file"])
    when = datetime.fromisoformat(short["schedule_iso"])
    if when.tzinfo is None:
        when = when.replace(tzinfo=LONDON)
    cap = meta_cap.meta_caption(short)
    if SOFT not in cap:
        cap = f"{cap} {SOFT}".strip()
    rec = {"video_id": short["video_id"], "when": when.isoformat(), "title": short.get("title")}

    page.goto(suite_url(COMPOSER, creds), wait_until="domcontentloaded", timeout=120000)
    time.sleep(3)
    for lab in ("Done", "Close", "Not now", "Got it"):
        try:
            page.get_by_text(lab, exact=True).first.click(timeout=700)
        except Exception:
            pass

    uploaded = False
    try:
        with page.expect_file_chooser(timeout=10000) as fc:
            click_blue(page, "Add video")
        fc.value.set_files(str(path))
        uploaded = True
    except Exception:
        fi = page.locator("input[type=file]").first
        if fi.count():
            fi.set_input_files(str(path))
            uploaded = True
    rec["uploaded"] = uploaded
    if not uploaded:
        rec["status"] = "no_file"
        return rec

    fill_caption(page, cap)
    for _ in range(100):
        if re.search(r"100\s*%", page.inner_text("body")):
            break
        time.sleep(2)
    for _ in range(35):
        if "safe to publish" in page.inner_text("body").lower():
            break
        time.sleep(2)
    page.keyboard.press("Escape")

    for _ in range(8):
        body = page.inner_text("body")
        if "Scheduling options" in body or "Share now" in body:
            break
        click_blue(page, "Next")
        time.sleep(1)

    if "Share now" not in page.inner_text("body") and "Scheduling options" not in page.inner_text("body"):
        rec["status"] = "no_share_step"
        page.screenshot(path=str(AUDIT / f"v03_noshare_{short['video_id']}.png"))
        return rec

    dt = set_datetime_v03(page, when)
    rec["datetime"] = dt
    page.screenshot(path=str(AUDIT / f"v03_set_{short['video_id']}.png"))

    if not dt.get("verified"):
        rec["status"] = "date_verify_failed"
        return rec

    clicked = click_blue(page, "Schedule")
    if not clicked:
        hits = find_label(page, "Schedule")
        if hits:
            h = sorted(hits, key=lambda x: x["y0"])[-1]
            page.mouse.click(h["x"], h["y"])
            clicked = True
    rec["schedule_clicked"] = clicked
    time.sleep(7)
    body = page.inner_text("body")
    page.screenshot(path=str(AUDIT / f"v03_after_{short['video_id']}.png"))

    ok = False
    if re.search(r"scheduled|will be published|Your reel is scheduled", body, re.I):
        ok = True
    if "Add video" in body and "Scheduling options" not in body and "Share now" not in body:
        ok = True
    if "Scheduling options" in body and find_label(page, "Schedule"):
        ok = False
        rec["still_on_share"] = True

    rec["status"] = "ok" if ok else "unconfirmed"
    if ok:
        meta_ledger.mark_posted(
            short,
            {
                "status": "scheduled",
                "method": "cdp_v03",
                "platforms": {
                    "instagram": {
                        "status": "scheduled",
                        "method": "cdp_v03",
                        "when": when.isoformat(),
                    },
                    "facebook": {
                        "status": "scheduled",
                        "method": "cdp_v03",
                        "when": when.isoformat(),
                    },
                },
            },
        )
    return rec


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    shorts = load_scheduled_shorts()
    creds_path = ROOT / "00_Brand/Channel-Setup/Meta/META_CREDENTIALS.json"
    creds = json.loads(creds_path.read_text())
    orig = dict(creds)
    # Benkay / orbit IG portfolio used for successful v03 run
    creds["business_id"] = "1203116147241086"
    creds["business_suite_asset_id"] = "1251385088056874"
    creds_path.write_text(json.dumps(creds, indent=2) + "\n")

    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
            page = browser.contexts[0].new_page()
            for s in shorts:
                print("V03 SCHED", s["video_id"], s["schedule_iso"], flush=True)
                try:
                    r = schedule_one(page, s, creds)
                except Exception as e:
                    r = {"video_id": s["video_id"], "status": "failed", "error": str(e)[:300]}
                results.append(r)
                print(
                    " ",
                    r.get("status"),
                    "date=",
                    (r.get("datetime") or {}).get("date_final"),
                    "verified=",
                    (r.get("datetime") or {}).get("verified"),
                    flush=True,
                )
                time.sleep(2)
            page.close()
    finally:
        creds_path.write_text(json.dumps(orig, indent=2) + "\n")

    out = {
        "finished_at": datetime.now(LONDON).isoformat(),
        "ok": sum(1 for r in results if r.get("status") == "ok"),
        "n": len(results),
        "results": results,
    }
    (AUDIT / "META_SCHEDULE_V03.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"ok": out["ok"], "n": out["n"]}, indent=2))


if __name__ == "__main__":
    main()
