#!/usr/bin/env python3
"""025 Mars Short VO pipeline — TTS (orbit_voice LOCK) → pause-trim → Scribe → check.

Usage:
  python3 _short_vo_pipeline_v01.py mon02_gps_relativity
  python3 _short_vo_pipeline_v01.py wed04_robot_light
  python3 _short_vo_pipeline_v01.py fri06_muons_ground
  python3 _short_vo_pipeline_v01.py all
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
TOOLS = REPO / "04_Audio" / "tools"
sys.path.insert(0, str(TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import multipart_post, request, slugify  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_SETTINGS  # noqa: E402

ICLOUD_UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
MAX_GAP_S = 0.4
SILENCE_THRESH = "-38dB"
TARGET_MAX_S = 25.0
MEAN_MIN, MEAN_MAX = -28.0, -19.0
PEAK_MAX = -1.0

META = {
    "mon09_opportunity_90_days": {
        "title": "Mon 9 (Opportunity 90 days / 14 years)",
        "script_ref": "MARS_SHORTS_SCRIPTS_v01.md §1 Mon 9 (prose only; brackets skipped)",
        "icloud": "025_Mars_Mon09_VO",
        "stem": "mon09_opportunity_90_days_vo_v01",
        "status_label": "Mars 025 Short",
    },
    "wed11_night_cold": {
        "title": "Wed 11 (Mars night cold)",
        "script_ref": "MARS_SHORTS_SCRIPTS_v01.md §2 Wed 11 (prose only; brackets skipped)",
        "icloud": "025_Mars_Wed11_VO",
        "stem": "wed11_night_cold_vo_v01",
        "status_label": "Mars 025 Short",
    },
    "fri13_ingenuity_72": {
        "title": "Fri 13 (Ingenuity 72 flights)",
        "script_ref": "MARS_SHORTS_SCRIPTS_v01.md §3 Fri 13 (prose only; brackets skipped)",
        "icloud": "025_Mars_Fri13_VO",
        "stem": "fri13_ingenuity_72_vo_v01",
        "status_label": "Mars 025 Short",
    },
}


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


def silencedetect(path: Path, thresh: str = SILENCE_THRESH, min_d: float = 0.15) -> list[tuple[float, float]]:
    """Return list of (silence_start, silence_end) from ffmpeg silencedetect."""
    proc = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
            "-af", f"silencedetect=n={thresh}:d={min_d}", "-f", "null", "-",
        ],
        capture_output=True, text=True, errors="replace",
    )
    err = proc.stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    # Pair starts with ends; if trailing start without end, use duration
    pairs: list[tuple[float, float]] = []
    dur = probe_dur(path)
    for i, s in enumerate(starts):
        if i < len(ends):
            pairs.append((s, ends[i]))
        else:
            pairs.append((s, dur))
    return pairs


def pause_trim(raw_wav: Path, out_dir: Path, max_gap: float = MAX_GAP_S) -> tuple[Path, dict]:
    """Cap inter-phrase silence to max_gap; keep speed. Write segments + trimmed wav."""
    raw_wav = raw_wav.resolve()
    out_dir = out_dir.resolve()
    work = out_dir / "_pause_trim"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    dur = probe_dur(raw_wav)
    silences = silencedetect(raw_wav)
    # Build timeline of speech/silence in raw coords
    segments: list[dict] = []
    cursor = 0.0
    for s0, s1 in silences:
        if s0 > cursor + 0.01:
            segments.append({"kind": "speech", "start": round(cursor, 3), "end": round(s0, 3)})
        gap = s1 - s0
        keep = min(gap, max_gap)
        segments.append({"kind": "sil", "start": round(s0, 3), "end": round(s0 + keep, 3)})
        # note: we skip (s0+keep)→s1 from output
        cursor = s1
    if cursor < dur - 0.01:
        segments.append({"kind": "speech", "start": round(cursor, 3), "end": round(dur, 3)})

    # Extract and concat
    parts: list[Path] = []
    for i, seg in enumerate(segments):
        # For sil segments, start/end already capped; for speech use raw start/end
        # But sil start is raw s0; we need actual extract from raw:
        if seg["kind"] == "speech":
            a, b = seg["start"], seg["end"]
        else:
            # sil: extract from raw silence start for keep duration
            a = seg["start"]
            b = seg["end"]
        length = b - a
        if length <= 0.001:
            continue
        part = work / f"seg_{i:02d}_{seg['kind']}.wav"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{a:.6f}", "-t", f"{length:.6f}", "-i", str(raw_wav),
                "-c:a", "pcm_s16le", str(part),
            ],
            check=True,
        )
        parts.append(part)

    # concat
    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    trimmed = work / "trimmed.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(trimmed),
        ],
        check=True,
        cwd=str(work),
    )
    tdur = probe_dur(trimmed)
    meta = {
        "raw_duration_s": round(dur, 3),
        "trimmed_duration_s": round(tdur, 3),
        "max_gap_s": max_gap,
        "threshold": SILENCE_THRESH,
        "speech_end_used": round(dur, 3),
        "segments": segments,
    }
    return trimmed, meta


def wav_to_mp3(wav: Path, mp3: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "128k", str(mp3),
        ],
        check=True,
    )


def measure_loudness(path: Path) -> dict:
    # volumedetect
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True, errors="replace",
    )
    err = proc.stderr
    mean = float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))
    peak = float(re.search(r"max_volume: (-?[\d.]+)", err).group(1))
    # ebur128 integrated
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


def silence_gt(path: Path, db: int = -45, min_s: float = 1.0) -> list[dict]:
    proc = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
            "-af", f"silencedetect=n={db}dB:d={min_s}", "-f", "null", "-",
        ],
        capture_output=True, text=True, errors="replace",
    )
    err = proc.stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    durs = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", err)]
    return [{"start": s, "duration": d} for s, d in zip(starts, durs) if d > 1.0]


def norm_words(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().replace("\u2019", "'").replace("'", "'")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    return [w for w in text.split() if w]


def script_scribe_diff(script: str, scribe_text: str) -> dict:
    sw = norm_words(script)
    ww = norm_words(scribe_text)
    sm = SequenceMatcher(None, sw, ww)
    mismatches = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        mismatches.append({
            "op": tag,
            "script": sw[i1:i2],
            "whisper": ww[j1:j2],
        })
    # Match rate: ratio of equal opcodes over max len
    equal = sum(i2 - i1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == "equal")
    denom = max(len(sw), 1)
    rate = round(100.0 * equal / denom, 2)
    # number-spelling-only heuristic
    num_only = True
    for m in mismatches:
        s = " ".join(m["script"])
        w = " ".join(m["whisper"])
        # digits vs spelled: allow if one side is mostly digits/number words
        if not (re.search(r"\d", w) or re.search(r"\d", s)):
            # also allow percent / degrees style
            if m["script"] or m["whisper"]:
                # if both sides pure alpha words that aren't number-related, not number-only
                numberish = set(
                    "zero one two three four five six seven eight nine ten eleven twelve "
                    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty "
                    "thirty forty fifty sixty seventy eighty ninety hundred thousand million "
                    "billion percent degrees".split()
                )
                if any(x not in numberish for x in m["script"] + m["whisper"]):
                    num_only = False
                    break
    return {
        "script_words": len(sw),
        "whisper_words": len(ww),
        "match_rate_pct": rate,
        "mismatches": mismatches,
        "script_norm": " ".join(sw),
        "whisper_norm": " ".join(ww),
        "mismatches_are_number_spelling_only": num_only if mismatches else True,
    }


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
    raw_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    text = (data.get("text") or "").strip()
    (stt_dir / f"{stem}_transcript.txt").write_text(text + "\n", encoding="utf-8")
    # Import SRT helper
    from transcribe_vo import words_to_srt  # local
    words = data.get("words") or []
    (stt_dir / f"{stem}.srt").write_text(words_to_srt(words), encoding="utf-8")
    meta = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "audio": str(audio),
        "model_id": "scribe_v2",
        "language_code": "eng",
        "status": "generated",
        "files": {
            "raw_json": raw_path.name,
            "transcript": f"{stem}_transcript.txt",
            "srt": f"{stem}.srt",
        },
        "duration_seconds": data.get("audio_duration_secs") or data.get("audio_duration_seconds"),
        "word_count": len([w for w in words if (w.get("type") or "word") == "word"]),
    }
    (stt_dir / f"{stem}_stt_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return data


def now_bst() -> str:
    return time.strftime("%Y-%m-%d %H:%M %Z")


def process(slug: str) -> dict:
    if slug not in META:
        raise SystemExit(f"unknown slug {slug}; choose from {list(META)}")
    info = META[slug]
    out = HERE / slug
    out.mkdir(parents=True, exist_ok=True)
    stem = info["stem"]
    txt = out / f"{stem}.txt"
    if not txt.exists():
        raise SystemExit(f"missing spoken text: {txt}")
    text = txt.read_text().strip()
    raw_mp3 = out / f"{stem}_raw.mp3"
    raw_wav = out / f"{stem}_raw.wav"
    final_mp3 = out / f"{stem}.mp3"
    final_wav = out / f"{stem}.wav"

    token, mode = load_token()
    before = sub_chars(token, mode)
    print(
        f"[{slug}] auth={mode} voice={VOICE_ID} model={MODEL_ID} "
        f"chars={len(text)} words={len(text.split())} "
        f"credits_before={before['character_count']}/{before['character_limit']}",
        flush=True,
    )
    speak(token, mode, text, raw_mp3)
    mp3_to_wav(raw_mp3, raw_wav)
    raw_dur = probe_dur(raw_wav)
    print(f"[{slug}] raw TTS {raw_dur:.2f}s", flush=True)

    # poll credits (subscription counter can lag)
    time.sleep(2)
    after = sub_chars(token, mode)
    time.sleep(3)
    after_poll = sub_chars(token, mode)
    delta = (after_poll["character_count"] or 0) - (before["character_count"] or 0)

    # pause trim if over target OR raw has silence >1s (gate would FAIL)
    sil_raw = silence_gt(raw_wav)
    did_trim = (raw_dur > TARGET_MAX_S) or bool(sil_raw)
    if did_trim:
        trimmed_wav, trim_meta = pause_trim(raw_wav, out, MAX_GAP_S)
        shutil.copy2(trimmed_wav, final_wav)
        wav_to_mp3(final_wav, final_mp3)
        (out / "pause_trim_meta.json").write_text(json.dumps(trim_meta, indent=2) + "\n")
        final_dur = trim_meta["trimmed_duration_s"]
        print(f"[{slug}] pause-trim {raw_dur:.2f}s → {final_dur:.2f}s (max_gap={MAX_GAP_S})", flush=True)
    else:
        shutil.copy2(raw_mp3, final_mp3)
        shutil.copy2(raw_wav, final_wav)
        trim_meta = {
            "raw_duration_s": round(raw_dur, 3),
            "trimmed_duration_s": round(raw_dur, 3),
            "max_gap_s": MAX_GAP_S,
            "threshold": SILENCE_THRESH,
            "note": "under 25s; no pause trim applied",
            "segments": [],
        }
        (out / "pause_trim_meta.json").write_text(json.dumps(trim_meta, indent=2) + "\n")
        final_dur = raw_dur
        print(f"[{slug}] under 25s — kept raw as final ({final_dur:.2f}s)", flush=True)

    sha = hashlib.sha256(final_mp3.read_bytes()).hexdigest()
    loud = measure_loudness(final_mp3)
    # Soft peak safety (one TTS take; post gain only if near-clip). Speed unchanged.
    if loud["max_volume_db"] > PEAK_MAX:
        peak_before = loud["max_volume_db"]
        gain = -1.5 - peak_before
        print(f"[{slug}] peak {peak_before} > {PEAK_MAX}; applying {gain:.2f} dB gain", flush=True)
        peak_safe = out / "_peak_safe.wav"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(final_wav), "-af", f"volume={gain}dB",
                "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(peak_safe),
            ],
            check=True,
        )
        shutil.copy2(peak_safe, final_wav)
        wav_to_mp3(final_wav, final_mp3)
        sha = hashlib.sha256(final_mp3.read_bytes()).hexdigest()
        loud = measure_loudness(final_mp3)
        (out / "peak_safe_meta.json").write_text(json.dumps({
            "applied_gain_db": round(gain, 3),
            "peak_before": peak_before,
            "peak_after": loud["max_volume_db"],
            "mean_after": loud["mean_volume_db"],
            "lufs_after": loud["lufs_integrated"],
            "note": "one TTS take; peak soft-limit only (speed unchanged)",
        }, indent=2) + "\n")
    sil_long = silence_gt(final_mp3)

    # Scribe STT
    print(f"[{slug}] Scribe STT…", flush=True)
    stt_data = run_scribe(token, mode, final_mp3, out / "stt")
    stt_words = [w for w in (stt_data.get("words") or []) if (w.get("type") or "word") == "word"]
    words_payload = {
        "file": str(final_mp3.relative_to(REPO)),
        "duration_s": stt_data.get("audio_duration_secs") or final_dur,
        "model": "elevenlabs_scribe_v2",
        "text": (stt_data.get("text") or "").strip(),
        "words": [{"text": w.get("text"), "start": w.get("start"), "end": w.get("end")} for w in stt_words],
    }
    (out / "words.json").write_text(json.dumps(words_payload, indent=2) + "\n")

    diff = script_scribe_diff(text, words_payload["text"])
    (out / "script_whisper_diff.json").write_text(
        json.dumps({k: diff[k] for k in (
            "script_words", "whisper_words", "match_rate_pct", "mismatches",
            "script_norm", "whisper_norm",
        )}, indent=2) + "\n"
    )

    # gates (HOS-style + Short pace warn)
    fails: list[str] = []
    warns: list[str] = []
    if loud["mean_volume_db"] < MEAN_MIN or loud["mean_volume_db"] > MEAN_MAX:
        fails.append(f"mean_volume {loud['mean_volume_db']} outside {MEAN_MIN}..{MEAN_MAX}")
    if loud["max_volume_db"] > PEAK_MAX:
        fails.append(f"peak {loud['max_volume_db']} above {PEAK_MAX} (clipped?)")
    if sil_long:
        fails.append(f"silence>1s: {sil_long}")
    wpm = len(text.split()) / (final_dur / 60.0) if final_dur else 0
    if wpm < 145:
        warns.append(f"pace {wpm:.1f} wpm under 145 (Short house target ~23-25s / ~132-143 wpm)")
    if not diff["mismatches_are_number_spelling_only"] and diff["match_rate_pct"] < 90:
        fails.append(f"script/Scribe match {diff['match_rate_pct']}% with non-number mismatches")
    elif diff["match_rate_pct"] < 85:
        fails.append(f"script/Scribe match {diff['match_rate_pct']}% too low")

    status = "PASS" if not fails else "FAIL"
    credits = {
        "before": before,
        "after": after,
        "delta_characters": (after["character_count"] or 0) - (before["character_count"] or 0),
        "spoken_chars": len(text),
        "spoken_words": len(text.split()),
        "duration_s": round(raw_dur, 3),
        "sha256": hashlib.sha256(raw_mp3.read_bytes()).hexdigest(),
        "updated": now_bst(),
        "after_poll": {
            "character_count": after_poll["character_count"],
            "character_limit": after_poll["character_limit"],
            "polled": now_bst(),
        },
        "delta_characters_polled": delta,
        "note": "subscription character_count may lag immediately after TTS; after_poll is the recheck",
    }
    (out / "credits_before_after.json").write_text(json.dumps(credits, indent=2) + "\n")

    vo_check = {
        "tool": "owb_short_vo_check_v01 (HOS vo_check gates; Scribe word check — faster-whisper broken on py3.14/av)",
        "status": status,
        "fails": fails,
        "warns": warns,
        "duration_s": round(final_dur, 3),
        "lufs_integrated": loud["lufs_integrated"],
        "mean_volume_db": loud["mean_volume_db"],
        "max_volume_db": loud["max_volume_db"],
        "wpm": round(wpm, 1),
        "words": len(text.split()),
        "silence_gt_1s": sil_long,
        "script_whisper_match_rate_pct": diff["match_rate_pct"],
        "script_whisper_mismatches": diff["mismatches"],
        "mismatches_are_number_spelling_only": diff["mismatches_are_number_spelling_only"],
        "raw_duration_s": round(raw_dur, 3),
        "pause_trim_max_gap_s": MAX_GAP_S if did_trim else None,
        "sha256_mp3": sha,
        "updated": now_bst(),
    }
    (out / "vo_check.json").write_text(json.dumps(vo_check, indent=2) + "\n")
    mismatch_note = ""
    if diff["mismatches"]:
        if diff["mismatches_are_number_spelling_only"]:
            mismatch_note = "mismatches = number spelling only"
        else:
            mismatch_note = "see script_whisper_diff.json"
    (out / "vo_check.txt").write_text(
        f"""VO CHECK — Light-speed 024 Short {info['title']}
Status: {status}
Duration: {final_dur:.3f}s (raw {raw_dur:.2f}s{' → pause-trim max_gap=0.4s' if did_trim else ''})
LUFS integrated: {loud['lufs_integrated']}
mean_volume: {loud['mean_volume_db']} dB | max_volume: {loud['max_volume_db']} dB
Pace: {wpm:.1f} wpm ({len(text.split())} words)
Script vs Scribe: {diff['match_rate_pct']}% match; {mismatch_note}
Fails: {'none' if not fails else fails}
Warns: {warns if warns else 'none'}
Notes: HOS vo_check.py crashed (faster-whisper/av metadata_errors on Py3.14). Used same loudness/silence gates + ElevenLabs Scribe word diff.
"""
    )

    icloud_dir = ICLOUD_UAT / info["icloud"]
    icloud_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        f"{stem}.mp3", f"{stem}.wav", f"{stem}_raw.mp3", f"{stem}_raw.wav",
        f"{stem}.txt", "VO_STATUS.md", "credits_before_after.json",
        "pause_trim_meta.json", "script_whisper_diff.json", "vo_check.json",
        "vo_check.txt", "words.json",
    ):
        src = out / name
        if src.exists():
            shutil.copy2(src, icloud_dir / name)
    # LISTEN copy of final wav
    shutil.copy2(final_wav, icloud_dir / f"{stem}_LISTEN.wav")

    # Write VO_STATUS after iCloud path known
    status_md = f"""# VO status — Light-speed 024 Short {info['title']}

| Field | Value |
|---|---|
| Status | {status} |
| Script | {info['script_ref']} |
| Claude lock | comment 5982343917 — Locked VO for 024 |
| Voice | Ben Orbit Narrator (`{VOICE_ID}`) |
| Model | `{MODEL_ID}` |
| Settings | {{stability:0.34, similarity_boost:0.78, style:0.42, speed:1.04, use_speaker_boost:true}} |
| Words | {len(text.split())} |
| Spoken chars | {len(text)} |
| Raw duration | {raw_dur:.2f}s |
| Final duration | {final_dur:.3f}s {'(pause-trim max gap 0.4s; speed kept 1.04)' if did_trim else '(no pause trim; under 25s; speed 1.04)'} |
| LUFS integrated | {loud['lufs_integrated']} |
| mean / peak | {loud['mean_volume_db']} / {loud['max_volume_db']} dB |
| Credits before | {before['character_count']} / {before['character_limit']} |
| Credits after | {after_poll['character_count']} / {after_poll['character_limit']} |
| Credits delta | {delta} (spoken_chars={len(text)}; subscription counter may lag/partial) |
| Scribe match | {diff['match_rate_pct']}% {'(number-spelling mismatches only)' if diff['mismatches_are_number_spelling_only'] and diff['mismatches'] else ''} |
| SHA-256 mp3 | `{sha}` |
| TXT | `{txt}` |
| MP3 (repo, gitignored) | `{final_mp3}` |
| WAV (repo, gitignored) | `{final_wav}` |
| iCloud UAT copies | `{icloud_dir}` |
| Updated | {now_bst()} |
"""
    (out / "VO_STATUS.md").write_text(status_md)
    shutil.copy2(out / "VO_STATUS.md", icloud_dir / "VO_STATUS.md")

    # Also write per-slug generator (mirror mon19) for audit
    gen = out / f"_generate_{slug}_vo_v01.py"
    if not gen.exists():
        gen.write_text(
            f'''#!/usr/bin/env python3
"""024 Light-speed Short {info['title']} VO — Ben Orbit Narrator LOCK (orbit_voice).
Delegates to ../_short_vo_pipeline_v01.py
"""
from pathlib import Path
import subprocess, sys
subprocess.check_call([sys.executable, str(Path(__file__).resolve().parents[1] / "_short_vo_pipeline_v01.py"), "{slug}"])
'''
        )
        gen.chmod(0o755)

    print(
        f"[{slug}] {status} final={final_dur:.2f}s lufs={loud['lufs_integrated']} "
        f"match={diff['match_rate_pct']}% credits {before['character_count']}->{after_poll['character_count']} "
        f"delta={delta} sha={sha[:12]} icloud={icloud_dir}",
        flush=True,
    )
    return {
        "slug": slug,
        "status": status,
        "final_dur": final_dur,
        "raw_dur": raw_dur,
        "lufs": loud["lufs_integrated"],
        "mean": loud["mean_volume_db"],
        "peak": loud["max_volume_db"],
        "match": diff["match_rate_pct"],
        "credits_before": before["character_count"],
        "credits_after": after_poll["character_count"],
        "delta": delta,
        "sha": sha,
        "repo_mp3": str(final_mp3),
        "repo_wav": str(final_wav),
        "icloud": str(icloud_dir),
        "fails": fails,
        "warns": warns,
        "words": len(text.split()),
        "spoken_chars": len(text),
        "wpm": round(wpm, 1),
        "did_trim": did_trim,
    }


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: _short_vo_pipeline_v01.py <mon02_gps_relativity|wed04_robot_light|fri06_muons_ground|all>")
    arg = sys.argv[1]
    slugs = list(META) if arg in ("both", "all") else [arg]
    results = [process(s) for s in slugs]
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
