#!/usr/bin/env python3
"""Fix two Studio schedule mistakes using calendar aria-labels (no typed dates).

- FbRFvSApfOQ: 3 Sep 20:00 launch (was 11:30, colliding with eVp9 upcoming)
- 92vmMxSNmlk: 10 Sep 11:30 Neutron upcoming (was wrongly saved as 27 Sep 19:30)
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
AUDIT = Path("/tmp/orbit_schedule_fix")
OUT = Path("/tmp/orbit_schedule_fix_result.json")

JOBS = [
    {"id": "FbRFvSApfOQ", "day": 3, "month_name": "September", "month_short": "Sep", "time": "20:00", "tag": "fbrf_launch_2000"},
    {"id": "92vmMxSNmlk", "day": 10, "month_name": "September", "month_short": "Sep", "time": "11:30", "tag": "cantstand_10sep"},
]


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=500)
        except Exception:
            pass


def open_visibility(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(250)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1200)


def privacy_dialog(page):
    return page.locator('tp-yt-paper-dialog[aria-label="Select video privacy"]')


def datetime_visible(page) -> bool:
    dlg = privacy_dialog(page)
    if not dlg.count():
        return False
    try:
        t = dlg.first.inner_text()
    except Exception:
        return False
    return bool(re.search(r"\d{1,2}\s+\w+\s+2026", t))


def expand_schedule(page) -> str:
    """Expand only if the date picker is not already showing. Re-clicking collapse it."""
    if datetime_visible(page):
        return "already_visible"
    page.evaluate(
        """() => {
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=el.getAttribute('aria-label')||'';
              const id=el.id||'';
              if (/click to expand/i.test(al) || id==='first-container-expand-button') {
                const r=el.getBoundingClientRect();
                if (r.width>5) { el.click(); return true; }
              }
              if (el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
          };
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          walk(dlg||document);
        }"""
    )
    page.wait_for_timeout(900)
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=800)
    except Exception:
        pass
    return "expanded"


def calendar_pick(page, day: int, month_name: str, year: int = 2026) -> str | None:
    """Click the date trigger, then the calendar cell whose aria-label is that day."""
    dlg = privacy_dialog(page)
    trigger = dlg.locator("ytcp-text-dropdown-trigger")
    clicked = False
    for i in range(trigger.count()):
        try:
            t = trigger.nth(i).inner_text().strip()
        except Exception:
            continue
        if re.search(r"\d{1,2}\s+\w+", t):
            trigger.nth(i).click(force=True)
            clicked = True
            break
    if not clicked and trigger.count():
        trigger.first.click(force=True)
    page.wait_for_timeout(800)

    wanted = [
        f"{day} {month_name} {year}",
        f"{day} {month_name[:3]} {year}",
        f"{day} Sept {year}" if month_name == "September" else "",
    ]
    wanted = [w for w in wanted if w]

    def click_cell() -> str | None:
        return page.evaluate(
            """(needles) => {
              const walk=(root)=>{
                for (const el of root.querySelectorAll('[aria-label]')) {
                  const al=el.getAttribute('aria-label')||'';
                  if (!needles.some(n => al.includes(n))) continue;
                  const r=el.getBoundingClientRect();
                  if (r.width>8 && r.height>8) { el.click(); return al; }
                }
                for (const el of root.querySelectorAll('*')) {
                  if (el.shadowRoot) {
                    const x=walk(el.shadowRoot);
                    if (x) return x;
                  }
                }
                return null;
              };
              return walk(document);
            }""",
            wanted,
        )

    hit = click_cell()
    if hit:
        return hit

    # Flip calendar months (max 14) until the cell exists.
    for _ in range(14):
        page.evaluate(
            """() => {
              const walk=(root)=>{
                for (const el of root.querySelectorAll('button,ytcp-icon-button,[aria-label]')) {
                  const al=(el.getAttribute('aria-label')||'').toLowerCase();
                  if (al.includes('next') || al.includes('forward')) {
                    const r=el.getBoundingClientRect();
                    if (r.width>8) { el.click(); return true; }
                  }
                  if (el.shadowRoot && walk(el.shadowRoot)) return true;
                }
                return false;
              };
              return walk(document);
            }"""
        )
        page.wait_for_timeout(400)
        hit = click_cell()
        if hit:
            return hit
    return None


def time_pick(page, time_str: str) -> bool:
    tloc = privacy_dialog(page).locator("input")
    for i in range(tloc.count()):
        try:
            v = tloc.nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tloc.nth(i).click(force=True)
            page.wait_for_timeout(300)
            page.keyboard.press("Meta+a")
            page.keyboard.type(time_str, delay=40)
            page.wait_for_timeout(350)
            clicked = page.evaluate(
                """(t) => {
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('tp-yt-paper-item,[role=option],div,span')) {
                      if ((el.innerText||'').trim()!==t) continue;
                      const r=el.getBoundingClientRect();
                      if (r.width>24 && r.height>8 && r.height<48) { el.click(); return true; }
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
            try:
                now = tloc.nth(i).input_value()
            except Exception:
                now = ""
            return bool(clicked) or (now or "").startswith(time_str[:4])
    return False


def read_fields(page) -> dict:
    date = ""
    dlg = privacy_dialog(page)
    trig = dlg.locator("ytcp-text-dropdown-trigger")
    for i in range(trig.count()):
        try:
            t = trig.nth(i).inner_text().strip().replace("\n", " ")
        except Exception:
            continue
        if re.search(r"\d{1,2}\s+\w+", t):
            date = t
            break
    tval = ""
    for i in range(dlg.locator("input").count()):
        try:
            v = dlg.locator("input").nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tval = v
            break
    return {"date": date, "time": tval}


def click_done(page) -> None:
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=600)
    except Exception:
        pass
    btn = page.get_by_role("button", name="Done", exact=True)
    if btn.count():
        target = btn.last if btn.count() > 1 else btn.first
        target.click(force=True, timeout=3000)
        page.wait_for_timeout(1500)
        return
    page.evaluate(
        """() => {
          const walk=(root)=>{
            for (const b of root.querySelectorAll('button,ytcp-button,[role=button]')) {
              const t=(b.innerText||'').replace(/\\s+/g,' ').trim();
              if (t!=='Done') continue;
              const r=b.getBoundingClientRect();
              if (r.width>20 && r.y>250) { b.click(); return; }
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(document.querySelector('tp-yt-paper-dialog')||document);
        }"""
    )
    page.wait_for_timeout(1500)


def save_edit(page) -> bool:
    b = page.get_by_role("button", name="Save", exact=True)
    if b.count() and b.first.is_enabled():
        b.first.click(force=True)
        page.wait_for_timeout(3200)
        return True
    return False


def fields_match(fields: dict, job: dict) -> bool:
    hay = (fields.get("date") or "") + " " + (fields.get("time") or "")
    return bool(
        re.search(rf"\b{job['day']}\b", hay)
        and re.search(job["month_short"][:3], hay, re.I)
        and (fields.get("time") or "").startswith(job["time"][:4])
    )


def fix_one(page, job: dict) -> dict:
    vid = job["id"]
    row: dict = {"id": vid, "tag": job["tag"], "ok": False, "target": f"{job['day']} {job['month_short']} {job['time']}"}
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3200)
    if vid not in page.url:
        row["error"] = f"url_mismatch:{page.url[:160]}"
        return row
    dismiss(page)
    open_visibility(page)
    row["expand"] = expand_schedule(page)
    row["cal"] = calendar_pick(page, job["day"], job["month_name"])
    row["time_clicked"] = time_pick(page, job["time"])
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=800)
    except Exception:
        pass
    pre = read_fields(page)
    row["pre_done"] = pre
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{job['tag']}_filled.png"))
    if not fields_match(pre, job):
        row["error"] = f"abort_save_mismatch:{pre}"
        # Close dialog without saving the bad date
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        return row
    click_done(page)
    row["saved"] = save_edit(page)
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    dismiss(page)
    open_visibility(page)
    expand_schedule(page)
    v = read_fields(page)
    row["verify"] = v
    row["ok"] = fields_match(v, job)
    page.screenshot(path=str(AUDIT / f"{job['tag']}_verify.png"))
    click_done(page)
    return row


def main() -> int:
    AUDIT.mkdir(parents=True, exist_ok=True)
    report = {"started_at": datetime.now(timezone.utc).isoformat(), "jobs": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        for job in JOBS:
            print(f"FIX {job['id']} → {job['day']} Sep {job['time']}", flush=True)
            try:
                row = fix_one(page, job)
            except Exception as e:
                row = {"id": job["id"], "ok": False, "error": str(e)[:400]}
            report["jobs"].append(row)
            print(json.dumps(row, indent=2), flush=True)
        page.close()
    report["all_ok"] = all(j.get("ok") for j in report["jobs"])
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
