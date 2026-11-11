# J2478 natural-speed checkpoint

Codex covering. Incomplete; step 1 of the existing 4-step plan. Chief ruling at the top of J2478 is implemented in isolated voice candidate v02c. No new take or credit spend, no picture render or approval.

## Evidence

- Raw source SHA-256 checked: 95a24bc9c4b1352f333c121e96d88483afd7688229e037ba9a51958feeb9f385.
- Output WAV SHA-256: 894345b024af235f786eb84949f2119aa4362f513566060c15bc36108f677b64.
- Output 17.255 seconds, 48kHz stereo; with the existing one-second loop tail: 18.255 seconds.
- Mapped source alignment: first word 0.070s, Moon 0.175s, closer ends 2.095s, date ends 3.385s, If starts 3.565s, nickel-to-the gap 0.140s, answer starts 9.765s.
- Opening internal gaps 0.040–0.045s; first sentence breath 0.180s. All timing assertions ran.
- All 37 Scribe tokens remain covered; direct PCM comparison confirms word spans unchanged at natural speed, excluding the last 20ms of as under the inherited loop fade. No tempo filter, resampling or rate change.
- ffmpeg decode completed; integrated -21.3 LUFS, mean -23.9dB, peak -5.1dB. This is a voice stem, not the final mix.
- Python compile and diff check succeed. No output ASR/vo_check, listening review or finished-film gate claimed.
- Five files copied to NAS and SHA-256 checked: natural_speed_v02c_codex_20261111 under the film folder. Includes audio, script, edit map, words and picture-timing recipe. Old v01/v02b retained.

## Resume

Worktree /Volumes/MiniWork/scratch/J2478-natural-speed, branch codex/J2478-natural-speed. Use orbit-code-graphics venv for splice_v02c.py. Raw input symlink resolves to the preserved Gemini worktree; do not remove it. Runtime v02c WAV is ignored by git and stored on NAS.

NATURAL_SPEED_TIMELINE_v02c.json is a recipe, not rendered picture. Title 6.5–9.5s clears answer by 0.265s. Build into separate v02 export/work/graphics directories; do not overwrite v01. The old assemble_j2478.py still builds v01 and must be adapted before running: replace hardcoded frame boundaries, voice/word paths, captions, SFX delays, title/data windows, sidecars and gate references together. Decode SVS at native 3840x2160 BEFORE cropping; old decoder downscales first. Opening Moon and date punch-in must be full bleed. Earth and pair shots need seamless space to all edges with full real-body discs. Replace the Apollo 14 instrument shot with a clean source, per J2556. Keep the answer picture changing within four seconds. Round cut times to 30fps and explicitly handle total frame/audio duration.

Remaining: independent output ASR/vo_check, picture rebuild, every original Shorts/picture/music/SFX/loop/first-second check with Chief waiver documented, full-Short padding gate without report-only, NAS delivery, review job. No review job queued for unfinished picture. Final watch remains Ben; no hold based solely on absent listening capability. No Studio, upload or Buffer change.

The complete remaining rebuild and gates exceed a further 20-minute bounded run; released at this verified checkpoint. No render process launched.

Startup repair: today's default rescue branch already existed, so preservation used rescue/mini-2026-11-11-orbit-with-ben-1185238a0b. Local relay commit hash matched that remote before resetting the clean shared checkout. About 24GB free. HOS untouched apart from required pull/read.

Thread read to #6789507234.
