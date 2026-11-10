#!/usr/bin/env python3
"""Neutron Star Part 05 v01 — Omni Flash via Gemini API first, Flow Playwright backup."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path("/Users/ben/code/Orbit-YouTube")
TOOLS = REPO / "04_Audio/tools"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import orbit_gemini_omni as omni  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

EP = REPO / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star"
IDENTITY = (
    REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
)
PLATES_JSON = HERE / "parts/part-05_omni_plates_cursor_v01.json"
PLATES = json.loads(PLATES_JSON.read_text())
OUT = EP / "04_Generated-Clips/01_Raw/part-05"
REPORT = HERE / "parts/part-05_omni_gen_report_cursor_v01.json"
PLAYWRIGHT_PY = Path("/usr/bin/python3")
PLAYWRIGHT_GEN = HERE / "_gen_part01_omni_cursor_v01.py"
ENV_CANDIDATES = [
    HERE / ".env",
    TOOLS / ".env",
    REPO / "02_Video-Projects/005_The-Last-Star-In-The-Universe/07_Edit-Project/.env",
]


def _is_billing_dead(exc: BaseException) -> bool:
    text = str(exc).lower()
    return any(
        s in text
        for s in (
            "prepayment credits are depleted",
            "too_many_requests",
            "429",
            "resource_exhausted",
            "billing",
        )
    )


def _run_playwright_backup(ids: list[str]) -> None:
    if not ids:
        return
    print(f"\n=== PLAYWRIGHT BACKUP ids={' '.join(ids)} ===", flush=True)
    env = os.environ.copy()
    env["ORBIT_PLATES_JSON"] = str(PLATES_JSON)
    env["ORBIT_OUT_DIR"] = str(OUT)
    subprocess.run(
        [str(PLAYWRIGHT_PY), "-u", str(PLAYWRIGHT_GEN), *ids],
        cwd=str(HERE),
        check=False,
        env=env,
    )


def main() -> None:
    only = {a for a in sys.argv[1:] if not a.startswith("--")}
    no_backup = "--no-backup" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    env_files = [p for p in ENV_CANDIDATES if p.exists()]
    client = veo.make_client(*env_files)
    report = []
    backup_ids: list[str] = []
    api_dead = False

    for plate in PLATES["plates"]:
        if only and plate["id"] not in only and plate["slug"] not in only:
            continue
        dest = OUT / plate["file"]
        if plate.get("keep") or (dest.exists() and dest.stat().st_size > 200_000):
            print(f"SKIP {dest.name}", flush=True)
            report.append({"id": plate["id"], "status": "skip", "file": dest.name})
            continue
        if api_dead:
            backup_ids.append(plate["id"])
            continue
        print(f"\n=== API Omni {plate['id']} {plate['slug']} ===", flush=True)
        try:
            start = plate.get("start_frame")
            orbit_ref = (HERE / start) if start else None
            if orbit_ref is not None and not orbit_ref.exists():
                orbit_ref = EP / start
            ident = IDENTITY if plate.get("orbit") else None
            prompt = (
                plate["prompt"]
                + " EMPTY BLACK VACUUM: zero pinprick stars, zero grain, zero starfield, zero white specks. Only the named subjects."
            )
            if plate.get("orbit"):
                prompt += (
                    " IDENTITY LOCK: same Orbit as the start frame — matte orange sphere, glossy black visor FACEPLATE"
                    " as the whole face, two cream circular eyes with dark pupils, stubby orange arms with dark"
                    " three-finger hands, single antenna with glowing bulb, one small underside glow."
                    " Not a cheap toy, not eyes on a blank ball, not a glowing yellow belly, no HUD, no drawn cartoon mouth."
                    " INTERACT with the scene — bank, drift, brace, tip — not a static hover looking around."
                )
            meta = omni.generate_omni_clip(
                client,
                prompt,
                dest,
                orbit_ref=orbit_ref,
                identity_ref=ident,
            )
            print(f"SAVED {dest.name} {meta}", flush=True)
            report.append({"id": plate["id"], "status": "ok", "file": dest.name, **meta})
        except Exception as e:
            print(f"FAIL {plate['id']}: {e}", flush=True)
            report.append({"id": plate["id"], "status": "fail", "error": str(e), "engine": "gemini-api-omni"})
            backup_ids.append(plate["id"])
            if _is_billing_dead(e):
                print("API billing dead — remaining plates go to Playwright backup.", flush=True)
                api_dead = True

    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    if backup_ids and not no_backup:
        _run_playwright_backup(backup_ids)
    ok_files = [
        p["file"]
        for p in PLATES["plates"]
        if (not only or p["id"] in only or p["slug"] in only)
        and ((OUT / p["file"]).exists() and (OUT / p["file"]).stat().st_size > 200_000 or p.get("keep"))
    ]
    missing = [
        p["id"]
        for p in PLATES["plates"]
        if (not only or p["id"] in only or p["slug"] in only)
        and not p.get("keep")
        and not ((OUT / p["file"]).exists() and (OUT / p["file"]).stat().st_size > 200_000)
    ]
    print(f"ALL DONE have={len(ok_files)} missing={missing}", flush=True)
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
