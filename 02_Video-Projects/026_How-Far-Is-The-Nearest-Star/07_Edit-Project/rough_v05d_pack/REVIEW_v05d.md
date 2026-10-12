# J0148 — Bessel WHO correction, v05d

Codex, 12 Oct 2026. Worker evidence only; Chief retains the review and final decision.

Chief requested sourced Bessel years and retained the existing overlays, including labels across one cut. This version adds only `Friedrich Bessel` / `1784–1846 · Astronomer` at 185.28–188.88 s (first name mention), a 3.6-second lower-third card. It fades and rises over 0.35 seconds, fades out over 0.3 seconds, and stays clear of the existing 1838 label. The date label and all existing cuts remain. Audio is stream-copied from v05c.

The birth, death and 1838 parallax claims each have an exact-excerpt source row in `01_Script/SOURCES.md`. Codex retrieved the RAS and ESA pages. `GEMINI_BESSEL_J0148.md` is Gemini's unchanged output: it supports the claims from supplied excerpts, not independent retrieval (its initial read_url request was unavailable in headless mode). No narration was rewritten.

Builder: `../_overlay_nearest_star_v05d.py`. Input: `/private/tmp/026_NearestStar_v05c_PHONE.mp4`. Output: `/private/tmp/026_NearestStar_v05d_PHONE.mp4`. The new graphic is listed on both intersecting cuts in `cuts_v05d.json`; `overlays_v05d.json` retains the earlier overlay metadata.

Detached process: `j0148-bessel-render`; log `/Users/benjaminoats/_desk/logs/j0148-bessel-render.log`; exit-code file `/Users/benjaminoats/_desk/logs/j0148-bessel-render.done`. Do not launch another copy while it runs.

Validation complete: detached run exited 0. `picture_qa` reports PASS, 0/103 failed cuts and 38 warnings; `polish_gate` reports PASS, 0/103 failed rows and 13 warnings. These are automated tool results, not a Chief sign-off. `audio_v05d.json` confirms identical encoded audio MD5; `stream_check.json` confirms unchanged 1920×1080, 30 fps, 14,803 frames and stream durations. Full-size card frames at 186.2 and 187.5 s were visually checked either side of the cut. Chief reviews the new card and decides acceptance. SHA256.txt records the output hash. Existing Chief-reviewed exceptions from `polish_reviewed_ok_v05b.json` are used unchanged; no new exception or worker PASS is issued. No spend or YouTube state change.
