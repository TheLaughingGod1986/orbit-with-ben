# J2787 — First-Day Check at 6 h: *What Was the Edward Jenner Experiment?* (`cLKDiYP55J8`)

- **Channel:** History of Science (`UCXp7HkBIl1LgaznXuZHJyRg`, verified on CDP `9222` before every page read)
- **Video:** `cLKDiYP55J8` (*What Was the Edward Jenner Experiment?*), Short (`22.40 s` / `0:23` badge; lead Short for 007 *How Was the First Vaccine Made? (And Why It's Named After a Cow)* `ETynHpIYLeY`)
- **Went live:** `2026-11-13T11:30:00Z` (Fri 13 Nov 11:30 London)
- **Read window:** `2026-11-13T17:51Z`–`17:56Z` UTC (~6 h 21 m–6 h 26 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed; reused existing `studio.youtube.com` tab on CDP `9222`, `Save` remained disabled)

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio & Watch-Page Readback (`2026-11-13T17:51Z`–`17:56Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` / `13 Nov 2026 Published` on `Content > Shorts` row and Video details; `VIDEO_PRIVACY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`; public Shorts page `isPrivate: false`, `isUnlisted: false`) | **OK** |
| **Listed under Content > Shorts tab** | **Yes** (`Content > Shorts`, first published row directly beneath the 5 scheduled Shorts; `contentType: CREATOR_CONTENT_TYPE_SHORTS`, `shorts.isShortsRenderable: true`, watch URL `https://youtube.com/shorts/cLKDiYP55J8`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, `VIDEO_COPYRIGHT_SUMMARY_STATUS_NO_CLAIMS_FOUND` (`activeThirdPartyClaimsCount: 0`), not Made for Kids (`VIDEO_MADE_FOR_KIDS_NOT_MFK`, `This video is set to not 'Made for Kids'`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`) | **OK** |
| **HD processing** | **Finished** (`status: VIDEO_STATUS_PROCESSED`, `videoResolutions.statusSd: RESOLUTION_STATUS_DONE`, `videoResolutions.statusHd: RESOLUTION_STATUS_DONE`) | **OK** |
| **Related video vs upload package** | **`How Was the First Vaccine Made? (And Why It's Named After a Cow)`** (`ETynHpIYLeY`) — `videoLinkageShortsAttribution.links[0].targetExternalVideoId: "ETynHpIYLeY"`, matching `SHORTS_UPLOAD_INDEX.json`, `SHORTS_RELEASE.json`, `LAUNCH_PLAN.md`, `social/hos/UPLOADS.json`, and `J0875_RELATED_READBACK.json` | **OK** |
| **Description vs upload package** | Exact byte-for-byte match to `10_Shorts/11_Upload-Package/s04_smallpox_test_v04/PACKAGE_MANIFEST.json` and `SHORTS_UPLOAD_INDEX.json`:<br>`Why Vaccines Are Named After a Cow`<br>`https://www.youtube.com/watch?v=ETynHpIYLeY`<br><br>`On 1 July 1796, Edward Jenner tested whether cowpox had protected James from smallpox. No disease followed.` | **OK** |
| **Cover, language, disclosure & tags** | Custom frame-0 cover `THE FIRST TEST` (`maxresdefault.jpg`) live, `audioLanguage: en-GB`, `metadataLanguage: en-GB`, `Altered content: Yes` (`VIDEO_HAS_ALTERED_CONTENT_YES`), `Category: Education`, `en-GB` standard captions serving, and all 6 manifest tags (`cowpox`, `edward jenner experiment`, `edward jenner smallpox vaccine`, `first vaccine`, `history of science`, `what was the edward jenner experiment`) confirmed live | **Confirmed** |

No faults found in Step 1.

---

## 2. Studio Analytics Numbers (`Since published`, at ~6 h 23 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Overview > Views** | **`9`** | `--views 9` |
| **Overview > N more/less than usual** | **`11 less than the usual 20 – 90`** (`9 + 11 = 20`) | `--typical 20` |
| **Dashboard > Ranking by views (Latest Short card)** | **`9 of 10`** (*First 6 hours 21 minutes*) | `--rank 9 --of 10` |
| **Reach > Traffic sources (Shorts feed)** | **Shorts feed `33.3%` = `3` views** (`YouTube search 66.7%` = `6` views; `Direct or unknown 0.0%` = `0`; `Other YouTube features 0.0%` = `0`, verified in Studio Advanced Mode `Traffic source` table) | `--feed-views 3` |
| **Reach > Shown in feed** | No separate `Shown in feed` number card in Studio (`launch_check.py` derives `~14` from `3 / 22.2%`; Engagement tab notes `Engaged views: 2`) | *(omitted)* |
| **Engagement > Viewed vs swiped away** | **`22.2%` Stayed to watch** / `77.8%` Swiped away | `--stayed 22.2` |
| **Dashboard / Explore > Average percentage viewed** | **`57.2%`** (`Average view duration: 0:13` on `0:23`; retention curve itself still processing) | `--avg-pct 57.2` |
| **Overview / Dashboard > Likes** | **`0`** | `--likes 0` |

Recorded in `05_Analytics/hos/launch/cLKDiYP55J8.json` via:
```bash
python3 scripts/launch_check.py record cLKDiYP55J8 --hours 6 --views 9 --rank 9 --of 10 --typical 20 --feed-views 3 --stayed 22.2 --avg-pct 57.2 --likes 0 --by macbook-2 --read-at 2026-11-13T17:53Z
```

---

## 3. Output of `python3 scripts/launch_check.py judge cLKDiYP55J8`

```text
"What Was the Edward Jenner Experiment?" (cLKDiYP55J8) · History of Science · Short · went live Fri 13 Nov 11:30 London
At 6 h: views 9 · Studio rank 9 of 10 · shown in feed about 14 (from 3 feed views) · stayed to watch 22.2% · average viewed 57.2%
Usual for this channel: stayed to watch 29.6%, average viewed 74.5%

Verdict: USUAL
  - 9 views at 6 h; Studio says the usual for us at this age is 20.
  - Studio ranks it 9 of 10 against our latest videos at the same age.

What is different about this one
  - The title starts with "What", like 3 earlier Shorts: they had 37 views by the next morning (median), against 81 for all Shorts.
  - It is a second upload of the same video (it replaced -I_GHK-GcFs).

Do now
  - Nothing to fix.
```

---

## 4. Disposition

- Step 1 found `0` faults and `launch_check.py judge` returned **`Verdict: USUAL`** (`9` views vs `20` typical = `0.45x`, above the `< 0.4x` `BEHIND` threshold; `6` of the `9` early views came from YouTube search and `3` from the Shorts feed).
- Per Step 5 (*"If step 1 found a fault, or the verdict is BEHIND, park for the Chief ... Otherwise close the job as done"*), `J2787` is closed as `done` with the full `judge` output and this evidence PR left open for Chief merge.
