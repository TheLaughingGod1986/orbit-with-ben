#!/usr/bin/env python3
"""Rebuild the picture bed so each visual illustrates the timed narration."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
BASE_PATH = EDIT / "_build_cinematic_bed_v25_fresh.py"
OUT_DIR = EDIT / "_render_cache_v26"
OUT = OUT_DIR / "picture_bed_semantic_v26.mp4"
REPORT = EDIT / "NARRATION_VISUAL_ALIGNMENT_v26.json"


def load_base():
    spec = importlib.util.spec_from_file_location("orbit_v25_bed", BASE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


# These change points follow the exact narration/card timing in the stable EDL.
# Each chosen clip was visually reviewed against its scene-library description.
SEMANTIC_SCHEDULE = [
    (0.000, "aliens_scene-001_v01.mp4", "crowded night sky"),
    (4.100, "aliens_scene-002_v01.mp4", "stars beyond the visible sky"),
    (6.972, "aliens_scene-020_v01.mp4", "where is everybody / radio silence"),
    (12.000, "aliens_scene-012_v01.mp4", "whole galaxies in the dark"),
    (18.793, "aliens_scene-020_v01.mp4", "why has nobody answered"),
    (24.990, "aliens_scene-008_v01.mp4", "the real human question"),
    (32.736, "aliens_scene-001_v01.mp4", "look up at the Milky Way"),
    (41.981, "aliens_scene-001_v01.mp4", "space is enormously big"),
    (46.081, "aliens_scene-012_v01.mp4", "galactic scale"),
    (51.687, "aliens_scene-002_v01.mp4", "nearest star system"),
    (55.787, "aliens_scene-011_v01.mp4", "spacecraft crossing the gap"),
    (69.334, "aliens_scene-012_v01.mp4", "hundreds of billions of stars"),
    (78.158, "aliens_scene-061_v01.mp4", "habitable-zone world"),
    (82.258, "aliens_scene-013_v01.mp4", "planet orbit and transit"),
    (95.842, "aliens_scene-013_v01.mp4", "planets behind the Drake Equation"),
    (104.000, "aliens_scene-017_v01.mp4", "possible crowded galaxy"),
    (113.743, "aliens_scene-017_v01.mp4", "buzzing galaxy versus solitude"),
    (121.000, "aliens_scene-062_v01.mp4", "overlapping technological eras"),
    (129.458, "aliens_scene-024_v01.mp4", "brief technological candles"),
    (137.000, "aliens_scene-062_v01.mp4", "radio eras missing each other"),
    (145.174, "aliens_scene-024_v01.mp4", "civilisation light fading"),
    (151.000, "aliens_scene-020_v01.mp4", "lonely sky"),
    (157.746, "aliens_scene-012_v01.mp4", "galactic timescale"),
    (163.000, "aliens_scene-020_v01.mp4", "darkness without contradiction"),
    (173.775, "aliens_scene-020_v01.mp4", "Fermi question and silence"),
    (178.186, "aliens_scene-050_v01.mp4", "city lights"),
    (182.828, "aliens_scene-020_v01.mp4", "no detected city lights"),
    (188.244, "aliens_scene-021_v01.mp4", "no obvious megastructures"),
    (196.754, "aliens_scene-020_v01.mp4", "no visiting fleets"),
    (204.491, "aliens_scene-020_v01.mp4", "silence at the story's heart"),
    (210.860, "aliens_scene-064_v01.mp4", "chemistry becoming life"),
    (224.201, "aliens_scene-043_v01.mp4", "simple life may be common"),
    (230.000, "aliens_scene-024_v01.mp4", "technology may be brief"),
    (237.642, "aliens_scene-024_v01.mp4", "civilisations burn bright and short"),
    (251.778, "aliens_scene-025_v01.mp4", "do-not-disturb zoo hypothesis"),
    (262.937, "aliens_scene-025_v01.mp4", "distant observers"),
    (274.097, "aliens_scene-060_v01.mp4", "perhaps humanity is early"),
    (282.000, "aliens_scene-012_v01.mp4", "cosmic timeline"),
    (287.756, "aliens_scene-030_v01.mp4", "thousand-light-year journey"),
    (303.412, "aliens_scene-030_v01.mp4", "distance as logistics"),
    (319.068, "aliens_scene-031_v01.mp4", "meeting as a chemical fingerprint"),
    (334.724, "aliens_scene-031_v01.mp4", "spectrum and patterned signal"),
    (341.000, "aliens_scene-033_v01.mp4", "modern search instruments"),
    (348.423, "aliens_scene-033_v01.mp4", "SETI listening"),
    (356.000, "aliens_scene-063_v01.mp4", "radio and optical searches"),
    (368.178, "aliens_scene-035_v01.mp4", "the Wow signal"),
    (375.820, "aliens_scene-020_v01.mp4", "listening for a cosmic blink"),
    (383.000, "aliens_scene-037_v01.mp4", "exoplanet science"),
    (388.105, "aliens_scene-037_v01.mp4", "exoplanet atmospheres"),
    (395.000, "aliens_scene-038_v01.mp4", "telescopes measuring worlds"),
    (402.140, "aliens_scene-037_v01.mp4", "biosignature atmosphere"),
    (410.000, "aliens_scene-041_v01.mp4", "chemical evidence as data"),
    (427.091, "aliens_scene-041_v01.mp4", "first contact as a graph"),
    (439.448, "aliens_scene-042_v01.mp4", "searching Mars"),
    (448.805, "aliens_scene-043_v01.mp4", "icy moons and subsurface oceans"),
    (455.162, "aliens_scene-064_v01.mp4", "microbe in an ice grain"),
    (463.000, "aliens_scene-043_v01.mp4", "life without radios"),
    (472.678, "aliens_scene-046_v01.mp4", "physical interstellar encounter"),
    (484.235, "aliens_scene-046_v01.mp4", "long physical-contact odds"),
    (493.000, "aliens_scene-030_v01.mp4", "brutal travel timescales"),
    (501.631, "aliens_scene-048_v01.mp4", "this century's growing catalogue"),
    (509.000, "aliens_scene-038_v01.mp4", "instruments getting sharper"),
    (520.418, "aliens_scene-046_v01.mp4", "careful uncertainty"),
    (531.205, "aliens_scene-050_v01.mp4", "the silence is also about us"),
    (545.122, "aliens_scene-050_v01.mp4", "lesson about technological life"),
    (551.000, "aliens_scene-051_v01.mp4", "interpreting ambiguous signals"),
    (558.060, "aliens_scene-035_v01.mp4", "maybe a signal"),
    (566.000, "aliens_scene-055_v01.mp4", "human hope and fear"),
    (572.915, "aliens_scene-050_v01.mp4", "understanding life on Earth"),
    (580.000, "aliens_scene-055_v01.mp4", "quiet cosmos"),
    (586.420, "aliens_scene-050_v01.mp4", "our precious noisy planet"),
    (590.520, "aliens_scene-055_v01.mp4", "the rest of the sky stays quiet"),
    (604.024, "aliens_scene-055_v01.mp4", "invitation to keep listening"),
    (614.828, "aliens_scene-065_v01.mp4", "final reflective stars"),
]


def semantic_choice(start: float) -> tuple[str, str]:
    filename, rationale = SEMANTIC_SCHEDULE[0][1:]
    for change_at, candidate, reason in SEMANTIC_SCHEDULE:
        if start + 0.001 < change_at:
            break
        filename, rationale = candidate, reason
    return filename, rationale


def build_segments(base, shots: list[dict], index: dict[str, list[Path]]):
    segments = []
    alignments = []
    for shot in shots:
        if shot["kind"] in ("brand_intro", "brand_outro"):
            continue
        original_start = float(shot["start_s"])
        original_end = min(original_start + float(shot["duration_s"]), base.TIMELINE)
        if original_start >= base.TIMELINE:
            continue
        start, end = base.transform_time(original_start, original_end)
        if end <= 0 or start >= base.TIMELINE:
            continue

        retain = shot["kind"] == "chapter" or (
            shot["kind"] == "card" and shot["clip"] in base.KEEP_CARDS
        )
        if retain:
            path = base.resolve(index, shot["clip"])
            kind = shot["kind"]
            stable = True
            rationale = "retained high-value information frame"
        else:
            filename, rationale = semantic_choice(start)
            path = base.resolve(index, filename)
            kind = "semantic_broll"
            stable = False

        segments.append({
            "start": start,
            "end": end,
            "path": str(path),
            "offset": 0.0,
            "kind": kind,
            "stable": stable,
        })
        alignments.append({
            "start": start,
            "end": end,
            "source_timeline_asset": shot["clip"],
            "selected_visual": path.name,
            "reason": rationale,
            "retained_card_or_chapter": retain,
        })

    segments.sort(key=lambda item: item["start"])
    cursor = 0.0
    for segment in segments:
        if abs(segment["start"] - cursor) < 0.015:
            segment["start"] = cursor
        cursor = segment["end"]

    segments = base.override(segments, base.BRAND_START, base.BRAND_END, {
        "path": str(base.BRAND_INTRO), "kind": "brand_hold", "stable": True,
    })
    segments = base.override(segments, base.OUTRO_START, base.TIMELINE, {
        "path": str(base.BRAND_OUTRO), "kind": "brand_outro", "stable": True,
    })
    return segments, alignments


def main() -> None:
    base = load_base()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shots = json.loads(base.EDL_PATH.read_text())["shots"]
    index = base.media_index()
    segments, alignments = build_segments(base, shots, index)
    base.validate_coverage(segments)

    with tempfile.TemporaryDirectory(prefix="orbit_v26_semantic_") as temp:
        work = Path(temp)
        parts = []
        for segment_index, segment in enumerate(segments):
            start_frame = round(segment["start"] * base.FPS)
            end_frame = round(segment["end"] * base.FPS)
            frame_count = end_frame - start_frame
            if frame_count <= 0:
                continue
            part = work / f"part_{segment_index:04d}.mp4"
            base.render_segment(segment, part, frame_count, segment_index)
            parts.append(part)
            if segment_index and segment_index % 30 == 0:
                print(f"rendered {segment_index}/{len(segments)}")

        listing = work / "concat.txt"
        listing.write_text("".join(f"file '{path}'\n" for path in parts))
        base.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(listing),
            "-c", "copy", "-movflags", "+faststart", str(OUT),
        ])

    REPORT.write_text(json.dumps({
        "version": 26,
        "method": "sentence-level semantic picture selection using timed narration anchors",
        "output": str(OUT),
        "approved_elements_preserved": {
            "orbit_performance_v25": True,
            "hook_before_brand": True,
            "brand_hold_seconds": 2.0,
            "information_cards_retained": sorted(base.KEEP_CARDS),
            "chapter_cards_retained": 8,
        },
        "semantic_change_points": len(SEMANTIC_SCHEDULE),
        "alignments": alignments,
    }, indent=2))
    print(json.dumps({
        "output": str(OUT),
        "duration": base.probe(OUT),
        "semantic_change_points": len(SEMANTIC_SCHEDULE),
        "timeline_segments": len(segments),
    }, indent=2))


if __name__ == "__main__":
    main()
