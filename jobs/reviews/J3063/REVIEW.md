# J3063 — First-Day Check at 12 h (Delayed 6 h Check): *How Do Plants Clean the Air?* (`ChbsigHD5_o`)

- **Channel:** History of Science (`@HistoryOfScienceYT`, `UCXp7HkBIl1LgaznXuZHJyRg`, verified on local MacBook CDP `9222` via `scripts/cdp_tabs.py:reuse_page` — single `studio.youtube.com` tab preserved; Orbit channel ID absent)
- **Video:** `ChbsigHD5_o` (*How Do Plants Clean the Air?*), Short (`24.25 s` / `0:25` badge; 006 *The Willow Tree That Was Made of Air* `VbPubYd6Fbs` Short B `v02`, uploaded in `J2272`)
- **Went live:** `2026-11-18T11:30:00Z` (Wed 18 Nov 11:30 London; `timePublishedSeconds: 1795001428` = `11:30:28Z`)
- **Read window:** `2026-11-18T23:55:02Z`–`2026-11-18T23:56:56Z` UTC (**12 h 26 m** elapsed since `11:30Z`; recorded at `--hours 12 --read-at 2026-11-18T23:56Z`, never labeled as 6 h, per the J3070 verified fallback handoff)
- **Mode:** Read-only (`£0` spend, zero YouTube/Studio/login edits; `Save` remained disabled on `/edit`; `1` page tab before and after)

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio Readback (`2026-11-18T23:55Z`–`23:56Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` / `18 Nov 2026 Published` on `Content > Shorts` row and Video details; `VIDEO_PRIVACY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`, `userSetVisibility: VIDEO_USER_SET_VISIBILITY_PUBLIC`) | **OK** |
| **Listed under Content > Shorts tab** | **Yes** (`Content > Shorts` row found directly for `ChbsigHD5_o`; `contentType: CREATOR_CONTENT_TYPE_SHORTS`, `shorts.isShortsRenderable: true`, `publicShorts.isShortsRenderable: true`, watch URL `https://youtube.com/shorts/ChbsigHD5_o`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, `allRestrictions.summary.severity: VIDEO_RESTRICTIONS_SEVERITY_UNSPECIFIED`, `copyrightPrechecksDone: true`, `brandSafetyPrechecksDone: true`, Claims tab reads *"No claims were found in this video / No copyrighted content was found in your video"*, not Made for Kids (`VIDEO_MADE_FOR_KIDS_NOT_MFK`, `effectiveMfk: VIDEO_MADE_FOR_KIDS_NOT_MFK`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`) | **OK** |
| **HD processing** | **Finished** (`status: VIDEO_STATUS_PROCESSED`, `videoResolutions.statusSd: RESOLUTION_STATUS_DONE`, `videoResolutions.statusHd: RESOLUTION_STATUS_DONE`) | **OK** |
| **Related video vs upload package** | **`The Willow Tree That Was Made of Air`** (`VbPubYd6Fbs`) — `videoLinkageShortsAttribution.links[0].targetExternalVideoId: "VbPubYd6Fbs"`, matching `origin/cursor/J2272-short-b-upload` (`c01a5e04`) `02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/11_Upload-Package/short_b_v02/PACKAGE_MANIFEST.json` and `00_Brand/Channel-Setup/social/hos/UPLOADS.json` | **OK** |
| **Description vs upload package** | Exact byte-for-byte match to `short_b_v02/PACKAGE_MANIFEST.json` (`c01a5e04`):<br>`The Willow Tree That Was Made of Air`<br>`https://www.youtube.com/watch?v=VbPubYd6Fbs`<br><br>`A sprig of mint repaired the air. Joseph Priestley burned a candle in a sealed jar until the flame died. Ten days after he added the mint, a candle burned in that same air.`<br><br>`Sources: Joseph Priestley, "Observations on Different Kinds of Air", Philosophical Transactions 62 (1772).`<br><br>`Pictures: illustrated scenes alongside the spoken experiment. Facts: the ten days and the mint are Priestley's 1771 trial, checked against the source above.` | **OK** |
| **Title, cover, language, disclosure, captions & tags** | Title `How Do Plants Clean the Air?` exact match; custom cover (`defaultStill: false`, `customThumbnail` set); `audioLanguage: en-GB`; `metadataLanguage: en-GB`; `Altered content: Yes` (`VIDEO_HAS_ALTERED_CONTENT_YES`); `Category: Education` (`CREATOR_VIDEO_CATEGORY_EDUCATION`); `Languages` page confirms `English (United Kingdom)` subtitles present (`Edit subtitles`); all 6 manifest tags (`history of science`, `how do plants clean the air`, `joseph priestley`, `joseph priestley experiment`, `mint plant`, `photosynthesis`) confirmed live | **Confirmed** |

No faults found in Step 1.

---

## 2. Studio Analytics Numbers (`Since published`, at `2026-11-18T23:56Z` — 12 h 26 m elapsed)

| Metric | Studio Value (`23:56:00Z`–`23:56:56Z`) | Flag Recorded |
|---|---|---|
| **Overview > Views** | **`0`** (`Since published`, chart range `18 Nov 2026, 11:30` – `18 Nov 2026, 23:56`; `publicMetrics.externalViewCount: "0"`; `60-minute views: 0`) | `--views 0` |
| **Overview > N more/less than usual** | **`20 less than the usual 20 – 110`** (`aria-label` on `Views` comparison badge; `0 + 20 = 20`) | `--typical 20` |
| **Dashboard > Ranking by views (Latest Short card)** | **`9 of 10`** (*First 12 hours 25 minutes* at `23:56:20Z`) | `--rank 9 --of 10` |
| **Reach > Traffic sources (Shorts feed)** | `Not enough data` on `How viewers found this Short` (`Views • Since published`, `23:56:05Z`) | *(omitted)* |
| **Reach > Shown in feed** | `Not enough data` on `How viewers engaged` (`Shorts feed impressions • Since published`, `23:56:10Z`); no `Shown in feed` card on Reach | *(omitted)* |
| **Engagement > Viewed vs swiped away** | `Not enough data` on `How viewers engaged` (`Since published`, `23:56:00Z` & `23:56:10Z`) | *(omitted)* |
| **Engagement > Average percentage viewed** | `Not enough data` (`Audience retention isn't ready yet. Processing can take up to two days.`; Dashboard placeholder `0%` over `0` views, `Average view duration: 0:00`) | *(omitted)* |
| **Overview / Dashboard > Likes** | **`0`** (`Likes • Since published: 0`, `publicMetrics.likeCount: "0"`) | `--likes 0` |

Recorded in `05_Analytics/hos/launch/ChbsigHD5_o.json` via:
```bash
python3 scripts/launch_check.py record ChbsigHD5_o --hours 12 --views 0 --rank 9 --of 10 --typical 20 --likes 0 --by macbook-2 --read-at 2026-11-18T23:56Z
```

---

## 3. Output of `python3 scripts/launch_check.py judge ChbsigHD5_o`

```text
"How Do Plants Clean the Air?" (ChbsigHD5_o) · History of Science · Short · went live Wed 18 Nov 11:30 London
At 12 h: views 0 · Studio rank 9 of 10 · shown in feed no figure yet · stayed to watch no figure yet · average viewed no figure yet
Usual for this channel: stayed to watch 29.6%, average viewed 74%

Verdict: BEHIND
  - 0 views at 12 h; Studio says the usual for us at this age is 20.
  - Studio ranks it 9 of 10 against our latest videos at the same age.

Do now
  - Studio gave no reach figures at this check, so the step that lost the viewers is not known. Read them again before deciding anything.
```

---

## 4. Context Notes for Chief

1. **Zero technical faults; zero feed seed at 12 h 26 m:** Every Studio setting on `ChbsigHD5_o` matches the approved `J2272` upload package (`Public`, under `Shorts`, `Notices: —`, zero copyright claims, not Made for Kids, no age restriction, HD done, `Related video` → `VbPubYd6Fbs`, exact description & tags, `en-GB` audio/metadata/subtitles, `Altered content: Yes`). All reach and engagement cards still show `Not enough data` with `0` views (`0` likes, `0.0` watch hours) vs `20 – 110` usual.
2. **Consecutive zero/near-zero HOS Short starts:** On the Dashboard `Published videos` list at `23:56Z`, yesterday's Short `xgx2lYHhYZM` (*Why Is It Called a Vaccine?*, Tue 17 Nov) now sits at just `2` views (after `0` views at 6 h in `J3004`), whereas the two Shorts before them (`xzKoHg0E0_U` *What Is Dalton's Atomic Theory?* `184` views; `Wvjd8g0CpzE` *The Blood Vessels Finer Than a Hair* `215` views) fed normally. That gives two consecutive HOS Shorts (`xgx2lYHhYZM` on 17 Nov and `ChbsigHD5_o` on 18 Nov) without an initial Shorts-feed push, ahead of `Bks_JLId1ew` (*How Do Plants Make Oxygen?*, 006 Short C, Sat 21 Nov 11:30Z).
3. **Next morning snapshot:** The 19 Nov `06:40Z` daily snapshot (~19 h after publish) will show whether `ChbsigHD5_o` received a delayed overnight feed test or remained unfed.

Per Step 5 (`Verdict: BEHIND`), parking `J3063` for the Chief (`parked for Chief: first-day check, Verdict: BEHIND`).
