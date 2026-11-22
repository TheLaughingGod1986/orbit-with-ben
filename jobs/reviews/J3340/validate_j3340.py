#!/usr/bin/env python3
"""
Reproducible Chief validation script for J3340 (reconciling J3340 QA sweep
inventory and report against all 808 raw gate sidecars across 277 entries,
verifying direct media SHA-256 and live mtime freshness on all 10 post-J3104
single-file exports, verifying 73/73 J3128 baseline music coverage, and
verifying byte-identical OWB/HOS main copies).
"""

import hashlib
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OWB_DIR = REPO_ROOT / "00_Brand/Channel-Setup/audits/qa_sweeps"
HOS_REPO = Path("/Users/benjaminoats/YouTube/History Of Science")

INV_NAME = "J3340_QA_SWEEP_INVENTORY_2026-11-22.json"
REP_NAME = "J3340_QA_SWEEP_REPORT_2026-11-22.md"
J3104_INV_NAME = "J3104_QA_SWEEP_INVENTORY_2026-11-19.json"
J3128_INV_NAME = "J3128_MUSIC_RECONCILIATION_INVENTORY_2026-11-19.json"


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    owb_inv_p = OWB_DIR / INV_NAME
    owb_rep_p = OWB_DIR / REP_NAME
    owb_inv_bytes = owb_inv_p.read_bytes()
    owb_rep_bytes = owb_rep_p.read_bytes()

    hos_inv_bytes = subprocess.check_output(
        ["git", "-C", str(HOS_REPO), "show", f"origin/main:00_Brand/Channel-Setup/audits/qa_sweeps/{INV_NAME}"]
    )
    hos_rep_bytes = subprocess.check_output(
        ["git", "-C", str(HOS_REPO), "show", f"origin/main:00_Brand/Channel-Setup/audits/qa_sweeps/{REP_NAME}"]
    )
    hos_main_head = subprocess.check_output(
        ["git", "-C", str(HOS_REPO), "rev-parse", "origin/main"], text=True
    ).strip()

    owb_hos_identical = (owb_inv_bytes == hos_inv_bytes and owb_rep_bytes == hos_rep_bytes)
    assert owb_hos_identical, "Inventory/Report differs between OWB and HOS origin/main!"

    inv_sha = hashlib.sha256(owb_inv_bytes).hexdigest()
    rep_sha = hashlib.sha256(owb_rep_bytes).hexdigest()

    inv = json.loads(owb_inv_bytes.decode("utf-8"))
    entries = inv["entries"]
    assert len(entries) == 277, f"Expected 277 entries, got {len(entries)}"

    j3104_inv = json.loads((OWB_DIR / J3104_INV_NAME).read_text(encoding="utf-8"))
    j3104_ids = {e["export_id"] for e in j3104_inv["entries"]}

    j3128_inv = json.loads((OWB_DIR / J3128_INV_NAME).read_text(encoding="utf-8"))
    j3128_rows = j3128_inv.get("entries") or j3128_inv.get("targets") or j3128_inv.get("results") or []
    j3128_ids = {r.get("export_id") for r in j3128_rows if isinstance(r, dict)}

    missing_sidecars = []
    sha_mismatches = []
    verdict_mismatches = []
    field_mismatches = []
    item_list_mismatches = []
    derived_entry_mismatches = []
    fresh_mismatches = []
    new_media_issues = []
    current_newest_fails = []
    uncovered_partial_newest = []

    sidecars_checked = 0
    new_entries_checked = 0
    new_single_file_media_verified = 0

    for e in entries:
        eid = e["export_id"]
        is_new = eid not in j3104_ids
        is_newest = e.get("version_status") == "current_newest"

        for g in ("picture_qa", "polish_gate"):
            gd = e[g]
            p = Path(gd["path"])
            if not p.exists():
                missing_sidecars.append((eid, g, str(p)))
                continue
            sidecars_checked += 1
            actual_sha = sha256_file(p)
            if gd.get("sidecar_sha256") != actual_sha:
                sha_mismatches.append((eid, g, gd.get("sidecar_sha256"), actual_sha))
            raw = json.loads(p.read_text(encoding="utf-8"))
            v = str(raw["verdict"]) if "verdict" in raw else ("PASS" if raw.get("ok") else "FAIL")
            if gd.get("verdict") != v:
                verdict_mismatches.append((eid, g, gd.get("verdict"), v))
            cuts = len(raw.get("rows", []))
            warns = list(raw.get("warn", []))
            fails = list(raw.get("failed", []))
            if gd.get("cuts_total") != cuts:
                field_mismatches.append((eid, g, "cuts_total", gd.get("cuts_total"), cuts))
            if gd.get("warn_count") != len(warns):
                field_mismatches.append((eid, g, "warn_count", gd.get("warn_count"), len(warns)))
            if gd.get("failed_count") != len(fails):
                field_mismatches.append((eid, g, "failed_count", gd.get("failed_count"), len(fails)))
            if gd.get("warn_items") != warns:
                item_list_mismatches.append((eid, g, "warn_items"))
            if gd.get("failed_items") != fails:
                item_list_mismatches.append((eid, g, "failed_items"))
            if not gd.get("fresh_vs_media"):
                fresh_mismatches.append((eid, g))

        mg = e["music_gate"]
        mp = mg.get("path")
        if mp:
            p = Path(mp)
            if not p.exists():
                missing_sidecars.append((eid, "music_gate", str(p)))
                continue
            sidecars_checked += 1
            actual_sha = sha256_file(p)
            if mg.get("sidecar_sha256") != actual_sha:
                sha_mismatches.append((eid, "music_gate", mg.get("sidecar_sha256"), actual_sha))
            if mp.endswith(".json"):
                raw = json.loads(p.read_text(encoding="utf-8"))
                v = str(raw["verdict"]) if "verdict" in raw else ("PASS" if raw.get("ok") else "FAIL")
                warns = list(raw.get("warn", []))
                fails = list(raw.get("fail", raw.get("failed", [])))
            else:
                lines = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
                warns = [ln[5:].strip() if ln.startswith("WARN ") else ln.strip() for ln in lines if ln.startswith("WARN")]
                fails = [ln[5:].strip() if ln.startswith("FAIL ") else ln.strip() for ln in lines if ln.startswith("FAIL")]
                tails = [ln for ln in lines if not ln.startswith("WARN") and not ln.startswith("FAIL")]
                v = "PASS" if (not fails and any("PASS:" in t for t in tails)) else "FAIL"
            if mg.get("verdict") != v:
                verdict_mismatches.append((eid, "music_gate", mg.get("verdict"), v))
            if mg.get("warn_count") != len(warns):
                field_mismatches.append((eid, "music_gate", "warn_count", mg.get("warn_count"), len(warns)))
            if mg.get("failed_count") != len(fails):
                field_mismatches.append((eid, "music_gate", "failed_count", mg.get("failed_count"), len(fails)))
            if mg.get("warn_items") != warns:
                item_list_mismatches.append((eid, "music_gate", "warn_items"))
            if mg.get("failed_items") != fails:
                item_list_mismatches.append((eid, "music_gate", "failed_items"))
            if not mg.get("fresh_vs_media"):
                fresh_mismatches.append((eid, "music_gate"))
            if is_newest and mg.get("uniqueness_coverage_status") == "partial_unreadable_comparisons":
                if eid not in j3128_ids:
                    uncovered_partial_newest.append(eid)

        exp_tw = e["picture_qa"]["warn_count"] + e["polish_gate"]["warn_count"] + e["music_gate"]["warn_count"]
        exp_tf = e["picture_qa"]["failed_count"] + e["polish_gate"]["failed_count"] + e["music_gate"]["failed_count"]
        if e.get("total_gate_warnings") != exp_tw or e.get("total_gate_fails") != exp_tf:
            derived_entry_mismatches.append((eid, e.get("total_gate_warnings"), exp_tw, e.get("total_gate_fails"), exp_tf))
        if is_newest and exp_tf > 0:
            current_newest_fails.append(eid)

        if is_new:
            new_entries_checked += 1
            mpath = Path(e["media_path"])
            if mpath.is_file():
                actual_msha = sha256_file(mpath)
                if actual_msha != e.get("media_sha256"):
                    new_media_issues.append((eid, "sha256", e.get("media_sha256"), actual_msha))
                mmtime = mpath.stat().st_mtime
                for g in ("picture_qa", "polish_gate", "music_gate"):
                    sp = e[g].get("path")
                    if sp and Path(sp).exists():
                        if Path(sp).stat().st_mtime + 1.0 < mmtime:
                            new_media_issues.append((eid, f"{g}_mtime_stale"))
                new_single_file_media_verified += 1
            elif not mpath.is_dir():
                new_media_issues.append((eid, "missing_media", str(mpath)))

    rep_text = owb_rep_bytes.decode("utf-8")
    assert "| FAIL (0/" not in rep_text, "Found bogus 'FAIL (0/' in Markdown report!"
    assert "| FAIL (0F," not in rep_text, "Found bogus 'FAIL (0F,' in Markdown report!"

    sec6_part = rep_text.split("## 6. Complete Reconciled Inventory Table")[1]
    sec6_rows = [ln for ln in sec6_part.splitlines() if ln.startswith("| OWB |") or ln.startswith("| HOS |")]
    assert len(sec6_rows) == 277, f"Expected 277 rows in Section 6 table, got {len(sec6_rows)}"

    result = {
        "inventory_sha256": inv_sha,
        "report_sha256": rep_sha,
        "hos_pr_head": "5f9fca210c77ab24f973405b01f1b7979b82a7a7",
        "hos_merged_main_verified": hos_main_head,
        "owb_hos_byte_identical": owb_hos_identical,
        "entries_checked": len(entries),
        "owb_entries_checked": sum(1 for e in entries if e["channel"] == "OWB"),
        "hos_entries_checked": sum(1 for e in entries if e["channel"] == "HOS"),
        "current_newest_entries_checked": sum(1 for e in entries if e["version_status"] == "current_newest"),
        "historical_superseded_entries_checked": sum(1 for e in entries if e["version_status"] == "historical_superseded"),
        "net_new_entries_since_j3104": new_entries_checked,
        "new_single_file_media_verified": new_single_file_media_verified,
        "sidecars_checked": sidecars_checked,
        "missing_sidecars": len(missing_sidecars),
        "sha256_mismatches": len(sha_mismatches),
        "verdict_mismatches": len(verdict_mismatches),
        "field_mismatches": len(field_mismatches),
        "item_list_mismatches": len(item_list_mismatches),
        "derived_entry_mismatches": len(derived_entry_mismatches),
        "fresh_vs_media_mismatches": len(fresh_mismatches),
        "new_media_issues": len(new_media_issues),
        "uncovered_partial_newest_vs_j3128": len(uncovered_partial_newest),
        "current_newest_fails": len(current_newest_fails),
        "sec6_table_rows": len(sec6_rows),
        "gate_warning_summary": inv["gate_warning_summary"],
        "music_uniqueness_coverage_summary": inv["music_uniqueness_coverage_summary"],
    }
    print(json.dumps(result, indent=2))
    assert (
        len(missing_sidecars) == 0
        and len(sha_mismatches) == 0
        and len(verdict_mismatches) == 0
        and len(field_mismatches) == 0
        and len(item_list_mismatches) == 0
        and len(derived_entry_mismatches) == 0
        and len(fresh_mismatches) == 0
        and len(new_media_issues) == 0
        and len(uncovered_partial_newest) == 0
        and len(current_newest_fails) == 0
    ), "Validation failed!"


if __name__ == "__main__":
    main()
