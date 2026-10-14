#!/usr/bin/env python3
"""026 long pickup line — 'Next week: what if Earth stopped spinning?'

One take, Ben Orbit Narrator / eleven_v3 / speed 1.04. API only.
Does NOT touch nearest_star_vo_v01 LOCK long.
Claude ask: OWB #99 5996295788; Chief claim 5996312767.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
TOOLS = REPO / "04_Audio" / "tools"
sys.path.insert(0, str(TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import multipart_post, request, slugify  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_NAME, VOICE_SETTINGS  # noqa: E402
from transcribe_vo import words_to_srt  # noqa: E402

TEXT = "Next week: what if Earth stopped spinning?"
STEM = "026_nearest_star_pickup_nextweek_v01"
STT_DIR = HERE / "stt" / "pickup_nextweek_v01"


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
    used = data.get("character_count")
    limit = data.get("character_limit")
    return {
        "character_count": used,
        "character_limit": limit,
        "remaining": (limit - used) if used is not None and limit is not None else None,
        "tier": data.get("tier"),
        "status": data.get("status"),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
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


def run_scribe(token: str, mode: str, audio: Path) -> dict:
    STT_DIR.mkdir(parents=True, exist_ok=True)
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
    (STT_DIR / f"{stem}_stt_raw.json").write_text(json.dumps(data, indent=2) + "\n")
    text = (data.get("text") or "").strip()
    (STT_DIR / f"{stem}_transcript.txt").write_text(text + "\n")
    words = data.get("words") or []
    (STT_DIR / f"{stem}.srt").write_text(words_to_srt(words))
    (STT_DIR / f"{stem}_stt_meta.json").write_text(
        json.dumps(
            {
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "audio": str(audio),
                "model_id": "scribe_v2",
                "word_count": len([w for w in words if (w.get("type") or "word") == "word"]),
            },
            indent=2,
        )
        + "\n"
    )
    return data


def norm_words(text: str) -> list[str]:
    import unicodedata

    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().replace("\u2019", "'")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    return [w for w in text.split() if w]


def script_diff(script: str, heard: str) -> dict:
    sw, ww = norm_words(script), norm_words(heard)
    sm = SequenceMatcher(None, sw, ww)
    mismatches = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        mismatches.append({"op": tag, "script": sw[i1:i2], "scribe": ww[j1:j2]})
    equal = sum(i2 - i1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == "equal")
    rate = round(100.0 * equal / max(len(sw), 1), 2)
    return {
        "script_words": len(sw),
        "scribe_words": len(ww),
        "match_rate_pct": rate,
        "exact_match": sw == ww,
        "mismatches": mismatches,
        "script_norm": " ".join(sw),
        "scribe_norm": " ".join(ww),
        "script_raw": script,
        "scribe_raw": heard,
    }


def main() -> None:
    # Refuse if LOCK long would be overwritten by our stem (sanity)
    for forbidden in (
        HERE / "nearest_star_vo_v01.wav",
        HERE / "nearest_star_vo_v01.mp3",
        HERE / "05_Master" / "nearest_star_vo_v01_master.wav",
        HERE / "05_Master" / "nearest_star_vo_v01_master.mp3",
    ):
        if not forbidden.exists():
            print(f"warn: LOCK long missing at {forbidden}", flush=True)

    mp3 = HERE / f"{STEM}.mp3"
    wav = HERE / f"{STEM}.wav"
    if mp3.exists() or wav.exists():
        raise SystemExit(f"pickup already exists: {mp3.exists()=} {wav.exists()=} — abort, no retake")

    token, mode = load_token(prefer_api_key=True)
    before = sub_chars(token, mode)
    print(
        f"auth={mode} voice={VOICE_NAME}/{VOICE_ID} model={MODEL_ID} "
        f"settings={VOICE_SETTINGS} chars={len(TEXT)} "
        f"credits_before={before['character_count']}/{before['character_limit']} "
        f"remaining={before['remaining']}",
        flush=True,
    )
    if before["remaining"] is not None and before["remaining"] < 50_000:
        raise SystemExit(f"STOP floor: remaining {before['remaining']} < 50000")

    speak(token, mode, TEXT, mp3)
    mp3_to_wav(mp3, wav)
    dur = probe_dur(wav)
    loud = measure_loudness(wav)
    sha = hashlib.sha256(mp3.read_bytes()).hexdigest()

    stt = run_scribe(token, mode, mp3)
    heard = (stt.get("text") or "").strip()
    diff = script_diff(TEXT, heard)

    time.sleep(4)
    after = sub_chars(token, mode)
    delta = None
    if before["character_count"] is not None and after["character_count"] is not None:
        delta = after["character_count"] - before["character_count"]

    take = {
        "stem": STEM,
        "text": TEXT,
        "voice_id": VOICE_ID,
        "voice_name": VOICE_NAME,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
        "mp3": str(mp3),
        "wav": str(wav),
        "duration_s": round(dur, 3),
        "bytes_mp3": mp3.stat().st_size,
        "bytes_wav": wav.stat().st_size,
        "sha256_mp3": sha,
        "loudness": loud,
        "credits_before": before,
        "credits_after": after,
        "credits_delta": delta,
        "spoken_chars": len(TEXT),
        "scribe": {
            "transcript": heard,
            "match_rate_pct": diff["match_rate_pct"],
            "exact_match": diff["exact_match"],
            "mismatches": diff["mismatches"],
            "script_norm": diff["script_norm"],
            "scribe_norm": diff["scribe_norm"],
        },
        "orders": ["5996295788", "5996312767"],
        "note": "Pickup only; LOCK long nearest_star_vo_v01 untouched. Edit butts this onto the end.",
        "updated": time.strftime("%Y-%m-%d %H:%M %Z"),
    }
    (HERE / f"{STEM}_TAKE.json").write_text(json.dumps(take, indent=2) + "\n")
    (HERE / f"{STEM}_scribe_diff.json").write_text(json.dumps(diff, indent=2) + "\n")
    (HERE / f"{STEM}_vo_check.json").write_text(
        json.dumps(
            {
                "status": "PASS" if diff["exact_match"] or diff["match_rate_pct"] >= 95 else "REVIEW",
                "duration_s": round(dur, 3),
                "lufs_integrated": loud["lufs_integrated"],
                "mean_volume_db": loud["mean_volume_db"],
                "max_volume_db": loud["max_volume_db"],
                "scribe_match_rate_pct": diff["match_rate_pct"],
                "exact_match": diff["exact_match"],
                "sha256_mp3": sha,
            },
            indent=2,
        )
        + "\n"
    )
    (HERE / f"{STEM}_vo_check.txt").write_text(
        f"""VO CHECK — 026 pickup nextweek v01
Text: {TEXT}
Duration: {dur:.2f}s
LUFS: {loud['lufs_integrated']} | mean {loud['mean_volume_db']} | peak {loud['max_volume_db']}
Scribe: {heard!r}
Exact match: {diff['exact_match']} ({diff['match_rate_pct']}%)
Mismatches: {diff['mismatches'] or 'none'}
Credits: {before['character_count']} -> {after['character_count']} (delta={delta}, spoken={len(TEXT)})
SHA-256 mp3: {sha}
"""
    )
    (HERE / f"{STEM}_NOTE.md").write_text(
        f"""# 026 pickup — Next week line (v01)

| Field | Value |
|---|---|
| Text | `{TEXT}` |
| Voice | {VOICE_NAME} (`{VOICE_ID}`) |
| Model | `{MODEL_ID}` |
| Settings | {VOICE_SETTINGS} |
| Duration | {dur:.2f}s |
| LUFS | {loud['lufs_integrated']} |
| mean / peak | {loud['mean_volume_db']} / {loud['max_volume_db']} dB |
| WAV | `{wav}` |
| MP3 | `{mp3}` |
| Scribe transcript | {heard!r} |
| Exact match | {diff['exact_match']} ({diff['match_rate_pct']}%) |
| Credits before | {before['character_count']} / {before['character_limit']} (remaining {before['remaining']}) |
| Credits after | {after['character_count']} / {after['character_limit']} (remaining {after['remaining']}) |
| Credits delta | {delta} (spoken_chars={len(TEXT)}; counter may lag) |
| SHA-256 mp3 | `{sha}` |
| Claude ask | #99 5996295788 |
| Chief claim | 5996312767 |
| Updated | {time.strftime("%Y-%m-%d %H:%M %Z")} |

LOCK long `nearest_star_vo_v01` untouched. Edit butts this pickup onto the end after "And we have only just begun to measure the gap."
"""
    )
    print(
        f"SAVED {wav.name} {dur:.2f}s lufs={loud['lufs_integrated']} "
        f"exact={diff['exact_match']} match={diff['match_rate_pct']}% "
        f"scribe={heard!r} credits {before['character_count']}->{after['character_count']} "
        f"delta={delta} sha={sha[:12]}",
        flush=True,
    )


if __name__ == "__main__":
    main()
