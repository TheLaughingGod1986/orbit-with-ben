#!/usr/bin/env python3
"""LEGACY — ElevenLabs Image & Video Gemini Omni Flash for JWST.

DO NOT USE FOR NEW EPISODES OR REGENS.
Default CG path: 04_Audio/tools/orbit_flow_veo_ui.py (Google Flow Ultra UI).
Secondary: 04_Audio/tools/orbit_aistudio_veo_ui.py · API: orbit_gemini_veo.py (avoid for routine).
VO remains ElevenLabs TTS (Ben Orbit Narrator) — that is separate from this script.

Kept only for historical inventory / debugging of already-generated Omni clips.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "004_JWST-Discoveries-That-Change-Everything"
)
PROMPTS = ROOT / "03_Animation-Prompts/02_Individual-Prompts"
RAW = ROOT / "04_Generated-Clips/01_Raw"
LOG = ROOT / "03_Animation-Prompts/03_Generation-Logs/jwst_omni_progress.jsonl"
QUEUE = ROOT / "03_Animation-Prompts/03_Generation-Logs/jwst_generation_queue_v01.md"
AUDIT = ROOT / "03_Animation-Prompts/03_Generation-Logs/_omni_probe"
PROFILE = Path("/Users/ben/code/youtube/.playwright-elevenlabs-profile")
API = "https://api.us.elevenlabs.io"
# Hero-first: galaxies, black holes, JWST, then rest
SCENE_ORDER = ["04", "05", "02", "06", "03", "07", "01", "08"]

ANTI_EIFFEL = (
    "CRITICAL START FRAME: open on Orbit the orange robot in space — never on paper, "
    "blueprints, schematics, architectural drawings, lattice towers, or the Eiffel Tower. "
    "FORBIDDEN: Eiffel Tower, Paris landmarks, vintage engineering blueprints, parchment "
    "diagrams, wireframe building holograms, Explore-gallery architecture refs. "
    "If any blueprint or tower appears, replace it immediately with Orbit against deep space / JWST scenery."
)
LOCK = (
    "Preserve Orbit exactly: rounded orange body, black faceplate, cream expressive eyes, "
    "single glowing antenna, short stubby side arms (no claws, no fingers), soft underside glow. "
    "Emotion through cream eyes and body language only. No text, logos, watermarks, or UI gibberish. "
    "SILENT PICTURE ONLY: no dialogue, no narration, no voiceover, no spoken words, no lip-sync speech. "
    + ANTI_EIFFEL
)
PREFACE = (
    "Premium cinematic 3D animation, educational space documentary. Soft warm key light on Orbit, "
    "cool scientific accents, shallow depth of field, continuous subtle hover. "
    "Full character motion — not a still with light wiggle. "
    "SILENT PICTURE ONLY: no dialogue, no narration, no voiceover, no spoken words "
    "(channel VO is British Ben Orbit Narrator mixed later in edit). "
    + ANTI_EIFFEL + " "
)


def slugify(title: str) -> str:
    title = re.sub(r"[\(（][^)\）]*[\)）]", "", title)
    title = re.sub(r"\d+\s*[–\-]\s*\d+\s*s", "", title, flags=re.I)
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:40] or "beat"


def load_beats():
    out = []
    for scene in SCENE_ORDER:
        files = sorted(PROMPTS.glob(f"jwst_scene-{scene}_*_prompt_v01.md"))
        if not files:
            continue
        text = files[0].read_text()
        for m in re.finditer(
            r"### ([A-C]) — ([^\n]+)\n.*?--- PROMPT ---\n\n(.*?)\n\n--- END ---",
            text,
            re.S,
        ):
            beat, title, body = m.group(1), m.group(2).strip(), m.group(3).strip()
            prompt = body
            if "Preserve Orbit exactly as shown" in prompt:
                prompt = re.sub(
                    r"Preserve Orbit exactly as shown in the uploaded reference image\..*$",
                    LOCK,
                    prompt,
                    flags=re.S,
                )
            if not prompt.startswith("Premium cinematic"):
                prompt = PREFACE + prompt
            if LOCK not in prompt:
                prompt = prompt.rstrip() + " " + LOCK
            if "SILENT PICTURE ONLY" not in prompt:
                prompt = prompt.rstrip() + " " + (
                    "SILENT PICTURE ONLY: no dialogue, no narration, no voiceover, "
                    "no spoken words (British Ben Orbit Narrator is mixed in edit)."
                )
            out.append((scene, beat, slugify(title), prompt))
    return out


def log(rec: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def clear_image_refs(page) -> None:
    """Remove accidental Start/End frame / Image refs (e.g. Explore Eiffel blueprint)."""
    page.evaluate(
        """() => {
          const kill=[];
          for (const b of document.querySelectorAll('button')) {
            const a=(b.getAttribute('aria-label')||'').toLowerCase();
            const t=(b.innerText||'').trim();
            if (/remove|clear|delete|close/.test(a) || t==='×' || t==='x' || t==='✕') {
              const r=b.getBoundingClientRect();
              // Composer + start/end frame chips sit mid-lower UI
              if (r.y>280 && r.width>6 && r.width<48 && r.height>6 && r.height<48) kill.push(b);
            }
          }
          kill.forEach(b=>{ try{b.click();}catch(e){} });
          for (const el of document.querySelectorAll('[class*="chip"],button,div,span')) {
            const t=(el.innerText||'').trim();
            const a=(el.getAttribute('aria-label')||'').toLowerCase();
            if (/^@image/i.test(t) || /^image refs/i.test(t) || /start frame|end frame|reference image|eiffel/i.test(a+t)) {
              const x=[...el.querySelectorAll('button')].find(b=>/remove|close|x|clear|delete/i.test(b.getAttribute('aria-label')||'') || ['×','x','✕'].includes((b.innerText||'').trim()));
              if (x) try{x.click();}catch(e){}
              // Parent remove if this node itself is a remove control
              if (/remove|clear/.test(a) && el.tagName==='BUTTON') try{el.click();}catch(e){}
            }
          }
        }"""
    )
    page.wait_for_timeout(500)
    # Second pass — Explore often rebinds after prompt paste
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const a=(b.getAttribute('aria-label')||'').toLowerCase();
            if (/remove (image|frame|reference|start|end)/i.test(a)) {
              try{b.click();}catch(e){}
            }
          }
        }"""
    )
    page.wait_for_timeout(300)


def bearer(page) -> str:
    """Fresh Firebase access token (refresh if near expiry)."""
    tok = page.evaluate(
        """async () => {
          const key='firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]';
          try {
            const auth=JSON.parse(localStorage.getItem(key)||'null');
            if (!auth || !auth.stsTokenManager) return null;
            const st=auth.stsTokenManager;
            const need=!st.expirationTime || Date.now()>(st.expirationTime-120000);
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
            return st.accessToken||null;
          } catch (e) { return null; }
        }"""
    )
    # evaluate async may need awaitPromise — Playwright sync evaluate handles promises
    if not tok:
        raise RuntimeError("no firebase token — log into ElevenLabs in the Playwright profile")
    Path("/tmp/elevenlabs_bearer.txt").write_text(tok + "\n")
    return tok


def api_get(path: str, token: str):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise RuntimeError("401 unauthorized — token expired") from e
        raise


def credits_left(page) -> str:
    """Composer-adjacent 'N left' only (not subscription balance). Prefer API chars elsewhere."""
    return (
        page.evaluate(
            """() => {
              const gens=[...document.querySelectorAll('button[aria-label="Generate"]')];
              if (!gens.length) return '';
              const gr=gens[0].getBoundingClientRect();
              let best='';
              for (const el of document.querySelectorAll('button,span,div')) {
                const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                const m=t.match(/^(\\d+)\\s*left$/i);
                if (!m) continue;
                const r=el.getBoundingClientRect();
                if (r.width<8 || Math.abs((r.y+r.height/2)-(gr.y+gr.height/2))>80) continue;
                if (r.x < gr.x) best=m[1];
              }
              return best;
            }"""
        )
        or ""
    )


def out_path(scene, beat, slug) -> Path:
    return RAW / f"scene-{scene}" / f"p0_{beat}_{slug}_gemini-omni-flash_v01_raw.mp4"


def already_done(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 800_000


ORBIT_START_FRAME = Path(
    "/Users/ben/code/Orbit-YouTube/01_Orbit-Character/05_Seedance-References/"
    "orbit-seedance-reference-16x9-v01.png"
)


def reject_eiffel_startframe(path: Path, quarantine_dir: Path | None = None) -> str | None:
    """Return reason if clip is unusable Eiffel/blueprint; else None.

    Prefer trim-salvage when parchment is only an early start-frame flash and
    Orbit orange returns by ~1.5–2s (common Explore contamination). Only
    quarantine + fail when mid-clip stays paper or never recovers orange.
    """
    import shutil
    import subprocess
    import tempfile

    import numpy as np
    from PIL import Image

    if not path.exists() or not shutil.which("ffmpeg"):
        return None

    # Dense enough to catch a 0.5–1s parchment flash mid-take
    sample_times = (0.0, 0.25, 0.5, 0.8, 1.2, 1.5, 2.0, 3.0, 4.5, 6.0)

    def scores(jpg: Path) -> tuple[float, float]:
        im = np.array(Image.open(jpg).convert("RGB").resize((320, 180)))
        r, g, b = im[:, :, 0].astype(float), im[:, :, 1].astype(float), im[:, :, 2].astype(float)
        orange = float(
            ((r > 140) & (r > g * 1.15) & (r > b * 1.4) & (g > 60) & (b < 180)).mean()
        )
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        sat = (im.max(axis=2) - im.min(axis=2)).astype(float)
        paper = float(((lum > 170) & (sat < 45)).mean())
        return paper, orange

    bad: list[tuple[float, float, float]] = []  # ss, paper, orange
    rows: list[tuple[float, float, float]] = []
    with tempfile.TemporaryDirectory(prefix="eiffel_qa_") as td:
        td_path = Path(td)
        for i, ss in enumerate(sample_times):
            jpg = td_path / f"f{i}.jpg"
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    str(ss),
                    "-i",
                    str(path),
                    "-frames:v",
                    "1",
                    str(jpg),
                ],
                check=False,
                capture_output=True,
            )
            if not jpg.exists() or jpg.stat().st_size <= 2000:
                continue
            paper, orange = scores(jpg)
            rows.append((ss, paper, orange))
            if paper >= 0.40 and orange < 0.01:
                bad.append((ss, paper, orange))

    if not bad:
        return None

    # Salvage: early flash only — first clean Orbit frame after last early bad
    late_bad = [b for b in bad if b[0] >= 2.5]
    if late_bad:
        # Mid/late contamination — cannot trim; quarantine
        ss, paper, orange = bad[0]
        reason = f"eiffel/blueprint flash t={ss:.2f}s paper={paper:.2f} orange={orange:.3f}"
        qdir = quarantine_dir or (RAW.parent / "_Rejected" / "eiffel-startframe-jwst-v02")
        qdir.mkdir(parents=True, exist_ok=True)
        dest = qdir / path.name
        if dest.exists():
            dest = qdir / f"{path.stem}_{int(time.time())}{path.suffix}"
        path.replace(dest)
        print(f"REJECT Eiffel → {dest.name}: {reason}", flush=True)
        return reason

    last_bad_t = max(b[0] for b in bad)
    clean_t = None
    for ss, paper, orange in rows:
        if ss > last_bad_t + 0.05 and orange >= 0.02 and paper < 0.20:
            clean_t = ss
            break
    if clean_t is None:
        ss, paper, orange = bad[0]
        reason = (
            f"eiffel/blueprint flash t={ss:.2f}s paper={paper:.2f} orange={orange:.3f} "
            "(no clean Orbit recovery)"
        )
        qdir = quarantine_dir or (RAW.parent / "_Rejected" / "eiffel-startframe-jwst-v02")
        qdir.mkdir(parents=True, exist_ok=True)
        dest = qdir / path.name
        if dest.exists():
            dest = qdir / f"{path.stem}_{int(time.time())}{path.suffix}"
        path.replace(dest)
        print(f"REJECT Eiffel → {dest.name}: {reason}", flush=True)
        return reason

    trim_in = round(clean_t + 0.05, 2)
    tmp = path.with_suffix(".eiffel_trim.mp4")
    proc = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{trim_in:.2f}",
            "-i",
            str(path),
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-an",
            str(tmp),
        ],
        capture_output=True,
    )
    if proc.returncode != 0 or not tmp.exists() or tmp.stat().st_size < 400_000:
        if tmp.exists():
            tmp.unlink()
        ss, paper, orange = bad[0]
        reason = f"eiffel trim failed after t={ss:.2f}s flash"
        qdir = quarantine_dir or (RAW.parent / "_Rejected" / "eiffel-startframe-jwst-v02")
        qdir.mkdir(parents=True, exist_ok=True)
        dest = qdir / path.name
        if dest.exists():
            dest = qdir / f"{path.stem}_{int(time.time())}{path.suffix}"
        path.replace(dest)
        print(f"REJECT Eiffel → {dest.name}: {reason}", flush=True)
        return reason

    # Keep raw contaminated copy for audit, replace working file with trimmed
    qdir = quarantine_dir or (RAW.parent / "_Rejected" / "eiffel-startframe-jwst-v02")
    qdir.mkdir(parents=True, exist_ok=True)
    archive = qdir / f"{path.stem}_pretrim_{int(time.time())}{path.suffix}"
    path.replace(archive)
    tmp.replace(path)
    print(
        f"SALVAGE Eiffel trim_in={trim_in:.2f}s → {path.name} (raw → {archive.name})",
        flush=True,
    )
    return None


def attach_orbit_start_frame(page, ref: Path | None = None) -> bool:
    """After clearing Explore refs, lock Start frame to Orbit 16:9 reference.

    Prevents Explore from rebinding the Eiffel blueprint as start frame.
    """
    img = ref or ORBIT_START_FRAME
    if not img.exists():
        print(f"WARN: Orbit start-frame missing: {img}", flush=True)
        return False

    # Open start-frame / image-ref upload if a control is visible
    page.evaluate(
        """() => {
          const candidates=[...document.querySelectorAll('button,div,[role="button"],label')];
          const hit=candidates.find(el=>{
            const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).toLowerCase();
            const r=el.getBoundingClientRect();
            if (r.width<8 || r.height<8 || r.y<200) return false;
            return /start frame|add start|image refs|upload image|add image|reference image/.test(t);
          });
          if (hit) try{hit.click();}catch(e){}
        }"""
    )
    page.wait_for_timeout(400)

    inputs = page.locator('input[type="file"]')
    n = inputs.count()
    attached = False
    for i in range(n):
        try:
            accept = (inputs.nth(i).get_attribute("accept") or "").lower()
            # Prefer image-accepting inputs; skip obvious video-only
            if accept and "image" not in accept and "video" in accept and "image" not in accept:
                continue
            if accept and not any(x in accept for x in ("image", "png", "jpg", "jpeg", "*", ".")):
                if "video" in accept:
                    continue
            inputs.nth(i).set_input_files(str(img), timeout=5000)
            attached = True
            print(f"orbit start-frame: set_input_files idx={i} accept={accept!r}", flush=True)
            break
        except Exception as e:
            print(f"orbit start-frame: idx={i} skip ({e})", flush=True)
    if not attached and n:
        try:
            inputs.last.set_input_files(str(img), timeout=5000)
            attached = True
            print("orbit start-frame: set_input_files last", flush=True)
        except Exception as e:
            print(f"orbit start-frame FAIL: {e}", flush=True)
    page.wait_for_timeout(700)
    page.keyboard.press("Escape")
    page.wait_for_timeout(250)
    return attached


def mark_queue_done(scene, beat, slug=None):
    if not QUEUE.exists():
        return
    text = QUEUE.read_text()
    # V004 queue lines: "- [ ] scene-04/A_galaxies-too-early"
    pat = rf"- \[ \] scene-{scene}/{beat}_[^\n]+"
    text2, n = re.compile(pat).subn(lambda m: m.group(0).replace("- [ ]", "- [x]", 1), text, count=1)
    if n:
        QUEUE.write_text(text2)
        return
    # fallback older formats
    text2, n = re.compile(rf"- \[ \] Scene {scene} · {beat} ·").subn(
        f"- [x] Scene {scene} · {beat} ·", text, count=1
    )
    if n:
        QUEUE.write_text(text2)


def dismiss(page):
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    page.evaluate(
        """() => {
          // Close Lip sync / modal dialogs that steal Generate clicks
          const closeBtn=[...document.querySelectorAll('button')].find(b=>{
            const a=(b.getAttribute('aria-label')||'').toLowerCase();
            const t=(b.innerText||'').trim();
            return a==='close' || a.includes('close dialog') || a.includes('dismiss')
              || t==='×' || t==='✕';
          });
          if (closeBtn) closeBtn.click();
          [...document.querySelectorAll('button')].forEach(b=>{
            const t=(b.innerText||'').trim();
            const a=b.getAttribute('aria-label')||'';
            if (/Remind Me Later|Accept all cookies|Get started|Maybe later|Not now|^Close$/i.test(t)
                || /close/i.test(a)) b.click();
          });
        }"""
    )
    page.wait_for_timeout(400)
    # If Lip sync tab/modal still visible, escape again and force Video modality URL
    body = ""
    try:
        body = page.locator("body").inner_text()[:800]
    except Exception:
        pass
    if "Lip sync" in body or "lip syncing" in body.lower():
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)


def select_orbit_headshot(page):
    page.evaluate(
        """() => {
          const orbit=[...document.querySelectorAll('button,div,span')].find(
            n => (n.innerText||'').trim()==='Orbit');
          if (orbit) orbit.click();
        }"""
    )
    page.wait_for_timeout(900)
    # Style picker: Headshot
    clicked = page.evaluate(
        """() => {
          const hs=[...document.querySelectorAll('button,div,[role="option"],img,span')].find(n=>{
            const t=(n.innerText||'').trim();
            const a=n.getAttribute('aria-label')||'';
            return /^Headshot$/i.test(t) || /Headshot/i.test(a);
          });
          if (hs) { hs.click(); return true; }
          // click first favorite card near "Favorites"
          const fav=[...document.querySelectorAll('div,button')].find(n=>/Favorites/i.test((n.innerText||'').trim()) && (n.innerText||'').length<40);
          if (fav && fav.parentElement) {
            const card=[...fav.parentElement.querySelectorAll('button,div')].find(c=>{
              const r=c.getBoundingClientRect();
              return r.width>60 && r.height>60 && r.width<220;
            });
            if (card) { card.click(); return 'card'; }
          }
          return false;
        }"""
    )
    print("orbit headshot:", clicked, flush=True)
    page.wait_for_timeout(700)
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)


def click_video_tab(page):
    """Force the Video modality tab — never leave Lip sync / Image selected."""
    page.evaluate(
        """() => {
          const tabs=[...document.querySelectorAll('button,[role="tab"]')];
          const n=tabs.find(el=>{
            const t=(el.innerText||'').trim();
            return t==='Video' || /^Video$/i.test(t.split('\\n')[0]);
          });
          if (n) n.click();
        }"""
    )
    page.wait_for_timeout(600)


def on_lip_sync(page) -> bool:
    try:
        return bool(
            page.evaluate(
                """() => {
                  const body=(document.body.innerText||'');
                  if (/Image is required for lip syncing/i.test(body)) return true;
                  const tabs=[...document.querySelectorAll('button,[role="tab"]')];
                  const lip=tabs.find(el=>/^Lip sync$/i.test((el.innerText||'').trim().split('\\n')[0]));
                  if (!lip) return false;
                  const sel=lip.getAttribute('aria-selected')==='true'
                    || /active|selected/i.test(lip.className||'')
                    || lip.getAttribute('data-state')==='active';
                  return !!sel;
                }"""
            )
        )
    except Exception:
        return False


def force_video_composer(page):
    """Hard navigate to video composer — Lip sync steals Generate clicks otherwise."""
    page.goto(
        "https://elevenlabs.io/app/image-video?modality=video",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)
    dismiss(page)
    click_video_tab(page)
    page.wait_for_timeout(400)
    if on_lip_sync(page):
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        click_video_tab(page)


def read_model_chip(page) -> str:
    return (
        page.evaluate(
            """() => {
              const chips=[...document.querySelectorAll('button')].map(x=>{
                const t=(x.innerText||'').trim().split('\\n')[0];
                const r=x.getBoundingClientRect();
                return {t, y:r.y, w:r.width, h:r.height, x:r.x};
              }).filter(o => o.t && o.t.length<40 && o.w>20 && o.h>10 && o.y>400
                && /(Veo|Seedance|Sora|Gemini|Mochi|Kling|Omni|Flash)/i.test(o.t));
              chips.sort((a,b)=>b.y-a.y);
              return chips[0] ? chips[0].t : '';
            }"""
        )
        or ""
    )


def force_omni(page) -> str:
    chip = read_model_chip(page)
    if "Omni" in chip:
        print("already Omni:", chip, flush=True)
        return chip
    # click model chip
    page.evaluate(
        """() => {
          const chips=[...document.querySelectorAll('button')].filter(x=>{
            const t=(x.innerText||'').trim().split('\\n')[0];
            const r=x.getBoundingClientRect();
            return t && t.length<40 && r.width>20 && r.y>400
              && /(Veo|Seedance|Sora|Gemini|Mochi|Kling|Omni|Flash)/i.test(t);
          });
          chips.sort((a,b)=>b.getBoundingClientRect().y-a.getBoundingClientRect().y);
          if (chips[0]) chips[0].click();
        }"""
    )
    page.wait_for_timeout(1200)
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / "model_menu_live.png"))
    # pick Gemini Omni Flash row
    ok = page.evaluate(
        """() => {
          const titles=[...document.querySelectorAll('div,span,button,p,li')].filter(n=>{
            const t=(n.innerText||'').trim();
            return t==='Gemini Omni Flash' || /^Gemini Omni Flash\\b/i.test(t) && t.length<60;
          });
          for (const n of titles) {
            let row=n;
            for (let i=0;i<8;i++) {
              const p=row.parentElement; if (!p) break;
              const pr=p.getBoundingClientRect();
              if (pr.height>=36 && pr.height<=140 && pr.width>180 && pr.y>150) {
                p.click();
                return {ok:true, t:(p.innerText||'').slice(0,60)};
              }
              row=p;
            }
            n.click();
            return {ok:true, t:(n.innerText||'').slice(0,60)};
          }
          return {ok:false};
        }"""
    )
    print("select omni:", ok, flush=True)
    page.wait_for_timeout(1000)
    chip2 = read_model_chip(page)
    print("chip after:", chip2, flush=True)
    return chip2


def set_duration_8s(page):
    # Open duration chip, click visible 8s in popper (not hidden <option>)
    opened = page.evaluate(
        """() => {
          const b=[...document.querySelectorAll('button')].find(x=>{
            const t=(x.innerText||'').trim();
            const r=x.getBoundingClientRect();
            return /^\\d+s$/.test(t) && r.y>400 && r.width>20;
          });
          if (!b) return null;
          const cur=b.innerText.trim();
          if (cur==='8s') return {already:true};
          b.click();
          return {opened:true, cur};
        }"""
    )
    print("duration open:", opened, flush=True)
    page.wait_for_timeout(500)
    if opened and not opened.get("already"):
        clicked = page.evaluate(
            """() => {
              // Radix popper visible items
              const items=[...document.querySelectorAll('[data-radix-popper-content-wrapper] span, [data-radix-popper-content-wrapper] div, [role=option], [role=menuitem]')];
              const hit=items.find(el=>{
                const t=(el.innerText||'').trim();
                const r=el.getBoundingClientRect();
                return t==='8s' && r.width>10 && r.height>10;
              });
              if (hit) { hit.click(); return true; }
              return false;
            }"""
        )
        print("duration 8s click:", clicked, flush=True)
        page.wait_for_timeout(400)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)


def set_prompt(page, prompt: str):
    page.keyboard.press("Escape")
    page.wait_for_timeout(250)
    # Prefer known prompt box id
    box = page.locator("#image-video-prompt-box")
    if box.count():
        box.first.click(force=True, timeout=5000)
        page.keyboard.press("Meta+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(prompt)
        page.wait_for_timeout(300)
        return
    eds = page.locator('[contenteditable="true"]')
    if eds.count() == 0:
        ta = page.locator("textarea").first
        ta.click(force=True, timeout=5000)
        page.keyboard.press("Meta+A")
        page.keyboard.insert_text(prompt)
        return
    idx = page.evaluate(
        """() => {
          const eds=[...document.querySelectorAll('[contenteditable="true"]')];
          let best=-1, area=0;
          eds.forEach((el,i)=>{
            const r=el.getBoundingClientRect();
            const a=r.width*r.height;
            if (a>area && r.width>100) { area=a; best=i; }
          });
          return best;
        }"""
    )
    ed = eds.nth(idx if idx is not None and idx >= 0 else 0)
    ed.click(force=True, timeout=5000)
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.keyboard.insert_text(prompt)
    page.wait_for_timeout(300)


def click_generate(page) -> bool:
    """Click enabled Generate only — never Loading / audio / quantity chips."""
    for _ in range(12):
        state = page.evaluate(
            """() => {
              // Prefer exact aria-label=Generate (right-side submit)
              const exact=[...document.querySelectorAll('button[aria-label="Generate"]')];
              const ranked=[];
              for (const b of exact) {
                const r=b.getBoundingClientRect();
                if (r.width<10 || r.height<10) continue;
                const a=(b.getAttribute('aria-label')||'').trim();
                const dis=!!(b.disabled || b.getAttribute('aria-disabled')==='true'
                  || /loading/i.test(a) || /loading/i.test(b.innerText||''));
                if (dis) continue;
                ranked.push({ok:true, x:r.x+r.width/2, y:r.y+r.height/2, a:'Generate', score:r.x});
              }
              if (ranked.length) {
                ranked.sort((a,b)=>b.score-a.score);
                return ranked[0];
              }
              // Fallback: circular send on far right — exclude audio/quantity
              const cands=[];
              for (const b of document.querySelectorAll('button')) {
                const a=(b.getAttribute('aria-label')||'').trim();
                const t=(b.innerText||'').trim();
                const r=b.getBoundingClientRect();
                if (r.width<28 || r.height<28 || r.y<450 || r.x<1050) continue;
                if (/loading|audio|quantity|credit|left|off|on/i.test(a+' '+t)) continue;
                const dis=!!(b.disabled || b.getAttribute('aria-disabled')==='true');
                if (dis) continue;
                if (/^Generate$/i.test(a) || (/^submit$|^send$/i.test(a)))
                  cands.push({x:r.x+r.width/2,y:r.y+r.height/2,a,w:r.width,score:r.x});
                else if (r.width>=34 && r.width<=72 && r.height>=34 && r.height<=72)
                  cands.push({x:r.x+r.width/2,y:r.y+r.height/2,a:a||'circle',w:r.width,score:r.x});
              }
              cands.sort((a,b)=>b.score-a.score || b.y-a.y);
              return cands[0] ? {ok:true, ...cands[0]} : {ok:false};
            }"""
        )
        if state and state.get("ok"):
            page.mouse.click(state["x"], state["y"])
            print("generate click", state, flush=True)
            return True
        page.wait_for_timeout(400)
    print("generate FAILED — still Loading/disabled", flush=True)
    return False


def wait_seen(token, before, timeout_s=90):
    """Return generation id as soon as it appears (do not wait for completion)."""
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        data = api_get("/v1/content/generations?per_page=30", token)
        for g in data.get("generations") or []:
            gid = g.get("id")
            if not gid or gid in before:
                continue
            print(
                f"  seen {gid} model={g.get('model_id')} status={g.get('status')}",
                flush=True,
            )
            return gid, g
        time.sleep(1.5)
    raise TimeoutError("no new generation")


def wait_new(token, before, timeout_s=420):
    t0 = time.time()
    gid, _ = wait_seen(token, before, timeout_s=min(90, timeout_s))
    return wait_done(token, gid, max(30, timeout_s - int(time.time() - t0)))


def wait_done(token, gid, timeout_s=420):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        g = api_get(f"/v1/content/generations/{gid}", token)
        st = g.get("status")
        print(f"  poll {gid} {st}", flush=True)
        if st == "completed":
            return g
        if st in ("failed", "error"):
            raise RuntimeError(g.get("error_message") or st)
        time.sleep(2)
    raise TimeoutError(gid)


def download(g, dest: Path):
    url = g.get("download_url") or g.get("content_url")
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    # Strip baked-in model speech (often American) — channel VO is British Ben only
    strip_native_audio(dest)
    return dest


def strip_native_audio(path: Path) -> None:
    """Rewrite mp4 without an audio track (ffmpeg). No-op if ffmpeg missing."""
    import shutil
    import subprocess

    if not shutil.which("ffmpeg"):
        print("WARN: ffmpeg missing — cannot strip native Veo/Omni audio", flush=True)
        return
    tmp = path.with_suffix(".silent.tmp.mp4")
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(path),
                "-c:v",
                "copy",
                "-an",
                str(tmp),
            ],
            check=True,
            capture_output=True,
        )
        tmp.replace(path)
    except subprocess.CalledProcessError as e:
        print(f"WARN: strip audio failed for {path.name}: {e}", flush=True)
        if tmp.exists():
            tmp.unlink()


def filter_beats(beats, arg):
    if not arg:
        return [b for b in beats if not already_done(out_path(*b[:3]))]
    if re.fullmatch(r"\d{2}", arg) and arg in SCENE_ORDER:
        return [b for b in beats if b[0] == arg]
    if arg.isdigit():
        pending = [b for b in beats if not already_done(out_path(*b[:3]))]
        return pending[: int(arg)]
    return beats


def setup_composer(page):
    # Always hard-open video composer — Lip Sync / History steal Generate otherwise
    force_video_composer(page)
    select_orbit_headshot(page)
    click_video_tab(page)
    clear_image_refs(page)
    chip = force_omni(page)
    if "Omni" not in chip:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        chip = force_omni(page)
    set_duration_8s(page)
    clear_image_refs(page)
    click_video_tab(page)
    dismiss(page)
    if on_lip_sync(page):
        print("WARN: still on Lip sync after setup — reforcing video", flush=True)
        force_video_composer(page)
        click_video_tab(page)
        chip = force_omni(page)
        set_duration_8s(page)
    return chip


def main(arg=None):
    AUDIT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    beats = filter_beats(load_beats(), arg)
    print("queue", [(s, b, slug) for s, b, slug, _ in beats], flush=True)
    if not beats:
        print("nothing to do")
        return

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE),
            headless=False,
            channel="chrome",
            viewport={"width": 1440, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(
            "https://elevenlabs.io/app/image-video?modality=video",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4500)
        chip = setup_composer(page)
        page.screenshot(path=str(AUDIT / "ready.png"))
        print("ready chip=", chip, "credits≈", credits_left(page), flush=True)
        if "Omni" not in (chip or ""):
            print("FATAL: could not select Gemini Omni Flash", flush=True)
            ctx.close()
            raise SystemExit(2)

        token = bearer(page)
        failures = 0
        for scene, beat, slug, prompt in beats:
            dest = out_path(scene, beat, slug)
            if already_done(dest):
                print("SKIP", dest.name, flush=True)
                mark_queue_done(scene, beat, slug)
                continue
            print(
                f"\n=== scene-{scene} {beat} {slug} · credits≈{credits_left(page)} ===",
                flush=True,
            )
            ok_one = False
            for attempt in range(1, 5):
                try:
                    left = credits_left(page)
                    if left == "0" or on_lip_sync(page) or "Omni" not in read_model_chip(page):
                        if left == "0":
                            print("concurrent 0 left — waiting 90s", flush=True)
                            time.sleep(90)
                        setup_composer(page)
                    click_video_tab(page)
                    if on_lip_sync(page):
                        force_video_composer(page)
                        setup_composer(page)
                    clear_image_refs(page)
                    token = bearer(page)
                    before = {
                        g["id"]
                        for g in (
                            api_get(
                                "/v1/content/generations?per_page=30", token
                            ).get("generations")
                            or []
                        )
                        if g.get("id")
                    }
                    set_prompt(page, prompt)
                    page.wait_for_timeout(600)
                    clear_image_refs(page)
                    # Skip attach_orbit_start_frame — upload disables Generate; trim-salvage instead
                    click_video_tab(page)
                    # Prompt typing can reset model chip — re-lock Omni + 8s
                    if "Omni" not in read_model_chip(page):
                        force_omni(page)
                        set_duration_8s(page)
                    if on_lip_sync(page):
                        raise RuntimeError("stuck on Lip sync before Generate")
                    if not click_generate(page):
                        page.screenshot(
                            path=str(AUDIT / f"no_gen_btn_{scene}{beat}_a{attempt}.png")
                        )
                        raise RuntimeError("no generate button")
                    page.wait_for_timeout(3000)
                    page.screenshot(
                        path=str(AUDIT / f"after_gen_{scene}{beat}_a{attempt}.png")
                    )
                    if on_lip_sync(page):
                        raise RuntimeError("Generate landed on Lip sync")
                    g = wait_new(token, before, timeout_s=420)
                    if g.get("model_id") and "omni" not in str(g.get("model_id")).lower():
                        print("WARN wrong model", g.get("model_id"), flush=True)
                    download(g, dest)
                    if not already_done(dest):
                        raise RuntimeError(f"download too small: {dest.stat().st_size}")
                    eiffel = reject_eiffel_startframe(dest)
                    if eiffel:
                        raise RuntimeError(f"Eiffel QA reject: {eiffel}")
                    log(
                        {
                            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            "scene": scene,
                            "beat": beat,
                            "slug": slug,
                            "generation_id": g["id"],
                            "model_id": g.get("model_id"),
                            "file": str(dest),
                            "bytes": dest.stat().st_size,
                            "attempt": attempt,
                        }
                    )
                    mark_queue_done(scene, beat, slug)
                    print(f"SAVED {dest} ({dest.stat().st_size})", flush=True)
                    ok_one = True
                    failures = 0
                    break
                except Exception as e:
                    print(f"  attempt {attempt} failed: {e}", flush=True)
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(800)
                    try:
                        force_video_composer(page)
                        setup_composer(page)
                    except Exception:
                        pass
            if not ok_one:
                failures += 1
                print(f"FAIL scene-{scene} {beat} after retries", flush=True)
                if failures >= 3:
                    print("ABORT: 3 consecutive failures", flush=True)
                    ctx.close()
                    raise SystemExit(1)
            time.sleep(12)  # cool-down between clips (avoid Lip Sync / rate stalls)

        ctx.close()
    print("\nbatch complete", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
