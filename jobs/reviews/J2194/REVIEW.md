# J2194 Review & Scope Decision — HOS 010 (`010_Alvarez-Clay-Line-Dinosaurs`) Missing-Plate Production Scope for `J2172`

- **Review Job**: `J2194` (`HOS 010: decide exact missing-plate production scope for J2172`)
- **Parent / Target Job**: `J2172` (`HOS 010: assemble and gate Shorts A and C on accepted J1894 v02 VO`, `status: blocked` at `1/3`)
- **Evidence Branch / PR Inspected**: HOS PR #424 (`codex/J2172`, commits `8b58cda3` and `ad3c0f4d6c566ccf6d04ba1c77dff5f0751d031a`, all 4 CI checks green)
- **Reviewer**: `gemini` (worker review lane; £0 spend; no final Chief merge or spend authorization)
- **Date**: 2026-11-05
- **Verdict**: **FIX** — `J2172`'s readiness inventory in HOS PR #424 (`ad3c0f4d`) is verified accurate on disk (2 of 14 required plate identities exist as approved `£0` code graphics; **12 of 14 moving long-plate identities are missing** and **no open named `010` picture producer job exists**). In addition, row-level verification against `LEARNINGS.md` Rule 8, `J1004` (Option A1), and `CHANNEL_AUTHORITY.md` (*picture matches the words*) found three pre-mint plan mismatches in `SHORTS_PICTURE_PLAN_v02.json`. A bounded **£0** row-mapping/readiness job is queued now to write `SHORTS_PICTURE_PLAN_v03.json` (and align Part 05 bird row prompts), while `J2172` remains **blocked at 1/3** awaiting that £0 readiness fix and Chief's separate spend/generation authorization for HOS 010 moving plates.

---

## 1. Verification of `J2172` Inventory & HOS PR #424 (`8b58cda3` / `ad3c0f4d`)

### 1.1 Locked Script, Fact & Plan Inputs (`INPUT_RECORDS.json`)
All six canonical inputs in `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/` were re-hashed on disk and match `jobs/evidence/J2172/INPUT_RECORDS.json` byte-for-byte:

| File | Verified SHA-256 | Bytes | Status |
|---|---|---:|---|
| `01_Script/FACT_NOTES_v01.md` | `7f68d4ca62eb3a81e7f63a8495c985be99a26d75ba29771996be77a78e858380` | 20,257 | Locked (`J0224` PASS) |
| `01_Script/HARD_CHECKS.md` | `4cededc1ff2192313507639a2cf831eb01a08df84031066510738b8744bc3c26` | 3,415 | Locked |
| `10_Shorts/SHORTS_SCRIPTS_v02.md` | `d6b9a960341a036c2dc1df9faaf7f09f34b97c52db550b216b2277007c02eb68` | 5,049 | Locked (`J0967` / `J1004`) |
| `10_Shorts/SHORTS_PICTURE_PLAN_v02.json` | `99eafcc928056ac6650934d5f8d04a1b9302620816fb3daab119ad0825343375` | 15,826 | Needs `v03` £0 repair (Section 2) |
| `02_Shot-List/PICTURE_PLAN_v03.json` | `4e3655e43fc24739a6e82ec0b23bb154cf19a91ecdfab8acbfed2601e0ec6aa8` | 120,031 | Priced board (no plates minted) |
| `02_Shot-List/SHOT_LIST_v01.md` | `f48bca560919c89d9b4f85583a22e153bc5c72c5ba8e87801ab7e7b3fcad0ca7` | 25,213 | Locked (`J0224` PASS) |

### 1.2 Accepted `J1894` Voiceover Masters & `J1004` Option A1 Disposition
- **`Short_A` (`hos_010_short_A_v02` — *What Killed the Dinosaurs?*)**:
  - `10_Shorts/vo_v02/hos_010_short_A_v02.mp3`: SHA-256 `68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb` (`24.868s` raw, `23.280s` trimmed speech end, 61 words).
  - `10_Shorts/vo_v02/hos_010_short_A_v02.wav`: SHA-256 `2488aa8b49beb3a642597e08f30ca53e723fbee00cd21ad8bdc581a9293ff228` (`24.869s`).
  - Accepted in `J1894` (05 Nov 2026) and `J1004` (HOS PR #366 `00b1e653`, 28 Oct 2026) under **Option A1**: `-0.260s` pause/onset trim across 6 natural silence windows + `atempo=1.06x` on Sentence 1 only (`0` words changed, `£0` EL spend), landing Sentence 1 (*"This thin line of clay marks the end of the dinosaurs."*) at **`2.849s <= 2.850s`** (`vo_duration_s = 22.289s`, `total_duration_s = 23.289s` with `1.000s` loop tail).
- **`Short_C` (`hos_010_short_C_v02` — *Are Birds Really Dinosaurs?*)**:
  - `10_Shorts/vo_v02/hos_010_short_C_v02.mp3`: SHA-256 `20432ecd645b28e9fdc051578a284cb2845bd09f3040170b192089b256055b87` (`23.797s` raw, `22.560s` trimmed speech end, 64 words).
  - `10_Shorts/vo_v02/hos_010_short_C_v02.wav`: SHA-256 `ca814ab01ad72fde015b4e157638b5e346d592e5df54cefe97e38969340fcb0c` (`23.797s`).
  - Accepted in `J1894` at `1.00x`: Sentence 1 (*"Not all the dinosaurs died."*) ends at **`1.780s <= 2.850s`** (`vo_duration_s = 22.560s`, `total_duration_s = 23.560s` with `1.000s` loop tail).

### 1.3 Existing vs. Missing Plates (`INVENTORY.json` Verified)
Across `Short_A` (9 rows: `S01..S08` + `loop_tail`) and `Short_C` (9 rows: `S01..S08` + `loop_tail`), `SHORTS_PICTURE_PLAN_v02.json` references **14 unique long-plate identities**:

1. **2 Approved `£0` Code Graphics Present on Disk (`07_Edit-Project/code_graphics_v01/`)**:
   - `P4:01_iridium_spike` (`Short_A:S07`): `code_graphic_010_p4_01_iridium_spike.mp4` (`1920x1080`, `30fps`, `17.033s`, SHA-256 `f9b504cf26e927d988a55aea58b4b2173660c2188b0ca94561e2c85479c2fd84`). Visual inspection of `code_graphic_010_p4_01_iridium_spike.jpg` + `picture_qa_v01.txt` (0/13 fails) + `polish_gate_v01.txt` (0/13 fails) confirms clean HOS navy card with gold spike at dark clay band and `ABOUT 30 TIMES` Didot italic header (Chief PASS in `J0348`/`J0383`).
   - `P5:11_why_survive` (`Short_C:S03`): `code_graphic_010_p5_11_why_survive.mp4` (`1920x1080`, `30fps`, `14.400s`, SHA-256 `0e71b03e41d0b16bb92afeb318798f796c06ae9cb78bdb776eba0e4f99940acd`). Visual inspection of `code_graphic_010_p5_11_why_survive.jpg` + `picture_qa_v01.txt` + `polish_gate_v01.txt` confirms three clean medallions (small bird, seed, ground nest with two eggs) under a protective arc with zero text (Chief PASS in `J0348`/`J0383`).
   - *Tooling defect noted*: `00_Brand/Channel-Setup/tools/hos_build_rule_v02.py` (`resolve_plate_path()`) checks only `04_Generated-Clips/part0{N}/raw/v01/` and `07_Edit-Project/stills/`, omitting `07_Edit-Project/code_graphics_v01/`. That is why `SHORTS_PICTURE_PLAN_v02.json` marked `plate_on_disk: false` for these two existing code graphics.

2. **12 Moving Long-Plate Identities Missing (Zero `.mp4` Clips on Mini or NAS; No Open Producer Job in Queue)**:
   - Neither `04_Generated-Clips/` nor `07_Edit-Project/stills/` exists yet in `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/`.
   - Unlike HOS `008` (`J1191` done) and HOS `009` (`J1192` done, `J2026`/`J2033` tranche 2 active), **HOS `010` has no open or blocked picture-mint job in `jobs/queue.json`**.
   - The 12 missing moving plate identities referenced by `SHORTS_PICTURE_PLAN_v02.json` are all `flow-first` **Veo 3.1 Quality** (8 s clips):
     1. `P1:01_clay_line` (`Short_A:S01`, `Short_A:loop_tail`) — Quality, 8s
     2. `P2:01_walter_hammer` (`Short_A:S02`) — Quality, 8s
     3. `P1:08_hand_on_rock` (`Short_A:S03`) — Quality, 8s
     4. `P2:03_tiny_shells` (`Short_A:S04`) — Quality, 8s
     5. `P2:05_almost_none` (`Short_A:S05`) — Quality, 8s
     6. `P3:08_asaro_michel` (`Short_A:S06`) — Quality, 8s
     7. `P4:06_dust_veil` (`Short_A:S08`, `Short_C:S02`) — Quality, 8s
     8. `P5:09_robin` (`Short_C:S01`, `Short_C:S05`, `Short_C:loop_tail`) — Quality, 8s *(requires row-mapping split on `S05`; see Section 2.2)*
     9. `P5:08_all_at_once` (`Short_C:S04`) — Quality, 8s
     10. `P5:13_window_song` (`Short_C:S06`) — Quality, 8s *(mismatches `"the gull at the seaside"`; see Section 2.2)*
     11. `P5:10_explorer_robin` (`Short_C:S07`) — Quality, 8s
     12. `P5:12_clay_callback` (`Short_C:S08`) — Quality, 8s

---

## 2. Rule 8 & Row-Mapping Audit (Fixes Required in Bounded £0 Readiness Job Before Mint/Assembly)

### 2.1 `Short_A` (`hos_010_short_A_v02` — *What Killed the Dinosaurs?*)
1. **Rule 8 Subject & Surprise Check (`<= 2.85s`)**:
   - Sentence 1 (*"This thin line of clay marks the end of the dinosaurs."*) names both the concrete visual anomaly at frame 0 (`"This thin line of clay"`, paired with `P1:01_clay_line` showing a finger resting on the dark clay band between pale limestone layers and frame-0 caption `THE LINE` with `LINE` in `#FFD400`) and the title subject + surprise (`"marks the end of the dinosaurs"`), with zero meta-promise.
   - Under `J1004` Option A1 (`-0.260s` pause/onset trim + `1.06x` on Sentence 1), `"dinosaurs."` finishes at **`2.849s <= 2.850s`** (`PASS`).
2. **Row-Mapping Fix 1 — `Short_A:S01` Mid-Sentence Cut & Option A1 Timestamps**:
   - In `SHORTS_PICTURE_PLAN_v02.json`, `Short_A` was left on pre-`J1004` raw timestamps (`status: "blocked_hook_and_missing_plates"`, `vo_duration_s: 23.28`), cutting `S01` (`P1:01_clay_line`) at **`2.40s`** after `"marks the end of the"` and pushing `"dinosaurs."` onto `S02` (`P2:01_walter_hammer`).
   - In `SHORTS_PICTURE_PLAN_v03.json`, `Short_A` must apply the approved `J1004` Option A1 timing schedule (`vo_duration_s: 22.289`, `total_duration_s: 23.289`) and extend `S01` (`P1:01_clay_line`) across the full first sentence **`0.000–2.849s`** (`use_s: 2.849s`, `cut_reason: "sentence_end_under_2.85s_option_A1"`), starting `S02` (`P2:01_walter_hammer`) at **`2.849s`** on *"It's in a cliff in Italy..."* and shifting `S02..S08` + `loop_tail` to match the Option A1 word timestamps.
3. **Row-Mapping Fix 2 — `Short_A:S07` Double-Label Prevention (*One Label at a Time*)**:
   - `Short_A:S07` uses `code_graphic_010_p4_01_iridium_spike.mp4`, which already renders the Didot italic label `ABOUT 30 TIMES` on screen.
   - `SHORTS_PICTURE_PLAN_v02.json` currently places `teach_overlay` (`DATA: THE IRIDIUM SPIKE`) at `14.2–18.0s`, overlapping `S07`. Under HOS `AGENTS.md` (*one label at a time*), `SHORTS_PICTURE_PLAN_v03.json` must either end `teach_overlay` before `S07` (window `13.6–16.2s` over `S06` `P3:08_asaro_michel` while *"thirty times more iridium"* begins) or rely solely on `S07`'s built-in `ABOUT 30 TIMES` graphic label so two labels never appear simultaneously.

### 2.2 `Short_C` (`hos_010_short_C_v02` — *Are Birds Really Dinosaurs?*)
1. **Rule 8 Subject & Surprise Check (`<= 2.85s`)**:
   - Sentence 1 (*"Not all the dinosaurs died."*, `0.10–1.78s` at `1.00x`) lands at **`1.780s <= 2.850s`**.
   - However, in `part-05_plates_v02/v03.json`, `P5:09_robin`'s prompt reads: *"A morning garden. A pigeon struts, then a robin hops along a fence and turns its head. A faint outline of a small feathered dinosaur fades in over the robin, then out."* If `P5:09_robin` opens on a strutting pigeon before the robin appears, `Short_C:S01` (`0.00–1.88s`) will fail its frame-0 brief (*"Living bird (robin) with a faint dinosaur skeleton overlay fading in and out"*) and weaken the Rule 8 visual bridge between `"dinosaurs"` and `"birds"`.
   - **Fix**: `P5:09_robin` must start immediately on the **robin on the garden fence** at `0.0s` with the faint feathered-dinosaur skeleton outline fading in during `0.3–1.8s` (no pigeon in `P5:09_robin`).
2. **Row-Mapping Fix 3 — `Short_C:S05` & `S06` Robin / Pigeon / Gull Visual-to-Spoken Mismatch & Triple Reuse of `P5:09_robin`**:
   - In `hos_010_short_C_v02` (`stt_raw.json`), the spoken phrases across `10.42–15.78s` (`5.36s`) are:
     - `10.90–12.16s`: *"the pigeon on the pavement,"*
     - `12.60–13.80s`: *"the robin in the garden,"*
     - `14.22–15.78s`: *"the gull at the seaside."*
   - Because `hos_build_rule_v02.py` enforces `body_cut_s` in **`[2.50, 3.80] s`** and `word_end_gap_s_max <= 0.10s`, `13.06s` (immediately after `"robin"`) is the **only** word end between `10.42s` and `15.78s` where both cuts (`S05 = 10.42–13.06s = 2.64s` and `S06 = 13.06–15.78s = 2.72s`) satisfy `[2.50, 3.80] s` (`12.16 - 10.42 = 1.74s < 2.50s`; `15.78 - 13.80 = 1.98s < 2.50s`).
   - In `SHORTS_PICTURE_PLAN_v02.json`:
     - `S05` (`10.42–13.06s`: *"the pigeon on the pavement, the robin"*) is mapped to `P5:09_robin` — the **exact same 8.0s plate** already mapped to `S01` (`0.00–1.88s`) and `loop_tail` (`22.56–23.56s`). That creates a **3-stretch reuse** of an 8.0s plate (violating `picture_qa.py`'s non-overlapping / 10s-reuse rule) and shows a garden robin while the narrator says *"the pigeon on the pavement"*.
     - `S06` (`13.06–15.78s`: *"in the garden, the gull at the seaside."*) is mapped to `P5:13_window_song` (*"A bird sings on a branch outside a window. Soft morning light."*), which shows neither a garden robin nor a seaside gull, violating `CHANNEL_AUTHORITY.md` (*picture matches the words*).
   - **Exact Fix for `SHORTS_PICTURE_PLAN_v03.json` and `part-05_plates_v04.json`**:
     - **`S01` (`0.00–1.88s`) and `loop_tail` (`22.56–23.56s`)**: Keep on `P5:09_robin` (`8.0s` Quality: robin hopping on a morning garden fence with faint feathered-dinosaur skeleton outline fading in/out; used only once in body + 1.0s loop tail).
     - **`S05` (`10.42–13.06s`: *"the pigeon on the pavement, the robin"*)**: Map to a dedicated plate **`P5:09a_pigeon_pavement`** (restoring `SHOT_LIST_v01.md` Part 05 Row 10 `pigeon`: *"A pigeon struts along a stone pavement beside a low garden wall where a robin perches on the fence; morning light"*, `8.0s` Fast or Quality). In the long edit, `P5:09a_pigeon_pavement` (`1.9s`) + `P5:09_robin` (`2.0s`) also cleanly cover the long VO line *"The pigeon on the pavement. The robin in the garden."* (`3.90s`).
     - **`S06` (`13.06–15.78s`: *"in the garden, the gull at the seaside."*)**: Map to a dedicated Shorts/cutaway plate **`P5:13a_gull_seaside`** (or update `P5:13` if shared: *"From a coastal garden fence overlooking the sea, a white-and-grey gull wheels over sunlit chalk cliffs and breaking waves at the seaside"*, `8.0s` Fast or Quality) so the picture matches both halves of `"in the garden, the gull at the seaside."`

### 2.3 Obsolete Promoted-Title Metadata & Code-Graphic Path Resolution
- Remove obsolete `"promoted_long_title": "What Killed the Dinosaurs Was Hidden in a Line of Clay"` and `"promoted_long_title_window_s": [9.0, 14.0]` from both `Short_A` and `Short_C` in `SHORTS_PICTURE_PLAN_v03.json` (`full_film_banner` is already `false` per `J0967` / `J1004`).
- Update `hos_build_rule_v02.py` (`resolve_plate_path()`) or `SHORTS_PICTURE_PLAN_v03.json` so `P4:01_iridium_spike` (`07_Edit-Project/code_graphics_v01/code_graphic_010_p4_01_iridium_spike.mp4`) and `P5:11_why_survive` (`07_Edit-Project/code_graphics_v01/code_graphic_010_p5_11_why_survive.mp4`) resolve as `plate_on_disk: true`.

---

## 3. Bounded Production Scope & Queue Disposition

### Step A — Queued Now (`£0`, No Spend, Worker Executable)
- **New Job Queued (`J2210`)**: Bounded `£0` HOS 010 readiness & row-mapping repair job (`repo: hos`, `film: 010`, `stage: picture`, `needs: mini`, `kind: video`) to:
  1. Write `10_Shorts/SHORTS_PICTURE_PLAN_v03.json` applying `J1004` Option A1 timestamps to `Short_A` (`S01 = 0.000–2.849s` on `P1:01_clay_line`, shifting `S02..S08` + `loop_tail` to `23.289s` total, non-overlapping `teach_overlay`), mapping `Short_C:S05` (`10.42–13.06s`) to `P5:09a_pigeon_pavement` and `Short_C:S06` (`13.06–15.78s`) to `P5:13a_gull_seaside` while keeping `P5:09_robin` strictly on `S01` + `loop_tail`, removing obsolete `promoted_long_title*` fields, and resolving `code_graphics_v01` paths (`P4:01_iridium_spike`, `P5:11_why_survive`) as `plate_on_disk: true`.
  2. Update `07_Edit-Project/parts/part-05_plates_v04.json` / `02_Shot-List/PICTURE_PLAN_v04.json` (`£0` JSON/board update only) so `P5:09_robin` starts on the robin + skeleton outline at frame 0 and `P5:09a_pigeon_pavement` + `P5:13a_gull_seaside` are explicitly defined with prompts, models, and credit budgets.
  3. Run `00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs` and open a clean HOS PR for Chief review.

### Step B — Reserved for Chief's Separate Spend & Merge Authorization (`£0` Spent Here)
1. **HOS PR #424 Merge (`codex/J2172`, `ad3c0f4d`)**:
   - Verified clean and CI-green (`no-desk-close`, `no-media`, `check`, `reopen-desk` all pass). Ready for **Chief merge**.
2. **Chief Spend / Mint Authorization Scope for HOS 010 Moving Plates**:
   - **No generation or Flow/Vertex spend is authorized by this worker review.**
   - When Flow capacity opens after HOS `009` tranche 2 (`J2026`/`J2033`) and Step A (`SHORTS_PICTURE_PLAN_v03.json` + `PICTURE_PLAN_v04.json`) is merged, Chief can authorize one of two bounded Flow mint scopes (keeping `>= 3,000` Flow credit buffer, max 3 takes/row, named producer + `claude` reviewer):
     - **Option 1 — Shorts-First 13-Moving-Plate Tranche** (to unblock `J2172` earliest):
       - **11 Quality plates** (`P1:01_clay_line`, `P2:01_walter_hammer`, `P1:08_hand_on_rock`, `P2:03_tiny_shells`, `P2:05_almost_none`, `P3:08_asaro_michel`, `P4:06_dust_veil`, `P5:09_robin`, `P5:08_all_at_once`, `P5:10_explorer_robin`, `P5:12_clay_callback` = `1,100` try-1 / `2,849` expected Flow credits) + **2 Fast environmental bird plates** (`P5:09a_pigeon_pavement`, `P5:13a_gull_seaside` = `20` try-1 / `40` expected Flow credits; or `200` try-1 / `518` expected if Quality) = **`1,120–1,300` try-1 / `2,889–3,367` expected Flow credits**.
     - **Option 2 — Full HOS 010 Long + Shorts Picture Mint (`PICTURE_PLAN_v04`)**:
       - Because HOS `010` long (`air: 2026-12-03`) must be Public before `Short_A` (`2026-12-04`) and `Short_C` (`2026-12-07`) air, minting the full `010` board (`47 Quality + 13 Fast = 60 Flow plates`, **`4,830` try-1 / `12,433` expected Flow credits**) in part-by-part tranches (`Part 01–02` + `Part 03–05`, starting with the 13 Shorts-parent plates) covers both the 3 Dec long and `J2172`.
3. **`J2172` Hold State**:
   - `J2172` stays **blocked at `1/3`** (`status: blocked`), with its `remaining_action` updated to wait on the new `£0` `SHORTS_PICTURE_PLAN_v03` repair job and Chief's separate HOS 010 moving-plate mint authorization.
