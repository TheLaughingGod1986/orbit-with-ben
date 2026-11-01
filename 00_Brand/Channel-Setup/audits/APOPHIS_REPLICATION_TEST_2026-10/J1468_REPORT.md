# J1468 audio repair — 1 November 2026

Codex covering. £0; no generation, upload, scheduling, or privacy changes. **Audio repair complete; cohort remains held for Chief / J1356. No film PASS or final OK.**

AR1 v01, AR2 v06 and AR3 v05 remain SHA-256 identical to their accepted inputs. All three new video elementary streams match their respective inputs byte for byte (`ffmpeg -c:v copy` plus stream SHA-256). Original h40 VO and house SFX stems are reused without editing words or timing. The existing 60-second score and plan were copied into this test’s 05_Music. A speech-keyed, quiet bed covers the full runtime including the loop tail. Separate source VO, SFX and laid music stems are retained with the persistent masters.

The package manifests on this branch now point to existing versioned 06_Final-Exports files; old masters and old export targets were not overwritten. This updates a pre-upload package only.

| Cut | LUFS | dBTP | Music / SFX / picture / polish | Shorts open |
|---|---:|---:|---|---|
| owb_ar1_2024_yr4_moon_v02.mp4 | -14.52 | -1.90 | PASS / PASS / PASS / PASS | FAIL: first cut at 6.00s > 3.0s (scene-change detect) |
| owb_ar2_iss_2030_deorbit_v07.mp4 | -14.57 | -1.89 | PASS / PASS / PASS / PASS | FAIL: pushed still at frame 0 (mean 0–1.5 s frame diff 0.25 < 1.50) — use moving footage |
| owb_ar3_2027_eclipse_v06.mp4 | -14.22 | -2.11 | PASS / PASS / PASS / PASS | FAIL: pushed still at frame 0 (mean 0–1.5 s frame diff 1.41 < 1.50) — use moving footage |

Music reuse is explicit in the J1468 brief. After rechecking `chief_relay.py status` (Codex elected; Grok and Claude down), Codex recorded `music_gate_j1468_chief_waiver.json` for the **reused** check alone, as the gate’s documented mechanism permits. Music own/brief/gap/length all pass; no other check is waived. Pace WARN remains: measured ~120 BPM versus the original 84–96 brief. Several unavailable legacy UAT comparison files produce WARNs. The score is the requested existing test score, not a newly generated bed.

The unmodified Shorts gate still FAILs on each accepted opening: AR1 first detected scene change at 6.00 s; AR2 and AR3 pushed-still opening detection. All durations remain the h40 17–20 s test cuts; the generic 22–27 s band is a WARN. The brief forbids changing picture, so these failures are retained for J1356; none is overridden. No meta sidecars were supplied, so these gate runs do not represent a complete packaging lint.

AR3 required a common +8 dB mix gain and peak limiter (ceiling 0.78, 5 ms attack / 50 ms release) to reach −14.22 LUFS while retaining −2.11 dBTP. AR1 and AR2 use measured loudness normalisation and a 0.7943 ceiling. The SFX/bed ratio gate checks the separate pre-master stems; the common mastering processing is recorded in repair_j1468.py. Final-second volumedetect reports and final file hashes are in J1468_evidence. No audio audition or new creative picture review is claimed.

Run with `/Users/benjaminoats/_desk/venv-graphics/bin/python repair_j1468.py` from this audit folder after staging the required media in the main checkout. The script refuses existing new-version masters; do not rerun over delivered files. The system Python lacks NumPy, so its initial QA attempts were discarded; final evidence uses the installed graphics environment. Earlier local attempts are preserved under 07_Edit-Project/assembly_j1468_attempt1 and `.attempt2.mp4` files, outside git.

Next: Chief / J1356 reviews the audio repair, the pace WARN and the existing opening failures. Picture remediation requires a separately scoped new version; these cuts must not be uploaded or scheduled with a failing ship gate. Nothing for Ben.
