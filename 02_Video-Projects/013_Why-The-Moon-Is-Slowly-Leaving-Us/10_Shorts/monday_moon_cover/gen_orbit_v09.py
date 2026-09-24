#!/usr/bin/env python3
"""Monday Orbit v09. One Omni take with the canonical still as an ingredient.

Frames mode kept the still and still redrew a toy. This pass uses Flow's
Ingredients control and orbit-seedance-reference-16x9-v01.png only.
Replaces the UAT Short only when the mid-frame matches that still.
Does not schedule. Does not touch the Jupiter upload.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(
    0,
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "013_Why-The-Moon-Is-Slowly-Leaving-Us/10_Shorts/monday_moon_cover",
)
import gen_orbit_v06 as v6  # noqa: E402
import gen_orbit_v07 as v7  # noqa: E402

ROOT = v6.ROOT
OUT = ROOT / "plates" / "orbit_v09"
OUT.mkdir(parents=True, exist_ok=True)
v6.OUT = OUT
MATCH_MIN = 0.62
PROMPT = (
    "The attached still is the only character. Copy that Orbit exactly. "
    "One solid matte orange rounded floater. One large black curved visor that is his face. "
    "Inside the visor, exactly two separate cream circular eyes, each with a dark pupil. "
    "Short stubby orange arms with dark three-finger hands. One antenna with a small bulb. "
    "One small soft glow centered under the body. "
    "He faces the camera, floats, and tips slightly toward the Moon. "
    "One grey cratered Moon is in the near-black sky beside him and drifts a little farther. "
    "Both stay in frame. One character only. "
    "Silent picture only. Vertical 9:16. Continuous motion. No text."
)


def ingredient_on(page) -> bool:
    return bool(v6.real_chips(page))


def ensure_ingredient(page) -> None:
    if ingredient_on(page):
        print(" ingredient already on the prompt", flush=True)
        return
    v6.configure_vertical(page)
    v6.g.open_settings(page)
    if not v6.g.click_button_including(page, "Ingredients"):
        raise RuntimeError("ingredients toggle missing")
    page.wait_for_timeout(400)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    v6.attach_ref(page)


def main() -> None:
    jup = Path(
        "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
        "020_What-Would-You-See-If-You-Fell-Into-Jupiter/04_Generated-Clips/picture_fix/status.json"
    )
    if jup.exists() and not json.loads(jup.read_text()).get("paused"):
        raise SystemExit("Jupiter is not paused")
    ref = v7.build_start()
    if "go" not in sys.argv:
        print("PROBE_OK", flush=True)
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
        ensure_ingredient(page)
        v6.abort_if_cushion(page)
        if not ingredient_on(page):
            raise RuntimeError("canonical still is not on the prompt")
        page.screenshot(path=str(OUT / "before_generate.png"))
        before = set(v7.portrait_ids(page))
        box = page.locator('[contenteditable="true"]').first
        box.click()
        page.keyboard.press("Meta+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(PROMPT)
        if not ingredient_on(page):
            raise RuntimeError("prompt edit removed the ingredient")
        summary = v6.summary_text(page)
        print(" settings", summary, flush=True)
        if "9:16" not in summary and "crop_9_16" not in summary:
            raise RuntimeError(f"not vertical: {summary}")
        v6.abort_if_cushion(page)
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
        ok = True
        for ss, name in (("0.5", "open"), ("1.625", "loop"), ("3.0", "react")):
            dest = OUT / f"hold_0_{name}.jpg"
            subprocess.run(
                [v6.FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(silent), "-frames:v", "1", str(dest)],
                check=True,
            )
            score = v7.match_score(dest, ref)
            scores[name] = round(score, 3)
            if score < MATCH_MIN:
                ok = False
        print(" scores", scores, flush=True)
        (OUT / "hold_0_match.json").write_text(json.dumps(scores, indent=2))
        if not ok or scores.get("react", 0) < MATCH_MIN:
            (OUT / "status.json").write_text(
                json.dumps({"passed": False, "scores": scores, "uat_replaced": False}, indent=2)
            )
            print("reject drift", flush=True)
            raise SystemExit(2)
        v6.FINAL = ROOT / "monday_moon_short_v09.mp4"
        v6.assemble(silent)
        final_scores = {}
        final_ok = True
        for ss, name in (("0.5", "qa_open"), ("3.0", "qa_react"), ("21.0", "qa_loop")):
            dest = OUT / f"{name}.jpg"
            subprocess.run(
                [v6.FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(v6.FINAL), "-frames:v", "1", str(dest)],
                check=True,
            )
            score = v7.match_score(dest, ref)
            final_scores[name] = round(score, 3)
            if score < MATCH_MIN:
                final_ok = False
        print(" final", final_scores, flush=True)
        if not final_ok or final_scores.get("qa_react", 0) < MATCH_MIN:
            (OUT / "status.json").write_text(
                json.dumps({"passed": False, "scores": scores, "final": final_scores, "uat_replaced": False}, indent=2)
            )
            print("final reject", flush=True)
            raise SystemExit(2)
        v6.replace_uat()
        (OUT / "status.json").write_text(json.dumps({"passed": True, "scores": final_scores}, indent=2))
        print("UAT_REPLACED", flush=True)


if __name__ == "__main__":
    main()
