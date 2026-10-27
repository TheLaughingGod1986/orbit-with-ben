# J0989 — audio-only v13a build, 27 October 2026

Original v13 SHA256: `2b276eb295dffbf4df0e81d874bce98295cfc8a3b94b4e6da945b162b5898abd`.
Candidate v13a SHA256: `898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3`.

Video stream copied; all 565 decoded frame hashes and timestamps equal. Video is H.264 High, 1080×1920, 30 fps, yuv420p. Container and video duration remain 18.833333 s; audio stream duration remains 18.820000 s, AAC stereo 48 kHz. Original v13, older masters and original stems preserved.

Two-pass loudnorm targets -14 LUFS / -2.3 dBTP, with timestamps rebuilt from sample count after resampling and the original audio-stream length preserved. First two candidates are retained only as scratch in /private/tmp/j0989-evidence; neither is the delivery. See audio_filter_final.txt for exact filter. Final encoded AAC measurements:

```
Summary:

  Integrated loudness:
    I:         -14.4 LUFS
    Threshold: -24.8 LUFS

  Loudness range:
    LRA:         2.2 LU
    Threshold: -34.6 LUFS
    LRA low:   -15.6 LUFS
    LRA high:  -13.3 LUFS

  True peak:
    Peak:       -2.3 dBFS
[out#0/null @ 0xc7cc30300] video:234KiB audio:3529KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown
frame=  565 fps=0.0 q=-0.0 Lsize=N/A time=00:00:18.83 bitrate=N/A speed=  23x elapsed=0:00:00.81
```

Strict Shorts gate (air date 2026-10-28), picture QA, polish, music, SFX, finish_scan and loop checks all exit 0. The 18.83 s duration warning is covered by the job's explicit already-approved exception; no padding to 22 s. Picture warnings describe identical approved v13 frames; no new visual approval is asserted. Music pace and unreadable comparison-file warnings remain recorded. Music check uses 030's own copied bed and plan; running it against the standalone audit folder falsely compared the bed to this same film's own copy. No gate code or waiver changed.

Alignment: all six speech windows at 0/3/6/9/12/15 s have zero measured lag (8-sample resolution), correlation 0.988–0.995. Small.en local ASR recognises the whole sentence, including 340, 36,000 and 32,000 (asr_full.txt). ASR is a machine intelligibility check, not an aural listening check. I have no audio-listening input available in this session, so cannot certify no perceptible pumping or speech artefacts. That required check remains OPEN; do not treat this build as complete or upload-approved.

Original separated stems are copied byte-for-byte to v13a_stems; SFX level gate passes (VO -20.3, SFX -38.6 LUFS), bed coverage is unchanged and the common final mix processing preserves its source timing. These are source-stem level checks, not a separately processed-stem reconstruction of the nonlinear final mix.

Archive check: j0974-archive.done = 0; log records an intermediate AssertionError as well as verified v11 moves. No archive restarted; v12/v13 scratch untouched.

No spend, upload, scheduling, privacy, title or Buffer changes. Ben's content OK applies to v13; dependent Chief review must decide on this derivative's exact hash after the outstanding aural check.
