#!/usr/bin/env python3
"""Replace excessive information cards with cinematic footage for v25."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
SOURCE_BED = EDIT / "_render_cache_v24/picture_bed_hook-first.mp4"
EDL_PATH = EDIT / "SECTION_EDL_v21_stable_orbit.json"
BASE_SCRIPT = EDIT / "_build_broadcast_noloop_v02.py"
POLISHED = ROOT / "04_Generated-Clips/03_Polished"
BRAND = POLISHED / "brand/orbit_brand_intro_v01.mp4"
OUT_DIR = EDIT / "_render_cache_v25"
OUT = OUT_DIR / "picture_bed_cinematic_cards-reduced.mp4"
REPORT = EDIT / "CINEMATIC_CARD_REDUCTION_v25.json"
TIMELINE = 635.475
BRAND_START = 10.0
BRAND_END = 12.0

# Six cards carry a real editorial job. The other 47 are replaced with moving
# imagery so narration, rather than typography, leads the experience.
KEEP_CARDS = {
    "card_hook_mystery_v01.mp4",
    "card_drake_blackboard_v01.mp4",
    "card_fermi_lunch_v01.mp4",
    "card_wow_1977_v01.mp4",
    "card_honest_v01.mp4",
    "card_end_invitation_v01.mp4",
}


def load_base():
    spec = importlib.util.spec_from_file_location("orbit_base", BASE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def transformed_interval(start: float, duration: float) -> tuple[float, float]:
    end = start + duration
    # v24 moved the original 0.75-second ident from the front to 11.072.
    if start >= 0.75 and end <= 11.822 + 0.001:
        return start - 0.75, end - 0.75
    return start, end


def subtract_brand(start: float, end: float) -> list[tuple[float, float]]:
    if end <= BRAND_START or start >= BRAND_END:
        return [(start, end)]
    pieces = []
    if start < BRAND_START:
        pieces.append((start, BRAND_START))
    if end > BRAND_END:
        pieces.append((BRAND_END, end))
    return pieces


def media_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in POLISHED.rglob("*.mp4"):
        index.setdefault(path.name, []).append(path)
    return index


def resolve(index: dict[str, list[Path]], filename: str) -> Path:
    candidates = index.get(filename, [])
    if not candidates:
        raise FileNotFoundError(filename)
    candidates.sort(key=lambda path: (
        "broll" not in str(path).lower(),
        "fill_plates" in str(path).lower(),
        len(str(path)),
    ))
    return candidates[0]


def choose_broll(shots: list[dict], shot_index: int, index: dict[str, list[Path]], duration: float, probe) -> Path:
    order = []
    for distance in range(1, len(shots)):
        order.extend((shot_index + distance, shot_index - distance))
    fallback = None
    for candidate_index in order:
        if not 0 <= candidate_index < len(shots):
            continue
        shot = shots[candidate_index]
        if shot["kind"] != "broll":
            continue
        try:
            path = resolve(index, shot["clip"])
        except FileNotFoundError:
            continue
        fallback = fallback or path
        if probe(path) >= min(4.0, duration):
            return path
    if fallback:
        return fallback
    raise RuntimeError(f"No replacement B-roll near shot {shot_index}")


def render_slice(source: Path, start: float, duration: float, output: Path) -> None:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{start:.3f}", "-i", str(source), "-t", f"{duration:.3f}",
        "-an", "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        str(output),
    ])


def render_brand(base, output: Path) -> None:
    raw = output.with_name(output.stem + "_raw.mp4")
    base.render_once(BRAND, BRAND_END - BRAND_START, raw, stable_text=True)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(raw),
        "-vf", "fade=t=in:st=0:d=0.18,fade=t=out:st=1.72:d=0.28",
        "-an", "-c:v", "libx264", "-preset", "veryfast",
        "-tune", "stillimage", "-crf", "14", str(output),
    ])


def normalise_frames(path: Path, frame_count: int) -> None:
    """Guarantee exact cumulative 30 fps boundaries before concatenation."""
    normalised = path.with_name(path.stem + "_frames.mp4")
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(path),
        "-vf", "fps=30,tpad=stop_mode=clone:stop_duration=10,format=yuv420p",
        "-frames:v", str(frame_count), "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        str(normalised),
    ])
    normalised.replace(path)


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = load_base()
    edl = json.loads(EDL_PATH.read_text())
    shots = edl["shots"]
    index = media_index()

    replacements = []
    for shot_index, shot in enumerate(shots):
        if shot["kind"] != "card" or shot["clip"] in KEEP_CARDS:
            continue
        start, end = transformed_interval(float(shot["start_s"]), float(shot["duration_s"]))
        for piece_start, piece_end in subtract_brand(start, end):
            if piece_end - piece_start < 0.08:
                continue
            replacement = choose_broll(
                shots, shot_index, index, piece_end - piece_start, base.probe
            )
            replacements.append({
                "start": piece_start,
                "end": piece_end,
                "kind": "broll_replacement",
                "removed_card": shot["clip"],
                "replacement": str(replacement),
            })

    replacements.append({
        "start": BRAND_START,
        "end": BRAND_END,
        "kind": "brand_hold",
        "removed_card": None,
        "replacement": str(BRAND),
    })
    replacements.sort(key=lambda item: item["start"])

    # Ensure intervals are ordered and non-overlapping.
    prior_end = 0.0
    for item in replacements:
        if item["start"] < prior_end - 0.001:
            raise RuntimeError(f"Overlapping replacement windows: {item}")
        prior_end = item["end"]

    with tempfile.TemporaryDirectory(prefix="orbit_v25_bed_") as temp:
        work = Path(temp)
        parts = []
        cursor = 0.0
        for replacement_index, item in enumerate(replacements):
            start, end = float(item["start"]), float(item["end"])
            if start > cursor + 0.001:
                original = work / f"part_{len(parts):04d}_original.mp4"
                render_slice(SOURCE_BED, cursor, start - cursor, original)
                normalise_frames(
                    original,
                    round(start * 30) - round(cursor * 30),
                )
                parts.append(original)

            replacement_part = work / f"part_{len(parts):04d}_{item['kind']}.mp4"
            if item["kind"] == "brand_hold":
                render_brand(base, replacement_part)
            else:
                base.render_once(
                    Path(item["replacement"]),
                    end - start,
                    replacement_part,
                    stable_text=False,
                    motion_seed=replacement_index,
                )
            normalise_frames(
                replacement_part,
                round(end * 30) - round(start * 30),
            )
            parts.append(replacement_part)
            cursor = end

        if cursor < TIMELINE - 0.001:
            tail = work / f"part_{len(parts):04d}_original.mp4"
            render_slice(SOURCE_BED, cursor, TIMELINE - cursor, tail)
            normalise_frames(
                tail,
                round(TIMELINE * 30) - round(cursor * 30),
            )
            parts.append(tail)

        listing = work / "concat.txt"
        listing.write_text("".join(f"file '{path}'\n" for path in parts))
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(listing),
            "-c", "copy", "-movflags", "+faststart", str(OUT),
        ])

    REPORT.write_text(json.dumps({
        "version": 25,
        "source_bed": str(SOURCE_BED),
        "output": str(OUT),
        "original_information_cards": 53,
        "kept_information_cards": sorted(KEEP_CARDS),
        "kept_information_card_count": len(KEEP_CARDS),
        "kept_chapter_cards": 8,
        "removed_information_card_count": 53 - len(KEEP_CARDS),
        "brand_start_seconds": BRAND_START,
        "brand_duration_seconds": BRAND_END - BRAND_START,
        "replacements": replacements,
    }, indent=2))
    print(json.dumps({
        "output": str(OUT),
        "cards_kept": len(KEEP_CARDS),
        "cards_replaced": 53 - len(KEEP_CARDS),
        "chapter_cards_kept": 8,
        "brand_hold_seconds": BRAND_END - BRAND_START,
    }, indent=2))


if __name__ == "__main__":
    build()
