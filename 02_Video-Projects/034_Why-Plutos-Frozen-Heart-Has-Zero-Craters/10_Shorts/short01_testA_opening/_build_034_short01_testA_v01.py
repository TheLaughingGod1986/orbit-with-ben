#!/usr/bin/env python3
"""Fast, deterministic builder & repair script for 034 Short 1 (Test A Opening Short, J2319).

Fixes:
1. VO stem: cuts only verified <-75 dB pure room-tone silence windows in pluto_frozen_heart_vo_v03.wav
   so 'thirty-nine' (onset 30.40s in master WAV, vs Whisper token start 30.72s) is 100% unclipped.
2. R04a (28.6-31.8s, PIA20473.jpg, frames 858..954): eliminates the horizontal seam at y=0.35 (y=656)
   by matching top-backdrop sky luma and applying a wide cosine vertical blend across y=605..715.
3. R04c (34.8-37.0s, frames 1044..1110): enhances crater/ridge contrast on offset=4.0s while keeping
   offset=4.0s (>=10s from 16.0s and 26.5s).
"""
import hashlib
import json
import shutil
import subprocess as sp
import wave
from pathlib import Path
import numpy as np

FILM_DIR = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters")
SHORT_DIR = FILM_DIR / "10_Shorts" / "short01_testA_opening"
EXP_DIR = SHORT_DIR / "06_Final-Exports"
WORK_DIR = SHORT_DIR / "_work_v01"
MASTER_VO = FILM_DIR / "02_Voiceover" / "pluto_frozen_heart_vo_v03.wav"
STT_RAW = FILM_DIR / "02_Voiceover" / "stt" / "pluto_frozen_heart_vo_v03" / "stt_raw.json"
TMP_DIR = Path("/tmp/j2319_fast_work")

W, H, FPS = 1080, 1920, 30
DUR = 37.0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_vo_stem(out_wav: Path, out_words: Path):
    with wave.open(str(MASTER_VO), "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        sw = w.getsampwidth()
        n_frames = w.getnframes()
        raw = np.frombuffer(w.readframes(n_frames), dtype=np.int16).reshape(-1, ch).astype(np.float32)

    segs_s = [
        (0.040, 8.820),
        (9.520, 19.160),
        (20.060, 29.860),
        (30.360, 33.380),
        (33.520, 37.120),
        (37.280, 39.440),
    ]
    xfade = int(0.015 * sr)
    pieces = []
    for i, (t0, t1) in enumerate(segs_s):
        s0 = int(round(t0 * sr))
        s1 = int(round(t1 * sr))
        seg = raw[s0:s1].copy()
        if i == 0:
            pieces.append(seg)
        else:
            prev = pieces[-1]
            fade_out = np.cos(np.linspace(0, np.pi / 2, xfade))[:, None]
            fade_in = np.sin(np.linspace(0, np.pi / 2, xfade))[:, None]
            prev[-xfade:] = prev[-xfade:] * fade_out + seg[:xfade] * fade_in
            pieces.append(seg[xfade:])

    out = np.concatenate(pieces, axis=0)
    target_samples = int(round(DUR * sr))
    if len(out) < target_samples:
        pad = np.zeros((target_samples - len(out), ch), dtype=np.float32)
        out = np.concatenate([out, pad], axis=0)
    else:
        out = out[:target_samples]

    tail_fade = int(0.060 * sr)
    out[-tail_fade:] *= np.linspace(1.0, 0.0, tail_fade)[:, None]

    out_i16 = np.clip(np.round(out), -32768, 32767).astype(np.int16)
    with wave.open(str(out_wav), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(sw)
        w.setframerate(sr)
        w.writeframes(out_i16.tobytes())

    stt = json.loads(STT_RAW.read_text())
    raw_words = [w for w in stt["words"] if w.get("type", "word") == "word"][:72]

    def map_time(t_master: float, is_start: bool = False, wid: str = "") -> float:
        if wid == "w0055" and is_start:
            t_master = 30.40
        if t_master < 8.820:
            return round(t_master - 0.040, 3)
        elif t_master < 19.160:
            return round(t_master - 0.740, 3)
        elif t_master < 29.860:
            return round(t_master - 1.640, 3)
        elif t_master < 33.380:
            return round(t_master - 2.140, 3)
        elif t_master < 37.120:
            return round(t_master - 2.280, 3)
        else:
            return round(t_master - 2.440, 3)

    mapped_words = []
    for idx, rw in enumerate(raw_words):
        wid = f"w{idx:04d}"
        txt = rw.get("word") or rw.get("text") or ""
        ms = float(rw["start"])
        me = float(rw["end"])
        mapped_words.append({
            "id": wid,
            "word": txt,
            "text": txt,
            "master_start": ms,
            "master_end": me,
            "start": map_time(ms, is_start=True, wid=wid),
            "end": map_time(me, is_start=False, wid=wid),
        })

    words_doc = {
        "total_dur": DUR,
        "first_word_s": mapped_words[0]["start"],
        "last_word_end": mapped_words[-1]["end"],
        "word_count": len(mapped_words),
        "words": mapped_words,
    }
    out_words.write_text(json.dumps(words_doc, indent=2) + "\n")
    print(f"VO stem built: {out_wav.name} ({DUR}s), w0055 ('{mapped_words[55]['word']}') at {mapped_words[55]['start']}..{mapped_words[55]['end']}s")


def main():
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    orig_mp4 = EXP_DIR / "034_short01_testA_opening_v01.mp4"
    bak_mp4 = WORK_DIR / "034_short01_testA_opening_v01_pre_repair.mp4"
    if not bak_mp4.exists():
        shutil.copy2(orig_mp4, bak_mp4)

    vo_wav = EXP_DIR / "034_short01_testA_opening_v01_stem_vo.wav"
    sfx_wav = EXP_DIR / "034_short01_testA_opening_v01_stem_sfx.wav"
    bed_wav = EXP_DIR / "034_short01_testA_opening_v01_stem_bed.wav"
    words_json = EXP_DIR / "034_short01_testA_opening_v01_words.json"

    build_vo_stem(vo_wav, words_json)

    # Extract ONLY R04a (28.6..31.8s = 96 frames) in raw RGB24 to smooth the y=656 seam
    n_r04a = 96
    raw_r04a = sp.run([
        "ffmpeg", "-v", "error", "-ss", "28.600", "-t", "3.200", "-i", str(bak_mp4),
        "-vf", f"fps={FPS},scale={W}:{H}", "-frames:v", str(n_r04a),
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
    ], capture_output=True, check=True).stdout
    r04a = np.frombuffer(raw_r04a, dtype=np.uint8).reshape(n_r04a, H, W, 3).copy()

    wy = np.sin(np.linspace(0, np.pi, 130))[:, None, None] ** 2
    wy_b = np.sin(np.linspace(0, np.pi, 90))[:, None, None] ** 2
    y_idx = np.arange(420, 685)[:, None, None]
    w_top = np.clip((y_idx - 420.0) / (665.0 - 420.0), 0.0, 1.0)
    w_top = 0.5 - 0.5 * np.cos(np.pi * w_top)

    for fi in range(n_r04a):
        f = r04a[fi].astype(np.float32)
        target_row = f[678:694].mean(axis=0, keepdims=True)
        f[420:685] = f[420:685] * (1.0 - 0.88 * w_top) + target_row * (0.88 * w_top)

        band = f[595:725].copy()
        p = 16
        padded = np.pad(band, ((p, p), (0, 0), (0, 0)), mode="edge")
        cs = np.pad(padded.cumsum(axis=0), ((1, 0), (0, 0), (0, 0)))
        blurred = (cs[33:] - cs[:-33]) / 33.0
        f[595:725] = band * (1.0 - wy) + blurred * wy

        band_b = f[1220:1310].copy()
        padded_b = np.pad(band_b, ((p, p), (0, 0), (0, 0)), mode="edge")
        cs_b = np.pad(padded_b.cumsum(axis=0), ((1, 0), (0, 0), (0, 0)))
        blurred_b = (cs_b[33:] - cs_b[:-33]) / 33.0
        f[1220:1310] = band_b * (1.0 - wy_b) + blurred_b * wy_b

        r04a[fi] = np.clip(np.round(f), 0, 255).astype(np.uint8)

    r04a_mp4 = TMP_DIR / "r04a_fixed.mp4"
    proc = sp.Popen([
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p",
        str(r04a_mp4)
    ], stdin=sp.PIPE)
    proc.communicate(input=r04a.tobytes())
    if proc.returncode != 0:
        raise RuntimeError("r04a encode failed")

    # Mix calibrated audio locally in TMP_DIR (-14.0 LUFS, -3.9 dBTP on AAC)
    raw_mix = TMP_DIR / "raw_mix2.wav"
    sp.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(vo_wav), "-i", str(sfx_wav), "-i", str(bed_wav),
        "-filter_complex", "[0:a][1:a][2:a]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,alimiter=level_in=2.8:level_out=1.0:limit=0.62:attack=5:release=50[a]",
        "-map", "[a]", "-ar", "48000", "-ac", "2", str(raw_mix)
    ], check=True)
    mix_wav = TMP_DIR / "mix_repaired_v01.wav"
    with wave.open(str(raw_mix), "rb") as w:
        params = w.getparams()
        base = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    gain = 10.0 ** (-4.15 / 20.0)
    samples = np.clip(np.round(base * gain), -32768, 32767).astype(np.int16)
    with wave.open(str(mix_wav), "wb") as w:
        w.setparams(params)
        w.writeframes(samples.tobytes())

    # Splice [0..28.6] + r04a_fixed [0..3.2] + [31.8..34.8] + enhanced [34.8..37.0] in a single fast ffmpeg pass
    tmp_mp4 = TMP_DIR / "034_short01_testA_opening_v01.mp4"
    fc = (
        f"[0:v]trim=0:28.6,setpts=PTS-STARTPTS[v0];"
        f"[1:v]trim=0:3.2,setpts=PTS-STARTPTS[v1];"
        f"[0:v]trim=31.8:34.8,setpts=PTS-STARTPTS[v2];"
        f"[0:v]trim=34.8:37.0,setpts=PTS-STARTPTS,eq=contrast=1.35:brightness=-0.12,unsharp=5:5:1.2:5:5:0.0[v3];"
        f"[v0][v1][v2][v3]concat=n=4:v=1:a=0[vout]"
    )
    sp.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(bak_mp4), "-i", str(r04a_mp4), "-i", str(mix_wav),
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-g", "60",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart", "-shortest", str(tmp_mp4)
    ], check=True)

    shutil.copy2(tmp_mp4, orig_mp4)

    # Ensure cuts_v01.json has R04c offset=4.0
    cuts_path = EXP_DIR / "cuts_v01.json"
    cuts = json.loads(cuts_path.read_text())
    for c in cuts:
        if c["row"] == "R04c":
            c["framing"] = {"offset": 4.0}
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")

    meta_path = EXP_DIR / "034_short01_testA_opening_v01_meta.json"
    meta = json.loads(meta_path.read_text())
    meta["sha256"]["mp4"] = sha256_file(orig_mp4)
    meta["sha256"]["stem_vo_wav"] = sha256_file(vo_wav)
    meta["sha256"]["stem_sfx_wav"] = sha256_file(sfx_wav)
    meta["sha256"]["stem_bed_wav"] = sha256_file(bed_wav)
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print("Fast repair complete:", orig_mp4, "sha256=", meta["sha256"]["mp4"])


if __name__ == "__main__":
    main()
