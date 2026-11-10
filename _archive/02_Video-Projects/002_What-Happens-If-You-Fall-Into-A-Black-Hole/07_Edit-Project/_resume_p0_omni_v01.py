#!/usr/bin/env python3
"""Resume Video 002 CG clips — Gemini Omni Flash + Orbit via Chrome CDP :9223.

Runs 01 C Omni regen + full P1 queue. Skips any beat already saved (>800KB).
"""
from __future__ import annotations

import asyncio
import json
import re
import time
import urllib.request
from pathlib import Path

import websockets

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
RAW = ROOT / "04_Generated-Clips/01_Raw"
LOG = ROOT / "03_Animation-Prompts/03_Generation-Logs/blackhole_p0_progress.jsonl"
QUEUE = ROOT / "03_Animation-Prompts/03_Generation-Logs/blackhole_generation_queue_v01.md"
API = "https://api.us.elevenlabs.io"
CDP = "http://127.0.0.1:9223"
LOCK = (
    "Preserve Orbit exactly: rounded orange body, black faceplate, cream expressive eyes, "
    "single glowing antenna, short stubby side arms (no claws, no fingers), soft underside glow. "
    "No text, logos, watermarks. "
    "Audio: prefer ambient space only. If Orbit vocalises or speaks at all, use a warm British English "
    "accent (never American)."
)

# Speaking / camera-facing Orbit — British accent regen
BEATS = [
    ("01", "C", "determined", f"Orbit faces camera, determined little hover forward. Cream eyes resolve. Soft brand-friendly framing; black hole a tiny dark coin with faint ring far behind. Premium cinematic 3D. If any speech or vocalisation, warm British English accent only — never American. {LOCK}"),
]

P0_KEYS = {("01", "C")}  # still P0 priority naming


def out_path(scene: str, beat: str, slug: str) -> Path:
    prefix = "p0" if (scene, beat) in P0_KEYS else "p1"
    return RAW / f"scene-{scene}" / f"{prefix}_{beat}_{slug}_gemini-omni-flash_v01_raw.mp4"


def done(path: Path) -> bool:
    # Tiny Omni fails / truncated downloads are usually < ~0.8MB for these 8s clips
    return path.exists() and path.stat().st_size > 800_000


def api_get(path: str, tok: str):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def wait_done(gid: str, tok: str, timeout: int = 480) -> dict:
    t0 = time.time()
    while time.time() - t0 < timeout:
        g = api_get(f"/v1/content/generations/{gid}", tok)
        st = g.get("status")
        print(f"  {gid} {st}", flush=True)
        if st == "completed":
            return g
        if st in ("failed", "error"):
            raise RuntimeError(g.get("error_message"))
        time.sleep(5)
    raise TimeoutError(gid)


def save(g: dict, scene: str, beat: str, slug: str) -> Path:
    dest = out_path(scene, beat, slug)
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = g.get("download_url") or g.get("content_url")
    urllib.request.urlretrieve(url, dest)
    with LOG.open("a") as f:
        f.write(
            json.dumps(
                {
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "scene": scene,
                    "beat": beat,
                    "slug": slug,
                    "generation_id": g["id"],
                    "model_id": g.get("model_id"),
                    "file": str(dest),
                    "bytes": dest.stat().st_size,
                }
            )
            + "\n"
        )
    text = QUEUE.read_text()
    # Queue uses zero-padded scene ids (Scene 08); keep padding when marking done
    scene_label = scene if len(scene) >= 2 else f"{int(scene):02d}"
    text2, n = re.compile(rf"- \[ \] Scene {scene_label} · {beat} ·").subn(
        f"- [x] Scene {scene_label} · {beat} ·", text, count=1
    )
    if n:
        QUEUE.write_text(text2)
    print(f"SAVED {dest.name} model={g.get('model_id')} bytes={dest.stat().st_size}", flush=True)
    return dest


def find_ws() -> str:
    tabs = json.load(urllib.request.urlopen(f"{CDP}/json/list"))
    for t in tabs:
        if (t.get("url") or "").startswith("https://elevenlabs.io/app/image-video"):
            return t["webSocketDebuggerUrl"]
    raise RuntimeError("No ElevenLabs Image & Video tab on CDP 9223")


async def main():
    state = {"ws": None, "n": 0, "tok": ""}

    async def connect():
        if state["ws"] is not None:
            try:
                await state["ws"].close()
            except Exception:
                pass
        url = find_ws()
        state["ws"] = await websockets.connect(url, max_size=50_000_000)
        state["n"] = 0
        await _call_raw("Runtime.enable")
        await _call_raw("Page.enable")
        print(f"CDP connected …{url.split('/')[-1][:8]}", flush=True)

    async def _call_raw(method, params=None):
        state["n"] += 1
        n = state["n"]
        ws = state["ws"]
        await ws.send(json.dumps({"id": n, "method": method, "params": params or {}}))
        while True:
            resp = json.loads(await ws.recv())
            if "method" in resp:
                continue
            if resp.get("id") == n:
                return resp

    async def call(method, params=None):
        last_err = None
        for _ in range(3):
            try:
                return await _call_raw(method, params)
            except Exception as e:
                last_err = e
                print(f"  CDP reconnect after {type(e).__name__}", flush=True)
                await asyncio.sleep(1.0)
                await connect()
        raise last_err

    async def ev(expr):
        r = await call(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True, "awaitPromise": False},
        )
        return r.get("result", {}).get("result", {}).get("value")

    async def click_xy(x: float, y: float):
        await call(
            "Input.dispatchMouseEvent",
            {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1},
        )
        await call(
            "Input.dispatchMouseEvent",
            {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1},
        )

    async def press_escape():
        await call(
            "Input.dispatchKeyEvent",
            {"type": "keyDown", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27},
        )
        await call(
            "Input.dispatchKeyEvent",
            {"type": "keyUp", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27},
        )

    await connect()
    await call("Page.navigate", {"url": "https://elevenlabs.io/app/image-video?modality=video"})
    await asyncio.sleep(4)
    await ev(
        """(() => {
          const b=[...document.querySelectorAll('button')].find(x=>/Get started|Remind Me Later|Accept all cookies/i.test((x.innerText||'').trim()));
          if (b) b.click();
          [...document.querySelectorAll('button')].filter(x=>/close/i.test(x.getAttribute('aria-label')||'')).forEach(x=>x.click());
          return true;
        })()"""
    )
    await asyncio.sleep(0.8)

    async def refresh_tok():
        """Pull Firebase access token; force securetoken refresh if expired/near-expiry."""
        try:
            r = await call(
                "Runtime.evaluate",
                {
                    "expression": """(async () => {
                  const key='firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]';
                  const auth=JSON.parse(localStorage.getItem(key)||'null');
                  if (!auth || !auth.stsTokenManager) return null;
                  const st=auth.stsTokenManager;
                  const need = !st.expirationTime || Date.now() > (st.expirationTime - 120000);
                  if (need && st.refreshToken) {
                    const body=new URLSearchParams({grant_type:'refresh_token', refresh_token: st.refreshToken});
                    const resp=await fetch('https://securetoken.googleapis.com/v1/token?key=AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys', {
                      method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body
                    });
                    const data=await resp.json();
                    if (data.access_token) {
                      st.accessToken=data.access_token;
                      st.expirationTime=Date.now()+(Number(data.expires_in||3600)*1000);
                      if (data.refresh_token) st.refreshToken=data.refresh_token;
                      auth.stsTokenManager=st;
                      localStorage.setItem(key, JSON.stringify(auth));
                    }
                  }
                  return st.accessToken || null;
                })()""",
                    "awaitPromise": True,
                    "returnByValue": True,
                },
            )
            tok = r.get("result", {}).get("result", {}).get("value")
        except Exception as e:
            print(f"  token refresh warn: {e}", flush=True)
            tok = None
        if not tok:
            p = Path("/tmp/elevenlabs_bearer.txt")
            if p.exists():
                tok = p.read_text().strip()
        if not tok:
            raise RuntimeError("signed out")
        Path("/tmp/elevenlabs_bearer.txt").write_text(tok + "\n")
        state["tok"] = tok
        return tok

    async def dismiss_noise():
        try:
            await ev(
                """(() => {
                  [...document.querySelectorAll('button')].filter(x=>/Remind Me Later|Accept all cookies|Get started|Maybe later|Not now/i.test((x.innerText||'').trim())).forEach(b=>b.click());
                  [...document.querySelectorAll('button')].filter(x=>/close/i.test(x.getAttribute('aria-label')||'')).forEach(x=>x.click());
                  if (/Select one of Orbit|Use Style|Headshot/i.test(document.body.innerText||'')) {
                    const hs=[...document.querySelectorAll('button,div,[role="option"]')].find(n=>{
                      const t=(n.innerText||'').trim();
                      return /^Headshot$/i.test(t) || t.startsWith('Headshot');
                    });
                    if (hs) hs.click();
                  }
                })()"""
            )
        except Exception as e:
            print(f"  dismiss_noise skip: {type(e).__name__}", flush=True)

    async def read_model_chip() -> str:
        return (
            await ev(
                """(() => {
                  const gens=[...document.querySelectorAll('button[aria-label="Generate"]')].filter(g=>{
                    const r=g.getBoundingClientRect();
                    return r.width>10 && r.height>10 && r.y>100;
                  });
                  if (!gens.length) return '';
                  gens.sort((a,b)=>b.getBoundingClientRect().y - a.getBoundingClientRect().y);
                  const gr=gens[0].getBoundingClientRect();
                  const chips=[...document.querySelectorAll('button')].map(x=>{
                    const t=(x.innerText||'').trim().split('\\n')[0];
                    const r=x.getBoundingClientRect();
                    return {
                      t,
                      dy: Math.abs((r.y+r.height/2)-(gr.y+gr.height/2)),
                      leftOf: r.x < gr.x,
                      vis: r.width>10 && r.height>10
                    };
                  }).filter(o => o.vis && o.t && o.t.length < 40
                    && /(Veo|Seedance|Sora|Gemini|Mochi|Kling|Omni|Aurora|Creatify)/i.test(o.t)
                    && o.leftOf && o.dy < 90)
                    .sort((a,b)=>a.dy-b.dy);
                  return chips[0] ? chips[0].t : '';
                })()"""
            )
            or ""
        )

    async def ensure_create_surface():
        href = (await ev("location.href")) or ""
        if "history" in href or "creationType=voiceRemix" in href:
            await call("Page.navigate", {"url": "https://elevenlabs.io/app/image-video?modality=video"})
            await asyncio.sleep(3.5)
            await dismiss_noise()

    async def click_video_modality():
        rect = await ev(
            """(() => {
              const n=[...document.querySelectorAll('button,[role="tab"]')].find(el=>{
                const t=(el.innerText||'').trim();
                const p=(el.parentElement&&el.parentElement.innerText)||'';
                return t==='Video' && /Image/.test(p) && /Lip sync/.test(p);
              });
              if (!n) return null;
              const r=n.getBoundingClientRect();
              return {x:r.x+r.width/2, y:r.y+r.height/2};
            })()"""
        )
        if rect:
            await click_xy(rect["x"], rect["y"])
            await asyncio.sleep(0.9)

    orbit_selected = {"ok": False}

    async def ensure_video_orbit(reselect_orbit: bool = False):
        await ensure_create_surface()
        if reselect_orbit or not orbit_selected["ok"]:
            await ev(
                """(() => {
                  const orbit=[...document.querySelectorAll('button,div,span')].find(n=>(n.innerText||'').trim()==='Orbit');
                  if (orbit) orbit.click();
                })()"""
            )
            await asyncio.sleep(0.6)
            await dismiss_noise()
            await asyncio.sleep(0.3)
            orbit_selected["ok"] = True
        await click_video_modality()
        chip = await read_model_chip()
        href = await ev("location.href") or ""
        if "lipsync" in href or "Aurora" in chip or "Creatify" in chip:
            await click_video_modality()
            await asyncio.sleep(0.4)

    async def open_composer_chip_and_click():
        return await ev(
            """(() => {
              const gens=[...document.querySelectorAll('button[aria-label="Generate"]')].filter(g=>{
                const r=g.getBoundingClientRect();
                return r.width>10 && r.height>10 && r.y>100;
              });
              if (!gens.length) return null;
              gens.sort((a,b)=>b.getBoundingClientRect().y - a.getBoundingClientRect().y);
              const gr=gens[0].getBoundingClientRect();
              const chip=[...document.querySelectorAll('button')].filter(x=>{
                const t=(x.innerText||'').trim().split('\\n')[0];
                const r=x.getBoundingClientRect();
                return t && t.length<40
                  && /(Veo|Seedance|Sora|Gemini|Mochi|Kling|Omni|Aurora|Creatify)/i.test(t)
                  && r.x < gr.x
                  && Math.abs((r.y+r.height/2)-(gr.y+gr.height/2)) < 90
                  && r.width>10 && r.height>10;
              }).sort((a,b)=>Math.abs(a.getBoundingClientRect().y-gr.y)-Math.abs(b.getBoundingClientRect().y-gr.y))[0];
              if (!chip) return null;
              chip.click();
              return chip.innerText.trim().split('\\n')[0];
            })()"""
        )

    async def select_omni_from_menu() -> bool:
        omni = await ev(
            """(() => {
              const titles=[...document.querySelectorAll('div,span,button,p')].filter(n=>{
                const t=(n.innerText||'').trim();
                return t==='Gemini Omni Flash' || (/^Gemini Omni Flash/i.test(t) && t.length < 55 && /New|Beta|2,?451/.test(t));
              });
              for (const n of titles) {
                let row=n;
                for (let i=0;i<6;i++) {
                  const p=row.parentElement; if (!p) break;
                  const pr=p.getBoundingClientRect();
                  const pt=(p.innerText||'');
                  if (pr.height>=48 && pr.height<=110 && pr.width>250
                      && /New|Beta|2,?451/.test(pt) && pr.y>250 && pr.y<800) {
                    p.click();
                    return {ok:true, y:Math.round(pr.y), t:pt.slice(0,50)};
                  }
                  row=p;
                }
              }
              return {ok:false};
            })()"""
        )
        if not omni or not omni.get("ok"):
            return False
        print(f"  click_omni={omni.get('t')} y={omni.get('y')}", flush=True)
        await asyncio.sleep(1.1)
        return True

    async def force_omni() -> str:
        await press_escape()
        await asyncio.sleep(0.2)

        chip = await read_model_chip()
        href = (await ev("location.href")) or ""
        if "Omni" in chip and "lipsync" not in href and "Aurora" not in chip and "Creatify" not in chip:
            print(f"  already Omni chip={chip}", flush=True)
            return chip

        await ensure_video_orbit(reselect_orbit=False)
        chip = await read_model_chip()
        if "Omni" not in chip:
            opened = await open_composer_chip_and_click()
            print(f"  open_picker chip={opened}", flush=True)
            if not opened:
                print("  WARN: no composer model chip found", flush=True)
                return chip
            await asyncio.sleep(1.3)
            ok = await select_omni_from_menu()
            if not ok:
                print("  WARN: Gemini Omni Flash not in open menu", flush=True)
                await press_escape()
                return await read_model_chip()

        await ev(
            """(() => {
              const b=document.querySelector('button[aria-label="Duration"]');
              if (b && b.innerText.trim() !== '8s') b.click();
            })()"""
        )
        await asyncio.sleep(0.3)
        await ev(
            """(() => {
              const e=[...document.querySelectorAll('button,[role="option"],div,span')].find(n=>(n.innerText||'').trim()==='8s');
              if (e) e.click();
            })()"""
        )
        href = (await ev("location.href")) or ""
        if "lipsync" in href:
            await click_video_modality()
            await asyncio.sleep(0.5)
            chip = await read_model_chip()
            if "Omni" not in chip:
                opened = await open_composer_chip_and_click()
                if opened:
                    await asyncio.sleep(1.2)
                    await select_omni_from_menu()
        cur = await read_model_chip()
        print(f"  cur_chip={cur}", flush=True)
        return cur

    async def wait_for_slot(timeout_s: int = 90) -> bool:
        """Avoid hard-blocking on Generate disabled — empty prompt often disables it.

        Only stop for upgrade paywall with no Generate, or prolonged missing composer.
        """
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            info = await ev(
                """(() => {
                  const text=document.body.innerText||'';
                  const m=text.match(/(\\d+)\\s*left/i);
                  const gen=document.querySelector('button[aria-label="Generate"]');
                  return {
                    left: m ? Number(m[1]) : null,
                    genDis: gen ? !!gen.disabled : true,
                    genExists: !!gen,
                    upgrade: /Remind Me Later/i.test(text) || /Upgrade to (Pro|Creator)/i.test(text),
                    captcha: !!document.querySelector('iframe[src*="hcaptcha"]')
                  };
                })()"""
            )
            if info and info.get("upgrade"):
                await dismiss_noise()
            left = (info or {}).get("left")
            gen_dis = (info or {}).get("genDis", True)
            gen_exists = (info or {}).get("genExists")
            print(
                f"  slots left={left} genDis={gen_dis} genExists={gen_exists} "
                f"captcha={(info or {}).get('captcha')}",
                flush=True,
            )
            # Composer present → proceed (prompt fill enables Generate)
            if gen_exists:
                return True
            await asyncio.sleep(4)
            if int(time.time() - t0) > 20:
                await call(
                    "Page.navigate",
                    {"url": "https://elevenlabs.io/app/image-video?modality=video"},
                )
                await asyncio.sleep(3.5)
                await dismiss_noise()
                orbit_selected["ok"] = False
                await ensure_video_orbit(reselect_orbit=True)
                await force_omni()
        return False

    async def click_generate() -> bool:
        await dismiss_noise()
        ok = await ev(
            """(() => {
              const b=document.querySelector('button[aria-label="Generate"]');
              if (!b || b.disabled) return false;
              b.click();
              return true;
            })()"""
        )
        if ok:
            return True
        await dismiss_noise()
        await asyncio.sleep(0.5)
        return bool(
            await ev(
                """(() => {
                  const b=document.querySelector('button[aria-label="Generate"]');
                  if (!b || b.disabled) return false;
                  b.click();
                  return true;
                })()"""
            )
        )

    # Prime Orbit once, then lock Omni
    await ensure_video_orbit(reselect_orbit=True)
    primed = await force_omni()
    print(f"PRIMED chip={primed}", flush=True)
    if "Omni" not in primed:
        print("STOP: could not prime Omni at session start", flush=True)
        return

    for scene, beat, slug, prompt in BEATS:
        dest = out_path(scene, beat, slug)
        if done(dest):
            print(f"SKIP {dest.name}", flush=True)
            continue

        attempts = 0
        while attempts < 4 and not done(dest):
            attempts += 1
            print(f"\n=== scene-{scene} {beat} {slug} attempt={attempts} ===", flush=True)
            try:
                await ensure_create_surface()
                cur = await force_omni()
                if "Omni" not in cur:
                    await asyncio.sleep(0.5)
                    cur = await force_omni()
                if "Omni" not in cur:
                    print(f"WARN: Omni lock failed chip={cur!r} — retrying beat", flush=True)
                    continue

                if not await wait_for_slot():
                    print("STOP: no concurrent generation slots", flush=True)
                    return

                tok = await refresh_tok()
                # re-assert Omni after possible slot-wait reload
                cur = await force_omni()
                if "Omni" not in cur:
                    print(f"WARN: Omni lost after slot wait chip={cur!r}", flush=True)
                    continue

                before = {
                    g["id"]
                    for g in (api_get("/v1/content/generations?per_page=40", tok).get("generations") or [])
                    if g.get("id")
                }

                plen = await ev(
                    f"""(() => {{
                      const ed=[...document.querySelectorAll('[contenteditable="true"]')].find(el => el.getBoundingClientRect().width > 100);
                      if (!ed) return -1;
                      ed.focus();
                      document.execCommand('selectAll', false, null);
                      document.execCommand('insertText', false, {json.dumps(prompt)});
                      return (ed.innerText || '').length;
                    }})()"""
                )
                print(f"  prompt_len={plen}", flush=True)
                if plen < 40:
                    print("STOP: prompt not inserted", flush=True)
                    return

                ok = False
                for _gwait in range(8):
                    ok = await click_generate()
                    print(f"  generate={ok}", flush=True)
                    if ok:
                        break
                    await asyncio.sleep(1.5)
                    await dismiss_noise()
                if not ok:
                    print("WARN: Generate still disabled after prompt — retrying beat", flush=True)
                    continue

                head = prompt[:36]
                # Confirm submission quickly; if nothing appears, dismiss modals and re-click
                submitted = False
                for _try in range(6):
                    await asyncio.sleep(3)
                    try:
                        await dismiss_noise()
                    except Exception:
                        pass
                    try:
                        tok = await refresh_tok()
                    except Exception:
                        tok = state["tok"] or Path("/tmp/elevenlabs_bearer.txt").read_text().strip()
                    try:
                        data = api_get("/v1/content/generations?per_page=15", tok)
                    except Exception as e:
                        print(f"  api_err early {e}", flush=True)
                        continue
                    for g in data.get("generations") or []:
                        if g["id"] in before:
                            continue
                        p = g.get("prompt") or ""
                        if head not in p and p[:36] not in prompt:
                            continue
                        submitted = True
                        break
                    if submitted:
                        break
                    print("  generate click produced no API row — retry Generate", flush=True)
                    await dismiss_noise()
                    rect = await ev(
                        """(() => {
                          const b=document.querySelector('button[aria-label="Generate"]');
                          if (!b || b.disabled) return null;
                          const r=b.getBoundingClientRect();
                          return {x:r.x+r.width/2, y:r.y+r.height/2};
                        })()"""
                    )
                    if rect:
                        await click_xy(rect["x"], rect["y"])
                    else:
                        await click_generate()

                if not submitted:
                    print(
                        "WARN: no generation submitted (captcha/rate?) — cooldown + retry beat",
                        flush=True,
                    )
                    await asyncio.sleep(20)
                    await call(
                        "Page.navigate",
                        {"url": "https://elevenlabs.io/app/image-video?modality=video"},
                    )
                    await asyncio.sleep(4)
                    await dismiss_noise()
                    orbit_selected["ok"] = False
                    continue

                # Poll API — refresh token each loop
                t0 = time.time()
                meta = None
                while time.time() - t0 < 420:
                    await asyncio.sleep(4)
                    try:
                        tok = await refresh_tok()
                    except Exception:
                        tok = state["tok"] or Path("/tmp/elevenlabs_bearer.txt").read_text().strip()
                    try:
                        data = api_get("/v1/content/generations?per_page=15", tok)
                    except Exception as e:
                        print(f"  api_err {e}", flush=True)
                        continue
                    for g in data.get("generations") or []:
                        if g["id"] in before:
                            continue
                        p = g.get("prompt") or ""
                        if head not in p and p[:36] not in prompt:
                            continue
                        mid = g.get("model_id")
                        print(f"  NEW {g['id']} {mid} {g.get('status')}", flush=True)
                        if mid != "gemini-omni-flash":
                            print(f"  REJECT non-omni {mid}", flush=True)
                            before.add(g["id"])
                            meta = {"_reject": True, "id": g["id"], "model_id": mid}
                            break
                        meta = wait_done(g["id"], tok)
                        break
                    if meta:
                        break
                else:
                    print("WARN: timeout waiting for generation — retrying beat", flush=True)
                    continue

                if meta.get("_reject"):
                    print(f"  retry after reject {meta.get('model_id')}", flush=True)
                    continue

                save(meta, scene, beat, slug)
                # Return to create surface for next beat
                try:
                    await connect()
                    await call(
                        "Page.navigate",
                        {"url": "https://elevenlabs.io/app/image-video?modality=video"},
                    )
                    await asyncio.sleep(3)
                    await dismiss_noise()
                    orbit_selected["ok"] = False
                except Exception as e:
                    print(f"  post-save nav warn: {e}", flush=True)
                break
            except Exception as e:
                print(f"  attempt error: {type(e).__name__}: {e}", flush=True)
                try:
                    await connect()
                except Exception:
                    pass
                continue

        if not done(dest):
            print(f"STOP: failed after retries for {dest.name}", flush=True)
            return
        await asyncio.sleep(1.0)

    print("\nRESUME COMPLETE", flush=True)
    for p in sorted(RAW.glob("scene-*/p0_*.mp4")):
        print(f"  {p.relative_to(RAW)} {p.stat().st_size}", flush=True)

    if state["ws"] is not None:
        try:
            await state["ws"].close()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
