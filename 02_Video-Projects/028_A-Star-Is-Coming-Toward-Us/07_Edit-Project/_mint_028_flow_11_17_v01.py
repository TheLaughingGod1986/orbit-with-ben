#!/usr/bin/env python3
"""028 Gliese 710 Flow Veo beats, SHOT_LIST_v01 rows 11 and 17 (J0850, Chief price PASS).

Flow UI via CDP :9222 (benoats@googlemail.com):
- r11_night_road: Veo 3.1 - Quality (100 cr try-1 / 259 cr expected), 1 take, 8 s
- r17_pitch: Veo 3.1 - Fast (10 cr try-1 / 20 cr expected), 1 take, 8 s
Text-to-video (scenery_only=True, no Orbit). Silent picture only.
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
TRY1 = {"Quality": 100, "Fast": 10}
BUFFER = 3000

ROWS = [
    {
        "row": 11,
        "plate_id": "r11_night_road",
        "id": "night_road_veo_v01",
        "quality": "Quality",
        "model": "Veo 3.1 - Quality",
        "prompt": (
            "Photorealistic cinema shot: a long straight empty two-lane country road at night. "
            "One car's warm headlights far down the road come straight toward the camera and slowly grow brighter "
            "as the car approaches along the asphalt. Dark open fields on both sides under a dark night sky. "
            "No brands, no number plates, no text, no people, no road signs, no buildings with signs. "
            "Continuous smooth motion through the final frame. No robot, no cartoon. Silent."
        ),
    },
    {
        "row": 17,
        "plate_id": "r17_pitch",
        "id": "football_pitch_veo_v01",
        "quality": "Fast",
        "model": "Veo 3.1 - Fast",
        "prompt": (
            "Photorealistic cinema shot: an empty green grass football pitch at dusk, seen from a high wide angle "
            "with a gentle slow aerial drift across the turf. Crisp white touchlines and centre circle only. "
            "No crowds, no players, no club colours, no banners, no text, no logos. "
            "Natural twilight fading, nothing glowing. Continuous smooth camera drift through the final frame. "
            "No robot, no cartoon. Silent."
        ),
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def sheet_6frame(mp4: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f"_tmp_{dest.stem}"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    dur = float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(mp4)],
            text=True,
        ).strip()
        or 8.0
    )
    frames = []
    for i, t in enumerate(dur * k for k in (0.05, 0.2, 0.4, 0.6, 0.8, 0.95)):
        f = tmp / f"f{i}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-vf", "scale=320:-2", str(f)],
            check=True,
        )
        frames.append(f)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *[x for f in frames for x in ("-i", str(f))], "-filter_complex", "hstack=inputs=6", "-frames:v", "1", str(dest)],
        check=True,
    )
    shutil.rmtree(tmp, ignore_errors=True)


def harvest_project_mp4(page, flow, mint006, project_url: str, dest: Path, wait_s: int = 420) -> None:
    captured: list[bytes] = []

    def on_resp(resp) -> None:
        try:
            u = (resp.url or "").lower()
            ct = (resp.headers.get("content-type") or "").lower()
            if resp.status == 200 and (
                "flow-content.google/video" in u
                or "googlevideo.com" in u
                or "videoplayback" in u
                or "video/mp4" in ct
            ):
                body = resp.body()
                if body and len(body) > 400_000 and b"ftyp" in body[:64]:
                    captured.append(body)
        except Exception:
            pass

    page.on("response", on_resp)
    try:
        if project_url not in (page.url or ""):
            page.goto(project_url, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3000)
            flow.dismiss_banners(page)
        t0 = time.time()
        last_reload = t0
        while time.time() - t0 < wait_s:
            if dest.exists() and dest.stat().st_size >= 400_000:
                return
            if captured:
                dest.write_bytes(max(captured, key=len))
                return
            gen_thumbs = page.locator('img[alt*="Generated video" i]').count()
            vids = page.locator("video").count()
            elapsed = time.time() - t0
            print(f"  harvest poll gen_thumbs={gen_thumbs} vids={vids} elapsed={elapsed:.0f}s", flush=True)
            if gen_thumbs > 0 or vids > 0 or elapsed >= 45:
                body = mint006.hover_fetch(page)
                if body and len(body) >= 400_000:
                    dest.write_bytes(body)
                    return
                if captured:
                    dest.write_bytes(max(captured, key=len))
                    return
            if time.time() - last_reload >= 60 and gen_thumbs == 0:
                try:
                    page.reload(wait_until="domcontentloaded", timeout=60_000)
                    page.wait_for_timeout(3000)
                    flow.dismiss_banners(page)
                    last_reload = time.time()
                except Exception as exc:
                    print(f"  reload warn: {exc}", flush=True)
            page.wait_for_timeout(8000)
    finally:
        try:
            page.remove_listener("response", on_resp)
        except Exception:
            pass
    raise RuntimeError(f"harvest timeout {wait_s}s project={project_url}")


def record_flow_balance(credits: int | None, note: str) -> None:
    if credits is None:
        return
    ai_spend = REPO / "scripts/ai_spend.py"
    if not ai_spend.exists():
        return
    subprocess.run(
        [sys.executable, str(ai_spend), "record", "--pool", "flow", "--left", str(credits), "--by", "gemini", "--note", note],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=30,
    )


def main() -> int:
    sys.path.insert(0, str(HOS_REPO / "04_Audio/tools"))
    mint006 = load_mod(
        "hos006_mint",
        HOS_REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py",
    )
    import orbit_flow_veo_ui as flow
    import orbit_gemini_veo as veo
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    SHEETS.mkdir(parents=True, exist_ok=True)

    report = {
        "startedAt": now(),
        "job": "J0850",
        "film": "028",
        "engine": "flow-cdp-9222",
        "request": "Chief J0850 price PASS (Claude, acting Chief, 22 Oct 2026): r11_night_road 1 Quality + r17_pitch 1 Fast",
        "rows": [],
        "balance_reads": [],
    }
    if REPORT.exists():
        old = json.loads(REPORT.read_text())
        report["rows"] = [x for x in old.get("rows", []) if x.get("status") in ("ok", "skip")]
        report["balance_reads"] = old.get("balance_reads", [])

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        page = mint006.flow_page(browser, flow)
        credits, account = mint006.read_account(page)
        print(f"GATE account={account} credits={credits}", flush=True)
        if account != REQUIRED or (account and FORBIDDEN in account):
            raise SystemExit(f"STOP wrong Flow account: {account}")
        if credits is None:
            raise SystemExit("STOP Flow credits unreadable")
        report["balance_reads"].append({"at": now(), "credits": credits, "when": "start"})
        REPORT.write_text(json.dumps(report, indent=2) + "\n")

        for r in ROWS:
            dest = OUT / f"{r['id']}.mp4"
            sh6 = SHEETS / f"{r['id']}_6frame.jpg"
            sh3x2 = SHEETS / f"{r['id']}_sheet.jpg"
            if dest.exists() and dest.stat().st_size > 400_000:
                if not sh6.exists():
                    sheet_6frame(dest, sh6)
                if not sh3x2.exists():
                    mint006.contact_sheet(dest, sh3x2)
                report["rows"] = [x for x in report["rows"] if x["id"] != r["id"]]
                report["rows"].append(
                    {
                        "row": r["row"],
                        "plate_id": r["plate_id"],
                        "id": r["id"],
                        "quality": r["quality"],
                        "model": r["model"],
                        "status": "skip",
                        "note": "take already exists; no second take without Chief",
                        "file": str(dest.relative_to(HERE.parent)),
                        "sheet_6frame": str(sh6.relative_to(HERE.parent)),
                        "sheet_3x2": str(sh3x2.relative_to(HERE.parent)),
                        "bytes": dest.stat().st_size,
                        "duration_s": round(mint006.duration(dest), 3),
                        "sha256": mint006.sha256(dest),
                    }
                )
                REPORT.write_text(json.dumps(report, indent=2) + "\n")
                continue

            cost = TRY1[r["quality"]]
            credits, account = mint006.read_account(page)
            if credits is None or credits - cost < BUFFER:
                raise SystemExit(f"STOP gate: credits={credits} cost={cost} buffer={BUFFER}")
            if mint006.UNPAID_RE.search(mint006.body_text(page)):
                raise SystemExit(f"STOP billing banner before {r['id']}")

            print(f"\n=== row {r['row']} ({r['plate_id']}) {r['model']} ~{cost} cr (live={credits}) ===", flush=True)
            os.environ["ORBIT_FLOW_VEO_MODEL"] = r["model"]
            os.environ["OWB_AGENT"] = "gemini"
            t0 = time.time()
            entry = {
                "row": r["row"],
                "plate_id": r["plate_id"],
                "id": r["id"],
                "quality": r["quality"],
                "model": r["model"],
                "prompt": r["prompt"],
                "credits_before": credits,
                "submitted_at": now(),
                "status": "submitting",
            }
            info = (
                flow.generate_clip(
                    page,
                    r["prompt"],
                    dest,
                    model=r["model"],
                    timeout_s=600,
                    scenery_only=True,
                    attempts=1,
                    reuse_project=False,
                )
                or {}
            )
            entry["project_url"] = info.get("project_url") or info.get("url") or ""
            if not dest.exists() or dest.stat().st_size < 400_000:
                if "/project/" not in entry["project_url"]:
                    raise RuntimeError(f"no mp4 and no project URL: {entry['project_url']!r}")
                print(f"  gallery harvest {entry['project_url']}", flush=True)
                harvest_project_mp4(page, flow, mint006, entry["project_url"], dest, wait_s=420)

            veo.strip_audio(dest)
            sheet_6frame(dest, sh6)
            mint006.contact_sheet(dest, sh3x2)
            after, account = mint006.read_account(page)
            ui_drop = max(0, credits - after) if after is not None else cost
            used = max(ui_drop, cost) if ui_drop in (0, cost) else cost
            entry.update(
                status="ok",
                wall_seconds=round(time.time() - t0, 1),
                file=str(dest.relative_to(HERE.parent)),
                sheet_6frame=str(sh6.relative_to(HERE.parent)),
                sheet_3x2=str(sh3x2.relative_to(HERE.parent)),
                bytes=dest.stat().st_size,
                duration_s=round(mint006.duration(dest), 3),
                sha256=mint006.sha256(dest),
                freeze_events_0p8s=mint006.freeze_events(dest),
                credits_after=after,
                credits_used=used,
                credits_ui_drop=ui_drop,
                account=account,
                finished_at=now(),
            )
            report["rows"] = [x for x in report["rows"] if x["id"] != r["id"]]
            report["rows"].append(entry)
            report["balance_reads"].append({"at": now(), "credits": after, "after": r["id"]})
            REPORT.write_text(json.dumps(report, indent=2) + "\n")
            print(
                f"  -> OK {dest.name} ({entry['duration_s']}s, {entry['bytes']}B) used={used} (ui_drop={ui_drop}) balance={after}",
                flush=True,
            )

        end_credits, _ = mint006.read_account(page)
        report["finishedAt"] = now()
        report["credits_end"] = end_credits
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
        record_flow_balance(
            end_credits,
            f"J0850 OWB 028 Flow Veo mint done (r11_night_road Quality + r17_pitch Fast, 110 cr priced)",
        )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
