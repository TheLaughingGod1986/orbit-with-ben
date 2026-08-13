#!/usr/bin/env python3
"""Europa Part 01 — 3 continuous Omni Flash plates (Flow Ultra). Experiment-forward long."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path("/Users/ben/code/Orbit-YouTube")
TOOLS = REPO / "04_Audio/tools"
sys.path.insert(0, str(TOOLS))
# Reuse Omni configure helpers from oort experiment
EXP = REPO / "02_Video-Projects/_Experiments/omni-oort-1min-test"
sys.path.insert(0, str(EXP))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402
from _flow_omni_sync_batch import configure_omni, read_prompt_pill, OMNI_LABELS  # noqa: E402

EP = REPO / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa"
PLATES = json.loads((EP / "07_Edit-Project/parts/part-01_omni_plates_v01.json").read_text())
OUT = EP / "04_Generated-Clips/01_Raw/part-01"


def generate_omni(page, prompt: str, dest: Path, *, configure: bool, timeout_s: int = 700) -> dict:
    t0 = time.time()
    ref = veo.ORBIT_REF
    if "/project/" not in (page.url or ""):
        page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
        flow.settle_after_nav(page, wait_ms=1500)
        flow.dismiss_banners(page)
        flow.ensure_project(page)
    flow.ensure_agent_session(page)
    before = flow.collect_media_ids(page)
    if configure:
        configure_omni(page)
        flow.settle_after_nav(page, wait_ms=400)
        flow.ensure_agent_session(page)
    flow.ensure_orbit_agent_instruction(page)
    if flow._prompt_attachment_count(page) < 1:
        for attempt in range(3):
            try:
                flow.attach_orbit_to_prompt(page, ref)
                break
            except Exception as e:
                print(f"  attach retry {attempt+1}/3: {e}", flush=True)
                try:
                    page.keyboard.press("Escape")
                except Exception:
                    pass
                page.wait_for_timeout(1500)
                flow.ensure_agent_session(page)
        else:
            raise RuntimeError("Orbit attach failed")
    flow.set_prompt(
        page,
        prompt + " Target length about 8 to 10 seconds. Fully animated continuous motion the whole time.",
    )
    if flow._prompt_attachment_count(page) < 1:
        flow.attach_orbit_to_prompt(page, ref)
    pill = read_prompt_pill(page)
    if pill and not any(lbl.lower() in pill.lower() for lbl in OMNI_LABELS):
        print(f"  pill drifted to {pill!r} — reconfigure", flush=True)
        configure_omni(page)
    flow.submit_create(page)
    media_id = flow.wait_and_download(page, dest, before_ids=before, timeout_s=timeout_s)
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": dest.stat().st_size,
        "media_id": media_id,
        "engine": "flow-omni",
        "pill": read_prompt_pill(page),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[1:])
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=flow.profile_path(None))
        configured = False
        try:
            for plate in PLATES["plates"]:
                if only and plate["id"] not in only and plate["slug"] not in only:
                    continue
                dest = OUT / f"omni_p01_{plate['id']}_{plate['slug']}_v01.mp4"
                if dest.exists() and dest.stat().st_size > 500_000:
                    print(f"SKIP {dest.name}", flush=True)
                    continue
                print(f"\n=== Part01 {plate['id']} {plate['slug']} ===", flush=True)
                meta = generate_omni(page, plate["prompt"], dest, configure=not configured)
                configured = True
                print(f"SAVED {dest.name} {meta}", flush=True)
        finally:
            ctx.close()
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
