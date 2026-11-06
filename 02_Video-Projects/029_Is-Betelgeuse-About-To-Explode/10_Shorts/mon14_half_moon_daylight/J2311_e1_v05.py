#!/usr/bin/env python3
"""J2311 — local E1 re-cut for the Mon 14 Dec Short.

Leaves 029_short_mon14_half_moon_daylight_v04.mp4, its hash and the upload
manifest untouched. Writes v05 beside it. £0. No generation.

Picture: cut 1 at 2.30 s, cut 2 at 4.63 s, later holds under 4 s, the v04
end card removed, and a 0.30 s crossfade onto frame 0 so the loop tail is
under 1.2 s. The 22 s floor is kept (22.04 s).

Speech: the recorded words, with the setup words "So imagine" trimmed off.
The facts in the remaining lines are unchanged. The 0.22 s gap inside
sentence 1 is left in the recording and reported; closing it cannot meet
the 22 s floor and the 1.2 s tail together.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = FILM.parents[1]
EXPORT = HERE / "06_Final-Exports"
SRC = EXPORT / "029_short_mon14_half_moon_daylight_v04.mp4"
STEM = "029_short_mon14_half_moon_daylight_v05"
FINAL = EXPORT / f"{STEM}.mp4"
WORK = Path("/private/tmp/j2311-recut")
PRESERVED_SHA = "31f362f4437b4ca56ec16b8abef1dce4c65fb5a5c6c7b5b4e2ba39229a33efd5"

END = 22.04
XFADE_D = 0.30
XFADE_AT = 21.74
AUDIO_TOTAL = 22.54  # bed fade in the assembler starts at total-0.50; trim keeps the seam up

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(HERE.parent))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import _assemble_029_shorts_v04 as asm  # noqa: E402


SLICES = [
    {"a": 248.82, "b": 250.96, "local": 0.06},
    {"a": 251.88, "b": 254.38, "local": 2.40},
    {"a": 255.30, "b": 261.70, "local": 5.10},
    {"a": 274.12, "b": 275.72, "local": 11.70},
    {"a": 276.70, "b": 282.16, "local": 13.50},
    {"a": 282.92, "b": 284.64, "local": 19.16},
]

PLATES = [
    {"row": "s01_casa", "in": 0.00, "out": 2.30, "kind": "still", "src": "casa.jpg",
     "box": (0.18, 0.05, 0.82, 0.95), "rings": True, "drive": True},
    {"row": "s02_neutrino", "in": 2.30, "out": 4.63, "kind": "neutrino"},
    {"row": "s03_chajnantor", "in": 4.63, "out": 8.14, "kind": "video", "src": "chajnantor_mw.m4v",
     "offset": 3.25, "mode": "band"},
    {"row": "s04_epic", "in": 8.14, "out": 11.60, "kind": "still", "src": "dscovr_epic.jpg",
     "box": (0.12, 0.08, 0.88, 0.92)},
    {"row": "s05_orion_flare", "in": 11.60, "out": 15.40, "kind": "code",
     "src": "code_graphic_029_r25_orion_v01.mp4", "offset": 0.4},
    {"row": "s06_half_moon", "in": 15.40, "out": 19.06, "kind": "still", "src": "half_moon.jpg",
     "box": (0.1, 0.08, 0.9, 0.92)},
    {"row": "s07_daylight", "in": 19.06, "out": 21.74, "kind": "code",
     "src": "code_graphic_029_r27_orion_v01.mp4", "offset": 2.0},
]


def run(cmd: list) -> None:
    sp.run([str(c) for c in cmd], check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dur(path: Path) -> float:
    return float(sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def build_words() -> tuple[list[dict], float]:
    words = []
    for sl in SLICES:
        for w in asm.ALL_WORDS:
            if w["end"] <= sl["a"] + 0.005 or w["start"] >= sl["b"] - 0.005:
                continue
            start = round(w["start"] - sl["a"] + sl["local"], 3)
            end = round(min(sl["b"], w["end"]) - sl["a"] + sl["local"], 3)
            words.append({"text": w["text"], "w": w["text"], "s": start, "e": end, "start": start, "end": end})
    last = round(SLICES[-1]["local"] + (SLICES[-1]["b"] - SLICES[-1]["a"]), 3)
    return words, last


def clips(t: float, words: list[dict]) -> bool:
    return any(w["s"] < t - 0.02 and w["e"] > t + 0.02 for w in words)


def assert_plan(words: list[dict], last: float) -> None:
    joined = " ".join(w["w"] for w in words)
    if not joined.startswith("the night Betelgeuse explodes."):
        raise SystemExit(f"unexpected opening: {joined[:80]}")
    if "So" in joined.split() or "imagine" in joined.split():
        raise SystemExit("setup words were not trimmed")
    if abs(words[0]["s"] - 0.06) > 0.02:
        raise SystemExit(f"onset {words[0]['s']}")
    explodes = next(w for w in words if w["w"].startswith("explodes"))
    if explodes["s"] > 1.5:
        raise SystemExit(f"surprise {explodes['s']}")
    the = next(w for w in words if w["w"] == "The")
    if the["s"] - explodes["e"] >= 0.25:
        raise SystemExit(f"breath {the['s'] - explodes['e']}")
    if abs(last - 20.88) > 0.02:
        raise SystemExit(f"last word {last}")
    if not (22.0 <= END < last + 1.2):
        raise SystemExit(f"length pair end={END} last={last}")
    for i, p in enumerate(PLATES):
        if i == 0 and p["out"] > 2.8:
            raise SystemExit("cut 1")
        if i == 1 and p["out"] > 4.8:
            raise SystemExit("cut 2")
        if p["out"] - p["in"] > 4.0:
            raise SystemExit(f"hold {p['row']}")
        if clips(p["out"], words) and p["out"] < XFADE_AT - 0.01:
            raise SystemExit(f"cut clips a word at {p['out']} ({p['row']})")
    night = next(w for w in words if w["w"] == "night")
    bet = next(w for w in words if w["w"] == "Betelgeuse")
    gap = round(bet["s"] - night["e"], 3)
    if gap <= 0.15:
        raise SystemExit(f"expected the recorded 0.22 s gap, got {gap}")
    print(f"plan ok last={last} gap={gap} explodes={explodes['s']} breath={round(the['s'] - explodes['e'], 3)}", flush=True)


def render_picture(words_unused: list[dict]) -> tuple[Path, list[dict], list[dict]]:
    concat = []
    cuts = []
    pool = []
    seen = set()
    for i, p in enumerate(PLATES):
        piece = WORK / f"piece_{i:02d}.mp4"
        pdur = round(p["out"] - p["in"], 3)
        kind = p["kind"]
        src_name = p.get("src", "code_graphic_029_mon_neutrino_v01.mp4")
        if kind == "still":
            animated = bool(p.get("rings") or p.get("drive"))
            up = asm.render_still(
                asm.HDIR / p["src"], pdur, piece, p["box"], pct=0.04,
                rings=p.get("rings", False), drive=p.get("drive", False),
                save_f0=(WORK / "open_f0.png") if i == 0 else None,
            )
            video = animated
            framing = {"offset": 0.0} if animated else {"box": list(p["box"])}
        elif kind == "video":
            up = asm.render_video(asm.resolve_src(p), p.get("offset", 0.0), pdur, piece, p.get("mode", "crop"))
            video = True
            framing = {"offset": p.get("offset", 0.0)}
        elif kind == "code":
            up = asm.render_video(asm.resolve_src(p), p.get("offset", 0.0), pdur, piece, "band")
            video = True
            framing = {"offset": p.get("offset", 0.0)}
        elif kind == "neutrino":
            up = asm.render_neutrinos(pdur, piece)
            src_name = "code_graphic_029_mon_neutrino_v01.mp4"
            video = True
            framing = {"offset": 0.0}
        else:
            raise SystemExit(kind)
        cuts.append({
            "row": p["row"], "timeline_in": p["in"], "timeline_out": p["out"],
            "source": src_name, "upscale": up, "framing": framing, "video": video,
        })
        if src_name not in seen:
            seen.add(src_name)
            pool.append({"file_id": src_name, "title": asm.POOL.get(src_name, "our own code graphic")})
        concat.append(f"file '{piece.name}'")
        print(f"    plate {p['row']} {p['in']:.2f}-{p['out']:.2f}", flush=True)
    (WORK / "list.txt").write_text("\n".join(concat) + "\n")
    body = WORK / "picture_body.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"), "-c", "copy", str(body)])
    body_d = dur(body)
    offset = round(body_d - XFADE_D, 3)
    hold = round(END - offset, 3)
    if offset <= cuts[-1]["timeline_in"] or hold <= XFADE_D:
        raise SystemExit(f"bad loop geometry body={body_d} offset={offset} hold={hold}")
    cuts[-1]["timeline_out"] = offset
    looped = WORK / "picture_loop.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(body),
        "-loop", "1", "-framerate", "30", "-t", f"{hold:.3f}", "-i", str(WORK / "open_f0.png"),
        "-filter_complex",
        (
            f"[0:v]fps=30,setpts=PTS-STARTPTS,format=yuv420p[a];"
            f"[1:v]scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setpts=PTS-STARTPTS[b];"
            f"[a][b]xfade=transition=fade:duration={XFADE_D:.2f}:offset={offset:.2f},format=yuv420p[v]"
        ),
        "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
        "-t", f"{END:.3f}", str(looped),
    ])
    cuts.append({
        "row": "s08_loop",
        "timeline_in": offset,
        "timeline_out": END,
        "source": "frame0_hold_mon14_half_moon_daylight.png",
        "upscale": 1.0,
        "framing": {"offset": 0.0},
        "video": True,
        "end_card": False,
        "note": "0.30s crossfade onto frame 0, then a short hold. No end card.",
    })
    pool.append({"file_id": "frame0_hold_mon14_half_moon_daylight.png", "title": "opening frame held for the loop"})
    return looped, cuts, pool


def main() -> int:
    if sha256(SRC) != PRESERVED_SHA:
        raise SystemExit(f"v04 hash changed; refusing to cut from {sha256(SRC)}")
    words, last = build_words()
    assert_plan(words, last)
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    EXPORT.mkdir(parents=True, exist_ok=True)

    picture, cuts, pool = render_picture(words)
    teach_s, teach_e = asm.teach_at(words, "half", XFADE_AT)
    if not (teach_s >= asm.TITLE_OUT - 0.05 and teach_e <= XFADE_AT - 0.05 and teach_e - teach_s <= 4.0):
        raise SystemExit(f"teach window {teach_s}-{teach_e}")
    print(f"  teach {teach_s:.2f}-{teach_e:.2f}", flush=True)

    hook = asm.make_hook(WORK / "hook.png", [("BRIGHT AS A", asm.WHITE), ("HALF MOON", asm.YELLOW)])
    title = asm.make_title(WORK / "title.png")
    teach_bb = asm.make_teach(WORK / "teach.png", "HALF MOON BRIGHT")
    caps = asm.caption_chunks(words, last)
    for i, c in enumerate(caps):
        c["bbox"] = asm.make_caption(WORK / f"cap_{i:02d}.png", c["text"])

    hits = [("whoosh", 0.0, -6.0), ("tick", asm.TITLE_IN, -8.0), ("tick", teach_s, -8.0)]
    aud = asm.build_audio(WORK, SLICES, AUDIO_TOTAL, hits)
    for name in ("mix.wav", "stem_vo.wav", "stem_bed.wav", "stem_sfx.wav"):
        trimmed = WORK / f"trim_{name}"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / name), "-t", f"{END:.3f}", str(trimmed)])
        shutil.move(trimmed, WORK / name)
    cal_wav, aac_i, aac_tp = asm.calibrate_aac_wav(WORK, WORK / "mix.wav", END)
    aud["mix_lufs"] = aac_i
    aud["aac_lufs"] = aac_i
    aud["aac_tp_dbtp"] = aac_tp

    inputs = ["-t", f"{END:.3f}", "-i", str(picture)]
    for name in ("hook.png", "title.png", "teach.png"):
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{END:.3f}", "-i", str(WORK / name)]
    inputs += ["-i", str(cal_wav)]
    base = 5
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{END:.3f}", "-i", str(WORK / f"cap_{i:02d}.png")]
    fc = [
        "[0:v]fps=30,setsar=1,format=yuv420p[v0]",
        f"[1:v]format=rgba,fade=t=out:st={asm.HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='gte(t,0)*lt(t,{asm.HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={asm.TITLE_IN}:d=0.30:alpha=1,fade=t=out:st={asm.TITLE_OUT - 0.30:.2f}:d=0.30:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{asm.TITLE_IN})*lt(t,{asm.TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={teach_s}:d=0.25:alpha=1,fade=t=out:st={teach_e - 0.25:.2f}:d=0.25:alpha=1[th]",
        f"[v2][th]overlay=0:0:enable='gte(t,{teach_s})*lt(t,{teach_e})'[v3]",
    ]
    last_v = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last_v}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last_v = f"c{i}"
    fc.append(f"[{last_v}]noise=alls=3:allf=t,format=yuv420p[v]")
    run([
        "ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
        "-map", "[v]", "-map", "4:a", *shorts_encode_args(fps=30), "-t", f"{END:.3f}", str(FINAL),
    ])
    if sha256(SRC) != PRESERVED_SHA:
        raise SystemExit("v04 hash changed during the cut")

    phone = EXPORT / f"{STEM}_PHONE.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(FINAL),
        "-vf", "scale=720:1280:flags=lanczos",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone),
    ])
    cover = EXPORT / f"{STEM}_cover.jpg"
    shutil.copy2(EXPORT / "029_short_mon14_half_moon_daylight_v04_cover.jpg", cover)
    (EXPORT / f"{STEM}_cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (EXPORT / f"{STEM}_pool.json").write_text(json.dumps(pool, indent=2) + "\n")
    (EXPORT / f"{STEM}_words.json").write_text(json.dumps(words, indent=2) + "\n")
    joined = " ".join(w["w"] for w in words)
    (EXPORT / f"{STEM}_transcript.txt").write_text(joined + "\n")
    for name in ("stem_vo.wav", "stem_bed.wav", "stem_sfx.wav"):
        shutil.copy2(WORK / name, EXPORT / f"{STEM}_{name}")

    f0 = np.asarray(Image.open(WORK / "open_f0.png").convert("RGB").resize((1080, 1920)), dtype=np.float32)
    luma = 0.2126 * f0[:, :, 0] + 0.7152 * f0[:, :, 1] + 0.0722 * f0[:, :, 2]
    near_black = round(float((luma < 16).mean()), 4)
    last_png = WORK / "last.png"
    last_n = max(0, round(dur(FINAL) * 30) - 1)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(FINAL), "-vf", f"select=eq(n\\,{last_n})", "-frames:v", "1", str(last_png)])
    fl = np.asarray(Image.open(last_png).convert("RGB").resize((1080, 1920)), dtype=np.int16)
    f0i = f0.astype(np.int16)
    loop_diff = round(float(np.abs(f0i - fl).mean()), 3)

    night = next(w for w in words if w["w"] == "night")
    bet = next(w for w in words if w["w"] == "Betelgeuse")
    explodes = next(w for w in words if w["w"].startswith("explodes"))
    the = next(w for w in words if w["w"] == "The")
    holds = [(round(c["timeline_out"] - c["timeline_in"], 3), c["row"]) for c in cuts]
    meta = {
        "job": "J2311",
        "label": "EXCEPTION",
        "e1_label": (
            "EXCEPTION. Local candidate only. Cuts, tail and the end card are repaired, and the "
            "setup words 'So imagine' are trimmed. The 0.22 s gap inside sentence 1 is still in "
            "the recording. This is not a full E1 PASS and not a swap."
        ),
        "slug": "mon14_half_moon_daylight",
        "stem": STEM,
        "day": "Mon 14 Dec",
        "air_date": "2026-12-14",
        "title": "How Bright Will Betelgeuse Get When It Explodes?",
        "youtube_id_preserved": "heiGCnGKTkE",
        "source_v04_sha256": PRESERVED_SHA,
        "long": {"id": "vP1BbqZ_dnM", "title": "Is Betelgeuse About to Explode?"},
        "spoken": joined,
        "trimmed_words": ["So", "imagine"],
        "last_word_end_s": last,
        "duration_s": round(dur(FINAL), 3),
        "tail_s": round(dur(FINAL) - last, 3),
        "cut1_s": 2.30,
        "cut2_s": 4.63,
        "onset_s": words[0]["s"],
        "surprise_word": "explodes",
        "surprise_s": explodes["s"],
        "sentence1_breath_s": round(the["s"] - explodes["e"], 3),
        "sentence1_internal_gap_s": round(bet["s"] - night["e"], 3),
        "sentence1_internal_gap_words": "night -> Betelgeuse",
        "loop_crossfade_s": XFADE_D,
        "loop_diff_mean_abs": loop_diff,
        "frame0_near_black_frac": near_black,
        "frame0_mean_luma": round(float(luma.mean()), 2),
        "end_card": None,
        "teach": {"text": "HALF MOON BRIGHT", "s": teach_s, "e": teach_e, "bbox": teach_bb},
        "hook": hook,
        "title_banner": title,
        "sha256": sha256(FINAL),
        "phone_sha256": sha256(phone),
        "phone_bytes": phone.stat().st_size,
        "words_count": len(words),
        "max_hold_s": max(holds)[0],
        "max_hold_row": max(holds)[1],
        "audio": aud,
        "spend": "£0",
        "heard": False,
        "watched_motion": False,
    }
    (EXPORT / f"{STEM}_e1.json").write_text(json.dumps(meta, indent=2) + "\n")
    (EXPORT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({
        "final": str(FINAL),
        "duration_s": meta["duration_s"],
        "tail_s": meta["tail_s"],
        "sha256": meta["sha256"],
        "v04_sha": sha256(SRC),
        "aac_lufs": aac_i,
        "aac_tp": aac_tp,
        "loop_diff": loop_diff,
        "near_black": near_black,
        "last_word": last,
        "surprise_s": explodes["s"],
        "internal_gap": meta["sentence1_internal_gap_s"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
