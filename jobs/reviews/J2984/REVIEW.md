# J2984 review: HOS 008 Short C v07 (J2662, HOS PR #556)

- **Reviewer:** `claudecode` (Claude Code on the Mac mini, `claude-opus-5-5`). Not a producer of v07: `macbook`/`gemini` assembled it, `cursor` minted the plates.
- **Date:** 18 Nov 2026, about 10:20–10:45Z. £0, 0 credits. No upload, no schedule, no Studio change.
- **Verdict: KEEP.** One thing to look at in Ben's watch (S06 hammer, below). It is not a fix.

## What I could and could not check

I looked at still frames, ran tools on the audio and read the measurements. I did not watch the motion or listen to the audio. Under the 4 Nov order (AGENTS.md, "Ben's final watch"), Ben's UAT watch is the watch-and-listen check.

## Master

| Check | Brief | Measured here |
|---|---|---|
| SHA-256 (NAS) | `a3404a31…51c8f06a8` | match |
| Frames / fps / size | 530 / 24 / 936×1664 | 530 / 24 / 936×1664, 22.083 s |
| Loudness | -14.0 LUFS, -2.5 dBTP | -14.2 LUFS, -2.5 dBTP (ffmpeg loudnorm measure, one pass; inside the ±0.5 LU target), LRA 3.0 |
| Full decode | | `ffmpeg -f null` with no errors |
| VO stem `J2662_v07/vo.wav` | `50d65ab8…` | match |

## The 5 J2485 fixes

1. **"Franklin's" ends by 1.50 s: PASS.**
   - Forced alignment (`spoken.json`): 0.980–1.489 s.
   - My own faster-whisper `small` run on the muxed master: "That lightning rod was Franklin's idea." with "Franklin's" at 0.900–1.520 s.
   - Whisper's word edges are only good to about ±0.1 s, so I checked the VO stem directly in 10 ms windows. The "s" hiss is 1.44–1.49 s (zero crossings 46–93 per window, level falling to -47 dB) and voicing for "idea" starts at 1.50 s. So the word ends at about 1.49 s.
   - Sentence 1 is exactly the 6 words Chief approved.
   - Body VO starts at 2.08 s (ASR) and the last word "year" ends at 20.74 s (ASR), against 20.78 s aligned.
2. **Captions: PASS, with a small mismatch in the records.**
   - I re-ran the build's own grouping and clamp (`_build_short_c_v07.py`, `render_captions`) on `spoken.json`. It gives **10** body chunks, not the 9 that RESULT.md states. None is dropped.
   - Boundary gaps are 0.04–0.72 s, so no two captions are ever on screen together.
   - There are no 1–2 word orphans. One chunk has 3 words ("round the building,", 14.90–15.92 s), so RESULT.md's "4–7 words per chunk" is also not quite right.
   - The hook caption (0–2.022 s) ends before the first body caption (2.10 s).
   - Frames at the boundaries agree: at 14.80, 15.95 and 19.03 s, a frame falls in the gap and shows no caption.
   - The captions are legible on the soft panel at full resolution, for example at 5.6 s and 19.5 s.
3. **S07 offset 3.10 s: PASS.** In `cuts.json`, `06_rod_fitting_c1_t1.mp4` starts at 3.1, which skips the 1.8–2.9 s shovel morph in the source. Frames at 16.4–18.9 s show hands and rod with no morph.
4. **S06 offset 4.00 s: PASS for the fix as asked.** In `cuts.json`, `06_rod_fitting_t1.mp4` starts at 4.0, which skips the 2.8–3.7 s vanishing handle in the source.
   - **Look at in Ben's watch:** from frame 331 to 339 (13.79–14.13 s), he moves the hammer toward the ladder rail as he grips it. After about 14.13 s the hammer is no longer visible.
   - In the stills this reads as the hammer passing behind the rail and his hand. Stills cannot show whether it is hidden or disappears. It happens in under half a second, about 0.3 s into the shot.
5. **Crops: PASS.** From `cuts.json`:
   - S01 and `loop_tail` are `[600,0,405,720]`. The struck spire is centred, as the 0.0 s and 21.5 s frames show.
   - S02 is `[180,0,405,720]`. The gable, chimney and rod are in frame (2.06, 3.68 and 4.20 s).
   - S03–S08 are `[438,0,405,720]`.
   - Every shot is upscaled 2.31×, under the 2.35× limit.

## Other notes (none blocks)

- The overlay "20+ STRIKES A YEAR" (19.10–20.95 s) sits in its upper panel, clear of the body caption panel. The "+" is legible at full size.
- The promoted long title "Why Did Franklin Fly a Kite in a Storm?" (9–14 s) is very small, top left. That was in the plan and is not part of J2485.
- S07's picture (hands at the rod's foot) runs under "Some towers are struck" (17.82–19.02 s). This was in the plan and is not part of J2485.
- PR #556 is **closed and not merged**. Codex, as acting Chief, closed it on 18 Nov at 09:50Z after carrying its J2662 files to HOS main in #644 (`872916d2`). They are on main under `10_Shorts/J2662/`. So there is nothing left to merge.

## UAT staging

- Copied to `HOS UAT/008_Lightning-Franklin/10_Shorts/hos_008_short_C_v07.mp4`. Its SHA-256 matches the NAS master.
- Air date stays conditional. The HOS 008 long (planned Thu 19 Nov 18:00 London) must be public before Short C airs. Short C's earliest slot is Tue 1 Dec 11:30 London, otherwise the next locked Sat/Fri/Sun/Tue 11:30 slot. Wed 2 Dec is not a locked HOS Shorts day.
