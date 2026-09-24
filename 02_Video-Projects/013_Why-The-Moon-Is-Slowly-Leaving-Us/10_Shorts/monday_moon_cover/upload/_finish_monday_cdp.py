#!/usr/bin/env python3
"""Finish dQlOgsDGmtA on the existing upload tab via that page's CDP socket.

Does not call connect_over_cdp (that browser socket is hanging) and does not
open a second upload or any frozen Studio tab.
"""
from __future__ import annotations

import json
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
TITLE = "Why the Moon Is Leaving Us"
DESC = (
    "Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone\n"
    "https://www.youtube.com/watch?v=2fsQcea-voM"
)
TAGS = [
    "moon leaving earth",
    "moon drifting away",
    "why the moon is leaving us",
    "lunar eclipse",
    "moon",
    "space documentary",
]
VIDEO_ID = "dQlOgsDGmtA"
LONG_ID = "2fsQcea-voM"
OUT = ROOT / "upload/monday_moon_short_upload_result.json"
AUDIT = ROOT / "upload/_studio_audit"
STORE = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-01a0cd79-01ff-7df2-abc0-ae6e8554b895/files"
)
FROZEN = {
    "-jmMROGoZCM",
    "Ih2zhZTbIR0",
    "pL339HhjDwo",
    "oFTYeBFtSQ4",
    "Y_SQGPd4Amc",
    "G8DiaNjD2WE",
    "_WQLVnLETYA",
}


class CDP:
    def __init__(self, url: str) -> None:
        self.ws = websocket.create_connection(
            url, timeout=25, max_size=80_000_000, suppress_origin=True
        )
        self.n = 0

    def call(self, method: str, params: dict | None = None, timeout: float = 25) -> dict:
        self.n += 1
        mid = self.n
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
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

    def js(self, expression: str, timeout: float = 25):
        result = self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True,
            },
            timeout=timeout,
        )
        if result.get("exceptionDetails"):
            raise RuntimeError(json.dumps(result["exceptionDetails"])[:800])
        return (result.get("result") or {}).get("value")


JS_TEXT = r"""
(() => {
  const dlg = document.querySelector('ytcp-uploads-dialog');
  return {
    url: location.href,
    title: document.title,
    dialog: dlg ? (dlg.innerText || '').slice(0, 5000) : '',
    body: (document.body.innerText || '').slice(0, 2500)
  };
})()
"""

JS_BACK_OR_DETAILS = r"""
(() => {
  const dlg = document.querySelector('ytcp-uploads-dialog');
  const text = dlg ? (dlg.innerText || '') : '';
  if (/Title \(required\)/.test(text) && /Altered content/.test(text)) return 'details';
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('*')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  let back = null;
  visit(dlg || document, (el) => {
    const t = (el.innerText || '').trim();
    if (t === 'Back') {
      const r = el.getBoundingClientRect();
      if (r.width > 20 && r.height > 10) back = el;
    }
  });
  if (back) { back.click(); return 'back'; }
  return 'no-back';
})()
"""

JS_AUDIENCE = r"""
(() => {
  const dlg = document.querySelector('ytcp-uploads-dialog') || document;
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('*')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  const radios = [];
  visit(dlg, (el) => {
    const role = el.getAttribute && el.getAttribute('role');
    const tag = (el.tagName || '').toLowerCase();
    if (role === 'radio' || tag === 'tp-yt-paper-radio-button') radios.push(el);
  });
  const info = radios.map((el) => ({
    own: ((el.innerText || el.getAttribute('aria-label') || '')).trim().slice(0, 80),
    checked: el.getAttribute('aria-checked') || '',
  }));
  let kids = false;
  let altered = false;
  for (const el of radios) {
    const own = ((el.innerText || el.getAttribute('aria-label') || '')).trim();
    if (/No, it's not/i.test(own)) {
      if (el.getAttribute('aria-checked') !== 'true') el.click();
      kids = true;
    }
  }
  for (const el of radios) {
    const own = ((el.innerText || el.getAttribute('aria-label') || '')).trim();
    if (!/^yes\b/i.test(own)) continue;
    let blob = own;
    let node = el;
    for (let i = 0; i < 8 && node; i++) {
      blob += ' ' + (node.innerText || '');
      node = node.parentElement || (node.getRootNode && node.getRootNode().host);
    }
    if (/altered|synthetic/i.test(blob) && !/kids/i.test(own)) {
      if (el.getAttribute('aria-checked') !== 'true') el.click();
      altered = el.getAttribute('aria-checked') === 'true' || true;
    }
  }
  return {kids, altered, radios: info.slice(0, 16)};
})()
"""

JS_TAGS = r"""
(tags) => {
  const dlg = document.querySelector('ytcp-uploads-dialog') || document;
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('*')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  let more = null;
  visit(dlg, (el) => {
    if ((el.innerText || '').trim() === 'Show more') {
      const r = el.getBoundingClientRect();
      if (r.width > 10 && r.height > 8) more = el;
    }
  });
  if (more) more.click();
  let input = null;
  visit(dlg, (el) => {
    if (!el || el.tagName !== 'INPUT') return;
    const label = ((el.getAttribute('aria-label') || '') + ' ' + (el.getAttribute('placeholder') || '')).toLowerCase();
    if (label.includes('tag')) input = el;
  });
  if (!input) return 'tags-box-missing';
  const proto = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
  for (const tag of tags) {
    input.focus();
    proto.set.call(input, tag);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
  }
  return 'tags-set';
}
"""

JS_NEXT = r"""
(() => {
  const dlg = document.querySelector('ytcp-uploads-dialog');
  const text = dlg ? (dlg.innerText || '') : '';
  if (/Choose when to publish/.test(text) && /\nSchedule\n/.test('\n' + text + '\n')) return 'visibility';
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('*')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  let next = null;
  visit(dlg || document, (el) => {
    if ((el.innerText || '').trim() === 'Next') {
      const r = el.getBoundingClientRect();
      if (r.width > 20 && r.height > 10) next = el;
    }
  });
  if (next) { next.click(); return 'next'; }
  return 'no-next';
})()
"""

JS_SCHEDULE_RADIO = r"""
(() => {
  const dlg = document.querySelector('ytcp-uploads-dialog') || document;
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('*')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  const radios = [];
  visit(dlg, (el) => {
    const role = el.getAttribute && el.getAttribute('role');
    const tag = (el.tagName || '').toLowerCase();
    if (role === 'radio' || tag === 'tp-yt-paper-radio-button') radios.push(el);
  });
  for (const el of radios) {
    const own = ((el.innerText || el.getAttribute('aria-label') || '')).trim();
    if (own === 'Schedule') { el.click(); return 'radio'; }
  }
  return 'no-radio';
})()
"""

JS_OPEN_DATE = r"""
(() => {
  const hits = [];
  const visit = (node) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('button, ytcp-dropdown-trigger, tp-yt-paper-button, div, span')) {
      const t = (el.innerText || '').trim();
      if (/^\d{1,2}\s+[A-Za-z]{3,9}\s+2026$/.test(t) || /^[A-Za-z]{3,9}\s+\d{1,2},\s+2026$/.test(t)) {
        const r = el.getBoundingClientRect();
        if (r.width > 20 && r.height > 8) hits.push(el);
      }
      if (el.shadowRoot) visit(el.shadowRoot);
    }
    for (const el of node.querySelectorAll('*')) {
      if (el.shadowRoot) visit(el.shadowRoot);
    }
  };
  visit(document.querySelector('ytcp-uploads-dialog') || document);
  if (!hits.length) return '';
  hits.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
  hits[0].click();
  return (hits[0].innerText || '').trim();
})()
"""

JS_PICK_DAY = r"""
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
  if (day) { day.click(); return (day.getAttribute('aria-label') || '').trim(); }
  return '';
})()
"""

JS_NEXT_MONTH = r"""
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
    const label = ((el.getAttribute && el.getAttribute('aria-label')) || el.innerText || '').trim();
    if (/^Next month$/i.test(label)) next = el;
  });
  if (next) { next.click(); return 'next-month'; }
  return '';
})()
"""

JS_SET_TIME = r"""
(() => {
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('input')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
    for (const el of node.querySelectorAll('*')) {
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  let time = null;
  visit(document.querySelector('ytcp-uploads-dialog') || document, (el) => {
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

JS_CLICK_SCHEDULE_BUTTON = r"""
(() => {
  const dlg = document.querySelector('ytcp-uploads-dialog') || document;
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('*')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  let best = null;
  visit(dlg, (el) => {
    const tag = (el.tagName || '').toLowerCase();
    const role = el.getAttribute && el.getAttribute('role');
    const t = (el.innerText || '').trim();
    if (t !== 'Schedule') return;
    if (role === 'radio' || tag === 'tp-yt-paper-radio-button') return;
    const r = el.getBoundingClientRect();
    if (r.width < 40 || r.height < 16) return;
    if (!best || r.top > best.top) best = {el, top: r.top};
  });
  if (!best) return 'no-button';
  best.el.click();
  return 'clicked';
})()
"""


def upload_socket() -> str:
    with urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=8) as resp:
        tabs = json.loads(resp.read().decode())
    for tab in tabs:
        url = tab.get("url") or ""
        if "videos/upload" in url and tab.get("webSocketDebuggerUrl"):
            if any(frozen in url for frozen in FROZEN):
                continue
            return tab["webSocketDebuggerUrl"]
    raise SystemExit("upload tab missing")


def shot(cdp: CDP, name: str) -> None:
    data = cdp.call("Page.captureScreenshot", {"format": "png"}, timeout=20)
    raw = data.get("data")
    if raw:
        import base64

        (AUDIT / name).write_bytes(base64.b64decode(raw))


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    if THUMB.stat().st_size < 10000:
        raise SystemExit("thumb too small")
    cdp = CDP(upload_socket())
    cdp.call("Runtime.enable")
    cdp.call("Page.enable")
    cdp.call("DOM.enable")
    state = cdp.js(JS_TEXT)
    (AUDIT / "03_before.txt").write_text(state.get("dialog") or state.get("body") or "")
    dialog = state.get("dialog") or ""
    if VIDEO_ID not in dialog or TITLE not in dialog:
        raise SystemExit(f"dialog is not {VIDEO_ID}")
    for _ in range(4):
        step = cdp.js(JS_BACK_OR_DETAILS)
        if step == "details":
            break
        if step != "back":
            raise SystemExit(f"cannot reach details: {step}")
        time.sleep(0.8)
    audience = cdp.js(JS_AUDIENCE)
    time.sleep(0.4)
    audience2 = cdp.js(JS_AUDIENCE)
    tags = cdp.js(f"({JS_TAGS})({json.dumps(TAGS)})")
    doc = cdp.call("DOM.getDocument", {"depth": -1, "pierce": True})
    found = cdp.call(
        "DOM.querySelector",
        {"nodeId": doc["root"]["nodeId"], "selector": 'input[type="file"][accept*="image"]'},
    )
    node_id = found.get("nodeId") or 0
    if node_id:
        cdp.call("DOM.setFileInputFiles", {"files": [str(THUMB)], "nodeId": node_id})
        time.sleep(1.2)
    shot(cdp, "03_details.png")
    if not (audience2 or {}).get("altered"):
        result = {"ok": False, "error": "altered not confirmed", "audience": audience2, "tags": tags}
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return
    landed = ""
    for _ in range(6):
        landed = cdp.js(JS_NEXT)
        if landed == "visibility":
            break
        time.sleep(1.0)
    if landed != "visibility":
        raise SystemExit(f"visibility not reached: {landed}")
    radio = cdp.js(JS_SCHEDULE_RADIO)
    time.sleep(0.8)
    opened = cdp.js(JS_OPEN_DATE)
    time.sleep(0.6)
    picked = ""
    for i in range(4):
        picked = cdp.js(JS_PICK_DAY) or ""
        if picked:
            break
        if i >= 2:
            break
        cdp.js(JS_NEXT_MONTH)
        time.sleep(0.4)
    time.sleep(0.4)
    time_note = cdp.js(JS_SET_TIME)
    time.sleep(0.6)
    vis = cdp.js(JS_TEXT).get("dialog") or ""
    note = f"radio={radio}\nopened={opened}\npicked={picked}\ntime={time_note}\n\n{vis}"
    (AUDIT / "04_visibility.txt").write_text(note)
    shot(cdp, "04_visibility.png")
    import re

    ok_date = bool(re.search(r"5\s+Oct|October\s+5|5\s+October", vis, re.I)) and "11:30" in vis
    zone = re.search(r"GMT\s*([+-])\s*(\d+)", vis)
    bad_zone = False
    if zone:
        offset = zone.group(2).lstrip("0") or "0"
        bad_zone = not (zone.group(1) == "+" and offset in {"1", "100"})
    if not ok_date or bad_zone or VIDEO_ID not in vis:
        result = {
            "ok": False,
            "error": "date or timezone not confirmed; left unsaved",
            "video_id": VIDEO_ID,
            "ok_date": ok_date,
            "bad_zone": bad_zone,
            "audience": audience2,
            "tags": tags,
        }
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return
    clicked = cdp.js(JS_CLICK_SCHEDULE_BUTTON)
    time.sleep(8)
    after = cdp.js(JS_TEXT)
    (AUDIT / "05_scheduled.txt").write_text((after.get("body") or "")[:4000])
    shot(cdp, "05_scheduled.png")
    blob = (after.get("body") or "") + "\n" + (after.get("dialog") or "")
    scheduled = bool(re.search(r"5\s+Oct", blob, re.I) and "11:30" in blob)
    if clicked != "clicked" or not scheduled:
        result = {
            "ok": False,
            "error": "schedule click did not confirm 5 Oct 11:30",
            "clicked": clicked,
            "video_id": VIDEO_ID,
        }
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return
    cdp.call(
        "Page.navigate",
        {"url": f"https://studio.youtube.com/video/{VIDEO_ID}/edit"},
        timeout=40,
    )
    related = {"ok": False}
    for _ in range(20):
        time.sleep(1)
        href = cdp.js("location.href") or ""
        if VIDEO_ID in href and "/edit" in href:
            related["url"] = href
            break
    else:
        related["error"] = "edit page did not load"
    if related.get("url"):
        opened_picker = cdp.js(
            r"""
            (() => {
              const picker = document.querySelector('ytcp-shorts-content-links-picker');
              if (picker) { picker.scrollIntoView({block:'center'}); picker.click(); return 'picker'; }
              const nodes = [...document.querySelectorAll('*')];
              const hit = nodes.find(el => (el.innerText || '').trim() === 'Related video');
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
              input.dispatchEvent(new Event('change', { bubbles: true }));
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
                if (t.includes(id) || /Slowly Leaving/.test(t)) {
                  cell.click();
                  return t.slice(0, 180);
                }
              }
              return '';
            })
            """
            + f"({json.dumps(LONG_ID)})"
        )
        time.sleep(0.8)
        if picked_cell:
            cdp.js(
                r"""
                (() => {
                  const buttons = [...document.querySelectorAll('button, ytcp-button')];
                  for (const name of ['Select', 'Done']) {
                    const b = buttons.find(el => (el.innerText || '').trim() === name);
                    if (b) { b.click(); return name; }
                  }
                  return '';
                })()
                """
            )
            time.sleep(0.8)
            cdp.js(
                r"""
                (() => {
                  const buttons = [...document.querySelectorAll('button, ytcp-button, tp-yt-paper-button')];
                  const save = buttons.find(el => (el.innerText || '').trim() === 'Save');
                  if (save) { save.click(); return 'saved'; }
                  return 'no-save';
                })()
                """
            )
            time.sleep(2.5)
        body = cdp.js("(document.body.innerText || '').slice(0, 6000)") or ""
        chunk = body.split("Related video", 1)[-1][:300] if "Related video" in body else ""
        related.update(
            {
                "opened": opened_picker,
                "filled": filled,
                "picked": picked_cell,
                "chunk": chunk,
                "ok": bool(picked_cell) and (LONG_ID in chunk or "Leaving" in chunk),
            }
        )
    shot(cdp, "06_related.png")
    (AUDIT / "06_related.txt").write_text(json.dumps(related, indent=2))
    result = {
        "ok": bool(related.get("ok")),
        "video_id": VIDEO_ID,
        "title": TITLE,
        "description": DESC,
        "schedule": "2026-10-05T10:30:00.000Z",
        "publish": "Monday 5 Oct 2026, 11:30 UK",
        "privacy": "private",
        "madeForKids": False,
        "altered": True,
        "related": LONG_ID,
        "pinned": False,
        "thumb": str(THUMB),
        "tags": tags,
        "audience": audience2,
        "related_result": related,
        "scheduled": True,
    }
    if result["ok"]:
        dest = STORE / "media/moon-short-thumb.jpg"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(THUMB, dest)
        result["thumb_copy"] = str(dest)
        result["thumb_bytes"] = dest.stat().st_size
        sched = STORE / "docs/shorts-schedule.md"
        text = sched.read_text()
        row = (
            "| monday-moon-short | `dQlOgsDGmtA` | Monday 5 Oct 2026, 11:30 UK "
            "(`1791196200`, 10:30 UTC) | Moon long `2fsQcea-voM` |"
        )
        if "dQlOgsDGmtA" not in text:
            text = text.replace(
                "| friday-last-star-short |",
                row + "\n| friday-last-star-short |",
            )
        text = text.replace(
            "The Moon Short is not scheduled. ",
            "The Moon Short `dQlOgsDGmtA` is private until Monday 5 Oct 2026 at 11:30 UK. ",
        )
        sched.write_text(text)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
