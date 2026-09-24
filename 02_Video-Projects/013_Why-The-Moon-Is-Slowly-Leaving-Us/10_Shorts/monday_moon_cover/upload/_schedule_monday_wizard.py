#!/usr/bin/env python3
"""Set Monday 5 Oct 2026 11:30 on the open Moon Short wizard, then Related."""
from __future__ import annotations

import base64
import json
import re
import shutil
import time
import urllib.request
from pathlib import Path

import websocket

ROOT = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "013_Why-The-Moon-Is-Slowly-Leaving-Us/10_Shorts/monday_moon_cover"
)
THUMB = ROOT / "thumb/monday_moon_thumb.jpg"
VIDEO_ID = "dQlOgsDGmtA"
LONG_ID = "2fsQcea-voM"
OUT = ROOT / "upload/monday_moon_short_upload_result.json"
AUDIT = ROOT / "upload/_studio_audit"
STORE = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-01a0cd79-01ff-7df2-abc0-ae6e8554b895/files"
)
FROZEN = {"-jmMROGoZCM", "Ih2zhZTbIR0", "pL339HhjDwo", "oFTYeBFtSQ4", "Y_SQGPd4Amc", "G8DiaNjD2WE"}


class CDP:
    def __init__(self) -> None:
        ver = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=5))
        self.ws = websocket.create_connection(
            ver["webSocketDebuggerUrl"], timeout=25, suppress_origin=True, max_size=40_000_000
        )
        self.n = 0
        self.sid = ""

    def call(self, method: str, params: dict | None = None, timeout: float = 25, session: bool = False) -> dict:
        self.n += 1
        mid = self.n
        msg: dict = {"id": mid, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = self.sid
        self.ws.send(json.dumps(msg))
        self.ws.settimeout(timeout)
        deadline = time.time() + timeout
        while time.time() < deadline:
            data = json.loads(self.ws.recv())
            if data.get("id") != mid:
                continue
            if "error" in data:
                raise RuntimeError(f"{method}: {data['error']}")
            return data.get("result") or {}
        raise TimeoutError(method)

    def js(self, expression: str, timeout: float = 20):
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True},
            timeout=timeout,
            session=True,
        )
        if result.get("exceptionDetails"):
            raise RuntimeError(json.dumps(result["exceptionDetails"])[:500])
        return (result.get("result") or {}).get("value")

    def shot(self, name: str) -> None:
        data = self.call("Page.captureScreenshot", {"format": "png"}, timeout=20, session=True)
        (AUDIT / name).write_bytes(base64.b64decode(data["data"]))


def wizard_text(cdp: CDP) -> str:
    return cdp.js(
        r"""
        (() => {
          const nodes = [...document.querySelectorAll('ytcp-uploads-dialog, tp-yt-paper-dialog')];
          const hit = nodes.map(n => n.innerText || '').find(t => t.includes('Why the Moon Is Leaving Us') && t.includes('Visibility'));
          return hit || '';
        })()
        """
    ) or ""


def click_wizard(cdp: CDP, label: str) -> str:
    return cdp.js(
        r"""
        ((label) => {
          const nodes = [...document.querySelectorAll('ytcp-uploads-dialog, tp-yt-paper-dialog')];
          const root = nodes.find(n => (n.innerText || '').includes('Visibility')) || document;
          const visit = (node, fn) => {
            if (!node || !node.querySelectorAll) return;
            for (const el of node.querySelectorAll('*')) {
              fn(el);
              if (el.shadowRoot) visit(el.shadowRoot, fn);
            }
          };
          let best = null;
          visit(root, (el) => {
            const t = (el.innerText || '').trim();
            if (t !== label) return;
            const tag = (el.tagName || '').toLowerCase();
            const role = el.getAttribute && el.getAttribute('role');
            if (label === 'Schedule' && (role === 'radio' || tag === 'tp-yt-paper-radio-button')) return;
            const r = el.getBoundingClientRect();
            if (r.width < 30 || r.height < 14) return;
            if (!best || r.top > best.top) best = {el, top: r.top};
          });
          if (!best) return 'missing';
          best.el.click();
          return 'clicked';
        })
        """
        + f"({json.dumps(label)})"
    ) or ""


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    cdp = CDP()
    infos = cdp.call("Target.getTargets").get("targetInfos") or []
    tid = next(i["targetId"] for i in infos if "dQlOgsDGmtA/edit" in (i.get("url") or ""))
    cdp.call("Target.activateTarget", {"targetId": tid})
    attached = cdp.call("Target.attachToTarget", {"targetId": tid, "flatten": True})
    cdp.sid = attached["sessionId"]
    try:
        href = cdp.js("location.href") or ""
        if VIDEO_ID not in href or any(item in href for item in FROZEN):
            raise SystemExit(href)
        text = wizard_text(cdp)
        if "Visibility" not in text:
            cdp.js("document.querySelector('#action-1') && document.querySelector('#action-1').click()")
            time.sleep(2)
            text = wizard_text(cdp)
        if VIDEO_ID not in text and "Why the Moon Is Leaving Us" not in text:
            raise SystemExit("wizard is not the Moon Short")
        for _ in range(5):
            text = wizard_text(cdp)
            if "Choose when to publish" in text:
                break
            step = cdp.js(
                """(() => {
                  const b = document.querySelector('#next-button');
                  if (!b) return 'missing';
                  b.click();
                  return 'clicked';
                })()"""
            )
            if step != "clicked":
                break
            time.sleep(1.2)
        text = wizard_text(cdp)
        if "Choose when to publish" not in text:
            (AUDIT / "09_wizard.txt").write_text(text[:4000])
            cdp.shot("09_wizard.png")
            raise SystemExit("visibility step not open")
        radio = cdp.js(
            r"""
            (() => {
              const nodes = [...document.querySelectorAll('ytcp-uploads-dialog, tp-yt-paper-dialog')];
              const root = nodes.find(n => (n.innerText || '').includes('Choose when to publish')) || document;
              const visit = (node, fn) => {
                if (!node || !node.querySelectorAll) return;
                for (const el of node.querySelectorAll('*')) {
                  fn(el);
                  if (el.shadowRoot) visit(el.shadowRoot, fn);
                }
              };
              let hit = 'missing';
              visit(root, (el) => {
                const role = el.getAttribute && el.getAttribute('role');
                const tag = (el.tagName || '').toLowerCase();
                const own = ((el.innerText || '')).trim();
                if ((role === 'radio' || tag === 'tp-yt-paper-radio-button') && own === 'Schedule') {
                  el.click();
                  hit = 'radio';
                }
              });
              return hit;
            })()
            """
        )
        time.sleep(0.8)
        opened = cdp.js(
            r"""
            (() => {
              const hits = [];
              const visit = (node) => {
                if (!node || !node.querySelectorAll) return;
                for (const el of node.querySelectorAll('*')) {
                  const t = (el.innerText || '').trim();
                  if (/^\d{1,2}\s+[A-Za-z]{3,9}\s+2026$/.test(t) || /^[A-Za-z]{3,9}\s+\d{1,2},\s+2026$/.test(t)) {
                    const r = el.getBoundingClientRect();
                    if (r.width > 20 && r.height > 8 && el.childElementCount < 4) hits.push(el);
                  }
                  if (el.shadowRoot) visit(el.shadowRoot);
                }
              };
              visit(document);
              if (!hits.length) return '';
              hits.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
              hits[0].click();
              return (hits[0].innerText || '').trim();
            })()
            """
        )
        time.sleep(0.6)
        picked = ""
        for i in range(4):
            picked = cdp.js(
                r"""
                (() => {
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
                    if (/^5\s+October\s+2026$|^October\s+5,?\s+2026$|^5\s+Oct\s+2026$/i.test(label)) day = el;
                  });
                  if (!day) return '';
                  day.click();
                  return (day.getAttribute('aria-label') || '').trim();
                })()
                """
            ) or ""
            if picked:
                break
            if i >= 2:
                break
            cdp.js(
                r"""
                (() => {
                  const visit = (node, fn) => {
                    if (!node || !node.querySelectorAll) return;
                    for (const el of node.querySelectorAll('*')) {
                      fn(el);
                      if (el.shadowRoot) visit(el.shadowRoot, fn);
                    }
                  };
                  let next = null;
                  visit(document, (el) => {
                    const label = ((el.getAttribute && el.getAttribute('aria-label')) || '').trim();
                    if (label === 'Next month') next = el;
                  });
                  if (next) next.click();
                  return !!next;
                })()
                """
            )
            time.sleep(0.4)
        time.sleep(0.4)
        time_note = cdp.js(
            r"""
            (() => {
              const visit = (node, fn) => {
                if (!node || !node.querySelectorAll) return;
                for (const el of node.querySelectorAll('input')) {
                  fn(el);
                  if (el.shadowRoot) visit(el.shadowRoot, fn);
                }
                for (const el of node.querySelectorAll('*')) if (el.shadowRoot) visit(el.shadowRoot, fn);
              };
              let time = null;
              visit(document, (el) => {
                if (!el || el.tagName !== 'INPUT') return;
                const label = (el.getAttribute('aria-label') || '') + ' ' + (el.getAttribute('placeholder') || '');
                if (/time/i.test(label) || el.type === 'time') time = el;
              });
              if (!time) return 'no-time';
              const current = time.value || '';
              const twelve = /[ap]m/i.test(current) || /[ap]\.?m/i.test(time.getAttribute('aria-label') || '');
              const value = twelve ? '11:30 AM' : '11:30';
              const proto = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
              proto.set.call(time, value);
              time.dispatchEvent(new Event('input', { bubbles: true }));
              time.dispatchEvent(new Event('change', { bubbles: true }));
              time.blur();
              return current + ' -> ' + (time.value || value);
            })()
            """
        )
        time.sleep(0.7)
        vis = wizard_text(cdp)
        note = f"radio={radio}\nopened={opened}\npicked={picked}\ntime={time_note}\n\n{vis}"
        (AUDIT / "09_visibility.txt").write_text(note)
        cdp.shot("09_visibility.png")
        ok_date = bool(re.search(r"5\s+Oct|October\s+5|5\s+October", vis, re.I)) and "11:30" in vis
        zone = re.search(r"GMT\s*([+-])\s*(\d+)", vis)
        bad_zone = False
        if zone:
            offset = zone.group(2).lstrip("0") or "0"
            bad_zone = not (zone.group(1) == "+" and offset in {"1", "100"})
        if not ok_date or bad_zone:
            result = {
                "ok": False,
                "error": "date or timezone not confirmed; left unsaved",
                "video_id": VIDEO_ID,
                "ok_date": ok_date,
                "bad_zone": bad_zone,
                "radio": radio,
                "picked": picked,
                "time": time_note,
            }
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2), flush=True)
            return
        clicked = cdp.js(
            """(() => {
              const done = document.querySelector('#done-button');
              if (done && (done.innerText || '').trim() === 'Schedule') { done.click(); return 'clicked'; }
              return 'missing';
            })()"""
        )
        time.sleep(6)
        after = (cdp.js("(document.body.innerText || '').slice(0, 4000)") or "") + "\n" + wizard_text(cdp)
        (AUDIT / "10_scheduled.txt").write_text(after[:5000])
        cdp.shot("10_scheduled.png")
        scheduled = bool(re.search(r"5\s+Oct", after, re.I) and "11:30" in after)
        if clicked != "clicked" or not scheduled:
            result = {
                "ok": False,
                "error": "schedule click did not confirm 5 Oct 11:30",
                "clicked": clicked,
                "video_id": VIDEO_ID,
            }
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2), flush=True)
            return
        # Related on the same edit page. Close a leftover dialog first if it blocks the page.
        cdp.js(
            r"""
            (() => {
              const close = [...document.querySelectorAll('button, ytcp-button')].find(el => (el.innerText || '').trim() === 'Close');
              const dlg = document.querySelector('ytcp-uploads-dialog');
              if (dlg && close) close.click();
              return true;
            })()
            """
        )
        time.sleep(1)
        cdp.js(
            r"""
            (() => {
              const picker = document.querySelector('ytcp-shorts-content-links-picker');
              if (picker) { picker.scrollIntoView({block:'center'}); picker.click(); return 'picker'; }
              const all = [];
              const visit = (node) => {
                if (!node || !node.querySelectorAll) return;
                for (const el of node.querySelectorAll('*')) {
                  all.push(el);
                  if (el.shadowRoot) visit(el.shadowRoot);
                }
              };
              visit(document);
              const hit = all.find(el => (el.innerText || '').trim() === 'Related video');
              if (hit) { hit.click(); return 'text'; }
              return 'missing';
            })()
            """
        )
        time.sleep(1.5)
        filled = cdp.js(
            r"""
            ((id) => {
              const dlg = document.querySelector('ytcp-video-pick-dialog');
              if (!dlg) return 'no-dialog';
              const input = dlg.querySelector('#search-yours') || dlg.querySelector('input');
              if (!input) return 'no-input';
              const proto = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
              input.focus();
              proto.set.call(input, id);
              input.dispatchEvent(new Event('input', { bubbles: true }));
              return 'filled';
            })
            """
            + f"({json.dumps(LONG_ID)})"
        )
        time.sleep(2.5)
        picked_cell = cdp.js(
            r"""
            ((id) => {
              const dlg = document.querySelector('ytcp-video-pick-dialog');
              if (!dlg) return '';
              const cells = [...dlg.querySelectorAll('ytcp-video-list-cell-video, ytcp-entity-card')];
              for (const cell of cells) {
                const t = cell.innerText || '';
                if (t.includes(id) || /Slowly Leaving/.test(t)) { cell.click(); return t.slice(0, 180); }
              }
              return '';
            })
            """
            + f"({json.dumps(LONG_ID)})"
        ) or ""
        time.sleep(0.6)
        if picked_cell:
            cdp.js(
                r"""
                (() => {
                  const buttons = [...document.querySelectorAll('button, ytcp-button')];
                  for (const name of ['Select', 'Done']) {
                    const b = buttons.find(el => (el.innerText || '').trim() === name && el.getBoundingClientRect().width > 20);
                    if (b) { b.click(); return name; }
                  }
                  return '';
                })()
                """
            )
            time.sleep(0.8)
            cdp.js("(() => { const b=[...document.querySelectorAll('button, ytcp-button')].find(el => (el.innerText||'').trim()==='Save' && el.getBoundingClientRect().width>20); if (b) b.click(); return !!b; })()")
            time.sleep(2.5)
        body = cdp.js("(document.body.innerText || '').slice(0, 7000)") or ""
        chunk = body.split("Related video", 1)[-1][:300] if "Related video" in body else ""
        cdp.shot("11_related.png")
        (AUDIT / "11_related.txt").write_text(chunk)
        related_ok = bool(picked_cell) and ("Leaving" in chunk or LONG_ID in chunk)
        result = {
            "ok": related_ok,
            "video_id": VIDEO_ID,
            "schedule": "2026-10-05T10:30:00.000Z",
            "publish": "Monday 5 Oct 2026, 11:30 UK",
            "scheduled": True,
            "privacy": "private",
            "madeForKids": False,
            "altered": True,
            "related": LONG_ID if related_ok else "",
            "pinned": False,
            "related_filled": filled,
            "related_picked": picked_cell,
            "related_chunk": chunk,
            "clicked": clicked,
        }
        if result["scheduled"]:
            dest = STORE / "media/moon-short-thumb.jpg"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(THUMB, dest)
            result["thumb_copy_bytes"] = dest.stat().st_size
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
    finally:
        try:
            cdp.call("Target.detachFromTarget", {"sessionId": cdp.sid}, timeout=5)
        except Exception:
            pass
        cdp.ws.close()


if __name__ == "__main__":
    main()
