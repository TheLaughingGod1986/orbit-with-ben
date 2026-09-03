#!/usr/bin/env python3
"""
Set YouTube Studio "Altered or synthetic content" (Made with AI) on Orbit videos
via Chrome CDP (raw websocket — Playwright crashes this Chrome profile).

Usage:
  python3 _set_youtube_synthetic_ai_label_cdp.py
  python3 _set_youtube_synthetic_ai_label_cdp.py --ids DN4L1DkerMM,ziKBPJ6FY0U
  python3 _set_youtube_synthetic_ai_label_cdp.py --dry-run
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import time
import urllib.request
from pathlib import Path

import websocket

PORT = 9335
PROFILE = Path.home() / ".orbit-chrome-takeover"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
OUT = Path(__file__).resolve().parent / "ai_synthetic_disclosure_2026-08-26"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def http_json(url: str):
    with urllib.request.urlopen(url, timeout=5) as r:
        return json.load(r)


def cdp_up() -> bool:
    try:
        http_json(f"http://127.0.0.1:{PORT}/json/version")
        return True
    except Exception:
        return False


def launch_chrome() -> subprocess.Popen | None:
    if cdp_up():
        return None
    for p in (PROFILE / "SingletonLock", PROFILE / "SingletonSocket", PROFILE / "SingletonCookie"):
        try:
            p.unlink()
        except FileNotFoundError:
            pass
    PROFILE.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        [
            CHROME,
            f"--remote-debugging-port={PORT}",
            "--remote-allow-origins=*",
            f"--user-data-dir={PROFILE}",
            "--no-first-run",
            "--no-default-browser-check",
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        ],
        stdout=open("/tmp/orbit-studio-ai-label.log", "w"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(40):
        if cdp_up():
            return proc
        time.sleep(0.25)
    raise RuntimeError("Chrome CDP failed to start")


class CDP:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=60)
        self.i = 0

    def call(self, method: str, params: dict | None = None, timeout: float = 90):
        self.i += 1
        mid = self.i
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
        raise TimeoutError(method)

    def eval(self, expression: str, timeout: float = 90):
        res = self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True,
            },
            timeout=timeout,
        )
        if res.get("exceptionDetails"):
            raise RuntimeError(str(res["exceptionDetails"])[:400])
        return res.get("result", {}).get("value")

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def pick_page_ws() -> str:
    tabs = http_json(f"http://127.0.0.1:{PORT}/json/list")
    pages = [t for t in tabs if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
    if not pages:
        raise RuntimeError("No CDP page targets")
    # Prefer Studio page
    for t in pages:
        if "studio.youtube.com" in (t.get("url") or ""):
            return t["webSocketDebuggerUrl"]
    return pages[0]["webSocketDebuggerUrl"]


def load_ids(explicit: list[str] | None) -> list[str]:
    if explicit:
        return [i for i in explicit if re.fullmatch(r"[\w-]{11}", i)]
    path = Path("/tmp/orbit_yt_ids.txt")
    if path.exists():
        return [ln.strip() for ln in path.read_text().splitlines() if re.fullmatch(r"[\w-]{11}", ln.strip())]
    raise SystemExit("No ids — pass --ids or create /tmp/orbit_yt_ids.txt")


SET_JS = r"""
async (wantYes) => {
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));

  // Expand Age restriction / advanced section that hides AI use
  for (const el of document.querySelectorAll('button, ytcp-button, tp-yt-paper-button, a, yt-formatted-string')) {
    const t = ((el.innerText || el.textContent || '')).trim().replace(/\s+/g, ' ');
    if (/^Show more$/i.test(t)) {
      try { el.click(); } catch (e) {}
    }
  }
  await sleep(1000);
  for (let i = 0; i < 30; i++) window.scrollBy(0, 500);
  await sleep(500);

  // Prefer dedicated altered-content select component
  let radios = [...document.querySelectorAll(
    'ytkp-altered-content-select tp-yt-paper-radio-button, tp-yt-paper-radio-button.style-scope.ytkp-altered-content-select'
  )];
  if (!radios.length) {
    // fallback: radios whose exact label is Yes/No near AI use copy
    radios = [...document.querySelectorAll('tp-yt-paper-radio-button[role=radio]')].filter(el => {
      const t = (el.innerText || '').trim();
      if (!/^(Yes|No)$/i.test(t)) return false;
      const ctx = (el.closest('ytkp-altered-content-select, ytcp-form-section, div') || el.parentElement);
      return /Was AI used|AI use|Selecting 'yes' adds a disclosure|altered-content/i.test(
        ((ctx && ctx.innerText) || '') + ' ' + (el.className || '')
      );
    });
  }

  const yes = radios.find(el => /^Yes$/i.test((el.innerText || '').trim()));
  const no = radios.find(el => /^No$/i.test((el.innerText || '').trim()));
  if (!yes) {
    return {
      ok: false,
      reason: 'ai_yes_not_found',
      radioCount: radios.length,
      hasComponent: !!document.querySelector('ytkp-altered-content-select'),
      hasAiUse: /AI use|Was AI used/i.test(document.body.innerText || ''),
    };
  }

  const selected = (el) => {
    if (!el) return false;
    if (el.getAttribute('aria-checked') === 'true') return true;
    if (el.getAttribute('aria-checked') === 'false') return false;
    return /iron-selected/.test(el.className || '');
  };

  const beforeYes = selected(yes);
  if (wantYes && !beforeYes) {
    yes.click();
    await sleep(700);
  }
  const afterYes = selected(yes);

  let saved = false;
  let saveDisabled = true;
  for (const el of document.querySelectorAll('ytcp-button, button, tp-yt-paper-button')) {
    const t = (el.innerText || el.getAttribute('aria-label') || '').trim();
    if (!/^Save$/i.test(t)) continue;
    saveDisabled = el.getAttribute('aria-disabled') === 'true' || el.hasAttribute('disabled');
    if (!saveDisabled) {
      el.click();
      saved = true;
      await sleep(2200);
    }
    break;
  }

  return {
    ok: wantYes ? afterYes === true : true,
    beforeYes,
    afterYes,
    noSelected: selected(no),
    saved,
    saveDisabled,
    alreadySet: beforeYes && afterYes,
    reason: (wantYes && !afterYes) ? 'yes_not_selected' : 'ok',
  };
}
"""


def process_video(cdp: CDP, video_id: str, *, dry_run: bool) -> dict:
    url = f"https://studio.youtube.com/video/{video_id}/edit"
    cdp.call("Page.navigate", {"url": url})
    # wait for edit UI
    for _ in range(50):
        time.sleep(0.4)
        ready = cdp.eval(
            "!!document.body && (/Video details|Title \\(required\\)|Audience/i.test(document.body.innerText||''))"
        )
        if ready:
            break
    time.sleep(1.0)

    # Force-expand advanced section a few times until AI use appears
    for _ in range(5):
        cdp.eval(
            """(() => {
              for (const el of document.querySelectorAll('button, ytcp-button, tp-yt-paper-button, yt-formatted-string, a')) {
                const t = ((el.innerText || el.textContent || '')).trim();
                if (/^Show more$/i.test(t)) { try { el.click(); } catch (e) {} }
              }
              for (let i=0;i<20;i++) window.scrollBy(0, 500);
              return /AI use|Was AI used|ytkp-altered-content/i.test(document.body.innerText||'')
                || !!document.querySelector('ytkp-altered-content-select');
            })()"""
        )
        time.sleep(0.8)
        has = cdp.eval(
            "!!document.querySelector('ytkp-altered-content-select') || /Was AI used to generate or edit your content/i.test(document.body.innerText||'')"
        )
        if has:
            break

    if dry_run:
        info = cdp.eval(
            """(() => {
              const t=document.body.innerText||'';
              return {
                hasAltered:/altered/i.test(t),
                hasAiUse:/AI use|Was AI used/i.test(t),
                title:(document.title||'')
              };
            })()"""
        )
        return {"id": video_id, "action": "dry_run", **(info or {})}

    result = cdp.eval(f"({SET_JS})(true)")
    if not result or not result.get("ok"):
        try:
            shot = cdp.call("Page.captureScreenshot", {"format": "png"})
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / f"fail_{video_id}.png").write_bytes(base64.b64decode(shot["data"]))
        except Exception:
            pass
    return {"id": video_id, "action": "set", **(result or {"ok": False, "reason": "no_result"})}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    explicit = [s.strip() for s in args.ids.split(",") if s.strip()] or None
    ids = load_ids(explicit)
    if args.limit:
        ids = ids[: args.limit]

    print(f"videos={len(ids)} dry_run={args.dry_run}")
    proc = launch_chrome()
    time.sleep(2)
    ws = pick_page_ws()
    cdp = CDP(ws)
    cdp.call("Page.enable")
    cdp.call("Runtime.enable")

    results = []
    for i, vid in enumerate(ids, 1):
        print(f"[{i}/{len(ids)}] {vid}", flush=True)
        try:
            row = process_video(cdp, vid, dry_run=args.dry_run)
            print(" ", row, flush=True)
            results.append(row)
        except Exception as e:
            print("  ERROR", e, flush=True)
            results.append({"id": vid, "ok": False, "reason": str(e)[:300]})
            # reconnect if chrome died
            if not cdp_up():
                print("Chrome died — relaunching", flush=True)
                proc = launch_chrome()
                time.sleep(2)
                cdp = CDP(pick_page_ws())
                cdp.call("Page.enable")
                cdp.call("Runtime.enable")

    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / ("DRY_RUN.json" if args.dry_run else "RESULT.json")
    ok_n = sum(1 for r in results if r.get("ok") or r.get("action") == "dry_run")
    report = {
        "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "dry_run": args.dry_run,
        "total": len(ids),
        "ok": ok_n,
        "results": results,
    }
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {out} ok={ok_n}/{len(ids)}")
    cdp.close()
    return 0 if ok_n == len(ids) else 1


if __name__ == "__main__":
    raise SystemExit(main())
