# J1204 Uranus v05: Chief ruling, 29 Oct 2026 (~17:15Z)

**Decision: FIX. No PASS, no Ben card. Authorize v06 (no spend) from the same approved Shot9 file, built to the notes below.**

Before ruling, Chief checked that nobody had ruled on v05 already. The J1204 log ends at cursor's 16:46Z park. PR #264 has nothing after the 16:55Z relay duty ping, HOS #180 has nothing on J1204, and `jobs/reviews/J1204` holds no v05 ruling.

## What Chief verified (independently, on the mini)
| Check | Result |
|---|---|
| v05 SHA-256 (repo export, iCloud UAT, NAS UAT, MANIFEST) | `6bcb32fa58635dc8574d6bc083c330587ae7867628e6f493d14958daf0c03cc4`: all four match |
| Shot9 source SHA-256 (`scratch/J1206/raw/Shot9_1k_mp4.mp4`) | `f964c7f1…249fb3e`: matches delivery and meta. 1920×1080, 60 fps, 9.97 s. NASA SVS 20390 (Conceptual Image Lab artist animation, public domain) |
| Loudness, re-measured (ebur128) | I −14.1 LUFS, TP −1.8 dBTP: inside −14.5..−13.5 and below −1.6. The 16:42 log FAIL (−14.7/−1.5) was before the remux, and the remuxed file passes |
| gate_shorts_open (`_gate.txt`) | PASS, f0diff 3.41, cut1 2.7 s, vo_onset 0.00 s. Warns only: 18.0 s duration, 2.08 s tail gap (same class as earlier SA Shorts) |
| finish_scan loop, re-run with `scripts/short_c37.loop_metrics` | **FAIL confirmed**: loop_diff_masked 7.45 > 2 × open median step 3.44 = 6.88. Head matches [0,0,0,0,0], so the tail runs forward and isn't a copy |
| Frames (f0, f30, f78, f510, f539 full size) | Real moving rings and disc. Recognisable Uranus. Hook and captions correct. Frame 0 is not a still, with no pan or zoom |
| polish / music / sfx / picture_qa | PASS (rc 0). Note: these reports and the PHONE/frames/2fps exports are timed 16:43, so they came from the pre-remux render (`00e4f679…`) and not from the 16:45 sha `6bcb32fa…` |

## Why the accept-hairline option is refused
1. Chief does not wave through a gate FAIL. The loop gate exists for Ben's bar of 70%+ average viewed, aiming past 100% with loop endings. Our recent Shorts sit near 30% stayed and 75% viewed (Earth Short OVLv9dxTcpE: 30.7% / 75.3%), so the loop is a lever we need.
2. The miss is structural, not noise. Chief's own Shot9 step profile (same 608×1080@656,0 crop, 270×480 mask rows 105–375) shows the rings motion **decelerating through 4.0–6.7 s**: steps fall from ~5.5 to ~1.8 per frame. So the open median (3.3–3.4) is far below the seam step (~5.6 raw, 7.45 with hook text present on frame 0 only). No v05 tweak fixes that ratio.

## Model of the authorised v06 window
The model is calibrated on v05: simulated seam 5.58 + 1.87 hook/encode offset = 7.45, which matches the actual figure.
| Open window | seam est | open median | 2× median | margin |
|---|---|---|---|---|
| 4.00–6.70 (v05) | 7.45 | 3.30 (actual 3.44) | 6.59 | −0.86 (actual −0.57) |
| 3.50–6.20 | 8.05 | 4.06 | 8.12 | +0.07 (too thin) |
| **2.00–4.70** | **8.30** | **6.26** | **12.52** | **+4.2** |
The silent-probe f0diff for 2.00–4.70 is 4.74 (≥1.50). The motion is nearly constant there (steps 6.0–6.5), so the open and the seam match.

**Source defect found by Chief:** Shot9 has a hitch at **2.37–2.47 s**. Two near-duplicate 60 fps frames (steps 0.19, 0.14) are followed by a double step. In the default even-frame 30 fps decimation, this becomes a held frame (step 0.24) and then a jump (11.92). With a 2.00 s open, that would land at 0.37–0.47 s on screen. Chief tested both decimation phases. The **odd phase is smooth**: steps around it run 6.0 / 7.05 / 2.95 / 6.25 / 8.57 / 6.4, with no hold and no double jump. That is the same footage at 1.0×, with no frames dropped or added beyond normal 60→30 decimation, and no motion assist.

## v06 notes (concrete, all required)
1. **Source:** same file, Shot9 `f964c7f1…`, same crop 608×1080 @ 656,0 → 1080×1920 (1.778×), 1.0× speed.
2. **Cycle:** start at 60 fps source frame **53 (0.8833 s)**, length 3.833 s (frames 53–282, every other frame → odd phase). The tail runway is source 0.8833–2.0167 s (34 frames, 1.133 s). The **open is source 2.0167–4.7167 s** (81 frames). Do not start at an even frame. Verify in the build log that the 30 fps frames used are the odd 60 fps indices.
3. **Everything else identical to v05:** S2-first VO `vo_v05.wav` (`f59211a8…`), word-for-word captions, URANUS first word, hook 21-YEAR / WINTER 0–2.2 s, TIPPED 97° overlay 2.2–4.2 s, title window, plates rows 2–5, music bed, SFX, mix. No new VO, no rewriting, no added zoom/jitter/overlay motion, gate thresholds unchanged.
4. **Loudness first, then everything else:** land −14.5..−13.5 LUFS and TP ≤ −1.6 in the master mux. Then generate PHONE, frames, 2fps, polish, music, sfx, picture_qa, gate and loop **all from the final-sha file**. Each report records the sha it ran on. MANIFEST covers every file.
5. **Picture QA provenance:** the Shot9 rows still warn "no title in the pool" and "upscale not recorded in the cut list". The 12:45Z brief requires honest source titles and measured upscale in the QA pool and cut list. Put "Beauty shot of Uranus' rings (Shot9), NASA SVS 20390, Conceptual Image Lab artist animation" and 1.778× where picture_qa reads them, so those two warns clear on rows 1 and 6. A low-detail warn on the PIA00346 plate may stay.
6. **Full gate set:** gate_shorts_open (f0diff ≥1.50), finish_scan loop and all finish_scan checks, polish, picture_qa, music, sfx. Also add to the delivery: the steps for timeline 0.30–0.55 s (none <0.35 or >2× median) and full-size frames at 0.33/0.40/0.47 s. These prove the 2.4 s source hitch isn't on screen.
7. **Preserve** v02/v03/v04/v05 files and hashes. Deliver `URANUS_V06_DELIVERY_2026-10-29.md` with sha, reports, frames, PHONE, UAT iCloud + NAS, and park for Chief.

## Stop rule / fallback
- If v06 passes every gate, park for Chief cut review. Only a Chief PASS goes on Ben's board, with his 10:30 London watch deadline on Tue 3 Nov.
- If v06 still fails loop or any gate, **do not iterate further on Shot9 windows.** Park with the numbers. The 16:15Z rule stands: if nothing clears by **1 Nov 18:00Z**, close the Uranus branch as unsuccessful, and the scheduled `ZpEA8stoSPA` copy airs Tue 3 Nov as J1199's fallback.
- No upload, swap, schedule, privacy, Buffer or UPLOADS change. £0. J1199 stays held. S5/S6 remain with J1208.
