#!/usr/bin/env python3
"""Click a calendar day by visible number inside September 2026 grid, then set time."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
OUT = Path("/tmp/orbit_calclick_result.json")
AUDIT = Path("/tmp/orbit_calclick")

JOBS = [
    {"id": "FbRFvSApfOQ", "day": 3, "time": "20:00", "tag": "fbrf"},
    {"id": "92vmMxSNmlk", "day": 10, "time": "11:30", "tag": "cantstand"},
]


CLICK_DAY = """
({day, monthNeedle}) => {
  const cells = [];
  const walk = (root) => {
    for (const el of root.querySelectorAll('*')) {
      const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
      const r = el.getBoundingClientRect();
      if (r.width >= 18 && r.width <= 56 && r.height >= 18 && r.height <= 56 && r.y > 80) {
        if (t === String(day) || t === String(day) + '') {
          cells.push({x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height, t, tag: el.tagName});
        }
      }
      if (el.shadowRoot) walk(el.shadowRoot);
    }
  };
  walk(document);
  // Prefer the leftmost/topmost day in the visible popup (September grid comes first).
  cells.sort((a,b) => a.y - b.y || a.x - b.x);
  return cells;
}
"""


def dismiss(page) -> None:
    page.evaluate("() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())")


def open_privacy(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1300)


def open_calendar(page) -> dict:
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('#datepicker-trigger, ytcp-text-dropdown-trigger')) {
              const r=el.getBoundingClientRect();
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (r.width>80 && r.height>20 && /\\d/.test(t)) { el.click(); return {t, x:r.x, y:r.y}; }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
            }
            return null;
          };
          return walk(dlg||document);
        }"""
    )


def read_fields(page) -> dict:
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          let date='';
          let time='';
          const walk=(root)=>{
            for (const el of root.querySelectorAll('#datepicker-trigger, ytcp-text-dropdown-trigger')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const r=el.getBoundingClientRect();
              if (r.width>80 && /\\d/.test(t) && /202\\d/.test(t)) date = t;
            }
            for (const el of root.querySelectorAll('input')) {
              if (/^\\d{1,2}:\\d{2}$/.test(el.value||'')) time = el.value;
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(dlg||document);
          return {date, time};
        }"""
    )


def set_time(page, time_str: str) -> bool:
    return page.evaluate(
        """(t) => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('input')) {
              if (/^\\d{1,2}:\\d{2}$/.test(el.value||'')) {
                el.focus();
                el.value = t;
                el.dispatchEvent(new Event('input', {bubbles:true}));
                el.dispatchEvent(new Event('change', {bubbles:true}));
                return el.value;
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
            }
            return null;
          };
          return walk(dlg||document);
        }""",
        time_str,
    )


def click_done_save(page) -> dict:
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=800)
    except Exception:
        pass
    btn = page.get_by_role("button", name="Done", exact=True)
    done = False
    if btn.count():
        (btn.last if btn.count() > 1 else btn.first).click(force=True, timeout=3000)
        page.wait_for_timeout(1200)
        done = True
    saved = False
    sb = page.get_by_role("button", name="Save", exact=True)
    if sb.count() and sb.first.is_enabled():
        sb.first.click(force=True)
        page.wait_for_timeout(3200)
        saved = True
    return {"done": done, "saved": saved}


def match(fields: dict, day: int, time_str: str) -> bool:
    hay = (fields.get("date") or "") + " " + (fields.get("time") or "")
    return bool(re.search(rf"\b{day}\b", hay) and re.search(r"Sep", hay, re.I) and (fields.get("time") or "").startswith(time_str[:4]))


def run_job(page, job: dict) -> dict:
    vid = job["id"]
    row = {"id": vid, "ok": False, "target": f"{job['day']} Sep {job['time']}"}
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    if vid not in page.url:
        row["error"] = page.url[:160]
        return row
    dismiss(page)
    open_privacy(page)
    row["before"] = read_fields(page)
    cal = open_calendar(page)
    row["opened_cal"] = cal
    page.wait_for_timeout(700)
    cells = page.evaluate(CLICK_DAY, {"day": job["day"], "monthNeedle": "September"})
    row["cells"] = cells[:8]
    if not cells:
        row["error"] = "no_day_cells"
        page.screenshot(path=str(AUDIT / f"{job['tag']}_nocal.png"))
        page.keyboard.press("Escape")
        return row
    # First cell is September (grid is left/top). Skip a cell that is clearly October (much further right).
    cell = cells[0]
    page.mouse.click(cell["x"], cell["y"])
    page.wait_for_timeout(500)
    row["time_set"] = set_time(page, job["time"])
    # Also type time via keyboard on the visible time field
    page.evaluate(
        """(t) => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('input')) {
              const r=el.getBoundingClientRect();
              if (r.width>40 && r.width<140 && /^\\d{1,2}:\\d{2}$/.test(el.value||'')) {
                el.click();
                return {x:r.x+r.width/2, y:r.y+r.height/2};
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
            }
            return null;
          };
          return walk(dlg||document);
        }""",
        job["time"],
    )
    page.keyboard.press("Meta+a")
    page.keyboard.type(job["time"], delay=40)
    page.keyboard.press("Enter")
    page.wait_for_timeout(400)
    pre = read_fields(page)
    row["pre_done"] = pre
    page.screenshot(path=str(AUDIT / f"{job['tag']}_filled.png"))
    if not match(pre, job["day"], job["time"]):
        row["error"] = f"mismatch:{pre}"
        page.keyboard.press("Escape")
        return row
    row["save"] = click_done_save(page)
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    dismiss(page)
    open_privacy(page)
    v = read_fields(page)
    row["verify"] = v
    row["ok"] = match(v, job["day"], job["time"])
    page.screenshot(path=str(AUDIT / f"{job['tag']}_verify.png"))
    page.keyboard.press("Escape")
    return row


def main() -> int:
    AUDIT.mkdir(parents=True, exist_ok=True)
    report = {"jobs": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        for job in JOBS:
            print("JOB", job["id"], flush=True)
            try:
                row = run_job(page, job)
            except Exception as e:
                row = {"id": job["id"], "ok": False, "error": str(e)[:400]}
            report["jobs"].append(row)
            print(json.dumps(row, indent=2), flush=True)
        page.close()
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if all(j.get("ok") for j in report["jobs"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
