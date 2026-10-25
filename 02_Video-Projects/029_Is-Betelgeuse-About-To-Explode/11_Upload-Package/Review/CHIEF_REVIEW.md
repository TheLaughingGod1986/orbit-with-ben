# J0921 — 029 Betelgeuse release package v01

**Worker draft for Chief. No final OK, PASS, merge, upload or scheduling decision made.**

Proposed title: **Is Betelgeuse About to Explode?** (31 chars; backups B: *What Happens When Betelgeuse Finally Explodes?*, C: *Why Did Betelgeuse Suddenly Go Dim in 2019?* in `Titles/betelgeuse_title_v01.txt`).

Primary A: **BRIGHT AS MOON** (yellow hook `MOON`, top band). Test alternatives B: **PAST MARS** (yellow hook `MARS`, left edge band); C: **IT WAS DUST** (yellow hook `DUST`, top band). Built at 0 credits (£0) from approved `07_Edit-Project/harvest_v01/` agency plates via `08_Thumbnail/build_betelgeuse_covers_v01.py`. No Orbit on any variant.

Proposed slot: **Sun 6 Dec 2026 18:00 London (`2026-12-06T18:00:00.000Z`)** — first free Sunday 18:00 London long slot after 028 (`F-jImX5h7ws`, Sun 29 Nov 2026 18:00Z), verified free against `00_Brand/Channel-Setup/social/UPLOADS.json` (where only 028's weekday Shorts occupy 30 Nov, 2 Dec, 4 Dec and 7 Dec at 11:30Z). Left unscheduled (`status: "review"`, no `schedule` field) in `PACKAGE_MANIFEST.json` until Chief's upload/schedule ruling.

## Evidence

- **Approved master unchanged (`v03b` as release master):** NAS `/Volumes/data/mac-mini-archive/youtube-staging/029/029_Betelgeuse_full_rough_v03b.mp4`, SHA-256 `54e04d3bfcb42bcf9066a0613254f10c978435b148d158468711e25908060c93`, 542.230 s (9:02), 1920×1080, 30 fps, 84 cuts, **−14.0 LUFS / −1.2 dBTP / LRA 3.6 LU**. No picture or sound changes made.
- **`Review/episode_gate_v01.txt`:** `npm run review:script` PASS **92.2 / 100** (`01_Script/betelgeuse_script_master_v02.md`); `npm run gate:episode` 9/10 checks OK (`PRE_BUILD_VIDIQ_AUDIT.md` completed from J0027 neighbour audit; only historical `subscribe_beat` at 52% vs 50% on the locked v02 script, untouched per Chief Final OK `6384887788`).
- **`Review/THUMB_SCORE.txt`:** `thumb_preview.py --score` PASS on all three covers:
  - `betelgeuse_thumb_A.jpg` (`BRIGHT AS MOON`): `saturation=140.1`, `near_black=6%`, `PASS`
  - `betelgeuse_thumb_B.jpg` (`PAST MARS`): `saturation=150.1`, `near_black=10%`, `PASS`
  - `betelgeuse_thumb_C.jpg` (`IT WAS DUST`): `saturation=143.3`, `near_black=7%`, `PASS`
  - HOOK / BAND / GRADE / PHONE verified at `168×94` (`Review/thumb_preview_v01.jpg`), full size (`Review/THUMBNAILS_FULL_SIZE.jpg`), alongside 028 (`Review/owb_family_sheet_v01.jpg`), and against all 8 live OWB long primaries 021–028 (`Review/style_sheet_v01.jpg`). Zero overlap between text bounding boxes, hero objects, and bottom-right duration badge (`Review/COVER_LAYOUT.json`).
- **`Descriptions/betelgeuse_long_description_v01.txt` & `Chapters/betelgeuse_chapters_v03b.txt`:**
  - Six chapter timestamps from v03b cut list: `0:00 A dying star in Orion`, `0:37 The Star in Orion's Shoulder`, `1:45 The Great Dimming`, `2:50 How a Giant Star Dies`, `4:08 The Night It Goes`, `5:43 So When Will It Explode?`.
  - One `Sources:` line with 5 quote-backed papers from `01_Script/SOURCES.md`: Joyce et al. (2020, *ApJ* 902, 63), Montargès et al. (2021, *Nature* 594, 365–368), Dupree et al. (2022, *ApJ* 936, 18), Goldberg, Bauer & Howell (2020, *RNAAS* 4, 35), and Howell et al. (2025, *ApJL*, `arXiv:2507.15749`), followed by agency image credits and honest AI/facts disclosure.
- **`Captions/betelgeuse_long_v03b_en-GB.srt` (`Review/CAPTION_PROVENANCE.md`):** 174 cues, all 1,248 words from `07_Edit-Project/full_rough_v03b_pack/betelgeuse_words_list.json` (`0.080–514.260 s`), ≤2 lines and ≤42 chars/line, en-GB spelling (`centre`, `Moon`, `Sun`).
- **`Pinned-Comments/betelgeuse_pinned_v01.txt` & `Tags/betelgeuse_long_tags_v01.txt`:** Viewer question + subscriber thank-you; 8 subject tags (no channel names).
- **`Trailer/betelgeuse_trailer_v01.mp4` (`Review/TRAILER_RECIPE.md`, `Review/TRAILER_AUDIO.json`, `Review/trailer_end_v01.jpg`):** 40.4 s, vertical `608×1080`, 30 fps, `0–37.30 s` cold open from approved v03b master + `37.30–40.40 s` existing score bed tail with house CTA (`Full film / on YouTube`), two-pass loudnorm **−14.08 LUFS / −1.02 dBTP**.
- **`Review/YOUTUBE_DRY_RUN.txt` & `Review/VALIDATION.json`:** `npm run youtube:package -- --dry-run` `ok: true`, `dryRun: true`, `format: "longform"`, `privacy: "private"`, `madeForKids: false`, `containsSyntheticMedia: true`, `categoryId: "28"`. All 13 mechanical checks in `validate_package.py` PASS (`all_checks_ok: true`).

## Files and Handoff

- Local covers (git-ignored media, tracked in `Review/MEDIA_MANIFEST.json`): `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/08_Thumbnail/abc_v01/betelgeuse_thumb_{A,B,C}.jpg`
- Local trailer (git-ignored media, tracked in `Review/MEDIA_MANIFEST.json`): `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/11_Upload-Package/Trailer/betelgeuse_trailer_v01.mp4`
- Durable NAS backup: `/Volumes/data/mac-mini-archive/youtube-staging/029/release-package-v01/` (`Review/NAS_BACKUP.json`)
- Scratch used `/Volumes/data/mac-mini-archive/scratch/J0921/`; Mac mini free space ~21 GiB (`df -h /`). Nothing uploaded, scheduled, retitled, or deleted. £0.
