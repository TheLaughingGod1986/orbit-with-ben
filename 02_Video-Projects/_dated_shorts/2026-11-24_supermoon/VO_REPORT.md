# Supermoon dated Short: voice-over report (J2478, 10 Nov 2026)

Voice credit cap for this job (two takes, about 600 characters) is **used up: 536 characters**. No further take without a new OK.

| Take | Text | Characters | Result |
|---|---|---:|---|
| `supermoon_vo_v01` | Full 46-word script | 291 | Recorded. 23.36 s, -20.9 LUFS, peak -4.8 dBFS. Every word heard as written (Scribe differs only in how it writes numbers). |
| `supermoon_vo_v02` | Trim 1 (41 words, "Normally thirty Earths fit between us.") | 245 | **Audio lost.** The API returned the audio, but the take's `parts/` folder had gone from the scratch worktree by then and the file write failed. Credits were charged; logged by hand in `ai_spend.py`. |

## Take 1 against the bar (Scribe word starts, s)
- Line 1 0.08; "swings" 0.86; "two" 1.36; "Earths" 1.60; "closer" 2.10; "November" 2.96
- Line 2 5.34; Line 3 9.54; Line 4 15.50; Line 5 21.10; last word ends about 23.2
- Over the bar as recorded: VO + 1.0 s tail = 24.4 s (bar 20.0 s); Line 4 starts 15.50 s (bar 13.5 s).
- Sentence gaps are about 1.0 s each, so tightening saves roughly 2.5 s: still over.
- First-second gate risk: "two Earths closer" finishes after 1.5 s (about 2.5 s). Not yet run through `gate_shorts_open.py`.

## What is left, at no cost
Trim 1 needs words that were never recorded ("between us"), so it can't be spliced from take 1.
Trim 2 (drop Line 2, the nickel line) can be: cut 4.3 to 9.5 s at room tone and tighten the other gaps. Estimate: VO about 16.5 s, cut about 17.5 s, Line 4 at about 9.5 s. This skips Trim 1 in the plan's order, so the reviewer should confirm it.

Audio (not in git): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-11-24_supermoon/02_Voiceover/` (take 1 WAV sha256 in `supermoon_vo_v01_TAKE.json` for the MP3).
