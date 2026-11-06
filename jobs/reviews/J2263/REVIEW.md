# J2263 Review — HOS 006 Short B v02 and Short C v03 (Ref: J2169)

- **Reviewer**: `gemini` (`gemini-argon` / Gemini 4 Argon High, Mini specialist worker)
- **Date**: 2026-11-06
- **Reviewed Job**: `J2169` (`HOS 006: build active Short B and C for 18 and 21 Nov from existing media`, answering `J2258` FIX)
- **Evidence Commit**: HOS branch `cursor/J2169-bc-v02`, commit `b8230f85b76075489bf47f64cb9db17bea032cf9` (`02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/j2169_v02/ASSEMBLY.md`; earlier `v01`/`v02` cuts remain intact in `j2169_v01` at `699c359bf44ccda9d996dae4a2d6524be3774a03` and on disk/NAS)
- **Verdict**: **`KEEP`** (both `Short_B v02` and `Short_C v03` satisfy all `J2258` FIX requirements and current HOS channel/Shorts gates at **£0 / 0 credits**)
- **Approval / Gate Status**:
  - Neither cut is approved for publication (`approved: false`).
  - `watched: false` and `heard: false` remain unchanged until Ben's final watch (`AGENTS.md` 4 Nov 2026 order).
  - `awaits_ben` is set on `J2263` (`J2263.1` for `Short_B v02`, `J2263.2` for `Short_C v03`, watch-by `2026-11-15 18:00` London) with unique verified R2 Play links (`hos-j2263-1-v02` and `hos-j2263-2-v03`).
  - Long `VbPubYd6Fbs` (*The Willow Tree That Was Made of Air*) must be public before either Short is published.
  - Slots `2026-11-18 11:30` and `2026-11-21 11:30` Europe/London remain conditional planning targets, not a schedule.
  - Standalone `S7` (`hos_sa_s7_priestley_mint_v02`) was not built and stays planned; `Short_A` and retired/superseded `s04`–`s08` were not built.
  - **Spend**: £0 / 0 credits. No YouTube upload, schedule, privacy change, retitle, or Buffer write performed.

---

## 1. File Integrity, Hashes, Decode, and Repo Gate Verification

All rendered deliverables in `/Users/benjaminoats/_desk/renders/J2169/`, `/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/J2169/`, and `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/J2169/` were verified directly on the Mac mini:

| Artifact | SHA-256 | Desk / NAS / UAT | Stream & Decode Check (`ffmpeg` + `freezedetect=n=0.003:d=0.5`) |
|---|---|---|---|
| `Short_B_v02/hos006_short_b_v02.mp4` | `f4b046d41d0d6fcfbd14258abe472d57db5c9d53c1ed535141aa3281e1f3915b` | Exact match (`20,893,457` B across Desk, NAS `SHA256SUMS_v02.txt`, and `HOS UAT`) | `1080×1920` (`9:16`), `h264`, `24 fps` CFR, `24.250000 s` (`582` frames), AAC `48 kHz` stereo, `0` decode errors, `0` freezes |
| `Short_B_v02/picture.mp4` | `84bd83731083a01623229546042850771107d4ada786cf147277d30b77620e5b` | Desk (`25,364,782` B) | `1080×1920`, `24 fps` CFR, `24.250000 s` (`582` frames), `0` decode errors, `0` freezes |
| `Short_C_v03/hos006_short_c_v03.mp4` | `e1e3ff0ce3b5622b4a43d010a0df827bcd34e25ccd76a87338b286b0632c40c5` | Exact match (`30,846,220` B across Desk, NAS `SHA256SUMS_v02.txt`, and `HOS UAT`) | `1080×1920` (`9:16`), `h264`, `24 fps` CFR, `25.166667 s` (`604` frames), AAC `48 kHz` stereo, `0` decode errors, `0` freezes |
| `Short_C_v03/picture.mp4` | `7f88fec1831fde6d687482b0bf8d997f84aa7a07c38e982740e52d3f0adf62bb` | Desk (`38,873,692` B) | `1080×1920`, `24 fps` CFR, `25.166667 s` (`604` frames), `0` decode errors, `0` freezes |
| `Short_B` VO (`t2_mint_fixed_vo_v03b.mp3`) | `0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479` | Locked take | 57 words (`0.00–23.08 s`); sentence 1 *"A sprig of mint repaired the air."* ends at `2.24 s` (canonical mint take, not soil take; spoken lines not rewritten) |
| `Short_C` VO (`t3_bubbles_sunlight_vo_v01.mp3`) | `5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269` | Locked take | 56 words (`0.00–24.16 s`); sentence 1 *"Leaves only make oxygen in the light."* ends at `2.56 s` (spoken lines not rewritten) |
| Score bed (`trees006_score_bed_v01.mp3`) | `942c643850c6dc87ffbd12396984d3a7fa2318c78a7f6c9a55622a406875f854` | Locked bed | `66.7 BPM` (brief `Pace: 60-72 BPM`), full-runtime cover on both cuts |

- **HOS CI check on `b8230f85b76075489bf47f64cb9db17bea032cf9` (`00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/006_Trees-Are-Made-Of-Air`)**: `ALL CHECKS PASS` (`durable desk handoffs: PASS`, `no media: PASS`, `status board in sync: PASS`, `ElevenLabs guard tests: PASS`, `vo_check word tests: PASS`, `atempo check tests: PASS`, `voice speed (atempo <= 1.06): PASS`, `contract tests: PASS`, `package-lint: PASS`, `review:script trees_script_master_v02.md: PASS (93.7/100)`, `gate:episode: PASS`).
- **Automated Gate Exit Codes on `Short_B v02` and `Short_C v03`**:
  - `picture_qa.py`: `PASS` (`0 fail` on both `picture.mp4` and `master`)
  - `polish_gate.py`: `PASS` (`0 fail` on all 8 rows of `Short_B v02` and all 9 rows of `Short_C v03`)
  - `sfx_kit.py level`: `PASS` (`Short_B v02`: VO `-18.1 LUFS`, SFX `-36.1 LUFS`, `1` hit, `fails: []`; `Short_C v03`: VO `-17.6 LUFS`, SFX `-35.6 LUFS`, `1` hit, `fails: []`)
  - `music_gate.py`: `PASS` (`verdict: PASS`, `bpm: 66.7`, `fail: []`, `matches: []`)
  - `gate_shorts_open.py check`: `PASS` (`Short_B v02` air date `2026-11-18`: `duration_s: 24.25`, `lufs: -14.5`, `true_peak_dbtp: -1.9`, `motion_0_1s: 10.36`, `frame0_diff_0_1_5s: 2.15`, `first_cut_s: 2.25`, `last_word_end_s: 23.2`, `tail_gap_s: 1.05`, `fails: []`, `warns: []`; `Short_C v03` air date `2026-11-21`: `duration_s: 25.17`, `lufs: -14.1`, `true_peak_dbtp: -1.8`, `motion_0_1s: 28.85`, `frame0_diff_0_1_5s: 5.44`, `first_cut_s: 2.58`, `last_word_end_s: 24.16`, `tail_gap_s: 1.01`, `fails: []`, `warns: []`).

---

## 2. Explicit Decisions on the J2263 Review Points & J2258 Fixes

### Decision 1 — Captions Through `9–14 s` and Frame-0 Hooks (Stills at `0.00 s`, `2.10 s` / `2.40 s`, and `11.20 s`)
- **Ruling: `KEEP` on both `Short_B v02` and `Short_C v03`.**
- **Frame-0 Hook Verification (`0.00 s` and `2.10 s` / `2.40 s`)**:
  - `Short_B v02` (`0.000–2.250 s`, frames `0..53`): renders `MINT` / `FIXED` in cream `#F5E8D2` `(245, 232, 210)` on the setup words and `THE` / `AIR` in yellow `#F6C445` `(246, 196, 69)` on the hook words, with dark stroke `#14100E` `(20, 16, 14)`, in `Didot.ttc` Bold at `220 px` (`cap height = 158 px = 8.23%` of `1920`, inside the `8–10%` rule), vertically and horizontally centred over the sunlit glass bell jar containing the mint sprig. The hook stays up through the full `S01` opening row (`2.10 s` and `2.208 s` stills verified), covering all of sentence 1 (*"A sprig of mint repaired the air."*, `0.00–2.24 s`) with zero dropped words.
  - `Short_C v03` (`0.000–2.583 s`, frames `0..61`): renders `ONLY` / `IN` in cream `#F5E8D2` on the setup words and `THE` / `LIGHT` in yellow `#F6C445` on the hook words, in `Didot.ttc` Bold at `220 px` (`cap height = 8.23%` of `1920`), vertically and horizontally centred over the sunlit underwater green leaf releasing rising silver bubbles. The hook stays up through the full `S01` opening row (`2.40 s` and `2.542 s` stills verified), covering all of sentence 1 (*"Leaves only make oxygen in the light."*, `0.00–2.56 s`) with zero dropped words.
- **Spoken Captions Through `9.00–14.00 s` and Full Body (`11.20 s` stills and `chunks.json` coverage)**:
  - Both cuts render multi-word HOS house subtitle chunks (`Didot.ttc` Bold `64 px` in cream `#F5E8D2` with dark outline, `y = H - 340 - block` in the lower safe band, clear of YouTube Shorts bottom UI) continuously from sentence 2 through the end of the VO (`16` chunks on `Short_B v02` covering `2.98–23.25 s`; `16` chunks on `Short_C v03` covering `2.85–24.167 s`; `missing = []`, `band_missing = []`).
  - At `11.20 s`, while the promoted long's exact live title (`The Willow Tree / That Was Made of Air`, `Didot.ttc` Bold `78 px` at `y = 170`) sits in the upper safe band (`9.00–14.00 s`), `Short_B v02` cleanly displays `"He slid in a sprig"` at the bottom over Priestley's bell jar and `Short_C v03` cleanly displays `"Tiny silver"` at the bottom under the sunny window jars.

### Decision 2 — `Short_B v02` Opening at Source Time `1.375 s` (`Frame 33`) and No Return Dissolve on `Short_B v02` / `Short_C v03`
- **Ruling: `KEEP` on both `Short_B v02` and `Short_C v03`.**
- **`Short_B v02` `source_in = 1.375 s` (`33 / 24`)**:
  - At `source_in = 0.0 s`, `03_pot_jar_leaf_t1.mp4` begins with a gentle camera ease-in; once the centred `Didot` hook caption covers the centre of the frame, `gate_shorts_open.py` measures `frame0_diff_0_1_5s = 1.05` (hard fail `< 1.50`) and `motion_0_1s = 5.1` (warn `< 10.0`).
  - Starting both `S01` (`0.000–2.250 s`) and `loop_tail` (`23.250–24.250 s`) at `frame 33` (`1.375 s`, crop `[638, 0, 608, 1080]`) lands on the active push-in, passing `gate_shorts_open.py` cleanly (`frame0_diff_0_1_5s = 2.15`, `motion_0_1s = 10.36`, `first_cut_s = 2.25`, `verdict: PASS`) while preserving identical `source_in = 1.375 s` on `S01` and `loop_tail`.
- **Absence of a Cross-Dissolve on `loop_tail` (`Short_B v02` and `Short_C v03`)**:
  - `scripts/terminal_loop.py` requires `first['framing']['offset'] == start and tail['framing']['offset'] == start` and verifies `rendered_correspondence` by comparing rendered frames at `0.00 s` and `0.50 s` (and one frame before the end of `loop_tail`) against both `S01` and the un-dissolved source plate (`MAE <= 12.0` / `8.0`). Adding a cross-dissolve at the end of `loop_tail` modifies those terminal frames relative to `S01` and the source plate, causing `terminal_loop.py` to fail. Keeping `S01` and `loop_tail` on matching `source_in` (`1.375 s` on `Short_B v02`; `0.000 s` on `Short_C v03`) without a post-dissolve is the exact lawful configuration that passes both `gate_shorts_open.py` and `terminal_loop.py` (`status: "rendered_correspondence"`, `errors: []`).

### Decision 3 — Cut Boundaries (`Short_B S05/S06/S07`, `Short_C S06/S08`) and `1080×1920` Delivery
- **Ruling: `KEEP` on both `Short_B v02` and `Short_C v03`.**
  - `Short_B v02`: `S05` runs `13.042–16.292 s` (`78` frames, ending before `"bright"` at `16.30 s`), `S06` runs `16.292–19.458 s` (`76` frames, ending before `"the"` at `19.46 s`), and `S07` runs `19.458–23.250 s` (`91` frames), keeping total duration at `24.250 s` (`582` frames) with no cut landing inside a word onset.
  - `Short_C v03`: `S06` (`short_c_s06_t01_1920.mp4`) starts at `offset = 4.458 s` (`frame 107`, running all remaining `83` frames `15.000–18.458 s` to the end of the `190`-frame clip; at `15.00–15.35 s` the gloved fingers release the jar as the voice says *"Move the jar into the"*, and from `15.40–18.458 s` the jar sits still in shade with no rising bubbles as the voice says *"shade, and the bubbles stopped."*), and `S08` runs `70` frames (`21.250–24.167 s`) so `loop_tail` begins at `24.167 s` after the last spoken word `"sunlight."` (`24.160 s`).
  - Both masters are delivered at `1080×1920` (`9:16`) with pre-normalised `1920×1080` (`flags=lanczos`) source plates and `608×1080` crops (`upscale = 1.776316× <= 2.35×` across all 17 rows).

---

## 3. Explicit Rulings on Every Tool `WARN` (No `WARN` Waived by Silence)

Every row of `Short_B v02` (`S01..S07`, `loop_tail`) and `Short_C v03` (`S01..S08`, `loop_tail`) was inspected at full `1080×1920` resolution on the master stills and `picture_qa_review.jpg` sheets:

1. **WARN — `Short_B v02` Row `S07` (`19.458–23.250 s`, `0:21`, `01_soil_to_sky_t1.mp4` crop `[600, 0, 608, 1080]`) — `low detail: edge density 0.0305 < film p5 0.0334` (`picture_qa_master` / `polish_gate`) and `0.0228 < film p5 0.0284` (`picture_qa_picture`)**:
   - **Ruling: `KEEP` source plate and crop (confirming `J2258` KEEP).** Full-size visual inspection (`b_21.35.jpg`) confirms a crisp, sunlit 3D-cartoon close-up of a green plant stem and leaves rising against a smooth blue sky (`std = 61.34`, `edge8 = 0.2335`, well above the absolute floor `std 13.44 / edge 0.0259`, `seams: []`).
2. **WARN — `Short_C v03` Row `S05` (`12.042–15.000 s`, `0:14`, `03_pot_jar_leaf_t1.mp4` crop `[1120, 0, 608, 1080]`) — `low detail: edge density 0.0343 < film p5 0.0364` (`picture_qa_picture`; cleared to `0.0631 >= 0.0537` in `picture_qa_master` / `polish_gate`)**:
   - **Ruling: `KEEP` source plate and crop (confirming `J2258` KEEP).** Full-size visual inspection (`c_13.52.jpg`) confirms a sharp, sunlit glass jar containing a green leaf covered in tiny silver bubbles before a warm window (`std = 55.68`, `edge8 = 0.2066`, `seams: []`), matching *"Tiny silver bubbles rose from the green leaves."*
3. **WARN — `Short_C v03` Row `S03` (`5.708–8.833 s`, `0:07`, `03_plunge_leaf_t1.mp4` crop `[656, 0, 608, 1080]`) — `low detail: edge density 0.0475 < film p5 0.0537` (`picture_qa_master` and `polish_gate`)**:
   - **Ruling: `KEEP` source plate and crop.** Adding the required `9–14 s` title and spoken captions to `S04` and `S05` in `v03` raised `S05`'s master edge density from `0.0498` to `0.0631`, making `S03` (`edge = 0.0475`) the relative 5th-percentile outlier in a cut dominated by high-frequency macro bubble and brick plates (`edge = 0.0631–0.1721`). Full-size visual inspection (`c_7.27.jpg`) confirms a sharp, clean 3D-cartoon close-up of Jan Ingenhousz's hands with period white ruffled cuffs lowering a bright green leaf into a glass jar of water on a sunlit table (`std = 42.19`, `mean = 136.26`, `p95 = 221.0`, `edge = 0.0475`, `edge8 = 0.1681` — nearly `2×` the absolute `polish_gate` low-detail floor of `edge 0.0259` and `3.1×` the `std 13.44` floor, `seams: []`), directly illustrating *"a Dutch doctor called Jan Ingenhousz put fresh leaves in jars of water"* with the sound off.
4. **WARN — `terminal_loop.py` (`status == 'rendered_correspondence' is a sample check and does not establish seamless motion` on `Short_B v02` `0:24` and `Short_C v03` `0:25`)**:
   - **Ruling: `KEEP` for machine-verifiable correspondence; human real-time motion/loop check deferred to Ben's final watch.** Both cuts pass `terminal_loop.py` with `status: "rendered_correspondence"` and `errors: []` (`Short_B v02` `picture` MAE `[0.1107, 0.0768, 0.1409, 0.1725]`, `master` MAE `[6.4096, 1.2814, 6.1479, 1.1654] <= 12.0`; `Short_C v03` `picture` MAE `[0.1693, 0.1165, 0.2003, 0.2457]`, `master` MAE `[6.5904, 1.2789, 6.4001, 1.3067] <= 12.0`). Per Ben's 4 Nov 2026 order (`AGENTS.md` line 466), actual real-time motion/loop and audio perception is Ben's final watch (`watched: false`, `heard: false`).
5. **WARN — `music_gate.json` (`reused: couldn't read saturn_long_vo_v02_LISTEN.wav...`)**:
   - **Ruling: `KEEP` / accepted.** Refers to archived OWB stems not on local disk; `trees006_score_bed_v01.mp3` passes all `music_gate.py` checks (`verdict: PASS`, `fail: []`, `matches: []`).

---

## 4. Final-Watch Handoff (`awaits_ben` & Verified Unique R2 Play Links)

Both durable watch copies and `_PHONE.mp4` proxies are staged in `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/J2169/`, registered in `05_Analytics/kanban/watch_uploads.json` and `~/.config/studio-kanban/watch_uploads.json`, and verified over HTTPS (`302` redirect from `/api/watch` -> `200 OK` from Cloudflare R2):

| Ask ID | Short | Version | Unique Watch ID | iCloud UAT Path (`file`) | Target Slot (`airs`, London) | Watch-By (`due`, London) |
|---|---|---|---|---|---|---|
| `J2263.1` | `Short_B` — *How Do Plants Clean the Air?* | `v02` | `hos-j2263-1-v02` | `HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/J2169/hos006_short_b_v02_PHONE.mp4` | `2026-11-18 11:30` (`2026-11-18T11:30Z`) | `2026-11-15 18:00` (`2026-11-15T18:00Z`) |
| `J2263.2` | `Short_C` — *How Do Plants Make Oxygen?* | `v03` | `hos-j2263-2-v03` | `HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/J2169/hos006_short_c_v03_PHONE.mp4` | `2026-11-21 11:30` (`2026-11-21T11:30Z`) | `2026-11-15 18:00` (`2026-11-15T18:00Z`) |

No upload, schedule, retitle, privacy change, or Buffer action is performed; publishing waits until long `VbPubYd6Fbs` is public, Ben's watch OK is recorded, and Chief authorises scheduling.
