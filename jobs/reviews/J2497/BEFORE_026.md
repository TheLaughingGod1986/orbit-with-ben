# 026 `c5AdqQsnnys`: title test T022 as set, before any change (J2497)

Read 2026-11-10 about 12:00Z in YouTube Studio (CDP 9223, channel id on the page `UC_esArsDKd3GJvOkeO0DUog`, Orbit With Ben) and from the YouTube Data API at 2026-11-10T12:01:38.153Z.

## Test state

Studio title panel, word for word: A/B testing titles / Ineligible / The Nearest Star Is One You Can't See (And It Has a Planet) / The Star Next Door Is Invisible (And It Will Outlive Our Sun) / A/B testing / Edit title

- State: **Ineligible** (the video is private and scheduled; Studio shows 0 views). No impressions, no "running", no results shown. The test has not started.
- Thumbnail panel state: Ineligible. Two custom thumbnails on the video (`mqdefault_custom_1`, `mqdefault_custom_2`).

## Sides (titles read from Studio; thumbnails from the J2430 record, files checked on the Mini)

| Side | Title | Thumbnail file | sha256 on the Mini now | Matches J2430 |
|---|---|---|---|---|
| A | The Nearest Star Is One You Can't See (And It Has a Planet) | `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/08_Thumbnail/j2417_v01/026_j2417_A_11_day_year_v01.jpg` | `6917875bbdf207424ca4eb76a6b6f351511f9d0975b0fd81d0b5350e08f2a1a0` | yes |
| B | The Star Next Door Is Invisible (And It Will Outlive Our Sun) | `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/08_Thumbnail/j2417_v01/026_j2417_B_trillions_of_years_v01.jpg` | `7865817d793299912836c71e0fa49852a8d24c68dd734499158afb004fe1e90b` | yes |

Studio shows the thumbnails only as small previews, so which picture sits on which side was taken from the J2430 record (slot 1 = A, slot 2 = B), not compared pixel by pixel.

## Video as it stood

- Title (API): The Nearest Star Is One You Can't See (And It Has a Planet)
- Privacy: private; publishAt 2026-11-15T18:00:00Z; Studio visibility: Scheduled
- Description: 2485 characters, sha256 `0e11c159ba45af63ef97fd49b286c87847d22f61aa4f666325440697cc3df16e`; tags: 15
- Studio side panel lists End screen and Cards; this job does not open either.
