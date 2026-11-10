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

# 9 Nov 2026 (J2459): thumbnail-only test replaced by a title-and-thumbnail test

Brief: Ben's own yes, 9 Nov 2026 about 23:30 London (in chat with Claude), relayed in J2459. The Never list carries a one-video exception for this (PR #684): on `Js6EQJ8qDi8` only, pressing Continue on "Start a new experiment? This deletes your current experiment." is allowed. Done by Claude Code on the Mini, Orbit Studio, CDP 9223; channel read as **Orbit With Ben (@OrbitWithBen)** before any change.

## The old test's last state (read 2026-11-09 at about 23:39Z, before it was deleted)

- Type: **Thumbnail only**, "Test running…", "Estimated time remaining: 12 days 18 hours…".
- Arms, in Studio's order, each with the title "The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years)":
  1. `BUILT FOR 90 DAYS`: watch-time share **—** (none shown)
  2. `MINUS 90° NIGHTS`: watch-time share **—**
  3. `PLANNED 5, FLEW 72`: watch-time share **—**
- Studio showed no watch-time share and no impressions for any arm, so no result was lost.
- Screenshot (local only, PNGs are git-ignored): `_evidence/TITLE_TEST_2026-11-09_old_thumb_test_final_state.png`.

## The replacement

- **New test** pressed, then **Continue** on "Start a new experiment? This deletes your current experiment. Do you want to continue?" at **2026-11-09T23:40:35Z**.
- Studio offered Title only, Thumbnail only and **Title and thumbnail**; the last was chosen.
- Images: `08_Thumbnail/abc_v03/`. v03 is the live set (the last `PACKAGE_UPLOAD_RESULT` and `PACKAGE_MANIFEST.json` point at abc_v03; arm 1 kept the live image Studio already held).

| Arm | Title | Thumbnail |
|---|---|---|
| A, search-led (LEARNINGS rule 26) | Could a Robot Survive on Mars? (One Lasted 14 Years) | `mars_robot_thumb_A_built-for-90-days.jpg` (BUILT FOR 90 DAYS) |
| B | NASA Built This Robot to Last 90 Days on Mars. It Lasted 14 Years. | `mars_robot_thumb_B_planned-5-flew-72.jpg` (PLANNED 5, FLEW 72) |
| C, the title since 9 Nov 17:51Z | The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years) | `mars_robot_thumb_C_minus-90-nights.jpg` (MINUS 90° NIGHTS) |

- Studio said "Title and thumbnail test ready"; **Set test** pressed at **2026-11-09T23:43:14Z**; the details page then saved ("All changes saved.") at **23:43:31Z**. Arm A is the video's main title, so the details page now reads "Could a Robot Survive on Mars? (One Lasted 14 Years)".

## Read-back (23:44Z)

- A/B test report: **Title and thumbnail**, **Test running…**, the three arms above with the right image on each, "Estimated time remaining: 13 days 23 hours…" (ends about 23 Nov 2026). Watch-time share "—" on every arm so far. Screenshot: `_evidence/TITLE_TEST_2026-11-09_new_test_readback.png`.
- Details page: "A/B testing titles · Running…" listing the three titles. Visibility **Public**.
- Description: byte-for-byte the same as before the change (2,746 characters, compared against a copy taken first). Its chapter line still reads "0:00 Could a Robot Survive on Mars?".
- Not touched: description, tags, Shorts, end screen, privacy, any other video. £0.

## How to read it

The earlier before/after reading (old title vs title C) stops at 23:43Z on 9 Nov. From then, Studio's watch-time share across the three arms is the result. When Studio picks a winner, record it here and in `05_Analytics/tests/STUDIO_TESTS.md`; a win for arm A is evidence for rule 26 (search-led titles while the channel is small).
