# J2745 — First-Day Check at 6 h: *How Was the First Vaccine Made? (And Why It's Named After a Cow)* (`ETynHpIYLeY`)

- **Channel:** History of Science (`UCXp7HkBIl1LgaznXuZHJyRg`, verified on CDP `9222` before every page read)
- **Video:** `ETynHpIYLeY` (*How Was the First Vaccine Made? (And Why It's Named After a Cow)*), long (`8:52` / `531.083 s`)
- **Went live:** `2026-11-12T18:00:00Z` (Thu 12 Nov 18:00 London)
- **Read window:** `2026-11-13T00:12Z`–`00:15Z` UTC (~6 h 13 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed; reused existing `studio.youtube.com` tab on CDP `9222`, `Save` remained disabled)

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio & Watch-Page Readback (`2026-11-13T00:12Z`–`00:15Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` / `12 Nov 2026 Published` on `Content > Videos` row 0 and Video details; `VIDEO_PRIVACY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`; watch page `isPrivate: false`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, `VIDEO_COPYRIGHT_SUMMARY_STATUS_NO_CLAIMS_FOUND`, not Made for Kids (`VIDEO_MADE_FOR_KIDS_NOT_MFK`, `This video is set to not 'Made for Kids'`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`) | **OK** |
| **HD processing** | **Finished** (`status: VIDEO_STATUS_PROCESSED`, `videoResolutions.statusSd: RESOLUTION_STATUS_DONE`, `videoResolutions.statusHd: RESOLUTION_STATUS_DONE`) | **OK** |
| **Related video / End screen vs upload package** | Long-form has no Shorts `Related video` field; `PACKAGE_MANIFEST.json` specifies `"relatedVideoId": "_C92tIJCk8A"` (*End screen links to 001 Germs (`_C92tIJCk8A`) + Subscribe*). Public watch-page `endscreenRenderer` confirms both elements serving at `511083`–`531083 ms` (`8:31–8:51`): `VIDEO` `_C92tIJCk8A` (*How Did We Discover Germs?*) + `CHANNEL` `UCXp7HkBIl1LgaznXuZHJyRg` (`isSubscribe: true`) | **OK** |
| **Description vs upload package** | Exact match to `Descriptions/vaccine_long_description_v02.txt` (`sha256: 4721ecd5976559544575443ecbdb3c612d53ce3a758927ae33d994075ba0886a`, 995 chars, identical to `J2470` / `J2536` readback) | **OK** |
| **Title & Thumbnail Test & Compare** | `Running…` (`CREATOR_EXPERIMENT_STATE_STARTED`, `T029` armed in `J2536`): Arm 1 `How Was the First Vaccine Made? (And Why It's Named After a Cow)` + `mqdefault_custom_1.jpg`; Arm 2 `Why Vaccines Are Named After a Cow` + `mqdefault_custom_2.jpg` | **Confirmed** |
| **Language, captions, disclosure & tags** | `Video language: English (United Kingdom)` (`en-GB`), `Title and description language: English (United Kingdom)` (`en-GB`), `en-GB` captions track serving live, `Altered content: Yes` (`VIDEO_HAS_ALTERED_CONTENT_YES`), `Category: Education`, and all 8 manifest tags (`cowpox`, `deadly smallpox virus`, `edward jenner cowpox vaccine`, `edward jenner smallpox vaccine`, `first vaccine`, `history of science`, `history of vaccines`, `how was the first vaccine made`) confirmed live | **Confirmed** |

*(Note on sibling follow-ups already queued: `J2717` / `J0875` covers linking scheduled Shorts `cLKDiYP55J8` and `xgx2lYHhYZM` to `ETynHpIYLeY` now that it is public; `J2718` / `J0960` covers posting the post-publish pinned comment.)*

No faults found in Step 1.

---

## 2. Studio Analytics Numbers (`Since published`, at ~6 h 13 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Overview > Views** | **`0`** | `--views 0` |
| **Overview > N more/less than usual** | No delta line shown in Studio on `0` views | *(omitted)* |
| **Dashboard > Ranking by views (Latest video card)** | **`3 of 7`** (*First 6 hours 12 minutes*; History of Science has 7 published longs) | `--rank 3 --of 7` |
| **Reach > Impressions** | **`4`** | `--impressions 4` |
| **Reach > Impressions click-through rate** | **`0.0%`** | `--ctr 0.0` |
| **Engagement > Average percentage viewed** | No figure yet (`Audience retention: Not enough data` / `Audience retention isn't ready yet. Processing can take up to two days.`; `0` views) | *(omitted)* |
| **Engagement > Likes** | **`0`** | `--likes 0` |

Recorded in `05_Analytics/hos/launch/ETynHpIYLeY.json` via:
```bash
python3 scripts/launch_check.py record ETynHpIYLeY --hours 6 --views 0 --rank 3 --of 7 --impressions 4 --ctr 0.0 --likes 0 --by macbook-2 --read-at 2026-11-13T00:13Z
```

---

## 3. Output of `python3 scripts/launch_check.py judge ETynHpIYLeY`

```text
"How Was the First Vaccine Made? (And Why It's Named After a Cow)" (ETynHpIYLeY) · History of Science · long · went live Thu 12 Nov 18:00 London
At 6 h: views 0 · Studio rank 3 of 7 · impressions 4 · click rate 0.0% · average viewed no figure yet

Verdict: USUAL
  - Studio ranks it 3 of 7 against our latest videos at the same age.

Do now
  - Nothing to fix.
```

---

## 4. Disposition

- Step 1 found `0` faults and the verdict is **`USUAL`** (not `BEHIND`), so per Step 5 (`Otherwise close the job as done`), `J2745` is closed as `done` with the `judge` output and this evidence PR left open for Chief merge.
- Next scheduled check for this long: `48 h` (`ETynHpIYLeY@48`, due Sat 14 Nov 18:00 UTC).
