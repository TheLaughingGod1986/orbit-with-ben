#!/usr/bin/env python3
import json, re, sys
from faster_whisper import WhisperModel

video, words_json, out = sys.argv[1:4]
norm = lambda s: re.sub(r"[^a-z0-9' ]+", " ", s.lower().replace("-", " ")).split()
ref = norm(" ".join(w["text"] for w in json.load(open(words_json))))
model = WhisperModel("small.en", device="cpu", compute_type="int8")
import subprocess, numpy as np
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     check=True, capture_output=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
segs, _ = model.transcribe(audio, language="en", beam_size=5, vad_filter=False)
segs = list(segs)
hyp = norm(" ".join(s.text for s in segs))

# word-level Levenshtein
n, m = len(ref), len(hyp)
prev = list(range(m + 1))
for i in range(1, n + 1):
    cur = [i] + [0] * m
    for j in range(1, m + 1):
        cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ref[i - 1] != hyp[j - 1]))
    prev = cur
wer = prev[m] / max(n, 1)
json.dump({
    "video": video, "model": "faster-whisper small.en (local, no credit)",
    "ref_words": n, "hyp_words": m, "edits": prev[m], "wer": round(wer, 4),
    "pass": wer <= 0.05,
    "segments": [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segs],
}, open(out, "w"), indent=1)
print(f"WER {wer:.2%} ({prev[m]} edits / {n} ref words) -> {'PASS' if wer <= 0.05 else 'FAIL'}")
