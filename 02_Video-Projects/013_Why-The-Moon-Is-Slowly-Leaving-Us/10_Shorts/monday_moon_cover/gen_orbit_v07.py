#!/usr/bin/env python3
"""Monday Orbit again. The generic toy is rejected.

The only character reference is orbit-seedance-reference-16x9-v01.png.
A frame matches only when its body matches that still. The rejected toy
does not. The UAT file is replaced only after the open, react, and loop match.
Does not schedule. Does not resume Jupiter.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(
    0,
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "013_Why-The-Moon-Is-Slowly-Leaving-Us/10_Shorts/monday_moon_cover",
)
import gen_orbit_v06 as v6  # noqa: E402

ROOT = v6.ROOT
OUT = ROOT / "plates" / "orbit_v07"
OUT.mkdir(parents=True, exist_ok=True)
REF = v6.REF
STILL_CUT = OUT / "still_cut.png"
START = OUT / "start_from_still.png"
FFMPEG = v6.FFMPEG
MATCH_MIN = 0.62
MAX_FAILS = 3
PROMPT = (
    "The start frame is Orbit. Do not redesign him. "
    "Keep the large black curved visor that is his face, two round cream eyes with dark pupils, "
    "short stubby arms with dark three-finger hands, one antenna, one small underside glow, "
    "and the solid matte orange rounded body. Not an egg. Not a toy. Not oval cartoon eyes. "
    "He faces the camera, floats, and tips slightly. The same grey Moon drifts a little farther "
    "in the near-black sky. Both stay in frame. One character only. "
    "Silent picture only. Vertical 9:16. Continuous motion. No text."
)


def build_start() -> np.ndarray:
    """Place the still's own character on a 9:16 board. No other robot."""
    rgb = np.asarray(Image.open(REF).convert("RGB"))
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    orange = (r > 145) & (g > 55) & (g < 200) & (b < 115) & (r > g + 25)
    orange[:, 560:] = False
    seed = np.zeros(orange.shape, dtype=bool)
    seed[260:420, 240:500] = True
    labeled, n = ndimage.label(ndimage.binary_dilation(orange, iterations=2))
    best_i, best = 0, 0
    for i in range(1, n + 1):
        overlap = int(((labeled == i) & seed).sum())
        if overlap > best:
            best, best_i = overlap, i
    comp = ndimage.binary_dilation(labeled == best_i, iterations=8)
    ys, xs = np.where(comp)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())
    crop = rgb[y0 : y1 + 1, x0 : x1 + 1].copy()
    crop[~comp[y0 : y1 + 1, x0 : x1 + 1]] = 0
    Image.fromarray(crop).save(STILL_CUT)
    ch = crop.shape[0]
    scale = 820 / ch
    im = Image.fromarray(crop).resize((int(crop.shape[1] * scale), int(ch * scale)), Image.Resampling.LANCZOS)
    board = Image.new("RGB", (720, 1280), (0, 0, 0))
    board.paste(im, (max(0, (720 - im.width) // 2 - 40), max(0, (1280 - im.height) // 2 - 40)))
    ImageDraw.Draw(board).ellipse((520, 160, 690, 330), fill=(148, 148, 154))
    board.save(START)
    return np.asarray(Image.open(STILL_CUT).convert("RGB"))


def match_score(path: Path, ref: np.ndarray) -> float:
    rgb = np.asarray(Image.open(path).convert("RGB"))
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    orange = (r > 140) & (g > 50) & (g < 210) & (b < 130) & (r > g + 15)
    labeled, n = ndimage.label(ndimage.binary_dilation(orange, iterations=4))
    if n < 1:
        return 0.0
    sizes = ndimage.sum(labeled > 0, labeled, index=range(1, n + 1))
    comp = labeled == (int(np.argmax(sizes)) + 1)
    ys, xs = np.where(comp)
    pad = 8
    y0 = max(0, int(ys.min()) - pad)
    x0 = max(0, int(xs.min()) - pad)
    y1 = min(rgb.shape[0] - 1, int(ys.max()) + pad)
    x1 = min(rgb.shape[1] - 1, int(xs.max()) + pad)
    crop = Image.fromarray(rgb[y0 : y1 + 1, x0 : x1 + 1]).resize(
        (ref.shape[1], ref.shape[0]), Image.Resampling.BILINEAR
    )
    a = np.asarray(crop).astype(np.float32)
    b = ref.astype(np.float32)
    a = (a - a.mean()) / (a.std() + 1e-6)
    b = (b - b.mean()) / (b.std() + 1e-6)
    return float((a * b).mean())


def portrait_ids(page) -> list[str]:
    return page.evaluate(
        """() => [...document.querySelectorAll('img')].map(el => {
          const r=el.getBoundingClientRect();
          const src=el.currentSrc||'';
          if ((el.alt||'')!=='Generated video thumbnail') return '';
          if (!(r.height>r.width && r.height>80 && src.includes('/image/'))) return '';
          return src.split('/image/')[1].split('?')[0];
        }).filter(Boolean)"""
    )


def download_portrait(page, uid: str, dest: Path) -> None:
    box: dict[str, bytes] = {}

    def on_resp(resp) -> None:
        if resp.status == 200 and f"/video/{uid}" in resp.url:
            body = resp.body()
            if b"ftyp" in body[:64]:
                box["b"] = body

    page.on("response", on_resp)
    try:
        page.evaluate(
            """(uid) => {
              const el=[...document.querySelectorAll('img')].find(img => (img.currentSrc||'').includes(uid));
              if (el) el.click();
            }""",
            uid,
        )
        page.wait_for_timeout(2500)
    finally:
        try:
            page.remove_listener("response", on_resp)
        except Exception:
            pass
    if "b" not in box:
        raise RuntimeError(f"no video bytes for {uid}")
    dest.write_bytes(box["b"])


def upload_start(page) -> None:
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    page.evaluate(
        """() => {
          const el=[...document.querySelectorAll('button')].find(b => {
            const t=(b.innerText||'').trim();
            return t.includes('Frames') && b.getBoundingClientRect().width>4;
          });
          if (el) el.click();
        }"""
    )
    page.wait_for_timeout(500)
    clicked = False
    try:
        with page.expect_file_chooser(timeout=8000) as fc:
            page.evaluate(
                """() => {
                  const el=[...document.querySelectorAll('button')].find(b => {
                    const r=b.getBoundingClientRect();
                    return (b.innerText||'').trim()==='Start' && r.width>4 && r.y>700;
                  });
                  if (!el) throw new Error('no Start');
                  el.click();
                }"""
            )
        fc.value.set_files(str(START))
        clicked = True
        print(" start frame uploaded", flush=True)
    except Exception as exc:
        print(" start chooser", type(exc).__name__, flush=True)
    if not clicked:
        raise RuntimeError("could not attach the still as the start frame")
    page.wait_for_timeout(1500)
    page.screenshot(path=str(OUT / "start_attached.png"))


def main() -> None:
    jup = Path(
        "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
        "020_What-Would-You-See-If-You-Fell-Into-Jupiter/04_Generated-Clips/picture_fix/status.json"
    )
    if jup.exists() and not json.loads(jup.read_text()).get("paused"):
        raise SystemExit("Jupiter is not paused")
    ref = build_start()
    toy = Path(
        "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
        "cursor_agent_stores/bc-01a0cd79-01ff-7df2-abc0-ae6e8554b895/files/"
        "media/monday-moon-reject/open-generic-robot.jpg"
    )
    toy_score = match_score(toy, ref) if toy.exists() else 0.0
    start_score = match_score(START, ref)
    print(f" scores start {start_score:.2f} toy {toy_score:.2f}", flush=True)
    if start_score < MATCH_MIN or toy_score >= MATCH_MIN:
        raise SystemExit("match gate does not separate the still from the toy")
    if "go" not in sys.argv:
        print("PROBE_OK", flush=True)
        return

    from playwright.sync_api import sync_playwright

    fails = 0
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(v6.g.CDP)
        page = next(
            pg for ctx in browser.contexts for pg in ctx.pages
            if "d2ebe084-78fb-4d48-9006-2d897c5a80fb" in (pg.url or "") and "/edit/" not in (pg.url or "")
        )
        page.bring_to_front()
        v6.abort_if_cushion(page)
        v6.configure_vertical(page)
        upload_start(page)
        v6.abort_if_cushion(page)
        while fails < MAX_FAILS:
            before = set(portrait_ids(page))
            box = page.locator('[contenteditable="true"]').first
            box.click()
            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            page.keyboard.insert_text(PROMPT)
            page.locator('button[aria-label="Start generation"]').first.click()
            print("submitted", fails, flush=True)
            uid = None
            t0 = time.time()
            while time.time() - t0 < 240:
                page.wait_for_timeout(8000)
                v6.abort_if_cushion(page)
                fresh = [i for i in portrait_ids(page) if i and i not in before]
                print(f"  wait {int(time.time()-t0)}s fresh={len(fresh)}", flush=True)
                if fresh:
                    uid = fresh[0]
                    break
            if not uid:
                fails += 1
                print("timeout", fails, flush=True)
                continue
            raw = OUT / f"hold_{fails}.mp4"
            try:
                download_portrait(page, uid, raw)
            except Exception as exc:
                fails += 1
                print("download fail", exc, flush=True)
                page.keyboard.press("Escape")
                continue
            # Leave the edit page if the click opened one.
            if "/edit/" in (page.url or ""):
                page.evaluate(
                    """() => {
                      const el=[...document.querySelectorAll('button')].find(b =>
                        (b.getAttribute('aria-label')||'')==='Back button to go to previous page');
                      if (el) el.click();
                    }"""
                )
                page.wait_for_timeout(800)
            silent = OUT / f"hold_{fails}_silent.mp4"
            subprocess.run(
                [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw), "-an", "-c:v", "copy", str(silent)],
                check=True,
            )
            scores = {}
            ok = True
            for ss, name in (("0.5", "open"), ("1.625", "loop"), ("3.0", "react")):
                dest = OUT / f"hold_{fails}_{name}.jpg"
                subprocess.run(
                    [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(silent), "-frames:v", "1", str(dest)],
                    check=True,
                )
                score = match_score(dest, ref)
                scores[name] = round(score, 3)
                if score < MATCH_MIN:
                    ok = False
            print(" scores", scores, flush=True)
            (OUT / f"hold_{fails}_match.json").write_text(json.dumps(scores, indent=2))
            if not ok:
                fails += 1
                print("reject toy-or-drift", fails, flush=True)
                continue
            v6.OUT = OUT
            v6.FINAL = ROOT / "monday_moon_short_v07.mp4"
            v6.assemble(silent)
            final_scores = {}
            final_ok = True
            for ss, name in (("0.5", "qa_open"), ("3.0", "qa_react"), ("21.0", "qa_loop")):
                dest = OUT / f"{name}.jpg"
                subprocess.run(
                    [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(v6.FINAL), "-frames:v", "1", str(dest)],
                    check=True,
                )
                score = match_score(dest, ref)
                final_scores[name] = round(score, 3)
                if score < MATCH_MIN:
                    final_ok = False
            print(" final", final_scores, flush=True)
            if not final_ok:
                fails += 1
                print("final reject", fails, flush=True)
                continue
            v6.replace_uat()
            (OUT / "status.json").write_text(json.dumps({"passed": True, "scores": final_scores}, indent=2))
            print("UAT_REPLACED", flush=True)
            return
    (OUT / "status.json").write_text(json.dumps({"passed": False, "fails": fails}, indent=2))
    raise SystemExit(2)


if __name__ == "__main__":
    main()
