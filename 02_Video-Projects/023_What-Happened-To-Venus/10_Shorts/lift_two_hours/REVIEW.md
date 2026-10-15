# J0232 — Venus opening Short, worker handoff

Review only. No upload, scheduling, credit spend or final approval. Proposed Short title: **Why Venus Melts Lead**. Chief decides the title and air slot.

## Cut and evidence

Persistent delivery folder: `/Users/benjaminoats/_desk/J0232-venus-short/`

- Cut: `venus_two_hours_v01.mp4` (26.533 s, 1080×1920, 30 fps CFR, H.264).
- Full contact sheet: `venus_two_hours_v01_frames.jpg`; opening sheet: `open_sheet.jpg`.
- Custom cover: `venus_two_hours_v01_cover.jpg`; crop preview: `cover_preview.jpg`.
- Separate pre-normalisation stems: `vo_stem.wav`, `sfx_stem.wav`, `bed_reference_stem.wav` (same mix gains; final mix receives shared loudnorm).
- Hashes: SHA256.txt. Media remains outside Git and outside purgeable render scratch.

Selected 023: its three planned Shorts have locked scripts and VO but no built export in this checkout. Older 001–007 indexes confirm several Shorts each despite archived media being absent locally. 023 has an approved, now scheduled master; 024 is also approved but later. Later films with no picture master cannot supply the requested finished-picture lift.

Source: locked iCloud UAT `023_Venus_full_rough_v05e.mp4`, full SHA-256 recorded in meta. Original VO 0–23.52 s, 65 words, ending on “hours.”; trim at 24.05 s in the pause, before the next sentence. Picture is the same master, reframed from a 608×1080 centre crop (1.78× upscale). No source picture generated or changed. One 10% opening push, fine grain, captions, exact long title at 9–14 s and at the end with `VBaYRPp85Sw`. Last four seconds return to the opening picture via a 0.5 s crossfade. Custom cover uses a different master frame (14 s), with centre-safe white/yellow text.

One animated depth scale at 16.9–19.1 s: NEARLY 1 KM / DEEP, under the recorded “nearly a kilometer deep.” It stays inside the 16:9 centre band, clear of hook and title windows. The only SFX are the synthesised house whoosh (0 s) and tick (16.95 s). Locked original VO plus the film’s own score; music lowered to gain 0.06 because the initial 0.134 reference failed the spoken-window bed rule. Continuous bed through the loop.

## Automated checks

```
PASS venus_two_hours_v01.mp4 dur=26.53s audio=-18.4dB motion=19.08
polish gate PASS: 0 of 6 rows failed, 1 to look at
SFX level PASS: VO -20.3 LUFS, SFX -46.0 LUFS, 1 hits
```

Final loudness measured -14.94 LUFS, -1.46 dBTP (input values in final_loudness.txt). Cover preview inspected in both crops; no clipped text or Orbit.

Chief review points: the opening gate warns “possible Orbit” at visor score 0.0013; the actual frame is orange Venus terrain and outlined hook text, with no robot. Polish warns at 21.5 s about edge density 0.0335 vs film p5 0.0338; inspect the radar terrain at full size. Source imagery is inherited from the approved long, including radar terrain; this is not a fresh picture approval. The spoken opening is the long’s seven-word comparison (“Venus is the planet most like Earth”), rather than a newly recorded danger claim; the hook caption supplies “VENUS MELTS LEAD.” Chief should judge that opening against the Short rules before any approval.

The 17 Nov date is a gate comparison date only, not an authorised slot. Re-run the opening gate against Chief’s actual air date before upload. Related video is a package instruction only; nothing has been set in Studio.

## Rebuild

From this worktree, make the free kit with `python3 scripts/sfx_kit.py make --out-dir /private/tmp/j0232-assets/kit_v01`, then run `_assemble_venus_two_hours_v01.py`. Inputs are the locked iCloud master, original local VO/score and tracked word timestamps. Paths are explicit in the builder. Rendering is finished: tmux `j0232-render-v4`, log `~/_desk/logs/j0232-render-v4.log`, done file `~/_desk/logs/j0232-render-v4.done` contains 0. Earlier render attempts are finished; no render remains running.

Next: Chief reviews the cut, flagged frame, hook and cover; selects title/slot or requests edits. Parked for Chief: Short PASS. Nothing needed from Ben.
