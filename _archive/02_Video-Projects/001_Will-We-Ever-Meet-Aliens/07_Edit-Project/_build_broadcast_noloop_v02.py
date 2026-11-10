#!/usr/bin/env python3
"""Rebuild Orbit 001 with HARD rules:
- VO starts almost immediately (tiny brand sting only — no silent cold open)
- Chapter titles ONLY during narration pauses BETWEEN sections (not before first words)
- Visuals timed to what is being said (dense explainer cards + themed B-roll)
- Never reuse / never loop cutscenes (Orbit PiP may loop)
- HQ Seedance/mystery B-roll only (no fill_plates)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
SEC = ROOT / "02_Voiceover/04_Section-Exports"
BROLL = ROOT / "04_Generated-Clips/03_Polished/broll"
VIBRANT = ROOT / "04_Generated-Clips/03_Polished/broll_vibrant"
MYSTERY = ROOT / "04_Generated-Clips/03_Polished/broll_mystery"
FILLS = ROOT / "04_Generated-Clips/03_Polished/fill_plates"  # banned from final cuts — low quality
CARDS = ROOT / "04_Generated-Clips/03_Polished/unique_cards"
CHAPTERS = ROOT / "04_Generated-Clips/03_Polished/chapter_cards"
BRAND = ROOT / "04_Generated-Clips/03_Polished/brand"
POLISHED = ROOT / "04_Generated-Clips/03_Polished"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v10_clean_cuts.mp4"
EDL_OUT = ROOT / "07_Edit-Project/SECTION_EDL_v10_clean_cuts.json"
VO_SMOOTH = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_storyteller_v04.wav"
VO_MARKERS = ROOT / "07_Edit-Project/VO_MARKERS_v08.json"
ORBIT_NARR = ROOT / "04_Generated-Clips/03_Polished/orbit_narrator"
ORBIT_LOOPS = ORBIT_NARR / "rgba" / "loops"


W, H, FPS = 1920, 1080, 30
OPEN_BRAND_S = 0.75  # max silence before first spoken word
CHAPTER_GAP_S = 2.5  # narration pause under mid-film chapter cards only

# Corner companion — ONE stable bottom-left home. Emotion changes the face only.
# (Per-emotion X/Y jumps made Orbit look like he teleports between clips.)
ORBIT_HOME = {"bx": 0.038, "by": 0.755, "ax": 0.007, "ay": 0.016, "T": 4.8, "scale": 158}
ORBIT_MOODS = {
    # All moods share home — tiny amplitude tweaks only (same anchor).
    "curious":  {**ORBIT_HOME, "ay": 0.017, "T": 4.6},
    "wonder":   {**ORBIT_HOME, "ay": 0.018, "T": 5.2},
    "explain":  {**ORBIT_HOME, "ay": 0.014, "T": 5.5},
    "deep":     {**ORBIT_HOME, "ay": 0.012, "T": 6.2},
    "surprise": {**ORBIT_HOME, "ax": 0.010, "ay": 0.020, "T": 3.8},
    "scared":   {**ORBIT_HOME, "ay": 0.011, "T": 3.2},
    "warm":     {**ORBIT_HOME, "ay": 0.015, "T": 5.0},
    "invite":   {**ORBIT_HOME, "ay": 0.017, "T": 4.4},
    "still":    {**ORBIT_HOME, "ax": 0.004, "ay": 0.009, "T": 7.0},
}

# Distinct hard-alpha expression cutouts (v17 face set).
EMOTION_SPRITE = {
    "curious": "corner/sized/orbit_pip_curious.png",
    "wonder": "corner/sized/orbit_pip_wonder.png",
    "amazed": "corner/sized/orbit_pip_amazed.png",
    "explain": "corner/sized/orbit_pip_explain.png",
    "deep": "corner/sized/orbit_pip_deep.png",
    "thinking": "corner/sized/orbit_pip_thinking.png",
    "surprise": "corner/sized/orbit_pip_surprise.png",
    "surprised": "corner/sized/orbit_pip_surprise.png",
    "excited": "corner/sized/orbit_pip_excited.png",
    "scared": "corner/sized/orbit_pip_scared.png",
    "concerned": "corner/sized/orbit_pip_concerned.png",
    "warm": "corner/sized/orbit_pip_warm.png",
    "happy": "corner/sized/orbit_pip_happy.png",
    "playful": "corner/sized/orbit_pip_playful.png",
    "invite": "corner/sized/orbit_pip_invite.png",
    "neutral": "corner/sized/orbit_pip_neutral.png",
}

# Sparse VO-reactive beats — hold expressions longer so faces feel lived-in, not slideshow.
SECTION_EMOTION_BEATS: dict[str, list[tuple[float, str]]] = {
    "01_cold-open": [
        (0.00, "curious"), (0.28, "wonder"), (0.58, "thinking"), (0.82, "curious"),
    ],
    "02_galaxy-scale": [
        (0.00, "wonder"), (0.35, "amazed"), (0.65, "deep"), (0.88, "curious"),
    ],
    "03_exoplanets": [
        (0.00, "curious"), (0.30, "excited"), (0.58, "thinking"), (0.82, "wonder"),
    ],
    "04_fermi-paradox": [
        (0.00, "surprise"), (0.30, "concerned"), (0.60, "thinking"), (0.85, "deep"),
    ],
    "05_great-filter": [
        (0.00, "thinking"), (0.35, "scared"), (0.65, "deep"), (0.88, "concerned"),
    ],
    "06_explanations": [
        (0.00, "curious"), (0.30, "thinking"), (0.58, "explain"), (0.82, "wonder"),
    ],
    "07_detection": [
        (0.00, "curious"), (0.32, "excited"), (0.60, "wonder"), (0.85, "amazed"),
    ],
    "08_first-contact": [
        (0.00, "surprise"), (0.30, "thinking"), (0.58, "wonder"), (0.82, "happy"),
    ],
    "09_conclusion": [
        (0.00, "warm"), (0.35, "curious"), (0.65, "wonder"), (0.88, "warm"),
    ],
    "cta": [
        (0.00, "invite"), (0.50, "happy"), (0.80, "invite"),
    ],
}

# Map narrative emotion → flight motion preset
EMOTION_TO_MOTION = {
    "curious": "curious",
    "wonder": "wonder",
    "amazed": "wonder",
    "explain": "explain",
    "thinking": "deep",
    "deep": "deep",
    "surprise": "surprise",
    "surprised": "surprise",
    "excited": "surprise",
    "scared": "scared",
    "concerned": "scared",
    "warm": "warm",
    "happy": "warm",
    "playful": "invite",
    "invite": "invite",
    "neutral": "still",
}

# Legacy alias used by EDL orbit tags
SECTION_ORBIT = {
    sec: (
        EMOTION_TO_MOTION.get(beats[0][1], "curious"),
        EMOTION_SPRITE.get(beats[0][1], "corner/sized/orbit_pip_curious.png"),
    )
    for sec, beats in SECTION_EMOTION_BEATS.items()
}

INTERESTING_EXISTING = [
    "aliens_scene-011_v01.mp4", "aliens_scene-013_v01.mp4", "aliens_scene-017_v01.mp4",
    "aliens_scene-020_v01.mp4", "aliens_scene-024_v01.mp4", "aliens_scene-025_v01.mp4",
    "aliens_scene-030_v01.mp4", "aliens_scene-031_v01.mp4", "aliens_scene-033_v01.mp4",
    "aliens_scene-035_v01.mp4", "aliens_scene-037_v01.mp4", "aliens_scene-038_v01.mp4",
    "aliens_scene-041_v01.mp4", "aliens_scene-042_v01.mp4", "aliens_scene-043_v01.mp4",
    "aliens_scene-046_v01.mp4", "aliens_scene-048_v01.mp4", "aliens_scene-050_v01.mp4",
    "aliens_scene-051_v01.mp4", "aliens_scene-061_v01.mp4", "aliens_scene-062_v01.mp4",
    "aliens_scene-063_v01.mp4", "aliens_scene-064_v01.mp4",
]

BORING_STARFIELDS = {
    "aliens_scene-001_v01.mp4", "aliens_scene-002_v01.mp4", "aliens_scene-006_v01.mp4",
    "aliens_scene-008_v01.mp4", "aliens_scene-012_v01.mp4", "aliens_scene-021_v01.mp4",
    "aliens_scene-055_v01.mp4", "aliens_scene-060_v01.mp4", "aliens_scene-065_v01.mp4",
}

SECTION_ORDER = [
    "01_cold-open", "02_galaxy-scale", "03_exoplanets", "04_fermi-paradox",
    "05_great-filter", "06_explanations", "07_detection", "08_first-contact", "09_conclusion",
]

# Dense timed visuals: ("card"|"clip", filename, fraction_into_section)
# Cards explain the line being spoken; clips are themed mystery/AI B-roll.
SECTION_VISUALS: dict[str, list[tuple[str, str, float]]] = {
    "01_cold-open": [
        # Documentary hook: mystery → question → promise (before topic branding)
        ("card", "card_hook_mystery_v01.mp4", 0.00),
        ("card", "card_where_everybody_v01.mp4", 0.18),
        ("card", "card_hook_crowded_v01.mp4", 0.36),
        ("card", "card_hook_promise_v01.mp4", 0.52),
        ("card", "card_real_question_v01.mp4", 0.72),
        ("card", "card_look_up_v01.mp4", 0.88),
    ],
    "02_galaxy-scale": [
        ("card", "card_rudely_big_v01.mp4", 0.00),
        ("card", "card_alpha_v01.mp4", 0.22),
        ("card", "card_lightyears_explain_v01.mp4", 0.40),
        ("card", "card_milky_v01.mp4", 0.62),
        ("card", "card_habitable_zone_v01.mp4", 0.82),
    ],
    "03_exoplanets": [
        ("card", "card_drake_blackboard_v01.mp4", 0.04),
        ("card", "card_buzz_or_alone_v01.mp4", 0.32),
        ("card", "card_brief_candles_v01.mp4", 0.52),
        ("card", "card_candles_v01.mp4", 0.72),
        ("card", "card_scale_v01.mp4", 0.88),
    ],
    "04_fermi-paradox": [
        ("card", "card_fermi_lunch_v01.mp4", 0.00),
        ("card", "card_no_city_lights_v01.mp4", 0.22),
        ("clip", "mystery_A2_empty-nightside_v01_v01.mp4", 0.34),
        ("card", "card_no_megastructures_v01.mp4", 0.48),
        ("clip", "mystery_A3_megastructure_v01_v01.mp4", 0.58),
        ("card", "card_no_fleets_v01.mp4", 0.70),
        ("clip", "mystery_A4_visiting-fleet_v01_v01.mp4", 0.80),
        ("card", "card_silence_v01.mp4", 0.90),
    ],
    "05_great-filter": [
        ("card", "card_chemistry_curiosity_v01.mp4", 0.00),
        ("card", "card_rare_v01.mp4", 0.18),
        ("card", "card_burn_bright_v01.mp4", 0.36),
        ("card", "card_do_not_disturb_v01.mp4", 0.55),
        ("card", "card_zoo_v01.mp4", 0.70),
        ("card", "card_party_early_v01.mp4", 0.85),
    ],
    "06_explanations": [
        ("card", "card_thousand_years_v01.mp4", 0.00),
        ("card", "card_distance_v01.mp4", 0.16),
        ("card", "card_not_handshake_v01.mp4", 0.32),
        ("card", "card_spectrum_v01.mp4", 0.48),
        ("card", "card_seti_listen_v01.mp4", 0.62),
        ("card", "card_wow_1977_v01.mp4", 0.78),
        ("card", "card_cosmic_blink_v01.mp4", 0.90),
    ],
    "07_detection": [
        ("card", "card_exo_v01.mp4", 0.00),
        ("card", "card_biosignature_v01.mp4", 0.18),
        ("card", "card_bio_v01.mp4", 0.34),
        ("card", "card_line_on_graph_v01.mp4", 0.50),
        ("card", "card_graph_v01.mp4", 0.62),
        ("card", "card_mars_v01.mp4", 0.74),
        ("card", "card_ice_grain_v01.mp4", 0.86),
    ],
    "08_first-contact": [
        ("card", "card_faceplate_v01.mp4", 0.00),
        ("card", "card_odds_v01.mp4", 0.18),
        ("card", "card_this_century_v01.mp4", 0.38),
        ("card", "card_honest_v01.mp4", 0.55),
        ("card", "card_silence_us_v01.mp4", 0.72),
        ("card", "card_lesson_v01.mp4", 0.88),
    ],
    "09_conclusion": [
        ("card", "card_maybe_signal_v01.mp4", 0.00),
        ("card", "card_end_wonder_v01.mp4", 0.22),
        ("card", "card_end_perspective_v01.mp4", 0.42),
        ("card", "card_end_invitation_v01.mp4", 0.62),
        ("card", "card_invitation_v01.mp4", 0.78),
        ("card", "card_end_subscribe_v01.mp4", 0.90),
    ],
    "cta": [
        ("card", "card_end_subscribe_v01.mp4", 0.05),
        ("card", "card_end_invitation_v01.mp4", 0.55),
    ],
}

CHAPTER_CARD = {
    "02_galaxy-scale": "chapter_02_02_galaxy-scale_v01.mp4",
    "03_exoplanets": "chapter_03_03_exoplanets_v01.mp4",
    "04_fermi-paradox": "chapter_04_04_fermi-paradox_v01.mp4",
    "05_great-filter": "chapter_05_05_great-filter_v01.mp4",
    "06_explanations": "chapter_06_06_explanations_v01.mp4",
    "07_detection": "chapter_07_07_detection_v01.mp4",
    "08_first-contact": "chapter_08_08_first-contact_v01.mp4",
    "09_conclusion": "chapter_09_09_conclusion_v01.mp4",
}


def probe(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)], text=True).strip())


def make_silence(td: Path, dur: float, name: str) -> Path:
    out = td / name
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
        "-t", f"{dur:.4f}", "-c:a", "pcm_s16le", str(out),
    ], check=True)
    return out


def build_vo(td: Path) -> tuple[Path, list[dict]]:
    """Build storyteller VO: tiny brand sting, then VO immediately.

    Timeline:
      [~0.75s brand silence]
      [section1 VO]
      [chapter pause + section2 VO] …
      [cta]
    Chapter 1 does NOT delay the first words — mid-film chapters still pause.
    """
    parts = [SEC / f"aliens_vo_section-{n}_v03.wav" for n in SECTION_ORDER]
    cta = SEC / "aliens_vo_section-10_cta_subscribe_v02.wav"
    if not all(p.exists() for p in parts):
        parts = [SEC / f"aliens_vo_section-{n}_v02.wav" for n in SECTION_ORDER]
    if not cta.exists():
        cta = SEC / "aliens_vo_section-10_cta_subscribe_v01.wav"
    assert all(p.exists() for p in parts), "missing VO sections"
    assert cta.exists(), "missing CTA VO"

    intro = BRAND / "orbit_brand_intro_v01.mp4"
    assert intro.exists()
    brand_s = min(OPEN_BRAND_S, probe(intro))
    gap = CHAPTER_GAP_S

    markers: list[dict] = []
    concat_files: list[Path] = []
    t = 0.0

    lead_wav = make_silence(td, brand_s, "vo_lead_silence.wav")
    concat_files.append(lead_wav)
    markers.append({
        "kind": "lead", "start_s": t, "duration_s": brand_s,
        "hook_s": 0.0, "brand_s": brand_s, "chapter_s": 0.0,
    })
    t += brand_s

    for i, (n, wav) in enumerate(zip(SECTION_ORDER, parts)):
        if i > 0 and n in CHAPTER_CARD:
            gap_wav = make_silence(td, gap, f"vo_gap_{i:02d}.wav")
            concat_files.append(gap_wav)
            markers.append({
                "kind": "chapter_gap", "section": n,
                "start_s": t, "duration_s": gap,
            })
            t += gap
        concat_files.append(wav)
        d = probe(wav)
        markers.append({
            "kind": "vo", "section": n,
            "start_s": t, "duration_s": d,
        })
        t += d

    concat_files.append(cta)
    cta_d = probe(cta)
    markers.append({"kind": "cta", "section": "cta", "start_s": t, "duration_s": cta_d})
    t += cta_d

    lst = td / "vo_concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in concat_files))
    joined = td / "vo_joined.wav"
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined),
    ], check=True)

    polished = td / "vo_polished.wav"
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(joined),
        "-af",
        "highpass=f=70,"
        "lowpass=f=10500,"
        "acompressor=threshold=-20dB:ratio=2.1:attack=20:release=180:makeup=1.6,"
        "equalizer=f=120:t=q:w=1:g=1.2,"
        "equalizer=f=3200:t=q:w=1.2:g=1.5,"
        "loudnorm=I=-16:TP=-1.5:LRA=10",
        "-ar", "44100", "-ac", "1", str(polished),
    ], check=True)
    VO_SMOOTH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(polished, VO_SMOOTH)
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(VO_SMOOTH), "-codec:a", "libmp3lame", "-b:a", "192k",
        str(VO_SMOOTH.with_suffix(".mp3")),
    ], check=True)
    VO_MARKERS.write_text(json.dumps(markers, indent=2))
    return VO_SMOOTH, markers


def resolve_media(kind: str, name: str) -> Path | None:
    if kind == "card":
        p = CARDS / name
        return p if p.exists() else None
    for folder in (MYSTERY, VIBRANT, BROLL, POLISHED):
        p = folder / name
        if p.exists():
            return p
    # basename search
    for folder in (MYSTERY, VIBRANT, BROLL):
        hits = list(folder.glob(name))
        if hits:
            return hits[0]
    return None


def collect_unique_clips() -> list[Path]:
    """HQ cutscenes only — Seedance AI / mystery remaster.
    NEVER include procedural fill_plates (blurry low-quality).
    """
    clips: list[Path] = []
    seen: set[str] = set()

    def add(p: Path):
        if not p.exists() or p.name in seen or p.name in BORING_STARFIELDS:
            return
        if p.name.startswith("fill_plate"):
            return
        seen.add(p.name)
        clips.append(p)

    VIBRANT.mkdir(parents=True, exist_ok=True)
    MYSTERY.mkdir(parents=True, exist_ok=True)
    for p in sorted(VIBRANT.glob("*.mp4")):
        add(p)
    for p in sorted(MYSTERY.glob("*.mp4")):
        add(p)
    for name in INTERESTING_EXISTING:
        add(BROLL / name)
    for p in sorted(BROLL.glob("aliens_scene-*.mp4")):
        add(p)
    return clips


def build_edl(vo_dur: float, pool: list[Path], markers: list[dict]) -> list[dict]:
    """Picture locked to VO: immediate brand → VO visuals; chapter cards on gaps only."""
    used: set[str] = set()
    pool_i = 0
    edl: list[dict] = []
    t = 0.0

    def take_clip() -> Path | None:
        nonlocal pool_i
        while pool_i < len(pool):
            p = pool[pool_i]
            pool_i += 1
            if p.name in used:
                continue
            used.add(p.name)
            return p
        return None

    def append(kind: str, path: Path, section: str, orbit: str | None = None, dur: float | None = None):
        nonlocal t
        native = probe(path)
        d = min(native, dur) if dur is not None else native
        if d <= 0.01:
            return 0.0
        used.add(path.name)
        edl.append({
            "kind": kind, "path": path, "start_s": round(t, 3), "duration_s": d,
            "section": section, "orbit": orbit,
        })
        t += d
        return d

    def fill_to(section: str, end_target: float, orbit: str | None, visuals: list[tuple[str, str, float]]):
        """Fill to end_target with timed cards/clips matching narration beats.

        Never insert micro-flashes or random card_beat fillers — leftover gaps
        extend the previous shot (freeze-hold) so picture stays coherent.
        """
        nonlocal t
        MIN_SHOT = 1.8
        MIN_CARD = 2.6
        if t >= end_target - 0.02:
            t = end_target
            return

        def hold_to(target: float):
            """Absorb a gap by extending the previous visual — never chapter/brand."""
            nonlocal t
            if t >= target - 0.02:
                t = target
                return
            gap = target - t
            if not edl:
                t = target
                return
            if edl[-1]["kind"] not in ("chapter", "brand_intro", "brand_outro"):
                edl[-1]["duration_s"] = round(float(edl[-1]["duration_s"]) + gap, 3)
                t = target
                return
            # After a chapter title: continue with a freeze of the last real visual
            # (allowed hold-reuse — not a new cutscene appearance).
            src = next((s for s in reversed(edl) if s["kind"] in ("broll", "card")), None)
            if src is None:
                t = target
                return
            edl.append({
                "kind": src["kind"], "path": src["path"], "start_s": round(t, 3),
                "duration_s": gap, "section": section, "orbit": orbit,
            })
            t = target

        sec_start = t
        span = max(0.1, end_target - sec_start)
        scheduled: list[tuple[str, str, float]] = []
        for kind, name, frac in visuals:
            scheduled.append((kind, name, sec_start + max(0.0, min(0.95, frac)) * span))
        scheduled.sort(key=lambda x: x[2])
        bi = 0

        def next_barrier() -> float:
            if bi < len(scheduled):
                return min(end_target, scheduled[bi][2])
            return end_target

        while t < end_target - 0.05:
            if bi < len(scheduled) and t >= scheduled[bi][2] - 0.15:
                kind, name, _ = scheduled[bi]
                bi += 1
                path = resolve_media(kind, name)
                if path is None or path.name in used:
                    continue
                remain = end_target - t
                until_next = (scheduled[bi][2] - t) if bi < len(scheduled) else remain
                native = probe(path)
                want = min(4.8, MIN_CARD + 1.5) if kind == "card" else min(native, 4.5)
                budget = min(remain, max(0.0, until_next - 0.05), want, native)
                # If the leftover after this card would be an unusable sliver, absorb it
                if until_next <= remain and 0 < until_next - budget < MIN_SHOT:
                    budget = min(remain, until_next, native)
                if budget < MIN_SHOT:
                    continue
                append("card" if kind == "card" else "broll", path, section, orbit, dur=budget)
                continue

            barrier = next_barrier()
            remain_to_barrier = barrier - t
            if remain_to_barrier < MIN_SHOT:
                hold_to(barrier)
                continue

            clip = take_clip()
            if clip is not None:
                take = min(remain_to_barrier, 4.2)
                if 0 < remain_to_barrier - take < MIN_SHOT:
                    take = remain_to_barrier
                append("broll", clip, section, orbit, dur=take)
                continue

            # Pool empty — round-robin ALL distinct earlier B-roll (hold-reuse).
            seen_paths: list[Path] = []
            for s in edl:
                if s["kind"] != "broll":
                    continue
                p = s["path"] if isinstance(s["path"], Path) else Path(s["path"])
                if p not in seen_paths:
                    seen_paths.append(p)
            if seen_paths and remain_to_barrier >= MIN_SHOT:
                take = min(remain_to_barrier, 4.5)
                # Stable counter via shot count so we walk the full unique set
                reuse_path = seen_paths[sum(1 for s in edl if s["kind"] == "broll") % len(seen_paths)]
                edl.append({
                    "kind": "broll", "path": reuse_path, "start_s": round(t, 3),
                    "duration_s": take, "section": section, "orbit": orbit,
                })
                t += take
                continue

            hold_to(min(end_target, t + min(remain_to_barrier, 5.0)))
            if t >= end_target - 0.05:
                break

        if t < end_target - 0.02:
            hold_to(end_target)
        t = end_target

    intro = BRAND / "orbit_brand_intro_v01.mp4"
    outro = BRAND / "orbit_brand_outro_subscribe_v01.mp4"
    assert intro.exists() and outro.exists()

    lead = next(m for m in markers if m["kind"] == "lead")
    brand_s = float(lead["brand_s"])
    lead_end = float(lead["duration_s"])

    # Tiny brand sting — then VO starts
    append("brand_intro", intro, "brand", None, dur=brand_s)
    t = lead_end

    for m in markers:
        if m["kind"] == "lead":
            continue
        if m["kind"] == "chapter_gap":
            gap_start = float(m["start_s"])
            gap_end = gap_start + float(m["duration_s"])
            if t < gap_start - 0.02:
                fill_to(m["section"], gap_start, None, [])
            t = gap_start
            chap = CHAPTERS / CHAPTER_CARD[m["section"]]
            append("chapter", chap, m["section"], None, dur=float(m["duration_s"]))
            t = gap_end
            continue
        if m["kind"] in ("vo", "cta"):
            target_start = float(m["start_s"])
            end_target = target_start + float(m["duration_s"])
            if t < target_start - 0.02:
                fill_to(m.get("section", "fill"), target_start, None, [])
            t = target_start
            sec = m["section"]
            mood_info = SECTION_ORBIT.get(sec) or SECTION_ORBIT.get("cta")
            orbit = mood_info[0] if isinstance(mood_info, tuple) else mood_info
            visuals = SECTION_VISUALS.get(sec, [])
            fill_to(sec, end_target, orbit, visuals)

    append("brand_outro", outro, "outro", None)
    # Unique cards/chapters must never repeat as new "ideas".
    # Intentional B-roll hold-reuse is allowed once the unique pool is empty
    # (keeps end-of-film pacing alive without 15s static text plates).
    for kind in ("card", "chapter", "brand_intro", "brand_outro"):
        names = [e["path"].name for e in edl if e["kind"] == kind]
        assert len(names) == len(set(names)), f"REUSE DETECTED in {kind}"
    return edl, t, used


def render_once(path: Path, dur: float, out: Path, *, stable_text: bool = False, motion_seed: int = 0):
    """Render exactly dur seconds from start — NO stream_loop.

    B-roll gets a gentle Ken Burns move every shot (retention motion).
    Text cards stay locked still (readable typography).
    """
    native = probe(path)
    pad = max(0.0, dur - native)
    take = min(dur, native)
    if stable_text:
        vf = f"fps={FPS},format=yuv420p"
    else:
        # Soft cinematic push / drift — never static AI plate
        mode = motion_seed % 4
        z = 1.10
        # Start oversized, then crop with time-based pan/zoom
        if mode == 0:  # slow zoom in
            vf = (
                f"scale={int(W*z)}:{int(H*z)}:force_original_aspect_ratio=increase:flags=bicubic,"
                f"crop={W}:{H}:"
                f"x='(iw-ow)/2':"
                f"y='(ih-oh)/2-((ih-oh)/2)*(t/{max(take,0.1):.3f})',"
                f"fps={FPS},format=yuv420p"
            )
        elif mode == 1:  # slow zoom out (start tighter)
            vf = (
                f"scale={int(W*1.14)}:{int(H*1.14)}:force_original_aspect_ratio=increase:flags=bicubic,"
                f"crop={W}:{H}:"
                f"x='(iw-ow)/2':"
                f"y='((ih-oh)/2)*(t/{max(take,0.1):.3f})',"
                f"fps={FPS},format=yuv420p"
            )
        elif mode == 2:  # drift right
            vf = (
                f"scale={int(W*1.12)}:{int(H*1.12)}:force_original_aspect_ratio=increase:flags=bicubic,"
                f"crop={W}:{H}:"
                f"x='(iw-ow)*(t/{max(take,0.1):.3f})':"
                f"y='(ih-oh)/2',"
                f"fps={FPS},format=yuv420p"
            )
        else:  # drift left
            vf = (
                f"scale={int(W*1.12)}:{int(H*1.12)}:force_original_aspect_ratio=increase:flags=bicubic,"
                f"crop={W}:{H}:"
                f"x='(iw-ow)*(1-t/{max(take,0.1):.3f})':"
                f"y='(ih-oh)/2',"
                f"fps={FPS},format=yuv420p"
            )
    if pad > 0.02:
        vf = f"{vf},tpad=stop_mode=clone:stop_duration={pad:.4f}"
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(path), "-t", f"{take:.4f}", "-an", "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast",
    ]
    if stable_text:
        cmd += [
            "-tune", "stillimage", "-crf", "14",
            "-x264-params", "keyint=1:min-keyint=1:scenecut=0:bframes=0",
        ]
    else:
        cmd += ["-crf", "18"]
    cmd.append(str(out))
    subprocess.run(cmd, check=True)


def _motion_for_emotion(emotion: str) -> dict:
    key = EMOTION_TO_MOTION.get(emotion, "curious")
    return ORBIT_MOODS[key]


def _piecewise_pos_expr(windows: list[dict], axis: str) -> str:
    """Build nested ffmpeg if(between(t,...)) expression for x or y — clamped on-screen."""
    if not windows:
        return "0"
    expr = "0"
    for w in reversed(windows):
        m = _motion_for_emotion(w["emotion"])
        t0, t1 = w["start"], w["end"]
        base = m["bx"] if axis == "x" else m["by"]
        amp = m["ax"] if axis == "x" else m["ay"]
        T = m["T"]
        wave = (
            f"sin(2*PI*(t-{t0:.3f})/{T:.3f})"
            if axis == "x"
            else f"cos(2*PI*(t-{t0:.3f})/{T * 1.2:.3f})"
        )
        dim = "W" if axis == "x" else "H"
        ow = "w" if axis == "x" else "h"
        body = f"({dim}-{ow})*{base:.4f}+({dim}-{ow})*{amp:.4f}*{wave}"
        # Keep a safe margin so Orbit never clips or crowds the picture.
        margin = 24 if axis == "x" else 28
        body = f"max({margin}\\,min(({dim}-{ow})-{margin}\\,{body}))"
        expr = f"if(between(t\\,{t0:.3f}\\,{t1:.3f})\\,{body}\\,{expr})"
    return expr


def _dedupe_windows(windows: list[dict]) -> list[dict]:
    """One Orbit at a time; merge micro-holds so faces don't flicker every cut."""
    if not windows:
        return []
    ordered = sorted(windows, key=lambda w: (w["start"], w["end"]))
    out: list[dict] = []
    for w in ordered:
        w = dict(w)
        if out and w["start"] < out[-1]["end"]:
            if w["start"] - out[-1]["start"] < 0.35:
                out[-1] = w
                continue
            out[-1]["end"] = w["start"]
            if out[-1]["end"] - out[-1]["start"] < 0.35:
                out.pop()
        if w["end"] - w["start"] >= 0.35:
            out.append(w)
    # Merge consecutive same-sprite holds; extend short holds into neighbors
    merged: list[dict] = []
    for w in out:
        if merged and merged[-1]["sprite"] == w["sprite"] and w["start"] <= merged[-1]["end"] + 0.15:
            merged[-1]["end"] = max(merged[-1]["end"], w["end"])
            continue
        # If previous face held < 5s and this is a new face, steal time into previous
        if merged and (merged[-1]["end"] - merged[-1]["start"]) < 5.0 and w["sprite"] != merged[-1]["sprite"]:
            # Prefer longer hold on previous expression — delay new face
            need = 5.0 - (merged[-1]["end"] - merged[-1]["start"])
            steal = min(need, max(0.0, (w["end"] - w["start"]) - 2.0))
            if steal > 0.2:
                merged[-1]["end"] += steal
                w["start"] += steal
        if w["end"] - w["start"] >= 0.8:
            merged.append(w)
    return merged


def _orbit_intervals(edl: list[dict]) -> list[tuple[float, float]]:
    """Orbit companion stays present on picture — not brand plates."""
    out = []
    for s in edl:
        if s.get("kind") in ("brand_intro", "brand_outro"):
            continue
        a = float(s["start_s"])
        b = a + float(s["duration_s"])
        if b - a >= 0.35:
            out.append((a, b))
    return out


def _broll_intervals(edl: list[dict]) -> list[tuple[float, float]]:
    """Back-compat alias — Orbit now uses full picture intervals."""
    return _orbit_intervals(edl)


def _build_emotion_windows(markers: list[dict], edl: list[dict] | None = None) -> list[dict]:
    """Emotion beats clipped to picture (Orbit companion throughout)."""
    raw: list[dict] = []
    for m in markers:
        if m["kind"] not in ("vo", "cta"):
            continue
        sec = m["section"]
        st = float(m["start_s"])
        dur = float(m["duration_s"])
        beats = SECTION_EMOTION_BEATS.get(sec) or [(0.0, "curious")]
        fracs = [(float(f), e) for f, e in beats]
        for i, (frac, emotion) in enumerate(fracs):
            a = st + dur * frac
            b = st + dur * (fracs[i + 1][0] if i + 1 < len(fracs) else 1.0)
            if b - a < 0.2:
                continue
            sprite = EMOTION_SPRITE.get(emotion, "corner/sized/orbit_pip_curious.png")
            raw.append({
                "start": a, "end": b, "emotion": emotion,
                "sprite": sprite, "section": sec,
            })

    if not edl:
        return _dedupe_windows(raw)

    intervals = _orbit_intervals(edl)
    if not intervals:
        print("  no Orbit intervals — Orbit hidden for whole film")
        return []

    windows: list[dict] = []
    for w in raw:
        for ba, bb in intervals:
            a = max(w["start"], ba)
            b = min(w["end"], bb)
            if b - a < 0.35:
                continue
            windows.append({
                "start": a, "end": b,
                "emotion": w["emotion"],
                "sprite": w["sprite"],
                "section": w["section"],
            })
    windows = _dedupe_windows(windows)
    print(f"  Orbit visible on {len(windows)} windows ({sum(w['end']-w['start'] for w in windows):.0f}s)")
    return windows


def _simple_pos_expr(emotion: str, axis: str) -> str:
    """Shared bottom-left home + gentle continuous bob (same anchor for every face)."""
    m = ORBIT_HOME  # lock position — emotion must not teleport Orbit
    _ = emotion  # reserved for future per-mood amp tweaks
    base = m["bx"] if axis == "x" else m["by"]
    amp = m["ax"] if axis == "x" else m["ay"]
    # Shared phase so X/Y feel like one float, not independent jumps
    T = 4.8 if axis == "x" else 5.6
    wave = f"sin(2*PI*t/{T:.3f})" if axis == "x" else f"cos(2*PI*t/{T:.3f})"
    dim = "W" if axis == "x" else "H"
    ow = "w" if axis == "x" else "h"
    margin = 20 if axis == "x" else 24
    body = f"({dim}-{ow})*{base:.4f}+({dim}-{ow})*{amp:.4f}*{wave}"
    return f"max({margin}\\,min(({dim}-{ow})-{margin}\\,{body}))"


def _orbit_life_filter(inp_label: str, out_label: str) -> str:
    """Continuous micro-animation — soft hover breathe on top of blink/talk loops."""
    s = int(ORBIT_HOME["scale"])
    return (
        f"{inp_label}fps={FPS},format=rgba,"
        f"scale={s}:-1:flags=lanczos,"
        f"scale=w='iw*(1+0.03*sin(2*PI*t/3.2))':h='-1':eval=frame,"
        f"format=rgba{out_label}"
    )


def _merge_enable_segs(segs: list[dict]) -> list[tuple[float, float]]:
    """Collapse abutting/overlapping segments for shorter enable expressions."""
    if not segs:
        return []
    ordered = sorted((float(s["start"]), float(s["end"])) for s in segs)
    out = [list(ordered[0])]
    for a, b in ordered[1:]:
        if a <= out[-1][1] + 0.05:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(a, b) for a, b in out]


def _emotion_from_sprite(sprite: str) -> str:
    stem = Path(sprite).stem  # orbit_pip_curious
    return stem.replace("orbit_pip_", "").replace("orbit_corner_", "").replace("orbit_rgba_", "")


def _vo_speak_intervals(vo: Path, noise_db: float = -34.0, min_silence: float = 0.22) -> list[tuple[float, float]]:
    """Return speaking intervals by inverting ffmpeg silencedetect on the VO master."""
    dur = probe(vo)
    r = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(vo),
            "-af", f"silencedetect=noise={noise_db}dB:d={min_silence}",
            "-f", "null", "-",
        ],
        capture_output=True, text=True,
    )
    silences: list[tuple[float, float]] = []
    start = None
    for line in r.stderr.splitlines():
        if "silence_start:" in line:
            try:
                start = float(line.split("silence_start:")[1].split("|")[0].strip())
            except ValueError:
                start = None
        elif "silence_end:" in line and start is not None:
            try:
                end = float(line.split("silence_end:")[1].split("|")[0].strip())
                silences.append((start, end))
            except ValueError:
                pass
            start = None
    if start is not None:
        silences.append((start, dur))

    speak: list[tuple[float, float]] = []
    t = 0.0
    for a, b in silences:
        if a - t >= 0.12:
            speak.append((t, a))
        t = b
    if dur - t >= 0.12:
        speak.append((t, dur))
    return speak


def _intersect_intervals(a: list[tuple[float, float]], b: list[tuple[float, float]]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for a0, a1 in a:
        for b0, b1 in b:
            x0, x1 = max(a0, b0), min(a1, b1)
            if x1 - x0 >= 0.10:
                out.append((x0, x1))
    return _merge_enable_segs([{"start": x, "end": y} for x, y in out])


def _subtract_intervals(base: list[tuple[float, float]], cut: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """base minus cut — used for idle = emotion − speaking."""
    out: list[tuple[float, float]] = []
    for a0, a1 in base:
        pieces = [(a0, a1)]
        for c0, c1 in cut:
            nxt = []
            for p0, p1 in pieces:
                if c1 <= p0 or c0 >= p1:
                    nxt.append((p0, p1))
                    continue
                if c0 > p0:
                    nxt.append((p0, c0))
                if c1 < p1:
                    nxt.append((c1, p1))
            pieces = nxt
        out.extend(p for p in pieces if p[1] - p[0] >= 0.10)
    return _merge_enable_segs([{"start": x, "end": y} for x, y in out])


def compose_flying_orbit(bed: Path, vo: Path, edl: list[dict], markers: list[dict], out: Path, timeline: float):
    """Living corner Orbit — blink/talk loops + VO lip-sync + stable hover.

    Prefers rgba/loops/orbit_{emotion}_{idle|talk}.mov when present; falls back to still PNG.
    """
    rgba_dir = ORBIT_NARR / "rgba"
    windows = _build_emotion_windows(markers, edl)
    if not windows:
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed), "-i", str(vo),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-t", f"{timeline:.3f}", "-movflags", "+faststart",
            str(out),
        ], check=True)
        return

    speak = _vo_speak_intervals(vo)
    print(f"  VO speak intervals: {len(speak)}")

    # Group emotion windows
    by_emotion: dict[str, list[dict]] = {}
    for w in windows:
        emo = w.get("emotion") or _emotion_from_sprite(w["sprite"])
        by_emotion.setdefault(emo, []).append(w)

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(bed),
        "-i", str(vo),
    ]

    # Each layer: (label, input_index, enable_segs)
    layers: list[tuple[str, int, list[tuple[float, float]]]] = []
    next_inp = 2

    for emo, segs in by_emotion.items():
        emo_iv = _merge_enable_segs(segs)
        talk_iv = _intersect_intervals(emo_iv, speak)
        idle_iv = _subtract_intervals(emo_iv, talk_iv)

        idle_mov = ORBIT_LOOPS / f"orbit_{emo}_idle.mov"
        talk_mov = ORBIT_LOOPS / f"orbit_{emo}_talk.mov"
        still = rgba_dir / EMOTION_SPRITE.get(emo, f"corner/sized/orbit_pip_{emo}.png")
        if not still.exists():
            still = rgba_dir / "corner" / "sized" / f"orbit_pip_{emo}.png"

        if idle_mov.exists() and idle_iv:
            cmd += ["-stream_loop", "-1", "-i", str(idle_mov)]
            layers.append((f"{emo}/idle", next_inp, idle_iv))
            next_inp += 1
        elif idle_iv and still.exists():
            cmd += ["-loop", "1", "-i", str(still)]
            layers.append((f"{emo}/idle-still", next_inp, idle_iv))
            next_inp += 1

        if talk_mov.exists() and talk_iv:
            cmd += ["-stream_loop", "-1", "-i", str(talk_mov)]
            layers.append((f"{emo}/talk", next_inp, talk_iv))
            next_inp += 1
        elif talk_iv and still.exists():
            # No talk loop — keep still face during speech rather than going blank
            cmd += ["-loop", "1", "-i", str(still)]
            layers.append((f"{emo}/talk-still", next_inp, talk_iv))
            next_inp += 1

    if not layers:
        raise SystemExit("no Orbit layers resolved")

    print(f"  Orbit anim layers: {len(layers)} (blink/talk loops={'yes' if ORBIT_LOOPS.exists() else 'no'})")

    filters: list[str] = []
    cur = "[0:v]"
    x_expr = _simple_pos_expr("curious", "x")
    y_expr = _simple_pos_expr("curious", "y")
    for i, (label, inp, ivals) in enumerate(layers):
        filters.append(_orbit_life_filter(f"[{inp}:v]", f"[orb{i}]"))
        enable = "+".join(
            f"between(t\\,{max(0.0, a - 0.04):.3f}\\,{b + 0.04:.3f})" for a, b in ivals
        )
        filters.append(
            f"{cur}[orb{i}]overlay=x='{x_expr}':y='{y_expr}':format=auto:"
            f"alpha=straight:eof_action=pass:enable='{enable}'[v{i}]"
        )
        cur = f"[v{i}]"

    fc_path = out.parent / "_orbit_fc_v21.txt"
    fc_path.write_text(";\n".join(filters) + "\n")

    cmd += [
        "-filter_complex_script", str(fc_path),
        "-map", cur, "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{timeline:.3f}",
        "-movflags", "+faststart",
        str(out),
    ]
    subprocess.run(cmd, check=True)



def main():
    VIBRANT.mkdir(parents=True, exist_ok=True)
    ORBIT_NARR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="orbit_noloop_") as td:
        td = Path(td)
        print("building VO with chapter pauses…")
        vo, markers = build_vo(td)
        vo_dur = probe(vo)
        print(f"VO {vo_dur:.2f}s markers={len(markers)} — first VO @ {next(m['start_s'] for m in markers if m['kind']=='vo'):.2f}s")

        pool = collect_unique_clips()
        print(f"unique clip pool {len(pool)}")
        edl, pic_dur, used = build_edl(vo_dur, pool, markers)
        print(f"EDL shots {len(edl)} picture {pic_dur:.1f}s unique files {len(used)}")

        parts = []
        for i, shot in enumerate(edl):
            part = td / f"p_{i:04d}.mp4"
            dur = float(shot["duration_s"])
            stable = shot["kind"] in ("card", "chapter", "brand_intro", "brand_outro")
            render_once(shot["path"], dur, part, stable_text=stable, motion_seed=i)
            parts.append(part)
            shot["duration_s"] = round(dur, 3)
            shot["end_s"] = round(shot["start_s"] + dur, 3)

        lst = td / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        bed = td / "bed.mp4"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(bed)], check=True)
        bed_dur = probe(bed)

        if bed_dur < vo_dur - 0.05:
            pad = vo_dur - bed_dur
            padded = td / "bed_pad.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(bed),
                "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(padded),
            ], check=True)
            bed = padded

        OUT.parent.mkdir(parents=True, exist_ok=True)
        timeline = max(vo_dur, probe(bed))
        print("compositing flying Orbit narrator…")
        compose_flying_orbit(bed, vo, edl, markers, OUT, timeline)

        serial = []
        for e in edl:
            serial.append({
                "kind": e["kind"], "clip": e["path"].name, "section": e.get("section"),
                "start_s": round(e["start_s"], 3), "duration_s": round(e["duration_s"], 3),
                "orbit": e.get("orbit"),
            })
        EDL_OUT.write_text(json.dumps({
            "rules": [
                "immediate_vo", "flying_orbit_narrator",
                "no_corner_pip_box", "mood_matched_expressions",
                "no_reuse", "no_loop_cutscenes",
                "chapter_cards_between_sections_only",
                "dense_visuals_timed_to_narration", "hq_broll_only",
            ],
            "structure": (
                "0.75s brand → VO with flying Orbit narrator (mood paths + expression accents) → "
                "silent chapter breaks → outro"
            ),
            "markers": markers,
            "vo": str(vo), "vo_duration_s": round(vo_dur, 3),
            "unique_clips": len(used), "shots": serial,
            "out": str(OUT),
        }, indent=2))
        print(json.dumps({
            "out": str(OUT), "duration_s": round(probe(OUT), 3),
            "shots": len(edl), "unique": len(used),
            "vo_starts_s": next(m["start_s"] for m in markers if m["kind"] == "vo"),
            "flying_orbit": True,
        }, indent=2))


if __name__ == "__main__":
    main()
