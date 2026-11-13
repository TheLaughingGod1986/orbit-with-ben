#!/usr/bin/env python3
"""
Reproducible validation script for J2756 (reconciling J2753 QA sweep inventory
and report against all 663 raw gate sidecars and SIDECAR_RECONCILIATION.json).
"""

import hashlib
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OWB_DIR = REPO_ROOT / "00_Brand/Channel-Setup/audits/qa_sweeps"
HOS_WT_DIR = Path(os.environ.get("HOS_QA_SWEEPS_DIR", "/Volumes/MiniWork/scratch/J2756-hos/00_Brand/Channel-Setup/audits/qa_sweeps"))
HOS_MAIN_DIR = Path("/Users/benjaminoats/YouTube/History Of Science/00_Brand/Channel-Setup/audits/qa_sweeps")
CHIEF_RECON_PATH = REPO_ROOT / "jobs/reviews/J2753/SIDECAR_RECONCILIATION.json"

INV_NAME = "J2753_QA_SWEEP_INVENTORY_2026-11-13.json"
REP_NAME = "J2753_QA_SWEEP_REPORT_2026-11-13.md"


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    owb_inv_p = OWB_DIR / INV_NAME
    owb_rep_p = OWB_DIR / REP_NAME
    hos_dir = HOS_WT_DIR if (HOS_WT_DIR / INV_NAME).exists() else HOS_MAIN_DIR
    hos_inv_p = hos_dir / INV_NAME
    hos_rep_p = hos_dir / REP_NAME

    owb_hos_identical = (
        owb_inv_p.read_bytes() == hos_inv_p.read_bytes()
        and owb_rep_p.read_bytes() == hos_rep_p.read_bytes()
    )
    assert owb_hos_identical, f"Inventory/Report differs between OWB ({OWB_DIR}) and HOS ({hos_dir})!"

    inv_sha = sha256_file(owb_inv_p)
    rep_sha = sha256_file(owb_rep_p)

    inv = json.load(open(owb_inv_p, "r", encoding="utf-8"))
    entries = inv["entries"]
    assert len(entries) == 228, f"Expected 228 entries, got {len(entries)}"

    missing_sidecars = []
    sha_mismatches = []
    verdict_mismatches = []
    field_mismatches = []
    item_list_mismatches = []
    derived_entry_mismatches = []

    sidecars_checked = 0

    for e in entries:
        eid = e["export_id"]
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
            raw = json.load(open(p, "r", encoding="utf-8"))
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
                raw = json.load(open(p, "r", encoding="utf-8"))
                v = str(raw["verdict"]) if "verdict" in raw else ("PASS" if raw.get("ok") else "FAIL")
                warns = list(raw.get("warn", []))
                fails = list(raw.get("fail", raw.get("failed", [])))
            else:
                lines = [ln.strip() for ln in open(p, "r", encoding="utf-8").read().splitlines() if ln.strip()]
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

        exp_tw = e["picture_qa"]["warn_count"] + e["polish_gate"]["warn_count"] + e["music_gate"]["warn_count"]
        exp_tf = e["picture_qa"]["failed_count"] + e["polish_gate"]["failed_count"] + e["music_gate"]["failed_count"]
        if e.get("total_gate_warnings") != exp_tw or e.get("total_gate_fails") != exp_tf:
            derived_entry_mismatches.append((eid, e.get("total_gate_warnings"), exp_tw, e.get("total_gate_fails"), exp_tf))

    chief_recon = json.load(open(CHIEF_RECON_PATH, "r", encoding="utf-8"))
    by_eid = {e["export_id"]: e for e in entries}
    chief_remaining = []
    for m in chief_recon["field_mismatches"]:
        e = by_eid[m["export"]]
        actual_val = e[m["gate"]].get(m["field"])
        if actual_val != m["sidecar"]:
            chief_remaining.append((m["export"], m["gate"], m["field"], actual_val, m["sidecar"]))

    rep_text = owb_rep_p.read_text(encoding="utf-8")
    assert "| FAIL (0/" not in rep_text, "Found bogus 'FAIL (0/' in Markdown report!"
    assert "| FAIL (0F," not in rep_text, "Found bogus 'FAIL (0F,' in Markdown report!"

    sec6_part = rep_text.split("## 6. Complete Reconciled Inventory Table")[1]
    sec6_rows = [ln for ln in sec6_part.splitlines() if ln.startswith("| OWB |") or ln.startswith("| HOS |")]
    assert len(sec6_rows) == 228, f"Expected 228 rows in Section 6 table, got {len(sec6_rows)}"

    result = {
        "inventory_sha256": inv_sha,
        "report_sha256": rep_sha,
        "owb_hos_byte_identical": owb_hos_identical,
        "entries_checked": len(entries),
        "sidecars_checked": sidecars_checked,
        "missing_sidecars": len(missing_sidecars),
        "sha256_mismatches": len(sha_mismatches),
        "verdict_mismatches": len(verdict_mismatches),
        "field_mismatches": len(field_mismatches),
        "item_list_mismatches": len(item_list_mismatches),
        "derived_entry_mismatches": len(derived_entry_mismatches),
        "chief_66_mismatches_remaining": len(chief_remaining),
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
        and len(chief_remaining) == 0
    ), "Validation failed!"


if __name__ == "__main__":
    main()
