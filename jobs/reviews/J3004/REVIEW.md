# J3004 — First-Day Check at 6 h: *Why Is It Called a Vaccine?* (`xgx2lYHhYZM`)

- **Channel:** History of Science (`UCXp7HkBIl1LgaznXuZHJyRg`, verified on CDP `9222` before every page read)
- **Video:** `xgx2lYHhYZM` (*Why Is It Called a Vaccine?*), Short (`24.53 s` / `0:25` badge; second Short for 007 *How Was the First Vaccine Made? (And Why It's Named After a Cow)* `ETynHpIYLeY`)
- **Went live:** `2026-11-17T11:30:00Z` (Tue 17 Nov 11:30 London; `timePublishedSeconds: 1794915027` = `11:30:27Z`)
- **Read window:** `2026-11-17T17:41Z`–`17:48Z` UTC (~6 h 11 m–6 h 18 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed; reused existing `studio.youtube.com` tab on CDP `9222`, `Save` remained disabled)

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio Readback (`2026-11-17T17:41Z`–`17:48Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` / `17 Nov 2026 Published` on `Content > Shorts` row and Video details; `VIDEO_PRIVACY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`) | **OK** |
| **Listed under Content > Shorts tab** | **Yes** (`Content > Shorts`, first published row directly beneath the 6 scheduled Shorts; `contentType: CREATOR_CONTENT_TYPE_SHORTS`, `shorts.isShortsRenderable: true`, `publicShorts.isShortsRenderable: true`, watch URL `https://youtube.com/shorts/xgx2lYHhYZM`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, `VIDEO_COPYRIGHT_SUMMARY_STATUS_NO_CLAIMS_FOUND` (`activeThirdPartyClaimsCount: 0`), not Made for Kids (`VIDEO_MADE_FOR_KIDS_NOT_MFK`, `This video is set to not 'Made for Kids'`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`) | **OK** |
| **HD processing** | **Finished** (`status: VIDEO_STATUS_PROCESSED`, `videoResolutions.statusSd: RESOLUTION_STATUS_DONE`, `videoResolutions.statusHd: RESOLUTION_STATUS_DONE`) | **OK** |
| **Related video vs upload package** | **`How Was the First Vaccine Made? (And Why It's Named After a Cow)`** (`ETynHpIYLeY`) — `videoLinkageShortsAttribution.links[0].targetExternalVideoId: "ETynHpIYLeY"`, matching `SHORTS_UPLOAD_INDEX.json`, `SHORTS_RELEASE.json`, `LAUNCH_PLAN.md`, `social/UPLOADS.json`, and `J0875_RELATED_READBACK.json` | **OK** |
| **Description vs upload package** | Exact byte-for-byte match to `10_Shorts/11_Upload-Package/s05_vacca_jesty_v05/PACKAGE_MANIFEST.json` and `SHORTS_UPLOAD_INDEX.json`:<br>`Why Vaccines Are Named After a Cow`<br>`https://www.youtube.com/watch?v=ETynHpIYLeY`<br><br>`Twenty-two years before Edward Jenner's 1798 book, Benjamin Jesty tried cowpox in 1774. Jenner called the disease variolae vaccinae ("smallpox of the cow"), and from vacca, the Latin word for cow, came the name vaccination.`<br><br>`Pictures: AI-generated 3D scenes; voice: AI narration.` | **OK** |
| **Cover, language, disclosure & tags** | Custom frame-0 cover (`defaultStill: false`, `customThumbnail` set), `audioLanguage: en-GB`, `metadataLanguage: en-GB`, `Altered content: Yes` (`VIDEO_HAS_ALTERED_CONTENT_YES`), `Category: Education`, `en-GB` standard captions serving, and all 6 manifest tags (`benjamin jesty`, `edward jenner cowpox vaccine`, `first vaccine`, `history of science`, `vaccine latin word`, `why is it called a vaccine`) confirmed live | **Confirmed** |

No faults found in Step 1.

---

## 2. Studio Analytics Numbers (`Since published`, at ~6 h 12 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Overview > Views** | **`0`** | `--views 0` |
| **Overview > N more/less than usual** | **`20 less than the usual 20 – 90`** (`0 + 20 = 20`) | `--typical 20` |
| **Dashboard > Ranking by views (Latest Short card)** | **`10 of 10`** (*First 6 hours 11 minutes*) | `--rank 10 --of 10` |
| **Reach > Traffic sources (Shorts feed)** | `Not enough data` on `How viewers found this Short` (`Views • Since published`) | *(omitted)* |
| **Reach > Shown in feed** | `Not enough data` on `Shorts feed impressions • Since published` | *(omitted)* |
| **Engagement > Viewed vs swiped away** | `Not enough data` on `How viewers engaged` (`Since published`; tab header placeholder `0.0%` over `0` engaged views) | *(omitted)* |
| **Engagement > Average percentage viewed** | `Not enough data` (`Audience retention isn't ready yet. Processing can take up to two days.`; Dashboard placeholder `0%` over `0` views) | *(omitted)* |
| **Overview / Dashboard > Likes** | **`0`** | `--likes 0` |

Recorded in `05_Analytics/hos/launch/xgx2lYHhYZM.json` via:
```bash
python3 scripts/launch_check.py record xgx2lYHhYZM --hours 6 --views 0 --rank 10 --of 10 --typical 20 --likes 0 --by macbook-2 --read-at 2026-11-17T17:42Z
```

---

## 3. Output of `python3 scripts/launch_check.py judge xgx2lYHhYZM`

```text
"Why Is It Called a Vaccine?" (xgx2lYHhYZM) · History of Science · Short · went live Tue 17 Nov 11:30 London
At 6 h: views 0 · Studio rank 10 of 10 · shown in feed no figure yet · stayed to watch no figure yet · average viewed no figure yet
Usual for this channel: stayed to watch 28.9%, average viewed 75.9%

Verdict: BEHIND
  - 0 views at 6 h; Studio says the usual for us at this age is 20.
  - Studio ranks it 10 of 10 against our latest videos at the same age.

What is different about this one
  - It is a second upload of the same video (it replaced 4WUs0beKn0A).

Do now
  - Studio gave no reach figures at this check, so the step that lost the viewers is not known. Read them again before deciding anything.
```

---

## 4. Context Notes for Chief

1. **Zero technical faults; zero feed seed so far:** Every Studio setting on `xgx2lYHhYZM` matches the approved upload package (`Public`, under `Shorts`, `Notices: —`, not Made for Kids, HD done, `Related video` → `ETynHpIYLeY`, `en-GB` audio/metadata/captions, `Altered content: Yes`). Both `How viewers found this Short` and `Shorts feed impressions` still read `Not enough data` at 6 h 12 m (`0` views vs `20` usual).
2. **Comparison with adjacent HOS Shorts:** Between the first 007 Vaccine Short `cLKDiYP55J8` (*What Was the Edward Jenner Experiment?*, Fri 13 Nov: `9` views at 6 h, now `33` views) and today's `xgx2lYHhYZM`, non-vaccine HOS Shorts fed normally (`Wvjd8g0CpzE` Harvey `214` views on 15 Nov; `xzKoHg0E0_U` Dalton `121` views on 16 Nov), while the 007 long `ETynHpIYLeY` sits at `5` views. Tomorrow morning's 06:40 snapshot will show whether YouTube gives `xgx2lYHhYZM` a delayed Shorts-feed test overnight or keeps vaccine/smallpox Shorts throttled in the feed (relevant to the two scheduled 007 Shorts on 28–29 Nov, `sY0PSQFxjp8` and `jkUZpyO71lU`).
3. **Optional listing note:** Line 1 of `xgx2lYHhYZM`'s description matches `PACKAGE_MANIFEST.json` verbatim (`Why Vaccines Are Named After a Cow`, the long's Title T&C Arm 2 wording above `https://www.youtube.com/watch?v=ETynHpIYLeY`), while the `Related video` pill shows the search-led Arm 1 title `How Was the First Vaccine Made? (And Why It's Named After a Cow)`.

Per Step 5 (`Verdict: BEHIND`), parking `J3004` for the Chief (`parked for Chief: first-day check, Verdict: BEHIND`).
