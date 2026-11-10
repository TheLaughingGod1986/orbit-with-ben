#!/usr/bin/env python3
"""Neutron Star Part 01 — Omni Flash via Flow Playwright (BACKUP only).

Primary path: `_gen_part01_omni_api_v05.py` → Gemini Omni Flash API.
Use this script only when the API is down (billing, auth, or 429).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path("/Users/ben/code/Orbit-YouTube")
TOOLS = REPO / "04_Audio/tools"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(HERE))

import orbit_flow_veo_ui as flow  # noqa: E402
from _flow_omni_select_cursor import configure_omni, read_prompt_pill, OMNI_LABELS  # noqa: E402

EP = REPO / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star"
PLATES_PATH = Path(
    __import__("os").environ.get(
        "ORBIT_PLATES_JSON",
        str(HERE / "parts/part-01_omni_plates_cursor_v08.json"),
    )
)
PLATES = json.loads(PLATES_PATH.read_text())
OUT = Path(
    __import__("os").environ.get(
        "ORBIT_OUT_DIR",
        str(EP / "04_Generated-Clips/01_Raw/part-01"),
    )
)
ORBIT_REF = (
    REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
)
REPORT_PATH = HERE / PLATES_PATH.name.replace("plates", "gen_report")

VACUUM = (
    " EMPTY BLACK VACUUM: zero pinprick stars, zero grain, zero tiled starfield, zero white specks. "
    " Only the named subjects on near-black. "
)
LOCK = (
    " Hard lock: MATCH the attached start frame's Orbit exactly — same character, not a cheap toy. "
    " Matte orange sphere, glossy black visor FACEPLATE as the whole face, two cream circular eyes "
    " with dark pupils, stubby orange arms with dark three-finger hands, single antenna with glowing bulb, "
    " ONE small underside glow. Not eyes on a blank orange ball. Not a glowing yellow belly. "
    " Exactly ONE Orbit — never two, never a second face. When he turns, solid orange back. "
    " No readable HUD, lettering, or name on the body or visor. No drawn cartoon mouth. "
    " Orbit is IN the scene from the first frame of this clip — already present, not arriving. "
    " Target length about 8 seconds. Fully animated continuous motion — never freeze. "
    " No logo, no title, no brand sting, no subscribe graphic. "
    " FULL FRAME 16:9 fill — no letterbox, no cinematic black bars top or bottom. "
    " The remnant is a compact glowing STAR (about twenty kilometres across), NOT a planet, "
    " NOT a city, NO buildings, NO skyscrapers, NO streets, NO Earth. "
    " CAMERA VARIETY LOCK: do not fly Orbit in from the left. Do not zoom the star from a tiny point "
    " to fill the frame. Do not repeat a left-third Orbit / right-third giant-star medium portrait."
    + VACUUM
)
NO_ORBIT = (
    " HARD: do not generate Orbit, any robot, any spacecraft character, any logo, any title. "
    " Strange picture only. Empty space. No text."
    + VACUUM
)


def generate_omni(
    page,
    prompt: str,
    dest: Path,
    *,
    configure: bool,
    attach_orbit: bool,
    orbit_ref: Path | None = None,
    timeout_s: int = 700,
) -> dict:
    t0 = time.time()
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
    ref = orbit_ref or (ORBIT_REF if attach_orbit else None)
    if attach_orbit:
        try:
            flow.ensure_orbit_agent_instruction(page)
        except Exception as e:
            print(f"  agent instruction skipped: {e}", flush=True)
    if ref is not None:
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
                raise RuntimeError("start-frame attach failed")
    full = prompt + (LOCK if attach_orbit else NO_ORBIT)
    flow.set_prompt(page, full)
    if ref is not None and flow._prompt_attachment_count(page) < 1:
        flow.attach_orbit_to_prompt(page, ref)
    pill = read_prompt_pill(page)
    if pill and (not any(lbl.lower() in pill.lower() for lbl in OMNI_LABELS) or "x2" in pill.replace(" ", "").lower()):
        print(f"  pill needs reconfigure: {pill!r}", flush=True)
        configure_omni(page)
        pill = read_prompt_pill(page)
    print(f"  submit pill={pill!r}", flush=True)
    flow.submit_create(page)
    media_id = flow.wait_and_download(
        page, dest, before_ids=before, timeout_s=timeout_s, min_elapsed_s=22,
    )
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": dest.stat().st_size,
        "media_id": media_id,
        "engine": "flow-omni",
        "pill": read_prompt_pill(page),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    only = {a for a in sys.argv[1:] if not a.startswith("--")}
    headed = "--headed" in sys.argv
    from playwright.sync_api import sync_playwright

    report = []
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=headed, profile=flow.profile_path(None))
        configured = False
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=1500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("FLOW AUTH DEAD — Ben must sign in. Stop. No more gens.")
            print(f"logged_in url={page.url}", flush=True)
            for plate in PLATES["plates"]:
                if only and plate["id"] not in only and plate["slug"] not in only:
                    continue
                dest = OUT / plate["file"]
                if plate.get("keep") or (dest.exists() and dest.stat().st_size > 500_000):
                    print(f"SKIP {dest.name}", flush=True)
                    report.append({"id": plate["id"], "status": "skip", "file": dest.name})
                    continue
                print(f"\n=== Part01 cursor {plate['id']} {plate['slug']} orbit={plate.get('orbit')} ===", flush=True)
                try:
                    start = plate.get("start_frame")
                    orbit_ref = (HERE / start) if start else None
                    if orbit_ref is not None and not orbit_ref.exists():
                        orbit_ref = EP / start
                    meta = generate_omni(
                        page,
                        plate["prompt"],
                        dest,
                        configure=not configured,
                        attach_orbit=bool(plate.get("orbit")),
                        orbit_ref=orbit_ref,
                    )
                    configured = True
                    print(f"SAVED {dest.name} {meta}", flush=True)
                    report.append({"id": plate["id"], "status": "ok", "file": dest.name, **meta})
                except Exception as e:
                    print(f"FAIL {plate['id']}: {e}", flush=True)
                    report.append({"id": plate["id"], "status": "fail", "error": str(e)})
                    configured = False
                    try:
                        flow.recover_flow_home(page)
                    except Exception:
                        pass
                    if "sign in" in str(e).lower() or "auth" in str(e).lower():
                        print("AUTH DEAD — stopping remaining plates", flush=True)
                        break
        finally:
            ctx.close()
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    ok = sum(1 for r in report if r["status"] in ("ok", "skip"))
    fail = sum(1 for r in report if r["status"] == "fail")
    print(f"ALL DONE ok+skip={ok} fail={fail}", flush=True)
    if fail and not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
