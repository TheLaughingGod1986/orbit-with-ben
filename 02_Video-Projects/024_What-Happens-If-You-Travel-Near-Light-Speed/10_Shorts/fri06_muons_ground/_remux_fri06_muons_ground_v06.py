#!/usr/bin/env python3
"""J3136: remux fri06_muons_ground_v06. Picture is the v05 video stream, copied.
VO and SFX are the locked _work_v02 stems. Only the music bed is replaced.
No YouTube change. £0.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]  # 024_What-Happens-If-You-Travel-Near-Light-Speed
WORK = HERE / "_work_v06"
OUT = HERE / "06_Final-Exports"
V05 = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2550_muons_v05/fri06_muons_ground_v05.mp4")
V05_SHA = "1232cb5041f9aae09e51cbf3895136142e19af379331e2b93a8607d593b331b8"
BED = FILM / "05_Music/fri06_muons_ground_score_bed_v01.mp3"
VO = WORK / "stem_vo.wav"
SFX = WORK / "stem_sfx.wav"
FINAL = OUT / "fri06_muons_ground_v06.mp4"
TOTAL = 22.2


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def integrated_lufs(path: Path) -> float:
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    line = [ln for ln in p.stderr.splitlines() if "I:" in ln and "LUFS" in ln][-1]
    return float(line.split("I:")[1].split("LUFS")[0].strip())


def main() -> None:
    got = sha256(V05)
    if got != V05_SHA:
        raise SystemExit(f"v05 hash {got} != locked {V05_SHA}")
    for p in (VO, SFX, BED):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    vo_i = integrated_lufs(VO)
    bed_i = integrated_lufs(BED)
    # 28 LU under the VO before the mix loudnorm. The plucks are peakier than a pad,
    # and the level gate needs the bed 10 LU under the VO's momentary level while it speaks.
    bed_gain = (vo_i - 28.0) - bed_i
    bed_wav = WORK / "stem_bed.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(BED), "-af", f"volume={bed_gain:.2f}dB,atrim=0:{TOTAL},apad=whole_dur={TOTAL}",
         "-ar", "48000", "-ac", "2", str(bed_wav)])
    mix = (
        f"[1:a]atrim=0:{TOTAL},apad=whole_dur={TOTAL},aresample=48000[v];"
        f"[2:a]atrim=0:{TOTAL},apad=whole_dur={TOTAL},aresample=48000[b];"
        f"[3:a]atrim=0:{TOTAL},apad=whole_dur={TOTAL},aresample=48000[s];"
        "[v][b][s]amix=inputs=3:duration=first:normalize=0,"
    )
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(V05), "-i", str(VO), "-i", str(bed_wav), "-i", str(SFX),
         "-filter_complex", mix + "loudnorm=I=-14:TP=-2:LRA=11:print_format=json[a]",
         "-map", "[a]", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    norm = (
        f"loudnorm=I=-14:TP=-2.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:"
        "linear=true,alimiter=limit=0.89:level=false,aresample=48000[a]"
    )
    OUT.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(V05), "-i", str(VO), "-i", str(bed_wav), "-i", str(SFX),
         "-filter_complex", mix + norm,
         "-map", "0:v:0", "-c:v", "copy", "-map", "[a]", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(FINAL)])
    info = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                           "format=duration:stream=codec_type,codec_name,nb_frames,width,height",
                           "-of", "json", str(FINAL)]).stdout)
    print(json.dumps({
        "file": str(FINAL),
        "sha256": sha256(FINAL),
        "v05_sha256": got,
        "vo_sha256": sha256(VO),
        "sfx_sha256": sha256(SFX),
        "bed_sha256": sha256(BED),
        "vo_lufs": round(vo_i, 2),
        "bed_lufs": round(bed_i, 2),
        "bed_gain_db": round(bed_gain, 2),
        "probe": info,
    }, indent=2))


if __name__ == "__main__":
    main()
