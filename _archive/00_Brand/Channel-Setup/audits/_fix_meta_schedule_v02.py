#!/usr/bin/env python3
"""Re-schedule Meta reels correctly: set date+time, click blue Schedule (not Share)."""
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


def set_datetime(page, when: datetime) -> dict:
    info = {"target": when.isoformat()}
    # Ensure Schedule mode selected (not Share now)
    click_blue(page, "Schedule")
    time.sleep(1)
    # Prefer clicking the Schedule option text if needed
    try:
        page.get_by_text("Schedule", exact=True).first.click(timeout=2000)
    except Exception:
        pass
    time.sleep(0.8)

    date_str = f"{when.day}/{when.month}/{when.year}"  # Suite UK style e.g. 3/8/2026
    date_alts = [date_str, when.strftime("%d/%m/%Y"), when.strftime("%m/%d/%Y")]
    time_str = when.strftime("%H:%M")

    # Fill via JS — more reliable for Suite inputs
    filled = page.evaluate(
        """({dates, timeStr}) => {
          const inputs=[...document.querySelectorAll('input')].filter(a=>{
            const r=a.getBoundingClientRect();
            return r.width>40 && r.height>10 && a.offsetParent!==null;
          });
          let dateOk=false, timeOk=false;
          for (const a of inputs) {
            const ph=((a.placeholder||'')+(a.getAttribute('aria-label')||'')+(a.getAttribute('name')||'')).toLowerCase();
            const val=(a.value||'');
            const looksDate = /date|dd|mm|yyyy|\/|day/.test(ph) || /\\d{1,2}\\/\\d{1,2}\\/\\d{2,4}/.test(val);
            const looksTime = /time|hour|:/.test(ph) || /^\\d{1,2}:\\d{2}/.test(val);
            const proto=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value');
            const set=(el,v)=>{ if(proto&&proto.set) proto.set.call(el,v); else el.value=v;
              el.dispatchEvent(new Event('input',{bubbles:true}));
              el.dispatchEvent(new Event('change',{bubbles:true}));
              el.dispatchEvent(new KeyboardEvent('keyup',{bubbles:true}));
            };
            if (!dateOk && looksDate) { set(a, dates[0]); dateOk=true; continue; }
            if (!timeOk && looksTime) { set(a, timeStr); timeOk=true; continue; }
          }
          // Fallback: last two visible text inputs near Schedule section
          if (!dateOk || !timeOk) {
            const texts=inputs.filter(a=>a.type==='text' || !a.type);
            if (texts.length>=2) {
              if (!dateOk) { const a=texts[texts.length-2]; set(a, dates[0]); dateOk=true; }
              if (!timeOk) { const a=texts[texts.length-1]; set(a, timeStr); timeOk=true; }
            }
          }
          return {dateOk, timeOk, inputCount: inputs.length, values: inputs.slice(0,8).map(a=>({v:a.value,ph:a.placeholder}))};
        }""",
        {"dates": date_alts, "timeStr": time_str},
    )
    info.update(filled or {})
    # Also try keyboard into focused time field
    if not info.get("timeOk"):
        try:
            # click any input showing HH:MM
            page.locator("input").evaluate_all(
                """(els, t) => {
                  for (const a of els) {
                    if (/^\\d{1,2}:\\d{2}/.test(a.value||'') || /time/i.test(a.placeholder||'')) {
                      a.focus(); a.select(); return true;
                    }
                  }
                  return false;
                }""",
                time_str,
            )
            page.keyboard.type(time_str, delay=30)
            info["time_typed"] = True
        except Exception as e:
            info["time_type_err"] = str(e)[:100]
    page.keyboard.press("Escape")
    time.sleep(0.5)
    # Read back body for date/time confirmation
    body = page.inner_text("body")
    info["body_has_date"] = str(when.day) in body or when.strftime("%d") in body
    info["body_has_time"] = time_str in body or f"{when.hour}:{when.strftime('%M')}" in body
    return info


def schedule_one(page, short: dict, creds: dict) -> dict:
    path = Path(short["_abs_file"])
    when = datetime.fromisoformat(short["schedule_iso"])
    if when.tzinfo is None:
        when = when.replace(tzinfo=LONDON)
    cap = meta_cap.meta_caption(short)
    if SOFT not in cap:
        cap = f"{cap} {SOFT}".strip()
    rec = {"video_id": short["video_id"], "when": when.isoformat()}

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
        page.screenshot(path=str(AUDIT / f"fix_noshare_{short['video_id']}.png"))
        return rec

    rec["datetime"] = set_datetime(page, when)
    page.screenshot(path=str(AUDIT / f"fix_set_{short['video_id']}.png"))

    # CRITICAL: final CTA is "Schedule" when schedule mode is on
    clicked = click_blue(page, "Schedule")
    if not clicked:
        # try any Schedule button
        hits = find_label(page, "Schedule")
        if hits:
            h = sorted(hits, key=lambda x: x["y0"])[-1]
            page.mouse.click(h["x"], h["y"])
            clicked = True
    rec["schedule_clicked"] = clicked
    time.sleep(7)
    body = page.inner_text("body")
    page.screenshot(path=str(AUDIT / f"fix_after_{short['video_id']}.png"))

    # Success: left composer, or toast
    ok = False
    if re.search(r"scheduled|will be published|Your reel is scheduled", body, re.I):
        ok = True
    if "Add video" in body and "Scheduling options" not in body and "Share now" not in body:
        ok = True
    # Still on share with Schedule button = failed
    if "Scheduling options" in body and find_label(page, "Schedule"):
        ok = False
        rec["still_on_share"] = True

    rec["status"] = "ok" if ok else "unconfirmed"
    if ok:
        meta_ledger.mark_posted(
            short,
            {
                "status": "scheduled",
                "method": "cdp",
                "platforms": {
                    "instagram": {
                        "status": "scheduled",
                        "method": "cdp",
                        "when": when.isoformat(),
                    },
                    "facebook": {
                        "status": "scheduled",
                        "method": "cdp",
                        "when": when.isoformat(),
                    },
                },
            },
        )
    return rec


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    shorts = load_scheduled_shorts()
    # Clear prior false scheduled marks so we re-run cleanly
    data = meta_ledger.load()
    for s in shorts:
        key = f"yt:{s['video_id']}"
        entry = data.get("posted", {}).get(key)
        if entry and (
            entry.get("result_status") == "scheduled"
            or (entry.get("instagram") or {}).get("status") == "scheduled"
        ):
            data["posted"].pop(key, None)
    meta_ledger.save(data)

    creds_path = ROOT / "00_Brand/Channel-Setup/Meta/META_CREDENTIALS.json"
    creds = json.loads(creds_path.read_text())
    orig = dict(creds)
    creds["business_id"] = "1203116147241086"
    creds["business_suite_asset_id"] = "1251385088056874"
    creds_path.write_text(json.dumps(creds, indent=2) + "\n")

    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
            page = browser.contexts[0].new_page()
            for s in shorts:
                print("FIX SCHED", s["video_id"], s["schedule_iso"], flush=True)
                try:
                    r = schedule_one(page, s, creds)
                except Exception as e:
                    r = {"video_id": s["video_id"], "status": "failed", "error": str(e)[:300]}
                results.append(r)
                print(" ", r.get("status"), r.get("datetime", {}).get("timeOk"), r.get("still_on_share"), flush=True)
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
    (AUDIT / "META_SCHEDULE_FIX.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"ok": out["ok"], "n": out["n"]}, indent=2))


if __name__ == "__main__":
    main()
