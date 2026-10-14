#!/usr/bin/env python3
"""OWB compilation film (J0167) step 5b: intro, bridge and closing segments.

Each segment lays the plate windows from COMPILATION_PLATES_v01.json (the films' own passed cuts, master audio
muted) under its recorded VO, one plate per spoken line, timed from the VO's Scribe word times, ~0.4 s xfade,
lanczos to 1080p30. Writes per segment: <seg>.mp4 (picture + VO + SFX, no bed), <seg>_vo.wav, <seg>_sfx.wav and
<seg>_cuts.json (picture_qa format). The bed and the J0207 chapter cards / timeline overlays are laid at step 6.

  python3 _assemble_compilation_segments_v01.py [--plates COMPILATION_PLATES_v02.json]
      [--out /private/tmp/owb_comp/segments_v02] [--only intro,bridge1] [--plan]

A plate with `windows` splits its line across several master windows, cut at the VO gap before each window's `from`
words.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLATES = HERE / "COMPILATION_PLATES_v02.json"
VO_DIR = HERE / "vo_compilation_v01"
KIT = HERE / "06_Sound-Effects" / "compilation_kit_v01"
MASTERS = json.loads(Path("/private/tmp/owb_comp/masters.json").read_text())

FPS = 30
XF = 0.4            # plate-to-plate crossfade
LEAD = 0.6          # picture before the first word (the film's crossfade lands here)
TAIL = 0.8          # breath after the last word, before the next card
TAIL_CLOSING = 2.6  # closing holds 2-3 s past the last word, then fades
SFX_GAIN_DB = {"rumble": -20.0, "tick": -22.0, "whoosh": -22.0}
SFX_FILE = {"rumble": "sfx_owb_rumble_low_v01.wav", "tick": "sfx_owb_tick_ui_v01.wav",
            "whoosh": "sfx_owb_whoosh_soft_v01.wav"}


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def words_of(stem):
    d = json.loads((VO_DIR / "stt" / stem / "stt_raw.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"], d.get("audio_duration_secs")


def find_words(text, words, i, n=3):
    toks = [norm(t) for t in text.replace("...", " ").split() if norm(t)][:n]
    for j in range(i, len(words)):
        if all(j + k < len(words) and norm(words[j + k]["text"]) == toks[k] for k in range(len(toks))):
            return j
    sys.exit(f"not found in Scribe words: {text!r}")


def line_starts(lines, words):
    """Index of each line's first word in the Scribe word list, matched in order on its first three tokens."""
    out, i = [], 0
    for ln in lines:
        j = find_words(ln, words, i)
        out.append(j)
        i = j + 1
    return out


def gap_mid(words, k):
    return LEAD + (words[k - 1]["end"] + words[k]["start"]) / 2


def probe_dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(path)]).decode().strip())


def plan_segment(seg):
    stem = Path(seg["vo"]).stem
    vo = HERE / seg["vo"]
    words, _ = words_of(stem)
    vo_len = probe_dur(vo)
    lines = [p["line"] for p in seg["plates"]]
    idx = line_starts(lines, words)
    tail = TAIL_CLOSING if seg["segment"] == "closing" else TAIL
    total = LEAD + vo_len + tail
    bounds = [0.0] + [gap_mid(words, k) for k in idx[1:]] + [total]
    cuts = []
    for n, p in enumerate(seg["plates"]):
        wins = p.get("windows") or [dict(film=p["film"], at=p["at"], what=p["what"])]
        edges = [bounds[n]]
        for w in wins[1:]:
            edges.append(gap_mid(words, find_words(w["from"], words, idx[n] + 1, n=2)))
        edges.append(bounds[n + 1])
        for m, w in enumerate(wins):
            row = f"{seg['segment']}_{n + 1:02d}" + (chr(ord("a") + m) if len(wins) > 1 else "")
            cuts.append(dict(row=row, source=Path(MASTERS[w["film"]]).stem, film=w["film"],
                             timeline_in=round(edges[m], 3), timeline_out=round(edges[m + 1], 3),
                             framing={"offset": w["at"]}, what=w["what"], line=p["line"],
                             sfx=p.get("sfx") if m == 0 else None, overlay=p.get("overlay") if m == 0 else None))
    return dict(segment=seg["segment"], vo=str(vo), vo_s=round(vo_len, 3), total_s=round(total, 3), cuts=cuts)


def render(plan, out):
    segname, cuts, total = plan["segment"], plan["cuts"], plan["total_s"]
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    chains, n = [], len(cuts)
    for k, c in enumerate(cuts):
        dur = c["timeline_out"] - c["timeline_in"] + (XF if k < n - 1 else 0)
        cmd += ["-ss", f"{c['framing']['offset']:.3f}", "-t", f"{dur + 0.2:.3f}", "-i", MASTERS[c["film"]]]
        chains.append(f"[{k}:v]scale=1920:1080:flags=lanczos:force_original_aspect_ratio=increase,crop=1920:1080,"
                      f"fps={FPS},setsar=1,format=yuv420p,trim=duration={dur:.3f},setpts=PTS-STARTPTS[p{k}]")
    last = "p0"
    for k in range(1, n):
        off = cuts[k]["timeline_in"]
        chains.append(f"[{last}][p{k}]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{k}]")
        last = f"x{k}"
    fade = f",fade=t=out:st={total - 1.2:.3f}:d=1.2" if segname == "closing" else ""
    chains.append(f"[{last}]trim=duration={total:.3f}{fade}[vout]")

    vo_i = n
    cmd += ["-i", plan["vo"]]
    sfx_inputs = []
    for c in cuts:
        if c.get("sfx"):
            cmd += ["-i", str(KIT / SFX_FILE[c["sfx"]])]
            sfx_inputs.append((len(sfx_inputs) + n + 1, c["sfx"], c["timeline_in"]))
    ms = int(plan_lead_ms())
    chains.append(f"[{vo_i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms},"
                  f"apad=whole_dur={total:.3f},atrim=duration={total:.3f}[vo]")
    if sfx_inputs:
        parts = []
        for j, (i, kind, at) in enumerate(sfx_inputs):
            d = int(at * 1000)
            chains.append(f"[{i}:a]aresample=48000,volume={SFX_GAIN_DB[kind]}dB,adelay={d}|{d}[s{j}]")
            parts.append(f"[s{j}]")
        chains.append("".join(parts) + f"amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total:.3f},"
                      f"atrim=duration={total:.3f}[sfx]")
    else:
        chains.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={total:.3f}[sfx]")
    chains.append("[vo]asplit=2[vo_a][vo_b]")
    chains.append("[sfx]asplit=2[sfx_a][sfx_b]")
    chains.append("[vo_a][sfx_a]amix=inputs=2:normalize=0[mix]")

    mp4, vo_wav, sfx_wav = out / f"{segname}.mp4", out / f"{segname}_vo.wav", out / f"{segname}_sfx.wav"
    cmd += ["-filter_complex", ";".join(chains),
            "-map", "[vout]", "-map", "[mix]", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(mp4),
            "-map", "[vo_b]", "-c:a", "pcm_s16le", "-ar", "48000", str(vo_wav),
            "-map", "[sfx_b]", "-c:a", "pcm_s16le", "-ar", "48000", str(sfx_wav)]
    subprocess.run(cmd, check=True)
    (out / f"{segname}_cuts.json").write_text(json.dumps(cuts, indent=1))
    return mp4


def plan_lead_ms():
    return LEAD * 1000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plates", default=str(PLATES))
    ap.add_argument("--out", default="/private/tmp/owb_comp/segments_v02")
    ap.add_argument("--only", default="")
    ap.add_argument("--plan", action="store_true", help="print the timing plan only, render nothing")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    segs = json.loads(Path(a.plates).read_text())["segments"]
    if a.only:
        segs = [s for s in segs if s["segment"] in a.only.split(",")]
    plans = [plan_segment(s) for s in segs]
    for p in plans:
        print(f"{p['segment']}: vo {p['vo_s']} s, segment {p['total_s']} s")
        for c in p["cuts"]:
            d = c["timeline_out"] - c["timeline_in"]
            flag = "  LONG" if d > 6.5 else ("  SHORT" if d < 2.0 else "")
            print(f"  {c['row']}  {c['timeline_in']:6.2f}-{c['timeline_out']:6.2f} ({d:4.1f} s)  {c['film']}@{c['framing']['offset']}{flag}")
    (out / "segments_plan.json").write_text(json.dumps(plans, indent=1))
    if a.plan:
        return
    for p in plans:
        print("render", render(p, out), flush=True)


if __name__ == "__main__":
    main()
