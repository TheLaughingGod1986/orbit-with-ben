# Condition Verification — J3631 (Parent: J3434, WW2:006 De Havilland Mosquito)

- **Verifier:** `macbook-2` (read-only verification lane, `kind: review`; ordinary worker — not elected Chief)
- **Verified at:** `2026-11-24T22:03Z`
- **Parent job:** `J3434` (`WW2:006 edit`, `kind: assembly`, `status: blocked`, `by: gemini`, `due: 2026-12-02T20:00:00Z`, `air: 2026-12-05T17:00:00Z`)
- **Predecessor:** `J3433` (`done`, accepted by Claude under `ww2-channel` Rule 1 PR #59 at `49.98%` real archive)
- **Studio thread read to:** `#7145554901` (issue `#954`)
- **Verdict:** **CONDITION UNMET — KEEP `J3434` BLOCKED (DO NOT REOPEN `J3434`); PARKED FOR ELECTED CHIEF**

---

## 1. Why `J3434` Must Stay Blocked (Not Reopened)

`J3434`'s worker assembly work (steps 1–5 of 5) was already completed by `gemini` at `2026-11-24T21:35Z` and opened in `ww2-channel` **PR #107** (`gemini/J3434-mosquito-assembly`, commit `a251f00359611ce0c0c5ea703c54707051e348da`). The relay automatically queued `J3631` because `J3434` had `"after": "J3433"` (`done`) and was blocked without a structured hold.

Reopening `J3434` (`kind: assembly`) would re-dispatch an already-rendered assembly job to a worker. Instead, the **actual unmet conditions** blocking completion of `J3434` are:

1. **Elected Chief review & merge of `ww2-channel` PR #107** (`OPEN`, `MERGEABLE`, `CLEAN`, `0` reviews, `0` comments):
   - Confirm Rule-2 searched-name title (`De Havilland Mosquito: Why It Was Made of Wood`, 46 chars, matching `J3562` / open PR #98).
   - Reconcile `006/status.json` `picture` stage (still `"doing"` on both `main` and PR #107 despite `J3433` `done`) and coordinate merge ordering with open `ww2-channel` PR #98 (`J3562`), which also edits `006/status.json`.
2. **Full private audiovisual watch-through gate (`J3434` step 6):**
   - `J3434` step 6 requires *"Run the studio's QA gates and a full watch-through"*.
   - `HANDOFF_J3434_v01.md` and `RENDER_QA_v01.json` record only a **3-clip perceptual spot-check** (`0:00–0:45`, `1:45–2:20`, `16:40–17:15` = `115 s` / `7.5%` of the `1,542.83 s` master), deferring full watch-through to Ben.
   - Under the same-day `J3560` / `J3624` / `J3625` precedent on `WW2:004`, the elected Chief should decide whether to queue a dedicated full private audiovisual QA job (`kind: qa`, full end-to-end watch/listen with demonstrated `audio_input` and `moving_video_input`) before merging PR #107 and staging Ben's watch, or explicitly rule on sufficiency.
3. **Ben's watch not yet staged:**
   - The verified master `ww2_006_mosquito_v01.mp4` is **not** present in `WW2 UAT/` (which currently contains only `001` and `002`), and `J3434` has no `awaits_ben` entry set.
   - Original Ben approvals and schedule remain valid: **air `Sat 5 Dec 17:00` London**, **Ben's watch due `2026-12-02 20:00` UTC** (Ben 23 Nov build approval + 24 Nov three-a-week & fill Sat 28 Nov calendar updates).

---

## 2. Independent Evidence Verified (2026-11-24 21:58Z–22:03Z)

### A. `ww2-channel` PR #107 (`a251f00359611ce0c0c5ea703c54707051e348da`)
- **PR state:** `OPEN`, base `main`, head `gemini/J3434-mosquito-assembly`, `MERGEABLE`, `mergeStateStatus: CLEAN`, `0` reviews, `0` comments, `17` files (`+6,788` / `-6`).
- **Stage preservation:** Preserves all 7 `status.json` stages (`topic`, `script`, `sources`, `vo`, `shots`, `picture`, `edit`) with no dropped prior history.
- **Public-repo hygiene:** Independent diff scan found `0` email addresses, `0` private network addresses, and `0` personal home-directory paths.

### B. NAS Media & SHA-256 Verification (Read-Only)
All 7 delivered NAS artefacts exist under `/Volumes/data/studio-live/ww2/02_Video-Projects/006_De-Havilland-Mosquito-Plywood-Balsa-Bomber/` and match PR #107 recorded hashes exactly:

| File | Verified SHA-256 | Match |
|---|---|---|
| `07_Edit/v01_master/ww2_006_mosquito_v01.mp4` (`151,601,744` B) | `7561d4958875e3edc8464563281bc84134b7f4012f0ea04a8c5e93cee53cb993` | Exact |
| `05_Music/mosquito_score_v01.wav` | `9d8bb4442734c18c8119a2e824e27f7a1ff5db11e6962ef05945ec42740807df` | Exact |
| `10_Thumbnail/thumbnail_comparison_v01.jpg` | `1725bf044e63fea97213c19fdf4219f2823b6a73801457f17070bebfd66669d9` | Exact |
| `10_Thumbnail/ww2_006_thumb_A_v01.jpg` | `5c1ccc1563ac1e045a2e76ffea6748acc1d3474b573aaf7e33a2e09a21371a8f` | Exact |
| `10_Thumbnail/ww2_006_thumb_B_v01.jpg` | `59c5b9acc2e584afa02a511579839b2928eb47edfe0729dae50b60c8c0094f30` | Exact |
| `10_Thumbnail/ww2_006_thumb_C_v01.jpg` | `d4ead8d61b23770b9587136f0dcb2c825ccdd4ea7b90908bbbf34f46013ce88c` | Exact |
| `07_Edit/v01_master/qa_contact_sheet_v01.jpg` | `2787305dfe36dbed59721e97e0d7c100c29c1a05a819c3fbdafebe00ab00aa0a` | Exact |

- **Independent `ffprobe` on master:** `h264` `1920x1080` `24/1` fps, `37,028` frames, `1542.832357 s`; `aac` `48000 Hz` stereo, `72,321` frames, `1542.826667 s` (`0.0057 s` A/V diff); `151,601,744` bytes.
- **Recorded audio checks (`MIX_TECHNICAL_CHECK_v01.json` / `RENDER_QA_v01.json`):** final mux `-15.3 LUFS`, `LRA 4.0 LU`, `-1.3 dBTP`, score `20.0 LU` below VO, `0` full-decode errors.

### C. Cut Plan, Provenance, Captions & Packaging Checks
- **`EDIT_PLAN_v01.json` (independently recomputed):** `146` segments (`102` archive, `19` bespoke, `19` diagram, `6` chapter cards); `825.788 s / 1542.828 s = 53.52%` real archive across `62` distinct official photos (`>= 50%` Rule 1); `0` excluded photos (`CH 719`, `C 5284`, `CH 10111`, `TR 930`) in film body; `62/62` used photo IDs verified present in `03_Picture/ARCHIVE_PROVENANCE.md`.
- **Captions (`11_Upload-Package/ww2_006_en-GB_v01.srt`):** `376` cues, strictly monotonic (`0` index skips, `0` overlaps, `0` invalid durations, `max_end = 1542.720 s`), `0` US-spelling hits across 33 checked US-English forms.
- **Thumbnails (`thumbnail_comparison_v01.jpg`, visually inspected):** 3 single-subject Rule-2 designs at `168 px` and `320 px` on white and dark backgrounds — A (`CH 12416`, 0 words), B (`TR 930`, `PLYWOOD BOMBER`), C (`TR 1090`, `NO GUNS`); clear at 168 px; Rule-13 ad-safe (no Nazi insignia or gore).
- **Upload package (`metadata_v01.json`, `DESCRIPTION_v01.txt`, `PINNED_COMMENT_v01.txt`):**
  - Title: `De Havilland Mosquito: Why It Was Made of Wood` (`46` chars `<= 50`, Rule-2 searched-name-first, matches `J3562` PR #98).
  - 7 chapters starting at `00:00`, `Sources:` block, 62-photo + `TR 930` archive credits, AI-voice & diagram disclosure, pinned question comment, verified public series playlist `PLPPi-oWEDYtA` (`studio/channel.json`), `upload_authorized: false`.

### D. Minor Findings Flagged for Chief & QA Review
1. **Copy typo on diagram `G00B` (verified on clean extracted frame `00:25`, reused at `18:40`):** The middle timeline header reads **`16:00 PM`** (mixing 24-hour clock with `PM`; should be `16:00` or `4:00 PM` if patched). Verified that yellow timestamp boxes appear only on `qa_contact_sheet_v01.jpg` and are **not** burned into the master video.
2. **Long diagram segment durations to evaluate during full audiovisual QA:** `G5` (`S22_01_G5`, `33.0 s`), `G3` (`S13_01_G3`, `28.042 s`), `G18` (`S21_01_G18`, `20.458 s`), `G15` (`S16_02_G15`, `20.208 s`), `G06V2` (`S23_02_G06V2`, `19.292 s`).
3. **Bespoke diagram scratch paths in `EDIT_PLAN_v01.json`:** Bespoke PNGs point to `/Volumes/MiniWork/scratch/J3434-package-v01/bespoke_diagrams/...` (Mini local scratch rather than NAS `studio-live`); harmless for the already-rendered master, but worth noting if a re-render is ever requested on another host.
4. **`006/status.json` `picture` stage:** Still `"doing"` on both `main` and PR #107 even though `J3433` is `done`; Chief may set it to `"done"` on merge (and coordinate with PR #98).

---

## 3. Recommended Actions for the Elected Chief

Because `macbook-2` is an ordinary worker (not the elected Chief; `chief_relay.py status` shows `Chief: Claude`), `scripts/jobs.py` (`set_wait`, lines 591 & 610–611) restricts `jobs.py wait ... --recheck J3631` to the elected Chief. `J3631` is therefore parked for the elected Chief to:

1. **Merge this verification PR** (records `jobs/reviews/J3631/REVIEW.md`).
2. **Record the structured hold on `J3434`** (keeping `J3434` blocked; do not reopen `J3434`):
   ```bash
   python3 scripts/jobs.py wait J3434 --agent <chief-id> \
     --condition "WW2:006 v01 master rendered on NAS (sha256 7561d495...) and ww2 PR #107 open/CLEAN; awaiting Chief decision on full private audiovisual QA (J3434 step 6 / J3560-J3624 precedent; only 3-clip 115s spot-check done; minor 16:00 PM typo on G00B), Chief merge of PR #107 (confirm Rule-2 title + status.json picture=done), and verified WW2 UAT staging + jobs.py awaits (watch due 2026-12-02T20:00Z, air Sat 5 Dec 17:00 London)." \
     --check-at "2026-11-25T12:00:00Z" --type input --recheck J3631 \
     --action "Chief decision on WW2:006 full audiovisual QA, merge of ww2 PR #107, and Ben watch staging (due 2026-12-02 20:00 UTC)" --git
   ```
3. **Decide next step for `WW2:006`:**
   - Either queue a full private audiovisual QA job (`kind: qa`, mirroring `J3624`) followed by a `kind: chief` merge & Ben-watch staging job (mirroring `J3625`), **or** if accepting the delivered `v01` master as-is under `AGENTS.md`, review & merge `ww2-channel` PR #107, copy the verified master to `WW2 UAT`, and arm `jobs.py awaits` (`due 2026-12-02 20:00`).
4. **Close `J3631`** with `jobs.py done J3631 --agent <chief-id> --result "..." --git`.

**Guards honoured:** `£0` spent; zero uploads, schedule/privacy/Studio changes, PR merges, or NAS modifications.
