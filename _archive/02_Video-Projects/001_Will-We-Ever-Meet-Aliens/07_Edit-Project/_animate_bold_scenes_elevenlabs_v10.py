#!/usr/bin/env python3
"""Animate remaining bold_rebuild_v05 PNG scenes via ElevenLabs Seedance 1.5 Pro.

Drives the logged-in Chrome CDP session (port 9223) because create requires an
hCaptcha token minted by the Image & Video UI.
"""
from __future__ import annotations

import asyncio
import base64
import json
import re
import time
import urllib.request
from pathlib import Path

import websockets

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
SCENES = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/scenes"
OUT = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/animated"
PROGRESS = ROOT / "07_Edit-Project/bold-explainer-v10-elevenlabs-progress.jsonl"
CDP_BASE = "http://127.0.0.1:9223"
API = "https://api.us.elevenlabs.io"

BOARD_MOTION = {
    1: "slow push into a silent crowded night sky, soft star drift, faint signal-wave shimmer",
    2: "gentle drift along a light-year corridor, tiny probe motion, scale lines breathing",
    3: "ancient light travelling across a galaxy map, cities rising and fading as soft glows",
    4: "quiet expansion-wave ripple across an empty galactic diagram, contemplative stillness",
    5: "exoplanet catalogue filling with soft appearing worlds, transit shadow drifting",
    6: "habitable-zone orbit motion, atmosphere shimmer on temperate and hostile worlds",
    7: "Drake-chain stages lighting in sequence, clock-hand and forming-star motion",
    8: "deep-time ocean chemistry drift, microbial aeons, a tiny late radio-era spark",
    9: "rare-intelligence bottleneck reveal, one world turning to look back",
    10: "great-filter threshold crossing as luminous gate, cautious hopeful light",
    11: "fragile civilisation systems stressing, lights fading with restrained concern",
    12: "noisy city dimming into efficient quiet society, observational invisibility",
    13: "two radio bubbles narrowly missing across time, dark interval between eras",
    14: "distant observer motif, young world protected, future red-star lights switching on",
    15: "four unresolved scientific paths converging with soft doorway light",
    16: "technosignature fingerprints: radio line, laser pulse, atmosphere, waste-heat glow",
    17: "1977 Wow! pulse spike then empty repeats, evidence stamp remaining unconfirmed",
    18: "teaspoon against an ocean of unsearched sky-frequency grid, incomplete listening",
    19: "planet transit and prism spectrum growing molecular fingerprints",
    20: "evidence ladder climbing from ambiguous chemistry to converging telescopes",
    21: "Martian rivers, Europa ice cracks, Enceladus plume sampling, ice-grain microbe hint",
    22: "populated galaxy that still looks dark, reframing the paradox gently",
    23: "modern tools activating: counting worlds, reading atmospheres, listening, analysing ice",
    24: "archive anomaly resolving into a readable pattern, silence becoming data",
}


def board_for(path: Path) -> int:
    name = path.name
    if "board-" in name:
        return int(re.search(r"board-(\d+)", name).group(1))
    num = int(re.search(r"scene-(\d+)", name).group(1))
    return (num - 1) // 4 + 1


def prompt_for(path: Path) -> str:
    motion = BOARD_MOTION[board_for(path)]
    return (
        "Hand-painted editorial science illustration gently comes alive. "
        f"{motion}. "
        "Stable cinematic camera, smooth and locked — no handheld shake. "
        "Preserve exact composition, colours, paper grain, and illustrated style. "
        "Subtle atmospheric drift and light travel only. "
        "No text, letters, numbers, logos, watermarks, humanoid aliens, robots, "
        "mascots, or new objects. Do not morph the artwork into photorealism."
    )


def out_path(source: Path) -> Path:
    return OUT / f"{source.stem}_seedance-mini.mp4"


def is_ready(source: Path) -> bool:
    dest = out_path(source)
    return dest.exists() and dest.stat().st_size > 100_000


def append_progress(record: dict) -> None:
    with PROGRESS.open("a") as handle:
        handle.write(json.dumps(record) + "\n")


def missing_scenes() -> list[Path]:
    return [p for p in sorted(SCENES.glob("scene-*.png")) if not is_ready(p)]


class CdpSession:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.ws = None
        self.n = 0
        self.events: list[dict] = []

    async def __aenter__(self):
        self.ws = await websockets.connect(self.ws_url, max_size=50_000_000)
        await self.call("Runtime.enable")
        await self.call("Page.enable")
        await self.call(
            "Network.enable",
            {
                "maxTotalBufferSize": 100_000_000,
                "maxResourceBufferSize": 50_000_000,
                "maxPostDataSize": 10_000_000,
            },
        )
        await self.call("DOM.enable")
        await self.call("Input.enable")
        return self

    async def __aexit__(self, *exc):
        if self.ws:
            await self.ws.close()

    async def call(self, method: str, params: dict | None = None) -> dict:
        self.n += 1
        sid = self.n
        await self.ws.send(json.dumps({"id": sid, "method": method, "params": params or {}}))
        while True:
            resp = json.loads(await self.ws.recv())
            if "method" in resp:
                self.events.append(resp)
                continue
            if resp.get("id") == sid:
                return resp

    async def evaluate(self, expression: str, await_promise: bool = False):
        r = await self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "awaitPromise": await_promise,
                "returnByValue": True,
            },
        )
        result = r.get("result", {}).get("result", {})
        if result.get("subtype") == "error" or "exceptionDetails" in r.get("result", {}):
            raise RuntimeError(r)
        return result.get("value")

    async def screenshot(self, path: Path) -> None:
        shot = await self.call("Page.captureScreenshot", {"format": "png"})
        path.write_bytes(base64.b64decode(shot["result"]["data"]))

    def drain_create_ids(self) -> list[str]:
        ids = []
        for ev in self.events:
            if ev.get("method") != "Network.requestWillBeSent":
                continue
            req = ev["params"]["request"]
            url = req.get("url", "")
            if req.get("method") == "POST" and url.rstrip("/").endswith("/content/generations") and "/price" not in url and "/check-references" not in url:
                body = req.get("postData") or ""
                # generation id comes from response; keep asset id from body for correlation
                m = re.search(r'"content_asset_id":"([^"]+)"', body)
                ids.append(m.group(1) if m else body[:80])
        return ids

    def pop_status_ids(self) -> list[str]:
        found = []
        for ev in self.events:
            if ev.get("method") != "Network.requestWillBeSent":
                continue
            url = ev["params"]["request"].get("url", "")
            m = re.search(r"/v1/content/generations/([^/]+)/status", url)
            if m:
                found.append(m.group(1))
        return found


async def find_page_ws() -> str:
    tabs = json.load(urllib.request.urlopen(f"{CDP_BASE}/json/list"))
    for tab in tabs:
        if (tab.get("url") or "").startswith("https://elevenlabs.io/app/image-video"):
            return tab["webSocketDebuggerUrl"]
    raise RuntimeError("ElevenLabs Image & Video tab not open on CDP 9223")


async def ensure_composer(cdp: CdpSession) -> None:
    await cdp.evaluate(
        """(() => {
          const b=[...document.querySelectorAll('button')].find(x=>/Accept all cookies/i.test(x.innerText));
          if (b) b.click();
          return true;
        })()"""
    )
    url = await cdp.evaluate("location.href")
    token_ok = await cdp.evaluate(
        """(() => {
          try {
            const auth=JSON.parse(localStorage.getItem('firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]'));
            return !!(auth && auth.stsTokenManager && auth.stsTokenManager.accessToken);
          } catch (e) { return false; }
        })()"""
    )
    if (not token_ok) or "sign-in" in (url or "") or "history" in (url or "") or not await cdp.evaluate(
        r"""(() => !!document.querySelector('button[aria-label="Generate"]') || !!document.querySelector('[contenteditable="true"]'))()"""
    ):
        await cdp.call("Page.navigate", {"url": "https://elevenlabs.io/app/image-video?modality=video"})
        await asyncio.sleep(5)
    has = await cdp.evaluate(
        r"""(() => !!document.querySelector('button[aria-label="Generate"]'))()"""
    )
    if not has:
        await cdp.evaluate(
            """(() => {
              const b=[...document.querySelectorAll('button')].find(x=>/^(Create|New|Generate video)$/i.test((x.innerText||'').trim()));
              if (b) b.click();
              return !!b;
            })()"""
        )
        await asyncio.sleep(1.5)
    token_ok = await cdp.evaluate(
        """(() => {
          try {
            const auth=JSON.parse(localStorage.getItem('firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]'));
            return !!(auth && auth.stsTokenManager && auth.stsTokenManager.accessToken);
          } catch (e) { return false; }
        })()"""
    )
    if not token_ok:
        raise RuntimeError("no firebase token in page")


async def set_prompt(cdp: CdpSession, prompt: str) -> None:
    # Visible prompt is a contenteditable div; hidden textareas hold captcha tokens.
    ok = await cdp.evaluate(
        f"""(() => {{
          const ed=[...document.querySelectorAll('[contenteditable="true"]')]
            .find(el => el.getBoundingClientRect().width > 100);
          if(!ed) return false;
          ed.focus();
          ed.click();
          // Select all existing content then replace.
          const sel=window.getSelection();
          const range=document.createRange();
          range.selectNodeContents(ed);
          sel.removeAllRanges();
          sel.addRange(range);
          document.execCommand('selectAll', false, null);
          document.execCommand('insertText', false, {json.dumps(prompt)});
          ed.dispatchEvent(new InputEvent('input', {{bubbles:true, inputType:'insertText', data:{json.dumps(prompt)}}}));
          return (ed.innerText||'').length;
        }})()"""
    )
    if not ok or (isinstance(ok, int) and ok < 40):
        # Fallback: focus + CDP insertText
        focused = await cdp.evaluate(
            """(() => {
              const ed=[...document.querySelectorAll('[contenteditable="true"]')]
                .find(el => el.getBoundingClientRect().width > 100);
              if(!ed) return false;
              ed.focus(); ed.click();
              const sel=window.getSelection();
              const range=document.createRange();
              range.selectNodeContents(ed);
              sel.removeAllRanges(); sel.addRange(range);
              return true;
            })()"""
        )
        if not focused:
            raise RuntimeError("prompt editor missing")
        await cdp.call(
            "Input.dispatchKeyEvent",
            {"type": "keyDown", "modifiers": 2, "key": "a", "code": "KeyA", "windowsVirtualKeyCode": 65},
        )
        await cdp.call(
            "Input.dispatchKeyEvent",
            {"type": "keyUp", "modifiers": 2, "key": "a", "code": "KeyA", "windowsVirtualKeyCode": 65},
        )
        await cdp.call("Input.insertText", {"text": prompt})
        ok = await cdp.evaluate(
            """(() => {
              const ed=[...document.querySelectorAll('[contenteditable="true"]')]
                .find(el => el.getBoundingClientRect().width > 100);
              return ed ? (ed.innerText||'').length : -1;
            })()"""
        )
    if not ok or (isinstance(ok, int) and ok < 40):
        raise RuntimeError(f"failed to set prompt (len={ok})")


async def set_start_frame(cdp: CdpSession, scene: Path) -> None:
    doc = await cdp.call("DOM.getDocument", {"depth": 1})
    q = await cdp.call(
        "DOM.querySelectorAll",
        {"nodeId": doc["result"]["root"]["nodeId"], "selector": "input[type=file]"},
    )
    nodes = q["result"]["nodeIds"]
    if not nodes:
        raise RuntimeError("no file inputs")
    await cdp.call("DOM.setFileInputFiles", {"nodeId": nodes[0], "files": [str(scene)]})
    # wait for upload / no spinner overlay on start frame if possible
    for _ in range(40):
        left = await cdp.evaluate(
            r"""(() => {
              const m=/(\d+)\s+left/.exec(document.body.innerText||'');
              return m?m[1]:null;
            })()"""
        )
        # Heuristic: asset finalize network or generate enabled
        gen = await cdp.evaluate(
            """(() => {
              const b=document.querySelector('button[aria-label="Generate"]');
              return b ? {disabled: !!b.disabled} : null;
            })()"""
        )
        if gen and not gen.get("disabled"):
            return
        await asyncio.sleep(0.5)
    # continue anyway; Generate may still work


async def ensure_seedance_settings(cdp: CdpSession) -> None:
    # Model should already be Seedance from prior session; reopen if needed.
    model = await cdp.evaluate(
        r"""(() => {
          const b=[...document.querySelectorAll('button')].find(x=>/Seedance|Veo|Kling|Hailuo|Ray/i.test((x.innerText||'').trim()) && (x.innerText||'').trim().length<40);
          return b ? b.innerText.trim() : null;
        })()"""
    )
    if model and "Seedance 1.5 Pro" not in model:
        await cdp.evaluate(
            """(() => {
              const b=[...document.querySelectorAll('button')].find(x=>/Seedance|Veo|Kling|Hailuo|Ray/i.test((x.innerText||'').trim()) && (x.innerText||'').trim().length<40);
              if (b) b.click();
              return !!b;
            })()"""
        )
        await asyncio.sleep(0.8)
        await cdp.evaluate(
            r"""(() => {
              const hit=[...document.querySelectorAll('button,[role="option"],[role="menuitem"],div,span')]
                .find(n => /Seedance 1\.5 Pro/i.test((n.innerText||'').trim()) && (n.innerText||'').trim().length < 40);
              if (hit) hit.click();
              return !!hit;
            })()"""
        )
        await asyncio.sleep(0.5)

    # Duration 4s
    await cdp.evaluate(
        r"""(() => {
          const b=[...document.querySelectorAll('button')].find(x=>/^\d+s$/.test((x.innerText||'').trim()));
          if (b && b.innerText.trim() !== '4s') { b.click(); return 'open'; }
          return b ? b.innerText.trim() : null;
        })()"""
    )
    await asyncio.sleep(0.4)
    await cdp.evaluate(
        """(() => {
          const hit=[...document.querySelectorAll('button,[role="option"],div,span')]
            .find(n => (n.innerText||'').trim() === '4s');
          if (hit) hit.click();
          return !!hit;
        })()"""
    )

    # Audio Off — composer control uses aria-label "Generate audio ON/OFF"
    for _ in range(3):
        audio = await cdp.evaluate(
            """(() => {
              const b = document.querySelector('button[aria-label="Generate audio ON"], button[aria-label="Generate audio OFF"]')
                || [...document.querySelectorAll('button')].find(x => /Generate audio/i.test(x.getAttribute('aria-label')||''));
              if (!b) return {state:'missing'};
              const a = b.getAttribute('aria-label') || '';
              if (/audio OFF/i.test(a)) return {state:'off'};
              b.click();
              return {state:'clicked-on', aria:a};
            })()"""
        )
        if audio and audio.get("state") == "off":
            break
        await asyncio.sleep(0.4)
        await cdp.evaluate(
            """(() => {
              const off = [...document.querySelectorAll('button,[role="option"],[role="menuitem"],div,span')]
                .find(n => {
                  const a = n.getAttribute('aria-label') || '';
                  const t = (n.innerText || '').trim();
                  return /audio OFF/i.test(a) || t === 'Off';
                });
              if (off) off.click();
              return !!off;
            })()"""
        )
        await asyncio.sleep(0.3)


async def click_generate(cdp: CdpSession) -> None:
    # Prefer a real DOM click; fall back to coordinate click near "N left".
    ok = await cdp.evaluate(
        """(() => {
          const b=document.querySelector('button[aria-label="Generate"]');
          if (!b || b.disabled) return false;
          b.click();
          return true;
        })()"""
    )
    if ok:
        return
    info = await cdp.evaluate(
        r"""(() => {
          const b=document.querySelector('button[aria-label="Generate"]');
          if (b) {
            const r=b.getBoundingClientRect();
            return {cx:r.x+r.width/2, cy:r.y+r.height/2, disabled:!!b.disabled};
          }
          const walker=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          let node, hit=null;
          while (node=walker.nextNode()) {
            if (/\d+\s+left/.test(node.textContent||'')) { hit=node; break; }
          }
          if (!hit) return null;
          const tr=hit.parentElement.getBoundingClientRect();
          const near=[...document.querySelectorAll('button')].map(btn=>{
            const r=btn.getBoundingClientRect();
            return {aria:btn.getAttribute('aria-label'), disabled:btn.disabled, cx:r.x+r.width/2, cy:r.y+r.height/2, x:r.x};
          }).filter(b => b.aria==='Generate' && !b.disabled && Math.abs(b.cy-(tr.y+tr.height/2))<50 && b.x>=tr.x-10);
          return near[0] || null;
        })()"""
    )
    if not info or info.get("disabled"):
        raise RuntimeError("generate button not found or disabled")
    x, y = info["cx"], info["cy"]
    for typ in ("mousePressed", "mouseReleased"):
        await cdp.call(
            "Input.dispatchMouseEvent",
            {"type": typ, "x": x, "y": y, "button": "left", "clickCount": 1},
        )


KNOWN_GENERATION_IDS: set[str] = set()


def load_known_ids() -> None:
    if not PROGRESS.exists():
        return
    for line in PROGRESS.read_text().splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        gid = rec.get("generation_id")
        if gid:
            KNOWN_GENERATION_IDS.add(gid)


async def page_token(cdp: CdpSession) -> str:
    token = await cdp.evaluate(
        """(() => {
          const auth=JSON.parse(localStorage.getItem('firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]'));
          return auth && auth.stsTokenManager && auth.stsTokenManager.accessToken;
        })()"""
    )
    if not token:
        raise RuntimeError("no firebase token in page")
    open("/tmp/elevenlabs_bearer.txt", "w").write(token)
    return token


def api_get_json(path: str, token: str) -> tuple[int, dict | list | str]:
    req = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Origin": "https://elevenlabs.io",
            "Referer": "https://elevenlabs.io/",
            "User-Agent": "Mozilla/5.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            body = json.loads(raw)
        except Exception:
            body = raw.decode("utf-8", "replace")
        return exc.code, body


async def list_generations(cdp: CdpSession, per_page: int = 20) -> list[dict]:
    token = await page_token(cdp)
    code, listing = api_get_json(f"/v1/content/generations?per_page={per_page}", token)
    if code != 200 or not isinstance(listing, dict):
        return []
    return listing.get("generations") or listing.get("items") or []


async def seed_known_ids_from_api(cdp: CdpSession) -> None:
    for item in await list_generations(cdp, per_page=50):
        gid = item.get("id")
        if gid:
            KNOWN_GENERATION_IDS.add(gid)


async def wait_for_generation_id(
    cdp: CdpSession,
    *,
    prompt: str,
    timeout: float = 120,
) -> str:
    """Wait for a NEW list entry whose prompt matches; never reuse prior ids."""
    start = time.time()
    needle = prompt[:100]
    while time.time() - start < timeout:
        await asyncio.sleep(1.0)
        for item in await list_generations(cdp, per_page=15):
            gid = item.get("id")
            if not gid or gid in KNOWN_GENERATION_IDS:
                continue
            if needle and needle not in (item.get("prompt") or ""):
                continue
            KNOWN_GENERATION_IDS.add(gid)
            return gid
    raise TimeoutError("no generation id observed")


async def wait_and_download(cdp: CdpSession, generation_id: str, dest: Path, timeout: float = 420) -> dict:
    start = time.time()
    http_fails = 0
    while time.time() - start < timeout:
        token = await page_token(cdp)
        code, meta = api_get_json(f"/v1/content/generations/{generation_id}", token)
        if code != 200 or not isinstance(meta, dict):
            http_fails += 1
            print(f"  status {generation_id}: http {code} ({http_fails})", flush=True)
            # Fallback via list
            for item in await list_generations(cdp, per_page=20):
                if item.get("id") == generation_id:
                    meta = item
                    code = 200
                    break
            if code != 200 or not isinstance(meta, dict):
                if http_fails >= 25:
                    raise RuntimeError(f"persistent http {code} for {generation_id}: {meta}")
                await asyncio.sleep(4)
                continue
        http_fails = 0
        status = meta.get("status")
        print(f"  status {generation_id}: {status}", flush=True)
        if status == "completed":
            url = meta.get("download_url") or meta.get("content_url")
            if not url:
                raise RuntimeError(f"completed but no url: {list(meta.keys())}")
            tmp = dest.with_suffix(".partial.mp4")
            urllib.request.urlretrieve(url, tmp)
            tmp.replace(dest)
            return meta
        if status in {"failed", "error", "rejected", "cancelled"}:
            raise RuntimeError(f"generation failed: {meta}")
        await asyncio.sleep(4)
    raise TimeoutError(f"generation {generation_id} timed out")


async def animate_one(cdp: CdpSession, scene: Path) -> dict:
    dest = out_path(scene)
    if is_ready(scene):
        return {"scene": scene.name, "status": "skipped", "output": str(dest)}

    print(f"START {scene.name}", flush=True)
    prompt = prompt_for(scene)
    cdp.events.clear()
    print("  composer", flush=True)
    await ensure_composer(cdp)
    print("  settings", flush=True)
    await ensure_seedance_settings(cdp)
    print("  frame", flush=True)
    await set_start_frame(cdp, scene)
    print("  prompt", flush=True)
    await set_prompt(cdp, prompt)
    await asyncio.sleep(1.0)
    print("  generate", flush=True)
    await click_generate(cdp)
    print("  wait id", flush=True)
    gid = await wait_for_generation_id(cdp, prompt=prompt)
    print(f"  generation {gid}", flush=True)
    meta = await wait_and_download(cdp, gid, dest)
    record = {
        "scene": scene.name,
        "status": "generated",
        "generation_id": gid,
        "output": str(dest),
        "bytes": dest.stat().st_size,
        "duration_secs": (meta.get("file_properties") or {}).get("duration_secs"),
        "prompt_board": board_for(scene),
    }
    append_progress(record)
    print(f"DONE {scene.name} -> {dest.name} ({dest.stat().st_size} bytes)", flush=True)
    return record


async def connect_cdp() -> CdpSession:
    ws_url = await find_page_ws()
    cdp = CdpSession(ws_url)
    await cdp.__aenter__()
    return cdp


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    load_known_ids()
    todo = missing_scenes()
    print(f"Missing scenes: {len(todo)}/96", flush=True)
    print(f"Known generation ids: {len(KNOWN_GENERATION_IDS)}", flush=True)
    if not todo:
        print("Nothing to do", flush=True)
        return

    cdp = await connect_cdp()
    try:
        await ensure_composer(cdp)
        await seed_known_ids_from_api(cdp)
        print(f"Known after API seed: {len(KNOWN_GENERATION_IDS)}", flush=True)
        for i, scene in enumerate(todo, 1):
            print(f"\n=== [{i}/{len(todo)}] ===", flush=True)
            try:
                await animate_one(cdp, scene)
            except Exception as exc:
                record = {"scene": scene.name, "status": "error", "error": str(exc)}
                append_progress(record)
                print(f"ERROR {scene.name}: {exc}", flush=True)
                try:
                    await cdp.screenshot(Path(f"/tmp/el_err_{scene.stem}.png"))
                except Exception:
                    pass
                # Reconnect CDP if the socket died
                try:
                    await cdp.evaluate("1")
                except Exception:
                    print("Reconnecting CDP...", flush=True)
                    try:
                        await cdp.__aexit__(None, None, None)
                    except Exception:
                        pass
                    await asyncio.sleep(2)
                    cdp = await connect_cdp()
                    await ensure_composer(cdp)
                    await seed_known_ids_from_api(cdp)
                await asyncio.sleep(3)
            await asyncio.sleep(2)
    finally:
        try:
            await cdp.__aexit__(None, None, None)
        except Exception:
            pass
    remaining = missing_scenes()
    print(f"\nFinished pass. Still missing: {len(remaining)}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
