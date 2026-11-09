# 025 title test: Orbitra "lost / still out there" shape (J2425, Mini, 9 Nov 2026)

Brief: Ben, 8 Nov 2026 22:58Z, relayed in J2425 ("go ahead without a preview"). The facts come from the locked script `01_Script/mars_robot_script_master_v01.md`: Opportunity was designed for 90 sols and worked from January 2004 until its last contact on 10 June 2018 (about 14.4 years).

## Before

- YouTube id: `Js6EQJ8qDi8`. Public since Sun 8 Nov 2026 18:00 London.
- Title: **Could a Robot Survive on Mars?**
- Thumbnail: `BUILT FOR 90 DAYS` (arm 1 of the running test below)

## Arms in the brief

| Arm | Title | Chars |
|---|---|---|
| A (control) | Could a Robot Survive on Mars? | 30 |
| B | NASA Built This Robot to Last 90 Days on Mars. It Lasted 14 Years. | 66 |
| C | The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years) | 59 |

## What Studio allowed

Studio > `Js6EQJ8qDi8` > A/B testing (CDP 9223) opened onto a test that was **already running**:

- **Thumbnail only** test, "Test running…", "Estimated time remaining: 13 days 9 minutes" (read at about 17:48Z on 9 Nov).
- Its three arms are `BUILT FOR 90 DAYS`, `MINUS 90° NIGHTS` and `PLANNED 5, FLEW 72`. No watch-time share yet. Screenshot: `TITLE_TEST_2026-11-08_running_thumb_test.png`.
- This test has no row in `05_Analytics/tests/THUMB_LEDGER.json` (no `Js6EQJ8qDi8` entry at the time of writing).

Setting up a title test would have meant pressing **New test**, which deletes the running test. The brief says the running thumbnail test stays, and the Never list forbids pressing Continue on "Run a new test? Your current test will be deleted". So a 3-way title test could not be set up without breaking a protected test. I used the brief's fallback instead.

## Applied (fallback: title changed to C)

- **Changed at 2026-11-09T17:51:36Z** (Studio "Changes saved"; Save then greyed out).
- New title: **The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years)**
- Not touched: thumbnails, the running thumbnail test, privacy, description (its chapter list still opens "0:00 Could a Robot Survive on Mars?"), tags and Shorts.

## Read-back (Studio page reloaded after the save)

- Title field: `The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years)`
- Visibility: `Public`
- A/B testing: still **Thumbnail only, Test running…**, with all three arms now showing the new title. Screenshot: `TITLE_TEST_2026-11-08_after.png`.

## How to read it

The title changed about 24 h after the video went public, so the result is a before/after comparison, not a split test. In the daily Studio read, compare impressions CTR for 8 Nov 18:00 to 9 Nov 17:51Z (old title) with the days after 9 Nov 17:51Z (title C). Don't judge on fewer than about 500 impressions on each side (`STUDIO_PLAYBOOK.md`). Launch-day traffic is different from later traffic, so read this as a hint, not proof.

Because the thumbnail test shows the same title on every arm, it stays a fair comparison of thumbnails. Arm B was not shown to viewers. Once the thumbnail test has finished, B against C could run as a real title test.
