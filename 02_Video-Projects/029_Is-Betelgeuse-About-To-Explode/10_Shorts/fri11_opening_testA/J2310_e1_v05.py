#!/usr/bin/env python3
"""J2310 — local E1 tail cut for the Fri 11 Dec Test A Short.

Leaves 029_short_fri11_opening_testA_v04.mp4, its hash and the upload
manifest untouched. Writes v05 beside it. £0. No generation.

The only picture change is the loop: the v04 end card (31.88–33.88 s,
"Full film on the channel") is replaced by a 0.30 s crossfade onto frame 0,
ending at 32.68 s. Spoken lines, opening cuts and the J0991 meta waiver stay.

The shipped v05 audio uses this recipe with the bed end fade shortened to
0.12 s so the music is still up at the loop. A straight call of
asm.build_audio keeps the v04 0.50 s fade.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = FILM.parents[1]
EXPORT = HERE / "06_Final-Exports"
SRC = EXPORT / "029_short_fri11_opening_testA_v04.mp4"
STEM = "029_short_fri11_opening_testA_v05"
FINAL = EXPORT / f"{STEM}.mp4"
WORK = Path("/private/tmp/j2310-recut")

LAST_WORD = 31.58
XFADE_AT = 31.70
XFADE_D = 0.30
END = 32.68  # tail = END - LAST_WORD = 1.10 s
PRESERVED_SHA = "ff4194857a027cfc5f93551ef398125276e6bcfb9cd3ce2fd18d8ee1134e2405"

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(HERE.parent))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import _assemble_029_shorts_v04 as asm  # noqa: E402


def run(cmd: list) -> None:
    sp.run([str(c) for c in cmd], check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dur(path: Path) -> float:
    return float(sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def main() -> int:
    if sha256(SRC) != PRESERVED_SHA:
        raise SystemExit(f"v04 hash changed; refusing to cut from {sha256(SRC)}")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    frame0 = WORK / "frame0.png"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-vf", "select=eq(n\\,0)", "-frames:v", "1", str(frame0)])

    first = round(XFADE_AT + XFADE_D, 3)  # 32.00
    second = round(END - XFADE_AT, 3)  # 0.98
    picture = WORK / "picture.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(SRC),
        "-loop", "1", "-framerate", "30", "-t", f"{second:.3f}", "-i", str(frame0),
        "-filter_complex",
        (
            f"[0:v]trim=0:{first:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p[a];"
            f"[1:v]scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setpts=PTS-STARTPTS[b];"
            f"[a][b]xfade=transition=fade:duration={XFADE_D:.2f}:offset={XFADE_AT:.2f},format=yuv420p[v]"
        ),
        "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
        str(picture),
    ])

    spec = next(s for s in asm.SHORTS if s["slug"] == "fri11_opening_testA")
    slices, words, last = asm.build_voice(spec["sentences"], spec["lead"], spec["gap"])
    if abs(last - LAST_WORD) > 0.02:
        raise SystemExit(f"voice end {last} != preserved last word {LAST_WORD}")
    aud = asm.build_audio(
        WORK,
        slices,
        END,
        [("whoosh", 0.0, -6.0), ("tick", 9.0, -8.0), ("tick", 16.07, -8.0)],
    )
    cal_wav, aac_i, aac_tp = asm.calibrate_aac_wav(WORK, WORK / "mix.wav", END)
    aud["mix_lufs"] = aac_i
    aud["aac_lufs"] = aac_i
    aud["aac_tp_dbtp"] = aac_tp
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(picture), "-i", str(cal_wav),
        "-map", "0:v:0", "-map", "1:a:0",
        *shorts_encode_args(fps=30),
        "-movflags", "+faststart", "-t", f"{END:.3f}",
        str(FINAL),
    ])
    if sha256(SRC) != PRESERVED_SHA:
        raise SystemExit("v04 hash changed during the cut")

    phone = EXPORT / f"{STEM}_PHONE.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(FINAL),
        "-vf", "scale=720:1280:flags=lanczos",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
        str(phone),
    ])
    cover_src = EXPORT / "029_short_fri11_opening_testA_v04_cover.jpg"
    cover = EXPORT / f"{STEM}_cover.jpg"
    shutil.copy2(cover_src, cover)

    cuts = json.loads((EXPORT / "029_short_fri11_opening_testA_v04_cuts.json").read_text())
    for row in cuts:
        if row["row"] == "s10_lasillab":
            row["timeline_out"] = XFADE_AT
        if row["row"] == "s11_end":
            row["row"] = "s11_loop"
            row["timeline_in"] = XFADE_AT
            row["timeline_out"] = END
            row["source"] = "frame0_hold_fri11_opening_testA.png"
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["video"] = True
            row["end_card"] = False
            row["note"] = "0.30s crossfade onto frame 0. No end card."
    (EXPORT / f"{STEM}_cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")
    pool = json.loads((EXPORT / "029_short_fri11_opening_testA_v04_pool.json").read_text())
    pool.append({
        "file_id": "frame0_hold_fri11_opening_testA.png",
        "title": "opening frame held for the loop",
    })
    (EXPORT / f"{STEM}_pool.json").write_text(json.dumps(pool, indent=2) + "\n")
    (EXPORT / f"{STEM}_words.json").write_text(json.dumps(words, indent=2) + "\n")
    joined = " ".join(w["w"] for w in words)
    (EXPORT / f"{STEM}_transcript.txt").write_text(joined + "\n")
    for name in ("stem_vo.wav", "stem_bed.wav", "stem_sfx.wav"):
        shutil.copy2(WORK / name, EXPORT / f"{STEM}_{name}")

    holds = []
    for row in cuts:
        holds.append((round(row["timeline_out"] - row["timeline_in"], 3), row["row"]))
    f0 = np.asarray(Image.open(frame0).convert("RGB").resize((1080, 1920)), dtype=np.int16)
    last_png = WORK / "last.png"
    last_n = max(0, round(dur(FINAL) * 30) - 1)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(FINAL), "-vf", f"select=eq(n\\,{last_n})", "-frames:v", "1", str(last_png)])
    fl = np.asarray(Image.open(last_png).convert("RGB").resize((1080, 1920)), dtype=np.int16)
    loop_diff = round(float(np.abs(f0 - fl).mean()), 3)

    meta = {
        "job": "J2310",
        "label": "EXCEPTION",
        "e1_label": (
            "EXCEPTION. Test A opening, spoken lines and the J0991 spoken-meta waiver are unchanged. "
            "This is a local tail candidate, not a full E1 PASS and not a swap."
        ),
        "slug": "fri11_opening_testA",
        "stem": STEM,
        "day": "Fri 11 Dec (Test A)",
        "air_date": "2026-12-11",
        "title": "Is Betelgeuse Really About to Explode?",
        "youtube_id_preserved": "k2kEaA7ICjc",
        "source_v04_sha256": PRESERVED_SHA,
        "long": {"id": "vP1BbqZ_dnM", "title": "Is Betelgeuse About to Explode?"},
        "spoken": joined,
        "last_word_end_s": LAST_WORD,
        "duration_s": round(dur(FINAL), 3),
        "tail_s": round(dur(FINAL) - LAST_WORD, 3),
        "loop_crossfade_s": XFADE_D,
        "loop_diff_mean_abs": loop_diff,
        "end_card": None,
        "sha256": sha256(FINAL),
        "phone_sha256": sha256(phone),
        "phone_bytes": phone.stat().st_size,
        "words_count": len(words),
        "words_file": str(EXPORT / f"{STEM}_words.json"),
        "meta_promise_lint": spec["meta_promise_lint"],
        "audio": aud,
        "max_hold_s": max(holds)[0],
        "max_hold_row": max(holds)[1],
        "spend": "£0",
        "aac_measured": {"lufs": aac_i, "true_peak_dbtp": aac_tp},
    }
    (EXPORT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({
        "final": str(FINAL),
        "duration_s": meta["duration_s"],
        "tail_s": meta["tail_s"],
        "sha256": meta["sha256"],
        "v04_sha": sha256(SRC),
        "aac_lufs": aac_i,
        "aac_tp": aac_tp,
        "loop_diff": loop_diff,
        "last_word": last,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
