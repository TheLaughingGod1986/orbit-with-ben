#!/usr/bin/env python3
"""Saturn first cut v03f — five EL retakes + Next/leak + optional end-hold trim.

Picture: v03d picture trimmed by 7s (end hold 15→8; never cuts VO).
Audio: rebuilt from saturn_rings_vo_v03f_patched.wav against shot_list_v03j.csv.
LOCK master untouched. Nothing KEEP until Ben. No media in git. PR #99 untouched.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _assemble_saturn_first_cut_v03d as v03d

HERE = Path(__file__).resolve().parent
SHOT = HERE / "shot_list_v03j.csv"
VO = Path("/tmp/saturn_v03f/saturn_rings_vo_v03f_patched.wav")
WORK = HERE / "saturn_film/work_first_cut_v03f"
OUT_LOCAL = HERE / "saturn_film/saturn_first_cut_v03f.mp4"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
UAT_DIR = UAT / "saturn_first_cut_v03f"
ART = Path("/Users/benjaminoats/.local/share/cursor-mac-mini-worker/artifacts")
PIC_SRC = HERE / "saturn_film/work_first_cut_v03d/picture_all.mp4"
XFADE = 0.40
END_HOLD_TRIM = 7.0  # 15s → 8s


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


def write_fix_excerpts(video: Path) -> list[dict]:
    ex_dir = UAT_DIR / "excerpts"
    ex_dir.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    # film times ≈ VO + card offsets (v03d mapping; end trim doesn't shift earlier times)
    clips = [
        ("excerpt_01_solid_disc", 20.5, 8.0),
        ("excerpt_02_a_world", 48.0, 8.0),
        ("excerpt_03_mimas", 84.0, 8.0),
        ("excerpt_04_late_arrival", 378.0, 8.0),
        ("excerpt_05_forever_disc", 514.0, 12.0),
        ("excerpt_leak_bonus", 194.5, 8.0),
        ("excerpt_next_bonus", 530.0, 12.0),
        ("excerpt_last_45s", max(0.0, v03d.probe(video) - 45.0), 45.0),
    ]
    out = []
    for name, start, dur in clips:
        dest = ex_dir / f"{name}.mp4"
        # clamp
        total = v03d.probe(video)
        if start >= total:
            start = max(0.0, total - dur)
        v03d.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{start:.3f}", "-t", f"{min(dur, total-start):.3f}", "-i", str(video),
            "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
            str(dest),
        ])
        shutil.copy2(dest, ART / f"saturn_v03f_{name}.mp4")
        out.append({"name": name, "start": start, "dur": dur, "path": str(dest)})
    return out


def main() -> None:
    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not PIC_SRC.exists():
        raise SystemExit(f"missing picture {PIC_SRC}")
    if not SHOT.exists():
        raise SystemExit(f"missing shot list {SHOT}")

    WORK.mkdir(parents=True, exist_ok=True)
    UAT_DIR.mkdir(parents=True, exist_ok=True)

    v03d.VO = VO
    v03d.WORK = WORK
    v03d.UAT_DIR = UAT_DIR
    v03d.OUT_LOCAL = OUT_LOCAL
    v03d.XFADE = XFADE

    rows = list(csv.DictReader(SHOT.open(newline="", encoding="utf-8")))
    total = float(rows[-1]["vo_out"])
    print(f"shot_list={SHOT.name} rows={len(rows)} total={total:.3f}s", flush=True)

    # Trim end hold off v03d picture (never cuts VO — VO ends ~546 film / before hold)
    picture = WORK / "picture_all.mp4"
    pic_dur = v03d.probe(PIC_SRC)
    # target picture length ≈ total - sum of breath/card xfades (v03d was pic_dur for 561.07 list)
    # v03d: list 561.07 → pic 559.1 (Δ2.0). v03j: 554.07 → expect ~552.1
    target_pic = pic_dur - END_HOLD_TRIM
    print(f"picture trim {pic_dur:.2f} → {target_pic:.2f} (−{END_HOLD_TRIM:.0f}s end hold)", flush=True)
    v03d.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(PIC_SRC), "-t", f"{target_pic:.3f}",
        "-c", "copy", str(picture),
    ])

    audio_parts = WORK / "audio_parts"
    if audio_parts.exists():
        shutil.rmtree(audio_parts)
    audio = v03d.build_audio(rows, total)

    # Mux — use shorter of picture/audio
    out_dur = min(v03d.probe(picture), v03d.probe(audio), total)
    fade_pic_start = max(0.0, out_dur - 2.0)
    v03d.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(picture), "-i", str(audio),
        "-filter_complex",
        f"[0:v]trim=0:{out_dur:.3f},setpts=PTS-STARTPTS,"
        f"fade=t=out:st={fade_pic_start:.3f}:d=2,format=yuv420p[v];"
        f"[1:a]atrim=0:{out_dur:.3f},asetpts=PTS-STARTPTS[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k",
        str(OUT_LOCAL),
    ])
    print(f"LOCAL {OUT_LOCAL} {v03d.probe(OUT_LOCAL):.2f}s", flush=True)

    lufs = v03d.measure_lufs(OUT_LOCAL)
    vo_lufs = v03d.measure_lufs(VO)
    print(f"LUFS mix={lufs.get('integrated_lufs')} VO={vo_lufs.get('integrated_lufs')}", flush=True)

    for name in ("contact12.png", "per_row.png"):
        src = HERE / "saturn_film/work_first_cut_v03d" / name
        if src.exists():
            chunk_write(src, UAT_DIR / f"saturn_first_cut_v03f_{name}")
            shutil.copy2(src, ART / f"saturn_first_cut_v03f_{name}")

    excerpts = write_fix_excerpts(OUT_LOCAL)
    chunk_write(OUT_LOCAL, UAT_DIR / "saturn_first_cut_v03f.mp4")

    h = hashlib.sha256()
    with open(OUT_LOCAL, "rb") as f:
        while True:
            b = f.read(500 * 1024)
            if not b:
                break
            h.update(b)

    stem_v = {}
    p = Path("/tmp/saturn_v03f/stem_verify.json")
    if p.exists():
        stem_v = json.loads(p.read_text())

    fixes = [
        {"id": "solid_disc", "vo": [19.22, 21.55], "engine": "eleven_v3 Ben Orbit Narrator"},
        {"id": "a_world", "vo": [46.52, 51.10], "engine": "eleven_v3 Ben Orbit Narrator"},
        {"id": "mimas", "vo": [81.48, 85.10], "engine": "eleven_v3 Ben Orbit Narrator"},
        {"id": "late_arrival", "vo": [364.50, 366.62], "engine": "eleven_v3 Ben Orbit Narrator"},
        {"id": "forever_disc", "vo": [495.74, 503.86], "engine": "eleven_v3 Ben Orbit Narrator"},
        {"id": "leak", "vo": [188.18, 188.60], "engine": "in-VO donor splice"},
        {"id": "next", "vo": [520.18, 520.80], "engine": "in-VO donor splice"},
    ]

    md = f"""# Saturn first cut v03f — five re-records + trim

**Not KEEP** until Ben reviews. LOCK master untouched. PR #99 untouched.

| | |
|---|---|
| File | `saturn_first_cut_v03f.mp4` |
| Duration | **{v03d.probe(OUT_LOCAL):.1f} s** |
| sha256 | `{h.hexdigest()}` |
| LUFS | **{lufs.get('integrated_lufs')}** (LRA {lufs.get('lra')}) |
| Shot list | `shot_list_v03j.csv` (end hold 15→8 s; no VO cut) |
| VO | LOCK + 5 EL retakes + leak/Next donors |

## Voice note
Channel LOCK VO is **ElevenLabs Ben Orbit Narrator** (`orbit_voice.py` / eleven_v3), not Vertex TTS.
Retakes use the same voice id + settings as LOCK so they match. Vertex remains the picture engine.

## Five Ben-flagged fixes (sentence-boundary splices)

| # | line | VO t | stem Whisper |
|--:|---|---|---|
| 1 | not a solid **disc** | 19.22–21.55 | solid disk/disc (full word — not “dic”) |
| 2 | around **a** world | 46.52–51.10 | a world |
| 3 | **Mimas** | 81.48–85.10 | Mimas |
| 4 | **late arrival** | 364.50–366.62 | late arrival |
| 5 | forever **disc** | 495.74–503.86 | forever disk/disc (full word) |

Whisper `medium.en` often spells the word **disk** (US). Gate: complete word, never Ben’s clipped “dic”.

## Also carried
- leak clarity splice · Next (was Net)

## Optional trim
End hold **15 s → 8 s** (−7 s). No VO touched. Runtime ~552 s vs v03d 559 s.

## Excerpts
See `excerpts/excerpt_01_solid_disc.mp4` … `excerpt_05_forever_disc.mp4`.
"""
    (WORK / "WORD_FIXES_AND_RUNTIME.md").write_text(md)
    chunk_write(md.encode(), UAT_DIR / "WORD_FIXES_AND_RUNTIME.md")
    (ART / "saturn_first_cut_v03f_WORD_FIXES.md").write_text(md)

    meta = {
        "cut": "v03f",
        "shot_list": "shot_list_v03j.csv",
        "vo": VO.name,
        "vo_base": "saturn_rings_vo_v03b_tightened_LOCK.wav",
        "fixes": fixes,
        "trim": {"end_hold_was": 15.0, "end_hold_now": 8.0, "saved_s": END_HOLD_TRIM},
        "duration": v03d.probe(OUT_LOCAL),
        "sha256": h.hexdigest(),
        "excerpts": excerpts,
        "loudness": {
            "mix_integrated_lufs": lufs.get("integrated_lufs"),
            "mix_lra": lufs.get("lra"),
            "vo_integrated_lufs": vo_lufs.get("integrated_lufs"),
        },
        "stem_verify": {k: v.get("text") if isinstance(v, dict) else v for k, v in stem_v.items() if k != "_all_ok"},
        "icloud": str(UAT_DIR),
        "keep": False,
        "note": "media iCloud only; nothing KEEP until Ben; PR #99 untouched; LOCK untouched",
    }
    (WORK / "META.json").write_text(json.dumps(meta, indent=2))
    chunk_write(json.dumps(meta, indent=2).encode(), UAT_DIR / "ARRIVAL.json")
    (ART / "saturn_first_cut_v03f_ARRIVAL.json").write_text(json.dumps(meta, indent=2))
    print("DONE", json.dumps({k: meta[k] for k in ("cut", "duration", "sha256", "loudness", "trim")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
