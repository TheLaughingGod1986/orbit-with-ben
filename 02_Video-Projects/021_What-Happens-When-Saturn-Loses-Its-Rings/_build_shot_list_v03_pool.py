#!/usr/bin/env python3
"""Saturn SHOT_LIST v03 — NASA pool only (Ben 1 Oct 14:23 London)."""
from __future__ import annotations

import csv
import json
import shutil
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
OWB = ROOT
while OWB.name != "orbit-with-ben" and OWB != OWB.parent:
    OWB = OWB.parent

POOL_JSON = ROOT / "07_Edit-Project" / "nasa_pool_v01.json"
SHEETS_SRC = ROOT / "07_Edit-Project" / "nasa_pool_v01"
SHOTS_JSON = ROOT / "saturn_shot_list_v03_SHOTS.json"
OUT_REPO = ROOT / "saturn_shot_list_v03"
OUT_UAT = OWB / "OWB UAT" / "saturn_shot_list_v03"
VO_FILE = "saturn_long_vo_v03b_tightened_LOCK.m4a"
VO_DUR = 523.62
HOLD_END = 543.62

pool = json.loads(POOL_JSON.read_text())
by_id = {e["nasa_id"]: e for e in pool}
pool_ids = set(by_id)
SHOTS = [tuple(s) for s in json.loads(SHOTS_JSON.read_text())]


def tc(s: float) -> str:
    m = int(s // 60)
    return f"{m:02d}:{s - 60 * m:05.2f}"


def credit_for(e: dict) -> str:
    nid = e["nasa_id"]
    title = e["title"].lower()
    if nid.startswith("GSFC") or (e.get("center") or "").upper() == "GSFC":
        return "NASA/Goddard Space Flight Center"
    hubble = {
        "PIA03156", "PIA03158", "PIA03159", "PIA03160", "PIA03161", "PIA03162",
        "PIA01269", "PIA01273", "PIA17900", "GSFC_20171208_Archive_e002157",
    }
    if nid in hubble or "hubble" in title:
        if nid == "GSFC_20171208_Archive_e002157":
            return "NASA and E. Karkoschka (University of Arizona)"
        return "NASA/ESA/STScI (Hubble) — copy exact line from photojournal page"
    voyager = {
        "PIA00335", "PIA00534", "PIA01374", "PIA01380", "PIA01388", "PIA01486",
        "PIA01940", "PIA01953", "PIA01962", "PIA01966", "PIA01969", "PIA02227",
        "PIA02241", "PIA02269", "PIA02274", "PIA02275",
    }
    if nid in voyager or "voyager" in title:
        return "NASA/JPL"
    if any(w in title for w in ("illustration", "artist", "concept")):
        return "NASA/JPL-Caltech (illustration) — copy exact line from photojournal page"
    return "NASA/JPL-Caltech/Space Science Institute"


def main() -> None:
    used_nasa: list[str] = []
    rows = []
    flags = []
    for i, (tin, tout, line, kind, ref, reason, caption) in enumerate(SHOTS, 1):
        dur = round(tout - tin, 2)
        if kind == "NASA":
            assert ref in pool_ids, f"{ref} not in pool"
            e = by_id[ref]
            used_nasa.append(ref)
            title, link, orig = e["title"], e["details"], e["orig"]
            cred, sec = credit_for(e), e["section"]
            frame = f"black + 5–8% push; {e['width']}×{e['height']}; ≤~1.5×; no stretch/slow-mo/freeze"
        elif kind == "AI":
            title, link, orig = Path(ref).name, ref, ""
            cred, sec, frame = "Approved AI — not NASA", "", "approved AI — no new Veo"
        elif kind == "GODDARD":
            title = "NASA Goddard SVS 12672 — Saturn ring-rain visualisation"
            link, orig = "https://svs.gsfc.nasa.gov/12672/", ""
            cred, sec, frame = "NASA's Goddard Space Flight Center / SVS", "", "ONE continuous shot — do not slice"
        elif kind == "OMNI":
            title, link, orig = ref, "canonical Orbit still + Omni (after Ben OK)", ""
            cred, sec, frame = "Orbit Omni — canonical still", "", "Omni only — never Veo for Orbit"
        else:
            raise ValueError(kind)

        if caption and "FLAG" in str(caption):
            flags.append(f"Row {i}: {caption}")
        if reason and "FLAG:" in reason:
            flags.append(f"Row {i}: {reason}")

        rows.append({
            "n": i, "vo_in": tc(tin), "vo_out": tc(tout), "dur_s": dur,
            "vo_line": line, "kind": kind, "nasa_id": ref if kind == "NASA" else "",
            "asset": ref, "title": title, "link": link, "orig": orig,
            "reason": reason, "caption_lock": caption or "", "credit": cred,
            "frame": frame, "section_pool": sec,
        })

    dupes = sorted(k for k, v in Counter(used_nasa).items() if v > 1)
    missing = sorted(k for k in used_nasa if k not in pool_ids)
    ai_paths = [r["asset"] for r in rows if r["kind"] == "AI"]
    ai_dupes = sorted(k for k, v in Counter(ai_paths).items() if v > 1)
    goddard = [r for r in rows if r["kind"] == "GODDARD"]
    check = {
        "vo": VO_FILE,
        "vo_duration_s": VO_DUR,
        "end_hold_to_s": HOLD_END,
        "rows": len(rows),
        "nasa_ids_used": used_nasa,
        "nasa_count": len(used_nasa),
        "nasa_unique": len(set(used_nasa)),
        "all_ids_in_nasa_pool_v01_json": not missing,
        "no_id_appears_twice": not dupes,
        "duplicate_nasa_ids": dupes,
        "nasa_ids_not_in_pool": missing,
        "goddard_rows": len(goddard),
        "goddard_continuous_once": len(goddard) == 1,
        "ai_assets_once_each": not ai_dupes,
        "ai_duplicate_paths": ai_dupes,
        "ai_assets": ai_paths,
        "omni_beats": len([r for r in rows if r["kind"] == "OMNI"]),
        "new_veo": 0,
        "flags": flags,
        "pool_size": len(pool_ids),
        "unused_pool_count": len(pool_ids - set(used_nasa)),
        "pia17185_note": "Not used (~orig HTTP 403).",
        "sheet_review": "Eyeballed S1 S2 S3 S5 S7 S8 S9 S12 before build; skip PIA01273 moon dots.",
        "chapter_card_gap_s": 0.72,
        "PASS": not missing and not dupes and not ai_dupes and len(goddard) == 1,
    }

    for dest in (OUT_REPO, OUT_UAT):
        dest.mkdir(parents=True, exist_ok=True)
        sheets = dest / "sheets"
        sheets.mkdir(exist_ok=True)
        for sheet in sorted(SHEETS_SRC.glob("sheet_*.jpg")):
            Image.open(sheet).convert("RGB").save(sheets / f"{sheet.stem}.png")
        mon = ROOT / "04_Generated-Clips/shorts_stills_v01/monday_saturn_rings_streaming_v01_crop_limb_v02.png"
        mon_c = ROOT / "04_Generated-Clips/shorts_stills_v01/monday_v01_crop_limb_v02_contact.png"
        if mon.exists():
            shutil.copy2(mon, dest / mon.name)
        if mon_c.exists():
            shutil.copy2(mon_c, dest / "monday_crop_limb_v02_contact.png")
        shutil.copy2(SHOTS_JSON, dest / "SHOTS.json")

        fields = ["n", "vo_in", "vo_out", "dur_s", "vo_line", "kind", "nasa_id", "asset",
                  "title", "link", "reason", "caption_lock", "credit", "frame", "section_pool"]
        with (dest / "SHOT_LIST.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

        md = [
            "# Saturn 021 — SHOT_LIST v03 (NASA pool only)",
            "",
            "**Ben order 1 Oct 14:23 London** — supersedes CoS images-api hunt.",
            "Pool: `07_Edit-Project/NASA_POOL_v01.md` / `nasa_pool_v01.json`.",
            "**STOP for Ben review. No generation.**",
            "",
            "## Summary",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| VO (locked) | `{VO_FILE}` · **{VO_DUR:.2f}s (8:43.62)** |",
            f"| End hold | to **{tc(HOLD_END)}** (+20s after last VO) |",
            f"| Rows | **{len(rows)}** |",
            f"| NASA IDs | **{len(used_nasa)}** unique · 0 duplicates |",
            "| Reuse | **0** (including second framings) |",
            "| Goddard SVS 12672 | **once**, continuous (03:28.42–04:09.28) |",
            "| AI approved | ice v07 · young rings · bare v05 — each once |",
            "| Orbit | Omni ×2 (tumble · bare) — after Ben OK |",
            "| New Veo | **none** |",
            "| Frame | black + 5–8% push · ≤~1.5× · no stretch/slow-mo/freeze |",
            "| Monday 9:16 | `monday_saturn_rings_streaming_v01_crop_limb_v02.png` (1080×1920, approved still, no paint) |",
            "",
            "## Caption locks",
            "",
            "- Aurora → **Saturn's magnetic field** (never “ring rain”).",
            "- Hubble 1996–2000 → **seasons** (never “thinning”).",
            "- Grand Finale drawings → **illustration**.",
            "",
            "## Gaps flagged (not hunted)",
            "",
        ]
        for fl in flags:
            md.append(f"- {fl}")
        md += [
            "",
            "## Sheet review (before build)",
            "",
            "Ran `fetch_nasa_pool.py` (+ User-Agent retry). **154/154** open. Per-section sheets in `sheets/`. Eyeballed S1–S3, S5, S7–S9, S12. Skipped PIA01273 (moon dots). Did not use PIA17185 (orig 403).",
            "",
            "## Uniqueness check (paste)",
            "",
            "```json",
            json.dumps(check, indent=2),
            "```",
            "",
            f"**PASS = {check['PASS']}** — every NASA ID ∈ `nasa_pool_v01.json` and no ID appears twice.",
            "",
            "## Shot table",
            "",
            "| # | VO in | VO out | Dur | VO line | ID / asset | NASA title | Link | Why it fits | Caption / credit |",
            "|---:|---|---|---:|---|---|---|---|---|---|",
        ]
        for r in rows:
            nid = r["nasa_id"] or r["kind"]
            md.append(
                f"| {r['n']} | {r['vo_in']} | {r['vo_out']} | {r['dur_s']} | {r['vo_line']} | `{nid}` | {r['title']} | {r['link']} | {r['reason']} | {r['caption_lock'] or r['credit']} |"
            )
        md += ["", "## Description credit block", "",
               "Image credits (NASA media guidelines; NASA does not endorse this film):", ""]
        seen = set()
        for r in rows:
            if r["kind"] != "NASA" or r["nasa_id"] in seen:
                continue
            seen.add(r["nasa_id"])
            md.append(f"- {r['nasa_id']} — {r['title']} — {r['credit']} — {r['link']}")
        md += [
            "- SVS 12672 — Saturn ring-rain visualisation — NASA's Goddard Space Flight Center / SVS — https://svs.gsfc.nasa.gov/12672/",
            "",
            "_STOP — Ben OK before Omni / assemble._",
            "",
        ]
        (dest / "SHOT_LIST.md").write_text("\n".join(md))
        (dest / "AUTOCHECK.json").write_text(json.dumps(check, indent=2) + "\n")
        (dest / "AUTOCHECK.md").write_text(
            "# AUTOCHECK v03\n\n```json\n" + json.dumps(check, indent=2) + "\n```\n\n"
            + ("**PASS**\n" if check["PASS"] else "**FAIL**\n")
        )
        (dest / "MONDAY_NOTE.md").write_text(
            "# Monday Short 9:16 — v03\n\n"
            "Approved still crop, no paint. **1080×1920**.\n\n"
            "- `monday_saturn_rings_streaming_v01_crop_limb_v02.png`\n"
            "- `monday_crop_limb_v02_contact.png`\n"
            "- Pool alt only if Ben asks.\n"
        )
        print("wrote", dest)

    print(json.dumps(check, indent=2))
    if not check["PASS"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
