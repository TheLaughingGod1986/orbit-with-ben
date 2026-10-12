#!/usr/bin/env python3
"""Private Jupiter test Short. Does not upload or schedule.

World plates: Veo Fast. Orbit motion: Omni only, from the canonical still.
Voice: Ben Orbit Narrator. Script words are 01_JUPITER.md exactly.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from el_auth import load_token  # noqa: E402
from el_client import request  # noqa: E402
from orbit_gemini_omni import generate_omni_clip  # noqa: E402
from orbit_gemini_veo import resolve_api_key, strip_audio  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_SETTINGS  # noqa: E402

from google import genai  # noqa: E402
from google.genai import types  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

ENV = REPO / "02_Video-Projects/019_Andromeda-Milky-Way-Collision/07_Edit-Project/.env"
ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
OUT = REPO / "00_Brand/Channel-Setup/could-orbit-survive/jupiter_v01"
W, H = 720, 1280
VEO = "veo-3.1-fast-generate-preview"
IMAGE_MODEL = "gemini-2.5-flash-image"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

SPOKEN = (
    "Jupiter has no ground to land on. "
    "Stay, and I'll show you how long a robot lasts. "
    "In 1995, a NASA probe fell in. "
    "It lasted fifty-eight minutes. "
    "The pressure passed twenty times Earth's air. "
    "Then the signal died. No bottom. "
    "I'm not staying to find out. "
    "Watch the full film, What Would You See If You Fell Into Jupiter?"
)
LINES = [
    "Jupiter has no ground to land on.",
    "Stay, and I'll show you how long a robot lasts.",
    "In 1995, a NASA probe fell in.",
    "It lasted fifty-eight minutes.",
    "The pressure passed twenty times Earth's air.",
    "Then the signal died. No bottom.",
    "I'm not staying to find out.",
    "Watch the full film, What Would You See If You Fell Into Jupiter?",
]
LONG_TITLE = "What Would You See If You Fell Into Jupiter?"
SILENT = (
    "Silent picture only. No dialogue, no narration, no letters, no numbers, "
    "no logos, no watermark, no UI. One world: Jupiter's clouds. "
    "No Earth, no second planet, no second spacecraft, no robot, no mascot."
)
IDENTITY = (
    "Exactly one matte orange floating robot. No legs. One large black curved visor "
    "as the only face. Two cream eyes with dark pupils. Stubby arms, dark three-finger hands. "
    "One antenna. Exactly one soft underside glow, centred on the bottom. "
    "No twin, no second face, no text on the body. He is not damaged."
)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    return float(out)


def client():
    key = resolve_api_key(ENV)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GEMINI_API_KEY"] = key
    return genai.Client(api_key=key)


def save_image(response, dest: Path) -> None:
    for cand in getattr(response, "candidates", None) or []:
        content = getattr(cand, "content", None)
        for part in getattr(content, "parts", None) or []:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                dest.write_bytes(inline.data)
                return
    raise RuntimeError(f"no image bytes for {dest.name}")


def still(cli, name: str, prompt: str, *, orbit: bool) -> Path:
    dest = OUT / "stills" / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 10_000:
        print(f"still keep {name}", flush=True)
        return dest
    contents: list = []
    if orbit:
        contents.append(types.Part.from_bytes(data=ORBIT_REF.read_bytes(), mime_type="image/png"))
    contents.append(prompt)
    print(f"still {name}", flush=True)
    response = cli.models.generate_content(
        model=IMAGE_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="9:16"),
        ),
    )
    save_image(response, dest)
    print(f"  {dest.stat().st_size}", flush=True)
    return dest


def veo_world(cli, still_path: Path, prompt: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 200_000:
        print(f"veo keep {dest.name}", flush=True)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"veo {dest.name}", flush=True)
    image = types.Image.from_file(location=str(still_path))
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="9:16",
        resolution="720p",
    )
    t0 = time.time()
    try:
        operation = cli.models.generate_videos(
            model=VEO,
            source=types.GenerateVideosSource(prompt=prompt, image=image),
            config=config,
        )
    except TypeError:
        operation = cli.models.generate_videos(
            model=VEO,
            prompt=prompt,
            image=image,
            config=config,
        )
    while not operation.done:
        time.sleep(10)
        operation = cli.operations.get(operation)
        print(f"  poll {dest.stem} {int(time.time() - t0)}s", flush=True)
    if operation.error:
        raise RuntimeError(f"Veo error: {operation.error}")
    response = operation.response
    if not response or not response.generated_videos:
        raise RuntimeError("Veo returned no videos")
    video = response.generated_videos[0]
    cli.files.download(file=video.video)
    video.video.save(str(dest))
    strip_audio(dest)
    print(f"  saved {dest.stat().st_size}", flush=True)


def omni(cli, start: Path, prompt: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 200_000:
        print(f"omni keep {dest.name}", flush=True)
        return
    generate_omni_clip(
        cli,
        prompt + " " + IDENTITY,
        dest,
        orbit_ref=start,
        identity_ref=ORBIT_REF,
        aspect_ratio="9:16",
    )
    strip_audio(dest)


def voice() -> Path:
    dest = OUT / "vo.mp3"
    if dest.exists() and dest.stat().st_size > 20_000:
        print("vo keep", flush=True)
        return dest
    token, mode = load_token()
    print(f"vo auth={mode} chars={len(SPOKEN)}", flush=True)
    code, body, _ = request(
        "POST",
        f"/v1/text-to-speech/{VOICE_ID}",
        token,
        mode,
        data={"text": SPOKEN, "model_id": MODEL_ID, "voice_settings": VOICE_SETTINGS},
        query="output_format=mp3_44100_128",
        accept="audio/mpeg",
    )
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:240]!r}")
    dest.write_bytes(body)
    return dest


def fit_voice(src: Path, work: Path) -> float:
    """Land the narration inside 22–27s without freezing picture."""
    raw = dur(src)
    target = raw
    if raw > 26.5:
        target = 26.2
    elif raw < 22.4:
        target = raw  # picture hold of moving clouds covers the rest; voice stays natural
    work.parent.mkdir(parents=True, exist_ok=True)
    if abs(target - raw) > 0.15:
        tempo = raw / target
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-filter:a", f"atempo={tempo:.4f}", str(work)])
    else:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-c", "copy", str(work)])
    return dur(work)


def norm_clip(src: Path, dest: Path, start: float, length: float) -> None:
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-ss", f"{start:.3f}", "-t", f"{length:.3f}", "-i", str(src),
            "-an",
            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,format=yuv420p",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            str(dest),
        ]
    )


def whoosh(dest: Path) -> None:
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=0.45:sample_rate=48000",
            "-af", "highpass=f=300,lowpass=f=2200,afade=t=in:st=0:d=0.02,afade=t=out:st=0.12:d=0.33,volume=0.55",
            str(dest),
        ]
    )


def caption_png(text: str, dest: Path, *, hook: bool = False) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    if hook:
        words = [("THERE", WHITE), ("IS", WHITE), ("NO", WHITE), ("BOTTOM", YELLOW)]
        size = 78
        font = ImageFont.truetype(FONT, size)
        gap = 8
        widths = []
        for word, _ in words:
            box = draw.textbbox((0, 0), word, font=font, stroke_width=6)
            widths.append(box[2] - box[0])
        total = sum(widths) + gap * (len(words) - 1)
        while total > W - 48 and size > 42:
            size -= 2
            font = ImageFont.truetype(FONT, size)
            widths = []
            for word, _ in words:
                box = draw.textbbox((0, 0), word, font=font, stroke_width=6)
                widths.append(box[2] - box[0])
            total = sum(widths) + gap * (len(words) - 1)
        x = (W - total) // 2
        y = int(H * 0.38)
        for (word, color), ww in zip(words, widths):
            draw.text((x, y), word, font=font, fill=color, stroke_width=6, stroke_fill=(0, 0, 0, 255))
            x += ww + gap
    else:
        font = ImageFont.truetype(FONT, 36)
        # wrap
        words = text.split()
        rows: list[str] = []
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            box = draw.textbbox((0, 0), trial, font=font, stroke_width=4)
            if box[2] - box[0] > W - 64 and cur:
                rows.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            rows.append(cur)
        y = H - 220 - 46 * (len(rows) - 1)
        for row in rows:
            box = draw.textbbox((0, 0), row, font=font, stroke_width=4)
            x = (W - (box[2] - box[0])) // 2
            draw.text((x, y), row, font=font, fill=WHITE, stroke_width=4, stroke_fill=(0, 0, 0, 255))
            y += 46
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 40)
    words = LONG_TITLE.replace("?", "").split()
    # two centred lines
    mid = len(words) // 2
    rows = [" ".join(words[:mid]), " ".join(words[mid:]) + "?"]
    y = int(H * 0.22)
    for row in rows:
        box = draw.textbbox((0, 0), row, font=font, stroke_width=5)
        x = (W - (box[2] - box[0])) // 2
        draw.text((x, y), row, font=font, fill=WHITE, stroke_width=5, stroke_fill=(0, 0, 0, 255))
        y += 52
    im.save(dest)


def assemble(vo_dur: float) -> Path:
    work = OUT / "work"
    work.mkdir(parents=True, exist_ok=True)
    clouds = OUT / "veo" / "clouds.mp4"
    # Veo turned the probe still into Orbit twice. The beat uses the probe still,
    # pushed downward, so the craft on screen stays the one cone.
    probe = OUT / "veo" / "galileo_from_still.mp4"
    if not probe.exists():
        run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-loop", "1", "-i", str(OUT / "stills" / "galileo_9x16.png"),
                "-vf",
                f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                "zoompan=z='min(1.18,1.04+0.0012*on)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+on*1.4':d=1:s=720x1280:fps=30",
                "-t", "6.2", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                str(probe),
            ]
        )
    tumble = OUT / "omni" / "tumble.mp4"
    climb = OUT / "omni" / "climb.mp4"
    total = max(22.4, min(26.8, max(vo_dur, 22.4)))
    if vo_dur > total:
        total = min(26.8, vo_dur)
    loop = 4.0
    head = 1.0
    # Picture after the head, before the loop.
    body = total - head - loop
    tumble_len = min(6.5, body * 0.38)
    galileo_len = min(6.0, body * 0.34)
    climb_len = body - tumble_len - galileo_len
    # Trim ease-in off generated clips. Opening window used at both ends.
    norm_clip(clouds, work / "head.mp4", 0.7, head)
    norm_clip(clouds, work / "loop.mp4", 0.7, loop)
    norm_clip(tumble, work / "tumble.mp4", 0.35, tumble_len)
    norm_clip(probe, work / "galileo.mp4", 0.05, galileo_len)
    norm_clip(climb, work / "climb.mp4", 0.35, climb_len)
    concat = work / "concat.txt"
    concat.write_text(
        "\n".join(
            f"file '{p}'"
            for p in [
                work / "head.mp4",
                work / "tumble.mp4",
                work / "galileo.mp4",
                work / "climb.mp4",
                work / "loop.mp4",
            ]
        )
        + "\n"
    )
    silent = work / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
    picture_dur = dur(silent)
    # Overlays
    weights = [len(line.split()) for line in LINES]
    span = sum(weights)
    t = 0.0
    cuts = []
    for line, w in zip(LINES, weights):
        length = picture_dur * w / span
        cuts.append((t, t + length, line))
        t += length
    overlays = work / "overlays"
    overlays.mkdir(exist_ok=True)
    hook = overlays / "hook.png"
    caption_png("", hook, hook=True)
    title = overlays / "title.png"
    title_png(title)
    inputs = ["-i", str(silent)]
    filters = []
    idx = 1
    inputs += ["-i", str(hook)]
    filters.append(f"[{idx}:v]format=rgba[hook]")
    last = "0:v"
    filters.append(f"[{last}][hook]overlay=0:0:enable='between(t,0,2.2)'[v1]")
    last = "v1"
    idx = 2
    for i, (a, b, line) in enumerate(cuts):
        png = overlays / f"cap_{i}.png"
        caption_png(line, png)
        inputs += ["-i", str(png)]
        filters.append(f"[{idx}:v]format=rgba[c{i}]")
        nxt = f"c{i}o"
        filters.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[{nxt}]")
        last = nxt
        idx += 1
    galileo_label = overlays / "galileo.png"
    caption_png("1995  ·  GALILEO PROBE", galileo_label)
    minutes_label = overlays / "minutes.png"
    caption_png("58 MIN", minutes_label)
    inputs += ["-i", str(galileo_label)]
    filters.append(f"[{idx}:v]format=rgba[gal]")
    filters.append(f"[{last}][gal]overlay=0:0:enable='between(t,7.6,9.0)'[vgal]")
    last = "vgal"
    idx += 1
    inputs += ["-i", str(minutes_label)]
    filters.append(f"[{idx}:v]format=rgba[minl]")
    filters.append(f"[{last}][minl]overlay=0:0:enable='between(t,14.2,17.2)'[vmin]")
    last = "vmin"
    idx += 1
    inputs += ["-i", str(title)]
    filters.append(f"[{idx}:v]format=rgba[ttl]")
    filters.append(f"[{last}][ttl]overlay=0:0:enable='between(t,9,14)'[vout]")
    voiced = work / "vo.mp3"
    whoosh(work / "whoosh.m4a")
    final = OUT / "could-orbit-survive-jupiter.mp4"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            *inputs,
            "-i", str(voiced),
            "-i", str(work / "whoosh.m4a"),
            "-filter_complex",
            ";".join(filters)
            + ";[vout]format=yuv420p[v];"
            + f"[{idx+1}:a]volume=1,apad[va];[{idx+2}:a]adelay=0|0,volume=0.45[wh];"
            + "[va][wh]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k",
            "-t", f"{picture_dur:.3f}",
            "-movflags", "+faststart",
            str(final),
        ]
    )
    meta = {
        "duration_s": dur(final),
        "vo_s": vo_dur,
        "picture_s": picture_dur,
        "lines": LINES,
        "title_on_screen": LONG_TITLE,
        "orbit_in_s": 1.0,
    }
    (OUT / "assemble_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta), flush=True)
    return final


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not ORBIT_REF.exists():
        raise SystemExit(f"missing orbit ref {ORBIT_REF}")
    cli = client()
    clouds_still = still(
        cli,
        "clouds_9x16.png",
        "Vertical 9:16. Already mid-fall inside Jupiter. Orange, cream and rust cloud bands "
        "rush upward past the camera, fast, filling the frame. No planet marble, no ground, no robot. "
        + SILENT,
        orbit=False,
    )
    probe_still = still(
        cli,
        "galileo_9x16.png",
        "Vertical 9:16. One blunt brown-gold cone spacecraft, heat shield facing forward, "
        "falling through darker amber Jupiter clouds. Exactly one craft, the Galileo probe shape. "
        "No second ship, no robot, no text. " + SILENT,
        orbit=False,
    )
    tumble_still = still(
        cli,
        "orbit_enter_9x16.png",
        "Vertical 9:16. Jupiter cloud bands rushing upward. The attached robot is just entering "
        "from the top edge, small, tumbling, antenna up, eyes wide. One robot only. " + IDENTITY,
        orbit=True,
    )
    climb_still = still(
        cli,
        "orbit_deep_9x16.png",
        "Vertical 9:16. Darker Jupiter clouds. The attached robot is in the stream, one underside "
        "glow, looking down, not damaged, about to climb. One robot only. " + IDENTITY,
        orbit=True,
    )
    veo_world(
        cli,
        clouds_still,
        "Continue the fall. Cloud bands rush upward fast from the first frame. No ease-in. "
        "No robot. " + SILENT,
        OUT / "veo" / "clouds.mp4",
    )
    veo_world(
        cli,
        probe_still,
        "The same one brown-gold cone probe keeps falling, heat shield forward, through darker cloud. "
        "No second craft. No robot. " + SILENT,
        OUT / "veo" / "galileo.mp4",
    )
    omni(
        cli,
        tumble_still,
        "He tumbles down into the rushing Jupiter clouds, rights himself, and looks down. "
        "Continuous motion. One robot. No speech.",
        OUT / "omni" / "tumble.mp4",
    )
    omni(
        cli,
        climb_still,
        "The squeeze flexes nothing off the body. His single underside glow flares and he climbs "
        "up out of the dark clouds. He is not damaged. One robot. No speech.",
        OUT / "omni" / "climb.mp4",
    )
    vo = voice()
    voiced = OUT / "work" / "vo.mp3"
    vo_dur = fit_voice(vo, voiced)
    print(f"vo_s {vo_dur:.2f}", flush=True)
    final = assemble(vo_dur)
    print(f"FINAL {final} {dur(final):.2f}s", flush=True)


if __name__ == "__main__":
    main()
