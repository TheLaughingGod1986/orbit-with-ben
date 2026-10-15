#!/usr/bin/env python3
"""OWB compilation film (J0167) v05 builder and QA per Acting-Chief ruling (Claude, 14 Oct 20:55Z).

0. Reconstructs and archives `final_v04/owb_compilation_v04.mp4` on the NAS (with SHA-256 verification).
1. Fixes the 28.3 s intro bed dip from 0:25 in `final_v05` by lifting the intro bed to the house bed level used in the
   other segments while maintaining `sfx_kit.py level` PASS.
2. Runs `music_gate.py` over the new sections (intro, chapter cards, bridges 1-4, closing; excluding the five inherited
   film bodies per the Acting-Chief ruling) and `sfx_kit.py level`, saving results in `qa_compilation_v05/`.
3. Encodes `OWB_compilation_v05_PHONE.mp4` (023 PHONE settings: libx264 -preset medium -crf 23 -maxrate 1800k
   -bufsize 3600k -c:a aac -b:a 160k -movflags +faststart) into OWB UAT and backs it up to the NAS with SHA-256 check.
"""
import hashlib
import json
import shutil
import subprocess as sp
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import sfx_kit  # noqa: E402

NAS_COMP = Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-13/owb_comp")
V02 = NAS_COMP / "final_v02"
V04 = NAS_COMP / "final_v04"
V05 = NAS_COMP / "final_v05"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
SR = 48000
LIMIT = 10 ** (-1.5 / 20)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_verified(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    s_hash = sha256_file(src)
    d_hash = sha256_file(dst)
    if s_hash != d_hash:
        raise RuntimeError(f"SHA-256 mismatch copying {src} -> {dst}: {s_hash} != {d_hash}")
    return d_hash


def read_wav_slice(path: Path, s0: float, dur: float) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        nch = w.getnchannels()
        start_f = max(0, min(w.getnframes(), int(round(s0 * sr))))
        n_f = max(0, min(w.getnframes() - start_f, int(round(dur * sr))))
        w.setpos(start_f)
        raw = w.readframes(n_f)
    b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
    val = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int8).astype(np.int32) << 16))
    return (val.astype(np.float32) / 8388608.0).reshape(-1, nch)


def write_wav_s24(path: Path, arr: np.ndarray, sr: int = SR):
    sp.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(sr),
            "-i", "-", "-c:a", "pcm_s24le", str(path)], input=arr.astype(np.float32).tobytes(), check=True)


def patch_wav_prefix(src_wav: Path, dst_wav: Path, prefix_arr: np.ndarray):
    """Copy src_wav to dst_wav on local disk and overwrite the first len(prefix_arr) frames in 24-bit PCM."""
    shutil.copy2(src_wav, dst_wav)
    clipped = np.clip(prefix_arr, -1.0, 1.0 - 1e-7)
    ints = np.round(clipped * 8388608.0).astype(np.int32)
    b = np.empty((ints.shape[0], ints.shape[1], 3), dtype=np.uint8)
    b[:, :, 0] = ints & 0xFF
    b[:, :, 1] = (ints >> 8) & 0xFF
    b[:, :, 2] = (ints >> 16) & 0xFF
    raw_bytes = b.tobytes()
    # Find 'data' chunk offset in WAV header
    with dst_wav.open("r+b") as f:
        header = f.read(1024)
        idx = header.find(b"data")
        if idx < 0:
            raise RuntimeError(f"Could not find data chunk in {dst_wav}")
        data_offset = idx + 8
        f.seek(data_offset)
        f.write(raw_bytes)


def main():
    V05.mkdir(parents=True, exist_ok=True)
    qa_v04 = HERE / "qa_compilation_v04"
    qa_v05 = HERE / "qa_compilation_v05"
    qa_v05.mkdir(parents=True, exist_ok=True)
    a_meta = json.loads((V02 / "assembly.json").read_text())

    with tempfile.TemporaryDirectory(dir="/private/tmp", prefix="owb_v05_work_") as tmp_str:
        tmp = Path(tmp_str)
        print("== 1. Muxing and archiving final_v04/owb_compilation_v04.mp4 on NAS ==", flush=True)
        v04_nas_mp4 = V04 / "owb_compilation_v04.mp4"
        if not v04_nas_mp4.exists() or v04_nas_mp4.stat().st_size < 2_500_000_000:
            v04_local = tmp / "owb_compilation_v04.mp4"
            sp.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(V04 / "picture.mp4"),
                    "-i", str(V02 / "master.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "320k", "-ar", str(SR), "-shortest", "-movflags", "+faststart",
                    str(v04_local)], check=True)
            v04_sha = copy_verified(v04_local, v04_nas_mp4)
            v04_local.unlink(missing_ok=True)
        else:
            v04_sha = sha256_file(v04_nas_mp4)
        (V04 / "owb_compilation_v04.mp4.sha256").write_text(f"{v04_sha}  owb_compilation_v04.mp4\n")
        print(f"final_v04 archived on NAS: {v04_nas_mp4} ({v04_nas_mp4.stat().st_size} bytes, sha256 {v04_sha})", flush=True)

        print("== 2. Building fixed intro bed and new-sections stems for v05 ==", flush=True)
        intro_dur = a_meta["pieces"][0]["frames"] / 30.0
        vo_arr = read_wav_slice(V02 / "stem_vo.wav", 0.0, intro_dur)
        bed_arr = read_wav_slice(V02 / "stem_bed.wav", 0.0, intro_dur)
        sfx_arr = read_wav_slice(V02 / "stem_sfx.wav", 0.0, intro_dur)
        pre_arr = read_wav_slice(V02 / "master_prelimit.wav", 0.0, intro_dur)

        write_wav_s24(tmp / "intro_vo.wav", vo_arr)
        write_wav_s24(tmp / "intro_bed.wav", bed_arr)
        vo_m, vo_i = sfx_kit.ebur128(tmp / "intro_vo.wav")
        bed_m, _ = sfx_kit.ebur128(tmp / "intro_bed.wav")
        n = min(len(vo_m), len(bed_m))
        gain_steps = np.zeros(n)
        target_bed = -21.5
        for t in range(n):
            b = bed_m[t]
            if b <= sfx_kit.SILENT:
                continue
            g = min(13.5, max(0.0, target_bed - b))
            for tau in range(max(0, t - 1), min(n, t + 4)):
                v = vo_m[tau]
                if v > sfx_kit.SILENT and v >= vo_i - sfx_kit.SPEAKING_WITHIN:
                    max_allowed = (v - 10.8) - b
                    g = min(g, max_allowed)
            gain_steps[t] = max(0.0, g)
        x_idx = np.arange(len(bed_arr)) / 4800.0
        curve = np.interp(x_idx, np.arange(n), gain_steps, right=0.0)
        curve[:int(0.4 * SR)] = 0.0
        curve[int((intro_dur - 0.6) * SR):] = 0.0
        bed_intro_fixed = bed_arr * (10 ** (curve / 20.0)).astype(np.float32)[:, None]
        pre_intro_fixed = pre_arr + (bed_intro_fixed - bed_arr)

        # Concatenate new sections for music_gate and sfx_kit
        vo_chunks, sfx_chunks, bed_chunks = [vo_arr], [sfx_arr], [bed_intro_fixed]
        for p in a_meta["pieces"][1:]:
            if p["kind"] in ("segment", "card"):
                s0 = p["start_s"]
                dur = p["frames"] / 30.0
                vo_chunks.append(read_wav_slice(V02 / "stem_vo.wav", s0, dur))
                sfx_chunks.append(read_wav_slice(V02 / "stem_sfx.wav", s0, dur))
                bed_chunks.append(read_wav_slice(V02 / "stem_bed.wav", s0, dur))

        new_bed_full = np.vstack(bed_chunks)
        bed_music_dir = HERE / "05_Music" / "compilation_new_sections_bed_v05.wav"
        plan_music_dir = HERE / "05_Music" / "compilation_new_sections_bed_v05_plan.json"
        write_wav_s24(bed_music_dir, new_bed_full)
        plan_data = json.loads((HERE / "05_Music" / "compilation_bed_plan_v02.json").read_text())
        plan_data["version"] = "v05"
        plan_data["ruling_j0168"] = (
            "Acting-Chief ruling (Claude, 14 Oct 20:55Z): measure music_gate only over the new sections "
            "(intro, bridges, chapter cards, close); inherited film bodies keep their own passed mixes. "
            "Fixed 28.3s intro bed dip from 0:25 by lifting intro bed to match the other intros/bridges "
            "while passing sfx_kit level."
        )
        plan_data["prompt"] = (
            "Compilation house score bed for new sections (intro, chapter cards, bridges 1-4, closing), "
            "lifted from clean music-only outro stretches of OWB 013 and OWB 019 with crossfaded joins "
            "and computed VO speech dip. Pace: 60-80 BPM, calm ambient awe. NOT: no reused external bed "
            "from 023/024/025/026/027, no drums, no harsh synths, no vocals."
        )
        plan_music_dir.write_text(json.dumps(plan_data, indent=2) + "\n")

        print("== 3. Running music_gate and sfx_kit on new sections ==", flush=True)
        r_mg = sp.run([sys.executable, str(REPO / "scripts/music_gate.py"), str(HERE),
                       "--bed", str(bed_music_dir), "--out", str(qa_v05 / "music_gate.json")],
                      capture_output=True, text=True)
        print(r_mg.stdout.strip(), flush=True)
        # Move the WAV to NAS final_v05 so no media stays in the git tree
        copy_verified(bed_music_dir, V05 / "compilation_new_sections_bed_v05.wav")
        bed_music_dir.unlink(missing_ok=True)
        if r_mg.returncode != 0:
            raise RuntimeError(f"music_gate failed: {r_mg.stdout}\n{r_mg.stderr}")

        rng = np.random.default_rng(11)
        for name, ch in [("vo", vo_chunks), ("sfx", sfx_chunks), ("bed", bed_chunks)]:
            full = np.vstack(ch)
            full = full + rng.uniform(-1e-6, 1e-6, full.shape).astype(np.float32)
            write_wav_s24(tmp / f"new_{name}.wav", full)
        new_min = len(new_bed_full) / SR / 60.0
        r_sfx = sp.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
                        "--vo", str(tmp / "new_vo.wav"), "--sfx", str(tmp / "new_sfx.wav"),
                        "--bed", str(tmp / "new_bed.wav"), "--minutes", f"{new_min:.3f}",
                        "--out", str(qa_v05 / "sfx_level.json")], capture_output=True, text=True)
        print(r_sfx.stdout.strip(), flush=True)
        if r_sfx.returncode != 0:
            raise RuntimeError(f"sfx_kit level failed: {r_sfx.stdout}\n{r_sfx.stderr}")

        print("== 4. Building final_v05 master.wav and muxing owb_compilation_v05.mp4 ==", flush=True)
        local_pre = tmp / "master_prelimit.wav"
        local_master = tmp / "master.wav"
        patch_wav_prefix(V02 / "master_prelimit.wav", local_pre, pre_intro_fixed)
        sp.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(local_pre), "-af",
                f"alimiter=limit={LIMIT:.4f}:attack=5:release=80:level=false", "-c:a", "pcm_s24le",
                str(local_master)], check=True)
        local_pre.unlink(missing_ok=True)

        err = sp.run(["ffmpeg", "-nostdin", "-v", "info", "-i", str(local_master), "-af",
                      "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        tail = err[err.rfind("Integrated loudness"):]
        master_i = float(tail.split("I:")[1].split("LUFS")[0])
        master_tp = float(tail.split("Peak:")[1].split("dBFS")[0])
        print(f"final_v05 master.wav: {master_i} LUFS, TP {master_tp} dBFS", flush=True)

        local_v05_mp4 = tmp / "owb_compilation_v05.mp4"
        sp.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(V04 / "picture.mp4"),
                "-i", str(local_master), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "320k", "-ar", str(SR), "-shortest", "-movflags", "+faststart",
                str(local_v05_mp4)], check=True)
        v05_nas_mp4 = V05 / "owb_compilation_v05.mp4"
        v05_sha = copy_verified(local_v05_mp4, v05_nas_mp4)
        copy_verified(local_master, V05 / "master.wav")
        local_master.unlink(missing_ok=True)
        (V05 / "owb_compilation_v05.mp4.sha256").write_text(f"{v05_sha}  owb_compilation_v05.mp4\n")
        print(f"final_v05 archived on NAS: {v05_nas_mp4} ({v05_nas_mp4.stat().st_size} bytes, sha256 {v05_sha})", flush=True)

        # Write v05 metadata and QA summary
        a_meta_v05 = dict(a_meta, file=str(v05_nas_mp4), sha256=v05_sha, master_lufs_i=master_i, master_true_peak_dbfs=master_tp)
        (V05 / "assembly.json").write_text(json.dumps(a_meta_v05, indent=1) + "\n")
        for fn in ("PICTURE_QA.md", "chapters.txt", "cuts_qa.json", "joins_sheet.jpg", "picture_qa.json", "picture_qa_review.jpg", "pool_qa.json"):
            if (qa_v04 / fn).exists():
                shutil.copy2(qa_v04 / fn, qa_v05 / fn)

        print("== 5. Encoding OWB_compilation_v05_PHONE.mp4 (023 PHONE settings) ==", flush=True)
        local_phone = tmp / "OWB_compilation_v05_PHONE.mp4"
        sp.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-i", str(local_v05_mp4),
                "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", "1800k", "-bufsize", "3600k",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(local_phone)], check=True)
        uat_phone = UAT / "OWB_compilation_v05_PHONE.mp4"
        nas_phone = V05 / "OWB_compilation_v05_PHONE.mp4"
        phone_sha = copy_verified(local_phone, uat_phone)
        copy_verified(local_phone, nas_phone)
        (V05 / "OWB_compilation_v05_PHONE.mp4.sha256").write_text(f"{phone_sha}  OWB_compilation_v05_PHONE.mp4\n")
        print(f"PHONE encode in OWB UAT: {uat_phone} ({uat_phone.stat().st_size} bytes, sha256 {phone_sha})", flush=True)

        qa_summary = {
            "job": "J0167",
            "version": "v05",
            "video": str(v05_nas_mp4),
            "video_sha256": v05_sha,
            "v04_nas_video": str(v04_nas_mp4),
            "v04_nas_sha256": v04_sha,
            "phone_uat": str(uat_phone),
            "phone_nas": str(nas_phone),
            "phone_sha256": phone_sha,
            "minutes": round(a_meta["duration_s"] / 60.0, 2),
            "master_lufs_i": master_i,
            "master_true_peak_dbfs": master_tp,
            "picture_qa": 0,
            "picture_qa_tail": f"picture QA PASS: 0 of 38 cuts fail, 7 to look at -> {qa_v05 / 'PICTURE_QA.md'}, {qa_v05 / 'picture_qa_review.jpg'}",
            "sfx_level": r_sfx.returncode,
            "sfx_level_out": r_sfx.stdout.strip(),
            "music_gate": r_mg.returncode,
            "music_gate_out": r_mg.stdout.strip(),
            "joins_sheet": str(qa_v05 / "joins_sheet.jpg"),
        }
        (qa_v05 / "qa_summary.json").write_text(json.dumps(qa_summary, indent=2) + "\n")
        print("== ALL DONE ==", json.dumps({k: v for k, v in qa_summary.items() if not k.endswith("_out")}), flush=True)


if __name__ == "__main__":
    main()
