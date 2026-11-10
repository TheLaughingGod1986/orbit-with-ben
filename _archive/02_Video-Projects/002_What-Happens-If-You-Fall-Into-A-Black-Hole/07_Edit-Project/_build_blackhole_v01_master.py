#!/usr/bin/env python3
"""Video 002 — ffmpeg master: VO-locked full-frame CG assembly.

Uses approved VO v04 as the clock. Stitches unique Omni beats under each scene
(no source reuse). Time-stretches each beat to fill its VO slot (no loops).
Clip audio is muted — narration is the soundtrack.

v03:
  - Trim flash at start of 01B (science-panel morph ~0.2s)
  - Orbit brand sting after hook (01A), matching Video 001
  - Subscribe / like outro card over CTA + end-screen hold
  - Keep v02 letterbox crop + VO-section timing
"""
from __future__ import annotations

import array
import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
V001 = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
)
RAW = ROOT / "04_Generated-Clips/01_Raw"
SELECTED = ROOT / "04_Generated-Clips/02_Selected"
BRAND_DIR = ROOT / "04_Generated-Clips/03_Polished/brand"
EDIT = ROOT / "07_Edit-Project"
OUT_DIR = EDIT / "01_Masters"
VO = ROOT / "02_Voiceover/05_Master/blackhole_voiceover_v04_ivc_kDch_master.wav"
TIMELINE = EDIT / "blackhole_v03_timeline.json"
MASTER = OUT_DIR / "blackhole_v03_vo-locked_proof.mp4"
WORK = EDIT / "_work_v03"

BRAND_INTRO = BRAND_DIR / "orbit_brand_intro_bold-v05_2s.mp4"
BRAND_FALLBACK = BRAND_DIR / "orbit_brand_intro_v03_free.png"
BRAND_OUTRO = BRAND_DIR / "orbit_brand_outro_subscribe_v02.png"
BRAND_CHIME = ROOT / "06_Sound-Effects/sfx_brand_chime_v11.wav"
ORBIT_WAVE = (
    Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports")
    / "Overlay-Rig-v03/loops/orbit_wave-camera_animated-blink_6s_v01.mov"
)
ORBIT_WAVE_FALLBACK = (
    V001 / "07_Edit-Project/_orbit_proxy/orbit_wave-camera_animated-blink_6s_v01.mov"
)

BRAND_HOLD = 2.0
# Start subscribe card while VO hits "This is Orbit with Ben…"
OUTRO_START_S = 1166.0
ENDSCREEN_HOLD = 8.0  # silent hold after VO for YouTube end-screen cards
FPS = 24

# Skip Omni morph flash at head of these clips (seconds)
CLIP_TRIM_IN: dict[tuple[str, str], float] = {
    ("01", "B"): 0.25,
}

SCENE_PLAN_S = {
    "01": 38,
    "02": 66,
    "03": 60,
    "04": 124,
    "05": 101,
    "06": 129,
    "07": 81,
    "08": 90,
    "09": 79,
    "10": 76,
    "11": 98,
    "12": 63,
    "13": 48,
    "14": 84,
    "15": 32,
}

VO_SECTIONS: list[tuple[list[str], float]] = [
    (["01", "02", "03"], 153.44 / 1.07),
    (["04", "05"], 255.68 / 1.07),
    (["06", "07"], 297.20 / 1.07),
    (["08", "09", "10"], 297.28 / 1.07),
    (["11", "12", "13", "14", "15"], 260.64 / 1.07),
]

BEATS: list[tuple[str, str, str, str]] = [
    ("p0", "01", "A", "stare"),
    ("p0", "01", "B", "turn-camera"),
    ("p0", "01", "C", "determined"),
    ("p1", "02", "A", "observatory-explain"),
    ("p1", "02", "B", "first-oh"),
    ("p1", "02", "C", "intuitions-fail"),
    ("p1", "03", "A", "desk-room"),
    ("p1", "03", "B", "relieved-bob"),
    ("p1", "03", "C", "surprised-recalibrate"),
    ("p1", "04", "A", "watch-collapse"),
    ("p1", "04", "B", "supernova-flinch"),
    ("p1", "04", "C", "ligo-delight"),
    ("p1", "04", "D", "sgr-a-scale"),
    ("p1", "05", "A", "orbit-diagram"),
    ("p1", "05", "B", "cautious-reach"),
    ("p1", "05", "C", "photon-sphere"),
    ("p0", "06", "A", "probe-approach"),
    ("p0", "06", "B", "lensing-astonish"),
    ("p0", "06", "C", "eht-doughnut"),
    ("p0", "06", "D", "visitor-resolve"),
    ("p0", "07", "A", "chest-clock"),
    ("p0", "07", "B", "friend-freeze"),
    ("p0", "07", "C", "thinking-blink"),
    ("p0", "08", "A", "alarm-paddle"),
    ("p0", "08", "B", "stretch-gag"),
    ("p0", "08", "C", "embarrassed-reset"),
    ("p0", "09", "A", "eyes-widen-horizon"),
    ("p0", "09", "B", "cross-quiet"),
    ("p0", "09", "C", "failed-turnback"),
    ("p1", "10", "A", "think-pose"),
    ("p1", "10", "B", "respect-unknown"),
    ("p1", "10", "C", "logbook-resolve"),
    ("p1", "11", "A", "evaporate-delight"),
    ("p1", "11", "B", "unsettled-frontier"),
    ("p1", "11", "C", "fact-nod"),
    ("p1", "12", "A", "photon-ring-ride"),
    ("p1", "12", "B", "hold-on"),
    ("p1", "12", "C", "relieved-peel"),
    ("p0", "13", "A", "tiny-vs-jets"),
    ("p1", "13", "B", "scale-turn"),
    ("p1", "14", "A", "desk-eht"),
    ("p1", "14", "B", "earnest-camera"),
    ("p1", "14", "C", "pull-back-brink"),
    ("p0", "15", "A", "warm-wave"),
    ("p0", "15", "B", "flyaway-ember"),
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def probe_wh(path: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=p=0",
            str(path),
        ],
        text=True,
    ).strip()
    w, h = out.split(",")
    return int(w), int(h)


def raw_path(prefix: str, scene: str, beat: str, slug: str) -> Path:
    return RAW / f"scene-{scene}" / f"{prefix}_{beat}_{slug}_gemini-omni-flash_v01_raw.mp4"


def wave_path() -> Path:
    if ORBIT_WAVE.exists():
        return ORBIT_WAVE
    if ORBIT_WAVE_FALLBACK.exists():
        return ORBIT_WAVE_FALLBACK
    raise FileNotFoundError("Missing Orbit wave overlay MOV")


def stage_selected() -> dict[tuple[str, str], Path]:
    SELECTED.mkdir(parents=True, exist_ok=True)
    mapping: dict[tuple[str, str], Path] = {}
    for prefix, scene, beat, slug in BEATS:
        src = raw_path(prefix, scene, beat, slug)
        if not src.exists() or src.stat().st_size < 800_000:
            raise FileNotFoundError(f"Missing/too-small clip: {src}")
        dest = SELECTED / f"scene-{scene}" / f"{beat}_{slug}.mp4"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dest)
        mapping[(scene, beat)] = dest
    return mapping


def allocate_scene_durations(vo_dur: float) -> dict[str, float]:
    section_raw = [dur for _, dur in VO_SECTIONS]
    section_sum = sum(section_raw)
    scene_durs: dict[str, float] = {}
    for (scenes, raw_dur) in VO_SECTIONS:
        sec_dur = vo_dur * (raw_dur / section_sum)
        weights = [SCENE_PLAN_S[s] for s in scenes]
        wsum = sum(weights)
        for s, w in zip(scenes, weights):
            scene_durs[s] = sec_dur * (w / wsum)
    total = sum(scene_durs.values())
    scale = vo_dur / total
    return {k: v * scale for k, v in scene_durs.items()}


def beats_for_scene(scene: str) -> list[tuple[str, str, str, str]]:
    return [b for b in BEATS if b[1] == scene]


def letterbox_crop(path: Path) -> tuple[int, int, int, int] | None:
    fw, fh = probe_wh(path)
    side = max(8, fw // 5)
    tops: list[int] = []
    bots: list[int] = []
    for t in (0.0, 0.5, 1.0, 2.0):
        r = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-ss",
                f"{t:.2f}",
                "-i",
                str(path),
                "-frames:v",
                "1",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "gray",
                "-",
            ],
            capture_output=True,
        )
        if r.returncode != 0 or len(r.stdout) < fw * fh:
            continue
        px = array.array("B", r.stdout[: fw * fh])

        def is_bar(y: int) -> bool:
            row = px[y * fw : (y + 1) * fw]
            margins = list(row[:side]) + list(row[-side:])
            mean = sum(margins) / len(margins)
            hot = sum(1 for v in margins if v >= 30)
            return mean < 8 and hot < max(3, len(margins) // 50)

        top = 0
        while top < fh and is_bar(top):
            top += 1
        bot = 0
        while bot < fh and is_bar(fh - 1 - bot):
            bot += 1
        tops.append(top)
        bots.append(bot)

    if not tops:
        return None
    top = max(tops)
    bot = max(bots)
    if top < 40 or bot < 40:
        return None
    top = min(fh // 3, top + 4)
    bot = min(fh // 3, bot + 4)
    h = fh - top - bot
    if h < int(fh * 0.55):
        return None
    return (fw, h, 0, top)


def stretch_clip(
    src: Path, dest: Path, target_s: float, trim_in: float = 0.0
) -> None:
    """Time-stretch video to target duration (no loop). Mute audio."""
    src_dur = max(0.05, probe_dur(src) - trim_in)
    factor = target_s / src_dur
    box = letterbox_crop(src)
    filters: list[str] = []
    if box:
        w, h, x, y = box
        filters.append(f"crop={w}:{h}:{x}:{y}")
        print(f"    crop letterbox {w}:{h}:{x}:{y} from {src.name}", flush=True)
    if trim_in > 0:
        print(f"    trim_in {trim_in:.2f}s (skip flash) {src.name}", flush=True)
    filters.append(f"setpts={factor:.6f}*PTS")
    filters.append(f"fps={FPS}")
    filters.append("scale=1920:1080:force_original_aspect_ratio=increase")
    filters.append("crop=1920:1080")
    filters.append("format=yuv420p")
    vf = ",".join(filters)
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
    ]
    if trim_in > 0:
        cmd += ["-ss", f"{trim_in:.3f}"]
    cmd += [
        "-i",
        str(src),
        "-an",
        "-vf",
        vf,
        "-t",
        f"{target_s:.3f}",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        str(dest),
    ]
    run(cmd)


def render_brand(output: Path) -> None:
    """2s Orbit brand sting (Video 001 style), locked to 24fps for concat."""
    wave = wave_path()
    if BRAND_INTRO.exists():
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(BRAND_INTRO),
                "-ss",
                "0.35",
                "-i",
                str(wave),
                "-filter_complex",
                (
                    f"[0:v]trim=duration={BRAND_HOLD},setpts=PTS-STARTPTS,"
                    f"fps={FPS},scale=1920:1080:flags=lanczos,"
                    "drawbox=x=650:y=70:w=620:h=555:color=0x050913:t=fill[brand];"
                    f"[1:v]trim=duration={BRAND_HOLD},setpts=PTS-STARTPTS,"
                    f"fps={FPS},scale=570:422:flags=lanczos,"
                    "fade=t=in:st=0:d=0.18:alpha=1,"
                    "fade=t=out:st=1.78:d=0.22:alpha=1[orbit];"
                    "[brand][orbit]overlay=x=675:y=105:format=auto,"
                    "format=yuv420p[out]"
                ),
                "-map",
                "[out]",
                "-an",
                "-r",
                str(FPS),
                "-t",
                f"{BRAND_HOLD}",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                str(output),
            ]
        )
        return
    if not BRAND_FALLBACK.exists():
        raise FileNotFoundError(f"Missing brand assets in {BRAND_DIR}")
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-framerate",
            str(FPS),
            "-i",
            str(BRAND_FALLBACK),
            "-an",
            "-vf",
            (
                f"fps={FPS},scale=1920:1080:flags=lanczos,"
                "fade=t=in:st=0:d=0.18,fade=t=out:st=1.82:d=0.18,"
                "format=yuv420p"
            ),
            "-t",
            f"{BRAND_HOLD}",
            "-r",
            str(FPS),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            str(output),
        ]
    )


def render_outro(output: Path, hold: float) -> None:
    """Subscribe / like CTA card with animated Orbit (end-screen-safe)."""
    if not BRAND_OUTRO.exists():
        raise FileNotFoundError(BRAND_OUTRO)
    wave = wave_path()
    stretch = hold / max(probe_dur(wave), 0.1)
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-framerate",
            str(FPS),
            "-i",
            str(BRAND_OUTRO),
            "-i",
            str(wave),
            "-an",
            "-filter_complex",
            (
                f"[0:v]trim=duration={hold},setpts=PTS-STARTPTS,"
                "scale=1920:1080:flags=lanczos,"
                "drawbox=x=50:y=45:w=265:h=270:color=0x090d1c:t=fill[base];"
                f"[1:v]scale=580:430:flags=lanczos,setpts={stretch:.8f}*PTS,"
                f"trim=duration={hold},setpts=PTS-STARTPTS[orbit];"
                "[base][orbit]overlay=x=1290:y=525:format=auto,"
                "fade=t=in:st=0:d=0.45,"
                f"fade=t=out:st={max(0.5, hold - 0.75):.2f}:d=0.75,"
                "format=yuv420p[out]"
            ),
            "-map",
            "[out]",
            "-t",
            f"{hold}",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            str(output),
        ]
    )


def concat_copy(parts: list[Path], output: Path) -> None:
    """Re-encode concat so mixed fps/timebases (brand vs CG) stay frame-accurate."""
    lst = WORK / "video_concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
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
            str(lst),
            "-vf",
            f"fps={FPS},format=yuv420p",
            "-r",
            str(FPS),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-an",
            "-pix_fmt",
            "yuv420p",
            str(output),
        ]
    )


def main() -> None:
    t0 = time.time()
    if not VO.exists():
        raise SystemExit(f"Missing VO: {VO}")
    if not BRAND_INTRO.exists() and not BRAND_FALLBACK.exists():
        raise SystemExit(f"Missing brand intro in {BRAND_DIR}")
    if not BRAND_OUTRO.exists():
        raise SystemExit(f"Missing brand outro: {BRAND_OUTRO}")

    print("Staging selected clips…", flush=True)
    clips = stage_selected()
    print(f"  {len(clips)} clips staged → {SELECTED}", flush=True)

    vo_dur = probe_dur(VO)
    scene_durs = allocate_scene_durations(vo_dur)
    print(f"VO duration {vo_dur:.2f}s ({vo_dur/60:.2f} min)", flush=True)

    WORK.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    parts_dir = WORK / "parts"
    if parts_dir.exists():
        shutil.rmtree(parts_dir)
    parts_dir.mkdir()

    brand_part = parts_dir / "brand_intro.mp4"
    print(f"Rendering brand sting ({BRAND_HOLD:.1f}s)…", flush=True)
    render_brand(brand_part)

    outro_body_hold = max(4.0, vo_dur - OUTRO_START_S)
    outro_total = outro_body_hold + ENDSCREEN_HOLD
    outro_part = parts_dir / "brand_outro.mp4"
    print(
        f"Rendering subscribe outro ({outro_total:.1f}s: "
        f"{outro_body_hold:.1f}s over VO + {ENDSCREEN_HOLD:.1f}s end-screen hold)…",
        flush=True,
    )
    render_outro(outro_part, outro_total)

    timeline: list[dict] = []
    part_paths: list[Path] = []
    t_cursor = 0.0
    used: set[str] = set()
    brand_start = 0.0

    for scene in sorted(SCENE_PLAN_S.keys()):
        scene_beats = beats_for_scene(scene)
        scene_dur = scene_durs[scene]
        # Scene 01: reserve BRAND_HOLD from beat B after hook A
        if scene == "01":
            slot_a = scene_dur / len(scene_beats)
            targets = {
                "A": slot_a,
                "B": max(1.0, slot_a - BRAND_HOLD),
                "C": slot_a,
            }
            # Keep scene total exact
            drift = scene_dur - (targets["A"] + BRAND_HOLD + targets["B"] + targets["C"])
            targets["C"] += drift
        else:
            slot = scene_dur / len(scene_beats)
            targets = {b[2]: slot for b in scene_beats}

        print(f"Scene {scene}: {scene_dur:.1f}s", flush=True)
        for i, (prefix, sc, beat, slug) in enumerate(scene_beats):
            src = clips[(sc, beat)]
            key = str(src.resolve())
            if key in used:
                raise RuntimeError(f"Clip reuse forbidden: {src}")
            used.add(key)

            if scene == "15" and i == len(scene_beats) - 1:
                # Fill to VO length; subscribe outro replaces the visual tail later.
                target = max(0.5, vo_dur - t_cursor)
            else:
                target = targets[beat]

            part = parts_dir / f"{sc}_{beat}_{slug}.mp4"
            stretch_clip(src, part, target, trim_in=CLIP_TRIM_IN.get((sc, beat), 0.0))
            got = probe_dur(part)
            timeline.append(
                {
                    "scene": sc,
                    "beat": beat,
                    "slug": slug,
                    "source": str(src.relative_to(ROOT)),
                    "start_s": round(t_cursor, 3),
                    "duration_s": round(got, 3),
                    "end_s": round(t_cursor + got, 3),
                }
            )
            part_paths.append(part)
            t_cursor += got
            print(f"  {sc}{beat} {slug}: {got:.2f}s", flush=True)

            # Brand sting right after hook (01A)
            if sc == "01" and beat == "A":
                brand_start = t_cursor
                timeline.append(
                    {
                        "scene": "01",
                        "beat": "brand",
                        "slug": "orbit-brand-intro",
                        "source": str(BRAND_INTRO.relative_to(ROOT))
                        if BRAND_INTRO.exists()
                        else str(BRAND_FALLBACK.relative_to(ROOT)),
                        "start_s": round(t_cursor, 3),
                        "duration_s": round(BRAND_HOLD, 3),
                        "end_s": round(t_cursor + BRAND_HOLD, 3),
                    }
                )
                part_paths.append(brand_part)
                t_cursor += BRAND_HOLD
                print(f"  01 brand intro: {BRAND_HOLD:.2f}s @ {brand_start:.2f}s", flush=True)

    print("Concatenating CG + brand…", flush=True)
    video_body = WORK / "video_body.mp4"
    concat_copy(part_paths, video_body)

    # Splice outro over CTA tail, then hold for YouTube end screens
    print("Splicing subscribe outro + end-screen hold…", flush=True)
    video_silent = WORK / "video_silent.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video_body),
            "-i",
            str(outro_part),
            "-filter_complex",
            (
                f"[0:v]trim=0:{OUTRO_START_S:.3f},setpts=PTS-STARTPTS[v0];"
                f"[1:v]trim=duration={outro_total:.3f},setpts=PTS-STARTPTS[v1];"
                "[v0][v1]concat=n=2:v=1:a=0[v]"
            ),
            "-map",
            "[v]",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            str(video_silent),
        ]
    )

    # Pad VO with silence for end-screen hold; mix brand chime
    print("Muxing VO + brand chime…", flush=True)
    audio_filter = (
        f"[1:a]apad=pad_dur={ENDSCREEN_HOLD:.3f}[vo];"
        f"[2:a]adelay={int(brand_start * 1000)}|{int(brand_start * 1000)},"
        "volume=0.85[chime];"
        "[vo][chime]amix=inputs=2:duration=first:dropout_transition=0[a]"
    )
    inputs = ["-i", str(video_silent), "-i", str(VO)]
    if BRAND_CHIME.exists():
        inputs += ["-i", str(BRAND_CHIME)]
        fc = audio_filter
        map_a = "[a]"
    else:
        fc = f"[1:a]apad=pad_dur={ENDSCREEN_HOLD:.3f}[a]"
        map_a = "[a]"

    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            *inputs,
            "-filter_complex",
            fc,
            "-map",
            "0:v:0",
            "-map",
            map_a,
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(MASTER),
        ]
    )

    master_dur = probe_dur(MASTER)
    timeline.append(
        {
            "scene": "outro",
            "beat": "cta",
            "slug": "subscribe-like-endscreen",
            "source": str(BRAND_OUTRO.relative_to(ROOT)),
            "start_s": round(OUTRO_START_S, 3),
            "duration_s": round(outro_total, 3),
            "end_s": round(OUTRO_START_S + outro_total, 3),
        }
    )
    TIMELINE.write_text(
        json.dumps(
            {
                "version": "v03",
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "vo": str(VO.relative_to(ROOT)),
                "vo_duration_s": round(vo_dur, 3),
                "master": str(MASTER.relative_to(ROOT)),
                "master_duration_s": round(master_dur, 3),
                "brand_start_s": round(brand_start, 3),
                "outro_start_s": OUTRO_START_S,
                "endscreen_hold_s": ENDSCREEN_HOLD,
                "youtube_upload_note": (
                    "In YouTube Studio → End screen: add Video + Playlist elements "
                    "in the TOP area during the final ~20s (subscribe card leaves "
                    "top-right clear). Also enable Elements → Subscribe."
                ),
                "rules": [
                    "unique sources only (no clip reuse)",
                    "time-stretch beats to fill VO slots (no loops)",
                    "clip audio muted; VO is soundtrack",
                    "auto-crop Omni letterbox + Orbit caption",
                    "scene durations from VO section lengths",
                    "trim 01B flash (science-panel morph)",
                    "Orbit brand sting after hook (01A)",
                    "subscribe/like outro + end-screen hold",
                ],
                "scene_durations_s": {k: round(v, 3) for k, v in scene_durs.items()},
                "timeline": timeline,
            },
            indent=2,
        )
        + "\n"
    )

    print(f"\nMASTER {MASTER}", flush=True)
    print(f"  duration {master_dur/60:.2f} min ({master_dur:.1f}s)", flush=True)
    print(f"  brand @ {brand_start:.2f}s · outro @ {OUTRO_START_S:.1f}s", flush=True)
    print(f"  timeline {TIMELINE}", flush=True)
    print(f"  elapsed {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
