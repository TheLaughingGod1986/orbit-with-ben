#!/usr/bin/env python3
"""Assemble Moon Leaving Part 03 rough v05 — provisional FAIL→KEEP swap (no Flow remint yet) — variety plates minted with remaining Flow credits.

v03 base + swaps in the six Flow variety plates (sundial / cliffs / estuary / basin /
spinning Earth+Moon / night-ocean) where their VO beds land. Leaves v01–v03 and Parts
01/02 LOCKED untouched.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PLATES = PROJ / "04_Generated-Clips/part03/flow_world_v01"
REJECTS = [
    PROJ / "04_Generated-Clips/part03/_rejected_tidal_plane_2026-09-10",
    PROJ / "04_Generated-Clips/part03/_rejected_v02_sliced_planet_2026-09-10",
]
VO = PROJ / "02_Voiceover/parts/moon_leaving_part-03_vo_v01.wav"
MUSIC = PROJ / "05_Music/moon-leaving-part03_score_bed_v01.mp3"
WORK = PROJ / "07_Edit-Project/parts/_work_p03_v05"
OUT = PROJ / "07_Edit-Project/parts/moon_leaving_part-03_rough_v05.mp4"
META = PROJ / "07_Edit-Project/parts/moon_leaving_part-03_rough_v05_meta.json"
PLATE_MAP = PROJ / "07_Edit-Project/parts/part-03_plates_v05.json"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
PLATE_NATIVE_S = 8.0

# Variety swaps vs v03:
#   click_09  -> p03_18 sundial
#   harvest_01 -> p03_19 sea cliffs
#   p03_01    -> p03_20 estuary from orbit
#   gallery_04 -> p03_21 basin currents
#   harvest_03 -> p03_22 spinning Earth + Moon arc
#   harvest_02 -> p03_17 night ocean from orbit
CUTS: list[tuple[str, float, float | None, str]] = [
    ("p03_10_", 0.0, 8.0, "Here is the engine — still running under your feet · Earth raises tides on the Moon"),
    ("p03_02_", 0.0, 15.2, "Moon's gravity raises tides on Earth — oceans, a little in the crust"),
    ("p03_harvest_03_", 0.0, 19.5, "Those bulges do not sit perfectly under the Moon"),
    ("p03_14_", 0.0, 27.5, "Earth spins faster than a month; friction drags the bulge ahead"),
    ("p03_harvest_02_", 0.0, 35.4, "Leading bulge pulls forward on the Moon · gains orbital energy"),
    ("p03_04_", 0.0, 43.3, "Climbing to a wider orbit — centimetre by centimetre"),
    ("p03_05_", 0.0, 51.1, "Earth loses a little spin · your day lengthens"),
    ("p03_18_", 0.0, 57.2, "Hours added to the clock of a single rotation"),
    ("p03_click_05_", 0.0, 63.3, "A fight between two worlds — or a ledger written in water?"),
    ("p03_19_", 0.0, 71.0, "Negotiation in water and rock · friction spends rotation like currency"),
    ("p03_12_", 0.0, 79.0, "Moon banks that energy as distance · the ledger balances"),
    ("p03_20_", 0.0, 87.0, "The process is messy: coasts, basins, solid-Earth tides"),
    ("p03_21_", 0.0, 94.5, "Not a single pure note — but the net effect is clear"),
    ("p03_22_", 0.0, 102.1, "Could it reverse? Not while Earth has oceans and spins faster"),
    ("p03_11_", 0.0, 109.5, "As long as that gear turns, the Moon keeps cashing cheques"),
    ("p03_08_", 0.0, 117.5, "Fossils whisper corroboration: corals and shells record more days"),
    ("p03_09_", 0.0, 125.0, "A diary of a quicker world written in calcium"),
    ("p03_17_", 0.0, 133.0, "Suddenly deep time has receipts · if the Moon keeps leaving, what do we lose?"),
    ("p03_00_", 4.0, None, "Not just romance. Geometry."),
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def resolve(prefix: str) -> Path:
    hits = sorted(PLATES.glob(f"{prefix}*.mp4"))
    if len(hits) != 1:
        raise SystemExit(
            f"{prefix}: expected exactly one plate in {PLATES}, found {[h.name for h in hits]}"
        )
    return hits[0]


def main() -> None:
    for p in (VO, MUSIC):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    vo_dur = probe(VO)
    WORK.mkdir(parents=True, exist_ok=True)

    beds: list[Path] = []
    rows: list[dict] = []
    used: set[Path] = set()
    t = 0.0
    for i, (prefix, ss, out_t, line) in enumerate(CUTS, 1):
        src = resolve(prefix)
        if src in used:
            raise SystemExit(f"plate reused: {src.name} (orbit-cutscene-no-reuse)")
        used.add(src)
        end = vo_dur if out_t is None else out_t
        dur = round(end - t, 3)
        if dur <= 0:
            raise SystemExit(f"cut {i} has non-positive duration ({t} -> {end})")
        if ss + dur > PLATE_NATIVE_S + 1e-6:
            raise SystemExit(
                f"cut {i} {src.name}: needs {dur:.2f}s from in-point {ss:.2f}s "
                f"but plate is {PLATE_NATIVE_S:.0f}s (no freeze-pad / loop allowed)"
            )
        bed = WORK / f"bed_{i:02d}.mp4"
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{ss:.3f}",
                "-i",
                str(src),
                "-an",
                "-vf",
                "scale=1920:1080:force_original_aspect_ratio=decrease,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p,"
                "setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "18",
                "-color_range",
                "tv",
                "-colorspace",
                "bt709",
                "-color_primaries",
                "bt709",
                "-color_trc",
                "bt709",
                "-t",
                f"{dur:.3f}",
                str(bed),
            ]
        )
        beds.append(bed)
        rows.append(
            {
                "i": i,
                "name": src.name,
                "path": str(src),
                "in_point": ss,
                "start": round(t, 3),
                "end": round(end, 3),
                "dur": dur,
                "vo_line": line,
            }
        )
        t = end

    concat = WORK / "concat.txt"
    concat.write_text("".join(f"file '{b}'\n" for b in beds))
    picture = WORK / "picture.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(picture),
        ]
    )

    pic_dur = probe(picture)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(
            f"picture too short: pic={pic_dur:.2f}s vo={vo_dur:.2f}s (freeze-pad forbidden)"
        )
    master = min(pic_dur, vo_dur)

    fade_st = max(0.0, master - 2.5)
    graph = (
        f"[0:v]trim=0:{master:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]atrim=0:{master:.3f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,"
        "loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[vo][vo_sc];"
        f"[2:a]aloop=loop=-1:size=2e+09,atrim=0:{master:.3f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,"
        "loudnorm=I=-22:LRA=9:TP=-2,"
        f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_st:.3f}:d=2.5[music];"
        "[music][vo_sc]sidechaincompress=threshold=0.03:ratio=3.5:attack=30:release=600[ducked];"
        "[vo][ducked]amix=inputs=2:weights='1 0.85':normalize=0,alimiter=limit=0.90:level=false[a]"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(picture),
            "-i",
            str(VO),
            "-i",
            str(MUSIC),
            "-filter_complex",
            graph,
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-b:a",
            "192k",
            "-t",
            f"{master:.3f}",
            str(OUT),
        ]
    )

    out_dur = probe(OUT)
    if abs(out_dur - master) > 0.25:
        raise SystemExit(f"final encode truncated: out={out_dur:.2f}s master={master:.2f}s")

    PLATE_MAP.write_text(json.dumps(rows, indent=2) + "\n")
    META.write_text(
        json.dumps(
            {
                "out": str(OUT),
                "duration_s": probe(OUT),
                "vo": str(VO),
                "music": str(MUSIC),
                "plates": [r["name"] for r in rows],
                "cuts": rows,
                "picture_first": True,
                "orbit_in_open": False,
                "from": "moon_leaving_part-03_rough_v04.mp4",
                "provisional_swaps": ["p03_03→harvest_03", "gallery_03→p03_14", "harvest_00→harvest_02"],
                "tidal_cleared": False,
                "awaiting_flow_remint": True,
                "variety_plates": [
                    "p03_18",
                    "p03_19",
                    "p03_20",
                    "p03_21",
                    "p03_22",
                    "p03_17",
                ],
                "flow_credits_after": 0,
                "amix_weights": "1 0.85",
                "music_target_lufs": -22,
                "vo_target_lufs": -16,
                "sidechain": "threshold=0.03:ratio=3.5:attack=30:release=600",
                "quarantined": {
                    d.name: sorted(f.name for f in d.glob("*.mp4")) for d in REJECTS
                },
            },
            indent=2,
        )
        + "\n"
    )
    print(f"OUT {OUT} ({probe(OUT):.3f}s, {len(rows)} beds, vo={vo_dur:.3f}s)")

    if not UAT.exists():
        print("UAT folder missing — rough left in Edit-Project/parts/")
        return
    dest = UAT / "moon_leaving_part-03_rough_v05.mp4"
    shutil.copy2(OUT, dest)
    (UAT / "moon_leaving_part-03_STATUS.txt").write_text(
        "Part 03 (Why It Drifts) — ROUGH v05 PROVISIONAL ready for watch\n"
        f"File: {dest.name}\n"
        f"Duration: {probe(OUT):.1f}s\n"
        "v05 is a provisional FAIL→KEEP swap while Flow login is rate-limited. Still awaiting proper remint plates (p03A/B/C). Original: (Veo 3.1 Fast @ 10 credits/gen) on the queued variety plates:\n"
        "sundial (p03_18), sea cliffs (p03_19), estuary from orbit (p03_20), basin currents (p03_21),\n"
        "spinning Earth + Moon arc (p03_22), night ocean from orbit (p03_17).\n"
        "Flow balance is now 0 — wait for monthly reset or top up for more gens.\n"
        "Music mix unchanged from v03 (bed -22 LUFS, 3.5:1 duck, mix 0.85). No freeze-pad / loop.\n"
        "No Orbit. Picture-first open. Leave v01–v03 alongside for compare. Parts 01/02 LOCKED unchanged.\n"
    )
    print(f"UAT {dest}")


if __name__ == "__main__":
    main()
