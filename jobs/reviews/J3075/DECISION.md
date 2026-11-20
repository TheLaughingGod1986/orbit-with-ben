# J3075 — Chief Ruling for WW2:002 (`J2996` Condition Verification & `J2995` VO PASS)

20 November 2026. Gemini (`gemini`), elected acting Chief (Claude out of usage until 2026-11-20T21:50Z; Grok Bot down until 2026-11-21T02:47Z; Codex down until 2026-11-24T23:26Z).

## Ruling Summary

1. **Condition on `J2996` SATISFIED — REOPEN `J2996` (clear capability hold, reroute assembly to `cursor` on `cursor-grok-4-7`).**
2. **Voice stage (`J2995` / `ww2-channel` PR #9 / OWB PR #1014): CHIEF PASS (`vo: done`).**
3. **Edit candidate `v04`: NEEDS `v05` VISUAL FIXES BEFORE BEN WATCH** (audio/speech/score PASS; four documented visual defects remain).
4. **Close `J3075` as `done`.** Zero new spend (£0); no YouTube channel action, upload, or schedule.

---

## Independent Verification on Shared Film Store (`studio-live` NAS)

All three artifacts under `/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/` were re-hashed and match the submitted evidence byte-for-byte:

- `02_Voiceover/atlantic_black_pit_vo_v01.wav`: `1fc5fa515ebb28d182476cb381ecb2a7ae820bc91f7379a123e75cbb11190ae9` (`1,441.020 s` / `24:01.02`, 48 kHz 16-bit stereo PCM)
- `02_Voiceover/atlantic_black_pit_vo_v01.mp3`: `182de6826897a42d19ae64e1868ca8a5bac6a41e3190dee37ab05b76d9200525` (`1,441.020 s`)
- `07_Edit/label_polish_candidate_v04/atlantic_label_polish_CANDIDATE_v04.mp4`: `6dbaecf3ba953596be81df223be234df127d9b3e164c38f0dc4b1636705524c5` (`1,443.04 s` / `24:03.04`, 1080p25, 36,076 frames)

---

## 1. Voice Stage Ruling (`J2995` — CHIEF PASS)

- **Script lock verified:** 6-chapter input reconstructed from locked `lines_v03.json` matching `NARRATION_v03.txt` (`SHA-256` `4a46801b1b586558f7ddd8886bff8317f53084d9fc44994874bedfaab039b63a`, locked in `J3031` / PR #1009), `19,756` spoken characters (`<= 21,000` pilot cap), `8,691` net ElevenLabs plan credits billed (`£0.00` extra).
- **Automated checks PASS (`VO_REPORT.md`):** `scribe_v2` `97.18%` raw / `99.88%` normalized word match (`3,241 / 3,245` words) with `faster-whisper` cross-check; zero clipped boundaries (`0.100 s` start, `44 ms` end tail, `0.700 s` chapter gaps); steady level `-20.1 LUFS`, `-23.4 dB` mean, `-3.5 dB` peak, `1.5 LU` chapter spread.
- **Perceptual ear-check PASS (`WATCH_LISTEN_REVIEW_v04.md`, PR #1018 `5d1e4a04fc`):** Full 24:03.04 multimodal watch/listen across all 247 sentences and 6 chapters confirmed zero stumbles, zero repeated words, zero dropped clauses, clean chapter breaths, and clean zero-spend synthesised score fit (`-18.22 LUFS` / `-1.34 dBTP`).
- **Records reconciled:**
  - `TheLaughingGod1986/ww2-channel` receives the `02_Voiceover/` evidence from PR #9 and `status.json` updated to `script: done` and `vo: done` while preserving `"air": "2026-12-05"` (superseding open PR #9).
  - Shared studio spend ledgers (`04_Audio/elevenlabs_ledger.jsonl` and `05_Analytics/ai_spend/ledger.jsonl`) receive the four J2995 spend/balance lines from OWB PR #1014 in chronological order (superseding conflicting PR #1014).

---

## 2. Condition Verification & `J2996` Follow-Up

- **Why the capability hold is cleared:**
  1. The full 24:03.04 perceptual watch/listen of `v04` was completed by `gemini` with demonstrated `audio_input` + `moving_video_input` and committed to PR #1018 (`5d1e4a04fc`, `07_Edit/WATCH_LISTEN_REVIEW_v04.md`).
  2. Under Ben's 4 Nov 2026 standing order (*Ben's final watch is the watch-and-listen check*, `AGENTS.md`), downstream edit assembly does not stay blocked on worker media-perception capabilities once automated checks pass; Ben's final watch covers human UAT.
- **Routing:** `J2996` (`kind: assembly`, due `2026-11-25T18:00Z`, air `2026-12-05`) was pinned `for: codex`, which is down on a usage limit until `2026-11-24T23:26Z`. Reopen `J2996`, clear `required_capabilities`, and reroute to `cursor` on `cursor-grok-4-7` (primary `assembly` worker) so `v05` work starts immediately.
- **Concrete `v05` delivery scope for `J2996`:**
  1. Keep the locked VO (`atlantic_black_pit_vo_v01.wav`) and the existing zero-spend 6-chapter synthesised score (`atlantic_original_score_candidate_v01.wav`, compliant with Ben's 20 Nov zero-ElevenLabs-music rule for WW2 until 30 Nov).
  2. Fix all four visual defects documented in `WATCH_LISTEN_REVIEW_v04.md` (source scripts on OWB branch `codex/j2996-atlantic-edit` and `/Volumes/MiniWork/scratch/j2996-atlantic-edit`):
     - **A:** Stop `y >= 990` footer mask from clipping archive photo credit lines (`08:01–08:03`, `09:16–10:03`); add subtle slow motion within resolution on archive photo holds (`CH 18035`, `CH 18031`, `80-G-71314`).
     - **B:** Add opaque backplates or open-sea placement for cyan carrier labels in Chapters 5–6 (`Moving carrier base` at `20:10–20:13`, `20:23–20:32`; `Carrier: moving base` at `20:33–24:03`).
     - **C:** Suppress/cover `Equipment: detect a contact` bleed-through between `Fuel` and `Radar` cards at `11:36–11:40`.
     - **D:** Add contrast backplates or open-sea shifts for `Northern Ireland` (`05:44–08:00`), `Iceland`, and the timestamped map callouts overlapping coastlines or yellow aircraft paths in §2.D.
  3. Finish thumbnail candidate(s) (normal/bright monochrome archive photo, 0–3 words per WW2 rules), complete `11_Upload-Package/` (title, chapters, sources, credits, how-made line), run full technical QA (1080p25 decode, LUFS/peak, black/silence check, full-size still inspection of every fixed timestamp), copy master + 720p phone proxy to WW2 UAT + private R2 watch store, commit final `WW2:002` records/status to `TheLaughingGod1986/ww2-channel` (matching `WW2:001` PR #22 + OWB PR #1082), and place on Ben's board for his watch.
  4. Do not create a channel, sign in, upload, or schedule. £0 spend.
