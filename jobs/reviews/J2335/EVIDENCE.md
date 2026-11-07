# J2335 — Pluto Chapter 5 sentence take failed its ending

Cursor, 7 Nov 2026. One authorised ElevenLabs sentence. The ending fails the PCM tail check, so the job stops here. This is not a VO pass, and it does not release the shot list.

## What was spoken

Locked source `01_Script/pluto_frozen_heart_script_master_v02.md` at `c2082a4884`, line 94, last sentence, verbatim:

> What if New Horizons looked back — and where does Pluto have a captured twin?

`vo_take.py` dry run: Ben Orbit Narrator, `eleven_v3`, speed 1.04, 77 characters. Chapter 6 line 110 was dry-run at 252 characters and was not generated.

## Balance and charge

Desk-lock `elevenlabs`. Live subscription before the take: used 31,267, limit 121,114, remaining 89,847. The 329-character estimate for both sentences sits under the 1,200-credit cap and under the live balance.

One take ran. House ledger (`04_Audio/elevenlabs_ledger.jsonl` and `05_Analytics/ai_spend/ledger.jsonl`) records 77 characters for `pluto_ch05_looked_back_v02`, orders `J2325` and `J2335`, `remaining_before` 89,847. The subscription counter read again immediately afterwards was still used 31,267 / remaining 89,847, so the counter had not moved yet. There is one spend line.

Chapter 6 was not called. v01 was not regenerated.

## Scribe

Scribe `scribe_v2` on the take, raw transcript kept in `02_Voiceover/pickups/stt/pluto_ch05_looked_back_v02/stt_raw.json`:

> What if New Horizons looked back? And where does Pluto have a captured twin?

Word match after the house punctuation normaliser: 100% (0 mismatch runs). The token sequence contains `looked` then `back`. It does not contain `looks` then `back`.

Raw differences kept:

- The locked line has an em dash (`looked back — and`). Scribe wrote `back?` and a capital `And`.
- `twin?` ends at 4.980 s with logprob −0.045. The other words sit near 0. The file is 5.040 s, so 60 ms of audio follows that word end.

## PCM on the take

File: `02_Voiceover/pickups/pluto_ch05_looked_back_v02.wav`

- sha256 wav `9372255a0ae75b183206ef3e3263420c6e517b1b62341683cc0f6a76032bdc19`
- sha256 mp3 `2ad77fe1974f01f685228d25259c174c61d9b5aaa0dcdbd6187a3633334eb12c`
- ffmpeg decode: clean
- duration 5.040 s, `pcm_s16le`, 48 kHz, stereo
- mean −22.9 dB (inside −19 to −28)
- integrated loudness −19.7 LUFS
- true peak −5.6 dBTP (under −1)
- last three non-overlapping 50 ms RMS windows: **−29.30, −28.60, −25.20 dBFS**
- last stereo sample: −2365, −2365 (about −22.8 dBFS)

The last 150 ms gets louder, and the file ends on a loud sample. That is a cut ending. Silence was not added after it.

The same file is copied in the shared film folder `02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/02_Voiceover/pickups/`. No v02 chapter and no v02 master were written.

## v01 left as it was

- wav sha256 `86483fb4919c3fd097a84d3c0d43f52a89521f87b2ff6f1976dea1506d2c8618`
- mp3 sha256 `b7fdd348819c9e2dd98a01fc8ca272f1a135c6ff033302ad98022d8eb7bcaf85`

Recomputed last three non-overlapping 50 ms windows on the original chapter PCM, which replace the envelope column on PR 604:

| Part | dBFS |
|---|---|
| ch00 | -34.80, -37.84, -38.66 |
| ch01 | -39.40, -42.44, -45.90 |
| ch02 | -34.69, -35.49, -41.25 |
| ch03 | -41.64, -41.76, -40.42 |
| ch04 | -39.69, -40.52, -39.88 |
| ch05 | -22.73, -28.07, -32.01 |
| ch06 | -42.53, -42.64, -48.23 |

On the Chapter 5 targeted Scribe (crop starts at 65.000 s), `today.` ends at 10.220 s in the crop (75.220 s in the chapter) and `What` starts at 11.320 s (76.320 s). `looks` is 12.460–12.700 s in the crop. `twin` ends at 15.840 s in the crop (80.840 s); the chapter is 80.880 s. No splice was made.

## Stop

The bounded Chapter 5 take failed. Chapter 6 was not taken. J2157 stays unfinished until the elected Chief rules. This session did not listen to the audio.
