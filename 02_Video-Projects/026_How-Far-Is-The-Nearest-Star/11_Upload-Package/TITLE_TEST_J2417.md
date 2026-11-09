# 026 title + thumbnail-text test (J2417, MacBook, 8 Nov 2026)

Shape: Orbitra's two hits (*"When Our Solar System Lost a Planet (And It Might Still Be Out There)"* 38k; *"Our Sun Had a Twin (And It's Still Out There)"* 21k). A hidden or missing thing, then why it still matters, in a bracketed tail. Every fact comes from the locked script `01_Script/nearest_star_script_master_v01.md`.

## Before (live on the private scheduled upload)

- YouTube id: `c5AdqQsnnys` (Private, publishAt 2026-11-15T18:00Z)
- Title: **Why Reaching the Nearest Star Takes 75,000 Years**
- Thumbnail: A set (`08_Thumbnail/abc_v04`, J1944 ruling)

## Candidates

| # | Title | Chars | Script line it rests on |
|---|---|---|---|
| 1 | **The Nearest Star Is One You Can't See (And It Has a Planet)** | 59 | "You cannot see that star at all. Not without a telescope." / "In 2016 astronomers found a planet around Proxima." |
| 2 | **The Star Next Door Is Invisible (And It Will Outlive Our Sun)** | 61 | "Proxima will still be glowing for trillions of years, long after our own Sun has gone." |
| 3 | Our Nearest Star Hides in Plain Sight (And It's 4 Light-Years Away) | 67 | "A faint red sun you cannot see, more than four light-years away" |

## Pick for Test & Compare

| Arm | Title | Thumbnail text (2-4 words, no title words) | One big object |
|---|---|---|---|
| A | The Nearest Star Is One You Can't See (And It Has a Planet) | **11-DAY YEAR** | Proxima b as a dark crescent against a small red star (ESO impression, labelled as one in the description as now) |
| B | The Star Next Door Is Invisible (And It Will Outlive Our Sun) | **TRILLIONS OF YEARS** | Proxima, a single red dot, huge, on black. High contrast, no other stars |

Why these two: A sells the planet (the thing still out there), B sells the star itself. They are deliberately far apart so the test can pick a winner at our impressions (T012/T014/T015 drew because the arms were too alike). Candidate 3 dropped: "in plain sight" is wrong, it is *not* in sight.

Payoff check: both are paid off in the film (planet: chapter "Is Anyone There?"; outlives the Sun: chapter "The Star You Cannot See"). No fear framing, no hedge, no hashtag, no series suffix.

## After (applied 2026-11-09T01:42Z, J2430)

- **Built thumbnails (`08_Thumbnail/j2417_v01`, `abc_*` untouched):**
  - **Arm A:** `026_j2417_A_11_day_year_v01.jpg` (`SHA-256: 6917875bbdf207424ca4eb76a6b6f351511f9d0975b0fd81d0b5350e08f2a1a0`, **11-DAY YEAR**, Proxima b dark crescent against small red star `eso1629e`, no Orbit) — `thumb_preview.py --score`: `PASS  026_j2417_A_11_day_year_v01.jpg  saturation=193.1  near_black=8%`
  - **Arm B:** `026_j2417_B_trillions_of_years_v01.jpg` (`SHA-256: 7865817d793299912836c71e0fa49852a8d24c68dd734499158afb004fe1e90b`, **TRILLIONS OF YEARS**, single huge red Proxima on black from `potw1343a`, high contrast, no other stars, no Orbit) — `thumb_preview.py --score`: `PASS  026_j2417_B_trillions_of_years_v01.jpg  saturation=210.6  near_black=17%`
  - **168×94 preview sheet:** `026_j2417_preview_sheet_v01.jpg` (`SHA-256: 0256a68bc84bfcea83ae4b35fa0264b525e240091aebcb11ee02db6f9dcd1e10`)
- **Applied in YouTube Studio (`c5AdqQsnnys`, CDP 9223, `Title and thumbnail` Test & Compare, `T022` in `05_Analytics/tests/THUMB_LEDGER.json`):**
  - No prior test was running (`#ab-test-button` showed `"A/B testing"`).
  - **Slot 1 (Arm A):** Title `The Nearest Star Is One You Can't See (And It Has a Planet)` + Thumbnail `026_j2417_A_11_day_year_v01.jpg`
  - **Slot 2 (Arm B):** Title `The Star Next Door Is Invisible (And It Will Outlive Our Sun)` + Thumbnail `026_j2417_B_trillions_of_years_v01.jpg`
  - **Saved & Read Back (YouTube Data API v3):** `title: "The Nearest Star Is One You Can't See (And It Has a Planet)"`, `privacyStatus: "private"`, `publishAt: "2026-11-15T18:00:00Z"`, `madeForKids: false`, `defaultLanguage: "en-GB"`, `defaultAudioLanguage: "en-GB"`, Studio `saveDisabled: true` (`All changes saved.`).

Deadline (Ben): before Sun 15 Nov 17:00 London.
