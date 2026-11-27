#!/usr/bin/env python3
"""
Reproducible Chief validation script for J3766 (reconciling J3766 QA sweep
inventory and report against all 816 raw gate sidecars across 280 entries,
verifying direct media SHA-256 and live mtime freshness on all 3 net new
post-J3340 entries + standalone OWB:064 score bed, verifying 73/73 J3128
baseline music coverage, verifying byte-identical OWB/HOS copies, and
verifying internal top-level identity/scope metadata consistency).
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OWB_DIR = REPO_ROOT / "00_Brand/Channel-Setup/audits/qa_sweeps"
HOS_REPO = Path("/Users/benjaminoats/YouTube/History Of Science")

INV_NAME = "J3766_QA_SWEEP_INVENTORY_2026-11-26.json"
REP_NAME = "J3766_QA_SWEEP_REPORT_2026-11-26.md"
J3340_INV_NAME = "J3340_QA_SWEEP_INVENTORY_2026-11-22.json"
J3128_INV_NAME = "J3128_MUSIC_RECONCILIATION_INVENTORY_2026-11-19.json"


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hos-ref", default="origin/gemini/J3766-qa-sweep",
                    help="Git ref in HOS repo to compare against OWB copy")
    ap.add_argument("--strict", action="store_true",
                    help="Exit non-zero if top-level metadata or Section 4 discrepancies exist")
    ap.add_argument("--out", default="", help="Optional path to write JSON summary")
    args = ap.parse_args()

    owb_inv_p = OWB_DIR / INV_NAME
    owb_rep_p = OWB_DIR / REP_NAME
    owb_inv_bytes = owb_inv_p.read_bytes()
    owb_rep_bytes = owb_rep_p.read_bytes()

    hos_inv_bytes = subprocess.check_output(
        ["git", "-C", str(HOS_REPO), "show", f"{args.hos_ref}:00_Brand/Channel-Setup/audits/qa_sweeps/{INV_NAME}"]
    )
    hos_rep_bytes = subprocess.check_output(
        ["git", "-C", str(HOS_REPO), "show", f"{args.hos_ref}:00_Brand/Channel-Setup/audits/qa_sweeps/{REP_NAME}"]
    )
    hos_ref_oid = subprocess.check_output(
        ["git", "-C", str(HOS_REPO), "rev-parse", args.hos_ref], text=True
    ).strip()

    owb_hos_identical = (owb_inv_bytes == hos_inv_bytes and owb_rep_bytes == hos_rep_bytes)
    inv_sha = hashlib.sha256(owb_inv_bytes).hexdigest()
    rep_sha = hashlib.sha256(owb_rep_bytes).hexdigest()

    inv = json.loads(owb_inv_bytes.decode("utf-8"))
    entries = inv["entries"]

    j3340_inv = json.loads((OWB_DIR / J3340_INV_NAME).read_text(encoding="utf-8"))
    j3340_ids = {e["export_id"] for e in j3340_inv["entries"]}

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
    metadata_issues = []

    sidecars_checked = 0
    new_entries_checked = 0
    new_single_file_media_verified = 0
    new_pack_members_verified = 0

    pic_cuts = pol_cuts = 0
    pic_f = pol_f = mus_f = 0
    pic_w = pol_w = mus_w = 0
    pic_sw = pol_sw = mus_sw = 0
    mus_json = mus_txt = mus_na = 0
    entries_with_w = 0

    for e in entries:
        eid = e["export_id"]
        is_new = eid not in j3340_ids
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
            if g == "picture_qa":
                pic_cuts += cuts; pic_f += len(fails); pic_w += len(warns); pic_sw += int(len(warns) > 0)
            else:
                pol_cuts += cuts; pol_f += len(fails); pol_w += len(warns); pol_sw += int(len(warns) > 0)

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
                mus_json += 1
                raw = json.loads(p.read_text(encoding="utf-8"))
                v = str(raw["verdict"]) if "verdict" in raw else ("PASS" if raw.get("ok") else "FAIL")
                warns = list(raw.get("warn", []))
                fails = list(raw.get("fail", raw.get("failed", [])))
            else:
                mus_txt += 1
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
            mus_f += len(fails); mus_w += len(warns); mus_sw += int(len(warns) > 0)
        else:
            mus_na += 1

        exp_tw = e["picture_qa"]["warn_count"] + e["polish_gate"]["warn_count"] + e["music_gate"]["warn_count"]
        exp_tf = e["picture_qa"]["failed_count"] + e["polish_gate"]["failed_count"] + e["music_gate"]["failed_count"]
        if exp_tw > 0:
            entries_with_w += 1
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
            elif mpath.is_dir():
                mp4s = sorted(f for f in mpath.glob("*.mp4") if not f.name.startswith("._"))
                if not mp4s:
                    new_media_issues.append((eid, "empty_pack_dir"))
                else:
                    max_m = max(f.stat().st_mtime for f in mp4s)
                    for g in ("picture_qa", "polish_gate"):
                        sp = e[g].get("path")
                        if sp and Path(sp).exists():
                            if Path(sp).stat().st_mtime + 1.0 < max_m:
                                new_media_issues.append((eid, f"{g}_pack_mtime_stale"))
                    for m in e.get("pack_members", []):
                        mp = Path(m["path"])
                        if not mp.exists() or sha256_file(mp) != m.get("sha256"):
                            new_media_issues.append((eid, "pack_member_sha256", m.get("name")))
                        else:
                            new_pack_members_verified += 1
            else:
                new_media_issues.append((eid, "missing_media", str(mpath)))

    # Verify standalone 064 score bed verification entries
    standalone_bed_issues = []
    for sb in inv.get("j3766_standalone_bed_verifications", []):
        sp = Path(sb["music_gate_path"])
        bp = Path(sb["bed_path"])
        if not sp.exists() or not bp.exists():
            standalone_bed_issues.append((sb.get("film"), "missing_path"))
            continue
        if sha256_file(sp) != sb.get("music_gate_sha256"):
            standalone_bed_issues.append((sb.get("film"), "sha256_mismatch"))
        raw = json.loads(sp.read_text(encoding="utf-8"))
        if raw.get("verdict") != sb.get("verdict") or len(raw.get("fail", [])) != sb.get("failed_count") or len(raw.get("warn", [])) != sb.get("warn_count"):
            standalone_bed_issues.append((sb.get("film"), "verdict_or_count_mismatch"))

    # Verify aggregate summary consistency
    gws = inv["gate_warning_summary"]
    if gws.get("picture_qa_cuts_total") != pic_cuts or gws.get("polish_gate_cuts_total") != pol_cuts:
        metadata_issues.append("gate_warning_summary:cuts_total")
    if gws.get("total_warn_instances") != pic_w + pol_w + mus_w:
        metadata_issues.append("gate_warning_summary:total_warn_instances")
    if gws.get("total_fail_indicators") != pic_f + pol_f + mus_f:
        metadata_issues.append("gate_warning_summary:total_fail_indicators")

    # Verify top-level identity/scope metadata consistency against entries
    sf = [e for e in entries if e.get("entry_kind") == "single_file"]
    vp = [e for e in entries if e.get("entry_kind") != "single_file"]
    vp_members = sum(e.get("pack_member_count") or 0 for e in vp)
    total_files = len(sf) + vp_members
    by_sk = {}
    for e in sf:
        sk = e.get("media_storage_kind")
        by_sk[sk] = by_sk.get(sk, 0) + 1
    expected_unwrapped_sf = len(sf) - by_sk.get("nas_tar_archive_member", 0) - by_sk.get("icloud_clouddocs_stub_verified_by_pack_and_upload_manifests", 0)
    expected_nas_hydrated = (
        by_sk.get("nas_archive_hydrated_mp4", 0)
        + by_sk.get("nas_staging_hydrated_mp4", 0)
        + by_sk.get("nas_studio_live_mp4", 0)
    )
    expected_desk_preserved = by_sk.get("desk_preserved_mp4", 0) + by_sk.get("desk_preserved_render_mp4", 0)

    ivs = inv.get("identity_verification_summary") or {}
    checks = [
        ("identity_verification_summary.total_entries", ivs.get("total_entries"), len(entries)),
        ("identity_verification_summary.single_file_entries", ivs.get("single_file_entries"), len(sf)),
        ("identity_verification_summary.visual_pack_entries", ivs.get("visual_pack_entries"), len(vp)),
        ("identity_verification_summary.visual_pack_member_files", ivs.get("visual_pack_member_files"), vp_members),
        ("identity_verification_summary.total_enumerated_files", ivs.get("total_enumerated_files"), total_files),
        ("identity_verification_summary.directly_hashed_pack_member_files", ivs.get("directly_hashed_pack_member_files"), vp_members),
        ("identity_verification_summary.directly_hashed_single_file_mp4s", ivs.get("directly_hashed_single_file_mp4s"), expected_unwrapped_sf),
        ("identity_verification_summary.directly_hashed_unwrapped_files", ivs.get("directly_hashed_unwrapped_files"), expected_unwrapped_sf + vp_members),
        ("directly_hashed_pack_member_files_count", inv.get("directly_hashed_pack_member_files_count"), vp_members),
        ("directly_hashed_single_file_exports_count", inv.get("directly_hashed_single_file_exports_count"), expected_unwrapped_sf),
        ("directly_hashed_unwrapped_files_count", inv.get("directly_hashed_unwrapped_files_count"), expected_unwrapped_sf + vp_members),
        ("directly_hashed_nas_hydrated_mp4_count", inv.get("directly_hashed_nas_hydrated_mp4_count"), expected_nas_hydrated),
        ("directly_hashed_desk_preserved_mp4_count", inv.get("directly_hashed_desk_preserved_mp4_count"), expected_desk_preserved),
        ("directly_readable_unwrapped_entries_count", inv.get("directly_readable_unwrapped_entries_count"), expected_unwrapped_sf + len(vp)),
    ]
    for label, actual, expected in checks:
        if actual != expected:
            metadata_issues.append(f"{label}: actual={actual} expected={expected}")

    scope_txt = str(inv.get("scope_and_limits") or "")
    if "280 entries" not in scope_txt or "816" not in scope_txt or "485" not in scope_txt:
        metadata_issues.append("scope_and_limits: stale_j3340_text")
    rec_txt = str(inv.get("reconciles_review") or "")
    if "J3766" not in rec_txt or "280 entries" not in rec_txt or "816" not in rec_txt:
        metadata_issues.append("reconciles_review: stale_j3340_text")

    rep_text = owb_rep_bytes.decode("utf-8")
    sec6_part = rep_text.split("## 6. Complete Reconciled Inventory Table")[1]
    sec6_rows = [ln for ln in sec6_part.splitlines() if ln.startswith("| OWB |") or ln.startswith("| HOS |")]

    if "## 4. Per-Member Identities & SHA-256 Hashes for All `13` Silent Visual Packs (`218` Member Files)" not in rep_text:
        metadata_issues.append("report_sec4: heading_still_lists_12_packs_194_members_missing_064_pack")

    result = {
        "inventory_sha256": inv_sha,
        "report_sha256": rep_sha,
        "hos_ref": args.hos_ref,
        "hos_ref_oid": hos_ref_oid,
        "owb_hos_byte_identical": owb_hos_identical,
        "entries_checked": len(entries),
        "owb_entries_checked": sum(1 for e in entries if e["channel"] == "OWB"),
        "hos_entries_checked": sum(1 for e in entries if e["channel"] == "HOS"),
        "current_newest_entries_checked": sum(1 for e in entries if e["version_status"] == "current_newest"),
        "historical_superseded_entries_checked": sum(1 for e in entries if e["version_status"] == "historical_superseded"),
        "net_new_entries_since_j3340": new_entries_checked,
        "new_single_file_media_verified": new_single_file_media_verified,
        "new_pack_members_verified": new_pack_members_verified,
        "standalone_bed_issues": len(standalone_bed_issues),
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
        "bogus_fail_0_in_report": ("| FAIL (0/" in rep_text or "| FAIL (0F," in rep_text),
        "sec6_table_rows": len(sec6_rows),
        "metadata_issues_count": len(metadata_issues),
        "metadata_issues": metadata_issues,
        "gate_warning_summary": inv["gate_warning_summary"],
        "music_uniqueness_coverage_summary": inv["music_uniqueness_coverage_summary"],
    }
    out_json = json.dumps(result, indent=2)
    print(out_json)
    if args.out:
        Path(args.out).write_text(out_json + "\n", encoding="utf-8")

    core_ok = (
        owb_hos_identical
        and len(entries) == 280
        and sidecars_checked == 816
        and len(missing_sidecars) == 0
        and len(sha_mismatches) == 0
        and len(verdict_mismatches) == 0
        and len(field_mismatches) == 0
        and len(item_list_mismatches) == 0
        and len(derived_entry_mismatches) == 0
        and len(fresh_mismatches) == 0
        and len(new_media_issues) == 0
        and len(standalone_bed_issues) == 0
        and len(uncovered_partial_newest) == 0
        and len(current_newest_fails) == 0
        and not result["bogus_fail_0_in_report"]
        and len(sec6_rows) == 280
    )
    if not core_ok:
        return 1
    if args.strict and metadata_issues:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
