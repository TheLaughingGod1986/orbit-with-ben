# J2717 Condition Verification Review — J0875 (`HOS 007 Shorts cLKDiYP55J8 & xgx2lYHhYZM: set Related -> ETynHpIYLeY`)

- **Verification Job:** `J2717` (`Verify condition for J0875`)
- **Parent Job:** `J0875` (`HOS 007 Shorts cLKDiYP55J8 & 4WUs0beKn0A: set Related -> the 007 long once it is uploaded (before Fri 13 Nov 11:30Z) + HOS Buffer register`, `status: blocked`, `by: gemini`, `for: gemini`, `model: gemini-argon`, `kind: listing`, `repo: hos`, `film: 007`, `stage: upload`, `progress: 3/4`)
- **Verifier:** `gemini` (`Gemini 4 Argon (High)`, specialist worker on the Mac mini; `Grok Bot` / `chief` is currently elected Chief per `chief_relay.py status`)
- **Checked At:** `2026-11-13T10:45:00Z`
- **Verdict:** **CONDITION SATISFIED — REOPEN `J0875` IMMEDIATELY (HOS 007 Vaccine long `ETynHpIYLeY` reads back `public` since `2026-11-12T18:00:36Z` in both live YouTube Data API via `npm run channel:audit` and `05_Analytics/hos/snapshots/2026-11-13.json`; all original gates, Ben approvals, and `social/hos/UPLOADS.json` registrations for live scheduled Shorts `cLKDiYP55J8` [airs `2026-11-13T11:30:00Z`] and `xgx2lYHhYZM` [airs `2026-11-17T11:30:00Z`] remain valid; `£0.00` / `0` credits).**

---

## 1. Recorded Waiting Condition on `J0875`

At `2026-10-25T21:07Z`, `J0875` was parked at step `3/4` (`hold.type = "public"`, `condition = "Vaccine long ETynHpIYLeY must read back Public"`, `check_at = "2026-11-12T19:05:57+00:00"`, `recheck_task = "J2717"`) with:
> `waits for input: HOS 007 long ETynHpIYLeY public (publishAt Thu 12 Nov 2026 18:00Z; Studio picker lists 23 public videos only, 0 matches while Private). HOS Buffer mirror registered for cLKDiYP55J8 (was -I_GHK-GcFs) & 4WUs0beKn0A with long=ETynHpIYLeY (OWB b8507a906) and HOS records updated (HOS 9b715232). Reopen on/after Thu 12 Nov 18:05Z (before Fri 13 Nov 11:30Z).`

Subsequent approved Short swaps updated the targets in `J0875`'s history:
- **`J1219` (`2026-10-29T20:27Z`):** Swapped Fri `13 Nov 2026 11:30Z` slot from `-I_GHK-GcFs` (`v01`, now Private and unscheduled) to Ben-OK'd **`cLKDiYP55J8`** (`hos_007_s04_smallpox_test_v04.mp4`, *What Was the Edward Jenner Experiment?*, `atempo=1.05`, sha256 `3ef3fa77375083622e8f8d6dee99f009cf60cbc27fc01f9d21857ba6b5b0c4e7`, Ben OK `J0966.1` / HOS `#180` `6507268470`).
- **`J1222` (`2026-10-30T00:59Z`) & `J1258` (`2026-10-30`):** Swapped Tue `17 Nov 2026 11:30Z` slot from `4WUs0beKn0A` (`v02`, now Private and unscheduled) to Ben-OK'd **`xgx2lYHhYZM`** (`hos_007_s05_vacca_jesty_v05.mp4`, *Why Is It Called a Vaccine?*, `atempo=1.03`, sha256 `e5ea76f012fb94c54c4a7224140d2d8ca342ea8c02a2fbdb30df17661f94f1ad`, Ben OK `J0966.3` / HOS `#180` `6507831644`), and repointed `SHORTS_UPLOAD_INDEX.json`, `SHORTS_RELEASE.json`, and `social/hos/UPLOADS.json` (HOS PR `#386` `c8fffe52`).

---

## 2. Direct Verification of Public Status, Gates & Approvals (`2026-11-13T10:45:00Z`)

| Requirement | Status | Direct Evidence |
|---|---|---|
| **1. `ETynHpIYLeY` reads back `public`** | **SATISFIED** | - **Live YouTube Data API (`cd 07_Content-Ops && npm run channel:audit` in `History Of Science` at `2026-11-13T10:44:42Z`):**<br>  `PASS  long  ETynHpIYLeY  public  How Was the First Vaccine Made? (And Why It's Named After a Cow)` (`64 videos, 0 errors`).<br>- **Daily YouTube Analytics snapshot (`05_Analytics/hos/snapshots/2026-11-13.json`):**<br>  `"id": "ETynHpIYLeY"`, `"title": "How Was the First Vaccine Made? (And Why It's Named After a Cow)"`, `"publishedAt": "2026-11-12T18:00:36Z"`, `"seconds": 532`, `"format": "long"`, `"privacy": "public"`, `"publishAt": null`.<br>- **Post-launch 6h check (`J2745`) & live listing check (`J2752` / HOS PR `#573` `e6006301`):** Confirmed `ETynHpIYLeY` is public with live end screen (`8:31:02–8:51:02`, Subscribe + `_C92tIJCk8A`), `en-GB` captions, and active 2-arm Title & Thumbnail Test & Compare (`J2536`). |
| **2. Target Shorts `cLKDiYP55J8` & `xgx2lYHhYZM` status and Ben approvals** | **SATISFIED** | - **`cLKDiYP55J8` (*What Was the Edward Jenner Experiment?*, `s04_smallpox_test_v04`):** Reads back `PASS  Short cLKDiYP55J8  private 2026-11-13 11:30 UK` (`publishAt: "2026-11-13T11:30:00Z"`). Ben OK recorded in `J0966.1` (`#180` `6507268470`) and `J1219`. Superseded `-I_GHK-GcFs` remains `private` with `publishAt: null`.<br>- **`xgx2lYHhYZM` (*Why Is It Called a Vaccine?*, `s05_vacca_jesty_v05`):** Reads back `PASS  Short xgx2lYHhYZM  private 2026-11-17 11:30 UK` (`publishAt: "2026-11-17T11:30:00Z"`). Ben OK recorded in `J0966.3` (`#180` `6507831644`) and `J1222`. Superseded `4WUs0beKn0A` remains `private` with `publishAt: null`. |
| **3. HOS Buffer registration & package records** | **SATISFIED** | - `00_Brand/Channel-Setup/social/hos/UPLOADS.json` in `orbit-with-ben` already registers both `cLKDiYP55J8` (`replaces: "-I_GHK-GcFs"`, `publishAt: "2026-11-13T11:30:00Z"`, `long: "ETynHpIYLeY"`) and `xgx2lYHhYZM` (`replaces: "4WUs0beKn0A"`, `publishAt: "2026-11-17T11:30:00Z"`, `long: "ETynHpIYLeY"`), with `-I_GHK-GcFs` and `4WUs0beKn0A` marked `supersededBy` (`Do not Buffer this id`).<br>- Remaining work on `J0875` (step 4 of 4) is setting Studio `Related video` → `ETynHpIYLeY` on `cLKDiYP55J8` and `xgx2lYHhYZM`, reading both back in Studio, and updating `relatedVideoId` in HOS 007 Shorts records (`SHORTS_RELEASE.json`, `SHORTS_UPLOAD_INDEX.json`, manifests, and `production-status.md`). |

---

## 3. Protected Elected-Chief Action (`chief` / Grok Bot)

Because `scripts/jobs.py` (`do_reopen`, lines 948–949) restricts releasing a job with a `hold` to the elected Chief (`ValueError: Only the elected Chief may release a verified hold`), `J2717` is parked for the elected Chief (`chief`) to run:

```bash
python3 scripts/jobs.py reopen J0875 --agent chief \
  --note "J2717 verified (jobs/reviews/J2717/REVIEW.md): HOS 007 long ETynHpIYLeY reads back public since 2026-11-12T18:00:36Z in live YouTube Data API (channel:audit: 64 videos, 0 errors) and 05_Analytics/hos/snapshots/2026-11-13.json. Live scheduled Shorts cLKDiYP55J8 (publishAt 2026-11-13T11:30:00Z, J1219) and xgx2lYHhYZM (publishAt 2026-11-17T11:30:00Z, J1222) are already registered in social/hos/UPLOADS.json with long=ETynHpIYLeY; set Related video -> ETynHpIYLeY on cLKDiYP55J8 and xgx2lYHhYZM in HOS Studio, read both back, and update HOS 007 Shorts records." \
  --git

python3 scripts/jobs.py done J2717 --agent chief --ref jobs/reviews/J2717/REVIEW.md \
  --result "CONDITION SATISFIED (jobs/reviews/J2717/REVIEW.md): HOS 007 long ETynHpIYLeY reads back public since 2026-11-12T18:00:36Z in live YouTube Data API (channel:audit: 64 videos, 0 errors) and 05_Analytics/hos/snapshots/2026-11-13.json; Ben approvals (J0946, J1219, J1222) and social/hos/UPLOADS.json entries for cLKDiYP55J8 & xgx2lYHhYZM verified intact. J0875 reopened to set Studio Related -> ETynHpIYLeY on cLKDiYP55J8 & xgx2lYHhYZM. GBP0." \
  --git
```
