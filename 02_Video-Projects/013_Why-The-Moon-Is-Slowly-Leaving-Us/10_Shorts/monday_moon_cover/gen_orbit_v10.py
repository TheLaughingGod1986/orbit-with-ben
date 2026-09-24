#!/usr/bin/env python3
"""Monday Orbit v10. One image-to-video take.

The start frame is orbit-seedance-reference-16x9-v01.png itself.
Frame 0 of the plate must already be that picture. A black-void or toy
mid-frame is rejected. Does not schedule. Does not touch Jupiter.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(
    0,
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "013_Why-The-Moon-Is-Slowly-Leaving-Us/10_Shorts/monday_moon_cover",
)
import gen_orbit_v06 as v6  # noqa: E402
import gen_orbit_v07 as v7  # noqa: E402

ROOT = v6.ROOT
OUT = ROOT / "plates" / "orbit_v10"
OUT.mkdir(parents=True, exist_ok=True)
v6.OUT = OUT
STILL = v6.REF
FRAME0_MIN = 0.75
MID_MIN = 0.55
PROMPT = (
    "Image to video from the first frame. That frame is already Orbit. "
    "Keep his exact face: the large black curved visor, two cream eyes with dark pupils, "
    "short stubby arms, dark three-finger hands, one antenna, one underside glow, "
    "and the solid matte orange body. "
    "He only floats and tips slightly. The grey Moon drifts a little farther in the near-black sky. "
    "One character only. Silent picture only. Vertical 9:16. Continuous motion. No text."
)


def gray(im: Image.Image) -> np.ndarray:
    rgb = np.asarray(im.convert("RGB")).astype(np.float32)
    return 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]


def ncc(a: np.ndarray, b: np.ndarray) -> float:
    a = (a - a.mean()) / (a.std() + 1e-6)
    b = (b - b.mean()) / (b.std() + 1e-6)
    return float((a * b).mean())


def same_picture(frame: Image.Image, still: Image.Image) -> float:
    """Score how well `frame` is the still or a crop of it."""
    picture = gray(frame)
    source = gray(still)
    fh, fw = picture.shape
    sh, sw = source.shape
    best = 0.0
    aspect = fw / fh
    for scale in (0.45, 0.6, 0.75, 0.9, 1.0):
        win_h = int(sh * scale)
        win_w = int(win_h * aspect)
        if win_w > sw or win_h > sh or win_h < 20:
            win_w = int(sw * scale)
            win_h = int(win_w / aspect)
        if win_w > sw or win_h > sh or win_h < 20 or win_w < 20:
            continue
        y_step = max(1, (sh - win_h) // 6)
        x_step = max(1, (sw - win_w) // 6)
        for y in range(0, sh - win_h + 1, y_step):
            for x in range(0, sw - win_w + 1, x_step):
                window = source[y : y + win_h, x : x + win_w]
                resized = np.array(
                    Image.fromarray(window.astype(np.uint8)).resize((fw, fh), Image.Resampling.BILINEAR)
                ).astype(np.float32)
                best = max(best, ncc(picture, resized))
    squashed = np.array(
        Image.fromarray(source.astype(np.uint8)).resize((fw, fh), Image.Resampling.BILINEAR)
    ).astype(np.float32)
    return max(best, ncc(picture, squashed))


def use_frames(page) -> None:
    v6.configure_vertical(page)
    clicked = False
    for _ in range(4):
        if not v6.panel_open(page):
            v6.g.open_settings(page)
        page.wait_for_timeout(400)
        clicked = v6.g.click_button_including(page, "Frames")
        if clicked:
            break
    if not clicked:
        page.screenshot(path=str(OUT / "frames_miss.png"))
        raise RuntimeError("Frames control missing")
    page.wait_for_timeout(400)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)


def start_chip_src(page) -> str:
    return page.evaluate(
        """() => {
          const chips=[...document.querySelectorAll('button.chip-container, button.empty-chip')].filter(b => {
            const r=b.getBoundingClientRect();
            return r.y>800 && r.x<500 && r.width>40;
          });
          const start=chips.find(b => /start/i.test(b.innerText||'')) || chips[0];
          if (!start) return '';
          const img=start.querySelector('img');
          return img ? (img.currentSrc||img.src||'') : '';
        }"""
    )


def download_image(page, src: str, dest: Path) -> None:
    b64 = page.evaluate(
        """async (src) => {
          const r = await fetch(src);
          const buf = await r.arrayBuffer();
          const bytes = new Uint8Array(buf);
          let s = '';
          const chunk = 0x8000;
          for (let i=0;i<bytes.length;i+=chunk) s += String.fromCharCode.apply(null, bytes.subarray(i, i+chunk));
          return btoa(s);
        }""",
        src,
    )
    import base64

    dest.write_bytes(base64.b64decode(b64))


def attach_still(page) -> None:
    """Put the canonical PNG on Start and leave End empty."""
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    src = start_chip_src(page)
    if src:
        print(" start already filled, replacing", flush=True)
        page.evaluate(
            """() => {
              const chip=[...document.querySelectorAll('button.chip-container')].find(b => {
                const r=b.getBoundingClientRect();
                return r.y>800 && r.x<450 && b.querySelector('img');
              });
              if (!chip) return;
              const cancel=chip.querySelector('.hover-icon-overlay, mat-icon');
              if (cancel) cancel.click();
            }"""
        )
        page.wait_for_timeout(400)
    page.locator("button.empty-chip", has_text="Start").first.click(force=True)
    page.wait_for_timeout(500)
    page.evaluate(
        """() => {
          window.__fileInput = null;
          const proto = HTMLInputElement.prototype;
          if (proto.__orbitPatched) return;
          const orig = proto.click;
          proto.click = function() {
            if (this.type === 'file') { window.__fileInput = this; return; }
            return orig.apply(this, arguments);
          };
          proto.__orbitPatched = true;
        }"""
    )
    page.locator('button:has-text("Upload media")').locator("visible=true").last.click()
    page.wait_for_timeout(400)
    el = page.evaluate_handle("() => window.__fileInput || null").as_element()
    if el is None:
        page.screenshot(path=str(OUT / "start_miss.png"))
        raise RuntimeError("file input missing")
    el.set_input_files(str(STILL))
    asset = page.locator("button.asset-item", has_text="orbit-seedance-reference-16x9-v01.png").locator("visible=true")
    asset.first.wait_for(timeout=30000)
    asset.last.click()
    page.wait_for_timeout(600)
    detail = page.locator("button.detail-add-to-prompt-btn").locator("visible=true")
    if detail.count() == 0:
        page.screenshot(path=str(OUT / "start_miss.png"))
        raise RuntimeError("Add to prompt missing")
    detail.first.click()
    print(" add-to-prompt True", flush=True)
    page.wait_for_timeout(1200)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)


def main() -> None:
    jup = Path(
        "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
        "020_What-Would-You-See-If-You-Fell-Into-Jupiter/04_Generated-Clips/picture_fix/status.json"
    )
    if jup.exists() and not json.loads(jup.read_text()).get("paused"):
        raise SystemExit("Jupiter is not paused")
    if not STILL.exists():
        raise SystemExit(f"missing still {STILL}")
    still_im = Image.open(STILL)
    if "go" not in sys.argv:
        print("PROBE_OK", still_im.size, flush=True)
        return

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(v6.g.CDP)
        page = next(
            pg
            for ctx in browser.contexts
            for pg in ctx.pages
            if "d2ebe084-78fb-4d48-9006-2d897c5a80fb" in (pg.url or "") and "/edit/" not in (pg.url or "")
        )
        page.bring_to_front()
        v6.abort_if_cushion(page)
        src = start_chip_src(page)
        if src:
            chip_path = OUT / "start_chip.png"
            download_image(page, src, chip_path)
            existing = same_picture(Image.open(chip_path), still_im)
            print(f" existing chip {existing:.3f}", flush=True)
            if existing < FRAME0_MIN:
                src = ""
        if not src:
            use_frames(page)
            v6.abort_if_cushion(page)
            attach_still(page)
            src = start_chip_src(page)
        if not src:
            page.screenshot(path=str(OUT / "start_miss.png"))
            raise RuntimeError("start frame missing after attach")
        chip_path = OUT / "start_chip.png"
        download_image(page, src, chip_path)
        chip_score = same_picture(Image.open(chip_path), still_im)
        print(f" chip score {chip_score:.3f}", flush=True)
        page.screenshot(path=str(OUT / "start_attached.png"))
        if chip_score < FRAME0_MIN:
            (OUT / "status.json").write_text(
                json.dumps({"passed": False, "reason": "start chip is not the still", "chip_score": round(chip_score, 3), "uat_replaced": False})
            )
            raise SystemExit(2)
        end_filled = page.evaluate(
            """() => [...document.querySelectorAll('button.chip-container')].some(b => {
              const r=b.getBoundingClientRect();
              return r.y>800 && r.x>400 && r.x<520 && b.querySelector('img');
            })"""
        )
        if end_filled:
            raise RuntimeError("End frame is set; this take is start-frame only")
        box = page.locator('[contenteditable="true"]').first
        box.click()
        page.keyboard.press("Meta+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(PROMPT)
        if not start_chip_src(page):
            raise RuntimeError("prompt edit removed the start frame")
        summary = v6.summary_text(page)
        print(" settings", summary, flush=True)
        if "9:16" not in summary and "crop_9_16" not in summary:
            raise RuntimeError(f"not vertical: {summary}")
        v6.abort_if_cushion(page)
        before = set(v7.portrait_ids(page))
        page.locator('button[aria-label="Start generation"]').first.click()
        print("submitted", flush=True)
        uid = None
        t0 = time.time()
        while time.time() - t0 < 240:
            page.wait_for_timeout(8000)
            v6.abort_if_cushion(page)
            fresh = [i for i in v7.portrait_ids(page) if i and i not in before]
            print(f"  wait {int(time.time()-t0)}s fresh={len(fresh)}", flush=True)
            if fresh:
                uid = fresh[0]
                break
        if not uid:
            (OUT / "status.json").write_text(json.dumps({"passed": False, "reason": "timeout", "uat_replaced": False}))
            raise SystemExit(2)
        raw = OUT / "hold_0.mp4"
        v7.download_portrait(page, uid, raw)
        if "/edit/" in (page.url or ""):
            page.evaluate(
                """() => {
                  const el=[...document.querySelectorAll('button')].find(b =>
                    (b.getAttribute('aria-label')||'')==='Back button to go to previous page');
                  if (el) el.click();
                }"""
            )
            page.wait_for_timeout(800)
        silent = OUT / "hold_0_silent.mp4"
        subprocess.run(
            [v6.FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw), "-an", "-c:v", "copy", str(silent)],
            check=True,
        )
        scores = {}
        for ss, name in (("0.0", "frame0"), ("3.0", "react")):
            dest = OUT / f"hold_0_{name}.jpg"
            subprocess.run(
                [v6.FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(silent), "-frames:v", "1", str(dest)],
                check=True,
            )
            scores[name] = round(same_picture(Image.open(dest), still_im), 3)
        print(" scores", scores, flush=True)
        (OUT / "hold_0_match.json").write_text(json.dumps(scores, indent=2))
        if scores["frame0"] < FRAME0_MIN or scores["react"] < MID_MIN:
            (OUT / "status.json").write_text(
                json.dumps({"passed": False, "scores": scores, "uat_replaced": False}, indent=2)
            )
            print("reject", flush=True)
            raise SystemExit(2)
        v6.FINAL = ROOT / "monday_moon_short_v10.mp4"
        v6.assemble(silent)
        qa = {}
        ok = True
        for ss, name in (("0.0", "qa_frame0"), ("3.0", "qa_react")):
            dest = OUT / f"{name}.jpg"
            subprocess.run(
                [v6.FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(v6.FINAL), "-frames:v", "1", str(dest)],
                check=True,
            )
            qa[name] = round(same_picture(Image.open(dest), still_im), 3)
            if (name == "qa_frame0" and qa[name] < FRAME0_MIN) or (name == "qa_react" and qa[name] < MID_MIN):
                ok = False
        print(" final", qa, flush=True)
        if not ok:
            (OUT / "status.json").write_text(
                json.dumps({"passed": False, "scores": scores, "final": qa, "uat_replaced": False}, indent=2)
            )
            print("final reject", flush=True)
            raise SystemExit(2)
        v6.replace_uat()
        (OUT / "status.json").write_text(json.dumps({"passed": True, "scores": qa}, indent=2))
        print("UAT_REPLACED", flush=True)


if __name__ == "__main__":
    main()
