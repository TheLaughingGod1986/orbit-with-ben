#!/usr/bin/env python3
"""Saturn first cut v03e — LOCK VO word audit splices on top of v03d picture.

Reuse v03d picture (cards +2s unchanged). Rebuild audio from
saturn_rings_vo_v03e_patches.wav (leak + Next splices; LOCK untouched).

Nothing KEEP until Ben reviews. No media in git. PR #99 untouched.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Reuse helpers from v03d
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _assemble_saturn_first_cut_v03d as v03d

HERE = Path(__file__).resolve().parent
SHOT = HERE / "shot_list_v03i.csv"
VO = Path("/tmp/saturn_v03d/saturn_rings_vo_v03e_patches.wav")
WORK = HERE / "saturn_film/work_first_cut_v03e"
OUT_LOCAL = HERE / "saturn_film/saturn_first_cut_v03e.mp4"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
UAT_DIR = UAT / "saturn_first_cut_v03e"
ART = Path("/Users/benjaminoats/.local/share/cursor-mac-mini-worker/artifacts")
PIC_SRC = HERE / "saturn_film/work_first_cut_v03d/picture_all.mp4"
AUDIT = Path("/tmp/saturn_v03d/lock_vo_word_diff.md")
PATCH_REPORT = Path("/tmp/saturn_v03d/v03e_vo_patches.json")
XFADE = 0.40


def chunk_write(src, dest: Path, retries: int = 14) -> None:
    data = src if isinstance(src, (bytes, bytearray)) else Path(src).read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            tmp = dest.with_suffix(dest.suffix + ".partial")
            with open(tmp, "wb") as o:
                for i in range(0, len(data), 256 * 1024):
                    o.write(data[i : i + 256 * 1024])
                    o.flush()
            tmp.replace(dest)
            time.sleep(0.2)
            if dest.stat().st_size == len(data):
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.0 * (attempt + 1))
    Path("/tmp").joinpath(f"uat_stage_{dest.name}").write_bytes(data)


def write_word_excerpts(video: Path) -> list[dict]:
    """Excerpts around each VO splice + re-record candidates."""
    ex_dir = UAT_DIR / "excerpts"
    ex_dir.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    # film times ≈ VO + card offsets (same mapping as v03d)
    clips = [
        ("excerpt_leak_fix", 194.5, 8.0),       # ~VO 188 → film ~195.7
        ("excerpt_next_fix", 537.5, 12.0),      # end hand-off
        ("excerpt_a_world_rerecord", 51.5, 6.0),
        ("excerpt_mimas_rerecord", 85.5, 6.0),
        ("excerpt_late_arrival_rerecord", 378.5, 8.0),
        ("excerpt_forever_disk_rerecord", 515.5, 8.0),
        ("excerpt_last_60s", max(0.0, v03d.probe(video) - 60.0), 60.0),
    ]
    out = []
    for name, start, dur in clips:
        dest = ex_dir / f"{name}.mp4"
        v03d.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(video),
            "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
            str(dest),
        ])
        shutil.copy2(dest, ART / dest.name)
        out.append({"name": name, "start": start, "dur": dur, "path": str(dest)})
    return out


def main() -> None:
    if not VO.exists():
        raise SystemExit(f"missing patched VO {VO}")
    if not PIC_SRC.exists():
        raise SystemExit(f"missing v03d picture {PIC_SRC}")

    WORK.mkdir(parents=True, exist_ok=True)
    UAT_DIR.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)

    # Point v03d module globals at v03e paths for build_audio / measure_lufs
    v03d.VO = VO
    v03d.WORK = WORK
    v03d.UAT_DIR = UAT_DIR
    v03d.OUT_LOCAL = OUT_LOCAL
    v03d.XFADE = XFADE

    rows = list(csv.DictReader(SHOT.open(newline="", encoding="utf-8")))
    total = float(rows[-1]["vo_out"])
    print(f"shot list rows={len(rows)} total={total:.3f}s", flush=True)

    picture = WORK / "picture_all.mp4"
    if not picture.exists() or picture.stat().st_size != PIC_SRC.stat().st_size:
        print("copying v03d picture_all.mp4 → v03e work", flush=True)
        shutil.copy2(PIC_SRC, picture)
    print(f"picture {picture} {v03d.probe(picture):.2f}s", flush=True)

    # Fresh audio parts from patched VO (do not reuse v03d cached wavs)
    audio_parts = WORK / "audio_parts"
    if audio_parts.exists():
        shutil.rmtree(audio_parts)
    audio = v03d.build_audio(rows, total)

    fade_pic_start = max(0.0, total - 2.0)
    v03d.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(picture), "-i", str(audio),
        "-filter_complex",
        f"[0:v]fade=t=out:st={fade_pic_start:.3f}:d=2,format=yuv420p[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(OUT_LOCAL),
    ])
    print(f"LOCAL {OUT_LOCAL} {v03d.probe(OUT_LOCAL):.2f}s", flush=True)

    lufs = v03d.measure_lufs(OUT_LOCAL)
    vo_lufs = v03d.measure_lufs(VO)
    print(f"LUFS mix={lufs.get('integrated_lufs')} VO={vo_lufs.get('integrated_lufs')}", flush=True)

    # Contact / per-row from v03d
    for name in ("contact12.png", "per_row.png"):
        src = HERE / "saturn_film/work_first_cut_v03d" / name
        if src.exists():
            chunk_write(src, UAT_DIR / f"saturn_first_cut_v03e_{name}")
            shutil.copy2(src, ART / f"saturn_first_cut_v03e_{name}")

    excerpts = write_word_excerpts(OUT_LOCAL)
    chunk_write(OUT_LOCAL, UAT_DIR / "saturn_first_cut_v03e.mp4")

    h = hashlib.sha256()
    with open(OUT_LOCAL, "rb") as f:
        while True:
            b = f.read(500 * 1024)
            if not b:
                break
            h.update(b)

    patch = json.loads(PATCH_REPORT.read_text()) if PATCH_REPORT.exists() else {}
    # Refresh patch report timestamps for donor324 build
    patch_note = {
        "spliced": [
            {
                "script": "leak",
                "vo_t": [188.18, 188.60],
                "v03d_t": [195.68, 196.10],
                "donor_vo_t": [324.10, 324.52],
                "issue": "plain ASR leaf/leap; spliced clean 'leak' from later line",
            },
            {
                "script": "next",
                "vo_t": [520.18, 520.80],
                "v03d_t": [540.63, 541.25],
                "donor_vo_t": [206.30, 206.54],
                "issue": "swallowed Next→Net (Ben); same fix as v03d",
            },
        ],
        "re_record_candidates": patch.get("re_record_candidates_not_spliced", []),
        "false_positives_excluded": patch.get("false_positives_excluded", []),
    }
    (WORK / "WORD_AUDIT.json").write_text(json.dumps(patch_note, indent=2))
    chunk_write(json.dumps(patch_note, indent=2).encode(), UAT_DIR / "WORD_AUDIT.json")
    if AUDIT.exists():
        chunk_write(AUDIT.read_bytes(), UAT_DIR / "LOCK_VO_WORD_DIFF.md")

    md = f"""# Saturn first cut v03e — LOCK VO word audit

**Not KEEP** until Ben reviews. Media iCloud only. PR #99 untouched.

| | |
|---|---|
| File | `saturn_first_cut_v03e.mp4` |
| Duration | **{v03d.probe(OUT_LOCAL):.1f} s** |
| sha256 | `{h.hexdigest()}` |
| LUFS | **{lufs.get('integrated_lufs')}** (LRA {lufs.get('lra')}) |
| Shot list | `shot_list_v03i.csv` (picture = v03d) |
| VO | LOCK + leak + Next splices (LOCK file untouched) |

## Method
- Whisper **medium.en** word timestamps on clean LOCK stem
- SequenceMatcher vs locked shot-list script (alignment ratio **0.978**)
- Isolated-clip re-ASR to drop false positives (tokenization, spelling, compound slips)
- Splice only where a clean in-VO donor verifies; else re-record list

## Spliced (Next-style)

### 1. leak — FIXED
- VO **188.18–188.60** · v03d/v03e film **~195.7**
- Plain ASR on LOCK: leaf/leap; donor `@324.10–324.52` (“either leak as…”)
- Excerpt: `excerpts/excerpt_leak_fix.mp4`

### 2. Next — FIXED (carried from v03d)
- VO **520.18** (dur 0.08s in LOCK) · film **~540.6**
- Donor subscribe-line `next` `@206.30–206.54`
- Excerpt: `excerpts/excerpt_next_fix.mp4`

## Re-record candidates (no clean donor / micro-splice failed)

| word | VO t | v03d/v03e film t | ASR heard | note |
|---|---|---|---|---|
| a | 49.98–50.12 | 53.73–53.87 | the | said “the world” not “a world”; 0.14s splice failed verify |
| Mimas | 84.12–84.66 | 87.87–88.41 | Mimath/Mima | no donor; proper-noun ASR may be wrong — ear-check |
| late arrival | 365.82–366.62 | 381.52–382.32 | later rival | consistent full-film + clip; no donors |
| disk (forever-disk) | 498.04–498.40 | 518.49–518.85 | diff/did | only other disc@20.9 is itself low-confidence |

## Excluded false positives
- emptier roads → empty erodes (ASR compound)
- subscribe-line is→as (isolated clip: **is** @0.90)
- vapour↔vapor (spelling)
- three hundred↔300, twenty-two↔22, a hundred (number tokenization)

## Runtime
Same picture as v03d → **~559.1 s**. No trim without Ben OK.
"""
    (WORK / "WORD_FIXES_AND_RUNTIME.md").write_text(md)
    chunk_write(md.encode(), UAT_DIR / "WORD_FIXES_AND_RUNTIME.md")
    (ART / "saturn_first_cut_v03e_WORD_FIXES.md").write_text(md)

    meta = {
        "cut": "v03e",
        "shot_list": "shot_list_v03i.csv",
        "picture": "reused v03d picture_all.mp4",
        "vo": VO.name,
        "vo_base": "saturn_rings_vo_v03b_tightened_LOCK.wav",
        "vo_patches": patch_note["spliced"],
        "re_record_candidates": patch_note["re_record_candidates"],
        "duration": v03d.probe(OUT_LOCAL),
        "sha256": h.hexdigest(),
        "excerpts": excerpts,
        "loudness": {
            "mix_integrated_lufs": lufs.get("integrated_lufs"),
            "mix_lra": lufs.get("lra"),
            "vo_integrated_lufs": vo_lufs.get("integrated_lufs"),
        },
        "icloud": str(UAT_DIR),
        "keep": False,
        "note": "media iCloud only; nothing KEEP until Ben reviews; PR #99 untouched",
    }
    (WORK / "META.json").write_text(json.dumps(meta, indent=2))
    chunk_write(json.dumps(meta, indent=2).encode(), UAT_DIR / "ARRIVAL.json")
    (ART / "saturn_first_cut_v03e_ARRIVAL.json").write_text(json.dumps(meta, indent=2))
    print("DONE", json.dumps({k: meta[k] for k in ("cut", "duration", "sha256", "loudness")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
