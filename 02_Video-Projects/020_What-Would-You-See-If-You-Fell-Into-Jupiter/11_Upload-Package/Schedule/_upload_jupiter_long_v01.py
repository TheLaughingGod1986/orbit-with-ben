#!/usr/bin/env python3
"""Schedule the Jupiter long in the already-open Studio Chrome.

New tab only. Private until Sunday 4 Oct 2026 18:00 Europe/London.
Does not delete anything and does not touch other Studio tabs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "020_What-Would-You-See-If-You-Fell-Into-Jupiter"
)
VIDEO = ROOT / "09_Final-Export/jupiter_film_v04.mp4"
THUMB = ROOT / "08_Thumbnail/Selected/jupiter_thumb_primary_cloud-deck.jpg"
DESC = (ROOT / "11_Upload-Package/Descriptions/jupiter_long_description_v01.txt").read_text()
TAGS = ", ".join(
    line.strip()
    for line in (ROOT / "11_Upload-Package/Tags/jupiter_long_tags_v01.txt").read_text().splitlines()
    if line.strip()
)
PINNED = (ROOT / "11_Upload-Package/Pinned-Comments/jupiter_long_pinned_v01.txt").read_text().strip()
TITLE = "What Would You See If You Fell Into Jupiter?"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
OUT = ROOT / "11_Upload-Package/Schedule/jupiter_longform_upload_result.json"
AUDIT = ROOT / "11_Upload-Package/Schedule/_studio_audit"
CDP = "http://127.0.0.1:9222"


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Not now", "No thanks", "Skip"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(timeout=700)
        except Exception:
            pass


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


def _shadow_eval(page, script: str):
    return page.evaluate(script)


def schedule_sunday(page) -> str:
    page.get_by_text("Schedule", exact=True).first.click()
    page.wait_for_timeout(900)
    opened = _shadow_eval(
        page,
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
          const root = document.querySelector('ytcp-uploads-dialog') || document;
          const visitAll = (node) => {
            if (!node || !node.querySelectorAll) return;
            visit(node);
            for (const el of node.querySelectorAll('*')) {
              if (el.shadowRoot) visitAll(el.shadowRoot);
            }
          };
          visitAll(root);
          if (!hits.length) return '';
          hits.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
          hits[0].click();
          return (hits[0].innerText || '').trim();
        }""",
    )
    page.wait_for_timeout(700)
    picked = ""
    for _ in range(6):
        picked = _shadow_eval(
            page,
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
                const label = (el.getAttribute && (el.getAttribute('aria-label') || '')) || '';
                if (/^4\\s+October\\s+2026$|^October\\s+4,?\\s+2026$|^4\\s+Oct\\s+2026$/i.test(label.trim())) {
                  day = el;
                }
              });
              if (day) { day.click(); return (day.getAttribute('aria-label') || '').trim(); }
              let next = null;
              visit(document, (el) => {
                const label = ((el.getAttribute && el.getAttribute('aria-label')) || el.innerText || '').trim();
                if (/^Next month$/i.test(label)) next = el;
              });
              if (next) next.click();
              return '';
            }""",
        )
        if picked:
            break
        page.wait_for_timeout(400)
    page.wait_for_timeout(500)
    time_note = _shadow_eval(
        page,
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
          const twelve = /[ap]m/i.test(current) || /[ap]\\.?m/i.test(time.getAttribute('aria-label') || '');
          const value = twelve ? '6:00 PM' : '18:00';
          const proto = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
          proto.set.call(time, value);
          time.dispatchEvent(new Event('input', { bubbles: true }));
          time.dispatchEvent(new Event('change', { bubbles: true }));
          return current + ' -> ' + (time.value || value);
        }""",
    )
    page.wait_for_timeout(400)
    text = page.locator("ytcp-uploads-dialog").inner_text()
    return f"opened={opened}\npicked={picked}\ntime={time_note}\n\n{text}"


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result = {
        "ok": False,
        "title": TITLE,
        "thumb": str(THUMB),
        "schedule": "2026-10-04T17:00:00Z",
        "privacy": "private",
        "madeForKids": False,
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next(
            (pg for pg in ctx.pages if "videos/upload" in (pg.url or "")),
            None,
        )
        if page is None:
            page = ctx.new_page()
            page.goto(
                f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
                wait_until="domcontentloaded",
                timeout=120000,
            )
        page.bring_to_front()
        page.wait_for_timeout(1500)
        dismiss(page)
        # connect_over_cdp refuses files over 50MB. Chrome can set a local path directly.
        captured: dict[str, str] = {}

        def on_response(response) -> None:
            url = response.url
            if "youtubei" not in url and "upload" not in url:
                return
            try:
                body = response.text()
            except Exception:
                return
            match = re.search(r'"videoId"\s*:\s*"([A-Za-z0-9_-]{11})"', body)
            if match:
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
            raise RuntimeError(f"file input missing: {found}")
        print("attaching", VIDEO, flush=True)
        session.send(
            "DOM.setFileInputFiles",
            {"nodeId": node_id, "files": [str(VIDEO)]},
        )
        print("attached, waiting for title", flush=True)
        title_box = page.get_by_role("textbox", name=re.compile(r"title that describes", re.I))
        title_box.wait_for(timeout=900000)
        page.wait_for_timeout(1500)
        title_box.fill(TITLE)
        desc = page.get_by_role("textbox", name=re.compile(r"tell viewers about your video", re.I))
        desc.click()
        desc.fill(DESC)
        page.get_by_text("No, it's not made for kids", exact=False).click()
        altered = page.evaluate(
            """() => {
              const radios = [];
              const visit = (node) => {
                if (!node || !node.querySelectorAll) return;
                for (const el of node.querySelectorAll('[role="radio"], tp-yt-paper-radio-button')) {
                  radios.push(el);
                  if (el.shadowRoot) visit(el.shadowRoot);
                }
                for (const el of node.querySelectorAll('*')) {
                  if (el.shadowRoot) visit(el.shadowRoot);
                }
              };
              visit(document.querySelector('ytcp-uploads-dialog') || document);
              for (const el of radios) {
                const own = (el.innerText || el.getAttribute('aria-label') || '').trim();
                if (!/^yes\\b/i.test(own) || /kids/i.test(own)) continue;
                let blob = own;
                let node = el;
                for (let i = 0; i < 8 && node; i++) {
                  blob += ' ' + (node.innerText || '');
                  node = node.parentElement || (node.getRootNode && node.getRootNode().host);
                }
                if (/altered|synthetic/i.test(blob)) {
                  el.click();
                  return own;
                }
              }
              return '';
            }"""
        )
        result["altered"] = altered or "not-set"
        try:
            page.get_by_role("button", name="Show more").click(timeout=2500)
            page.wait_for_timeout(400)
            page.get_by_role("textbox", name="Tags").fill(TAGS)
            result["tags"] = True
        except Exception as exc:
            result["tags_err"] = str(exc)[:180]
        try:
            page.get_by_text("Add a first comment", exact=False).first.click(timeout=2000)
            page.wait_for_timeout(300)
            page.keyboard.type(PINNED)
            result["first_comment"] = True
        except Exception as exc:
            result["first_comment_err"] = str(exc)[:180]
        page.locator('input[type="file"][accept*="image"]').last.set_input_files(str(THUMB))
        page.wait_for_timeout(2000)
        result["thumb_set"] = True
        page.screenshot(path=str(AUDIT / "02_details.png"))
        next_to_visibility(page)
        vis = schedule_sunday(page)
        (AUDIT / "03_visibility.txt").write_text(vis)
        page.screenshot(path=str(AUDIT / "03_visibility.png"))
        ok_date = bool(re.search(r"4\s+Oct|Oct(?:ober)?\s+4|4\s+October", vis, re.I)) and (
            "18:00" in vis or "6:00" in vis
        )
        result["visibility_has_date"] = ok_date
        result["video_id"] = captured.get("video_id", "")
        if not ok_date or result.get("altered") in ("", "not-set"):
            result["error"] = "schedule date not confirmed; left unsaved"
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2), flush=True)
            return
        page.get_by_role("button", name="Schedule", exact=True).last.click()
        page.wait_for_timeout(8000)
        page.screenshot(path=str(AUDIT / "04_after_save.png"))
        body = page.locator("body").inner_text()
        vid = captured.get("video_id", "")
        for pat in (r"youtu\.be/([A-Za-z0-9_-]{11})", r"/video/([A-Za-z0-9_-]{11})/"):
            m = re.search(pat, body + " " + page.url)
            if m and m.group(1) not in ("upload", "shorts"):
                vid = m.group(1)
                break
        result["video_id"] = vid
        result["ok"] = bool(vid)
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
