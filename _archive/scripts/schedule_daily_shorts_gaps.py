#!/usr/bin/env python3
"""Fill daily Short gaps in desktop Studio via CDP.

Cadence Ben locked this session:
- One Short every day
- Thursday 11:30 = promo for the upcoming Thursday long (before Premiere 18:00)
- Thu 20:00 = launch Short after the long is public
- Fri–Wed 11:30 = punches from that week's long

Does not remint. Does not change Related unless the field is empty.
Does not touch leftover duplicate ids.
"""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
OUT = Path("/tmp/orbit_schedule_gaps_result.json")
AUDIT = Path("/tmp/orbit_schedule_gaps")
EUROPA = "NbW5G1BpPY0"
NEUTRON = "Yk1tLh23rko"

MONTHS = {
    1: ("January", "Jan"),
    2: ("February", "Feb"),
    3: ("March", "Mar"),
    4: ("April", "Apr"),
    5: ("May", "May"),
    6: ("June", "Jun"),
    7: ("July", "Jul"),
    8: ("August", "Aug"),
    9: ("September", "Sep"),
    10: ("October", "Oct"),
    11: ("November", "Nov"),
    12: ("December", "Dec"),
}

# Fill empties first; move Can't Stand onto Thu 10 Sep 11:30 as Neutron upcoming
# because the 6th Neutron punch (bible prefix fhJP) is not in live Studio.
JOBS = [
    {
        "id": "eVp9a7f4rWg",
        "day": 3,
        "month": 9,
        "time": "11:30",
        "related": EUROPA,
        "tag": "europa_thu_upcoming",
        "title": "We Could Kill the Life We're Looking For",
    },
    {
        "id": "D3KSYrqip5A",
        "day": 8,
        "month": 9,
        "time": "11:30",
        "related": EUROPA,
        "tag": "europa_8sep_gap",
        "title": "Europa Clipper Is Already Flying",
    },
    {
        "id": "92vmMxSNmlk",
        "day": 10,
        "month": 9,
        "time": "11:30",
        "related": NEUTRON,
        "tag": "neutron_thu_upcoming",
        "title": "You Can't Stand on a Neutron Star",
    },
]


def cdp_pages() -> list[str]:
    try:
        with urllib.request.urlopen(f"{CDP}/json/list", timeout=5) as r:
            tabs = json.loads(r.read())
        return [t.get("url", "") for t in tabs if t.get("type") == "page"]
    except Exception:
        return []


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


def open_visibility(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1400)


def expand_schedule(page) -> dict | None:
    text = page.locator("body").inner_text()
    if "Schedule as public" in text:
        return {"via": "already_expanded"}

    rect = page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          let hit=null;
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=el.getAttribute('aria-label')||'';
              const id=el.id||'';
              if (/click to expand/i.test(al) || id==='first-container-expand-button') {
                const r=el.getBoundingClientRect();
                if (r.width>5) hit={x:r.x+r.width/2,y:r.y+r.height/2,al};
              }
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(dlg||document);
          return hit;
        }"""
    )
    if rect:
        page.mouse.click(rect["x"], rect["y"])
        page.wait_for_timeout(1100)
        return {"via": "expand", **rect}

    hit = page.evaluate(
        """() => {
          const hits=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t!=='Schedule') continue;
              const r=el.getBoundingClientRect();
              if (r.width>200 && r.height>=20 && r.height<=100 && r.y>200) {
                hits.push({x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height});
              }
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          walk(dlg||document);
          if (!hits.length) return null;
          hits.sort((a,b)=>b.w-a.w);
          return hits[0];
        }"""
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(1100)
        return {"via": "schedule_row", **hit}
    return None


def set_date(page, day: int, month: str, month_short: str, result: dict) -> None:
    trigger = page.locator("tp-yt-paper-dialog ytcp-text-dropdown-trigger")
    if trigger.count():
        trigger.first.click(force=True)
        page.wait_for_timeout(700)
    el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
    date_str = f"{day} {month} 2026"
    if el.count():
        el.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(date_str, delay=35)
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        result["date"] = date_str
    page.evaluate(
        """({day, mon}) => {
          const walk=(root)=>{
            for (const el of root.querySelectorAll('[aria-label]')) {
              const al=el.getAttribute('aria-label')||'';
              if (!/2026/.test(al) || !new RegExp(mon,'i').test(al)) continue;
              if (!new RegExp('\\\\b'+day+'\\\\b').test(al)) continue;
              const r=el.getBoundingClientRect();
              if (r.width>10) { el.click(); return al; }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
            }
            return null;
          };
          return walk(document);
        }""",
        {"day": day, "mon": month_short[:3]},
    )
    page.wait_for_timeout(400)
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=1200)
    except Exception:
        pass


def set_time(page, time_str: str, result: dict) -> None:
    tloc = page.locator("tp-yt-paper-dialog input")
    for i in range(tloc.count()):
        try:
            v = tloc.nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tloc.nth(i).click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(time_str, delay=40)
            page.wait_for_timeout(400)
            page.evaluate(
                """(t) => {
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('tp-yt-paper-item,[role=option],div,span')) {
                      if ((el.innerText||'').trim()!==t) continue;
                      const r=el.getBoundingClientRect();
                      if (r.width>30 && r.height>10 && r.height<40) { el.click(); return true; }
                    }
                    for (const el of root.querySelectorAll('*')) {
                      if (el.shadowRoot && walk(el.shadowRoot)) return true;
                    }
                    return false;
                  };
                  return walk(document);
                }""",
                time_str,
            )
            result["time"] = time_str
            break
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=1200)
    except Exception:
        pass


def read_fields(page) -> dict:
    date = ""
    trig = page.locator("tp-yt-paper-dialog ytcp-text-dropdown-trigger")
    if trig.count():
        date = trig.first.inner_text().strip().replace("\n", " ")
    tval = ""
    for i in range(page.locator("tp-yt-paper-dialog input").count()):
        try:
            v = page.locator("tp-yt-paper-dialog input").nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tval = v
            break
    return {"date": date, "time": tval}


def click_done(page) -> dict | None:
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=800)
        page.wait_for_timeout(300)
    except Exception:
        pass
    try:
        btn = page.get_by_role("button", name="Done", exact=True)
        if btn.count():
            target = btn.last if btn.count() > 1 else btn.first
            if target.is_visible():
                target.click(force=True, timeout=3000)
                page.wait_for_timeout(1800)
                return {"via": "role"}
    except Exception:
        pass
    coords = page.evaluate(
        """() => {
          const cands=[];
          const walk=(root)=>{
            for (const b of root.querySelectorAll('button, ytcp-button, [role=button]')) {
              const t=(b.innerText||b.textContent||'').replace(/\\s+/g,' ').trim();
              if (t!=='Done') continue;
              const r=b.getBoundingClientRect();
              if (r.width>20 && r.height>10 && r.y>300) {
                cands.push({x:r.x+r.width/2,y:r.y+r.height/2,yPos:r.y,
                  dis:!!(b.disabled||b.getAttribute('aria-disabled')==='true')});
              }
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          walk(dlg||document);
          if (!cands.length) walk(document);
          cands.sort((a,b)=>b.yPos-a.yPos);
          return cands.find(c=>!c.dis)||cands[0]||null;
        }"""
    )
    if coords:
        page.mouse.click(coords["x"], coords["y"])
        page.wait_for_timeout(1800)
    return coords


def save_edit(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(3500)
            return True
    except Exception:
        pass
    return False


def scrape_edit(page) -> dict:
    body = page.inner_text("body")
    vis = None
    for v in ("Scheduled", "Premiere", "Public", "Private", "Draft"):
        if v in body:
            vis = v
            break
    return {
        "url": page.url,
        "vis": vis,
        "has_europa": EUROPA in body or "Could Life Exist Under The Ice Of Europa" in body,
        "has_neutron": NEUTRON in body or "What Happens to Your Body Near a Neutron Star" in body,
        "snip": [
            ln.strip()
            for ln in body.splitlines()
            if any(
                k in ln
                for k in (
                    "Scheduled",
                    "Private",
                    "Premiere",
                    "11:30",
                    "20:00",
                    "18:00",
                    "Sept",
                    "Sep",
                    "Related",
                )
            )
        ][:16],
    }


def schedule_one(page, job: dict) -> dict:
    month, month_short = MONTHS[job["month"]]
    vid = job["id"]
    result: dict = {
        "id": vid,
        "ok": False,
        "tag": job["tag"],
        "title": job["title"],
        "target": f"{job['day']} {month_short} 2026 {job['time']}",
        "related_target": job["related"],
    }
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    if vid not in page.url:
        result["error"] = f"url_mismatch:{page.url[:180]}"
        return result
    if "accounts.google.com" in page.url:
        result["error"] = "BLOCKED_NEED_BEN_LOGIN"
        return result
    dismiss(page)
    result["before"] = scrape_edit(page)
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{job['tag']}_01.png"))

    try:
        open_visibility(page)
    except Exception as e:
        result["open_err"] = str(e)[:200]
        page.get_by_text(re.compile(r"Private|Visibility|Scheduled", re.I)).first.click(force=True)
        page.wait_for_timeout(1200)

    result["expand"] = expand_schedule(page)
    set_date(page, job["day"], month, month_short, result)
    set_time(page, job["time"], result)
    result["pre_done"] = read_fields(page)
    page.screenshot(path=str(AUDIT / f"{job['tag']}_02_filled.png"))
    result["done"] = click_done(page)
    page.wait_for_timeout(800)
    result["saved"] = save_edit(page)
    page.wait_for_timeout(2200)

    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3200)
    dismiss(page)
    after = scrape_edit(page)
    result["after"] = after
    result["chip_scheduled"] = after.get("vis") == "Scheduled"
    try:
        open_visibility(page)
        expand_schedule(page)
        v = read_fields(page)
        result["verify"] = v
        hay = (v.get("date") or "") + (v.get("time") or "") + " ".join(after.get("snip") or [])
        result["ok"] = bool(
            result["chip_scheduled"]
            and re.search(rf"\b{job['day']}\b", hay)
            and re.search(month_short[:3], hay, re.I)
        )
        click_done(page)
    except Exception as e:
        result["verify_err"] = str(e)[:200]
        result["ok"] = result["chip_scheduled"]
    page.screenshot(path=str(AUDIT / f"{job['tag']}_03_verify.png"))
    return result


def peek_fbrf(page) -> dict:
    page.goto(
        "https://studio.youtube.com/video/FbRFvSApfOQ/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3200)
    dismiss(page)
    info = scrape_edit(page)
    try:
        open_visibility(page)
        expand_schedule(page)
        info["fields"] = read_fields(page)
        click_done(page)
    except Exception as e:
        info["fields_err"] = str(e)[:200]
    page.screenshot(path=str(AUDIT / "fbrf_peek.png"))
    return info


def main() -> int:
    AUDIT.mkdir(parents=True, exist_ok=True)
    report: dict = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "cdp_pages": cdp_pages(),
        "jobs": [],
        "fbrf": None,
        "note": "Thu 3 Sep 11:30 eVp9 Europa upcoming · 8 Sep D3KS · Thu 10 Sep 11:30 Can't Stand Neutron upcoming. fhJP not in live Studio.",
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)
        if "accounts.google.com" in page.url:
            report["error"] = "BLOCKED_NEED_BEN_LOGIN"
            OUT.write_text(json.dumps(report, indent=2))
            print("BLOCKED_NEED_BEN_LOGIN")
            page.close()
            return 2
        report["fbrf"] = peek_fbrf(page)
        for job in JOBS:
            print(f"Schedule {job['id']} → {job['day']} Sep {job['time']}…", flush=True)
            try:
                row = schedule_one(page, job)
            except Exception as e:
                row = {"id": job["id"], "ok": False, "error": str(e)[:400], "tag": job["tag"]}
            report["jobs"].append(row)
            print(json.dumps({k: row.get(k) for k in ("id", "ok", "verify", "chip_scheduled", "error")}, indent=2), flush=True)
            OUT.write_text(json.dumps(report, indent=2))
        page.close()
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    report["all_ok"] = all(j.get("ok") for j in report["jobs"]) if report["jobs"] else False
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
