#!/usr/bin/env python3
"""Neutron Star broadcast v02 — locked later standard.

Picture-first open (already inside Part 01). Mid-film chapter cards on act
joins. Soft xfade + acrossfade. 10s last-picture hold for Studio end screens.
No brand sting first. No baked like/subscribe graphic. No /go/.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

EP = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star")
HERE = Path(__file__).resolve().parent
PARTS_DIR = HERE / "parts"
CARDS = EP / "04_Generated-Clips/03_Polished/chapter_cards"
OUT_DIR = EP / "09_Final-Export"
WORK = HERE / "parts/_work_broadcast_v02"
QC = EP / "_qc_broadcast_v02"
HOLD_S = 10.0
CARD_XFADE = 0.40
PART_XFADE = 0.40

PART_FILES = {
    "01": PARTS_DIR / "neutron_star_part-01_cursor_rough_v12.mp4",
    "02": PARTS_DIR / "neutron_star_part-02_cursor_rough_v01.mp4",
    "03": PARTS_DIR / "neutron_star_part-03_cursor_rough_v02.mp4",
    "04": PARTS_DIR / "neutron_star_part-04_cursor_rough_v01.mp4",
    "05": PARTS_DIR / "neutron_star_part-05_cursor_rough_v02.mp4",
    "06": PARTS_DIR / "neutron_star_part-06_cursor_rough_v02.mp4",
    "07": PARTS_DIR / "neutron_star_part-07_cursor_rough_v04.mp4",
    "08": PARTS_DIR / "neutron_star_part-08_cursor_rough_v01.mp4",
}
CARD_FILES = {
    "c01": CARDS / "chapter_01_01_corpse_v01.mp4",
    "c02": CARDS / "chapter_02_02_density_v01.mp4",
    "c03": CARDS / "chapter_03_03_see_v01.mp4",
    "c04": CARDS / "chapter_04_04_feel_v01.mp4",
    "c05": CARDS / "chapter_05_05_surface_v01.mp4",
}
MUSIC_FILES = {
    "01": EP / "05_Music/neutron_star_part01_score_bed_v01.mp3",
    "02": EP / "05_Music/neutron_star_part02_score_bed_v01.mp3",
    "03": EP / "05_Music/neutron_star_part03_score_bed_v01.mp3",
    "04": EP / "05_Music/neutron_star_part04_score_bed_v01.mp3",
    "05": EP / "05_Music/neutron_star_part05_score_bed_v01.mp3",
    "06": EP / "05_Music/neutron_star_part06_score_bed_v01.mp3",
    "07": EP / "05_Music/neutron_star_part07_score_bed_v01.mp3",
    "08": EP / "05_Music/neutron_star_part08_score_bed_v01.mp3",
}
# Card sits between these parts. Audio is leftover outgoing score faded
# into the incoming score — never digital silence, never two VOs.
CARD_NEIGHBORS = {
    "c01": ("01", "02"),
    "c02": ("02", "03"),
    "c03": ("03", "04"),
    "c04": ("05", "06"),
    "c05": ("07", "08"),
}

# Story order. xfade/trans apply INTO this segment from the previous.
# Cards sit on the abrupt act joins, not on the open.
TIMELINE = [
    ("01", PART_FILES["01"], "fade", 0.0),
    ("c01", CARD_FILES["c01"], "fade", CARD_XFADE),
    ("02", PART_FILES["02"], "fade", CARD_XFADE),
    ("c02", CARD_FILES["c02"], "fade", CARD_XFADE),
    ("03", PART_FILES["03"], "fade", CARD_XFADE),
    ("c03", CARD_FILES["c03"], "fade", CARD_XFADE),
    ("04", PART_FILES["04"], "fade", CARD_XFADE),
    ("05", PART_FILES["05"], "fade", 1.20),
    ("c04", CARD_FILES["c04"], "fade", CARD_XFADE),
    ("06", PART_FILES["06"], "fade", CARD_XFADE),
    ("07", PART_FILES["07"], "fade", 2.00),
    ("c05", CARD_FILES["c05"], "fade", CARD_XFADE),
    ("08", PART_FILES["08"], "fade", CARD_XFADE),
]

CHAPTER_LABELS = [
    (0.0, "Orbit hangs in the dark"),
    ("c01", "The Corpse of a Star"),
    ("c02", "Density You Can't Imagine"),
    ("c03", "What You Would See"),
    ("c04", "What You Would Feel"),
    ("c05", "The Surface That Isn't a Floor"),
]


def probe(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    ).strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def encode_bed(src: Path, dest: Path) -> None:
    reuse = (
        dest.exists()
        and dest.stat().st_size > 200_000
        and dest.stat().st_mtime >= src.stat().st_mtime
    )
    if reuse:
        print(f"reuse {dest.name}", flush=True)
        return
    print(f"encode {dest.name} from {src.name}", flush=True)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24,format=yuv420p",
        "-af", "aformat=sample_rates=48000:channel_layouts=stereo",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(dest),
    ])


def encode_card_bed(src: Path, dest: Path, prev_id: str, next_id: str) -> None:
    """Keep the locked still picture; replace silent anullsrc with living score."""
    prev_dur = probe(PART_FILES[prev_id])
    card_dur = probe(src)
    prev_music = MUSIC_FILES[prev_id]
    next_music = MUSIC_FILES[next_id]
    if not prev_music.exists() or not next_music.exists():
        raise SystemExit(f"missing score for card {src.name}: {prev_music} / {next_music}")
    # Continue the outgoing bed from just before the part ends so the
    # acrossfade off leftover music is the same score, not a VO tail.
    prev_start = max(0.0, prev_dur - CARD_XFADE)
    fade = min(0.70, max(0.25, card_dur * 0.28))
    fade_out_at = max(0.05, card_dur - fade)
    print(
        f"encode {dest.name} card-score {prev_id}@{prev_start:.2f}s → {next_id} "
        f"({card_dur:.2f}s)",
        flush=True,
    )
    graph = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,"
        f"crop=1920:1080,fps=24,format=yuv420p[v];"
        f"[1:a]atrim=start={prev_start:.3f},asetpts=PTS-STARTPTS,"
        f"apad=whole_dur={card_dur:.3f},atrim=0:{card_dur:.3f},"
        f"loudnorm=I=-28:LRA=9:TP=-3,volume=0.55,"
        f"afade=t=out:st={fade_out_at:.3f}:d={fade:.3f},"
        f"aformat=sample_rates=48000:channel_layouts=stereo[prev];"
        f"[2:a]atrim=0:{card_dur:.3f},asetpts=PTS-STARTPTS,"
        f"loudnorm=I=-28:LRA=9:TP=-3,volume=0.55,"
        f"afade=t=in:st=0:d={fade:.3f},"
        f"aformat=sample_rates=48000:channel_layouts=stereo[nxt];"
        f"[prev][nxt]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        f"alimiter=limit=0.90:level=false[a]"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src), "-i", str(prev_music), "-i", str(next_music),
        "-filter_complex", graph,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-t", f"{card_dur:.3f}",
        str(dest),
    ])


def fmt_ts(seconds: float) -> str:
    s = max(0, int(round(seconds)))
    m, sec = divmod(s, 60)
    if m >= 60:
        h, m = divmod(m, 60)
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QC.mkdir(parents=True, exist_ok=True)

    missing = [p for _, p, _, _ in TIMELINE if not p.exists() or p.stat().st_size < 50_000]
    if missing:
        raise SystemExit("missing clips:\n" + "\n".join(str(p) for p in missing))

    beds = []
    ids = []
    xfades = []
    trans = []
    for i, (sid, src, tr, xd) in enumerate(TIMELINE):
        bed = WORK / f"seg_{i:02d}_{sid}.mp4"
        if sid in CARD_NEIGHBORS:
            prev_id, next_id = CARD_NEIGHBORS[sid]
            encode_card_bed(src, bed, prev_id, next_id)
        else:
            encode_bed(src, bed)
        beds.append(bed)
        ids.append(sid)
        if i > 0:
            xfades.append(float(TIMELINE[i][3]))
            trans.append(str(TIMELINE[i][2]))

    n = len(beds)
    durs = [probe(b) for b in beds]
    offsets = [0.0]
    for i in range(1, n):
        offsets.append(offsets[-1] + durs[i - 1] - xfades[i - 1])
    joined_dur = offsets[-1] + durs[-1]

    ins: list[str] = []
    for b in beds:
        ins += ["-i", str(b)]
    filters = []
    vprev, aprev = "0:v", "0:a"
    for i in range(1, n):
        vout, aout = f"v{i}", f"a{i}"
        xd = xfades[i - 1]
        tr = trans[i - 1]
        filters.append(
            f"[{vprev}][{i}:v]xfade=transition={tr}:duration={xd:.3f}:offset={offsets[i]:.3f}[{vout}]"
        )
        filters.append(f"[{aprev}][{i}:a]acrossfade=d={xd:.3f}[{aout}]")
        vprev, aprev = vout, aout

    joined = WORK / "joined_v02.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *ins,
        "-filter_complex", ";".join(filters),
        "-map", f"[{vprev}]", "-map", f"[{aprev}]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-t", f"{joined_dur:.3f}",
        str(joined),
    ])

    hold_at = max(0.05, joined_dur - 0.12)
    hold_frame = WORK / "hold_frame.jpg"
    hold_clip = WORK / "hold_10s.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{hold_at:.3f}", "-i", str(joined), "-frames:v", "1", "-q:v", "2",
        str(hold_frame),
    ])
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(hold_frame),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", f"{HOLD_S:.3f}",
        "-vf", "scale=1920:1080,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(hold_clip),
    ])

    master = OUT_DIR / "neutron_star_broadcast_v02.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(joined), "-i", str(hold_clip),
        "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-movflags", "+faststart",
        str(master),
    ])

    dur = probe(master)
    id_to_offset = {sid: off for sid, off in zip(ids, offsets)}

    lines = ["CHAPTERS"]
    for key, label in CHAPTER_LABELS:
        t = 0.0 if key == 0.0 else float(id_to_offset[key])
        lines.append(f"{fmt_ts(t)} {label}")
    chap_path = EP / "11_Upload-Package/Chapters/neutron_star_long_chapters_v02.txt"
    chap_path.parent.mkdir(parents=True, exist_ok=True)
    chap_path.write_text("\n".join(lines) + "\n")

    qc_times = [
        (0.5, "open_t00_5"),
        (3.0, "open_t03"),
        (5.0, "open_t05"),
        (8.0, "open_t08"),
    ]
    for sid, label in [
        ("c01", "card_corpse"),
        ("c02", "card_density"),
        ("c03", "card_see"),
        ("c04", "card_feel"),
        ("c05", "card_surface"),
    ]:
        t = id_to_offset[sid] + 0.4
        qc_times.append((t, label))
        qc_times.append((t + 2.0, f"{label}_mid"))
    qc_times += [
        (joined_dur - 2.0, "p08_last2s"),
        (joined_dur + 1.0, "hold_plus1"),
        (max(0.05, dur - 0.3), "t_last"),
    ]
    for t, name in qc_times:
        t = min(max(0.05, t), max(0.05, dur - 0.08))
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(master), "-frames:v", "1", "-q:v", "2",
            str(QC / f"qc_{name}.jpg"),
        ])

    # Short join proofs around each card.
    for sid in ("c01", "c02", "c03", "c04", "c05"):
        start = max(0.0, id_to_offset[sid] - 1.5)
        clip = QC / f"join_{sid}.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{start:.3f}", "-i", str(master), "-t", "6.0",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k",
            str(clip),
        ])

    # Longer P03→P04 VO proof (last line, card, first line of P04).
    vo_join = EP / "_qc_p03_p04_vo"
    vo_join.mkdir(parents=True, exist_ok=True)
    c03_at = float(id_to_offset["c03"])
    start = max(0.0, c03_at - 6.0)
    vo_clip = vo_join / "join_p03_card_p04.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{start:.3f}", "-i", str(master), "-t", "14.0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(vo_clip),
    ])
    print(f"vo join {vo_clip} start={start:.2f}s card@{c03_at:.2f}s", flush=True)

    open15 = PARTS_DIR / "neutron_star_broadcast_v02_open15.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(master), "-t", "15",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(open15),
    ])

    print(f"joined {joined} {probe(joined):.3f}s")
    print(f"master {master} {dur:.3f}s  hold={HOLD_S:.1f}s")
    print(f"seg ids {ids}")
    print(f"seg durs {[round(d, 2) for d in durs]}")
    print(f"offsets {[round(o, 2) for o in offsets]}")
    print(f"chapters {chap_path}")
    minutes = dur / 60.0
    if not (7.0 <= minutes <= 9.5):
        print(f"WARN duration {minutes:.2f} min is outside 7–9 target", flush=True)
    else:
        print(f"duration {minutes:.2f} min — inside 7–9 ship target", flush=True)


if __name__ == "__main__":
    main()
