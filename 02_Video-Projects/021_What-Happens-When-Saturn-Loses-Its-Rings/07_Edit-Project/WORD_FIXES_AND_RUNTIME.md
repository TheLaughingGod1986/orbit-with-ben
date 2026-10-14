# Saturn first cut v03f — five re-records + trim

**Not KEEP** until Ben reviews. LOCK master untouched. PR #99 untouched.

| | |
|---|---|
| File | `saturn_first_cut_v03f.mp4` |
| Duration | **552.1 s** |
| sha256 | `2d2728c626699e5481a8b356393c5761b4749dad384b44dccc4c5727b1be1ad0` |
| LUFS | **-14.7** (LRA 3.6) |
| Shot list | `shot_list_v03j.csv` (end hold 15→8 s; no VO cut) |
| VO | LOCK + 5 EL retakes + leak/Next donors |

## Voice note
Channel LOCK VO is **ElevenLabs Ben Orbit Narrator** (`orbit_voice.py` / eleven_v3), not Vertex TTS.
Retakes use the same voice id + settings as LOCK so they match. Vertex remains the picture engine.

## Five Ben-flagged fixes (sentence-boundary splices)

| # | line | VO t | stem Whisper |
|--:|---|---|---|
| 1 | not a solid **disc** | 19.22–21.55 | solid disk/disc (full word — not “dic”) |
| 2 | around **a** world | 46.52–51.10 | a world |
| 3 | **Mimas** | 81.48–85.10 | Mimas |
| 4 | **late arrival** | 364.50–366.62 | late arrival |
| 5 | forever **disc** | 495.74–503.86 | forever disk/disc (full word) |

Whisper `medium.en` often spells the word **disk** (US). Gate: complete word, never Ben’s clipped “dic”.

## Also carried
- leak clarity splice · Next (was Net)

## Optional trim
End hold **15 s → 8 s** (−7 s). No VO touched. Runtime ~552 s vs v03d 559 s.

## Excerpts
See `excerpts/excerpt_01_solid_disc.mp4` … `excerpt_05_forever_disc.mp4`.
