#!/usr/bin/env python3
"""028 Gliese 710 Flow Veo Fast retake for r17_pitch (J0855, Chief FIX ruling on J0850).

One Fast retake (10 cr): an empty grass pitch at dusk, the camera gliding low and slow
over the centre circle towards halfway, no goals or nets in frame, stands soft and distant,
no text/logos/people. KEEP it if clean.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
HOS_REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
OUT = HERE.parent / "04_Generated-Clips/01_Raw/veo_v01"
SHEETS = OUT / "sheets"
REPORT = HERE / "flow_gen_report_11_17_v01.json"
CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRED = "benoats@googlemail.com"
FORBIDDEN = "benoats86@gmail.com"
COST = 10
BUFFER = 3000

PROMPT = (
    "Photorealistic cinema shot: an empty green grass football pitch at dusk, "
    "the camera gliding low and slow over the centre circle towards the halfway line. "
    "Crisp white centre circle and halfway line on grass turf only. "
    "No goals or goal nets anywhere in frame. Stands soft and distant in the background. "
    "No text, no logos, no banners, no people, no players, no club colours. "
    "Natural twilight fading, nothing glowing. Continuous smooth low camera glide through the final frame. "
    "No robot, no cartoon. Silent."
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    sys.path.insert(0, str(HOS_REPO / "04_Audio/tools"))
    mint006 = load_mod(
        "hos006_mint",
        HOS_REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py",
    )
    mint028 = load_mod("mint028", HERE / "_mint_028_flow_11_17_v01.py")
    import orbit_flow_veo_ui as flow
    import orbit_gemini_veo as veo
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    SHEETS.mkdir(parents=True, exist_ok=True)

    dest_v02 = OUT / "football_pitch_veo_v02.mp4"
    dest_v01 = OUT / "football_pitch_veo_v01.mp4"
    backup_v01 = OUT / "football_pitch_veo_v01_take1_d224e044.mp4"
    sh6_v02 = SHEETS / "football_pitch_veo_v02_6frame.jpg"
    sh3x2_v02 = SHEETS / "football_pitch_veo_v02_sheet.jpg"
    sh6_v01 = SHEETS / "football_pitch_veo_v01_6frame.jpg"
    sh3x2_v01 = SHEETS / "football_pitch_veo_v01_sheet.jpg"

    if dest_v02.exists() and dest_v02.stat().st_size > 400_000:
        print(f"SKIP: {dest_v02} already exists ({dest_v02.stat().st_size} B)")
        return 0

    if dest_v01.exists() and not backup_v01.exists():
        shutil.copy2(dest_v01, backup_v01)

    report = json.loads(REPORT.read_text()) if REPORT.exists() else {"rows": [], "balance_reads": []}

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        page = mint006.flow_page(browser, flow)
        credits, account = mint006.read_account(page)
        print(f"GATE account={account} credits={credits}", flush=True)
        if account != REQUIRED or (account and FORBIDDEN in account):
            raise SystemExit(f"STOP wrong Flow account: {account}")
        if credits is None or credits - COST < BUFFER:
            raise SystemExit(f"STOP gate: credits={credits} cost={COST} buffer={BUFFER}")
        if mint006.UNPAID_RE.search(mint006.body_text(page)):
            raise SystemExit("STOP billing banner before football_pitch_veo_v02")

        os.environ["ORBIT_FLOW_VEO_MODEL"] = "Veo 3.1 - Fast"
        os.environ["OWB_AGENT"] = "gemini"
        t0 = time.time()
        info = (
            flow.generate_clip(
                page,
                PROMPT,
                dest_v02,
                model="Veo 3.1 - Fast",
                timeout_s=600,
                scenery_only=True,
                attempts=1,
                reuse_project=False,
            )
            or {}
        )
        project_url = info.get("project_url") or info.get("url") or ""
        if not dest_v02.exists() or dest_v02.stat().st_size < 400_000:
            if "/project/" not in project_url:
                raise RuntimeError(f"no mp4 and no project URL: {project_url!r}")
            print(f"  gallery harvest {project_url}", flush=True)
            mint028.harvest_project_mp4(page, flow, mint006, project_url, dest_v02, wait_s=420)

        veo.strip_audio(dest_v02)
        mint028.sheet_6frame(dest_v02, sh6_v02)
        mint006.contact_sheet(dest_v02, sh3x2_v02)

        # Promote clean retake to football_pitch_veo_v01.mp4 as the active r17_pitch plate
        shutil.copy2(dest_v02, dest_v01)
        shutil.copy2(sh6_v02, sh6_v01)
        shutil.copy2(sh3x2_v02, sh3x2_v01)

        after, account = mint006.read_account(page)
        ui_drop = max(0, credits - after) if after is not None else COST
        used = max(ui_drop, COST) if ui_drop in (0, COST) else COST

        entry = {
            "row": 17,
            "plate_id": "r17_pitch",
            "id": "football_pitch_veo_v02",
            "active_file": str(dest_v01.relative_to(HERE.parent)),
            "take": 2,
            "quality": "Fast",
            "model": "Veo 3.1 - Fast",
            "prompt": PROMPT,
            "credits_before": credits,
            "submitted_at": now(),
            "status": "ok",
            "project_url": project_url,
            "wall_seconds": round(time.time() - t0, 1),
            "file": str(dest_v02.relative_to(HERE.parent)),
            "sheet_6frame": str(sh6_v02.relative_to(HERE.parent)),
            "sheet_3x2": str(sh3x2_v02.relative_to(HERE.parent)),
            "bytes": dest_v02.stat().st_size,
            "duration_s": round(mint006.duration(dest_v02), 3),
            "sha256": mint006.sha256(dest_v02),
            "freeze_events_0p8s": mint006.freeze_events(dest_v02),
            "credits_after": after,
            "credits_used": used,
            "credits_ui_drop": ui_drop,
            "account": account,
            "finished_at": now(),
        }
        report["rows"].append(entry)
        report["balance_reads"].append({"at": now(), "credits": after, "after": "football_pitch_veo_v02"})
        report["retake_J0855_finishedAt"] = now()
        report["credits_end"] = after
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
        mint028.record_flow_balance(
            after,
            "J0855 OWB 028 r17_pitch Fast retake (10 cr, no goal net)",
        )
        print(
            f"  -> OK {dest_v02.name} ({entry['duration_s']}s, {entry['bytes']}B, sha={entry['sha256'][:12]}) used={used} balance={after}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
