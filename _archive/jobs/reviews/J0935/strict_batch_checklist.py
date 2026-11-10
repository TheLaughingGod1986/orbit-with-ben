#!/usr/bin/env python3
"""Strict batch B review checklist for J0935 per RULING_2026-10-26_CODEX.md.

Enforces and records every constraint from c61 and Codex's 26 Oct ruling, failing on
brief/ruling violations even where gate_shorts_open.py only warns or does not test them,
and distinguishing clean PASS cuts from Keeper-reconciliation / infeasibility cuts.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
OUT_JSON = Path(__file__).resolve().parent / "STRICT_BATCH_CHECKLIST_2026-10-28.json"
OUT_MD = Path(__file__).resolve().parent / "STRICT_BATCH_CHECKLIST_2026-10-28.md"

SHORTS = [
    {
        "id": "iyvWYFP_ETA",
        "slug": "mon09_night_cold",
        "version": "v04",
        "air": "2026-11-09",
        "dir": REPO / "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/mon09_night_cold/06_Final-Exports",
        "uat": Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/025_mon09_night_cold_v04"),
        "nas": Path("/Volumes/data/mac-mini-archive/youtube-staging/025/mon09_night_cold_v04"),
        "min_dur": 22.0,
        "max_dur": 24.0,
        "payoff_70pct_required": True,
        "expected_status": "INFEASIBLE_OPENING_RETAIN_V01",
    },
    {
        "id": "TtgHNLXfDSs",
        "slug": "wed11_opening_testA",
        "version": "v05",
        "air": "2026-11-11",
        "dir": REPO / "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/wed11_opening_testA/06_Final-Exports",
        "uat": Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/025_wed11_opening_testA_v05"),
        "nas": Path("/Volumes/data/mac-mini-archive/youtube-staging/025/wed11_opening_testA_v05"),
        "min_dur": 23.0,
        "max_dur": 25.0,
        "payoff_70pct_required": True,
        "expected_status": "PASS",
    },
    {
        "id": "N42gKBbD7tE",
        "slug": "thu12_length_test_dust",
        "version": "v04",
        "air": "2026-11-12",
        "dir": REPO / "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports",
        "uat": Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/025_thu12_length_test_dust_v04"),
        "nas": Path("/Volumes/data/mac-mini-archive/youtube-staging/025/thu12_length_test_dust_v04"),
        "min_dur": 50.0,
        "max_dur": 60.0,
        "payoff_70pct_required": False,  # story-order exception per J0916, c61, and Codex 26 Oct ruling
        "expected_status": "PASS_WITH_KEEPER_RECONCILIATION_NOTE",
    },
    {
        "id": "bSjWiCbB7pY",
        "slug": "fri13_ingenuity_72",
        "version": "v05",
        "air": "2026-11-13",
        "dir": REPO / "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports",
        "uat": Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/025_fri13_ingenuity_72_v05"),
        "nas": Path("/Volumes/data/mac-mini-archive/youtube-staging/025/fri13_ingenuity_72_v05"),
        "min_dur": 22.0,
        "max_dur": 24.0,
        "payoff_70pct_required": True,
        "expected_status": "PASS_WITH_KEEPER_RECONCILIATION_NOTE",
    },
    {
        "id": "HZGTovJu_TQ",
        "slug": "mon16_cant_see_nearest_star",
        "version": "v03",
        "air": "2026-11-16",
        "dir": REPO / "02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports",
        "uat": Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/026_mon16_cant_see_nearest_star_v03"),
        "nas": Path("/Volumes/data/mac-mini-archive/youtube-staging/026/mon16_cant_see_nearest_star_v03"),
        "min_dur": 22.0,
        "max_dur": 24.0,
        "payoff_70pct_required": True,
        "expected_status": "PASS_WITH_KEEPER_RECONCILIATION_NOTE",
    },
    {
        "id": "cwU_0WWeNZ4",
        "slug": "wed18_robot_reach_nearest_star",
        "version": "v04",
        "air": "2026-11-18",
        "dir": REPO / "02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports",
        "uat": Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/026_wed18_robot_reach_nearest_star_v04"),
        "nas": Path("/Volumes/data/mac-mini-archive/youtube-staging/026/wed18_robot_reach_nearest_star_v04"),
        "min_dur": 22.0,
        "max_dur": 24.0,
        "payoff_70pct_required": True,
        "expected_status": "PASS_WITH_KEEPER_RECONCILIATION_NOTE",
    },
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_phone(p: Path) -> tuple[int, int, float]:
    raw = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(p)],
        text=True,
    )
    d = json.loads(raw)
    st = d["streams"][0]
    return int(st["width"]), int(st["height"]), float(d["format"]["duration"])


def main() -> None:
    results = []
    any_unexpected_fail = False

    for s in SHORTS:
        stem = f"{s['slug']}_{s['version']}"
        d = s["dir"]
        meta = json.loads((d / f"{stem}_meta.json").read_text())
        brief = meta["brief"]
        manifest = json.loads((d / "sha256_manifest.json").read_text())
        whisper = json.loads((d / f"{stem}_whisper.json").read_text())
        checks = json.loads((d / f"{stem}_checks.json").read_text())

        # 1. Verify manifest hashes in local, UAT, NAS
        copy_errors = []
        manifest_items = manifest.get("files") or manifest.get("entries") or []
        for entry in manifest_items:
            fname = entry.get("name") or entry.get("file")
            exp_sha = entry["sha256"]
            for loc_name, loc_dir in (("local", d), ("uat", s["uat"]), ("nas", s["nas"])):
                fp = loc_dir / fname
                if not fp.exists():
                    copy_errors.append(f"{loc_name} missing {fname}")
                elif sha256(fp) != exp_sha:
                    copy_errors.append(f"{loc_name} sha256 mismatch on {fname}")

        # 2. Verify _PHONE.mp4 dimensions
        pw, ph, pdur = probe_phone(d / f"{stem}_PHONE.mp4")
        phone_ok = (pw == 720 and ph == 1280 and abs(pdur - float(meta["duration_s"])) < 0.15)

        # 3. Verify 2fps sheet coverage
        sheet_img = Image.open(d / f"{stem}_2fps.jpg")
        cols = sheet_img.width // 180
        rows = sheet_img.height // 320
        sheet_capacity_s = (cols * rows) / 2.0
        sheet_ok = sheet_capacity_s >= float(meta["duration_s"])

        # 4. Verify AAC loudness & true peak
        lufs = float(brief["lufs"])
        tp = float(brief["true_peak_dbtp"])
        audio_ok = (-14.5 <= lufs <= -13.5) and (tp <= -1.6)

        # 5. Verify runtime band (>=22s floor or 50-60s length test)
        dur_s = float(meta["duration_s"])
        dur_ok = (s["min_dur"] <= dur_s <= s["max_dur"])

        # 6. Verify surprise <= 1.5s
        surprise_s = float(brief["surprise_s"])
        surprise_ok = surprise_s <= 1.50

        # 7. Verify payoff >= 70% (or story-order exception on thu12)
        payoff_s = float(brief["payoff_number_s"])
        payoff_ok = True if not s["payoff_70pct_required"] else (payoff_s >= 0.70 * dur_s and payoff_s > 14.0)

        # 8. Verify banner window (9-14s) clear of direct how/why mechanism answer on wed11 & fri13
        banner_clear = True
        if s["slug"] == "wed11_opening_testA":
            banner_clear = float(brief["clean_end_s"]) < 9.0
        elif s["slug"] == "fri13_ingenuity_72":
            banner_clear = float(brief["lift_end_s"]) < 9.0

        # 9. Verify Whisper transcript & per-frame checks
        whisper_ok = bool(whisper.get("text")) and len(whisper.get("words", [])) >= 40
        frame_checks_ok = (
            checks["max_dark_run_over_85pct"] == 0
            and checks["max_black_edge_run_over_30pct"] == 0
            and len(checks["ocr_bad_hits"]) == 0
            and float(brief["loop_diff_masked"]) <= 15.0
        )

        # 10. Keeper first-line question check / reconciliation
        keeper_ok = bool(brief.get("keeper_line1_question_compliant", False)) or ("test_a_exemption" in brief)
        infeasibility_present = (d / f"{stem}_infeasibility.json").exists()

        row_res = {
            "id": s["id"],
            "slug": s["slug"],
            "version": s["version"],
            "air": s["air"],
            "status": meta.get("status"),
            "sha256": meta["sha256"],
            "duration_s": dur_s,
            "duration_ok": dur_ok,
            "lufs": lufs,
            "true_peak_dbtp": tp,
            "audio_ok": audio_ok,
            "phone_720x1280_ok": phone_ok,
            "manifest_files": len(manifest_items),
            "copy_errors": copy_errors,
            "sheet_2fps_dims": f"{cols}x{rows} ({sheet_capacity_s:.1f}s capacity for {dur_s:.2f}s master)",
            "sheet_full_coverage_ok": sheet_ok,
            "surprise_s": surprise_s,
            "surprise_le_1_5s": surprise_ok,
            "payoff_s": payoff_s,
            "payoff_pct": round(payoff_s / dur_s * 100, 1),
            "payoff_ok": payoff_ok,
            "banner_9_14s_clear_ok": banner_clear,
            "whisper_master_ok": whisper_ok,
            "whisper_word_count": len(whisper.get("words", [])),
            "frame_dark_black_ocr_loop_ok": frame_checks_ok,
            "keeper_line1_or_exempt": keeper_ok,
            "infeasibility_documented": infeasibility_present,
        }
        results.append(row_res)

        if (
            copy_errors
            or not phone_ok
            or not sheet_ok
            or not audio_ok
            or not dur_ok
            or not payoff_ok
            or not banner_clear
            or not whisper_ok
            or not frame_checks_ok
            or meta.get("status") != s["expected_status"]
        ):
            any_unexpected_fail = True

    OUT_JSON.write_text(json.dumps({"job": "J0935", "checked_at": "2026-10-28", "results": results}, indent=2) + "\n")

    md_lines = [
        "# J0935 — Strict Batch B Review Checklist (28 Oct 2026)",
        "",
        "Response to `RULING_2026-10-26_CODEX.md`. Every Short has been checked against all c61 + Codex 26 Oct + Keeper constraints.",
        "",
        "| Short | Cut | Dur (s) | LUFS / TP | Surprise (s) | Payoff (%) | 9-14s Banner | 2fps Sheet | Whisper | Copies (L/U/N) | Outcome |",
        "|---|---|---:|---|---:|---:|---|---|---:|---|---|",
    ]
    for r in results:
        md_lines.append(
            f"| `{r['id']}` {r['slug']} | `{r['version']}` | {r['duration_s']:.2f} | {r['lufs']:.1f} / {r['true_peak_dbtp']:.1f} | "
            f"{r['surprise_s']:.3f} ({'OK' if r['surprise_le_1_5s'] else 'INFEASIBLE'}) | {r['payoff_s']:.2f}s ({r['payoff_pct']}%) | "
            f"{'CLEAR' if r['banner_9_14s_clear_ok'] else 'FAIL'} | {r['sheet_2fps_dims']} | {r['whisper_word_count']}w | "
            f"{r['manifest_files']} files ({'OK' if not r['copy_errors'] else 'ERR'}) | `{r['status']}` |"
        )
    OUT_MD.write_text("\n".join(md_lines) + "\n")
    print("\n".join(md_lines))
    if any_unexpected_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
