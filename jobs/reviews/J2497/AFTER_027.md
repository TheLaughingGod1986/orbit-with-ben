# 027 `6bbbvfCx6zY`: after (J2497, 10 Nov 2026)

Done in YouTube Studio (CDP 9223; channel id `UC_esArsDKd3GJvOkeO0DUog` checked on the page before every click).

## What was done

1. `Edit title` clicked. Dialog: "Editing your video title will delete your A/B test including your other title options. Do you want to continue?" Continue pressed (the exception named in AGENTS.md, Never, Studio). Studio showed "Experiment deleted". T008 is gone; it had not started.
2. Title set to **What If Earth Stopped Spinning? (It's Already Slowing Down)** and saved.
3. `A/B testing` opened, `Title and thumbnail` chosen. Slot 1: the new title + `027_j2417_A_4_cm_a_year_v01.jpg` (uploaded again from the Mini, sha256 `dc1373490ab0ab37dd9c9d56dec2d33133191a3b393819c73ff9a6c0393ef8d0`). Slot 2: Earth's Day Used to Be 22 Hours (And It's Still Getting Longer) + `027_j2417_B_corals_kept_count_v01.jpg` (sha256 `b7a2cc2875f950cbc9b79528572e09855f922a8c80dde4240db775fd7e0ad46a`). Studio: "Title and thumbnail test ready". `Set test`, then Save. First try, no retry needed.

## Read-back

- Studio after a reload, title panel word for word: A/B testing titles / Ineligible / What If Earth Stopped Spinning? (It's Already Slowing Down) / Earth's Day Used to Be 22 Hours (And It's Still Getting Longer)
- Studio: two custom thumbnails on the video; visibility Scheduled; 0 views. Both thumbnails were seen in the test dialog before `Set test` (side A and side B pictures in slots 1 and 2).
- API at 2026-11-10T12:06:48.904Z: title `What If Earth Stopped Spinning? (It's Already Slowing Down)`; privacy private; publishAt 2026-11-22T18:00:00Z (same as before).
- Description: sha256 `a858107264b3c61025e24c98910f547cfcb6033c5d0b1a3f6a1351f0b7775474`, 1834 characters, identical to before. Tags: 13, same count as before.
- End screen and cards: not opened and not changed by this job. They were not read back element by element; the Studio side panel still lists both.
- Ledger: T008 closed as replaced with no result; new test **T028** in `05_Analytics/tests/THUMB_LEDGER.json`.

Not touched: privacy, schedule, description, tags, cards, end screen, any other video. £0.
