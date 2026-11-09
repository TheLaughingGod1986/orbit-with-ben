# J2369 Chief Review — Weekly Dated-Event Short (`24 November 2026 Full Supermoon`, `LEARNINGS` Rule 16 Test)

- **Job**: `J2369` (`Backlog OWB: this week's dated-event Short (LEARNINGS rule 16 test), script + packaging, park for Chief`, `kind: script`, `backlog: owb-dated-short`)
- **Deliverable Reviewed**: PR #642 (`macbook/J2369`, commit `6d44167fdbf63ab21f2adfbf06c8cfc35a22a74e`, `02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md`)
- **Reviewer**: `gemini` (Elected Acting Chief under Ben's 26 Oct 2026 succession chain; `chief_relay.py status` re-verified at `2026-11-08T19:14Z`: `chief` down, `claude` down `4043 min`, `codex` down on usage limit until `2026-11-08T19:28:14Z`, `gemini` UP)
- **Verdict**: **EVENT, OFFICIAL NASA SOURCES & SAT 21 NOV 2026 11:30 UTC SLOT `PASS`; SCRIPT & PICTURE PLAN `FIX` (5 concrete corrections required on PR #642 `02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md` before `script PASS` and any VO spend). Reopen `J2369` to apply the 5 fixes on PR #642 (`£0` spend).**

---

## 1. What Passes (`KEEP` in `2026-11-24_supermoon-two-earths-closer.md`)

1. **Event Selection & Non-Overlap (`PASS`):**
   - **Event**: **24 November 2026 Full Supermoon (`14:54 UTC`) & Lunar Perigee (`25 November 2026, 21:00 UTC`)**, the first of three consecutive full Supermoons (17 days ahead of 7 Nov 2026, inside the `10–21 days ahead` brief window).
   - **Non-overlap verified**: Checked against `00_Brand/Channel-Setup/social/UPLOADS.json`, `05_Analytics/kanban/film_briefs.json`, `05_Analytics/owb/snapshots/2026-11-08.json`, `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/SCRIPTS_v01.md`, and the Apophis Replication cohort (`J1356` / `AR1`–`AR4`). Voyager 1 (`kKN8Ale42sE`, 17 Nov), Leonids (`T9fVlG3CCzU`, 7 Nov), and Uranus (`ZpEA8stoSPA`, 3 Nov; `033` Shorts) were rightly skipped. No open, scheduled, or live OWB Short covers the 24 November 2026 Supermoon / perigee.

2. **Official NASA Sources & Numbers (`PASS`):**
   - Directly verified against live NASA pages and the NASA SVS #5587 Dial-A-Moon Ephemeris API on `2026-11-08T19:11Z`:
     - **`S1` / `S1b`**: NASA Science — *Supermoons: In Depth* (`https://science.nasa.gov/solar-system/moon/what-is-a-supermoon/`) confirms `"Upcoming Supermoons: November 24, 2026 (14:54 UTC)"` and `"14 percent bigger and 30 percent brighter"`.
     - **`S2`**: NASA Science — *What's Up: November 2026 Skywatching Tips from NASA* (`https://science.nasa.gov/solar-system/skywatching/whats-up-november-2026-skywatching-tips-from-nasa/`) confirms `"Nov. 24: Full supermoon; first in a series of three consecutive supermoons"` and `"Look east around sunset to watch it rise."`
     - **`S3`**: NASA Science — *Moon Facts* (`https://science.nasa.gov/moon/facts/`) confirms `"If Earth were the size of a nickel, the Moon would be about as big as a coffee bean. The Moon is an average of 238,855 miles (384,400 kilometers) away. That means 30 Earth-sized planets could fit in between Earth and the Moon."`
     - **`S4` & `S5`**: NASA SVS #5587 (`https://svs.gsfc.nasa.gov/5587`) confirms `"ranging between 28 and 32 Earth diameters, or about 356,400 and 406,700 kilometers"`. Live API queries confirm `https://svs.gsfc.nasa.gov/api/dialamoon/2026-11-24T15:00` → `{"time": "2026-11-24T15:00", "phase": 99.81, "distance": 360755.0, "diameter": 1986.7}` (`23,645 km` closer than `384,400 km`, ~`28` vs `30` Earth diameters) and `https://svs.gsfc.nasa.gov/api/dialamoon/2026-11-25T21:00` → `{"time": "2026-11-25T21:00", "phase": 97.51, "distance": 359336.0, "diameter": 1994.6}` (`25,064 km` closer).

3. **Target Publish Slot & Packaging Hook (`PASS`):**
   - **Locked Target Slot**: **Saturday, 21 November 2026 at 11:30 UTC (London)** (3 days / 75 hours before the event, inside the `3–7 days before` Rule 16 window; standard OWB `Mon/Wed/Fri/Sat 11:30 London` slot, verified empty in `05_Analytics/owb/snapshots/2026-11-08.json`).
   - **Title (`48 chars <= 50`)**: `How Close Will the Supermoon Get on November 24?` (plain positive question naming the subject and the date hook).
   - **Frame-0 Hook Caption (`0.0–2.0 s`, 3 words)**: `**TWO EARTHS** CLOSER` (distinct from title).
   - **Cover Text (3 words)**: `**24,000 KM** / NEARER` (no words shared with title).
   - **Related Video**: `2fsQcea-voM` (*Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone*, public Long `013`).

---

## 2. Five Required Fixes on PR #642 (`02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md`)

Before `J2369` receives `script PASS` and unlocks VO/assembly, update `02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md` on PR #642 to fix these five concrete defects:

1. **Replace labelled `phases_2026_fancy_*` (`s01`, `s06`) with unlabelled `phases_2026_plain_*` (`picture_qa.py` / Lesson 7 gate):**
   - In NASA SVS #5587 (`https://svs.gsfc.nasa.gov/api/5587`), `phases_2026_fancy_2160p30.mov` (`media_group_379010`) and `phases_2026_fancy_720p30.mp4` include **baked-in crater/maria/Apollo landing-site text labels and supplemental orbital/subsolar graphics**, which **FAIL `picture_qa.py`**.
   - Update `s01` (`0.00–2.65 s`) and `s06` (`13.10–16.45 s`) to use NASA SVS #5587's **unlabelled plain** Moon animations: `phases_2026_plain_2160p30.mp4` / `phases_2026_plain_1080p30.mp4` (`media_group_379015`, `https://svs.gsfc.nasa.gov/vis/a000000/a005500/a005587/phases_2026_plain_2160p30.mp4`) or portrait `phases_2026_plain_v_1920p30.mp4` (`media_group_379014`, `"showing only the Moon"`), and unlabelled frame `frames/3840x2160_16x9_30p/plain/comp.7864.tif` (never the labelled `fancy` render).

2. **Replace external diagram `moon_distance_2026_1080p30.mp4` in `s04` (`6.15–9.40 s`) (`picture_qa.py` / Lesson 7 gate):**
   - Under `AGENTS.md` Lesson 7 and *Teach on screen*, pulling any chart, diagram, or labelled animation from a source (`moon_distance_2026_1080p30.mp4`, `media_group_379020`: *"An animated diagram of the Moon's distance from the Earth"*) **FAILs `picture_qa.py`**.
   - Replace `s04` (`6.15–9.40 s`, *"Normally thirty Earths fit across"*) with an unlabelled real-body visual: either our own unlabelled `code_graphics.py` true-scale Earth-to-Moon span render using real NASA Blue Marble Earth (`GSFC_20171208_Archive_e002130.jpg`) and Moon (`GSFC_20171208_Archive_e001939.jpg`) discs over graded dark space (zero text/labels), or a clean unlabelled NASA Earth/Moon plate from `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/`.

3. **Replace `ISS_sunrise_to_sunset.ogv` in `s07` (`16.45–18.80 s`) (`CHIEF_H37` C4b asset rule):**
   - Per `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/CHIEF_H37_CORRECTIONS.md` C4(b), `ISS_sunrise_to_sunset.ogv` shows the tail fin of Space Shuttle **Discovery** (with `"Discovery"` painted on it) and contains no rising Moon, contradicting `s07`'s description (*"pushing toward the rising Moon to match s01 at 18.80 s"*).
   - Replace `s07` (`16.45–18.80 s`, *"Look east at sunset, as…"* + `1.00 s` loop tail) with `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/moon/s103e5050.jpg` (NASA STS-103 photo of the full Moon shining through Earth's glowing blue-orange sunset atmosphere limb, verified on NAS at `2,250,538` bytes / `s103e5050.jpg`) or `phases_2026_plain_2160p30.mp4` rising over a clean cropped Earth twilight limb, framed so the `17.80–18.80 s` loop tail bridges cleanly into `s01` Frame 0 (`≤0.3 s` crossfade per `OWB-2026-11-E1`).

4. **Enforce the 1-overlay Short cap in `[VISUAL MUST]` & Shot List (`AGENTS.md` *Teach on screen*):**
   - A Short allows **at most one teach overlay** (`≤4 words` per label, inside the `16:9` centre band, clear of `0–2 s` and the `9–14 s` title banner).
   - In `[VISUAL MUST]` (line 119) and `s02` (line 173), remove the extra `coffee-bean-to-nickel scale badge`, remove the `orbital diagram (30 Earth diameters)` at `6.15 s`, and remove `WHEN: 24 Nov 2026` at `13.25 s`, keeping **only** the single animated `DATA` scale bar at `13.25–16.35 s` (`384,400 KM (30 EARTHS)` → `360,000 KM (28 EARTHS)` · `SCALE: two Earths closer`). `s02`/`s03` show the real Blue Marble Earth (`GSFC_20171208_Archive_e002130.jpg`) and LRO Moon (`GSFC_20171208_Archive_e001939.jpg`) discs side by side at true `1 : 3.67` diameter scale with no text/badge overlay.

5. **Add Pre-Approved `C7` VO Trim Hierarchy + Fix Fabricated §3 Schedule Titles & Off-Cadence Thursday Fallback:**
   - **Pre-approved `C7` VO trim hierarchy (`CHIEF_H37` C7 / `CHIEF_H40` lesson)**: In `J1306`, 46-word 5-sentence scripts with multi-digit spelled-out numbers ran `24.0–27.2 s` in `eleven_v3` with answer starts at `16.5–19.1 s`. Add a binding **Pre-Approved VO Trim Order (`C7`)** in §4 so that if the 46-word primary take exceeds the `17.0–20.0 s` Rule 16 Apophis-mould cut bar (`VO + 1.00 s loop tail`) or starts Line 4 past `13.5 s`, the VO job applies these deterministic trims in order (or splices at room-tone points per `CHIEF_H40_VO_LOCK.md`):
     1. *Trim 1*: shorten Line 3 from *"Normally thirty Earths fit across three hundred and eighty-four thousand kilometres."* (`11` words) to *"Normally thirty Earths fit between us."* (`6` words; total `41` words; `384,400 KM (30 EARTHS)` stays on the `DATA` scale bar).
     2. *Trim 2*: if still over `20.0 s` cut / `13.5 s` answer start, drop Line 2 (*"If Earth were a nickel, the Moon is a coffee bean."*), keeping full Line 3 *"Normally thirty Earths fit across three hundred and eighty-four thousand kilometres."* as the everyday 30-Earths scale comparison (`35` words, `4` sentences, matching `AR1 v03` `33w` / `AR3 v03` `31w`).
   - **Fix fabricated §3 schedule titles (`lines 83–88`)**: Replace the three wrong titles in §3 with the exact titles from `05_Analytics/owb/snapshots/2026-11-07.json` / `2026-11-08.json`:
     - `Wed 18 Nov 2026, 11:30 UTC`: `cwU_0WWeNZ4` — *If Voyager Needs 75,000 Years, How Far Is the Nearest Star?* (`026` Short #2)
     - `Fri 20 Nov 2026, 11:30 UTC`: `aAUgIGEuPwQ` — *The Nearest Star Is a Cherry Past Cairo. How Do We Know?* (`026` Short #3)
     - `Mon 23 Nov 2026, 11:30 UTC`: `Dm4xsF1Ateg` — *Why Do You Weigh Less at Earth's Equator?* (`027` Short #1)
   - **Remove off-cadence Thursday fallback (`lines 94, 204`)**: OWB Shorts air only on **Monday, Wednesday, Friday, and Saturday at 11:30 London** (`AGENTS.md` Locked Weekly Targets; `jobs/reviews/J2023/PLAN.md`: *"Leave Tue/Thu/Sun free under the current Mon/Wed/Fri/Sat rule"*). Remove `Thursday, 19 November 2026 at 11:30 UTC` / `fallbackPublishAt` and lock **Saturday, 21 November 2026 at 11:30 UTC** as the sole target slot.
