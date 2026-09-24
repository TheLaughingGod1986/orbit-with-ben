#!/usr/bin/env python3
"""Schedule the Moon Short from its Studio edit tab.

The upload dialog tab is frozen. This uses the healthy edit tab for
dQlOgsDGmtA only, through the browser CDP socket, and does not attach to
frozen videos.
"""
from __future__ import annotations

import base64
import json
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
EDIT = f"https://studio.youtube.com/video/{VIDEO_ID}/edit"
OUT = ROOT / "upload/monday_moon_short_upload_result.json"
AUDIT = ROOT / "upload/_studio_audit"
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
    def __init__(self) -> None:
        ver = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=5))
        self.ws = websocket.create_connection(
            ver["webSocketDebuggerUrl"], timeout=20, suppress_origin=True, max_size=40_000_000
        )
        self.n = 0
        self.sid = ""

    def call(self, method: str, params: dict | None = None, timeout: float = 20, session: bool = False) -> dict:
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
            {"expression": expression, "returnByValue": True, "awaitPromise": True},
            timeout=timeout,
            session=True,
        )
        details = result.get("exceptionDetails")
        if details:
            raise RuntimeError(json.dumps(details)[:600])
        return (result.get("result") or {}).get("value")

    def shot(self, name: str) -> None:
        data = self.call("Page.captureScreenshot", {"format": "png"}, timeout=20, session=True)
        (AUDIT / name).write_bytes(base64.b64decode(data["data"]))


def edit_target(cdp: CDP) -> str:
    infos = cdp.call("Target.getTargets").get("targetInfos") or []
    for info in infos:
        url = info.get("url") or ""
        if VIDEO_ID in url and "/edit" in url and info.get("type") == "page":
            if any(frozen in url for frozen in FROZEN):
                continue
            return info["targetId"]
    created = cdp.call("Target.createTarget", {"url": EDIT, "background": True})
    return created["targetId"]


JS_AI_YES = r"""
(() => {
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('*')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  const radios = [];
  visit(document, (el) => {
    const role = el.getAttribute && el.getAttribute('role');
    const tag = (el.tagName || '').toLowerCase();
    if (role === 'radio' || tag === 'tp-yt-paper-radio-button') radios.push(el);
  });
  for (const el of radios) {
    const own = ((el.innerText || el.getAttribute('aria-label') || '')).trim();
    if (own !== 'Yes') continue;
    let blob = own;
    let node = el;
    for (let i = 0; i < 10 && node; i++) {
      blob += ' ' + (node.innerText || '').slice(0, 400);
      node = node.parentElement || (node.getRootNode && node.getRootNode().host);
    }
    if (/AI use|realistic-looking|altered|synthetic/i.test(blob)) {
      if (el.getAttribute('aria-checked') !== 'true') el.click();
      return {clicked: true, checked: el.getAttribute('aria-checked')};
    }
  }
  return {clicked: false};
})()
"""

JS_PAID_NO = r"""
(() => {
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('*')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  let hit = '';
  visit(document, (el) => {
    const own = ((el.innerText || '')).trim();
    if (/^No, my video doesn't include paid promotion/.test(own)) {
      if (el.getAttribute('aria-checked') !== 'true') el.click();
      hit = el.getAttribute('aria-checked') || 'clicked';
    }
  });
  return hit || 'missing';
})()
"""

JS_CLICK_EXACT = r"""
(label) => {
  const visit = (node, fn) => {
    if (!node || !node.querySelectorAll) return;
    for (const el of node.querySelectorAll('button, ytcp-button, tp-yt-paper-button, a')) {
      fn(el);
      if (el.shadowRoot) visit(el.shadowRoot, fn);
    }
  };
  let best = null;
  visit(document, (el) => {
    const t = (el.innerText || el.getAttribute('aria-label') || '').trim();
    if (t !== label) return;
    const r = el.getBoundingClientRect();
    if (r.width < 20 || r.height < 10) return;
    best = el;
  });
  if (!best) return 'missing';
  best.click();
  return 'clicked';
}
"""


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    cdp = CDP()
    tid = edit_target(cdp)
    attached = cdp.call("Target.attachToTarget", {"targetId": tid, "flatten": True})
    cdp.sid = attached["sessionId"]
    try:
        href = cdp.js("location.href") or ""
        if VIDEO_ID not in href or any(frozen in href for frozen in FROZEN):
            raise SystemExit(f"wrong tab: {href}")
        for _ in range(20):
            body = cdp.js("(document.body && document.body.innerText || '').slice(0,400)") or ""
            if "Why the Moon Is Leaving Us" in body:
                break
            time.sleep(0.5)
        ai = cdp.js(JS_AI_YES)
        time.sleep(0.4)
        ai2 = cdp.js(JS_AI_YES)
        paid = cdp.js(JS_PAID_NO)
        cdp.call("DOM.enable", session=True)
        doc = cdp.call("DOM.getDocument", {"depth": -1, "pierce": True}, session=True)
        found = cdp.call(
            "DOM.querySelector",
            {"nodeId": doc["root"]["nodeId"], "selector": 'input[type="file"][accept*="image"]'},
            session=True,
        )
        node_id = found.get("nodeId") or 0
        if not node_id:
            raise SystemExit("thumbnail input missing")
        cdp.call(
            "DOM.setFileInputFiles",
            {"nodeId": node_id, "files": [str(THUMB)]},
            session=True,
        )
        time.sleep(2)
        cdp.shot("07_edit_details.png")
        if not (ai2 or {}).get("clicked"):
            result = {"ok": False, "error": "AI disclosure Yes not found", "ai": ai2, "paid": paid}
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2))
            return
        saved = cdp.js(f"({JS_CLICK_EXACT})('Save')")
        time.sleep(2.5)
        draft = cdp.js(f"({JS_CLICK_EXACT})('Edit draft')")
        time.sleep(2)
        dialog = cdp.js(
            """(() => {
              const dlg = document.querySelector('ytcp-uploads-dialog');
              return dlg ? (dlg.innerText || '').slice(0, 2500) : '';
            })()"""
        ) or ""
        (AUDIT / "08_draft_dialog.txt").write_text(dialog or cdp.js("(document.body.innerText||'').slice(0,2000)"))
        cdp.shot("08_draft.png")
        result = {
            "ok": False,
            "video_id": VIDEO_ID,
            "ai": ai2,
            "paid": paid,
            "saved": saved,
            "draft": draft,
            "dialog_has_schedule": "Schedule" in dialog,
            "href": cdp.js("location.href"),
        }
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
