#!/usr/bin/env python3
"""Neutron Star Part 01 — Omni Flash plates via Flow UI."""
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
import orbit_gemini_veo as veo  # noqa: E402
from _flow_omni_select import configure_omni, read_prompt_pill, OMNI_LABELS  # noqa: E402

EP = REPO / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star"
PLATES = json.loads((HERE / "parts/part-01_omni_plates_v01.json").read_text())
OUT = EP / "04_Generated-Clips/01_Raw/part-01"

LOCK = (
    " Hard lock: exactly ONE Orbit robot in frame when Orbit is called for — never two, never a second face. "
    " Cream eyes with dark pupils. One soft underside glow. Orbit is IN the scene — banks/turns/reacts, not a sticker. "
    " Target length about 8 seconds. Fully animated continuous motion — never freeze. "
    " No logo, no title, no HUD, no brand sting, no subscribe graphic."
)
NO_ORBIT = (
    " HARD: do not generate Orbit, any robot, any spacecraft character, any logo, any title. "
    " Strange picture only."
)


def generate_omni(page, prompt: str, dest: Path, *, configure: bool, attach_orbit: bool, timeout_s: int = 700) -> dict:
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
    if attach_orbit:
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
    full = prompt + (LOCK if attach_orbit else NO_ORBIT)
    flow.set_prompt(page, full)
    if attach_orbit and flow._prompt_attachment_count(page) < 1:
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
    only = {a for a in sys.argv[1:] if not a.startswith("--")}
    headed = "--headed" in sys.argv
    from playwright.sync_api import sync_playwright

    report = []
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=headed, profile=flow.profile_path(None))
        configured = False
        try:
            for plate in PLATES["plates"]:
                if only and plate["id"] not in only and plate["slug"] not in only:
                    continue
                dest = OUT / plate["file"]
                if dest.exists() and dest.stat().st_size > 500_000:
                    print(f"SKIP {dest.name}", flush=True)
                    report.append({"id": plate["id"], "status": "skip", "file": dest.name})
                    continue
                print(f"\n=== Part01 {plate['id']} {plate['slug']} orbit={plate.get('orbit')} ===", flush=True)
                try:
                    meta = generate_omni(
                        page,
                        plate["prompt"],
                        dest,
                        configure=not configured,
                        attach_orbit=bool(plate.get("orbit", True)),
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
        finally:
            ctx.close()
    (HERE / "parts/part-01_omni_gen_report_v01.json").write_text(json.dumps(report, indent=2) + "\n")
    ok = sum(1 for r in report if r["status"] in ("ok", "skip"))
    fail = sum(1 for r in report if r["status"] == "fail")
    print(f"ALL DONE ok+skip={ok} fail={fail}", flush=True)
    if fail and not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
