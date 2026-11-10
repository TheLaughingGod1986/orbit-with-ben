#!/usr/bin/env python3
"""J2494 — 026 Mon 16 / Wed 18 Shorts: re-cut the opening picture only. £0, no upload.

Built on the v01 assembly (J0141, the cuts scheduled as HZGTovJu_TQ and cwU_0WWeNZ4).
The audio is the v01 file's own finished mix (same voice take, words, bed, effects),
with one level-only change: the scheduled v01 mix reads -15.2 LUFS / -1.4 dBTP (mon16)
and -14.7 LUFS / -1.5 dBTP (wed18), outside the 26 Oct gate (-14.0 +/-0.5 LUFS, true
peak <= -1.6 dBTP), so it gets a flat gain and a peak limiter, nothing else. Titles, hook text, captions and end card
come from the same v01 functions. Only the span order/lengths change:

  mon16 (first cut was 4.80 s): the Paranal opening shot is split. 2.40 s opens the
        Short, the other 2.40 s of the same shot closes the picture before the end card.
  wed18 (frame 0 was a pushed still): opens on the long's own opening Milky Way
        time-lapse (v06 0.30-2.90 s, no card; movement about 2.0 against the 1.50 floor);
        the two Voyager plates follow. The Paranal sky span (8.40) is dropped and the
        flare runs 0.30 s longer, still inside its full-disc stretch.

Every span stays inside a window the v01 plan already cleared of v06 overlay cards.
New names: v02-v04 already exist for these slugs (older cuts that changed the voice),
so the files are mon16 _v04 and wed18 _v05. v01 is not touched.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec_ = importlib.util.spec_from_file_location("v01", HERE / "_assemble_026_weekday_shorts_v01.py")
v01 = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(v01)

STAGING = Path("/Volumes/data/mac-mini-archive/youtube-staging/026")
v01.PICTURE = STAGING / "026_NearestStar_v06.mp4"
GATE = v01.REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"

RECUTS = {
    "mon16_cant_see_nearest_star": {
        "stem": "mon16_cant_see_nearest_star_v04",
        "video_id": "HZGTovJu_TQ",
        "spans": [
            (98.17, 2.40, "ESO Paranal night sky (uhd_bt_paranal_07)"),
            (152.73, 4.50, "ESO VLT from Vista time-lapse"),
            (157.57, 4.50, "NASA/ESA Hubble star field (e000256)"),
            (68.33, 4.50, "ESO La Silla Crux (bt_lasilla_crux)"),
            (200.50, 4.33, "ESO La Silla night-sky time-lapse"),
            (100.57, 2.40, "ESO Paranal night sky (uhd_bt_paranal_07), rest of the opening shot"),
        ],
    },
    "wed18_robot_reach_nearest_star": {
        "stem": "wed18_robot_reach_nearest_star_v05",
        "video_id": "cwU_0WWeNZ4",
        "spans": [
            (0.30, 2.60, "Milky Way time-lapse, opening shot of 026 v06"),
            (296.75, 2.85, "NASA Voyager plate (PIA17049)"),
            (337.45, 3.50, "NASA Voyager plate (PIA14111)"),
            (408.25, 4.50, "NASA SDO solar flare"),
            (346.50, 3.10, "ESO star trails at Paranal"),
            (13.80, 3.20, "ESO Paranal observatory (uhd_bt_paranal_06)"),
        ],
    },
}


def relevel(src: Path, work: Path) -> dict:
    """Flat gain + peak limiter on the v01 mix until the encoded AAC reads -14.0 LUFS, <= -1.8 dBTP."""
    sys.path.insert(0, str(GATE.parent))
    import gate_shorts_open as g
    i0, p0 = g.aac_loudness(src)
    gain, limit = -14.0 - i0, -2.4
    out = work / "mix_relevel.m4a"
    for n in range(8):
        lin = 10 ** (limit / 20)
        v01.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn", "-af",
                 f"volume={gain:.2f}dB,alimiter=limit={lin:.4f}:level=disabled:attack=2:release=60:latency=1",
                 "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", str(out)])
        i1, p1 = g.aac_loudness(out)
        print(f"  relevel pass {n}: gain {gain:+.2f} dB limit {limit:.1f} -> {i1} LUFS {p1} dBTP", flush=True)
        if abs(i1 + 14.0) <= 0.2 and p1 <= -1.8:
            return {"source": "v01 final mix, level only", "v01_lufs": i0, "v01_true_peak": p0,
                    "gain_db": round(gain, 2), "limiter_ceiling_db": limit, "lufs": i1, "true_peak": p1}
        if p1 > -1.8:
            limit -= 0.3
        gain += -14.0 - i1
    raise SystemExit("relevel did not converge")


def build(base: dict) -> dict:
    slug = base["slug"]
    rc = RECUTS[slug]
    stem, spans = rc["stem"], rc["spans"]
    folder = HERE / slug
    work = folder / "_work_j2494"
    out = folder / "06_Final-Exports"
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    final = out / f"{stem}.mp4"
    if final.exists():
        raise SystemExit(f"{final} exists; refuse to overwrite")
    src = STAGING / "shorts_j0141" / f"{base['stem']}.mp4"
    want = (STAGING / "shorts_j0141" / f"{base['stem']}.mp4.sha256").read_text().split()[0]
    if v01.sha256(src) != want:
        raise SystemExit(f"{src} does not hash to its recorded sha256")
    vo_len = base["vo"]
    total = round(vo_len + v01.HOLD, 2)
    card_in = round(vo_len + v01.HOLD - v01.CARD, 2)
    if abs(sum(s[1] for s in spans) - card_in) > 0.02:
        raise SystemExit(f"{slug} spans do not sum to {card_in}")
    if spans[0][1] > 3.0:
        raise SystemExit(f"{slug} first cut after 3.0 s")
    words = v01.load_words(folder / base["words"], work, vo_len)
    caps = v01.caption_chunks(words, vo_len, card_in)
    hook = v01.hook_png(work / "hook.png", base["hook"])
    title = v01.title_png(work / "title.png", base["title_rows"])
    for i, c in enumerate(caps):
        v01.caption_png(work / f"cap_{i:02d}.png", c["text"])
    end = v01.end_card_png(work / "end_card.png", base["quote"], base["voyager"])
    aud = relevel(src, work)
    pic = work / "picture_final.mp4"

    W, H, FPS, PUSH, CARD = v01.W, v01.H, v01.FPS, v01.PUSH, v01.CARD
    inputs = [
        "-t", f"{card_in:.3f}", "-i", str(work / "picture_span.mp4"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{CARD:.3f}", "-i", str(work / "end_card.png"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(work / "hook.png"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(work / "title.png"),
    ]
    base_i = 4
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i",
                   str(work / f"cap_{i:02d}.png")]
    fc = [
        f"[0:v]fps={FPS},crop=ih*9/16:ih,"
        f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.0)/1.0)/2)*2':"
        f"h='trunc({H}*(1+{PUSH}*min(t,1.0)/1.0)/2)*2':eval=frame:flags=lanczos,"
        f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[a]",
        f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p,trim=0:{CARD:.3f},setpts=PTS-STARTPTS[e]",
        "[a][e]concat=n=2:v=1:a=0[v0]",
        f"[2:v]format=rgba,fade=t=out:st={v01.HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='lt(t,{v01.HOOK_END})'[v1]",
        f"[3:v]format=rgba,fade=t=in:st={v01.TITLE_IN}:d=0.30:alpha=1,"
        f"fade=t=out:st={v01.TITLE_OUT - 0.30}:d=0.30:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='between(t,{v01.TITLE_IN},{v01.TITLE_OUT})'[v2]",
    ]
    last = "v2"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base_i + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    enc = v01.shorts_encode_args(fps=FPS)
    venc = enc[:enc.index("-c:a")]
    if not pic.exists():
        print(f"{slug}: cutting {len(spans)} spans", flush=True)
        v01.cut_spans(work, spans)
        print(f"{slug}: encoding", flush=True)
        v01.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
                 "-map", "[v]", *venc, "-an", "-t", f"{total:.3f}", str(pic)])
    v01.run(["ffmpeg", "-y", "-v", "error", "-i", str(pic), "-i", str(work / "mix_relevel.m4a"),
             "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart",
             "-t", f"{total:.3f}", str(final)])
    gate = subprocess.run([sys.executable, str(GATE), "check", str(final), "--air-date", base["air"],
                           "--id", rc["video_id"], "--json"], capture_output=True, text=True)
    (out / f"{stem}_gate.json").write_text(gate.stdout or gate.stderr)
    gate_txt = subprocess.run([sys.executable, str(GATE), "check", str(final), "--air-date", base["air"],
                               "--id", rc["video_id"]], capture_output=True, text=True)
    (out / f"{stem}_gate.txt").write_text((gate_txt.stdout or "") + (gate_txt.stderr or ""))

    t, cuts = 0.0, []
    for i, (src_t, length, label) in enumerate(spans):
        cuts.append({"row": f"s{i + 1:02d}", "timeline_in": round(t, 2), "timeline_out": round(t + length, 2),
                     "source": f"v06_{src_t:.2f}.mp4", "what": label})
        t += length
    cuts.append({"row": "end_card", "timeline_in": card_in, "timeline_out": total, "source": "end_card_thumb_A.png"})
    meta = {
        "job": "J2494", "file": str(final.relative_to(v01.REPO)), "sha256": v01.sha256(final),
        "duration_s": v01.dur(final), "listing_title": base["title"], "on_screen_title": title,
        "replaces_if_ben_oks": {"video_id": rc["video_id"], "file": src.name, "sha256": want},
        "audio": aud,
        "long": {"id": v01.LONG_ID, "title": v01.LONG_TITLE, "cut": "v06"},
        "end_card": {"start_s": card_in, "len_s": CARD, **end},
        "hook": hook, "words": len(words), "captions": caps, "cuts": cuts,
        "gate_exit": gate.returncode,
        "gate_ok": gate.returncode == 0 and '"verdict": "PASS"' in (gate.stdout or ""),
        "spend": "none", "uploaded": False,
    }
    (out / f"{stem}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{slug}: {meta['duration_s']:.2f}s gate={meta['gate_ok']} {aud['lufs']} LUFS {aud['true_peak']} dBTP "
          f"{meta['sha256'][:12]}", flush=True)
    return meta


def main() -> int:
    only = sys.argv[1:]
    fails = 0
    for base in v01.SHORTS:
        if base["slug"] in RECUTS and (not only or base["slug"] in only):
            fails += 0 if build(base)["gate_ok"] else 1
    print(f"done fails={fails}", flush=True)
    return fails


if __name__ == "__main__":
    raise SystemExit(main())
