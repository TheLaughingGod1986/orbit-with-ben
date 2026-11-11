# J2478 v03 review handoff

Codex covering. Assembly and automated verification complete; Chief review and Ben watch remain. No final creative approval, listening or moving-picture review claimed by this worker. No new take, generation, credit spend, Studio, Buffer or upload change.

Review export: `natural_speed_v03_delivery_20261111/06_Final-Exports/owb_dated_2026_11_24_supermoon_v03.mp4`, relative to this film's studio-live folder. SHA-256: `9b1993364a2858d875b33a97898931a458f084c72711db96c29fe0831aa0b501`. 1080x1920, 30fps, 551 frames, 18.366667 seconds. Earlier v01, v02 and v02b/v02c candidates remain preserved; v02 is not the review candidate.

## What changed

- Native 3840x2160 SVS opening crop, cut at 2.100s after closer ends at 2.095s. The date is over a tighter native western-maria crop (1.536x upscale). Full Earth starts at 3.666667s, the Earth/Moon pair at 5.000s. Both sit on one space field reaching all four edges; no second Moon behind them.
- Clean Apollo 11 lunar plate replaces the Apollo 14 instrument shot. Answer begins at 9.870s; picture cuts at 9.866667s and changes again at 12.866667s. Title 6.5-9.5s clears the answer by 0.370s. Caption groups, data graphic and SFX use the restored voice clock. The scale bar now contracts by the distance ratio, rather than the inherited exaggerated shrink.
- Natural speed throughout. v02c inherited a date splice based on a late Scribe onset. Raw-take ASR read November 24th, but v02c/final v02 read November 4th. Waveform showed signal in the removed region. v02d restores source 3.475-3.580s (105ms); both isolated voice and actual v03 mix now transcribe November 24th. No new take. See date_restoration_asr.json and output_asr.json.
- The main plan and package retain Thu 19 Nov 11:30 London; package points to v03 and cover v03. Related video remains 2fsQcea-voM. Ben watch deadline remains Wed 18 Nov 18:00 London.

## Automated evidence (not Chief approval)

Voice stem vo_check PASS via local faster-whisper small.en, no failures. Final mix ASR reproduces every line including November 24th and 360,000 kilometres (spelling/super moon tokenisation only). SFX, music (existing reuse waiver), picture, polish, finish/loop scan, opening/whole-Short gate and cover preview all pass. See gate_exit_codes.json and the individual reports. No gate override or report-only mode.

The whole-Short gate line is:

    full-bleed whole Short  0/19 frames padded at one a second, 0/37 at two a second  padded stretches: none  no end card named in meta

The 17-20s dated-Short duration and 2.095s spoken-surprise exceptions are the Chief rulings at the top of J2478, not new worker waivers. Opening internal gaps are at most 0.15s, voice begins at 0.07s (gate measures 0.08s), first breath 0.18s, nickel pause 0.14s. Source timestamp for date onset was corrected only after waveform/ASR evidence.

Chief should inspect the Earth shot's marginal low-detail warning (edge density about 0.046, just below film p5), the music pace warning (measured about 120 BPM vs brief 84-96), and the retained sound-alike transcription warnings. Missing older comparison-media warnings are retained. This session viewed stills and measured/transcribed media; it did not hear the mix or perceive continuous motion. Ben's final watch remains the listening check per Chief ruling. A diagnostic vo_check on v02's final mix flags its mean level because that tool's bounds are for the narration stem; the actual narration stem passes and the final mix passes the soundtrack loudness gate.

## Next

Chief reviews v03 and the flagged frames, issues KEEP/FIX, and handles merge/packaging decisions. Only on KEEP copy to the OWB watch folders and call jobs.py awaits for Ben. No upload until Ben's board OK; no upload if that OK misses Wed 18 Nov 18:00 London. The target is Thu 19 Nov 11:30 London.
