#!/usr/bin/env python3
"""Build the v25 cinematic bed directly from source assets and intended timings."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
EDL_PATH = EDIT / "SECTION_EDL_v21_stable_orbit.json"
POLISHED = ROOT / "04_Generated-Clips/03_Polished"
BRAND_INTRO = POLISHED / "brand/orbit_brand_intro_v01.mp4"
BRAND_OUTRO = POLISHED / "brand/orbit_brand_outro_subscribe_v01.mp4"
OUT_DIR = EDIT / "_render_cache_v25"
OUT = OUT_DIR / "picture_bed_cinematic_fresh.mp4"
REPORT = EDIT / "CINEMATIC_CARD_REDUCTION_v25.json"
FPS = 30
TIMELINE = 635.475
BRAND_START = 10.0
BRAND_END = 12.0
OUTRO_START = 625.583

KEEP_CARDS = {
    "card_hook_mystery_v01.mp4",
    "card_drake_blackboard_v01.mp4",
    "card_fermi_lunch_v01.mp4",
    "card_wow_1977_v01.mp4",
    "card_honest_v01.mp4",
    "card_end_invitation_v01.mp4",
}


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def probe(path: Path) -> float:
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


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


def choose_broll(shots: list[dict], shot_index: int, index: dict[str, list[Path]], duration: float) -> Path:
    fallback = None
    for distance in range(1, len(shots)):
        for candidate_index in (shot_index + distance, shot_index - distance):
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


def transform_time(start: float, end: float) -> tuple[float, float]:
    # Remove the original 0.75-second opening ident. Everything after the
    # opening question keeps its established absolute timeline.
    if start >= 0.75 and end <= 11.822 + 0.001:
        return start - 0.75, end - 0.75
    return start, end


def override(segments: list[dict], start: float, end: float, replacement: dict) -> list[dict]:
    output = []
    for segment in segments:
        a, z = segment["start"], segment["end"]
        if z <= start or a >= end:
            output.append(segment)
            continue
        if a < start:
            before = dict(segment)
            before["end"] = start
            output.append(before)
        if z > end:
            after = dict(segment)
            after["offset"] += end - a
            after["start"] = end
            output.append(after)
    output.append({**replacement, "start": start, "end": end, "offset": 0.0})
    return sorted(output, key=lambda item: item["start"])


def render_segment(segment: dict, output: Path, frame_count: int, seed: int) -> None:
    path = Path(segment["path"])
    offset = float(segment.get("offset", 0.0))
    stable = bool(segment.get("stable", False))
    source_duration = probe(path)
    available = max(0.04, source_duration - offset)
    target_duration = frame_count / FPS
    take = min(target_duration, available)

    if stable:
        vf = (
            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,fps=30,"
            "tpad=stop_mode=clone:stop_duration=12,format=yuv420p"
        )
    else:
        mode = seed % 4
        if mode == 0:
            x, y = "(iw-ow)/2", f"(ih-oh)/2-((ih-oh)/2)*(t/{max(take,0.1):.3f})"
        elif mode == 1:
            x, y = "(iw-ow)/2", f"((ih-oh)/2)*(t/{max(take,0.1):.3f})"
        elif mode == 2:
            x, y = f"(iw-ow)*(t/{max(take,0.1):.3f})", "(ih-oh)/2"
        else:
            x, y = f"(iw-ow)*(1-t/{max(take,0.1):.3f})", "(ih-oh)/2"
        vf = (
            "scale=2150:1210:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1920:1080:x='{x}':y='{y}',fps=30,"
            "tpad=stop_mode=clone:stop_duration=12,format=yuv420p"
        )

    command = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{offset:.3f}", "-i", str(path),
        "-an", "-vf", vf, "-frames:v", str(frame_count),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    ]
    if stable:
        command += ["-tune", "stillimage"]
    command.append(str(output))
    run(command)


def build_segments(shots: list[dict], index: dict[str, list[Path]]) -> tuple[list[dict], list[dict]]:
    segments = []
    removals = []
    for shot_index, shot in enumerate(shots):
        if shot["kind"] in ("brand_intro", "brand_outro"):
            continue
        original_start = float(shot["start_s"])
        original_end = original_start + float(shot["duration_s"])
        if original_start >= TIMELINE:
            continue
        start, end = transform_time(original_start, min(original_end, TIMELINE))
        if end <= 0 or start >= TIMELINE:
            continue

        if shot["kind"] == "card" and shot["clip"] not in KEEP_CARDS:
            path = choose_broll(shots, shot_index, index, end - start)
            kind = "broll_replacement"
            stable = False
            removals.append({
                "card": shot["clip"],
                "start": start,
                "end": end,
                "replacement": str(path),
            })
        else:
            path = resolve(index, shot["clip"])
            kind = shot["kind"]
            stable = shot["kind"] in ("card", "chapter")

        segments.append({
            "start": start,
            "end": end,
            "path": str(path),
            "offset": 0.0,
            "kind": kind,
            "stable": stable,
        })

    segments.sort(key=lambda item: item["start"])
    # Snap millisecond rounding differences without changing editorial lengths.
    cursor = 0.0
    for segment in segments:
        if abs(segment["start"] - cursor) < 0.015:
            segment["start"] = cursor
        cursor = segment["end"]

    segments = override(segments, BRAND_START, BRAND_END, {
        "path": str(BRAND_INTRO), "kind": "brand_hold", "stable": True,
    })
    segments = override(segments, OUTRO_START, TIMELINE, {
        "path": str(BRAND_OUTRO), "kind": "brand_outro", "stable": True,
    })
    return segments, removals


def validate_coverage(segments: list[dict]) -> None:
    cursor = 0.0
    for segment in segments:
        if segment["start"] > cursor + 0.02:
            raise RuntimeError(f"Timeline gap {cursor:.3f}-{segment['start']:.3f}")
        if segment["start"] < cursor - 0.02:
            raise RuntimeError(f"Timeline overlap at {segment['start']:.3f}")
        cursor = segment["end"]
    if cursor < TIMELINE - 0.02:
        raise RuntimeError(f"Timeline ends early at {cursor:.3f}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shots = json.loads(EDL_PATH.read_text())["shots"]
    index = media_index()
    segments, removals = build_segments(shots, index)
    validate_coverage(segments)

    with tempfile.TemporaryDirectory(prefix="orbit_v25_fresh_") as temp:
        work = Path(temp)
        parts = []
        for segment_index, segment in enumerate(segments):
            start_frame = round(segment["start"] * FPS)
            end_frame = round(segment["end"] * FPS)
            frame_count = end_frame - start_frame
            if frame_count <= 0:
                continue
            part = work / f"part_{segment_index:04d}.mp4"
            render_segment(segment, part, frame_count, segment_index)
            parts.append(part)
            if segment_index and segment_index % 30 == 0:
                print(f"rendered {segment_index}/{len(segments)}")

        listing = work / "concat.txt"
        listing.write_text("".join(f"file '{path}'\n" for path in parts))
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(listing),
            "-c", "copy", "-movflags", "+faststart", str(OUT),
        ])

    REPORT.write_text(json.dumps({
        "version": 25,
        "method": "fresh source rebuild using intended EDL timings",
        "output": str(OUT),
        "original_information_cards": 53,
        "retained_information_cards": sorted(KEEP_CARDS),
        "retained_information_card_count": len(KEEP_CARDS),
        "replaced_information_card_count": len(removals),
        "retained_chapter_cards": 8,
        "brand_start_seconds": BRAND_START,
        "brand_duration_seconds": BRAND_END - BRAND_START,
        "outro_start_seconds": OUTRO_START,
        "segments": segments,
        "removals": removals,
    }, indent=2))
    print(json.dumps({
        "output": str(OUT),
        "duration": probe(OUT),
        "cards_kept": len(KEEP_CARDS),
        "cards_replaced": len(removals),
        "chapters_kept": 8,
        "brand_hold_seconds": BRAND_END - BRAND_START,
    }, indent=2))


if __name__ == "__main__":
    main()
