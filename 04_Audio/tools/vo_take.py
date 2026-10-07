#!/usr/bin/env python3
"""One ElevenLabs VO take, the house way. Use this instead of copying a `_generate_*.py` per take.

  # a long, straight from the script master (prose only; a 0.7 s gap at each CHAPTER CARD)
  python3 04_Audio/tools/vo_take.py --script 02_Video-Projects/027_…/01_Script/earth_spin_script_master_v01.md \
      --out 02_Video-Projects/027_…/02_Voiceover --stem earth_spin_vo_v01 --order 5996295788

  # a Short or a pickup line
  python3 04_Audio/tools/vo_take.py --text "Next week: what if Earth stopped spinning?" \
      --out 02_Video-Projects/026_…/02_Voiceover --stem 026_pickup_nextweek_v01 --order 5996295788

  add --dry-run to print the plan and character count and spend nothing.
  --rescore --out <dir> --stem <stem> re-measures an existing take's loudness and verdict (no API call).

It always:
- uses the locked voice from `orbit_voice.py` (Ben Orbit Narrator, eleven_v3, speed 1.04). There is no voice option.
- calls the API only (never the ElevenLabs website) and makes one take. It refuses if the stem already exists, unless
  you pass --retake with Claude's comment id.
- stops before spending if the take needs more than the credits left in the month (--floor, default 0). Ben, 7 Oct:
  the plan is paid monthly, use all of it; never go past it into overage or a top-up.
- runs Scribe and diffs the transcript against the script words.
- writes one `<stem>_TAKE.json` (take, loudness, Scribe diff, vo_check verdict and credits) next to the audio, plus
  `stt/<stem>/`. Audio stays out of git.
- appends one line to `04_Audio/elevenlabs_ledger.jsonl` with the characters this take spent, so the account
  counter's lag never hides spend.

Run it under the pool lock on the Mini: `desk-lock elevenlabs -- python3 04_Audio/tools/vo_take.py …`.
"""
from __future__ import annotations

import argparse, hashlib, json, re, subprocess, sys, time, unicodedata
from difflib import SequenceMatcher
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
LEDGER = TOOLS.parent / "elevenlabs_ledger.jsonl"
sys.path.insert(0, str(TOOLS))

from orbit_voice import MODEL_ID, VOICE_ID, VOICE_NAME, VOICE_SETTINGS  # noqa: E402


# ---------- pure helpers (tested in test_vo_take.py) ----------

def spoken_chapters(markdown: str) -> list[dict]:
    """Split a script master into spoken chapters. Keeps prose only: drops headings, [MARKER] lines and comments.
    A new chapter starts at each [CHAPTER CARD: …]; the text before the first card is the open. Paragraphs are
    joined with a blank line."""
    markdown = re.sub(r"<!--.*?-->", "", markdown, flags=re.S)
    chapters = [{"title": "open", "paras": [[]]}]
    for raw in markdown.splitlines():
        line = raw.strip()
        card = re.match(r"\[CHAPTER CARD:\s*(.+?)\]\s*$", line)
        if card:
            chapters.append({"title": card.group(1).strip(), "paras": [[]]})
        elif not line or line.startswith("#") or line.startswith("["):
            chapters[-1]["paras"].append([])  # markers and blanks end a paragraph
        else:
            chapters[-1]["paras"][-1].append(line)
    out = []
    for ch in chapters:
        text = "\n\n".join(" ".join(p) for p in ch["paras"] if p)
        if text:
            out.append({"title": ch["title"], "text": text})
    return out


def norm_words(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().replace("\u2019", "'")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    return [w for w in text.split() if w]


def script_diff(script: str, heard: str) -> dict:
    sw, ww = norm_words(script), norm_words(heard)
    ops = SequenceMatcher(None, sw, ww, autojunk=False).get_opcodes()
    equal = sum(i2 - i1 for tag, i1, i2, _, _ in ops if tag == "equal")
    return {
        "script_words": len(sw),
        "scribe_words": len(ww),
        "match_rate_pct": round(100.0 * equal / max(len(sw), 1), 2),
        "exact_match": sw == ww,
        "mismatches": [{"op": t, "script": sw[i1:i2], "scribe": ww[j1:j2]} for t, i1, i2, j1, j2 in ops if t != "equal"],
    }


def verdict(diff: dict, lufs: float | None) -> str:
    """PASS needs ≥95% word match and a non-silent file. Claude still reads the mismatches before Locked."""
    if lufs is None or lufs < -35:
        return "FAIL (silent or near-silent)"
    return "PASS" if diff["exact_match"] or diff["match_rate_pct"] >= 95 else "REVIEW"


def spend_check(remaining: int | None, chars: int, floor: int) -> str | None:
    if remaining is None:
        return None
    if remaining - chars < floor:
        return f"STOP: {remaining} left, this take needs {chars}, floor is {floor}"
    return None


# ---------- audio and API ----------

def ff(*args, **kw):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True, **kw)


def duration(path: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "default=noprint_wrappers=1:nokey=1", str(path)], text=True))


def parse_loudness(stderr: str) -> dict:
    """ebur128 prints a running "I: … LUFS" on every frame line (the first reads -70.0 at t=0.1 s); the integrated
    value is the LAST match, in the Summary block (bug fixed 5 Oct 2026, #106)."""
    def num(rx):
        m = re.findall(rx, stderr)
        return float(m[-1]) if m else None
    return {"lufs_integrated": num(r"I:\s+(-?[\d.]+)\s+LUFS"), "mean_volume_db": num(r"mean_volume: (-?[\d.]+)"),
            "max_volume_db": num(r"max_volume: (-?[\d.]+)")}


def loudness(path: Path) -> dict:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect,ebur128",
                          "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
    return parse_loudness(err)


def rescore(out: Path, stem: str) -> int:
    """Re-measure loudness and re-run the verdict on an existing take. No API call, no spend."""
    take_path, wav = out / f"{stem}_TAKE.json", out / f"{stem}.wav"
    if not take_path.exists() or not wav.exists():
        print(f"vo_take: need {take_path.name} and {wav.name} in {out}", file=sys.stderr)
        return 2
    take = json.loads(take_path.read_text())
    loud = loudness(wav)
    before = take.get("vo_check")
    take["loudness"] = loud
    take["vo_check"] = verdict(take["scribe"], loud["lufs_integrated"])
    take["rescored_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    take_path.write_text(json.dumps(take, indent=2, ensure_ascii=False) + "\n")
    print(f"rescored {stem}: {before} -> {take['vo_check']} (LUFS {loud['lufs_integrated']})")
    return 0


def credits(token, mode):
    from el_client import request
    code, body, _ = request("GET", "/v1/user/subscription", token, mode, accept="application/json", timeout=60)
    if code != 200:
        raise SystemExit(f"subscription check failed {code}")
    d = json.loads(body)
    used, limit = d.get("character_count"), d.get("character_limit")
    return {"used": used, "limit": limit, "remaining": None if used is None or limit is None else limit - used}


def speak(token, mode, text: str, dest: Path):
    from el_client import request
    code, body, _ = request("POST", f"/v1/text-to-speech/{VOICE_ID}", token, mode,
                            data={"text": text, "model_id": MODEL_ID, "voice_settings": VOICE_SETTINGS},
                            query="output_format=mp3_44100_128", accept="audio/mpeg", timeout=600)
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:300]!r}")
    dest.write_bytes(body)


def scribe(token, mode, audio: Path, stt_dir: Path) -> str:
    from el_client import multipart_post
    from transcribe_vo import words_to_srt
    code, body = multipart_post("/v1/speech-to-text", token, mode,
                                fields={"model_id": "scribe_v2", "language_code": "eng",
                                        "timestamps_granularity": "word", "diarize": "false"},
                                files=[("file", audio)], timeout=900)
    if code != 200:
        raise SystemExit(f"Scribe failed {code}: {body[:300]!r}")
    data = json.loads(body)
    stt_dir.mkdir(parents=True, exist_ok=True)
    (stt_dir / "stt_raw.json").write_text(json.dumps(data, indent=2) + "\n")
    (stt_dir / "words.srt").write_text(words_to_srt(data.get("words") or []))
    return (data.get("text") or "").strip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--script", type=Path, help="script master .md (prose only, chapters at CHAPTER CARD)")
    src.add_argument("--text")
    src.add_argument("--text-file", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--stem", required=True)
    ap.add_argument("--order", action="append", default=[], help="Claude comment id(s) that cleared this take")
    ap.add_argument("--gap", type=float, default=0.7, help="seconds of silence between chapters")
    ap.add_argument("--floor", type=int, default=0)
    ap.add_argument("--retake", metavar="CLAUDE_COMMENT_ID", help="allow replacing an existing stem")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--rescore", action="store_true", help="re-measure loudness + verdict of an existing --stem; no spend")
    a = ap.parse_args(argv)

    if a.rescore:
        return rescore(a.out, a.stem)
    if not (a.script or a.text is not None or a.text_file):
        ap.error("one of --script, --text or --text-file is required")
    if a.script:
        chapters = spoken_chapters(a.script.read_text())
    else:
        chapters = [{"title": "take", "text": (a.text if a.text is not None else a.text_file.read_text()).strip()}]
    full = "\n\n".join(c["text"] for c in chapters)
    chars = sum(len(c["text"]) for c in chapters)
    print(f"{VOICE_NAME} / {MODEL_ID} / speed {VOICE_SETTINGS['speed']}: {len(chapters)} chapter(s), "
          f"{chars} chars, {len(full.split())} words -> {a.out / a.stem}.wav")
    for c in chapters:
        print(f"  {c['title'][:40]:<40} {len(c['text']):>5} chars  {c['text'][:60]!r}")
    if not a.order:
        print("vo_take: give --order <Claude comment id> (the Locked: VO or PASS that cleared this take)", file=sys.stderr)
        return 2
    mp3, wav = a.out / f"{a.stem}.mp3", a.out / f"{a.stem}.wav"
    if (mp3.exists() or wav.exists()) and not a.retake:
        print(f"vo_take: {a.stem} already exists; one take only (pass --retake <Claude id> if cleared)", file=sys.stderr)
        return 2
    if a.dry_run:
        print("dry run: nothing spent")
        return 0

    from el_auth import load_token
    token, mode = load_token(prefer_api_key=True)
    before = credits(token, mode)
    stop = spend_check(before["remaining"], chars, a.floor)
    if stop:
        print(f"vo_take: {stop}", file=sys.stderr)
        return 3

    parts = a.out / "parts" / a.stem
    parts.mkdir(parents=True, exist_ok=True)
    gap = parts / "gap.wav"
    ff("-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(a.gap), "-c:a", "pcm_s16le", str(gap))
    pieces, meta = [], []
    for i, c in enumerate(chapters):
        cm, cw = parts / f"ch{i:02d}.mp3", parts / f"ch{i:02d}.wav"
        if not (cm.exists() and cm.stat().st_size > 10_000):  # an interrupted run reuses finished chapters
            speak(token, mode, c["text"], cm)
        ff("-i", str(cm), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(cw))
        meta.append({"title": c["title"], "chars": len(c["text"]), "duration_s": round(duration(cw), 3)})
        pieces += [cw] + ([gap] if i < len(chapters) - 1 else [])
    (parts / "concat.txt").write_text("".join(f"file '{p.name}'\n" for p in pieces))
    ff("-f", "concat", "-safe", "0", "-i", "concat.txt", "-c:a", "pcm_s16le", str(wav.resolve()), cwd=str(parts))
    ff("-i", str(wav), "-c:a", "libmp3lame", "-b:a", "128k", str(mp3))

    heard = scribe(token, mode, mp3, a.out / "stt" / a.stem)
    diff = script_diff(full, heard)
    loud = loudness(wav)
    time.sleep(4)
    after = credits(token, mode)
    take = {
        "stem": a.stem, "voice": VOICE_NAME, "voice_id": VOICE_ID, "model_id": MODEL_ID, "settings": VOICE_SETTINGS,
        "orders": a.order, "retake_of": a.retake, "chapters": meta, "gap_s": a.gap,
        "spoken_chars": chars, "words": len(full.split()), "duration_s": round(duration(wav), 3), "loudness": loud,
        "sha256_mp3": hashlib.sha256(mp3.read_bytes()).hexdigest(),
        "scribe": {"transcript": heard, **diff}, "vo_check": verdict(diff, loud["lufs_integrated"]),
        "credits": {"before": before, "after": after, "counter_delta": None if None in (before["used"], after["used"])
                    else after["used"] - before["used"]},
        "text": full, "made_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    (a.out / f"{a.stem}_TAKE.json").write_text(json.dumps(take, indent=2, ensure_ascii=False) + "\n")
    with LEDGER.open("a") as f:
        f.write(json.dumps({"at": take["made_at"], "stem": a.stem, "chars": chars, "orders": a.order,
                            "remaining_before": before["remaining"]}) + "\n")
    print(f"{take['vo_check']}: {a.stem} {take['duration_s']} s, LUFS {loud['lufs_integrated']}, "
          f"Scribe {diff['match_rate_pct']}% ({len(diff['mismatches'])} mismatch runs), {chars} chars spent")
    return 0 if take["vo_check"] != "FAIL (silent or near-silent)" else 1


if __name__ == "__main__":
    sys.exit(main())
