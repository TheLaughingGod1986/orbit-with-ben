# J0889 — 028 Gliese 710 release package v01

**Worker draft for Chief. No final OK, PASS, merge, upload or scheduling decision made.**

Proposed title: **Why Will Gliese 710 Brighten Our Night Sky?**

Primary A: **STAR VISITOR**. Test alternatives B: **COMET NUDGE**; C: **SUN’S NEIGHBOUR**. Three distinct editorial illustrations; none represents true relative distance/size or a photographed encounter. A has an Earth context cue; B shows the gravity/comet consequence; C includes the Sun and an illustrative probe. Chief should judge whether those illustrative cues communicate the distant flyby clearly enough. B’s wording deliberately says nudge, not creation of comets.

## Evidence

- Approved master unchanged: NAS `youtube-staging/028/028_Gliese710_full_master_v03.mp4`, SHA-256 `a9780e548a2775f4e7a1acecb6ac24308927f0b58ab1d606e67d27741e3db824`, 497.833 seconds, 1920×1080, 30 fps. Hash read back this run.
- `YOUTUBE_DRY_RUN.txt`: `ok: true`, `dryRun: true`, published false, scheduled false, private, not made for kids, synthetic disclosure true. The dry-run's `primary_thumbnail: api_done` is simulated; **no thumbnail was actually set**.
- `VALIDATION.json`: all mechanical checks true, including all caption words preserved after documented en-GB spelling and the 10,000–13,000 transcription correction. 126 cues; last spoken word 469.340 s. Captions need their separate Studio upload; the package loader ignores `captionsFile`.
- Five-source description follows chapters → Sources → image credits → honest production line. Sources are the quote-backed rows already in `01_Script/SOURCES.md`; no new scientific findings claimed. Eight subject tags, social hook/question/alt and pinned-comment draft included.
- Seven chapter starts come from v03's cut list: 0:00, 0:42, 2:06, 3:29, 4:41, 5:35, 6:17. No new VO.
- `THUMB_SCORE.txt`: tool PASS on A/B/C. Saturation 224.3 / 226.0 / 226.0; near-black 24% / 29% / 28%. Phone-size sheet (`thumb_preview_v01.jpg`), full-size sheet (`THUMBNAILS_FULL_SIZE.jpg`) and 360×202 style sheet against all 7 live OWB long primaries (`style_sheet_v01.jpg`) included. Worker visual check: lettering readable, yellow hook, whole hero stars (variant C top-pad adjusted to 26 px with no paste seam), clear top band, no Orbit or duration-badge overlap. Arial Black cap heights 79–80 px on 720 (~11%). This is advice, not Chief's visual PASS.
- `episode_gate_v01.txt`: `npm run gate:episode` PASS (script score 91/100).
- The OWB family sheet (`owb_family_sheet_v01.jpg`) compares preceding 027 primary with all three new covers (`thumb_preview.py`), and `style_sheet_v01.jpg` renders all three new covers (red-framed) alongside the 7 live OWB long primaries (021–027) at 360×202.
- Trailer v01: 45.3 seconds, vertical 608×1080, retains the approved 16:9 picture over a blurred moving background, first sentence group ends at 41.86 s, audio switches from master to its own existing score at 42.32 s. End CTA: Full film / on YouTube. Measured **−14.35 LUFS / −1.28 dBTP**. End-frame sheet included; Chief should watch it before release.

## Brief mismatches requiring Chief acceptance

1. OWB has **no `npm run lint:package` and no `style_sheet.py`**; those are HOS tools. They were not run or claimed to PASS. OWB package dry-run, direct mechanical validation and OWB family/phone sheets are supplied instead. Do not import HOS rules into this package.
2. Art used built-in image_gen on the ChatGPT plan under the standing AGENTS.md thumbnail permission, **not Nano Banana**. No Flow/Vertex/ElevenLabs API call, top-up, paid API or new music/VO. Final typography is code-built; prompt set and route are in `PROMPTS.md`.
3. The master watch is recorded in the job brief; these new covers, listing and trailer still need Chief review. No schedule is set in the draft manifest. Board's proposed slot remains a decision for the release job.

## Files and handoff

Local final covers: shared checkout `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/08_Thumbnail/abc_v01/gliese_thumb_{A,B,C}.jpg`.
Local trailer: same film's `11_Upload-Package/Trailer/gliese_trailer_v01.mp4`.
Review branch has metadata, captions, builders, checks and review sheets only. Media hashes and local paths: `MEDIA_MANIFEST.json`. Durable NAS package backup: `youtube-staging/028/release-package-v01/` (verified manifest accompanies it).

Next: Chief accepts or revises title/A/B/C/trailer and the two tool substitutions, obtains the packaging panel required by house rules, merges the review branch, then queues the authorised upload/Studio finish. Future Studio work includes captions en-GB, audience/disclosure read-back, A/B/C test, end screen and pinned comment. Nothing public was changed.

## Storage

9.3 GiB free at start. Attempted to follow the superseded v01 scratch archive rule; automatic approval review rejected the proposed local video removal, citing “never delete a video”, even with a verified NAS copy. No removal occurred. v02/v03 and existing scratch were left intact. No NAS deletion attempted. The new package uses small assets and the already-archived master, not another full master render.
