# J3243 — First-Day Check at 6 h: *Will Asteroid 2024 YR4 Hit the Moon in 2032?* (`93JL_IK57EM`)

- **Channel:** Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`, verified on CDP `9223` before reading)
- **Video:** `93JL_IK57EM` (*Will Asteroid 2024 YR4 Hit the Moon in 2032?*), Short (`20 s` / `0:20` badge, `19,366 ms`; Apophis replication test Short `AR1`, uploaded via `J2228`, rescheduled from 27 Nov to 20 Nov via `J3121`)
- **Went live:** `2026-11-20T11:30:00Z` (Fri 20 Nov 11:30 London; `timePublishedSeconds: 1795174215` = `11:30:15Z`)
- **Read window:** `2026-11-20T17:45Z`–`17:49Z` UTC (~6 h 14 m–6 h 19 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed; reused existing `studio.youtube.com` tab on CDP `9223`)

---

## 1. Is Anything Broken? (`1` fault)

| Check | Studio Readback (`2026-11-20T17:45Z`–`17:49Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` / `20 Nov 2026 Published` on `Content > Shorts` row and Video details; `VIDEO_PRIVACY_PUBLIC`, `userSetVisibility: VIDEO_USER_SET_VISIBILITY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`) | **OK** |
| **Listed under Content > Shorts tab** | **Yes** (`Content > Shorts`, top published Short directly beneath scheduled Shorts; `contentType: CREATOR_CONTENT_TYPE_SHORTS`, `publicShorts.isShortsRenderable: true`, watch URL `https://youtube.com/shorts/93JL_IK57EM`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, `allRestrictions.summary.severity: VIDEO_RESTRICTIONS_SEVERITY_UNSPECIFIED`, `VIDEO_COPYRIGHT_SUMMARY_STATUS_NO_CLAIMS_FOUND` (`activeThirdPartyClaimsCount: 0`), not Made for Kids (`This video is set to not 'Made for Kids'`, `VIDEO_MADE_FOR_KIDS_NOT_MFK`), no age restriction (`VIDEO_AGE_RESTRICTION_NONE`), altered content disclosed (`VIDEO_HAS_ALTERED_CONTENT_YES`) | **OK** |
| **HD processing** | **Finished** (`status: VIDEO_STATUS_PROCESSED`, `videoResolutions.statusSd: RESOLUTION_STATUS_DONE`, `videoResolutions.statusHd: RESOLUTION_STATUS_DONE`, `[SD]` and `[HD]` badges solid on Video details) | **OK** |
| **Related video vs upload package** | **`None`** (`Related video: None` on Video details; `videoLinkageShortsAttribution` absent in `get_creator_videos`), whereas `jobs/reviews/J2228/PACKAGE_MANIFEST.json` specifies `"relatedVideoId": "VBaYRPp85Sw"` (*What Happened to Venus?*) and `00_Brand/Channel-Setup/social/UPLOADS.json` still marks `"relatedStatus": "pending_studio"` | **FAULT** |
| **Description vs upload package** | Exact byte-for-byte match (`1,190` characters) to `jobs/reviews/J2228/PACKAGE_MANIFEST.json` (Title and all 6 manifest tags — `2024 yr4`, `asteroid`, `astronomy`, `james webb space telescope`, `moon`, `space` — plus Category `Science and technology` also match) | **OK** |

**Fault recorded (1):**
- `Related video is None in Studio; upload package specifies VBaYRPp85Sw (What Happened to Venus?)`

---

## 2. Studio Analytics Numbers (`Since published`, at ~6 h 14 m–6 h 19 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Dashboard / Overview > Views** | **`179`** (`71` engaged views; `0.4` watch-time hours; `0` subscribers; green checkmark) | `--views 179` |
| **Overview > N more/less than usual** | **`About the same as the usual 110 – 630`** (Dashboard tooltip: `Your typical range: 110–630`; inside typical band, so no single "N more/less than usual" figure) | *(omitted)* |
| **Dashboard > Ranking by views (Latest Short card)** | **`4 of 10`** (*First 6 hours 14 minutes*) | `--rank 4 --of 10` |
| **Reach / Advanced Mode > Traffic source (Shorts feed)** | **`156`** (`How viewers found this Short • Since published`: `Shorts feed 87.2%` [`156` views, `0.3 h`, `0:13` AVD], `YouTube search 12.3%` [`22` views, `0.1 h`, `0:42` AVD], `Other YouTube features 0.6%` [`1` view, `0.0 h`, `0:04` AVD]) | `--feed-views 156` |
| **Reach > Shown in feed** | No `Shown in feed` card present on Reach | *(omitted)* |
| **Engagement > Viewed vs swiped away** | **`43.8%` Stayed to watch** / `56.2%` Swiped away (`How viewers engaged • Shorts feed impressions • Since published`) | `--stayed 43.8` |
| **Dashboard > Average percentage viewed** | **`88.6%`** (green up arrow; typical range `61.8%–64.4%`; `0:17` average view duration; `Key moments for audience retention` still processing) | `--avg-pct 88.6` |
| **Dashboard / Overview > Likes** | **`1`** (typical range `1–6`) | `--likes 1` |

Recorded in `05_Analytics/owb/launch/93JL_IK57EM.json` via:
```bash
python3 scripts/launch_check.py record 93JL_IK57EM --hours 6 --views 179 --rank 4 --of 10 --feed-views 156 --stayed 43.8 --avg-pct 88.6 --likes 1 --fault "Related video is None in Studio; upload package specifies VBaYRPp85Sw (What Happened to Venus?)" --by macbook --read-at 2026-11-20T17:45Z
```

---

## 3. Output of `python3 scripts/launch_check.py judge 93JL_IK57EM`

```text
"Will Asteroid 2024 YR4 Hit the Moon in 2032?" (93JL_IK57EM) · Orbit With Ben · Short · went live Fri 20 Nov 11:30 London
At 6 h: views 179 · Studio rank 4 of 10 · shown in feed about 356 (from 156 feed views) · stayed to watch 43.8% · average viewed 88.6%
Usual for this channel: stayed to watch 32.5%, average viewed 66.0%

Verdict: FAULT
  - Fault: Related video is None in Studio; upload package specifies VBaYRPp85Sw (What Happened to Venus?)
  - 179 views at 6 h; the last 9 checked at the same age had 45 (median).
  - Studio ranks it 4 of 10 against our latest videos at the same age.

Do now
  - Put the fault right today. The Chief queues the Studio fix; visibility and schedule changes are Ben's.

Carry forward
  - A strong start is a lesson too: note what is different about this one.
```

---

## 4. Additional Context Notes for Chief

1. **Strong performance on the cut itself:** Setting aside the missing Related video, `93JL_IK57EM` is performing well above the channel's recent baseline — `179` views at 6 h (rank `4 of 10`, vs `45` median across the last 9 checked Shorts at 6 h), `87.2%` fed (`156` Shorts-feed views), **`43.8%` stayed to watch** (vs `32.5%` channel usual), and **`88.6%` average percentage viewed** (`0:17` AVD on a `19.4 s` cut, vs `66.0%` channel usual and Studio's `61.8%–64.4%` typical range).
2. **Related video (`FAULT`):** `Related video` is `None` in Studio. `jobs/reviews/J2228/PACKAGE_MANIFEST.json`, `jobs/reviews/J2228/PACKAGE_UPLOAD_RESULT_2026-11-07T04-51-51-259Z.json` (`related_watch_next: pending_studio`), and `00_Brand/Channel-Setup/social/UPLOADS.json` (`"long": "VBaYRPp85Sw"`, `"relatedStatus": "pending_studio"`) all specify `VBaYRPp85Sw` (*What Happened to Venus?*). The Chief can queue a Studio job to set Related video → `VBaYRPp85Sw` (and update `UPLOADS.json` `relatedStatus`).
3. **Two minor listing details also observed on Video details (for Chief's call if queuing a Studio pass):**
   - **Video language & Title/description language** are both unset (`Select` in Studio; `audioLanguage` / `metadataLanguage` absent in `get_creator_videos`), so setting `en-GB` could be bundled with the Related video fix if Chief wants.
   - **Short thumbnail/cover** is currently YouTube's auto-selected mid-video still (`2.jpg`, showing `"4.3% (JUNE 2025) → 0% (WEBB, FEB 2026)"`) rather than frame 0 (`coverMs: 0`, `HIT THE MOON?`), matching `primary_thumbnail: pending_studio` in the upload result.

Per Step 5 (Step 1 found a fault; `Verdict: FAULT`), parking `J3243` for the Chief (`parked for Chief: first-day check, Verdict: FAULT`).
