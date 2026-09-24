#!/usr/bin/env python3
"""Schedule the passed Monday Moon Short. New Studio tab only.

Private until Monday 5 Oct 2026 11:30 Europe/London.
Does not touch the Jupiter long or the Last Star / Neutron Shorts.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "013_Why-The-Moon-Is-Slowly-Leaving-Us/10_Shorts/monday_moon_cover"
)
VIDEO = ROOT / "monday_moon_short_v10.mp4"
THUMB = ROOT / "thumb/monday_moon_thumb.jpg"
TITLE = "Why the Moon Is Leaving Us"
DESC = (
    "Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone\n"
    "https://www.youtube.com/watch?v=2fsQcea-voM\n"
)
TAGS = "moon leaving earth, moon drifting away, why the moon is leaving us, lunar eclipse, moon, space documentary"
LONG_ID = "2fsQcea-voM"
LONG_TITLE = "Why the Moon Is Slowly Leaving Us"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
OUT = ROOT / "upload/monday_moon_short_upload_result.json"
AUDIT = ROOT / "upload/_studio_audit"
CDP = "http://127.0.0.1:9222"
FROZEN = {"-jmMROGoZCM", "Ih2zhZTbIR0", "pL339HhjDwo", "oFTYeBFtSQ4", "Y_SQGPd4Amc", "G8DiaNjD2WE"}


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Not now", "No thanks", "Skip"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(timeout=700)
        except Exception:
            pass


def abort_cushion(page) -> None:
    label = page.evaluate(
        """() => {
          const b=[...document.querySelectorAll('button')].find(el => {
            const t=el.innerText||'';
            if (!/Agree|Redeem/i.test(t)) return false;
            const r=el.getBoundingClientRect();
            return r.width>20 && r.height>20;
          });
          return b ? (b.innerText||'').trim().slice(0,80) : '';
        }"""
    )
    if label:
        raise SystemExit(f"cushion button visible, not clicking: {label}")


def next_to_visibility(page) -> None:
    for _ in range(12):
        dismiss(page)
        dlg = page.locator("ytcp-uploads-dialog")
        text = dlg.inner_text() if dlg.count() else ""
        if "Visibility" in text and "Schedule" in text:
            return
        nxt = page.get_by_role("button", name="Next", exact=True)
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click()
            page.wait_for_timeout(1500)
        else:
            page.wait_for_timeout(800)


def shadow_click_date(page) -> str:
    opened = page.evaluate(
        """() => {
          const hits = [];
          const visit = (node) => {
            if (!node || !node.querySelectorAll) return;
            for (const el of node.querySelectorAll('button, ytcp-dropdown-trigger, tp-yt-paper-button, div, span')) {
              const t = (el.innerText || '').trim();
              if (/^\\d{1,2}\\s+[A-Za-z]{3,9}\\s+2026$/.test(t) || /^[A-Za-z]{3,9}\\s+\\d{1,2},\\s+2026$/.test(t)) {
                const r = el.getBoundingClientRect();
                if (r.width > 20 && r.height > 8) hits.push(el);
              }
              if (el.shadowRoot) visit(el.shadowRoot);
            }
          };
          visit(document.querySelector('ytcp-uploads-dialog') || document);
          if (!hits.length) return '';
          hits.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
          hits[0].click();
          return (hits[0].innerText || '').trim();
        }"""
    )
    page.wait_for_timeout(700)
    picked = ""
    for _ in range(8):
        picked = page.evaluate(
            """() => {
              const visit = (node, fn) => {
                if (!node || !node.querySelectorAll) return;
                for (const el of node.querySelectorAll('*')) {
                  fn(el);
                  if (el.shadowRoot) visit(el.shadowRoot, fn);
                }
              };
              let day = null;
              visit(document, (el) => {
                const label = ((el.getAttribute && el.getAttribute('aria-label')) || '').trim();
                if (/^5\\s+October\\s+2026$|^October\\s+5,?\\s+2026$|^5\\s+Oct\\s+2026$/i.test(label)) day = el;
              });
              if (day) { day.click(); return (day.getAttribute('aria-label') || '').trim(); }
              let next = null;
              visit(document, (el) => {
                const label = ((el.getAttribute && el.getAttribute('aria-label')) || el.innerText || '').trim();
                if (/^Next month$/i.test(label)) next = el;
              });
              if (next) next.click();
              return '';
            }"""
        )
        if picked:
            break
        page.wait_for_timeout(400)
    page.wait_for_timeout(500)
    time_note = page.evaluate(
        """() => {
          const visit = (node, fn) => {
            if (!node || !node.querySelectorAll) return;
            for (const el of node.querySelectorAll('input')) {
              fn(el);
              if (el.shadowRoot) visit(el.shadowRoot, fn);
            }
          };
          let time = null;
          visit(document.querySelector('ytcp-uploads-dialog') || document, (el) => {
            const label = (el.getAttribute('aria-label') || '') + ' ' + (el.getAttribute('placeholder') || '');
            if (/time/i.test(label) || el.type === 'time') time = el;
          });
          if (!time) return 'no-time';
          const current = time.value || '';
          const twelve = /[ap]m/i.test(current);
          const value = twelve ? '11:30 AM' : '11:30';
          const proto = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
          proto.set.call(time, value);
          time.dispatchEvent(new Event('input', { bubbles: true }));
          time.dispatchEvent(new Event('change', { bubbles: true }));
          return current + ' -> ' + (time.value || value);
        }"""
    )
    text = page.locator("ytcp-uploads-dialog").inner_text()
    return f"opened={opened}\npicked={picked}\ntime={time_note}\n\n{text}"


def set_related(page, video_id: str) -> dict:
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
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
    page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    search.first.fill(LONG_ID)
    page.wait_for_timeout(2500)
    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
    picked = ""
    for i in range(min(cells.count(), 8)):
        t = cells.nth(i).inner_text()
        if LONG_ID in t or "Slowly Leaving" in t:
            cells.nth(i).click(force=True)
            picked = t[:180]
            break
    if not picked:
        return {"ok": False, "error": "moon long not in picker"}
    page.wait_for_timeout(800)
    for name in ("Select", "Done"):
        b = page.get_by_role("button", name=name, exact=True)
        if b.count() and b.first.is_visible() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(800)
            break
    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click()
        page.wait_for_timeout(2500)
    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:220] if "Related video" in body else ""
    return {"ok": LONG_ID in chunk or "Leaving" in chunk, "picked": picked, "chunk": chunk}


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    if not VIDEO.exists() or VIDEO.stat().st_size != 9582309:
        raise SystemExit(f"passed cut missing or wrong size: {VIDEO}")
    result = {
        "ok": False,
        "title": TITLE,
        "description": DESC.strip(),
        "thumb": str(THUMB),
        "schedule": "2026-10-05T10:30:00.000Z",
        "privacy": "private",
        "madeForKids": False,
        "related": LONG_ID,
        "pinned": False,
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            url = pg.url or ""
            for frozen in FROZEN:
                if frozen in url:
                    continue
        page = ctx.new_page()
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.bring_to_front()
        page.wait_for_timeout(1500)
        dismiss(page)
        abort_cushion(page)
        captured: dict[str, str] = {}

        def on_response(response) -> None:
            if "youtubei" not in response.url and "upload" not in response.url:
                return
            try:
                body = response.text()
            except Exception:
                return
            match = re.search(r'"videoId"\s*:\s*"([A-Za-z0-9_-]{11})"', body)
            if match and match.group(1) not in FROZEN:
                captured["video_id"] = match.group(1)

        page.on("response", on_response)
        session = page.context.new_cdp_session(page)
        doc = session.send("DOM.getDocument", {"depth": -1, "pierce": True})
        found = session.send(
            "DOM.querySelector",
            {"nodeId": doc["root"]["nodeId"], "selector": 'input[type="file"]'},
        )
        node_id = found.get("nodeId") or 0
        if not node_id:
            raise RuntimeError("file input missing")
        session.send("DOM.setFileInputFiles", {"nodeId": node_id, "files": [str(VIDEO)]})
        title_box = page.get_by_role("textbox", name=re.compile(r"title that describes", re.I))
        title_box.wait_for(timeout=180000)
        page.wait_for_timeout(1200)
        title_box.fill(TITLE)
        desc = page.get_by_role("textbox", name=re.compile(r"tell viewers about your video", re.I))
        desc.click()
        desc.fill(DESC)
        page.get_by_text("No, it's not", exact=False).first.click()
        altered = page.evaluate(
            """() => {
              const visit = (node, fn) => {
                if (!node || !node.querySelectorAll) return;
                for (const el of node.querySelectorAll('*')) {
                  fn(el);
                  if (el.shadowRoot) visit(el.shadowRoot, fn);
                }
              };
              let hit = '';
              visit(document.querySelector('ytcp-uploads-dialog') || document, (el) => {
                const own = (el.innerText || el.getAttribute('aria-label') || '').trim();
                if (!/^yes\\b/i.test(own) || /kids/i.test(own)) return;
                let blob = own;
                let node = el;
                for (let i = 0; i < 8 && node; i++) {
                  blob += ' ' + (node.innerText || '');
                  node = node.parentElement || (node.getRootNode && node.getRootNode().host);
                }
                if (/altered|synthetic/i.test(blob)) { el.click(); hit = own; }
              });
              return hit;
            }"""
        )
        result["altered"] = altered or "not-set"
        try:
            page.get_by_role("button", name="Show more").click(timeout=2500)
            page.wait_for_timeout(400)
            page.get_by_role("textbox", name="Tags").fill(TAGS)
        except Exception as exc:
            result["tags_err"] = str(exc)[:160]
        page.locator('input[type="file"][accept*="image"]').last.set_input_files(str(THUMB))
        page.wait_for_timeout(2000)
        page.screenshot(path=str(AUDIT / "01_details.png"))
        next_to_visibility(page)
        vis = shadow_click_date(page)
        (AUDIT / "02_visibility.txt").write_text(vis)
        page.screenshot(path=str(AUDIT / "02_visibility.png"))
        ok_date = bool(re.search(r"5\s+Oct|October\s+5|5\s+October", vis, re.I)) and "11:30" in vis
        result["visibility_has_date"] = ok_date
        result["video_id"] = captured.get("video_id", "")
        if not ok_date or result["altered"] in ("", "not-set"):
            result["error"] = "date or disclosure not confirmed; left unsaved"
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2), flush=True)
            return
        page.get_by_role("button", name="Schedule", exact=True).last.click()
        page.wait_for_timeout(8000)
        page.screenshot(path=str(AUDIT / "03_scheduled.png"))
        body = page.locator("body").inner_text() + " " + page.url
        vid = captured.get("video_id", "")
        for pat in (r"youtu\.be/([A-Za-z0-9_-]{11})", r"/video/([A-Za-z0-9_-]{11})"):
            m = re.search(pat, body)
            if m and m.group(1) not in FROZEN and m.group(1) not in ("upload",):
                vid = m.group(1)
                break
        result["video_id"] = vid
        result["schedule_text"] = "5 October" in body or "5 Oct" in body
        if not vid:
            result["error"] = "scheduled but video id not captured"
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2), flush=True)
            return
        related = set_related(page, vid)
        result["related_result"] = related
        page.screenshot(path=str(AUDIT / "04_related.png"))
        result["ok"] = bool(related.get("ok"))
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
