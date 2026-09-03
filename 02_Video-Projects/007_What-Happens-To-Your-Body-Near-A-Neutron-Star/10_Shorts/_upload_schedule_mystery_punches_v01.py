#!/usr/bin/env python3
"""Upload 3 mystery Neutron punches → Related Yk1tLh23rko → schedule 15/16/17 Sep 11:30 UK.

Uses live Studio Chrome via CDP (http://127.0.0.1:9222).
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
LONG_ID = "Yk1tLh23rko"
LONG_TITLE = "What Happens to Your Body Near a Neutron Star?"
ROOT = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "007_What-Happens-To-Your-Body-Near-A-Neutron-Star"
)
MANIFEST = ROOT / "10_Shorts/MYSTERY_PUNCHES_15_17_SEP.json"
OUT = Path("/tmp/orbit_neutron_mystery/upload_schedule_result.json")
AUDIT = Path("/tmp/orbit_neutron_mystery/upload_audit")

MONTHS = {9: ("September", "Sep")}


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Got it", "Dismiss", "Not now", "Close", "Skip"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


def next_vis(page) -> None:
    """Advance upload wizard until Visibility (Save button appears)."""
    for _ in range(16):
        dismiss(page)
        text = (
            page.locator("ytcp-uploads-dialog").inner_text()
            if page.locator("ytcp-uploads-dialog").count()
            else ""
        )
        save = page.get_by_role("button", name="Save", exact=True)
        if save.count() and "Visibility" in text:
            return
        if "Save or publish" in text:
            return
        nxt = page.get_by_role("button", name="Next", exact=True)
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1400)
            continue
        try:
            page.get_by_role("button", name="Visibility", exact=True).click(
                force=True, timeout=1500
            )
            page.wait_for_timeout(1200)
            return
        except Exception:
            break


def extract_vid(page) -> str:
    ban = {LONG_ID, "upload", "shorts"}
    m = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    if m and m.group(1) not in ban:
        return m.group(1)
    try:
        html = page.content()
    except Exception:
        html = ""
    for pat in (
        r'"videoId":"([A-Za-z0-9_-]{11})"',
        r"video_id=([A-Za-z0-9_-]{11})",
        r"/video/([A-Za-z0-9_-]{11})/edit",
        r"https://youtu\.be/([A-Za-z0-9_-]{11})",
    ):
        for hit in re.finditer(pat, html):
            vid = hit.group(1)
            if vid not in ban:
                return vid
    body = page.locator("body").inner_text()
    for pat in (
        r"/video/([A-Za-z0-9_-]{11})/",
        r"https://youtu\.be/([A-Za-z0-9_-]{11})",
    ):
        m = re.search(pat, body)
        if m and m.group(1) not in ban:
            return m.group(1)
    return ""


def ensure_orbit_channel(page) -> None:
    page.goto(
        "https://www.youtube.com/channel_switcher",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    try:
        page.locator("text=Orbit with Ben").first.click(force=True, timeout=5000)
        page.wait_for_timeout(2500)
    except Exception:
        pass
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)


def upload_one(page, item: dict) -> dict:
    path = Path(item["file"])
    r: dict = {"id": item["id"], "title": item["title"], "ok": False}
    if not path.exists():
        r["error"] = f"missing:{path}"
        return r
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    # Prefer hidden file input; fall back to Create → Upload videos.
    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.first.set_input_files(str(path))
    else:
        try:
            page.get_by_role("button", name=re.compile(r"^Create$", re.I)).first.click(
                force=True, timeout=4000
            )
            page.wait_for_timeout(800)
            page.get_by_text("Upload videos", exact=False).first.click(force=True)
            page.wait_for_timeout(1500)
        except Exception:
            pass
        inputs = page.locator('input[type="file"]')
        if inputs.count():
            inputs.first.set_input_files(str(path))
        else:
            with page.expect_file_chooser(timeout=25000) as fc:
                for name in ("Select files", "SELECT FILES", "Upload"):
                    btn = page.get_by_role("button", name=re.compile(name, re.I))
                    if btn.count() and btn.first.is_visible():
                        btn.first.click(force=True)
                        break
                else:
                    page.get_by_text("Select files", exact=False).first.click(force=True)
            fc.value.set_files(str(path))

    title_box = page.get_by_role(
        "textbox", name=re.compile(r"title that describes", re.I)
    )
    title_box.wait_for(timeout=240000)
    title_box.fill(item["title"][:100])
    desc_box = page.get_by_role(
        "textbox", name=re.compile(r"tell viewers about your video", re.I)
    )
    desc_box.click(force=True)
    desc_box.fill(item["description"])
    for kids in (
        "No, it's not made for kids",
        "No, it's not 'Made for Kids'",
        "No, it's not Made for Kids",
    ):
        try:
            page.get_by_text(kids, exact=False).first.click(force=True, timeout=1500)
            break
        except Exception:
            pass
    try:
        page.get_by_role("radio", name=re.compile(r"Yes, AI was used", re.I)).click(
            force=True, timeout=2000
        )
    except Exception:
        pass

    next_vis(page)
    # Visibility step only — wait for Save before clicking Private/Save.
    for _ in range(20):
        text = (
            page.locator("ytcp-uploads-dialog").inner_text()
            if page.locator("ytcp-uploads-dialog").count()
            else ""
        )
        if page.get_by_role("button", name="Save", exact=True).count() and (
            "Visibility" in text or "Save or publish" in text or "Private" in text
        ):
            break
        page.wait_for_timeout(500)
    page.evaluate(
        """() => {
          const walk=(r)=>{
            if(!r)return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])){
              const t=(el.innerText||'').toLowerCase();
              if(t.includes('private') && !t.includes('schedule')){ el.click(); return true; }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
              if(el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
          };
          return walk(document.querySelector('ytcp-uploads-dialog')||document);
        }"""
    )
    page.wait_for_timeout(600)
    save = page.get_by_role("button", name="Save", exact=True)
    if save.count():
        save.last.click(force=True, timeout=15000)
    else:
        page.get_by_role("button", name="Publish", exact=True).last.click(
            force=True, timeout=15000
        )
    page.wait_for_timeout(9000)
    dismiss(page)
    vid = extract_vid(page)
    if not vid:
        page.wait_for_timeout(2500)
        vid = extract_vid(page)
    r["video_id"] = vid
    r["url"] = f"https://youtu.be/{vid}" if vid else ""
    r["ok"] = bool(vid)
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"upload_{item['id']}.png"))
    try:
        page.get_by_role("button", name="Close").click(force=True, timeout=2000)
    except Exception:
        pass
    return r


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
                hits.push({x:r.x+r.width/2,y:r.y+r.height/2,w:r.width});
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


def set_date_time(page, day: int, time_str: str, result: dict) -> None:
    month, month_short = MONTHS[9]
    trigger = page.locator("tp-yt-paper-dialog ytcp-text-dropdown-trigger")
    if trigger.count():
        trigger.first.click(force=True)
        page.wait_for_timeout(700)
    el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
    date_str = f"{day} {month} 2026"
    if el.count():
        el.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(date_str, delay=30)
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
    tloc = page.locator("tp-yt-paper-dialog input")
    for i in range(tloc.count()):
        try:
            v = tloc.nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tloc.nth(i).click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(time_str, delay=35)
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


def click_done(page) -> None:
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
                return
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


def schedule_one(page, item: dict, video_id: str) -> dict:
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
    dismiss(page)
    try:
        open_visibility(page)
    except Exception:
        page.get_by_text(re.compile(r"Private|Visibility|Scheduled", re.I)).first.click(
            force=True
        )
        page.wait_for_timeout(1200)
    result["expand"] = expand_schedule(page)
    set_date_time(page, day, "11:30", result)
    click_done(page)
    result["saved"] = save_edit(page)
    page.wait_for_timeout(2200)
    body = page.locator("body").inner_text()
    snip = body.split("Visibility", 1)[-1][:220] if "Visibility" in body else body[:220]
    result["visibility_snip"] = snip.replace("\n", " ")
    result["ok"] = "Scheduled" in snip or "11:30" in snip
    page.screenshot(path=str(AUDIT / f"sched_{item['id']}.png"))
    return result


def set_related(page, sid: str, num: str) -> dict:
    r: dict = {"id": num, "video_id": sid, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{sid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    picker = page.locator("ytcp-shorts-content-links-picker")
    if picker.count():
        picker.first.scroll_into_view_if_needed()
        picker.first.click(force=True)
    else:
        page.get_by_text("Related video", exact=True).first.click(force=True)
    page.wait_for_timeout(1500)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
    except Exception:
        r["error"] = "no_dialog"
        return r
    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    for q in (LONG_TITLE, LONG_ID, "Neutron Star", "neutron"):
        search.first.fill(q)
        page.wait_for_timeout(2500)
        body = page.locator("ytcp-video-pick-dialog").inner_text()
        if "No matching results" not in body:
            break
    else:
        r["error"] = "not_found"
        page.keyboard.press("Escape")
        return r
    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
    for i in range(cells.count()):
        t = cells.nth(i).inner_text()
        is_short = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(
            r"\b[1-9]:\d{2}\b|\b1[0-9]:\d{2}\b", t
        )
        if (LONG_ID in t or "Neutron" in t) and not is_short:
            cells.nth(i).click(force=True)
            r["picked"] = t[:180]
            break
    else:
        r["error"] = "no_cell"
        page.keyboard.press("Escape")
        return r
    page.wait_for_timeout(800)
    for name in ("Done", "Select", "Save"):
        b = page.get_by_role("button", name=name, exact=True)
        if b.count() and b.first.is_visible() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(800)
            break
    r["saved"] = save_edit(page)
    page.goto(
        f"https://studio.youtube.com/video/{sid}/edit", wait_until="domcontentloaded"
    )
    page.wait_for_timeout(3000)
    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:280] if "Related video" in body else ""
    r["related_chunk"] = chunk.replace("\n", " ")
    r["ok"] = "None" not in chunk[:50] and (
        "Neutron" in chunk or LONG_ID in chunk or "Body" in chunk
    )
    page.screenshot(path=str(AUDIT / f"rel_{num}.png"))
    return r


def main() -> int:
    AUDIT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text())
    report: dict = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "related_target": LONG_ID,
        "uploads": [],
        "schedules": [],
        "related": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        ensure_orbit_channel(page)

        for item in manifest["shorts"]:
            print(f"Upload {item['id']} {item['title']}…", flush=True)
            up = upload_one(page, item)
            report["uploads"].append(up)
            print(json.dumps(up, indent=2), flush=True)
            OUT.write_text(json.dumps(report, indent=2))
            if not up.get("ok"):
                continue
            vid = up["video_id"]
            print(f"Schedule {vid}…", flush=True)
            sch = schedule_one(page, item, vid)
            report["schedules"].append(sch)
            print(json.dumps(sch, indent=2), flush=True)
            print(f"Related {vid} → {LONG_ID}…", flush=True)
            rel = set_related(page, vid, item["id"])
            report["related"].append(rel)
            print(json.dumps(rel, indent=2), flush=True)
            OUT.write_text(json.dumps(report, indent=2))

        page.close()
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    report["all_ok"] = (
        len(report["uploads"]) == 3
        and all(u.get("ok") for u in report["uploads"])
        and all(s.get("ok") for s in report["schedules"])
        and all(r.get("ok") for r in report["related"])
    )
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
