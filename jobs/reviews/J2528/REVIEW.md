# J2528 — First-Day Check at 6 h: *What Would Standing on Saturn's Moon Titan Feel Like?* (`ffYKoNVPoqg`)

- **Channel:** Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`, verified on CDP `9223` before reading)
- **Video:** `ffYKoNVPoqg` (*What Would Standing on Saturn's Moon Titan Feel Like?*), Short (`18.0 s` / `0:19` badge)
- **Went live:** `2026-11-10T11:30:32Z` (scheduled `2026-11-10T11:30:00Z`, Tue 10 Nov 11:30 London)
- **Read window:** `2026-11-10T17:48:32Z`–`17:52:38Z` UTC (~6 h 18 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed; reused existing `studio.youtube.com` tab)

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio Readback (`2026-11-10T17:48Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`VIDEO_PRIVACY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`) | **OK** |
| **Listed under Content > Shorts tab** | **Yes** (`list_creator_videos` on `/videos/short`, `contentType: CREATOR_CONTENT_TYPE_SHORTS`, `isShortsRenderable: true`, watch link `https://youtube.com/shorts/ffYKoNVPoqg`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — no copyright claim (`videoHasThirdPartyClaim: false`, `copyrightPrechecksDone: true`), not Made for Kids (`VIDEO_MADE_FOR_KIDS_NOT_MFK`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`, `VIDEO_TARGETED_AUDIENCE_ALL`) | **OK** |
| **HD processing** | **Finished** (`statusSd: RESOLUTION_STATUS_DONE`, `statusHd: RESOLUTION_STATUS_DONE`, UI badges `Standard Definition complete` + `High Definition complete`) | **OK** |
| **Related video vs upload package** | **`None`** — matches `PACKAGE_MANIFEST_v11.json` (`"relatedVideoId": null`; J0216 standalone test Short runs unlinked until 20 Nov, and 032 Titan long airs 25 Nov) | **OK** |
| **Description vs upload package** | Exact match to `PACKAGE_MANIFEST_v11.json`:<br>`Standing on Titan Feels Like Diving 15 Metres Down`<br><br>`Pictures: NASA imagery and artist concepts, with our own animated graphics. Facts checked against NASA sources.`<br>`Image credits: NASA; NASA/JPL-Caltech; NASA/ESA/CSA (as applicable).` | **OK** |
| **Earlier J2504 listing updates** | Confirmed live in Studio: `Video language: English (United Kingdom)` (`en-GB`) and 8 search-phrase/topic tags (`what would standing on titan feel like`, `standing on titan`, `titan surface pressure`, `titan atmosphere`, `saturn moon titan`, `titan`, `space`, `astronomy`). | **Confirmed** |

No faults found in Step 1.

---

## 2. Studio Analytics Numbers (`Since published`, at 6 h 18 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Overview > Views** | **`17`** (*"Views are lower than usual. Also, more viewers swiped away."*) | `--views 17` |
| **Overview > N more/less than usual** | **`223 less than usual`** (`17 + 223 = 240`; API `typicalRange`: `240–800`, `typicalValue: 443`) | `--typical 240` |
| **Dashboard > Ranking by views (Latest Short card)** | **`10 of 10`** (*First 6 hours 18 minutes*) | `--rank 10 --of 10` |
| **Reach > Traffic sources (Shorts feed)** | **Shorts feed `52.9%` = `9` views** (YouTube search `35.3%` = `6` views; Other YouTube features `11.8%` = `2` views) | `--feed-views 9` |
| **Reach > Shown in feed** | No separate "Shown in feed" card in Studio (`launch_check.py` derives `~34` from `9 / 26.3%`) | *(omitted)* |
| **Engagement > Viewed vs swiped away** | **`26.3%` Stayed to watch** / `73.7%` Swiped away (`Engaged views: 5`) | `--stayed 26.3` |
| **Dashboard / Engagement > Average percentage viewed** | **`22.2%`** on Dashboard Latest Short card (`AVERAGE_WATCH_PERCENTAGE: 0.2222`; Engagement tab shows `Average view duration: 0:04` of `18.0 s`) | `--avg-pct 22.2` |
| **Likes** | **`1`** (`RATINGS_LIKES: 1`) | `--likes 1` |

Recorded in [`05_Analytics/owb/launch/ffYKoNVPoqg.json`](../../../05_Analytics/owb/launch/ffYKoNVPoqg.json) via:
```bash
python3 scripts/launch_check.py record ffYKoNVPoqg --hours 6 --views 17 --rank 10 --of 10 --typical 240 --feed-views 9 --stayed 26.3 --avg-pct 22.2 --likes 1 --by macbook-2 --git
```

---

## 3. Output of `python3 scripts/launch_check.py judge ffYKoNVPoqg`

```text
"What Would Standing on Saturn's Moon Titan Feel Like?" (ffYKoNVPoqg) · Orbit With Ben · Short · went live Tue 10 Nov 11:30 London
At 6 h: views 17 · Studio rank 10 of 10 · shown in feed about 34 (from 9 feed views) · stayed to watch 26.3% · average viewed 22.2%
Usual for this channel: stayed to watch 31.9%, average viewed 66.3%

Verdict: BEHIND, not shown
  - 17 views at 6 h; Studio says the usual for us at this age is 240.
  - Studio ranks it 10 of 10 against our latest videos at the same age.

What is different about this one
  - "Saturn" was in the title of 4 earlier Shorts: they had 44 views by the next morning (median), against 145 for all Shorts.
  - It is a second upload of the same video (it replaced RLSJm59OSzI).

Do now
  - Nothing in the cut explains this yet: YouTube has shown it to too few people to judge it.
  - Check the faults list is empty, then read tomorrow morning's snapshot. Under a tenth of the usual first day means the feed tried it and stopped: treat the subject and the title as the cause, not the edit.

Carry forward
  - If "What is different about this one" says earlier videos on its subject were weak too, take that subject off the next four weeks of the schedule and tell the topic go/no-go.

Done (2026-11-10T14:06Z, claudecode): tags set to search phrases and language to en-GB (J2504)

Done (2026-11-10T14:09Z, claude): Nothing technically wrong (J2501, review merged as #738). Tags to search phrases and language to en-GB: J2504. No re-cut or second upload. The opening gate had no full-bleed check and passed this Short's blur-padded 16:9 opening: J2505 adds the check and runs it on every scheduled Short. Also found: the live Mars Short iyvWYFP_ETA had no Related video; J2504 sets it on all four Mars Shorts.
```
