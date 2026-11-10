# 027 `6bbbvfCx6zY`: title test T008 as set, before any change (J2497)

Read 2026-11-10 about 12:00Z in YouTube Studio (CDP 9223, channel id on the page `UC_esArsDKd3GJvOkeO0DUog`, Orbit With Ben) and from the YouTube Data API at 2026-11-10T12:01:38.154Z.

## Test state

Studio title panel, word for word: A/B testing titles / Ineligible / Earth Is Losing Its Spin (And the Moon Is Taking It) / Earth's Day Used to Be 22 Hours (And It's Still Getting Longer) / A/B testing / Edit title

- State: **Ineligible** (the video is private and scheduled; Studio shows 0 views). No impressions, no "running", no results shown. The test has not started.
- Thumbnail panel state: Ineligible. Two custom thumbnails on the video (`mqdefault_custom_1`, `mqdefault_custom_2`).

## Sides (titles read from Studio; thumbnails from the J2430 record, files checked on the Mini)

| Side | Title | Thumbnail file | sha256 on the Mini now | Matches J2430 |
|---|---|---|---|---|
| A | Earth Is Losing Its Spin (And the Moon Is Taking It) | `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/08_Thumbnail/j2417_v01/027_j2417_A_4_cm_a_year_v01.jpg` | `dc1373490ab0ab37dd9c9d56dec2d33133191a3b393819c73ff9a6c0393ef8d0` | yes |
| B | Earth's Day Used to Be 22 Hours (And It's Still Getting Longer) | `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/08_Thumbnail/j2417_v01/027_j2417_B_corals_kept_count_v01.jpg` | `b7a2cc2875f950cbc9b79528572e09855f922a8c80dde4240db775fd7e0ad46a` | yes |

Studio shows the thumbnails only as small previews, so which picture sits on which side was taken from the J2430 record (slot 1 = A, slot 2 = B), not compared pixel by pixel.

## Video as it stood

- Title (API): Earth Is Losing Its Spin (And the Moon Is Taking It)
- Privacy: private; publishAt 2026-11-22T18:00:00Z; Studio visibility: Scheduled
- Description: 1834 characters, sha256 `a858107264b3c61025e24c98910f547cfcb6033c5d0b1a3f6a1351f0b7775474`; tags: 13
- Studio side panel lists End screen and Cards; this job does not open either.
