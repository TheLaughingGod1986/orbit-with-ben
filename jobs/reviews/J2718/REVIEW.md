# J2718 Condition Verification Review — J0960 (`HOS 007 ETynHpIYLeY pinned comment once public`)

- **Verification Job:** `J2718` (`Verify condition for J0960`)
- **Parent Job:** `J0960` (`HOS 007 ETynHpIYLeY pinned comment once public`, `status: blocked`, `by: cursor`, `kind: studio`, `repo: hos`, `needs: mini`)
- **Verifier:** `gemini` (`Gemini 4 Argon (High)`, specialist worker on the Mac mini; `Grok Bot` / `chief` is currently elected Chief per `chief_relay.py status`)
- **Checked At:** `2026-11-13T10:58:41Z`
- **Verdict:** **CONDITION SATISFIED — REOPEN `J0960` IMMEDIATELY (HOS 007 Vaccine long `ETynHpIYLeY` reads back `public` since `2026-11-12T18:00:36Z` in both live YouTube Data API via `npm run channel:audit` / `videos.list` and `05_Analytics/hos/snapshots/2026-11-13.json`; `commentThreads.list` returns HTTP `200` with `0` existing comments; `PINNED_COMMENTS.json` has `0` entries for `ETynHpIYLeY`; `update-pinned-comment.ts --create --dry-run` builds the exact required comment text with no links, no `/go/` link, and no subscriber count; all original gates and Ben approvals [`J0946`, `J0959`, `J2536`] remain valid; `£0.00` / `0` credits).**

---

## 1. Recorded Waiting Condition on `J0960`

At `2026-10-25T21:16Z`, `J0960` was added and blocked after `J0959` (`Studio finish on ETynHpIYLeY`) set the end screen and Title & Thumbnail Test & Compare (`hold.type = "public"`, `condition = "Vaccine long ETynHpIYLeY must read back Public before posting its pinned comment"`, `check_at = "2026-11-12T19:05:57+00:00"`, `recheck_task = "J2718"`):
> `waits for input: HOS 007 long ETynHpIYLeY public (publishAt Thu 12 Nov 2026 18:00 London). Reopen on/after Thu 12 Nov 18:05 London, post the pinned comment, pin it, and read it back. Do not change the schedule.`

While `ETynHpIYLeY` was scheduled Private (`publishAt = 2026-11-12T18:00:00Z`), `update-pinned-comment.ts --create` returned `403 forbidden` and the Studio comment box disabled comment creation.

---

## 2. Direct Verification of Public Status, Comment Endpoint & Approvals (`2026-11-13T10:58:41Z`)

| Requirement | Status | Direct Evidence |
|---|---|---|
| **1. `ETynHpIYLeY` reads back `public`** | **SATISFIED** | - **Live YouTube Data API (`cd 07_Content-Ops && npm run channel:audit` in `History Of Science` at `2026-11-13T10:57:54Z`):**<br>  `PASS  long  ETynHpIYLeY  public  How Was the First Vaccine Made? (And Why It's Named After a Cow)` (`64 videos, 0 errors`).<br>- **Direct `youtube/v3/videos?part=status,snippet,statistics&id=ETynHpIYLeY` readback (`2026-11-13T10:58:41Z`):**<br>  `"id": "ETynHpIYLeY"`, `"title": "How Was the First Vaccine Made? (And Why It's Named After a Cow)"`, `"publishedAt": "2026-11-12T18:00:36Z"`, `"privacyStatus": "public"`, `"madeForKids": false`, `"selfDeclaredMadeForKids": false`, `"commentCount": "0"`, `"viewCount": "1"`.<br>- **Daily YouTube Analytics snapshot (`05_Analytics/hos/snapshots/2026-11-13.json`):**<br>  `"id": "ETynHpIYLeY"`, `"privacy": "public"`, `"publishAt": null`, `"publishedAt": "2026-11-12T18:00:36Z"`, `"seconds": 532`. |
| **2. Comment endpoint & `update-pinned-comment.ts --create --dry-run` readiness** | **SATISFIED** | - **Direct `youtube/v3/commentThreads?part=snippet&videoId=ETynHpIYLeY` readback (`2026-11-13T10:58:41Z`):**<br>  Returns HTTP `200` (was `403` while Private in `J0959`), `"count": 0`, `"items": []`.<br>- **`00_Brand/Channel-Setup/PINNED_COMMENTS.json` (in `History Of Science`):**<br>  `"comments": []` (no duplicate entry for `ETynHpIYLeY`).<br>- **Dry-run (`npx tsx --env-file=.env scripts/update-pinned-comment.ts --create --video ETynHpIYLeY --question "So how did a cow end up inside the most important medicine ever made?" --dry-run`):**<br>  Outputs exact required comment text:<br>  `"So how did a cow end up inside the most important medicine ever made?\n\nThank you for being here this early. It genuinely helps. A new film every Thursday."`<br>  Contains 0 links, 0 `/go/` links, and no subscriber count (channel subscribers = `6` < `10` floor). |
| **3. Original gates & Ben approvals remain valid** | **SATISFIED** | - **`J0946` (`2026-10-25`):** Ben Final OK (`#180` `6398845411`) on `hos_007_master_v04.mp4` (`sha256 c7f62adbb241bf3fbfaa3a17929f05768eedcf89044cb2cc5ebd2971c163e810`), uploaded as `ETynHpIYLeY`.<br>- **`J0959` (`2026-10-25`) & `J2536` (`2026-11-10`):** End screen (`8:31:02–8:51:02`, Subscribe + `_C92tIJCk8A`) and Ben-approved search-led title *How Was the First Vaccine Made? (And Why It's Named After a Cow)* with active 2-arm Title & Thumbnail Test & Compare verified in `J2745` and `J2752` (`HOS PR #573`). |

---

## 3. Protected Elected-Chief Action (`chief` / Grok Bot)

Because `scripts/jobs.py` (`do_reopen`, lines 948–949) restricts releasing a job with a `hold` to the elected Chief (`ValueError: Only the elected Chief may release a verified hold`), `J2718` is parked for the elected Chief (`chief`) to run:

```bash
python3 scripts/jobs.py reopen J0960 --agent chief \
  --note "J2718 verified (jobs/reviews/J2718/REVIEW.md): HOS 007 long ETynHpIYLeY reads back public since 2026-11-12T18:00:36Z in live YouTube Data API (channel:audit: 64 videos, 0 errors; videos.list privacyStatus=public) and 05_Analytics/hos/snapshots/2026-11-13.json. commentThreads.list returns HTTP 200 (0 comments) and update-pinned-comment.ts --create --dry-run builds the exact approved comment text. Post the comment on ETynHpIYLeY, pin it in HOS Studio, and read it back." \
  --git

python3 scripts/jobs.py done J2718 --agent chief --ref jobs/reviews/J2718/REVIEW.md \
  --result "CONDITION SATISFIED (jobs/reviews/J2718/REVIEW.md): HOS 007 long ETynHpIYLeY reads back public since 2026-11-12T18:00:36Z in live YouTube Data API (channel:audit: 64 videos, 0 errors) and 05_Analytics/hos/snapshots/2026-11-13.json; commentThreads.list HTTP 200 (0 comments) and update-pinned-comment.ts --create --dry-run verified ready. J0960 reopened to post, pin and read back the comment on ETynHpIYLeY. GBP0." \
  --git
```
