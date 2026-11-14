#!/usr/bin/env python3
"""Build j01_journey_laid_score_v02.wav + plan + manifest from the exact laid score stems across J01_Journey_v03.mp4."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SCRATCH = Path("/Volumes/MiniWork/scratch/J2221")
STEMS = SCRATCH / "stems" / "ducked"
WORK = SCRATCH / "laid_score_v02_work"
FILM = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World")
MUSIC_DIR = FILM / "05_Music"
EDIT_DIR = FILM / "07_Edit-Project"
V03 = EDIT_DIR / "J01_Journey_v03.mp4"
SR = 48000
XFADE = 0.50

# Exact score sources and their laid gain in the source master cuts:
# - 027, 028, 026, 029 files are already the ducked/laid stems (-31.9 to -35.4 LUFS) -> gain 1.0 (0.0 dB)
# - 023, 024, 025 files are raw score beds (-14.4 to -16.9 LUFS) laid with volume=0.134 (-17.46 dB) in their assemblers
PART_BEDS = {
    "part1_027": {
        "film": "027",
        "source": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/05_Music/earth-spin_score_take2_straight_v01j.wav",
        "gain": 1.0,
        "gain_db": 0.0,
        "gain_basis": "_mix_earth_spin_v01m.py (already ducked laid stem at -31.9 LUFS)",
        "windows": [(0.0, 443.50)],
    },
    "part2_023": {
        "film": "023",
        "source": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01_full.mp3",
        "gain": 0.134,
        "gain_db": -17.46,
        "gain_basis": "_assemble_venus_full_v05e.py line 311 (volume=0.134)",
        "windows": [(0.0, 35.80), (43.20, 212.20), (218.20, 504.80)],
    },
    "part3_025": {
        "film": "025",
        "source": "/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/05_Music/mars-robot_score_bed_v02_full.mp3",
        "gain": 0.134,
        "gain_db": -17.46,
        "gain_basis": "_assemble_mars_robot_full_v03f.py line 323 (volume=0.134)",
        "windows": [(0.0, 29.80), (40.80, 224.50), (231.00, 483.20)],
    },
    "part4_028": {
        "film": "028",
        "source": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/05_Music/gliese_score_bed_v03.mp3",
        "gain": 1.0,
        "gain_db": 0.0,
        "gain_basis": "_build_gliese_audio_v03.py (already ducked laid stem at -35.4 LUFS)",
        "windows": [(0.0, 30.80), (42.20, 204.20), (209.80, 469.80)],
    },
    "part5_026": {
        "film": "026",
        "source": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.wav",
        "gain": 1.0,
        "gain_db": 0.0,
        "gain_basis": "_assemble_nearest_star_rough_v06.py (already ducked laid stem at -34.0 LUFS)",
        "windows": [(0.0, 20.50), (32.80, 224.40), (232.00, 491.30)],
    },
    "part6_024": {
        "film": "024",
        "source": "/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/05_Music/light-speed_score_bed_v01_full.mp3",
        "gain": 0.134,
        "gain_db": -17.46,
        "gain_basis": "_assemble_light_speed_full_v05.py line 261 (volume=0.134)",
        "windows": [(0.0, 28.30), (41.60, 213.10), (220.00, 483.00)],
    },
    "part7_029": {
        "film": "029",
        "source": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/05_Music/betelgeuse_score_bed_v01.mp3",
        "gain": 1.0,
        "gain_db": 0.0,
        "gain_basis": "_build_betelgeuse_audio_v01.py (already ducked laid stem at -34.2 LUFS)",
        "windows": [(0.0, 22.10), (37.20, 242.20), (247.60, 514.80)],
    },
}

LINK_META = {
    "cold": ("026", "Cold Open ducked Option A bed (stems/ducked/cold_bed.wav)"),
    "card1": ("026", "Chapter Card 1 ducked Option A bed (stems/ducked/card1_bed.wav, -20 dB)"),
    "bridge1": ("023", "Bridge 1 ducked Option A bed (stems/ducked/bridge1_bed.wav)"),
    "card2": ("023", "Chapter Card 2 ducked Option A bed (stems/ducked/card2_bed.wav, -20 dB)"),
    "bridge2": ("023", "Bridge 2 ducked Option A bed (stems/ducked/bridge2_bed.wav)"),
    "card3": ("023", "Chapter Card 3 ducked Option A bed (stems/ducked/card3_bed.wav, -20 dB)"),
    "bridge3": ("024", "Bridge 3 ducked Option A bed (stems/ducked/bridge3_bed.wav)"),
    "card4": ("024", "Chapter Card 4 ducked Option A bed (stems/ducked/card4_bed.wav, -20 dB)"),
    "bridge4": ("026", "Bridge 4 ducked Option A bed (stems/ducked/bridge4_bed.wav)"),
    "card5": ("026", "Chapter Card 5 ducked Option A bed (stems/ducked/card5_bed.wav, -20 dB)"),
    "bridge5": ("024", "Bridge 5 ducked Option A bed (stems/ducked/bridge5_bed.wav)"),
    "card6": ("024", "Chapter Card 6 ducked Option A bed (stems/ducked/card6_bed.wav, -20 dB)"),
    "bridge6": ("026", "Bridge 6 ducked Option A bed (stems/ducked/bridge6_bed.wav)"),
    "card7": ("026", "Chapter Card 7 ducked Option A bed (stems/ducked/card7_bed.wav, -20 dB)"),
    "close": ("026", "Closing + 18s End Hold ducked Option A bed (stems/ducked/close_bed.wav)"),
}

FILM_ORDER = [
    ("cold", "link"),
    ("card1", "link"),
    ("part1_027", "part"),
    ("bridge1", "link"),
    ("card2", "link"),
    ("part2_023", "part"),
    ("bridge2", "link"),
    ("card3", "link"),
    ("part3_025", "part"),
    ("bridge3", "link"),
    ("card4", "link"),
    ("part4_028", "part"),
    ("bridge4", "link"),
    ("card5", "link"),
    ("part5_026", "part"),
    ("bridge5", "link"),
    ("card6", "link"),
    ("part6_024", "part"),
    ("bridge6", "link"),
    ("card7", "link"),
    ("part7_029", "part"),
    ("close", "link"),
]

def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "")[-800:])

def probe(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True).strip())

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def build_part_bed(name: str) -> Path:
    info = PART_BEDS[name]
    out = WORK / f"{name}_bed.wav"
    target_dur = probe(SCRATCH / "audio_v03" / f"{name}.wav")
    src = Path(info["source"])
    gain = info["gain"]
    slices = []
    for idx, (a, b) in enumerate(info["windows"]):
        sl = WORK / f"{name}_slice_{idx}.wav"
        dur = b - a
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{a:.3f}", "-i", str(src), "-t", f"{dur:.3f}",
            "-af", f"volume={gain},aresample={SR},aformat=channel_layouts=stereo",
            "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(sl)
        ])
        slices.append(sl)
    joined = WORK / f"{name}_joined.wav"
    if len(slices) == 1:
        joined = slices[0]
    else:
        parts = []
        acc_label = "[0:a]"
        for i in range(1, len(slices)):
            parts.append(f"{acc_label}[{i}:a]acrossfade=d={XFADE}:c1=tri:c2=tri[ax{i}]")
            acc_label = f"[ax{i}]"
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        for p in slices:
            cmd += ["-i", str(p)]
        cmd += ["-filter_complex", ";".join(parts), "-map", acc_label,
                "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(joined)]
        run(cmd)
    # Match exact duration of SCRATCH / audio_v03 / {name}.wav
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(joined),
        "-af", f"apad=whole_dur={target_dur:.6f},atrim=0:{target_dur:.6f},asetpts=PTS-STARTPTS",
        "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(out)
    ])
    return out

def build_link_bed(name: str) -> Path:
    out = WORK / f"{name}_bed.wav"
    target_dur = probe(SCRATCH / "audio_v03" / f"{name}.wav")
    src = STEMS / f"{name}_bed.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src),
        "-af", f"apad=whole_dur={target_dur:.6f},atrim=0:{target_dur:.6f},asetpts=PTS-STARTPTS",
        "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(out)
    ])
    return out

def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(REPO / "scripts"))
    import sfx_kit, music_gate

    seg_files = []
    manifest_rows = []
    timeline_cursor = 0.0
    for idx, (name, kind) in enumerate(FILM_ORDER):
        p = build_part_bed(name) if kind == "part" else build_link_bed(name)
        seg_files.append(p)
        dur = probe(p)
        _, seg_lufs = sfx_kit.ebur128(p)
        t_in = 0.0 if idx == 0 else timeline_cursor - XFADE
        t_out = t_in + dur - (XFADE if idx < len(FILM_ORDER) - 1 else 0.0)
        timeline_cursor = t_in + dur
        if kind == "part":
            info = PART_BEDS[name]
            manifest_rows.append({
                "index": idx + 1,
                "segment": name,
                "kind": "inherited_part_score",
                "film": info["film"],
                "source_file": info["source"],
                "source_sha256": sha256(Path(info["source"])),
                "source_windows_s": info["windows"],
                "applied_gain_linear": info["gain"],
                "applied_gain_db": info["gain_db"],
                "gain_basis": info["gain_basis"],
                "segment_duration_s": round(dur, 3),
                "timeline_in_s": round(t_in, 3),
                "timeline_out_s": round(t_out, 3),
                "integrated_lufs": round(seg_lufs, 2),
            })
        else:
            bfilm, note = LINK_META[name]
            src_file = STEMS / f"{name}_bed.wav"
            manifest_rows.append({
                "index": idx + 1,
                "segment": name,
                "kind": "linking_score_cue",
                "film": bfilm,
                "source_file": str(src_file),
                "source_sha256": sha256(src_file),
                "source_windows_s": [[0.0, round(dur, 3)]],
                "applied_gain_linear": 1.0,
                "applied_gain_db": 0.0,
                "gain_basis": note,
                "segment_duration_s": round(dur, 3),
                "timeline_in_s": round(t_in, 3),
                "timeline_out_s": round(t_out, 3),
                "integrated_lufs": round(seg_lufs, 2),
            })

    parts = []
    acc_label = "[0:a]"
    for i in range(1, len(seg_files)):
        parts.append(f"{acc_label}[{i}:a]acrossfade=d={XFADE}:c1=tri:c2=tri[ax{i}]")
        acc_label = f"[ax{i}]"
    local_out = WORK / "j01_journey_laid_score_v02.wav"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for p in seg_files:
        cmd += ["-i", str(p)]
    cmd += ["-filter_complex", ";".join(parts), "-map", acc_label,
            "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(local_out)]
    run(cmd)

    dur_out = probe(local_out)
    _, total_lufs = sfx_kit.ebur128(local_out)
    gap_s, gap_at = music_gate.longest_gap(music_gate.decode(local_out, None))
    print(f"Built local laid score: {dur_out:.3f}s, integrated={total_lufs:.2f} LUFS, longest_gap={gap_s}s at {gap_at}s")
    for r in manifest_rows:
        print(f"  {r['index']:02d} {r['segment']:10s} {r['timeline_in_s']:7.2f}-{r['timeline_out_s']:7.2f}s ({r['segment_duration_s']:6.2f}s) {r['integrated_lufs']:6.2f} LUFS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
