# J3064 — First-Day Check at 6 h: *If Voyager Needs 75,000 Years, How Far Is the Nearest Star?* (`dH_yCRmzkMo`)

- **Channel:** Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`, verified on CDP `9223` before reading)
- **Video:** `dH_yCRmzkMo` (*If Voyager Needs 75,000 Years, How Far Is the Nearest Star?*), Short (`24 s` / `0:24` badge; second Short for 026 *How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)* `c5AdqQsnnys`)
- **Went live:** `2026-11-18T11:30:00Z` (Wed 18 Nov 11:30 London; `timePublishedSeconds: 1795001426` = `11:30:26Z`)
- **Read window:** `2026-11-18T18:19Z`–`18:29Z` UTC (~6 h 49 m–6 h 59 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed; reused existing `studio.youtube.com` tab on CDP `9223`, `Save` remained disabled)

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio Readback (`2026-11-18T18:19Z`–`18:29Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` / `18 Nov 2026 Published` on `Content > Shorts` row and Video details; `VIDEO_PRIVACY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`) | **OK** |
| **Listed under Content > Shorts tab** | **Yes** (`Content > Shorts`, row 19 directly beneath the 18 scheduled Shorts; `contentType: CREATOR_CONTENT_TYPE_SHORTS`, watch URL `https://youtube.com/shorts/dH_yCRmzkMo`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, `VIDEO_COPYRIGHT_SUMMARY_STATUS_NO_CLAIMS_FOUND` (`activeThirdPartyClaimsCount: 0`), not Made for Kids (`This video is set to not 'Made for Kids'`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`) | **OK** |
| **HD processing** | **Finished** (`status: VIDEO_STATUS_PROCESSED`, `videoResolutions.statusSd: RESOLUTION_STATUS_DONE`, `videoResolutions.statusHd: RESOLUTION_STATUS_DONE`) | **OK** |
| **Related video vs upload package** | **`How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)`** (`c5AdqQsnnys`) — `videoLinkageShortsAttribution.links[0].targetExternalVideoId: "c5AdqQsnnys"`, matching `PACKAGE_MANIFEST_v07.json` and `00_Brand/Channel-Setup/social/UPLOADS.json` | **OK** |
| **Description vs upload package** | Exact byte-for-byte match to `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/11_Upload-Package/PACKAGE_MANIFEST_v07.json`:<br>`How Far Is the Nearest Star?`<br>`https://www.youtube.com/watch?v=c5AdqQsnnys`<br><br>`Voyager 1 leaves the solar system at about seventeen kilometres every second. At that speed, reaching the nearest star, Proxima Centauri, would take about 75,000 years.`<br><br>`Sources: NASA JPL Voyager Mission Status (Voyager 1 heliocentric speed ~17 km/s) · Gaia Collaboration, Vallenari et al. 2023 (A&A 674, A1), Proxima Centauri at 4.24 light-years.`<br><br>`Pictures: NASA/JPL-Caltech Voyager imagery (PIA17049, PIA14111), NASA SDO solar imagery, and ESO Paranal night-sky time-lapses (CC BY 4.0), alongside AI-assisted voice and editing. Facts: every number is checked against the sources listed above.`<br>`Image credits: NASA/JPL-Caltech; NASA SDO; ESO.` | **OK** |
| **Language & tags** | `audioLanguage: en-GB`, `metadataLanguage: en-GB`, `Category: Science and technology`, and all 7 manifest tags (`75000 years`, `how far is the nearest star`, `interstellar travel`, `nearest star`, `proxima centauri`, `space documentary`, `voyager 1`) confirmed live | **Confirmed** |

No faults found in Step 1.

---

## 2. Studio Analytics Numbers (`Since published`, at ~6 h 49 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Overview / Dashboard > Views** | **`5`** (`1` engaged view) | `--views 5` |
| **Overview > N more/less than usual** | **`105 less than the usual 110 – 860`** (`5 + 105 = 110`) | `--typical 110` |
| **Dashboard > Ranking by views (Latest Short card)** | **`9 of 10`** (*First 6 hours 49 minutes*) | `--rank 9 --of 10` |
| **Reach > Traffic sources (Shorts feed)** | **`0`** (`How viewers found this Short • Since published`: `YouTube search 100.0%` [`5` views], `Other YouTube features 0.0%` [`0` views], `Shorts feed` absent / `0` views) | `--feed-views 0` |
| **Reach > Shown in feed** | `Not enough data` on `Shorts feed impressions • Since published` (no `Shown in feed` card on Reach) | *(omitted)* |
| **Engagement > Viewed vs swiped away** | `Not enough data` on `How viewers engaged` (`Since published`; `—` in Advanced Mode `Stayed to watch` column) | *(omitted)* |
| **Dashboard / Advanced Mode > Average percentage viewed** | **`23.7%`** (`0:05` average view duration across `5` search views; `Audience retention` curve still processing) | `--avg-pct 23.7` |
| **Overview / Dashboard > Likes** | **`0`** | `--likes 0` |

Recorded in `05_Analytics/owb/launch/dH_yCRmzkMo.json` via:
```bash
python3 scripts/launch_check.py record dH_yCRmzkMo --hours 6 --views 5 --rank 9 --of 10 --typical 110 --feed-views 0 --avg-pct 23.7 --likes 0 --by macbook --read-at 2026-11-18T18:20Z
```

---

## 3. Output of `python3 scripts/launch_check.py judge dH_yCRmzkMo`

```text
"If Voyager Needs 75,000 Years, How Far Is the Nearest Star?" (dH_yCRmzkMo) · Orbit With Ben · Short · went live Wed 18 Nov 11:30 London
At 6 h: views 5 · Studio rank 9 of 10 · shown in feed about 0 (from 0 feed views) · stayed to watch no figure yet · average viewed 23.7%
Usual for this channel: stayed to watch 32.5%, average viewed 66.2%

Verdict: BEHIND, not shown
  - 5 views at 6 h; the last 7 checked at the same age had 147 (median).
  - 5 views at 6 h; Studio says the usual for us at this age is 110.
  - Studio ranks it 9 of 10 against our latest videos at the same age.

What is different about this one
  - It is a second upload of the same video (it replaced cwU_0WWeNZ4).

Do now
  - Nothing in the cut explains this yet: YouTube has shown it to too few people to judge it.
  - Check the faults list is empty, then read tomorrow morning's snapshot. Under a tenth of the usual first day means the feed tried it and stopped: treat the subject and the title as the cause, not the edit.

Carry forward
  - If "What is different about this one" says earlier videos on its subject were weak too, take that subject off the next four weeks of the schedule and tell the topic go/no-go.
```

---

## 4. Context Notes for Chief

1. **Zero technical faults; zero Shorts-feed impressions so far:** Every Studio setting on `dH_yCRmzkMo` matches `PACKAGE_MANIFEST_v07.json` (`Public`, listed under `Content > Shorts`, `Notices: —`, not Made for Kids, HD done, `Related video` → `c5AdqQsnnys`, `en-GB` audio/metadata). All `5` views so far came from `YouTube search` (`100.0%`), with `0` Shorts-feed views (`Not enough data` on `Shorts feed impressions`).
2. **Back-to-back topic overlap with Mon 16 Nov and Tue 17 Nov Shorts:** Unlike weak topics in general, both parent topics just fed well in the two days immediately before this Short:
   - Mon 16 Nov 11:30Z: `aEfdxex__Bo` (*If You Can't See the Nearest Star, How Far Away Is It?*, first 026 Short) — `234` views at 6 h (`212` Shorts feed), now `466` views.
   - Tue 17 Nov 11:30Z: `9q_OvQ1Rd8Y` (*How Far From Earth Is Voyager 1 Right Now?*) — `193` views at 6 h (`182` Shorts feed), now `253` views.
   - Wed 18 Nov 11:30Z: `dH_yCRmzkMo` (*If Voyager Needs 75,000 Years, How Far Is the Nearest Star?*, replacement upload for `cwU_0WWeNZ4`) — `5` views at 6 h (`0` Shorts feed, `5` YouTube search).
   Tomorrow morning's 06:40 snapshot will show whether YouTube gives `dH_yCRmzkMo` a delayed Shorts-feed seed overnight or skipped seeding after back-to-back *Nearest Star* + *Voyager 1* Shorts (similar to Learning 33 on back-to-back Mars rover Shorts `B1z2dv7m7Vk` → `uhZSRcvngvE`).

Per Step 5 (`Verdict: BEHIND, not shown`), parking `J3064` for the Chief (`parked for Chief: first-day check, Verdict: BEHIND, not shown`).
