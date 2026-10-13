#!/usr/bin/env python3
"""OWB compilation film (J0167) step 6b: the final join.

Order (COMPILATION_SCRIPT_v01.md): intro, card 1, 021, bridge 1, card 2, 013, bridge 2, card 3, 019, bridge 3,
card 4, 007, bridge 4, card 5, 005, closing.

Inputs (Mini scratch): segments_v03 (picture + VO/SFX stems), bed_v01 (one bed per segment), bodies_v01 (trimmed
films, picture + film-audio wav), graphics_v01 (J0207 cards and alpha timelines, ticks.json).

Picture: the three timelines are laid over bridge 1, bridge 3 and the closing at VO zero (+0.6 s lead). Every piece
is cut to its middle frames and every join is its own short xfade clip, all encoded with the same x264 settings,
then joined with the concat demuxer (no long multi-input xfade graph, which buffers whole films in RAM).
Joins: ~0.4 s at cards, 1.2 s from a film into its bridge, 0.5 s where the film keeps under 0.5 s after its last
word (021, 005) so the next VO never lands on that word.

Audio: built sample-accurately in numpy. Segments = VO + bed + SFX (timeline ticks added at ticks.json cue
times); cards = a 3 s bed piece plus the house low rumble; films = their own audio. Each piece is set to -14 LUFS
integrated (cards to -24), joins are linear crossfades of the same length as the picture xfade, and the master
goes through a -1.5 dBFS limiter. Stems (VO, SFX, bed, films) are written beside the master for the gates.

  python3 _assemble_compilation_v01.py [--out /private/tmp/owb_comp/final_v01] [--plan]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
COMP = Path("/private/tmp/owb_comp")
SEG, BED, BODY, GFX = COMP / "segments_v03", COMP / "bed_v01", COMP / "bodies_v01", COMP / "graphics_v01"
KIT = HERE / "06_Sound-Effects" / "compilation_kit_v01"
FPS, SR = 30, 48000
TARGET, CARD_TARGET = -14.0, -24.0
LIMIT = 10 ** (-1.5 / 20)
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-g", "60", "-bf", "2", "-video_track_timescale", "15360", "-an"]
TL_LEAD = 0.6
CARD_BED_LEAD = 0.5  # card bed waits out the 0.4 s join, so it never rises under the last VO word
TICK_DB, RUMBLE_DB = -22.0, -20.0
FILMS = {"021": "Saturn", "013": "Moon", "019": "Andromeda", "007": "Neutron Star", "005": "Last Star"}
CHAPTERS = [("01", "The Rings Are Leaving", "021"), ("02", "The Moon Lets Go", "013"),
            ("03", "Two Galaxies Meet", "019"), ("04", "What Dead Stars Leave", "007"),
            ("05", "The Last Light", "005")]
SHORT_HOLD = {"021", "005"}


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def frames(p):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
               "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(p)]).stdout
    return int(out.strip().split(",")[0])


def read_wav(p):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "2",
                          "-ar", str(SR), "-"], check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def write_wav(p, a):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR),
                    "-i", "-", "-c:a", "pcm_s24le", str(p)], input=a.astype(np.float32).tobytes(), check=True)


def fit(a, n):
    return a[:n] if len(a) >= n else np.vstack([a, np.zeros((n - len(a), 2), np.float32)])


def lufs(a, tmp):
    write_wav(tmp, a)
    err = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", str(tmp), "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = err[err.rfind("Integrated loudness"):]
    i = float(tail.split("I:")[1].split("LUFS")[0])
    tp = float(tail.split("Peak:")[1].split("dBFS")[0]) if "Peak:" in tail else None
    return i, tp


def place(dst, src, at_s, gain_db=0.0):
    k = int(round(at_s * SR))
    seg = src[: max(0, len(dst) - k)] * (10 ** (gain_db / 20))
    dst[k:k + len(seg)] += seg


def plan_pieces():
    ticks = json.loads((GFX / "ticks.json").read_text())
    tl = {t["file"].split("_timeline_")[1].split(".")[0]: t for t in ticks["timelines"]}
    tl_for = {"bridge1": tl["b1"], "bridge3": tl["b3"], "closing": tl["close"]}
    pieces = [dict(kind="segment", name="intro")]
    bridges = ["bridge1", "bridge2", "bridge3", "bridge4", "closing"]
    for (num, title, film), nxt in zip(CHAPTERS, bridges):
        pieces.append(dict(kind="card", name=f"card_{num}", title=title, film=film))
        pieces.append(dict(kind="film", name=f"film_{film}", film=film))
        pieces.append(dict(kind="segment", name=nxt, timeline=tl_for.get(nxt)))
    for p in pieces:
        if p["kind"] == "segment":
            p["video"] = SEG / f"{p['name']}.mp4"
        elif p["kind"] == "card":
            p["video"] = GFX / f"code_graphic_owbcomp_card_{p['name'][-2:]}.mp4"
        else:
            p["video"] = BODY / f"body_{p['film']}.mp4"
    joins = []
    for a, b in zip(pieces, pieces[1:]):
        if a["kind"] == "film":
            joins.append(15 if a["film"] in SHORT_HOLD else 36)
        else:
            joins.append(12)
    return pieces, joins


def piece_audio(p, idx, n, kit):
    """Unscaled stems of one piece: vo, sfx, bed, film (each its own array)."""
    z = lambda: np.zeros((n, 2), np.float32)
    vo, sfx, bed, film = z(), z(), z(), z()
    if p["kind"] == "segment":
        nm = p["name"]
        vo = fit(read_wav(SEG / f"{nm}_vo.wav"), n)
        sfx = fit(read_wav(SEG / f"{nm}_sfx.wav"), n)
        bed = fit(read_wav(BED / f"{nm}_bed.wav"), n)
        if p.get("timeline"):
            place(sfx, kit["tick"], p["timeline"]["tick_segment_seconds"], TICK_DB)
    elif p["kind"] == "card":
        st = kit["stretches"][idx % 2]
        off = int((2.0 + 1.7 * idx) % 6.0 * SR)
        bed = fit(st[off:].copy(), n)
        ramp = np.ones(n, np.float32)
        lead, f_in, f_out = int(CARD_BED_LEAD * SR), int(0.6 * SR), int(0.5 * SR)
        ramp[:lead] = 0
        ramp[lead:lead + f_in] = np.linspace(0, 1, f_in)
        ramp[-f_out:] = np.linspace(1, 0, f_out)
        bed *= ramp[:, None] * kit["card_bed_gain"][idx]
        place(sfx, kit["rumble"], 0.35, RUMBLE_DB)
    else:
        film = fit(read_wav(BODY / f"body_{p['film']}.wav"), n)
    return {"vo": vo, "sfx": sfx, "bed": bed, "film": film}


def build_audio(pieces, joins, out):
    kit = {"rumble": read_wav(KIT / "sfx_owb_rumble_low_v01.wav"),
           "tick": read_wav(KIT / "sfx_owb_tick_ui_v01.wav"),
           "stretches": [read_wav(BED / "stretch_A.wav"), read_wav(BED / "stretch_B.wav")],
           "card_bed_gain": {}}
    tmp = out / "_lufs_tmp.wav"
    report, starts, t = [], [], 0
    for idx, p in enumerate(pieces):
        n = int(round(p["frames"] / FPS * SR))
        p["n"] = n
        starts.append(t)
        t += n - (int(round(joins[idx] / FPS * SR)) if idx < len(joins) else 0)
        if p["kind"] == "card":
            kit["card_bed_gain"][idx] = 1.0
            bi, _ = lufs(piece_audio(p, idx, n, kit)["bed"], tmp)
            kit["card_bed_gain"][idx] = 10 ** ((CARD_TARGET - 2.0 - bi) / 20)
        s = piece_audio(p, idx, n, kit)
        i, _ = lufs(s["vo"] + s["sfx"] + s["bed"] + s["film"], tmp)
        g = (CARD_TARGET if p["kind"] == "card" else TARGET) - i
        p["gain"] = 10 ** (g / 20)
        report.append({"piece": p["name"], "lufs_before": round(i, 1), "gain_db": round(g, 1)})
        print(f"audio {p['name']}: {i:.1f} LUFS, gain {g:+.1f} dB", flush=True)
    total = t

    def env(idx, n):
        e = np.ones(n, np.float32)
        if idx:
            d = int(round(joins[idx - 1] / FPS * SR))
            e[:d] = np.linspace(0, 1, d)
        if idx < len(joins):
            d = int(round(joins[idx] / FPS * SR))
            e[-d:] *= np.linspace(1, 0, d)
        return e[:, None]

    master = np.zeros((total, 2), np.float32)
    for key in ("vo", "sfx", "bed", "film"):
        acc = np.zeros((total, 2), np.float32)
        for idx, p in enumerate(pieces):
            a = piece_audio(p, idx, p["n"], kit)[key] * p["gain"] * env(idx, p["n"])
            acc[starts[idx]:starts[idx] + p["n"]] += a[: total - starts[idx]]
        master += acc
        write_wav(out / f"stem_{key}.wav", acc)
        del acc
    peak = np.max(np.abs(master))
    write_wav(out / "master_prelimit.wav", master)
    del master
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(out / "master_prelimit.wav"), "-af",
         f"alimiter=limit={LIMIT:.4f}:attack=5:release=80:level=false", "-c:a", "pcm_s24le",
         str(out / "master.wav")])
    tmp.unlink(missing_ok=True)
    return report, float(20 * np.log10(peak + 1e-9))


def overlay_timelines(pieces, out):
    for p in pieces:
        t = p.get("timeline")
        if not t:
            continue
        dst = out / f"{p['name']}_tl.mp4"
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(p["video"]), "-itsoffset", f"{TL_LEAD}",
             "-i", str(GFX / t["file"]), "-filter_complex",
             "[1:v]format=yuva444p[g];[0:v][g]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]",
             "-map", "[v]", *X264, str(dst)])
        p["video"] = dst
        print("timeline laid", dst.name, flush=True)


def encode(src, start_f, n_f, dst, vf=""):
    chain = f"trim=start_frame={start_f}:end_frame={start_f + n_f},setpts=PTS-STARTPTS,fps={FPS},setsar=1"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src), "-vf", chain + vf, *X264, str(dst)])


def build_video(pieces, joins, out):
    parts = []
    for i, p in enumerate(pieces):
        d_in = joins[i - 1] if i else 0
        d_out = joins[i] if i < len(joins) else 0
        mid = out / f"v{i:02d}_{p['name']}.mp4"
        encode(p["video"], d_in, p["frames"] - d_in - d_out, mid)
        parts.append(mid)
        print("mid", mid.name, flush=True)
        if i < len(joins):
            nxt, d = pieces[i + 1], joins[i]
            x = out / f"x{i:02d}_{p['name']}__{nxt['name']}.mp4"
            fa = p["frames"] - d
            run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(p["video"]), "-i", str(nxt["video"]),
                 "-filter_complex",
                 f"[0:v]trim=start_frame={fa}:end_frame={fa + d},setpts=PTS-STARTPTS,fps={FPS},setsar=1[a];"
                 f"[1:v]trim=start_frame=0:end_frame={d},setpts=PTS-STARTPTS,fps={FPS},setsar=1[b];"
                 f"[a][b]xfade=transition=fade:duration={d / FPS:.4f}:offset=0[v]",
                 "-map", "[v]", *X264, str(x)])
            parts.append(x)
    lst = out / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(out / "picture.mp4")])


def cut_list(pieces, joins):
    cuts, chapters, t = [], [], 0.0
    for i, p in enumerate(pieces):
        start = t
        if p["kind"] == "segment":
            for c in json.loads((SEG / f"{p['name']}_cuts.json").read_text()):
                cuts.append(dict(c, timeline_in=round(start + c["timeline_in"], 3),
                                 timeline_out=round(start + c["timeline_out"], 3)))
            if p.get("timeline"):
                t0, t1 = p["timeline"]["visible"]
                cuts.append(dict(row=f"{p['name']}_timeline", source=Path(p["timeline"]["file"]).stem,
                                 film="comp", kind="code_graphic", overlay=True,
                                 timeline_in=round(start + TL_LEAD + t0, 3),
                                 timeline_out=round(start + TL_LEAD + t1, 3),
                                 what="countdown timeline (DATA)"))
        elif p["kind"] == "card":
            cuts.append(dict(row=p["name"], source=Path(p["video"]).stem, film=p["film"], kind="code_graphic",
                             timeline_in=round(start, 3), timeline_out=round(start + p["frames"] / FPS, 3),
                             what=f"chapter card: {p['title']}"))
            chapters.append((start, p["title"]))
        else:
            cuts.append(dict(row=p["name"], source=f"body_{p['film']}", film=p["film"], kind="film_body",
                             timeline_in=round(start, 3), timeline_out=round(start + p["frames"] / FPS, 3),
                             what=f"{p['film']} {FILMS[p['film']]} (its own passed cut, trimmed)"))
        p["start_s"] = round(start, 3)
        t += p["frames"] / FPS - (joins[i] / FPS if i < len(joins) else 0)
    return cuts, chapters, t


def ts(s):
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(COMP / "final_v01"))
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--seg", help="segments dir (default segments_v03)")
    ap.add_argument("--bed", help="bed dir (default bed_v01)")
    ap.add_argument("--resume", action="store_true",
                    help="reuse the out dir's timeline overlays and picture.mp4; rebuild audio, then mux")
    a = ap.parse_args()
    global SEG, BED
    SEG = Path(a.seg) if a.seg else SEG
    BED = Path(a.bed) if a.bed else BED
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pieces, joins = plan_pieces()
    for p in pieces:
        p["frames"] = frames(p["video"])
    cuts, chapters, total = cut_list(pieces, joins)
    chap_lines = ["0:00 Nothing in the sky is permanent"] + [f"{ts(s)} {title}" for s, title in chapters]
    print(f"{len(pieces)} pieces, {len(joins)} joins, total {total:.2f} s ({ts(total)})")
    for p in pieces:
        print(f"  {p['start_s']:8.2f}  {p['name']:<12} {p['frames'] / FPS:7.2f} s")
    print("\n".join(chap_lines))
    if a.plan:
        return
    if a.resume:
        for p in pieces:
            tl = out / f"{p['name']}_tl.mp4"
            if p.get("timeline") and tl.exists():
                p["video"] = tl
        if not (out / "picture.mp4").exists():
            sys.exit("--resume needs picture.mp4 in the out dir")
    else:
        overlay_timelines(pieces, out)
    for p in pieces:
        p["frames"] = frames(p["video"])
    report, peak = build_audio(pieces, joins, out)
    if not a.resume:
        build_video(pieces, joins, out)
    final = out / f"owb_compilation_{out.name.split('_')[-1]}.mp4"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(out / "picture.mp4"), "-i", str(out / "master.wav"),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", str(SR),
         "-shortest", "-movflags", "+faststart", str(final)])
    err = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", str(out / "master.wav"), "-af",
                          "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = err[err.rfind("Integrated loudness"):]
    i = float(tail.split("I:")[1].split("LUFS")[0])
    tp = float(tail.split("Peak:")[1].split("dBFS")[0])
    (out / "cuts.json").write_text(json.dumps(cuts, indent=1))
    (out / "chapters.txt").write_text("\n".join(chap_lines) + "\n")
    meta = {"job": "J0167", "by": "cursor", "file": str(final), "segments": str(SEG), "bed": str(BED), "duration_s": round(total, 2),
            "pieces": [{k: (str(v) if isinstance(v, Path) else v) for k, v in p.items()
                        if k not in ("timeline", "n")} for p in pieces],
            "joins_frames": joins, "audio": report, "prelimit_peak_dbfs": round(peak, 1),
            "master_lufs_i": i, "master_true_peak_dbfs": tp, "chapters": chap_lines}
    (out / "assembly.json").write_text(json.dumps(meta, indent=1))
    print(f"done {final}: {total:.2f} s, {i} LUFS, TP {tp} dBFS", flush=True)


if __name__ == "__main__":
    main()
