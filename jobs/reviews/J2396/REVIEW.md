# Chief Resolution — `031` Pipeline `missing-next-step` (`J2396`)

- **Film:** `031_What-Happens-When-Earths-Magnetic-Field-Flips` (`OWB:031`)
- **Stage / Handoff:** `{"film": "031", "stage": "pipeline", "kind": "missing-next-step", "signature": "15b72f9119326ab7f2d6"}`
- **Reviewer:** `gemini` (`J2396`, `kind: chief`, elected acting Chief)
- **Date:** `2026-11-08`
- **Ruling:** **PASS on `031` `edit` (`J2390` + `J2395` KEEP); queue missing `031` `stage: upload` release-package & held Private-upload successor jobs (`J2400` -> `J2401`).**

---

## 1. Current Film Status, Approval History & Verified Evidence (`031`)

1. **`topic` / `script` / `sources` (`done`, ref `666bacf8`):**
   - Locked script `01_Script/magnetic_field_flip_script_master_v03.md` (`95.4 / 100` on `review:script`, `J0259`) and quote-checked `01_Script/SOURCES.md` (`666bacf8`).
2. **`vo` (`done`, ref `6536440194`, `J1295` / Chief `h32`):**
   - Locked stem `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/02_Voiceover/magnetic_field_flip_vo_v02a.wav` (`SHA-256: 3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6`, `568.28 s`, `27,277,440` frames, `I -19.9 LUFS`, `-3.5 dBTP`). Technical verification `PASS` (`J1752`, `02_Voiceover/review_J1752/REVIEW.md`); `J1810` capability note preserved (`jobs/reviews/J1810/REPORT.md`).
3. **`shots` (`done`, ref `55d4dad1c2`) & `picture` (`done`, ref `ae085e857c`):**
   - Locked 54-row shot list `07_Edit-Project/SHOT_LIST_v02.md` (`55d4dad1c2`) and completed £0 picture package `07_Edit-Project/BUILD_HANDOFF_J2141.md` (`ae085e857c`).
4. **`thumbs` (`done`, ref `765d77f8f5`, `J2143` / `J2166` KEEP):**
   - Three approved 1280×720 thumbnails in `/Users/benjaminoats/_desk/j2143/final/` (`jobs/reviews/J2166/REVIEW.md`, `765d77f8f5`, proposed unarmed `T021` in `05_Analytics/tests/THUMB_LEDGER.json`):
     - **A (`COMPASS REVERSED`, rule 12):** `031_A_compass_v03.jpg` (`SHA-256: e1d396ebed9d5c2371a6dea4852dd2846e1541ac4cc6f360cb4d761afd2d6df0`, `sat=194.5`, `near_black=9.0%`).
     - **B (textless real NASA ISS `ISS062-E-98264`, rule 19):** `031_B_real_v04.jpg` (`SHA-256: 742c404da7ad74d3bad2bc4c91f8d5b860fd4e12bef3e37a6f1fbcbb657fa874`, `sat=133.3`, `near_black=24.1%`).
     - **C (`GLOBAL AURORAS`, rule 12 + rule 14 bright background):** `031_C_bright_v03.jpg` (`SHA-256: a4ee140a242a5a1c2a3eb1e2b8a4b4700685fccc94ca3055aca1dc2621c35ff0`, `sat=171.0`, `near_black=3.6%`).
5. **`edit` (`done`, ref `aa9ca3d244`, `J2390` `1f42136dce` + `J2395` `aa9ca3d244` KEEP):**
   - **Long Master `v02` (`J2387`, reviewed KEEP in `J2390`, `jobs/reviews/J2390/REVIEW.md`):**
     - Master MP4: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4` (`SHA-256: 680598ae3420afa9fd40efc954cf06cefcfff234044a62e90af6a143fdf4de43`, `570.80 s` / `14,270` frames @ `25 fps` CFR, `-14.6 LUFS`, `-1.0 dBTP`, `0` black frames; `clip_check` 54 rows `PASS`, `picture_qa` `0/115` fail `PASS`, `music_gate` `PASS`, `sfx_kit level` `PASS`).
     - 720p UAT proxy: `031_what_happens_when_earths_magnetic_field_flips_master_v02_PHONE.mp4` (`SHA-256: a8c748f68cf2215f224f0d616b145ec45ffe04db4b0bfd305a9541bbc9931c9d`), staged in NAS & iCloud `OWB UAT` and R2 (`owb-031-v02`), awaiting Ben's watch under `J2395.1` (`airs: 2026-12-02T18:00Z`, `due: 2026-12-01T18:00Z`).
   - **Active Short #1 (`J2388`, Test A opening cut, reviewed KEEP in `J2395`, `jobs/reviews/J2395/REVIEW.md`):**
     - Master MP4: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01.mp4` (`SHA-256: ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd`, `33.00 s` / `825` frames @ `25 fps` CFR; all 7 gates `PASS`), staged in NAS & iCloud `OWB UAT` and R2 (`owb-j2395-2-v01`), awaiting Ben's watch under `J2395.2` (`airs: 2026-12-05T11:30Z`, `due: 2026-12-01T18:00Z`).
   - **Active Short #2 `v02` (`J2394`, Keeper question cut, reviewed KEEP in `J2395`, `jobs/reviews/J2395/REVIEW.md`):**
     - Master MP4: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02.mp4` (`SHA-256: 4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450`, `24.48 s` / `612` frames @ `25 fps` CFR; all 7 gates `PASS`), staged in NAS & iCloud `OWB UAT` and R2 (`owb-j2395-3-v02`), awaiting Ben's watch under `J2395.3` (`airs: 2026-12-12T11:30Z`, `due: 2026-12-01T18:00Z`).

---

## 2. Root Cause of `missing-next-step` (`15b72f9119326ab7f2d6`)

1. When `J2395` closed `done` (`aa9ca3d244`), `031` remained in `queue.json` `focus` (`['032', 'OWB:032', '031', 'OWB:031', '033', 'OWB:033']`) with `stages.upload` not yet completed (`todo`) and zero live `owb` jobs (`open`, `claimed`, or `blocked`) carrying `film: "031"`.
2. Furthermore, `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/status.json` `stages.edit` retained the earlier `J2382` `FIX` metadata (`ruling`, `review_job: "J2382"`, `review_evidence: "jobs/reviews/J2381/REVIEW.md"`) because `studio.py set 031 edit done --ref aa9ca3d244` updated only `state` and `ref`.
3. In `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/11_Upload-Package/`, only the pre-assembly draft files (`metadata_DRAFT_v01.json` and `description_DRAFT_v01.txt` from `J1195`) exist, with `"time": "?:??"` chapter placeholders and explicit `"pre_upload_holds"` requiring:
   - Real chapter start times from the locked `master_v02` cut (`0:00 The Racing Pole`, `0:36 The Backwards Lava`, `2:05 The Ocean of Liquid Iron`, `3:46 The Dent Over South America`, `5:19 The Tree That Remembered`, `6:33 Why Our Air Stays Put`, `8:00 Poles All Over the Sky` per `cuts_v02.json`);
   - Exact image/agency credits from `cuts_v02.json` and `HARVEST_POOL_v01.json` plus a truthful making-of line in `Descriptions/magnetic_field_flip_long_description_v01.txt`;
   - `Captions/magnetic_field_flip_long_v02_en-GB.srt` generated from the locked VO word timings (`02_Voiceover/stt/magnetic_field_flip_vo_v02a/stt_raw.json`);
   - `Trailer/magnetic_field_flip_trailer_v01.mp4` (`608x1080` vertical trailer from `master_v02` cold open per `STUDIO_PLAYBOOK.md` §12);
   - `PACKAGE_MANIFEST.json` for Long Master `v02` (`Wed 2 Dec 2026 18:00` London) and `07_Upload-Package/PACKAGE_MANIFEST.json` for Active Shorts 1 (`Sat 5 Dec 2026 11:30` London) & 2 `v02` (`Sat 12 Dec 2026 11:30` London), verified by `npm run gate:episode` and `npm run youtube:package -- --dry-run` (`£0`, no YouTube upload);
   - Followed by the Private YouTube upload + Studio finish job (`stage: upload`) held on Ben's UAT watch (`J2395.1`–`J2395.3`, or the 24-hour pre-air fallback on `2026-12-01T18:00:00Z`).

---

## 3. Resolution Actions Taken

1. **Updated `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/status.json`:**
   - Updated `stages.edit` to record the `J2390` (`1f42136dce`) and `J2395` (`aa9ca3d244`) `KEEP` rulings and verified `SHA-256` hashes for `master_v02.mp4`, `031_short_testA_opening_flip_v01.mp4`, and `031_short_sat12_solar_wind_air_v02.mp4`.
   - Initialized `stages.upload` (`state: "todo"`) referencing the queued `stage: upload` release-package and held Private-upload jobs while preserving `J2395.1`–`J2395.3` `awaits_ben` cards in `Ready for OK`.
2. **Queued Linked `stage: upload` Successor Jobs (`film: "031"`):**
   - **Release Package + Dry-Run Job (`film: 031`, `stage: upload`, `kind: listing`, `needs: mini`, `status: open`, `due: 2026-12-02T18:00:00Z`):** Build `11_Upload-Package/PACKAGE_MANIFEST.json` (chapters `0:00`, `0:36`, `2:05`, `3:46`, `5:19`, `6:33`, `8:00`, agency credits from `cuts_v02.json`, `en-GB` SRT captions, `608x1080` vertical trailer, pinned comment, tags, titles) + Active Shorts 1 & 2 `07_Upload-Package/PACKAGE_MANIFEST.json` and run `gate:episode` + `youtube:package --dry-run` (`£0`, no upload).
   - **Held Private Upload + Studio Finish Job (`film: 031`, `stage: upload`, `kind: studio`, `needs: mini`, `--after <package_job>`, held with `jobs.py wait --type ben` until `2026-12-01T18:00:00Z`):** Private YouTube upload of Long Master `v02` (`Wed 2 Dec 2026 18:00` London, `T021` Test & Compare A/B/C, `en-GB` captions, end screen) and Active Shorts 1 & 2 (`Sat 5 Dec` & `Sat 12 Dec 2026 11:30` London, custom covers) once Ben OKs `J2395.1`–`J2395.3` (or at the 24h pre-air fallback `2026-12-01T18:00:00Z`).
