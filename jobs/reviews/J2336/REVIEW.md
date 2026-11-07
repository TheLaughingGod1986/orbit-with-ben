# J2336 — Pluto pickup ruling

7 November 2026, codex, elected acting Chief (relay checked before decision).

**FIX.** Reject the Chapter 5 v02 pickup for assembly. J2157 remains unapproved; no shot-list release. J2335 used its bounded attempt correctly and stopped on failure. J2337 is the immediately eligible repair successor; its brief is alongside this review. No generation or credit spent in J2336.

## Evidence checked

- PR611 head 6261719f0e3042e240b7c4e6155bfc74e7a881ef: reviewed J2335/EVIDENCE.md and file inventory. PR604 correction at 535ba3c502 explicitly supersedes its old envelope and listening claims; those claims are not accepted as perception evidence.
- Independently hashed shared pickup WAV: 9372255a0ae75b183206ef3e3263420c6e517b1b62341683cc0f6a76032bdc19. Python wave/array measurement: 48 kHz, stereo 16-bit, 241920 frames / 5.040 s; last three non-overlapping 50 ms RMS windows -29.3023, -28.5975, -25.1976 dBFS; final stereo sample -2365/-2365. This reproduces the reported rising, abruptly terminated tail. A nonzero sample alone would not establish a clipped word; the combined envelope and endpoint evidence fails the required decay check.
- The reported 100% normalised Scribe match establishes recognised tokens, not a complete ending or heard delivery. Raw punctuation difference remains documented. No audio perception was demonstrated or claimed in this session.
- Independently rehashed original v01 master: WAV 86483fb4919c3fd097a84d3c0d43f52a89521f87b2ff6f1976dea1506d2c8618; MP3 b7fdd348819c9e2dd98a01fc8ca272f1a135c6ff033302ad98022d8eb7bcaf85. Both match the protected originals.
- The raw API MP3 is absent at the shared pickups/parts/pluto_ch05_looked_back_v02/ch00.mp3 path. No assertion that truncation originated at the API: J2337 must locate the worker source and test recovery before spending. vo_take.py contains no explicit silence trim in its decode/concatenation path.

## Decision and next action

J2337 first tests no-spend recovery from the raw response. If that also ends prematurely, one request per target with verbatim trailing script context is authorised (two requests maximum, 1200 subscription credits aggregate). Context is discarded only at a verified pause after natural target decay. The hypothesis is that placing the target before the response end avoids endpoint truncation; success remains to be measured. No text change enters the film, no full-chapter regeneration, no padding/fade used to hide unfinished speech, no retries outside the cap. See REPAIR_BRIEF.md for the worker contract.

J2157 retains a dependency hold for J2337 and its required final ruling. J2335 is superseded failed work, not a completed VO repair. The future elected Chief may close J2157 and release the shot list only after all technical checks pass. Ben's finished-cut UAT supplies listening under STUDIO_PLAYBOOK section 10/Review; missing agent audio input is not itself a blocker. Nothing requires Ben now.

PR604 and PR611 remain evidence submissions, not merged or approved as a voice PASS by this ruling. No media or raw transcript/spend payload is copied into this decision branch. No upload, scheduling or privacy change.
