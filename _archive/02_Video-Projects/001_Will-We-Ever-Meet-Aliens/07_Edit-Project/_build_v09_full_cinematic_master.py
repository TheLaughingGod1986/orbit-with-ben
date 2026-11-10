#!/usr/bin/env python3
"""Build the full Orbit 001 cinematic/explainer master.

Rules:
- requested ElevenLabs IVC voice
- hook, then a clean two-second brand ident, then the story
- no fill plates
- no repeated visual source
- genuine moving B-roll or stable readable motion-graphic cards
- stable, animated Orbit companion
- narration-aligned EDL with excerpts
- branded like/subscribe end screen
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
POLISHED = ROOT / "04_Generated-Clips/03_Polished"
BROLL = POLISHED / "broll"
CARDS = POLISHED / "unique_cards"
RIG_A = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03/loops")
RIG_B = POLISHED / "orbit_narrator/rgba/loops"
RIG_POLISHED = POLISHED / "orbit_narrator/rgba/loops_polished_v25"
SCRIPT = ROOT / "01_Script/aliens_narration_bold_v05_18min.txt"

HOOK = ROOT / "02_Voiceover/04_Section-Exports/aliens_vo_bold-v07_hook_ivc_kDch_v01.mp3"
POST = ROOT / "02_Voiceover/04_Section-Exports/aliens_vo_bold-v07_section-01_post-brand_ivc_kDch_v01.mp3"
SEC2 = ROOT / "02_Voiceover/04_Section-Exports/aliens_vo_bold-v05_section-02_explanations_ivc_kDch_v01.mp3"
SEC3 = ROOT / "02_Voiceover/04_Section-Exports/aliens_vo_bold-v05_section-03_search_ivc_kDch_v01.mp3"
SEC4 = ROOT / "02_Voiceover/04_Section-Exports/aliens_vo_bold-v05_section-04_solution-cliffhanger_ivc_kDch_v01.mp3"
VOICE_MASTER = ROOT / "02_Voiceover/05_Master/aliens_voiceover_v10_ivc_kDch_full_master.wav"

BRAND = POLISHED / "brand/orbit_brand_intro_bold-v05_2s.mp4"
MUSIC_A = ROOT / "05_Music/aliens_score_cinematic_v19.wav"
MUSIC_B = ROOT / "05_Music/aliens_score_ambient_v16.wav"
CHIME = ROOT / "06_Sound-Effects/sfx_brand_chime_v11.wav"
WHOOSH = ROOT / "06_Sound-Effects/sfx_whoosh_v19.wav"

OUT = ROOT / "09_Final-Export/aliens_v14_FULL_CINEMATIC_MASTER_18m50s_FINAL.mp4"
EDL_OUT = ROOT / "07_Edit-Project/aliens_v14_full_cinematic_edl.json"
CTA_PNG = ROOT / "08_Thumbnail/aliens_v10_like_subscribe_end-screen.png"
CTA_SOURCE = POLISHED / "brand/orbit_brand_outro_subscribe_v02.png"

W, H, FPS = 1920, 1080, 30
HOOK_DUR = 16.614
BRAND_DUR = 2.0
GAP = 0.65
OUTRO_DUR = 10.0
# Polished Overlay-Rig companion — bottom-RIGHT so present-left gaze looks into frame
ORBIT_H = 500
ORBIT_PAD = 28  # margin from right edge
ORBIT_Y = 1080 - ORBIT_H - 72  # ~508 — clear of player chrome
ORBIT_X = ORBIT_PAD
# Keep Orbit on for the full shot so blink loops read as continuous life
ORBIT_SHOW_MAX = 1e9

SECTION_SOURCES: dict[str, list[tuple[str, str]]] = {
    "01_problem": [
        ("broll", "broll/aliens_scene-006_v01.mp4"),
        ("card", "unique_cards/card_real_question_v01.mp4"),
        ("broll", "broll/aliens_scene-008_v01.mp4"),
        ("card", "unique_cards/card_rudely_big_v01.mp4"),
        ("broll", "broll/aliens_scene-011_v01.mp4"),
        ("card", "unique_cards/card_alpha_v01.mp4"),
        ("broll", "broll/aliens_scene-012_v01.mp4"),
        ("card", "unique_cards/card_lightyears_explain_v01.mp4"),
        ("broll", "broll/aliens_scene-030_v01.mp4"),
        ("card", "unique_cards/card_milky_v01.mp4"),
        ("broll", "broll/aliens_scene-017_v01.mp4"),
        ("card", "unique_cards/card_fermi_lunch_v01.mp4"),
        ("broll", "broll/aliens_scene-020_v01.mp4"),
        ("card", "unique_cards/card_no_city_lights_v01.mp4"),
        ("broll", "broll/aliens_scene-021_v01.mp4"),
        ("card", "unique_cards/card_no_megastructures_v01.mp4"),
        ("broll", "broll/aliens_scene-024_v01.mp4"),
        ("card", "unique_cards/card_no_fleets_v01.mp4"),
        ("card", "unique_cards/card_silence_v01.mp4"),
        ("broll", "broll/aliens_scene-061_v01.mp4"),
        ("card", "unique_cards/card_habitable_zone_v01.mp4"),
    ],
    "02_explanations": [
        ("card", "unique_cards/card_drake_blackboard_v01.mp4"),
        ("broll", "broll/aliens_scene-062_v01.mp4"),
        ("card", "unique_cards/card_buzz_or_alone_v01.mp4"),
        ("broll", "broll_mystery/mystery_A1_exoplanet-city-lights_v01_v01.mp4"),
        ("card", "unique_cards/card_brief_candles_v01.mp4"),
        ("broll", "broll_mystery/mystery_A1_exoplanet-city-lights_v02_v01.mp4"),
        ("card", "unique_cards/card_candles_v01.mp4"),
        ("broll", "broll_mystery/mystery_A2_empty-nightside_v01_v01.mp4"),
        ("card", "unique_cards/card_scale_v01.mp4"),
        ("broll", "broll/aliens_scene-025_v01.mp4"),
        ("card", "unique_cards/card_chemistry_curiosity_v01.mp4"),
        ("broll", "broll_mystery/mystery_A3_megastructure_v01_v01.mp4"),
        ("card", "unique_cards/card_rare_v01.mp4"),
        ("broll", "broll_mystery/mystery_A3_megastructure_v02_v01.mp4"),
        ("card", "unique_cards/card_burn_bright_v01.mp4"),
        ("broll", "broll_mystery/mystery_A4_visiting-fleet_v01_v01.mp4"),
        ("card", "unique_cards/card_do_not_disturb_v01.mp4"),
        ("card", "chapter_cards/chapter_05_05_great-filter_v01.mp4"),
        ("card", "unique_cards/card_zoo_v01.mp4"),
        ("broll", "broll_mystery/mystery_A5_silence-void_v01_v01.mp4"),
        ("card", "unique_cards/card_party_early_v01.mp4"),
        ("broll", "broll_vibrant/aliens_mystery-city_v01.mp4"),
        ("card", "unique_cards/card_thousand_years_v01.mp4"),
        ("broll", "broll_vibrant/aliens_mystery-megastructure_v01.mp4"),
        ("card", "unique_cards/card_distance_v01.mp4"),
        ("card", "chapter_cards/chapter_04_04_fermi-paradox_v01.mp4"),
        ("card", "unique_cards/card_not_handshake_v01.mp4"),
        ("broll", "broll_vibrant/aliens_mystery-silence-void_v01.mp4"),
        ("card", "unique_cards/card_cosmic_blink_v01.mp4"),
        ("broll", "broll_vibrant/aliens_vibrant-001_v01.mp4"),
        ("card", "unique_cards/card_early_v01.mp4"),
        ("broll", "broll_vibrant/aliens_vibrant-002_v01.mp4"),
    ],
    "03_search": [
        ("broll", "broll/aliens_scene-035_v01.mp4"),
        ("card", "unique_cards/card_wow_1977_v01.mp4"),
        ("broll", "broll/aliens_scene-037_v01.mp4"),
        ("card", "unique_cards/card_biosignature_v01.mp4"),
        ("broll", "broll/aliens_scene-038_v01.mp4"),
        ("card", "unique_cards/card_bio_v01.mp4"),
        ("broll", "broll/aliens_scene-042_v01.mp4"),
        ("card", "unique_cards/card_mars_v01.mp4"),
        ("broll", "broll/aliens_scene-043_v01.mp4"),
        ("card", "unique_cards/card_ice_grain_v01.mp4"),
        ("broll", "broll/aliens_scene-046_v01.mp4"),
        ("card", "unique_cards/card_microbe_v01.mp4"),
        ("broll", "broll/aliens_scene-048_v01.mp4"),
        ("card", "unique_cards/card_exo_v01.mp4"),
        ("broll", "broll/aliens_scene-063_v01.mp4"),
        ("card", "unique_cards/card_seti_listen_v01.mp4"),
        ("broll", "broll/aliens_scene-064_v01.mp4"),
        ("card", "unique_cards/card_line_on_graph_v01.mp4"),
        ("card", "unique_cards/card_graph_v01.mp4"),
        ("card", "unique_cards/card_search_v01.mp4"),
    ],
    "04_solution": [
        ("broll", "broll/aliens_scene-031_v01.mp4"),
        ("card", "unique_cards/card_faceplate_v01.mp4"),
        ("card", "unique_cards/card_odds_v01.mp4"),
        ("broll", "broll/aliens_scene-033_v01.mp4"),
        ("card", "unique_cards/card_this_century_v01.mp4"),
        ("card", "unique_cards/card_honest_v01.mp4"),
        ("broll", "broll/aliens_scene-041_v01.mp4"),
        ("card", "unique_cards/card_maybe_signal_v01.mp4"),
        ("card", "unique_cards/card_beat_249_v01.mp4"),
        ("broll", "broll/aliens_scene-050_v01.mp4"),
        ("card", "unique_cards/card_end_wonder_v01.mp4"),
        ("broll", "broll/aliens_scene-051_v01.mp4"),
        ("card", "unique_cards/card_silence_us_v01.mp4"),
        ("card", "unique_cards/card_beat_259_v01.mp4"),
        ("broll", "broll/aliens_scene-055_v01.mp4"),
        ("card", "unique_cards/card_lesson_v01.mp4"),
        ("broll", "broll/aliens_scene-060_v01.mp4"),
        ("card", "unique_cards/card_end_perspective_v01.mp4"),
        ("broll", "broll/aliens_scene-065_v01.mp4"),
        ("card", "unique_cards/card_end_invitation_v01.mp4"),
        ("card", "unique_cards/card_invitation_v01.mp4"),
        ("card", "unique_cards/card_maybe_v01.mp4"),
        ("card", "unique_cards/card_beat_266_v01.mp4"),
    ],
}

HOOK_SOURCES = [
    ("broll", "broll/aliens_scene-001_v01.mp4", 6.000),
    ("broll", "broll/aliens_scene-002_v01.mp4", 5.500),
    ("broll", "broll/aliens_scene-013_v01.mp4", 5.114),
]


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def probe(path: Path) -> float:
    return float(subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nk=1:nw=1", str(path),
        ],
        text=True,
    ).strip())


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def make_voice_master(work: Path) -> tuple[Path, dict[str, float]]:
    sources = [HOOK, POST, SEC2, SEC3, SEC4]
    wavs: list[Path] = []
    for index, source in enumerate(sources):
        wav = work / f"voice_{index}.wav"
        args = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(source),
        ]
        if index == 0:
            args += ["-af", f"atrim=duration={HOOK_DUR:.6f}"]
        args += ["-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", str(wav)]
        run(args)
        wavs.append(wav)
    brand_silence = work / "brand_silence.wav"
    section_gap = work / "section_gap.wav"
    for target, seconds in ((brand_silence, BRAND_DUR), (section_gap, GAP)):
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-t", f"{seconds:.6f}", "-c:a", "pcm_s24le", str(target),
        ])
    ordered = [
        wavs[0], brand_silence, wavs[1], section_gap,
        wavs[2], section_gap, wavs[3], section_gap, wavs[4],
    ]
    listing = work / "voice_concat.txt"
    listing.write_text("".join(f"file '{path}'\n" for path in ordered))
    raw = work / "voice_raw.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(listing),
        "-c:a", "pcm_s24le", str(raw),
    ])
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(raw),
        "-af", "highpass=f=65,lowpass=f=15800,loudnorm=I=-17:LRA=7:TP=-1.5",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", str(VOICE_MASTER),
    ])
    durs = {
        "hook": HOOK_DUR,
        "brand": BRAND_DUR,
        "01_problem": probe(wavs[1]),
        "gap": GAP,
        "02_explanations": probe(wavs[2]),
        "03_search": probe(wavs[3]),
        "04_solution": probe(wavs[4]),
    }
    return VOICE_MASTER, durs


def paragraphs(start: int, end: int) -> list[str]:
    lines = SCRIPT.read_text().splitlines()
    return [line.strip() for line in lines[start-1:end] if line.strip()]


def divide_excerpt(paras: list[str], count: int) -> list[str]:
    words = [max(1, len(p.split())) for p in paras]
    total = sum(words)
    results: list[str] = []
    cursor = 0
    used = 0
    for index in range(count):
        remaining_slots = count - index
        target = (total - used) / remaining_slots
        bucket: list[str] = []
        bucket_words = 0
        while cursor < len(paras):
            remaining_paras = len(paras) - cursor
            if bucket and remaining_paras <= remaining_slots - 1:
                break
            bucket.append(paras[cursor])
            bucket_words += words[cursor]
            cursor += 1
            if bucket_words >= target:
                break
        used += bucket_words
        results.append(" ".join(bucket))
    if cursor < len(paras):
        results[-1] += " " + " ".join(paras[cursor:])
    return results


def orbit_assets() -> list[Path]:
    """Animated Overlay-Rig blink loops only — never the static hires still."""
    pool_dirs = [RIG_POLISHED, RIG_B]
    assets: list[Path] = []
    for d in pool_dirs:
        if not d.exists():
            continue
        assets = sorted(d.glob("orbit_*_idle.mov")) + sorted(d.glob("orbit_*_talk.mov"))
        # Drop static stills (present_hires is a 2s PNG hold)
        assets = [p for p in assets if "hires" not in p.name]
        if assets:
            break
    # Prefer present/neutral animated blink first
    preferred = [p for p in assets if any(k in p.name for k in ("present", "neutral"))]
    rest = [p for p in assets if p not in preferred]
    assets = preferred + rest
    unique: list[Path] = []
    seen: set[str] = set()
    for asset in assets:
        digest = sha(asset)
        if digest not in seen:
            seen.add(digest)
            unique.append(asset)
    return unique


def _orbit_prep(input_label: str, show: float, out_label: str = "[orbit]") -> str:
    """Scale polished Orbit; keep thin AA rim from Overlay-Rig source."""
    return (
        f"{input_label}fps={FPS},format=rgba,"
        f"scale=-1:{ORBIT_H}:flags=lanczos,"
        "lut=a='if(lt(val\\,30)\\,0\\,if(gt(val\\,220)\\,255\\,val))',"
        f"trim=duration={show:.6f},setpts=PTS-STARTPTS,"
        f"fade=t=in:st=0:d=0.22:alpha=1,"
        f"fade=t=out:st={max(0.0, show - 0.22):.6f}:d=0.22:alpha=1"
        f"{out_label}"
    )


def _card_heal_br(prev: str, out: str = "[cleanbr]") -> str:
    """Cover the baked dark BR rectangle in unique_cards with a feathered sky patch."""
    return (
        f"[{prev}]split[main][src];"
        # Larger sample + soft-edged mask so the heal doesn't leave a hard seam
        f"[src]crop=520:280:1080:780,scale=520:280:flags=lanczos,noise=alls=4:allf=t+u[rawpatch];"
        f"[rawpatch]format=rgba,"
        f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        f"a='255*min(1\\,min(X/48\\,(W-X)/48))*min(1\\,min(Y/48\\,(H-Y)/48))'[patch];"
        f"[main][patch]overlay=x=1400:y=800:format=auto{out}"
    )


def render_segment(
    source: Path,
    output: Path,
    target: float,
    kind: str,
    orbit: Path | None,
) -> None:
    source_duration = probe(source)
    stretch = target / source_duration
    command = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(source),
    ]
    if kind == "card":
        command += [
            "-f", "lavfi", "-i",
            f"color=c=white:s=480x1080:r={FPS}:d={target:.6f}",
        ]
    if orbit:
        # Loop the short blink/talk clip — do NOT time-stretch (avoids smear)
        command += ["-stream_loop", "-1", "-i", str(orbit)]
    base_motion = ",noise=alls=5:allf=t+u" if kind == "card" else ""
    filters: list[str] = [
        (
            "[0:v]scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,"
            f"setpts={stretch:.8f}*PTS,fps={FPS},trim=duration={target:.6f},"
            f"setpts=PTS-STARTPTS{base_motion}[base]"
        )
    ]
    previous = "base"
    next_input = 1
    if kind == "card":
        # Subtle sheen — keep very light so it never reads as a grey column
        filters += [
            f"[{next_input}:v]format=rgba,colorchannelmixer=aa=0.020,"
            f"trim=duration={target:.6f},setpts=PTS-STARTPTS[sweep]",
            (
                f"[{previous}][sweep]overlay="
                "x='-w+mod(t*280,W+w)':y=0:"
                "format=auto[cardmotion]"
            ),
        ]
        previous = "cardmotion"
        next_input += 1
        # Heal baked dark BR box in card masters
        filters.append(_card_heal_br(previous, "[cleanbr]"))
        previous = "cleanbr"
    if orbit:
        show = float(target)  # full shot — continuous blink life
        filters.append(_orbit_prep(f"[{next_input}:v]", show, "[orbit]"))
        filters.append(
            f"[{previous}][orbit]overlay=x='W-w-{ORBIT_PAD}':y={ORBIT_Y}:"
            f"enable='between(t\\,0\\,{show:.6f})':"
            f"format=auto:alpha=straight:eof_action=pass[final]"
        )
        previous = "final"
    filters.append(f"[{previous}]format=yuv420p[out]")
    command += [
        "-filter_complex", ";".join(filters),
        "-map", "[out]", "-an", "-t", f"{target:.6f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-r", str(FPS), str(output),
    ]
    run(command)


def render_cta(output: Path, orbit: Path) -> None:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(CTA_PNG),
        "-f", "lavfi", "-i",
        f"color=c=white:s=480x1080:r={FPS}:d={OUTRO_DUR}",
        "-stream_loop", "-1", "-i", str(orbit),
        "-filter_complex",
        (
            f"[0:v]trim=duration={OUTRO_DUR},setpts=PTS-STARTPTS,"
            "drawbox=x=50:y=45:w=265:h=270:color=0x090d1c:t=fill,"
            "noise=alls=5:allf=t+u[base];"
            f"[1:v]format=rgba,colorchannelmixer=aa=0.080,"
            f"trim=duration={OUTRO_DUR},setpts=PTS-STARTPTS[sweep];"
            "[base][sweep]overlay=x='-w+mod(t*420,W+w)':y=0:"
            "format=auto[lit];"
            + _orbit_prep("[2:v]", OUTRO_DUR, "[orbit]").replace(
                f"scale=-1:{ORBIT_H}:flags=lanczos",
                f"scale=-1:{ORBIT_H + 40}:flags=lanczos",
            )
            + ";"
            f"[lit][orbit]overlay=x='W-w-{ORBIT_PAD}':y={ORBIT_Y - 40}:"
            f"format=auto:alpha=straight,"
            "fade=t=in:st=0:d=0.5,fade=t=out:st=9.3:d=0.7,"
            "format=yuv420p[out]"
        ),
        "-map", "[out]", "-an", "-t", f"{OUTRO_DUR}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-r", str(FPS),
        str(output),
    ])


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    VOICE_MASTER.parent.mkdir(parents=True, exist_ok=True)
    CTA_PNG.parent.mkdir(parents=True, exist_ok=True)

    all_named = [name for items in SECTION_SOURCES.values() for _, name in items]
    all_named += [name for _, name, _ in HOOK_SOURCES]
    assert len(all_named) == len(set(all_named)), "visual source repeated"
    assert all("fill_plates" not in name for name in all_named)
    for name in all_named:
        assert (POLISHED / name).exists(), name

    with tempfile.TemporaryDirectory(prefix="orbit_v09_full_") as temp:
        work = Path(temp)
        shutil.copy2(CTA_SOURCE, CTA_PNG)
        voice, durs = make_voice_master(work)

        orbit_pool = orbit_assets()
        # Prefer a friendly talk/idle loop for the CTA (hard alpha only)
        cta_orbit = next(
            (p for p in orbit_pool if "invite_talk" in p.name or "happy_talk" in p.name),
            orbit_pool[-1] if orbit_pool else None,
        )
        assert cta_orbit is not None, "no Orbit loops found"
        orbit_pool = [path for path in orbit_pool if path != cta_orbit]

        edl: list[dict] = []
        visual_plan: list[dict] = []
        timeline = 0.0

        for kind, name, target in HOOK_SOURCES:
            visual_plan.append({
                "kind": kind, "source": POLISHED / name, "duration": target,
                "section": "hook", "excerpt": "Opening hook",
            })
        timeline += HOOK_DUR
        visual_plan.append({
            "kind": "brand", "source": BRAND, "duration": BRAND_DUR,
            "section": "brand", "excerpt": "Intentional brand ident after completed hook",
        })
        timeline += BRAND_DUR

        section_meta = [
            ("01_problem", durs["01_problem"] + GAP, paragraphs(7, 67)),
            ("02_explanations", durs["02_explanations"] + GAP, paragraphs(69, 141)),
            ("03_search", durs["03_search"] + GAP, paragraphs(143, 225)),
            ("04_solution", durs["04_solution"], paragraphs(227, 317)),
        ]
        for section, section_duration, paras in section_meta:
            assets = SECTION_SOURCES[section]
            excerpts = divide_excerpt(paras, len(assets))
            per_scene = section_duration / len(assets)
            for (kind, name), excerpt in zip(assets, excerpts):
                visual_plan.append({
                    "kind": kind,
                    "source": POLISHED / name,
                    "duration": per_scene,
                    "section": section,
                    "excerpt": excerpt,
                })
            timeline += section_duration

        # Evenly distribute unique Orbit performances across the main film.
        eligible = list(range(4, len(visual_plan)))
        orbit_slots = {
            eligible[round(i * (len(eligible) - 1) / (len(orbit_pool) - 1))]: orbit_pool[i]
            for i in range(len(orbit_pool))
        }

        parts: list[Path] = []
        cursor = 0.0
        for index, item in enumerate(visual_plan):
            part = work / f"part_{index:03d}.mp4"
            orbit = orbit_slots.get(index)
            if item["kind"] == "brand":
                render_segment(item["source"], part, item["duration"], "broll", None)
            else:
                render_segment(
                    item["source"], part, item["duration"], item["kind"], orbit
                )
            parts.append(part)
            edl.append({
                "index": index,
                "start": round(cursor, 3),
                "duration": round(item["duration"], 3),
                "end": round(cursor + item["duration"], 3),
                "section": item["section"],
                "kind": item["kind"],
                "source": str(item["source"]),
                "source_sha256": sha(item["source"]),
                "orbit": str(orbit) if orbit else None,
                "narration_excerpt": item["excerpt"],
            })
            cursor += item["duration"]
            print(f"rendered {index + 1}/{len(visual_plan)}", flush=True)

        cta = work / "part_cta.mp4"
        render_cta(cta, cta_orbit)
        parts.append(cta)
        edl.append({
            "index": len(edl), "start": round(cursor, 3),
            "duration": OUTRO_DUR, "end": round(cursor + OUTRO_DUR, 3),
            "section": "outro", "kind": "cta", "source": str(CTA_PNG),
            "orbit": str(cta_orbit),
            "narration_excerpt": "Like, subscribe, next video and Orbit branding",
        })
        cursor += OUTRO_DUR

        listing = work / "video_concat.txt"
        listing.write_text("".join(f"file '{part}'\n" for part in parts))
        bed = work / "full_picture.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(listing),
            "-c", "copy", str(bed),
        ])

        # The VO ends before the CTA; music carries through the end screen.
        voice_with_tail = work / "voice_with_tail.wav"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(voice),
            "-af", f"apad=pad_dur={OUTRO_DUR}", "-t", f"{cursor:.6f}",
            "-c:a", "pcm_s24le", str(voice_with_tail),
        ])

        section_boundaries = [
            HOOK_DUR,
            HOOK_DUR + BRAND_DUR + durs["01_problem"] + GAP,
            HOOK_DUR + BRAND_DUR + durs["01_problem"] + GAP + durs["02_explanations"] + GAP,
            HOOK_DUR + BRAND_DUR + durs["01_problem"] + GAP + durs["02_explanations"] + GAP
            + durs["03_search"] + GAP,
        ]
        delays = [round(value * 1000) for value in section_boundaries]
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed),
            "-i", str(voice_with_tail),
            "-stream_loop", "-1", "-i", str(MUSIC_A),
            "-stream_loop", "-1", "-i", str(MUSIC_B),
            "-i", str(CHIME),
            "-i", str(WHOOSH),
            "-stream_loop", "-1", "-i", str(MUSIC_A),
            "-filter_complex",
            (
                f"[1:a]volume=1.0[vo];"
                f"[2:a]atrim=duration={cursor:.6f},volume=1.0,"
                f"afade=t=in:st=0:d=2,afade=t=out:st={cursor-5:.6f}:d=5[ma];"
                f"[3:a]atrim=duration={cursor:.6f},volume=4.0,"
                f"afade=t=in:st=0:d=4,afade=t=out:st={cursor-6:.6f}:d=6[mb];"
                f"[4:a]atrim=duration=2,volume=0.28,"
                f"adelay={delays[0]}|{delays[0]}[chime];"
                f"[5:a]atrim=duration=1.2,volume=0.12,"
                f"adelay={delays[1]}|{delays[1]}[w1];"
                f"[5:a]atrim=duration=1.2,volume=0.12,"
                f"adelay={delays[2]}|{delays[2]}[w2];"
                f"[5:a]atrim=duration=1.2,volume=0.12,"
                f"adelay={delays[3]}|{delays[3]}[w3];"
                f"[6:a]atrim=duration={OUTRO_DUR},volume=1.0,"
                f"afade=t=in:st=0:d=0.5,afade=t=out:st=8:d=2,"
                f"adelay={round((cursor-OUTRO_DUR)*1000)}|{round((cursor-OUTRO_DUR)*1000)}[cta_music];"
                "[vo][ma][mb][chime][w1][w2][w3][cta_music]"
                "amix=inputs=8:duration=first:normalize=0,"
                "alimiter=limit=0.85:level=false[aout]"
            ),
            "-map", "0:v:0", "-map", "[aout]", "-t", f"{cursor:.6f}",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(OUT),
        ])

        EDL_OUT.write_text(json.dumps({
            "output": str(OUT),
            "duration_seconds": round(cursor, 3),
            "voice_id": "kDch6ACCIpqgQ0NsU9kk",
            "rules": [
                "no_fill_plates",
                "no_repeated_visual_source",
                "hook_then_brand_then_story",
                "stable_animated_orbit",
                "hard_alpha_orbit_no_squash",
                "orbit_bottom_left_companion",
                "narration_aligned_excerpts",
                "branded_like_subscribe_outro",
            ],
            "visual_source_count": len(all_named),
            "visual_source_unique_count": len(set(all_named)),
            "edl": edl,
        }, indent=2))
    print(OUT)


if __name__ == "__main__":
    main()
