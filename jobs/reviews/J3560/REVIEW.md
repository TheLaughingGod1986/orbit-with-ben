# J3560 — Condition Verification Review for J3430 (`WW2:004` v01 Assembly & Ben's Watch)

- **Verification Job:** `J3560` (`Verify condition for J3430`, `recheck_of: J3430`, `repo: owb`, `kind: review`)
- **Parent Job:** `J3430` (`WW2 film 004: edit, captions, three thumbnails and upload package, to Ben's watch`, `repo: ww2`, `film: WW2:004`, `stage: edit`, `kind: assembly`, `status: blocked`, `by: gemini`, `due: 2026-11-28T20:00:00Z`, planned air `Tue 1 Dec 17:00 London`)
- **Verifier:** `macbook` (MacBook specialist worker; **not** elected Chief — `chief_relay.py status` at `2026-11-24T16:22Z` shows **`Chief: Codex`** UP/ready, `gemini` UP/ready, `claude` down / no heartbeat, `chief` Grok Bot down)
- **Checked At:** `2026-11-24T16:22Z`–`2026-11-24T16:27Z`
- **Advisory Verdict (Parked for Elected Chief `codex`):** **CONDITION NOT MET — RECOMMEND ELECTED CHIEF KEEP `J3430` BLOCKED (do not reopen as an ordinary assembly job) UNTIL CHIEF REVIEW, `ww2-channel` PR `#94` MERGE-CONFLICT / `status.json` RECONCILIATION, PR `#60` CLEANUP, AND BEN-WATCH STAGING ARE COMPLETED.**
  - **Why `J3560` was queued:** `J3430` still carried `"after": "J3429"` (`done` by `claude` on `2026-11-24T09:09Z`). When `gemini` completed steps 1–3 of 4 and ran `jobs.py block J3430 --reason "parked for Chief: ..."` at `2026-11-24T16:20Z`, `reconcile_holds` created the generic `dependency` hold (`"Required predecessor is complete; verify remaining gates and approvals"`) and queued `J3560`.
  - **Technical assembly deliverables PASS independent verification:** All 7 NAS artifacts (`ww2_004_torpedoes_v01.mp4`, `torpedoes_score_v01.wav`, 3 thumbnails, thumbnail comparison sheet, 24-frame QA contact sheet) match their reported SHA-256 hashes byte-for-byte; `ffprobe` confirms `1920x1080` `24/1` fps `32,576` frames `1357.333 s` video + `48 kHz` stereo AAC `1357.333 s` audio (`0.0 s` sync diff); `EDIT_PLAN_v01.json` confirms `685.794 s` (`50.53%`) real archive across `50` unique verified public-domain photos (`>= 50%` per `ww2-channel` Rule 1, PR `#59`); visual inspection of `thumbnail_comparison_v02.jpg` and `qa_contact_sheet_v01.jpg` passes Rules 2 & 13; title (`49` chars), 6 shifted chapters, `Sources:`, grouped 50-photo credits, AI-voice disclosure, and `upload_authorized: false` all verify.
  - **Remaining gates are NOT yet met:**
    1. **Protected Chief review & PASS pending:** Elected Chief (`codex`) has not yet reviewed/accepted PR `#94`, merged it, reconciled/closed superseded PR `#60`, or staged Ben's watch.
    2. **Three merge conflicts between `ww2-channel` PR `#94` (`gemini/J3430-assembly`, `a3c6a03`) and `origin/main` (`dcf54e7`), including a critical `status.json` regression:**
       - `02_Video-Projects/004_Why-US-Submarine-Torpedoes-Failed-21-Months/status.json` (`CONFLICT (content)` — **CRITICAL**): PR `#94` branched from PR `#60` (`2bff1c0`) before PR `#56` (`db4830f`) and PR `#19` (`ea7eb26`) merged to `main`, so PR `#94`'s `status.json` **drops 6 stages** (`topic`, `script`, `sources`, `vo`, `shots`, `picture`) and keeps only `edit`. Must be reconciled against `origin/main` (preserving all 7 stages and marking `picture` `done` per `J3429`) before merge.
       - `03_Picture/ARCHIVE_PROVENANCE.md` (`CONFLICT (add/add)`): `origin/main` has the older 28-line file (PR `#13`); PR `#94` has the expanded 668-line 50-photo provenance file (`J3429` / PR `#49`) — keep PR `#94`'s 668-line version.
       - `03_Picture/HARVEST_LEDGER.md` (`CONFLICT (add/add)`): identical content except 1 trailing blank line (`origin/main` 99 lines vs PR `#94` 98 lines).
    3. **Ben's watch not yet staged:** `WW2 UAT/` currently has only `00_Channel-Kit`, `001_*`, and `002_*` (no `004_*` copy staged), and `jobs.py awaits` has not been set on `J3430` (watch due `2026-11-28T20:00:00Z`).
    4. **Two minor text-only items to clean up during PR `#94` reconciliation (no re-render needed):**
       - `11_Upload-Package/ww2_004_en-GB_v01.srt` (`355` cues, `0` timestamp errors, last cue ends `1357.210 s`) contains 1 US-spelling slip: `traveling` (UK `travelling`; the 4 `Pearl Harbor` hits are proper noun and fine).
       - `07_Edit/HANDOFF_J3430_v01.md` line 22 (carried from PR `#60`) contains a local Mini home-directory path (`<home>/_desk/logs/J3430-offload.log`); replace with `~/_desk/logs/J3430-offload.log` before merging to the public repo.
  - **Why `J3560` is parked for Chief instead of executed directly:** Under `scripts/jobs.py:603–604` (`set_wait` with `--recheck`) and `scripts/jobs.py:1094–1095` (`do_reopen` on a hold), only the elected Chief (`codex`) may record a condition check or release a hold, and `scripts/jobs.py:1595–1598` requires `J3430` to record `last_recheck == J3560` (or be reopened) before `jobs.py done J3560`.

---

## 1. Direct Verification Evidence (`2026-11-24T16:22Z`–`16:27Z`)

| Check | Status | Direct Evidence Verified |
|---|---|---|
| **1. Predecessor `J3429` & Rule 1** | **COMPLETE** | `J3429` marked `done` by `claude` at `2026-11-24T09:09Z`. `ww2-channel` `studio/RULES.md` Rule 1 (updated 24 Nov, PR `#59` `124d687`, `LEARNINGS #8`) sets real archive photographs at `>= 50%` screen time (two-thirds aim; never held for the last stretch). |
| **2. NAS Master & Audio Specs** | **VERIFIED** | `/Volumes/data/studio-live/ww2/02_Video-Projects/004_Why-US-Submarine-Torpedoes-Failed-21-Months/07_Edit/v01_master/ww2_004_torpedoes_v01.mp4`: `186,537,599` B, SHA-256 `d2656fea86b93c4b7978817153b46167934314e4e99307b59e47e33111ae03fc` (exact match). `ffprobe`: `1920x1080`, H.264 High (`yuv420p`), `24/1` fps, `32,576` frames, `1357.333333 s`; AAC LC `48000 Hz` stereo `1357.333333 s` (`0.0 s` sync diff). `RENDER_QA_v01.json` logs `-15.8 LUFS`, `4.7 LU` LRA, `-1.5 dBTP`, `0` full-decode errors. Zero-spend additive-synthesis bed `05_Music/torpedoes_score_v01.wav` matches SHA-256 `b65cf32b17e74bf4d7ac9527215d220e801b5ce3ea09bdc604cd9ae7770eaff9` (`£0`, logged in `SCORE_MANIFEST_v01.json`). |
| **3. Cut Plan & Archive Coverage** | **PASS (`50.53%`)** | Independent parse of `07_Edit/EDIT_PLAN_v01.json` on `origin/gemini/J3430-assembly`: `157` segments totalling `1,357.334 s` (`18` segments in first `2:00`, opening on archive `N01` and `N07`). Breakdown: `archive` `685.794 s` (`50.53%`, `50` unique verified US federal public-domain photo IDs), `diagram` `638.874 s` (`47.07%`), `source_scan` `24.666 s` (`1.82%`), `card` `8.000 s` (`0.59%`). All 12 `J3447`-audited paragraphs preserved. |
| **4. Thumbnails & QA Sheet (Visual + SHA-256)** | **PASS (STILLS)** | Independent SHA-256 matches on all 5 NAS JPEGs: `ww2_004_thumb_A_v02.jpg` (`799b0880...`), `B` (`8fa6cc77...`), `C` (`258a1b73...`), `thumbnail_comparison_v02.jpg` (`9a94f19b...`), `qa_contact_sheet_v01.jpg` (`f7a0398c...`). Visual inspection confirms Rule 2 (one archive subject filling the `168 px` frame, normal/bright grade, 2 legible words on solid dark band: `PERFECT HIT`, `NO EXPLOSION`, `FAILED WEAPON`) and Rule 13 (no Nazi insignia/gore). `qa_contact_sheet_v01.jpg` shows clean archive framing, captions/IDs, consistent navy/gold diagrams, zero black/corrupted frames. No audio or moving-video perception claimed (Ben's watch provides perceptual check). |
| **5. Upload Package, Captions & Privacy** | **PASS w/ 2 MINOR NOTES** | `metadata_v01.json` / `DESCRIPTION_v01.txt`: title `Why America's Torpedoes Failed Even When They Hit` (`49` chars `<= 50`), previous title preserved, `6` shifted chapters (`00:00`–`18:24`), `Sources:`, grouped credits for all `50` photos, AI-voice disclosure, `altered_content_disclosure: true`, `made_for_kids: false`, `upload_authorized: false`, `planned_air_date: 2026-12-01T17:00:00Z`, `ben_watch_due: 2026-11-28T20:00:00Z`, playlist `PLPPi-oWEDYtA`. `ww2_004_en-GB_v01.srt`: `355` cues, `0` monotonic timestamp errors (ends `1357.210 s`), 1 minor US-spelling slip (`traveling` -> `travelling`). Privacy scan across all 51 files in PR `#94`: `0` emails, `0` private-network IPs; 1 local home-directory path in `07_Edit/HANDOFF_J3430_v01.md` line 22 should be normalised to `~/_desk/logs/J3430-offload.log`. |
| **6. `ww2-channel` PR `#94` Mergeability & PR `#60`** | **BLOCKED (3 CONFLICTS)** | `git merge-tree --write-tree origin/main origin/gemini/J3430-assembly` reports 3 conflicts against `origin/main` (`dcf54e7`): `status.json` (**CRITICAL**: drops `topic`, `script`, `sources`, `vo`, `shots`, `picture` stages from `main`), `03_Picture/ARCHIVE_PROVENANCE.md` (add/add: 28 vs 668 lines — keep PR `#94`), `03_Picture/HARVEST_LEDGER.md` (add/add: 1 trailing blank line). Superseded draft PR `#60` (`codex/J3430`) remains `OPEN`. |
| **7. Ben's Watch (`WW2 UAT/` & `awaits`)** | **NOT STAGED** | `WW2 UAT/` holds only `00_Channel-Kit`, `001_*`, and `002_*` (no `004_*` cut copied yet); `J3430` has no `awaits_ben` entry yet (due `2026-11-28T20:00:00Z`). |

---

## 2. Guardrails & Approvals Check

- Ben's build approval (23 Nov) and updated three-a-week schedule (24 Nov: air `Tue 1 Dec 17:00 London`, Ben's watch due `2026-11-28T20:00:00Z`) remain valid and intact.
- `£0` spend, `0` credits; no upload, schedule change, privacy change, YouTube/Studio mutation, merge, or Chief PASS executed in `J3560`.

---

## 3. Recommended Action for Elected Chief (`codex`)

1. **Review & merge this verification record PR** (`jobs/reviews/J3560/REVIEW.md`).
2. **Reconcile `ww2-channel` PR `#94` against `origin/main`** (keeping all 7 stages in `status.json` with `picture: done` and `edit` updated, keeping PR `#94`'s 668-line `ARCHIVE_PROVENANCE.md`, resolving `HARVEST_LEDGER.md`, fixing `traveling` -> `travelling` in `ww2_004_en-GB_v01.srt`, and normalising line 22 of `HANDOFF_J3430_v01.md`), merge PR `#94`, and close superseded PR `#60`.
3. **Stage `ww2_004_torpedoes_v01.mp4` into `WW2 UAT/`** (SHA-256 verified) and set `jobs.py awaits J3430` (due `2026-11-28T20:00:00Z`, air `2026-12-01T17:00:00Z`), OR keep `J3430` held while resolving PR `#94` with:

```bash
python3 scripts/jobs.py wait J3430 --agent codex --type input --recheck J3560 \
  --condition "Chief (codex) to resolve 3 merge conflicts on ww2-channel PR #94 (preserve all 7 stages in status.json, keep 668-line ARCHIVE_PROVENANCE.md, resolve HARVEST_LEDGER.md, fix 'traveling' in en-GB SRT and local path in HANDOFF_J3430_v01.md), merge PR #94, close superseded PR #60, copy verified v01 master (sha256 d2656fea...) to WW2 UAT, and set Ben's watch (due 2026-11-28T20:00:00Z)." \
  --check-at "2026-11-25T10:00:00Z" \
  --action "Chief (codex) resolve PR #94 conflicts/status.json, merge, close PR #60, and stage WW2:004 v01 on Ben's watch" \
  --git

python3 scripts/jobs.py done J3560 --agent codex \
  --result "Verified J3430 deliverables on NAS (all 7 SHA-256 hashes & ffprobe specs match, 50.53% archive across 50 photos, 3 Rule-2 thumbnails pass). Condition NOT MET pending Chief resolution of 3 PR #94 merge conflicts (incl. dropped status.json stages), PR #60 close, and Ben-watch staging; J3430 input hold recorded via --recheck J3560." \
  --git
```
