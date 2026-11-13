# J2788 — First-Day Check at 6 h: *Why Does Pluto's Giant Ice Heart Have Zero Craters?* (`z5V6gIXXYs8`)

- **Channel:** Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`, verified on CDP `9223` before reading)
- **Video:** `z5V6gIXXYs8` (*Why Does Pluto's Giant Ice Heart Have Zero Craters?*), Short (`18 s` / `0:18` badge; standalone Shorts test S7 v02 per `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/TEST_LOG.md`)
- **Went live:** `2026-11-13T11:30:00Z` (Fri 13 Nov 11:30 London)
- **Read window:** `2026-11-13T17:50Z`–`17:53Z` UTC (~6 h 20 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed; reused existing `studio.youtube.com` tab on CDP `9223`)

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio Readback (`2026-11-13T17:50Z`–`17:53Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` on Content > Shorts row and Video details; `VIDEO_PRIVACY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`) | **OK** |
| **Listed under Content > Shorts tab** | **Yes** (First Public row under `Content > Shorts`; `contentType: CREATOR_CONTENT_TYPE_SHORTS`, watch URL `https://youtube.com/shorts/z5V6gIXXYs8`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, not Made for Kids (`VIDEO_MADE_FOR_KIDS_NOT_MFK`), no copyright claim (`VIDEO_COPYRIGHT_SUMMARY_STATUS_NO_CLAIMS_FOUND`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`) | **OK** |
| **HD processing** | **Finished** (`statusSd: RESOLUTION_STATUS_DONE`, `statusHd: RESOLUTION_STATUS_DONE`, `status: VIDEO_STATUS_PROCESSED`) | **OK** |
| **Related video vs upload package** | **`None`** — matches `PACKAGE_MANIFEST_v02.json` (`"relatedVideoId": null`) and `studio/RULES.md` (`J0216` standalone test Shorts unlinked until 20 Nov 2026) | **OK** |
| **Description vs upload package** | Exact match to `PACKAGE_MANIFEST_v02.json`:<br>`Pluto's Heart Has No Craters`<br><br>`Pictures: NASA imagery and artist concepts, with our own animated graphics. Facts checked against NASA sources.`<br>`Image credits: NASA; NASA/JPL-Caltech; NASA/ESA/CSA (as applicable).` | **OK** |
| **Language, tags & AI disclosure** | `en-GB` audio & metadata language, all 3 manifest tags (`astronomy`, `pluto heart`, `space`), and Altered content `Yes` (`VIDEO_HAS_ALTERED_CONTENT_YES`) confirmed live | **Confirmed** |

No faults found in Step 1.

---

## 2. Studio Analytics Numbers (`Since published`, at ~6 h 20 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Overview > Views** | **`147`** | `--views 147` |
| **Overview > N more/less than usual** | **`93 less than the usual 240 – 810`** (`147 + 93 = 240`) | `--typical 240` |
| **Dashboard > Ranking by views (Latest Short card)** | **`6 of 10`** (*First 6 hours 19 minutes*) | `--rank 6 --of 10` |
| **Reach > Traffic sources (Shorts feed)** | **Shorts feed `89.1%` = `131` views** (`YouTube search 9.5%` = `14` views; `Other YouTube features 1.4%` = `2` views) | `--feed-views 131` |
| **Reach > Shown in feed** | No separate "Shown in feed" number card in Studio (`launch_check.py` derives `~539` from `131 / 24.3%`; Engagement tab notes `Engaged views: 35`) | *(omitted)* |
| **Engagement > Viewed vs swiped away** | **`24.3%` Stayed to watch** / `75.7%` Swiped away | `--stayed 24.3` |
| **Dashboard / Engagement > Average percentage viewed** | **`88.0%`** on Dashboard Latest Short card (`Average view duration: 0:15` on `0:18`) | `--avg-pct 88.0` |
| **Likes** | **`4`** (`Since published` on Overview & Dashboard Latest Short card) | `--likes 4` |

Recorded in `05_Analytics/owb/launch/z5V6gIXXYs8.json` via:
```bash
python3 scripts/launch_check.py record z5V6gIXXYs8 --hours 6 --views 147 --rank 6 --of 10 --typical 240 --feed-views 131 --stayed 24.3 --avg-pct 88.0 --likes 4 --by macbook
```

---

## 3. Output of `python3 scripts/launch_check.py judge z5V6gIXXYs8`

```text
"Why Does Pluto's Giant Ice Heart Have Zero Craters?" (z5V6gIXXYs8) · Orbit With Ben · Short · went live Fri 13 Nov 11:30 London
At 6 h: views 147 · Studio rank 6 of 10 · shown in feed about 539 (from 131 feed views) · stayed to watch 24.3% · average viewed 88.0%
Usual for this channel: stayed to watch 32.0%, average viewed 65.4%

Verdict: AHEAD
  - 147 views at 6 h; the last 3 checked at the same age had 19 (median).
  - 147 views at 6 h; Studio says the usual for us at this age is 240.
  - Studio ranks it 6 of 10 against our latest videos at the same age.

What is different about this one
  - The title starts with "Why", like 9 earlier Shorts: they had 207 views by the next morning (median), against 72 for all Shorts.
  - It is a second upload of the same video (it replaced gmzaCfJF1gA).

Do now
  - Nothing to fix.

Carry forward
  - A strong start is a lesson too: note what is different about this one.
```

---

## 4. Notes

1. **Subject diversity restored Shorts-feed pick-up:** After three slow starts earlier this week (`ffYKoNVPoqg` Titan at `17` views, and back-to-back Mars rover Shorts `B1z2dv7m7Vk` at `45` views and `uhZSRcvngvE` at `19` views), switching subject to Pluto (`z5V6gIXXYs8`) entered the Shorts feed (`89.1%` Shorts feed = **FED**, `131` of `147` views; rank `6 of 10`), consistent with Chief's `B1z2dv7m7Vk` hypothesis on spreading subjects across the week.
2. **Retention vs swipe:** Viewers who stayed past the opening watched almost the entire cut (`88.0%` average viewed / `0:15` on `0:18`, well above `65.4%` channel usual), while `24.3%` stayed to watch (`75.7%` swiped away).
3. **Disposition:** Step 1 found `0` faults and the verdict is `AHEAD`, so per Step 5 this job closes as `done`.
