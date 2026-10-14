**027's bed, take 2: a brief for the re-ordered film (SHOT_LIST_v02), after the ElevenLabs reset on Fri 30 Oct (Claude, 9 Oct).**

Take 1 (J0080) has three problems:
- It was arranged for the v01 order. Its peak (3:20–3:50) now falls in the calm slow-stop chapter, and its hush (4:28–6:30) lands in "Earth is already slowing".
- It sounds like other films' beds (reused 0.80–0.87).
- It measured about 52 BPM.

Keep it in 05_Music, unused.

**Why wait:** air-date order across both channels (AGENTS.md). HOS's voiceovers air first: 007 Shorts from 8 Nov, then 009 and 010. They need about 12k of the 18,653 left. 027 airs 22 Nov, so a take on 30–31 Oct is in good time.

Run `generate_music_bed.py --project earth-spin --length-ms 470000 --out-dir 02_Video-Projects/027_What-If-Earth-Stopped-Spinning/05_Music --generate --prompt "<below>"` (v02 runs about 444 s plus the end hold):

"Instrumental science documentary underscore for Orbit with Ben, Earth Stopped Spinning film, told with calm wonder, never a disaster movie. Opens light and curious for twenty seconds, then a taut, rising pulse for the sudden-stop thought experiment (about 0:25 to 1:35) that peaks and eases rather than crashes; then relaxed and airy for the everyday spin (1:35 to 3:00); spacious and slow for a planet that has stopped turning (3:00 to 4:10); gently ticking and curious for clocks and tides (4:10 to 6:00); warm and grounded to close on a held chord. Plucked strings, marimba and soft clockwork percussion carry the pulse; warm woodwinds on top; light piano only near the end. Pace: 76-88 BPM, a clear steady pulse under British narration. NOT orchestral string-pad beds, NOT Jupiter music, NOT Saturn ring chimes, NOT Moon Leaving lunar piano, NOT Sun golden strings, NOT the Mars robot's lonely felt piano and low strings, NOT the Nearest Star's glassy celesta and bells, NOT Venus slow heat drones, NOT Light Speed clock arpeggios. No vocals, no choir words, no EDM, no trailer hit, no disaster-movie booms."

**Rules:** the same as J0080 (one continuation only if it comes back short, never a loop). music_gate must PASS against every other film's bed. Post the contour, then lay it into 027's cut.
