#!/usr/bin/env python3
"""024 Light-speed long VO — Ben Orbit Narrator LOCK (orbit_voice).

Chapter chunks from light_speed_script_master_v02.md (prose only).
Pauses (~0.7s silence) between CHAPTER CARD boundaries only.
Auth: el_auth.load_token + el_client.request — never print tokens.
Claude Locked: OWB #99 comment 5982343917.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
TOOLS = REPO / "04_Audio" / "tools"
sys.path.insert(0, str(TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import multipart_post, request, slugify  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_SETTINGS  # noqa: E402
from transcribe_vo import words_to_srt  # noqa: E402

PARTS = HERE / "parts"
MASTER_DIR = HERE / "05_Master"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/024_LightSpeed_Long_VO"
CHAPTER_GAP_S = 0.7
STEM = "light_speed_vo_v01"


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def sub_chars(token: str, mode: str) -> dict:
    code, body, _ = request(
        "GET", "/v1/user/subscription", token, mode,
        accept="application/json", timeout=60,
    )
    if code != 200:
        raise SystemExit(f"subscription failed {code}: {body[:300]!r}")
    data = json.loads(body.decode() if isinstance(body, (bytes, bytearray)) else body)
    return {
        "character_count": data.get("character_count"),
        "character_limit": data.get("character_limit"),
        "tier": data.get("tier"),
        "status": data.get("status"),
    }


def speak(token: str, mode: str, text: str, dest: Path) -> None:
    code, body, _hdrs = request(
        "POST",
        f"/v1/text-to-speech/{VOICE_ID}",
        token,
        mode,
        data={"text": text, "model_id": MODEL_ID, "voice_settings": VOICE_SETTINGS},
        query="output_format=mp3_44100_128",
        accept="audio/mpeg",
        timeout=600,
    )
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:400]!r}")
    dest.write_bytes(body)


def mp3_to_wav(mp3: Path, wav: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(mp3), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(wav),
        ],
        check=True,
    )


def make_silence(path: Path, seconds: float) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-t", f"{seconds:.3f}", "-c:a", "pcm_s16le", str(path),
        ],
        check=True,
    )


def measure_loudness(path: Path) -> dict:
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True, errors="replace",
    )
    err = proc.stderr
    mean = float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))
    peak = float(re.search(r"max_volume: (-?[\d.]+)", err).group(1))
    proc2 = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
            "-af", "ebur128=framelog=verbose", "-f", "null", "-",
        ],
        capture_output=True, text=True, errors="replace",
    )
    m = re.search(r"I:\s+(-?[\d.]+)\s+LUFS", proc2.stderr)
    lufs = float(m.group(1)) if m else None
    return {"mean_volume_db": mean, "max_volume_db": peak, "lufs_integrated": lufs}


def load_chapters() -> list[dict]:
    idx = json.loads((HERE / "chapters_index.json").read_text())
    for ch in idx:
        ch["text"] = (PARTS / ch["file"]).read_text().strip()
    return idx


def run_scribe(token: str, mode: str, audio: Path, stt_dir: Path) -> dict:
    stt_dir.mkdir(parents=True, exist_ok=True)
    stem = slugify(audio.stem)
    code, body = multipart_post(
        "/v1/speech-to-text",
        token,
        mode,
        fields={
            "model_id": "scribe_v2",
            "language_code": "eng",
            "timestamps_granularity": "word",
            "diarize": "false",
        },
        files=[("file", audio)],
        timeout=900,
    )
    if code != 200:
        raise SystemExit(f"STT failed {code}: {body[:800]!r}")
    data = json.loads(body.decode())
    raw_path = stt_dir / f"{stem}_stt_raw.json"
    raw_path.write_text(json.dumps(data, indent=2) + "\n")
    text = (data.get("text") or "").strip()
    (stt_dir / f"{stem}_transcript.txt").write_text(text + "\n")
    words = data.get("words") or []
    (stt_dir / f"{stem}.srt").write_text(words_to_srt(words))
    meta = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "audio": str(audio),
        "model_id": "scribe_v2",
        "status": "generated",
        "word_count": len([w for w in words if (w.get("type") or "word") == "word"]),
    }
    (stt_dir / f"{stem}_stt_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return data


def norm_words(text: str) -> list[str]:
    import unicodedata
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().replace("\u2019", "'")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    return [w for w in text.split() if w]


def script_diff(script: str, heard: str) -> dict:
    from difflib import SequenceMatcher
    sw, ww = norm_words(script), norm_words(heard)
    sm = SequenceMatcher(None, sw, ww)
    mismatches = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        mismatches.append({"op": tag, "script": sw[i1:i2], "whisper": ww[j1:j2]})
    equal = sum(i2 - i1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == "equal")
    rate = round(100.0 * equal / max(len(sw), 1), 2)
    return {
        "script_words": len(sw),
        "whisper_words": len(ww),
        "match_rate_pct": rate,
        "mismatches": mismatches[:40],
        "script_norm": " ".join(sw),
        "whisper_norm": " ".join(ww),
    }


def now_bst() -> str:
    return time.strftime("%Y-%m-%d %H:%M %Z")


def main() -> None:
    PARTS.mkdir(parents=True, exist_ok=True)
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    chapters = load_chapters()
    if not chapters:
        raise SystemExit("no chapters")
    full_text = "\n\n".join(ch["text"] for ch in chapters)
    token, mode = load_token()
    before = sub_chars(token, mode)
    print(
        f"auth={mode} voice={VOICE_ID} model={MODEL_ID} chapters={len(chapters)} "
        f"chars={len(full_text)} words={len(full_text.split())} "
        f"credits_before={before['character_count']}/{before['character_limit']}",
        flush=True,
    )

    concat_items: list[Path] = []
    chapter_meta = []
    sil = PARTS / f"{STEM}_chapter_gap.wav"
    make_silence(sil, CHAPTER_GAP_S)

    for i, ch in enumerate(chapters):
        mp3 = PARTS / f"{STEM}_ch{i:02d}.mp3"
        wav = PARTS / f"{STEM}_ch{i:02d}.wav"
        print(f"chapter {i}/{len(chapters)-1} {ch['title']!r} chars={len(ch['text'])}", flush=True)
        speak(token, mode, ch["text"], mp3)
        mp3_to_wav(mp3, wav)
        dur = probe_dur(wav)
        chapter_meta.append({
            "index": i,
            "title": ch["title"],
            "chars": len(ch["text"]),
            "words": len(ch["text"].split()),
            "duration_s": round(dur, 3),
            "mp3": mp3.name,
            "wav": wav.name,
        })
        concat_items.append(wav)
        if i < len(chapters) - 1:
            concat_items.append(sil)

    lst = PARTS / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in concat_items))
    master_wav = HERE / f"{STEM}.wav"
    master_mp3 = HERE / f"{STEM}.mp3"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", "concat.txt",
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(master_wav.resolve()),
        ],
        check=True,
        cwd=str(PARTS.resolve()),
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(master_wav), "-c:a", "libmp3lame", "-b:a", "128k", str(master_mp3),
        ],
        check=True,
    )
    master_copy = MASTER_DIR / f"{STEM}_master.mp3"
    master_copy.write_bytes(master_mp3.read_bytes())
    master_wav_copy = MASTER_DIR / f"{STEM}_master.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(master_wav), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(master_wav_copy),
        ],
        check=True,
    )

    time.sleep(2)
    after = sub_chars(token, mode)
    time.sleep(4)
    after_poll = sub_chars(token, mode)
    dur = probe_dur(master_wav)
    sha = hashlib.sha256(master_mp3.read_bytes()).hexdigest()
    loud = measure_loudness(master_mp3)
    delta = (after_poll["character_count"] or 0) - (before["character_count"] or 0)

    print(f"Scribe STT ({dur:.1f}s)…", flush=True)
    stt = run_scribe(token, mode, master_mp3, HERE / "stt")
    stt_words = [w for w in (stt.get("words") or []) if (w.get("type") or "word") == "word"]
    words_payload = {
        "file": str(master_mp3.relative_to(REPO)),
        "duration_s": stt.get("audio_duration_secs") or dur,
        "model": "elevenlabs_scribe_v2",
        "text": (stt.get("text") or "").strip(),
        "words": [{"text": w.get("text"), "start": w.get("start"), "end": w.get("end")} for w in stt_words],
    }
    (HERE / "words.json").write_text(json.dumps(words_payload, indent=2) + "\n")
    diff = script_diff(full_text, words_payload["text"])
    (HERE / "script_whisper_diff.json").write_text(json.dumps({
        k: diff[k] for k in ("script_words", "whisper_words", "match_rate_pct", "mismatches", "script_norm", "whisper_norm")
    }, indent=2) + "\n")

    credits = {
        "before": before,
        "after": after,
        "delta_characters": (after["character_count"] or 0) - (before["character_count"] or 0),
        "spoken_chars": len(full_text),
        "spoken_words": len(full_text.split()),
        "duration_s": round(dur, 3),
        "sha256": sha,
        "updated": now_bst(),
        "after_poll": {
            "character_count": after_poll["character_count"],
            "character_limit": after_poll["character_limit"],
            "polled": now_bst(),
        },
        "delta_characters_polled": delta,
        "chapter_gap_s": CHAPTER_GAP_S,
        "chapters": chapter_meta,
        "note": "subscription character_count may lag; after_poll is the recheck",
    }
    (HERE / "credits_before_after.json").write_text(json.dumps(credits, indent=2) + "\n")

    fails = []
    warns = []
    if loud["max_volume_db"] > -1.0:
        fails.append(f"peak {loud['max_volume_db']} above -1.0")
    if diff["match_rate_pct"] < 85:
        fails.append(f"Scribe match {diff['match_rate_pct']}%")
    status = "PASS" if not fails else "FAIL"
    if diff["match_rate_pct"] < 95:
        warns.append(f"Scribe match {diff['match_rate_pct']}%")

    vo_check = {
        "tool": "owb_long_vo_check_v01",
        "status": status,
        "fails": fails,
        "warns": warns,
        "duration_s": round(dur, 3),
        "lufs_integrated": loud["lufs_integrated"],
        "mean_volume_db": loud["mean_volume_db"],
        "max_volume_db": loud["max_volume_db"],
        "words": len(full_text.split()),
        "script_whisper_match_rate_pct": diff["match_rate_pct"],
        "chapter_gap_s": CHAPTER_GAP_S,
        "chapters": len(chapters),
        "sha256_mp3": sha,
        "updated": now_bst(),
    }
    (HERE / "vo_check.json").write_text(json.dumps(vo_check, indent=2) + "\n")
    (HERE / "vo_check.txt").write_text(
        f"""VO CHECK — Light-speed 024 long
Status: {status}
Duration: {dur:.2f}s ({dur/60:.2f} min)
Chapters: {len(chapters)} with {CHAPTER_GAP_S}s gaps
LUFS: {loud['lufs_integrated']} | mean {loud['mean_volume_db']} | peak {loud['max_volume_db']}
Scribe match: {diff['match_rate_pct']}%
Fails: {fails or 'none'}
Warns: {warns or 'none'}
"""
    )

    (HERE / "VO_STATUS.md").write_text(
        f"""# VO status — Light-speed 024 long (What Happens If You Travel Near the Speed of Light?)

| Field | Value |
|---|---|
| Status | {status} |
| Script | light_speed_script_master_v02.md (prose only; chapter cards skipped; pauses between chapters) |
| Claude lock | comment 5982343917 — Locked VO for 024 |
| Voice | Ben Orbit Narrator (`{VOICE_ID}`) |
| Model | `{MODEL_ID}` |
| Settings | {VOICE_SETTINGS} |
| Chapters | {len(chapters)} (gap {CHAPTER_GAP_S}s between cards) |
| Words | {len(full_text.split())} |
| Spoken chars | {len(full_text)} |
| Duration | {dur:.2f}s ({dur/60:.2f} min) |
| LUFS integrated | {loud['lufs_integrated']} |
| mean / peak | {loud['mean_volume_db']} / {loud['max_volume_db']} dB |
| Credits before | {before['character_count']} / {before['character_limit']} |
| Credits after | {after_poll['character_count']} / {after_poll['character_limit']} |
| Credits delta | {delta} (spoken_chars={len(full_text)}; counter may lag) |
| Scribe match | {diff['match_rate_pct']}% |
| SHA-256 mp3 | `{sha}` |
| MP3 | `{master_mp3}` |
| WAV | `{master_wav}` |
| Master | `{master_copy}` |
| iCloud UAT | `{ICLOUD}` |
| Updated | {now_bst()} |
"""
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    for name in (
        f"{STEM}.mp3", f"{STEM}.wav", "VO_STATUS.md", "credits_before_after.json",
        "script_whisper_diff.json", "vo_check.json", "vo_check.txt", "words.json",
        "chapters_index.json",
    ):
        src = HERE / name
        if src.exists():
            import shutil
            shutil.copy2(src, ICLOUD / name)
    import shutil
    shutil.copy2(master_wav, ICLOUD / f"{STEM}_LISTEN.wav")
    shutil.copy2(master_copy, ICLOUD / f"{STEM}_master.mp3")

    print(
        f"SAVED {status} {master_mp3} {dur:.2f}s lufs={loud['lufs_integrated']} "
        f"match={diff['match_rate_pct']}% credits {before['character_count']}->{after_poll['character_count']} "
        f"delta={delta} sha={sha[:12]}",
        flush=True,
    )


if __name__ == "__main__":
    main()
