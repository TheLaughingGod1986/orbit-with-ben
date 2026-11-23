# J3401 — First-Day Check at 6 h: *What If Earth Stopped Spinning? (It's Already Slowing Down)* (`6bbbvfCx6zY`)

- **Channel:** Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`, verified on CDP `9223` before reading)
- **Video:** `6bbbvfCx6zY` (*What If Earth Stopped Spinning? (It's Already Slowing Down)*), long (`7:27` / `447 s`, `446,299 ms`, film `027`)
- **Went live:** `2026-11-22T18:00:00Z` (Sun 22 Nov 18:00 London; `timePublishedSeconds: 1795370406` = `18:00:06Z`)
- **Read window:** `2026-11-23T00:47Z`–`00:48Z` UTC (~6 h 47 m–6 h 48 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed, no edits/saves)
- **Browser note:** The existing `studio.youtube.com` tab (`8A9E2F211C963F35D4B2E8AFFD33B157`, left on `OVLv9dxTcpE/edit`) had an unresponsive renderer (no JS dialog; `Page.getFrameTree` and `Runtime.evaluate` timed out while Drive responded normally). Closed that one hung tab via `/json/close/` and opened a single fresh `studio.youtube.com` tab via `cdp_tabs.reuse_page(ctx, "studio.youtube.com")`, leaving the browser running with the same 3 tabs (1 Studio, 1 Drive, 1 Sheets).

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio Readback (`2026-11-23T00:47Z`–`00:48Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` / `22 Nov 2026 Published` on `Content > Videos` row and Video details; `VIDEO_PRIVACY_PUBLIC`, `userSetVisibility: VIDEO_USER_SET_VISIBILITY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, `allRestrictions.summary.severity: VIDEO_RESTRICTIONS_SEVERITY_UNSPECIFIED`, `VIDEO_COPYRIGHT_SUMMARY_STATUS_NO_CLAIMS_FOUND` (`activeThirdPartyClaimsCount: 0`, `videoHasThirdPartyClaim: false`, `videoHasCommercialBlock: false`), not Made for Kids (`No, it's not Made for Kids`, `VIDEO_MADE_FOR_KIDS_NOT_MFK`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`), altered content disclosed (`VIDEO_HAS_ALTERED_CONTENT_YES`) | **OK** |
| **HD processing** | **Finished** (`status: VIDEO_STATUS_PROCESSED`, `videoResolutions.statusSd: RESOLUTION_STATUS_DONE`, `videoResolutions.statusHd: RESOLUTION_STATUS_DONE`, solid `[SD]` and `[HD]` badges on Video details) | **OK** |
| **Related video vs upload package** | **N/A / None** — long-form video (`CREATOR_CONTENT_TYPE_VIDEO_ON_DEMAND`); `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/11_Upload-Package/PACKAGE_MANIFEST.json` specifies `"relatedVideoId": null` and no Shorts linkage attribution is present (its Shorts `OVLv9dxTcpE` and `emwQsPxnRGM` were linked to `6bbbvfCx6zY` in `J0317`) | **OK** |
| **Description vs upload package** | Exact byte-for-byte match (`1,834` characters, SHA-256 `a858107264b3c61025e24c98910f547cfcb6033c5d0b1a3f6a1351f0b7775474`) to `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/11_Upload-Package/Descriptions/earth_spin_long_description_v01.txt` (matches `J2497` readback; 13 tags, `en-GB` video and metadata language, Category `Science and technology`, and Title/Thumbnail A/B test `T028` `Running...` all intact) | **OK** |

**Faults recorded:** none (`0`).

---

## 2. Studio Analytics Numbers (`Since published`, at ~6 h 47 m–6 h 48 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Dashboard / Overview > Views** | **`9`** (`0.0` watch-time hours, `0` subscribers, `1` comment; `Suggested videos` `6` [66.7%], `Direct or unknown` `3` [33.3%]) | `--views 9` |
| **Overview > N more/less than usual** | **`↑ 7`** above typical performance band (`9 - 7 = 2`; Dashboard API `typicalRange`: `typicalValue: 1`, `upperBound: 2`, `TREND_TYPE_UP`) | `--typical 2` |
| **Dashboard > Ranking by views (Latest video card)** | **`1 of 10`** (*First 6 hours 47 minutes*; next highest in last 10 longs are `c5AdqQsnnys` and `55AEQwvs36g` at 3 views each) | `--rank 1 --of 10` |
| **Reach > Impressions** | **`1`** (`Thumbnail impressions`, Since published) | `--impressions 1` |
| **Reach > Impressions click-through rate** | **`0.0%`** (`Thumbnail click-through rate`, Since published; Dashboard shows `0%`) | `--ctr 0.0` |
| **Overview / Engagement > Average percentage viewed** | **`2.0%`** (Overview Engagement card: `0:09 (2%)`; Engagement tab: `0:09` AVD, `AVERAGE_WATCH_TIME: 9455 ms` / `446,299 ms`; `Key moments for audience retention` still processing) | `--avg-pct 2.0` |
| **Engagement / Dashboard > Likes** | **`0`** (`Likes vs dislikes`: `Not enough data`) | `--likes 0` |

Recorded in `05_Analytics/owb/launch/6bbbvfCx6zY.json` via:
```bash
python3 scripts/launch_check.py record 6bbbvfCx6zY --hours 6 --views 9 --rank 1 --of 10 --typical 2 --impressions 1 --ctr 0.0 --avg-pct 2.0 --likes 0 --by macbook-2 --read-at 2026-11-23T00:48Z
```

---

## 3. Output of `python3 scripts/launch_check.py judge 6bbbvfCx6zY`

```text
"What If Earth Stopped Spinning? (It's Already Slowing Down)" (6bbbvfCx6zY) · Orbit With Ben · long · went live Sun 22 Nov 18:00 London
At 6 h: views 9 · Studio rank 1 of 10 · impressions 1 · click rate 0.0% · average viewed 2.0%
Usual for this channel: click rate 2.1%, average viewed 19.6%

Verdict: AHEAD
  - 9 views at 6 h; Studio says the usual for us at this age is 2.
  - Studio ranks it 1 of 10 against our latest videos at the same age.

What is different about this one
  - It is 447 s long; the last 10 longs were 491 to 2858 s.

Do now
  - Nothing to fix.

Carry forward
  - A strong start is a lesson too: note what is different about this one.
```

---

## 4. Context Notes

- **No faults and `Verdict: AHEAD`:** Per Step 5 (0 faults and verdict is `AHEAD`, not `BEHIND`), closing `J3401` as `done` (not parked for Chief).
- **Early traffic mix:** 6 of 9 views came from `Suggested videos` (66.7%) and 3 from `Direct or unknown` (33.3%), with only `1` thumbnail impression so far (`0.0%` CTR) and `0:09` (`2%`) average view duration across 9 views. A/B test `T028` (*What If Earth Stopped Spinning? (It's Already Slowing Down)* / `4 CM A YEAR` vs *Earth's Day Used to Be 22 Hours (And It's Still Getting Longer)* / `CORALS KEPT COUNT`) is running (`9 views since test start`). Full CTR and retention assessment waits for the 48 h check and retention autopsy.
