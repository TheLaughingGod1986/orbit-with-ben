# 026 `c5AdqQsnnys`: after (J2497, 10 Nov 2026)

Done in YouTube Studio (CDP 9223; channel id `UC_esArsDKd3GJvOkeO0DUog` checked on the page before every click).

## What was done

1. `Edit title` clicked. Dialog: "Editing your video title will delete your A/B test including your other title options. Do you want to continue?" Continue pressed (the exception named in AGENTS.md, Never, Studio). Studio showed "Experiment deleted". T022 is gone; it had not started.
2. Title set to **How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)** and saved.
3. `A/B testing` opened, `Title and thumbnail` chosen. Slot 1: the new title + `026_j2417_A_11_day_year_v01.jpg` (uploaded again from the Mini, sha256 `6917875bbdf207424ca4eb76a6b6f351511f9d0975b0fd81d0b5350e08f2a1a0`). Slot 2: The Star Next Door Is Invisible (And It Will Outlive Our Sun) + `026_j2417_B_trillions_of_years_v01.jpg` (sha256 `7865817d793299912836c71e0fa49852a8d24c68dd734499158afb004fe1e90b`). Studio: "Title and thumbnail test ready". `Set test`, then Save. First try, no retry needed.

## Read-back

- Studio after a reload, title panel word for word: A/B testing titles / Ineligible / How Far Is the Nearest Star? (You Can't See It, and It Has a Planet) / The Star Next Door Is Invisible (And It Will Outlive Our Sun)
- Studio: two custom thumbnails on the video; visibility Scheduled; 0 views. Both thumbnails were seen in the test dialog before `Set test` (side A and side B pictures in slots 1 and 2).
- API at 2026-11-10T12:06:48.903Z: title `How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)`; privacy private; publishAt 2026-11-15T18:00:00Z (same as before).
- Description: sha256 `0e11c159ba45af63ef97fd49b286c87847d22f61aa4f666325440697cc3df16e`, 2485 characters, identical to before. Tags: 15, same count as before.
- End screen and cards: not opened and not changed by this job. They were not read back element by element; the Studio side panel still lists both.
- Ledger: T022 closed as replaced with no result; new test **T027** in `05_Analytics/tests/THUMB_LEDGER.json`.

Not touched: privacy, schedule, description, tags, cards, end screen, any other video. £0.
