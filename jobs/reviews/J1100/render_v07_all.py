#!/usr/bin/env python3
"""Render J1100 v07 base (text-free) and final MP4s + PHONE copies for S2, S5, S6."""
import hashlib, importlib.util, json, subprocess
from pathlib import Path

ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
OUT_ROOT = Path("/Users/benjaminoats/_desk/renders/J1100-v07")
FPS = 30

def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1048576), b""):
            h.update(b)
    return h.hexdigest()

def ff(args):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", *[str(x) for x in args]], check=True)

def dump(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def load_module(p: Path):
    spec = importlib.util.spec_from_file_location("legacy_mix", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    legacy = load_module(ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/mon30_comets/_assemble_mon30_comets_v03.py")
    frame_bytes = 1080 * 1920 * 3 // 2
    idxs = list(range(29, 4, -1)) + [2, 2, 2, 2, 0]

    for key in ["S2_027_emwQsPxnRGM", "S5_028_jJ5LkFGyzLI", "S6_028_X768qs8sNQs"]:
        out = OUT_ROOT / key
        prep = json.loads((out / "locked_preparation.json").read_text())
        work = Path("/private/tmp") / f"j1100_v07_work_{key}"
        legacy.WORK = work

        total = prep["vo_splice_map"]["total_duration_s"]
        vo_end = prep["vo_splice_map"]["vo_end_s"]
        end_frame = round(vo_end * FPS)
        total_frames = round(total * FPS)
        plan = prep["shot_plan"]

        pic_raw = work / "picture_raw.mp4"
        if not pic_raw.exists():
            raw30 = subprocess.check_output(["ffmpeg","-v","error","-i",str(work/"s00.mp4"),"-frames:v","30","-f","rawvideo","-pix_fmt","yuv420p","-"])
            frames30 = [raw30[i*frame_bytes:(i+1)*frame_bytes] for i in range(30)]
            tail_yuv = b"".join(frames30[i] for i in idxs)
            p = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","yuv420p","-s","1080x1920","-r","30","-i","-","-vf","setparams=range=tv:colorspace=bt709:color_trc=bt709:color_primaries=bt709","-c:v","libx264","-preset","fast","-qp","12",str(work/"s07.mp4")], stdin=subprocess.PIPE)
            p.communicate(tail_yuv)
            inputs = []
            for i in range(8):
                inputs += ["-i", str(work / f"s{i:02d}.mp4")]
            fg = "".join(f"[{i}:v]fps=30,format=yuv420p,setparams=range=tv:colorspace=bt709:color_trc=bt709:color_primaries=bt709[v{i}];" for i in range(8)) + "".join(f"[v{i}]" for i in range(8)) + "concat=n=8:v=1:a=0[v]"
            ff([*inputs, "-filter_complex", fg, "-map", "[v]", "-c:v", "libx264", "-preset", "fast", "-qp", "14", pic_raw])

        pic_sha = sha(pic_raw)

        if key == "S6_028_X768qs8sNQs":
            audio_input = Path("/Users/benjaminoats/_desk/renders/J1100-S6-final02/S6_028_X768qs8sNQs/S6_028_X768qs8sNQs_v05.mp4")
            audio_codec_args = ["-c:a", "copy"]
        else:
            audio_input = work / "mix.wav"
            audio_codec_args = ["-c:a", "aac", "-b:a", "192k"]

        folder = work / "overlays"

        # Exposure lift on orion_paranal if present
        orion_rows = [r for r in plan if "orion_paranal" in r["row"]]
        pre_filter = ""
        if orion_rows:
            r = orion_rows[0]
            start_f = round(r["timeline_in"] * 30)
            end_t = round(r["timeline_out"] * 30) / 30
            if key == "S6_028_X768qs8sNQs":
                start_f += 1
                start_t = start_f / 30
                pre_filter = f"eq=brightness=0.03:enable='between(n,60,73)',eq=gamma=1.25:brightness=0.015:enable='gte(t,{start_t})*lt(t,{end_t})',"
            else:
                start_t = start_f / 30
                pre_filter = f"eq=gamma=1.25:brightness=0.015:enable='gte(t,{start_t})*lt(t,{end_t})',"

        def make_fg(enable_flag: str) -> str:
            return (
                f"[0:v]{pre_filter}noise=alls=4:allf=t:all_seed=1032[basev];"
                f"[basev][1:v]overlay=0:0:enable='{enable_flag}',format=yuv420p[v]"
            )

        fg_base = make_fg("0")
        fg_final = make_fg("1")

        base_mp4 = out / f"{key}_v07_base.mp4"
        final_mp4 = out / f"{key}_v07.mp4"
        phone_mp4 = out / f"{key}_v07_PHONE.mp4"

        print(f"Rendering {base_mp4.name}...", flush=True)
        ff(["-i", pic_raw, "-framerate", "30", "-i", folder / "%05d.png", "-i", audio_input,
            "-filter_complex", fg_base, "-map", "[v]", "-map", "2:a:0", "-frames:v", total_frames,
            "-c:v", "libx264", "-preset", "fast", "-qp", "16", *audio_codec_args, "-movflags", "+faststart", base_mp4])

        print(f"Rendering {final_mp4.name}...", flush=True)
        ff(["-i", pic_raw, "-framerate", "30", "-i", folder / "%05d.png", "-i", audio_input,
            "-filter_complex", fg_final, "-map", "[v]", "-map", "2:a:0", "-frames:v", total_frames,
            "-c:v", "libx264", "-preset", "fast", "-qp", "16", *audio_codec_args, "-movflags", "+faststart", final_mp4])

        ff(["-i", final_mp4, "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "copy", phone_mp4])

        manifest = {
            "key": key,
            "version": "v07",
            "picture_raw": str(pic_raw),
            "picture_sha256": pic_sha,
            "base_picture_sha256": pic_sha,
            "base_mp4": str(base_mp4),
            "base_sha256": sha(base_mp4),
            "final_mp4": str(final_mp4),
            "final_sha256": sha(final_mp4),
            "phone_mp4": str(phone_mp4),
            "phone_sha256": sha(phone_mp4),
            "filtergraph_base": fg_base,
            "filtergraph_final": fg_final,
        }
        dump(out / "h43_provenance_manifest.json", manifest)

        level = legacy.ebur128_stats(final_mp4)
        loop = legacy.loop_measures(final_mp4)
        base_loop = legacy.loop_measures(base_mp4)
        finish_rec = {
            "status": "UNREVIEWED v07; caption-free tail; h43-LOOP and final gates",
            "I_LUFS": level[0],
            "TP_dBTP": level[1],
            "audio_pass": -14.5 <= level[0] <= -13.5 and level[1] <= -1.6,
            "loop": loop,
            "base_loop": base_loop,
            "loop_pass": max(base_loop.values()) < 2.0 and loop["masked"] < 2.0,
            "files": {
                base_mp4.name: sha(base_mp4),
                final_mp4.name: sha(final_mp4),
                phone_mp4.name: sha(phone_mp4),
            },
        }
        dump(out / "FINISH_COMPLETE.json", finish_rec)
        print(f"DONE {key}: I={level[0]} TP={level[1]} base_loop={base_loop} final_loop={loop}", flush=True)

if __name__ == "__main__":
    main()
