#!/usr/bin/env python3
"""LEGACY — ElevenLabs Image & Video Omni for Video 002 P0.

DO NOT USE FOR NEW EPISODES. Default CG: 04_Audio/tools/orbit_gemini_veo.py
VO remains ElevenLabs TTS (Ben Orbit Narrator) — separate from this CG script.
"""
from __future__ import annotations

import base64
import json
import re
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
PROMPTS = ROOT / "03_Animation-Prompts/02_Individual-Prompts"
RAW = ROOT / "04_Generated-Clips/01_Raw"
LOG = ROOT / "03_Animation-Prompts/03_Generation-Logs/blackhole_p0_progress.jsonl"
QUEUE = ROOT / "03_Animation-Prompts/03_Generation-Logs/blackhole_generation_queue_v01.md"
PROFILE = Path("/Users/ben/code/youtube/.playwright-elevenlabs-profile")
API = "https://api.us.elevenlabs.io"
MODEL_LABEL = re.compile(r"Gemini.*Omni|Omni.?Flash|gemini-omni", re.I)

LOCK = (
    "Preserve Orbit exactly: rounded orange body, black faceplate, cream expressive eyes, "
    "single glowing antenna, short stubby side arms (no claws, no fingers), soft underside glow. "
    "Emotion through cream eyes and body language only. No text, logos, watermarks, or UI gibberish."
)

# (scene, beat, slug_hint, duration_hint, prompt)
P0_BEATS = [
    (
        "01",
        "A",
        "stare",
        8,
        "Deep space. Distant black hole silhouette wrapped in a thin glowing accretion ring. "
        "Orbit floats alone in mid-ground, cream eyes wide as he stares at the dark circle. "
        "Slow continuous hover. Slow camera push toward the ring. Premium cinematic 3D. "
        + LOCK,
    ),
    (
        "01",
        "B",
        "turn-camera",
        8,
        "Same deep-space set. Orbit turns from the black hole toward camera. Cream eyes nervous but curious. "
        "Antenna soft glow brightens. Medium close-up on faceplate. Shallow depth of field, accretion ring soft bokeh behind. "
        + LOCK,
    ),
    (
        "01",
        "C",
        "determined",
        8,
        "Orbit faces camera, determined little hover forward. Cream eyes resolve. "
        "Black hole still visible far behind as a tiny dark coin with a faint ring. Premium cinematic 3D. "
        + LOCK,
    ),
    (
        "06",
        "A",
        "probe-approach",
        8,
        "Orbit in a tiny illuminated probe-shell approaching a luminous black-hole accretion disk. "
        "Nervous hover wobble. Chase camera behind him; disk grows. Premium CG, intense but not horror. "
        + LOCK,
    ),
    (
        "06",
        "B",
        "lensing-astonish",
        8,
        "Orbit lifts both stubby arms in astonishment as the far side of the accretion disk warps into a glowing ring. "
        "Cream eyes huge. Epic medium-wide. Gravitational lensing spectacle. "
        + LOCK,
    ),
    (
        "07",
        "A",
        "chest-clock",
        8,
        "A simple glowing circular clock motif on Orbit's chest ticks normally for him. He glances down at it "
        "while falling toward distant darkness. Medium close-up. Time-dilation teaching beat. "
        + LOCK,
    ),
    (
        "08",
        "B",
        "stretch-gag",
        8,
        "Abstract tidal-gradient void. Teaching gag: Orbit tastefully elongates vertically like soft taffy "
        "(still recognisably Orbit, not gore). Cream eyes panicky-comical, then elastic snap-back toward normal. Spaghettification. "
        + LOCK,
    ),
    (
        "09",
        "A",
        "eyes-widen-horizon",
        8,
        "Orbit's cream eyes widen at a subtle shimmering event-horizon boundary. Reverent awe. "
        "Over-shoulder then reverse on faceplate. Point of no return. "
        + LOCK,
    ),
    (
        "09",
        "C",
        "failed-turnback",
        8,
        "Outside universe shrinks toward a bright point of light behind Orbit. He turns as if to go back, pauses, "
        "cream eyes dim — understands the trap. Quiet dread. "
        + LOCK,
    ),
    (
        "13",
        "A",
        "tiny-vs-jets",
        8,
        "Tiny Orbit against a galaxy-centre vista; twin jets punch from a bright nucleus. Epic wide. "
        "Orbit awed silence. Scale shot. "
        + LOCK,
    ),
    (
        "15",
        "A",
        "warm-wave",
        8,
        "Starfield. Orbit warm cream eyes, soft wave with stubby arm. Accretion glow far behind like a memory. Medium shot. "
        + LOCK,
    ),
    (
        "15",
        "B",
        "flyaway-ember",
        8,
        "Slow pull-back until Orbit is a small orange ember drifting into deep space. Continuous motion. Premium endcard energy. "
        + LOCK,
    ),
]


def log(rec: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def bearer_from_page(page) -> str:
    tok = page.evaluate(
        """() => {
          try {
            const auth=JSON.parse(localStorage.getItem('firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]'));
            return auth && auth.stsTokenManager && auth.stsTokenManager.accessToken;
          } catch (e) { return null; }
        }"""
    )
    if not tok:
        raise RuntimeError("no firebase token")
    Path("/tmp/elevenlabs_bearer.txt").write_text(tok + "\n")
    return tok


def api_get(path: str, token: str):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def known_ids() -> set[str]:
    ids: set[str] = set()
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("generation_id"):
                ids.add(rec["generation_id"])
    return ids


def dismiss_modals(page) -> None:
    for _ in range(4):
        clicked = False
        for label in [
            "Get started.",
            "Get started",
            "Accept all cookies",
            "Close",
            "Maybe later",
            "Not now",
            "Got it",
            "Continue",
        ]:
            try:
                loc = page.get_by_role("button", name=re.compile(rf"^{re.escape(label)}$", re.I))
                if loc.count():
                    loc.first.click(timeout=1500)
                    page.wait_for_timeout(400)
                    clicked = True
                    print("dismiss:", label, flush=True)
            except Exception:
                pass
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        if not clicked:
            break


def ensure_video_tab(page) -> None:
    # Prefer explicit Video tab
    for name in ["Video", "video"]:
        try:
            tab = page.get_by_role("tab", name=re.compile(rf"^{name}$", re.I))
            if tab.count():
                tab.first.click(timeout=2000)
                page.wait_for_timeout(600)
                print("video tab via role", flush=True)
                return
        except Exception:
            pass
    try:
        page.get_by_text(re.compile(r"^Video$"), exact=True).first.click(timeout=2000)
        page.wait_for_timeout(600)
        print("video tab via text", flush=True)
    except Exception:
        page.goto(
            "https://elevenlabs.io/app/image-video?modality=video",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        dismiss_modals(page)


def select_orbit_avatar(page) -> None:
    # Click Orbit avatar card if visible
    try:
        # avatar row often has img/button with name Orbit
        loc = page.get_by_text(re.compile(r"^Orbit$"), exact=True)
        if loc.count():
            loc.first.click(timeout=2000)
            page.wait_for_timeout(700)
            print("selected Orbit text", flush=True)
            return
    except Exception as e:
        print("orbit text click fail", e, flush=True)
    # fallback: open Avatars / View all
    try:
        page.get_by_text(re.compile(r"View all", re.I)).first.click(timeout=2000)
        page.wait_for_timeout(1000)
        page.get_by_text(re.compile(r"^Orbit$"), exact=True).first.click(timeout=3000)
        page.wait_for_timeout(700)
        print("selected Orbit from view-all", flush=True)
    except Exception as e:
        print("WARN could not click Orbit avatar:", e, flush=True)


def select_gemini_omni(page) -> None:
    # Open model picker — button often shows current model name
    opened = False
    for pat in [r"Sora", r"Seedance", r"Seedream", r"Gemini", r"Veo", r"Kling", r"Model"]:
        try:
            b = page.get_by_role("button", name=re.compile(pat, re.I))
            if b.count():
                b.first.click(timeout=2000)
                page.wait_for_timeout(800)
                opened = True
                print("opened model picker via", pat, flush=True)
                break
        except Exception:
            continue
    if not opened:
        # click any short model-like button near composer
        page.evaluate(
            """() => {
              const b=[...document.querySelectorAll('button')].find(x=>{
                const t=(x.innerText||'').trim();
                return t && t.length<40 && /(Sora|Seedance|Seedream|Gemini|Veo|Kling|Flash|Omni)/i.test(t);
              });
              if (b) b.click();
              return !!(b);
            }"""
        )
        page.wait_for_timeout(800)

    # Choose Gemini Omni Flash
    for pat in [
        r"Gemini Omni Flash",
        r"Omni Flash",
        r"gemini-omni-flash",
        r"Gemini.*Flash",
    ]:
        try:
            hit = page.get_by_text(re.compile(pat, re.I))
            if hit.count():
                hit.first.click(timeout=3000)
                page.wait_for_timeout(800)
                print("selected model", pat, flush=True)
                return
        except Exception:
            continue
    print("WARN: Gemini Omni Flash not confirmed selected", flush=True)


def set_duration_8s(page) -> None:
    try:
        b = page.get_by_role("button", name=re.compile(r"^\d+s$"))
        if b.count():
            cur = b.first.inner_text().strip()
            if cur != "8s":
                b.first.click(timeout=2000)
                page.wait_for_timeout(400)
                page.get_by_text(re.compile(r"^8s$"), exact=True).first.click(timeout=2000)
                page.wait_for_timeout(400)
                print("duration -> 8s", flush=True)
            else:
                print("duration already 8s", flush=True)
    except Exception as e:
        print("duration warn", e, flush=True)


def set_prompt(page, prompt: str) -> None:
    ed = page.locator('[contenteditable="true"]').first
    ed.click(timeout=5000)
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.keyboard.insert_text(prompt)
    page.wait_for_timeout(400)
    got = ed.inner_text()
    if len(got.strip()) < 40:
        # JS fallback
        page.evaluate(
            """(prompt) => {
              const ed=[...document.querySelectorAll('[contenteditable="true"]')]
                .find(el => el.getBoundingClientRect().width > 100);
              if (!ed) return false;
              ed.focus();
              document.execCommand('selectAll', false, null);
              document.execCommand('insertText', false, prompt);
              ed.dispatchEvent(new InputEvent('input', {bubbles:true}));
              return (ed.innerText||'').length;
            }""",
            prompt,
        )
        page.wait_for_timeout(300)


def click_generate(page) -> None:
    # aria-label Generate preferred
    btn = page.locator('button[aria-label="Generate"]')
    if btn.count() and not btn.first.is_disabled():
        btn.first.click(timeout=5000)
        print("generate via aria", flush=True)
        return
    # circular submit near "left"
    page.evaluate(
        """() => {
          const b=document.querySelector('button[aria-label="Generate"]');
          if (b && !b.disabled) { b.click(); return true; }
          const arrows=[...document.querySelectorAll('button')].filter(x=>{
            const a=x.getAttribute('aria-label')||'';
            return /generate|submit|send/i.test(a);
          });
          if (arrows[0]) { arrows[0].click(); return true; }
          return false;
        }"""
    )
    print("generate via js fallback", flush=True)


def wait_new_generation(token: str, before: set[str], timeout_s: int = 420) -> dict:
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        data = api_get("/v1/content/generations?per_page=20", token)
        gens = data.get("generations") or data.get("data") or []
        for g in gens:
            gid = g.get("id")
            if not gid or gid in before:
                continue
            if g.get("model_id") != "gemini-omni-flash":
                # still accept if it's our video modality and brand new
                if g.get("modality") != "video":
                    continue
            status = g.get("status")
            print(f"  seen {gid} model={g.get('model_id')} status={status}", flush=True)
            if status in ("pending", "processing", "queued", "in_progress"):
                before.add(gid)  # track but keep waiting for complete of this id
                # poll this id
                return wait_generation_done(token, gid, timeout_s=timeout_s - int(time.time() - t0))
            if status == "completed":
                return g
            if status in ("failed", "error"):
                raise RuntimeError(f"generation failed: {g.get('error_message')}")
        time.sleep(4)
    raise TimeoutError("no new generation observed")


def wait_generation_done(token: str, gid: str, timeout_s: int = 420) -> dict:
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        g = api_get(f"/v1/content/generations/{gid}", token)
        status = g.get("status")
        print(f"  poll {gid} {status}", flush=True)
        if status == "completed":
            return g
        if status in ("failed", "error"):
            raise RuntimeError(f"{gid} failed: {g.get('error_message')}")
        time.sleep(5)
    raise TimeoutError(f"{gid} not completed")


def download(g: dict, dest: Path) -> Path:
    url = g.get("download_url") or g.get("content_url")
    if not url:
        raise RuntimeError("no download_url")
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    return dest


def out_path(scene: str, beat: str, slug: str) -> Path:
    return RAW / f"scene-{scene}" / f"p0_{beat}_{slug}_gemini-omni-flash_v01_raw.mp4"


def already_done(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 100_000


def mark_queue_done(scene: str, beat: str) -> None:
    if not QUEUE.exists():
        return
    text = QUEUE.read_text()
    # "- [ ] Scene 01 · A ·"
    pat = re.compile(rf"- \[ \] Scene {int(scene)} · {beat} ·")
    text2, n = pat.subn(f"- [x] Scene {int(scene)} · {beat} ·", text, count=1)
    if n:
        QUEUE.write_text(text2)


def main(limit: int | None = None):
    RAW.mkdir(parents=True, exist_ok=True)
    beats = P0_BEATS[: limit or len(P0_BEATS)]
    seen = known_ids()

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            headless=False,
            viewport={"width": 1440, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(
            "https://elevenlabs.io/app/image-video?modality=video",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        dismiss_modals(page)
        ensure_video_tab(page)
        dismiss_modals(page)
        select_orbit_avatar(page)
        select_gemini_omni(page)
        set_duration_8s(page)
        token = bearer_from_page(page)
        print("auth ok", flush=True)

        for scene, beat, slug, _dur, prompt in beats:
            dest = out_path(scene, beat, slug)
            if already_done(dest):
                print(f"SKIP existing {dest.name}", flush=True)
                mark_queue_done(scene, beat)
                continue

            print(f"\n=== P0 scene-{scene} {beat} {slug} ===", flush=True)
            before = set(seen)
            # refresh listing snapshot
            try:
                listing = api_get("/v1/content/generations?per_page=30", token)
                for g in listing.get("generations") or []:
                    if g.get("id"):
                        before.add(g["id"])
            except Exception as e:
                print("listing warn", e, flush=True)

            set_prompt(page, prompt)
            page.wait_for_timeout(500)
            click_generate(page)
            page.wait_for_timeout(2000)

            # captcha may appear — wait for user solve if needed, or auto
            try:
                g = wait_new_generation(token, before, timeout_s=480)
            except Exception as e:
                print("wait err, refreshing token/page", e, flush=True)
                token = bearer_from_page(page)
                g = wait_new_generation(token, before, timeout_s=480)

            gid = g["id"]
            seen.add(gid)
            download(g, dest)
            rec = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "scene": scene,
                "beat": beat,
                "slug": slug,
                "generation_id": gid,
                "model_id": g.get("model_id"),
                "status": g.get("status"),
                "file": str(dest),
                "bytes": dest.stat().st_size,
                "prompt_head": prompt[:160],
            }
            log(rec)
            mark_queue_done(scene, beat)
            print(f"SAVED {dest} ({dest.stat().st_size} bytes)", flush=True)
            # small pause between gens
            time.sleep(2)

        context.close()
    print("\nP0 batch complete", flush=True)


if __name__ == "__main__":
    import sys

    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(limit=lim)
