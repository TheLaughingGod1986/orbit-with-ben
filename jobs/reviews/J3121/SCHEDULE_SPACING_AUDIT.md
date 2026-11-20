# J3121 — Scheduled OWB Shorts Spacing Audit & Mini Handoff

**Date:** 2026-11-19 (from `05_Analytics/owb/snapshots/2026-11-19.json`, `00_Brand/Channel-Setup/social/UPLOADS.json`, `BUFFER_POSTS.json`, and film `status.json` files)  
**Author:** `macbook-2`  
**Rule applied:** `05_Analytics/LEARNINGS.md` Rule 35 (same-subject Shorts spacing: no third Short in a row on the same subject — same parent long or same object; at least 1 Short on another subject between same-subject Shorts, and 2+ between when the earlier one stayed below the channel's usual 32.5% stayed-to-watch rate).  
**Scope:** Steps 2 and 3 complete here; **nothing was moved on YouTube or Buffer in this PR.** Step 1 is handed back to the Mini (see §1).

---

## 1. Step 1 Mini-only handoff (due before Fri 20 Nov 2026 10:30 London)

Under `AGENTS.md` (*Film folders on the NAS* / *Machine split*) and `scripts/jobs.py` (`macbook_studio_ok`), **YouTube privacy/schedule (`publishAt`) changes and Buffer updates are Mini-only**. `J3121` slipped past `STUDIO_BLOCK` only because the brief phrased the schedule swap as "move ... a week out" / "Swap its slot".

### Exact swap to execute on the Mini

| Video ID | Title | Old `publishAt` | New `publishAt` | Parent long (Related video) |
|---|---|---|---|---|
| `aAUgIGEuPwQ` | *The Nearest Star Is a Cherry Past Cairo. How Do We Know?* | `2026-11-20T11:30:00Z` (Fri 20 Nov) | **`2026-11-27T11:30:00Z`** (Fri 27 Nov) | `c5AdqQsnnys` (026 Nearest Star, public 15 Nov) |
| `93JL_IK57EM` | *Will Asteroid 2024 YR4 Hit the Moon in 2032?* | `2026-11-27T11:30:00Z` (Fri 27 Nov) | **`2026-11-20T11:30:00Z`** (Fri 20 Nov) | `VBaYRPp85Sw` (023 Venus, public 25 Oct) |

### Mini checklist (do in one job, no live video changes, £0)

1. **Swap `publishAt` in Studio** (move one to an interim free time if needed, or swap directly — never two Shorts on the same day, keep both Private scheduled, keep Related video links untouched, verify both in Studio afterwards).
2. **Buffer sync (critical — Never list forbids Buffer posts at a different time from YouTube go-public):**
   - `aAUgIGEuPwQ` **already has 3 live scheduled Buffer posts** in `00_Brand/Channel-Setup/social/BUFFER_POSTS.json` for `2026-11-20T11:30:00.000Z`:
     - `instagram`: `6af80829d8bd2962e411d4ac`
     - `facebook`: `6af8082a4b28296eb13edc6d`
     - `threads`: `6af8082b4b28296eb13edcab`
     Cancel or reschedule all 3 to `2026-11-27T11:30:00Z` (or cancel now so the 7-day Buffer mirror re-creates them at `2026-11-27T11:30:00Z`) and update `BUFFER_POSTS.json`.
   - `93JL_IK57EM` is **not in `BUFFER_POSTS.json` yet** (was outside the 7-day window). Moving it to Fri 20 Nov 11:30Z puts it inside the window immediately: mirror `93JL_IK57EM` to Buffer for `2026-11-20T11:30:00Z` (`buffer-mirror.ts mirror --video 93JL_IK57EM ...` or `check`) and update `BUFFER_POSTS.json`.
3. **Update records (leaving uploaded manifests/sha256 intact per Never list):**
   - `00_Brand/Channel-Setup/social/UPLOADS.json`: update `publishAt` for both `aAUgIGEuPwQ` and `93JL_IK57EM` (plus `bufferStatus`).
   - `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/status.json`: note `aAUgIGEuPwQ` moved `2026-11-20T11:30:00Z` → `2026-11-27T11:30:00Z`.
   - `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/status.json`: note `93JL_IK57EM` moved `2026-11-27T11:30:00Z` → `2026-11-20T11:30:00Z`.
   - Add a small schedule-swap note beside `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/fri20_grapefruit_cherry/11_Upload-Package/J1101_v04_swap/` and `jobs/reviews/J2228/` recording old → new `publishAt` (do **not** overwrite uploaded `PACKAGE_MANIFEST.json` or its sha256).
   - Update `shorts_open_library` via `gate_shorts_open.py status` if tracked there, and post the state-change line on the studio thread (Standing Lesson 6).

---

## 2. Step 3 Audit — All scheduled OWB Shorts (19 Nov – 16 Dec 2026)

*Assumes Step 1 swap (`aAUgIGEuPwQ` 20 Nov ↔ `93JL_IK57EM` 27 Nov) completes. Nothing moved in Step 3.*

### Full scheduled calendar against Rule 35

| Date (11:30 London/UTC) | Video ID | Title | Subject / Parent long (parent airs) | Constraints | Rule 35 status |
|---|---|---|---|---|---|
| Thu 19 Nov | `HXacmpYkXcA` | How Close Will the Supermoon Get on November 24? | Supermoon dated event (`2fsQcea-voM`, public) | **Date-tied** (stays); Buffer live | **PASS** |
| Fri 20 Nov | `93JL_IK57EM` *(post-Step 1)* | Will Asteroid 2024 YR4 Hit the Moon in 2032? | AR1 / Asteroid 2024 YR4 (`VBaYRPp85Sw`, public) | Step 1 swap target | **PASS** |
| Sat 21 Nov | `gc1hWQQJOq4` | Muons Shouldn't Reach the Ground. They Do. | 024 Light Speed (`rVqgtkBV3jc`, public) | Buffer live | **PASS** |
| Mon 23 Nov | `Dm4xsF1Ateg` | Why Do You Weigh Less at Earth's Equator? | 027 Earth Spin (`6bbbvfCx6zY`, Sun 22 Nov 18:00) | Rule 31 readout (no move); Buffer live | **PASS** |
| Wed 25 Nov | `_dVWVUnbDzA` | Where Will the International Space Station Crash? | AR2 / ISS deorbit (`VBaYRPp85Sw`, public) | Rule 31 readout (no move); Buffer live | **PASS** |
| Thu 26 Nov | `GbELka8Yu9U` | Why Is Jupiter Beside the Moon on November 30? | Jupiter–Moon dated event (`-jmMROGoZCM`, public) | **Date-tied** (stays) | **PASS** |
| Fri 27 Nov | `aAUgIGEuPwQ` *(post-Step 1)* | The Nearest Star Is a Cherry Past Cairo. How Do We Know? | 026 Nearest Star (`c5AdqQsnnys`, public) | Step 1 swap target (6 Shorts / 9 d clear of `dH_yCRmzkMo`) | **PASS** |
| Sat 28 Nov | `MScK2CK2ZFg` | Where Will the 2027 Total Solar Eclipse Last Over Six Minutes? | AR3 / 2027 Eclipse (`VBaYRPp85Sw`, public) | Rule 31 readout (no move) | **PASS** |
| **Mon 30 Nov** | `xvarZP2aYyE` | Why Will Gliese 710's Comets Arrive After It Has Gone? | **028 Gliese 710** (`F-jImX5h7ws`, Sun 29 Nov 18:00) | Earliest allowed: 30 Nov | **CLASH A (#1 of 3 in a row)** |
| **Wed 2 Dec** | `v6euXX2omz4` | Is a Star Really Coming Towards Us? | **028 Gliese 710** (`F-jImX5h7ws`, Sun 29 Nov 18:00) | Test A opening Short | **FAIL — 2nd consecutive 028 (0 between)** |
| **Fri 4 Dec** | `BTuL_QBbEgY` | How Close Will Gliese 710 Come to the Sun? | **028 Gliese 710** (`F-jImX5h7ws`, Sun 29 Nov 18:00) | Evergreen | **FAIL — 3rd consecutive 028 (0 between)** |
| Sat 5 Dec | `5qw8oW5Pwpc` | What Happens When Earth's Magnetic Field Flips? | 031 Magnetic Field (`G5uMANXHtNU`, Wed 2 Dec 18:00) | Test A; earliest allowed: Thu 3 Dec | **PASS** (only 1 divider between 028 #3 and #4) |
| **Mon 7 Dec** | `lsOCcIYCud0` | What Will the Night Sky Look Like When Gliese 710 Arrives? | **028 Gliese 710** (`F-jImX5h7ws`, Sun 29 Nov 18:00) | Evergreen | **AT RISK — 4th 028 in 8 days** (only 1 divider after 4 Dec; fails 2-Short gap if earlier 028 stays `<32.5%`) |
| **Wed 9 Dec** | `rXKIOUoZSGg` | Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light? | **029 Betelgeuse** (`vP1BbqZ_dnM`, Sun 6 Dec 18:00) | Earliest allowed: Mon 7 Dec | **CLASH B (#1 of 2 in a row)** |
| **Fri 11 Dec** | `k2kEaA7ICjc` | Is Betelgeuse Really About to Explode? | **029 Betelgeuse** (`vP1BbqZ_dnM`, Sun 6 Dec 18:00) | Test A opening Short | **FAIL — 2nd consecutive 029 (0 between)** |
| Sat 12 Dec | `QEoYKIVvKBA` | What If the Solar Wind Blew Earth's Atmosphere Into Space? | 031 Magnetic Field (`G5uMANXHtNU`, Wed 2 Dec 18:00) | Earliest allowed: Thu 3 Dec | **PASS** (3 Shorts after `5qw8oW5Pwpc`) |
| **Mon 14 Dec** | `heiGCnGKTkE` | How Bright Will Betelgeuse Get When It Explodes? | **029 Betelgeuse** (`vP1BbqZ_dnM`, Sun 6 Dec 18:00) | Evergreen | **WATCH — 3rd 029 in 6 days** (1 divider after 11 Dec; fails 2-Short gap if 11 Dec stays `<32.5%`) |
| Wed 16 Dec | `f17XCtUmN-g` | What Happens When Gliese 710 Passes Through the Oort Cloud? | 028 Gliese 710 (`F-jImX5h7ws`, Sun 29 Nov 18:00) | Evergreen | **PASS** (4 Shorts / 9 d after `lsOCcIYCud0`) |

### Unuploaded / queued Shorts that also clash before upload

| Queued job | Planned slot | Subject / Parent long (parent airs) | Finding |
|---|---|---|---|
| `J0979` (`032_short_fri27_opening_testA_v02.mp4`) | Fri 27 Nov 11:30 *(target)* | 032 Titan Test A (`T3cBBss1F60`, **Wed 25 Nov 18:00**; Ben UAT due 20 Nov) | **Slot already taken** by `93JL_IK57EM` now and `aAUgIGEuPwQ` after Step 1 (never two Shorts on one day). Ideal non-star divider for **Wed 2 Dec 11:30** once Ben approves. |
| `J2896` + `J2895` | **Fri 18 Dec** + **Sat 19 Dec** | **033 Uranus** Shorts 1 & 2 (`oASsmqZfWU4`, Wed 9 Dec 18:00) | **FAIL — back-to-back Uranus (0 Shorts between).** |
| `J3066` + `J3065` | **Mon 21 Dec** + **Wed 23 Dec** | **034 Pluto** Shorts 1 & 2 (long Sun 13 Dec 18:00) | **FAIL — back-to-back Pluto (0 Shorts between).** |

---

## 3. Proposed swaps for the Chief (move nothing yet)

All proposals obey every hard constraint:
- Never two Shorts on one day.
- Never a Short before its parent long is public (`028` ≥ 30 Nov; `032` ≥ 26 Nov; `031` ≥ 3 Dec; `029` ≥ 7 Dec; `033` ≥ 10 Dec; `034` ≥ 14 Dec).
- Dated-event Shorts (`HXacmpYkXcA` 19 Nov, `GbELka8Yu9U` 26 Nov) and Rule 31 readout Shorts (`Dm4xsF1Ateg` 23 Nov, `_dVWVUnbDzA` 25 Nov, `MScK2CK2ZFg` 28 Nov) stay untouched.
- Zero same-subject Shorts back-to-back; 2+ Shorts between same-subject cuts wherever possible.

### Option A (Recommended — uses `032` Titan Test A from `J0979` once Ben passes UAT by 20 Nov)

Because `J0979` (`032` Titan Test A) already cannot use its colliding Fri 27 Nov slot and its parent `T3cBBss1F60` goes public Wed 25 Nov 18:00, slotting it on **Wed 2 Dec 11:30** resolves the Mon 30 Nov / Wed 2 Dec Gliese 710 clash without leaving an empty slot or putting another star Short in between:

| Date (11:30) | Proposed Short | Subject | Change from current schedule | Gap since previous same-subject |
|---|---|---|---|---|
| Mon 30 Nov | `xvarZP2aYyE` *(or `v6euXX2omz4` Test A)* | 028 Gliese 710 #1 | Keep (or swap with `v6euXX2omz4` so Test A leads) | — |
| **Wed 2 Dec** | **`032` Titan Test A (`J0979`)** | **032 Titan** | New slot (replaces colliding 27 Nov target) | — |
| **Fri 4 Dec** | `5qw8oW5Pwpc` | 031 Magnetic Field #1 | Move from Sat 5 Dec *(parent public 2 Dec 18:00)* | — |
| **Sat 5 Dec** | `v6euXX2omz4` *(or `BTuL_QBbEgY`)* | 028 Gliese 710 #2 | Move from Wed 2 Dec / Fri 4 Dec | **2 Shorts between** |
| **Mon 7 Dec** | `rXKIOUoZSGg` | 029 Betelgeuse #1 | Move from Wed 9 Dec *(parent public 6 Dec 18:00)* | — |
| **Wed 9 Dec** | `QEoYKIVvKBA` | 031 Magnetic Field #2 | Move from Sat 12 Dec | **2 Shorts between** |
| **Fri 11 Dec** | `BTuL_QBbEgY` *(or `lsOCcIYCud0`)* | 028 Gliese 710 #3 | Move from Fri 4 Dec / Mon 7 Dec | **2 Shorts between** |
| **Sat 12 Dec** | `k2kEaA7ICjc` | 029 Betelgeuse #2 (Test A) | Move from Fri 11 Dec | **2 Shorts between** |
| **Mon 14 Dec** | `lsOCcIYCud0` *(or `033` Uranus #1 `J2896`)* | 028 Gliese 710 #4 *(or 033 Uranus)* | Move from Mon 7 Dec | **1 Short between** *(2+ if Uranus takes Mon 14 Dec)* |
| **Wed 16 Dec** | `heiGCnGKTkE` | 029 Betelgeuse #3 | Move from Mon 14 Dec | **1 Short between** *(2+ if Mon 14 & Tue/Thu dated Short intervene)* |
| **Fri 18 Dec** | `033` Uranus #1 (`J2896`) | 033 Uranus #1 | Keep `J2896` slot | — |
| **Sat 19 Dec** | `f17XCtUmN-g` | 028 Gliese 710 #5 | Move from Wed 16 Dec | **2 Shorts between** |
| **Mon 21 Dec** | `034` Pluto #1 (`J3066`) | 034 Pluto #1 | Keep `J3066` slot | — |
| **Wed 23 Dec** | `033` Uranus #2 (`J2895`) | 033 Uranus #2 | Move `J2895` from Sat 19 Dec | **2 Shorts between** |
| **Fri 25 / Sat 26 Dec** | `034` Pluto #2 (`J3065`) | 034 Pluto #2 | Move `J3065` from Wed 23 Dec | **1+ Shorts between** |

### Option B (Minimal fallback — strictly already-scheduled Shorts only, if `J0979` is not approved in time)

If no new Short is ready by Wed 2 Dec:
1. **Break `Fri 4 Dec` (028) & `Mon 7 Dec` (028) and `Wed 9 Dec` (029) & `Fri 11 Dec` (029) with two direct swaps:**
   - Swap `BTuL_QBbEgY` (Fri 4 Dec, 028) ↔ `5qw8oW5Pwpc` (Sat 5 Dec, 031 Magnetic Field — parent public Wed 2 Dec 18:00).
   - Swap `lsOCcIYCud0` (Mon 7 Dec, 028) ↔ `rXKIOUoZSGg` (Wed 9 Dec, 029 Betelgeuse — parent public Sun 6 Dec 18:00).
   - Result from Fri 4 Dec through Wed 16 Dec: `4 Dec 031 → 5 Dec 028 → 7 Dec 029 → 9 Dec 028 → 11 Dec 029 → 12 Dec 031 → 14 Dec 029 → 16 Dec 028` (**zero adjacent same-subject Shorts from 4 Dec onward**).
2. **Break the remaining `Mon 30 Nov` (`xvarZP2aYyE`, 028) + `Wed 2 Dec` (`v6euXX2omz4`, 028) pair:**
   - Push `v6euXX2omz4` (or `xvarZP2aYyE`) to **Sat 19 Dec** (or Fri 18 Dec, pushing `J2895` Uranus #2 to Wed 23 Dec), leaving Wed 2 Dec open for the early-December dated-event Short (`owb-dated-short`) or `032` Titan Test A (`J0979`) once approved (never fill with an unapproved cut).
3. **Before upload, interleave `J2896`/`J2895` (Uranus) and `J3066`/`J3065` (Pluto):**
   - `Fri 18 Dec` Uranus #1 (`J2896`) → `Mon 21 Dec` Pluto #1 (`J3066`) → `Wed 23 Dec` Uranus #2 (`J2895`) → `Fri 25 / Sat 26 Dec` Pluto #2 (`J3065`).

### Note on `scripts/jobs.py` routing guard (for Chief awareness)

`macbook_studio_ok` (`scripts/jobs.py`) is documented to exclude privacy and schedule changes from the MacBook, and `STUDIO_BLOCK` matches `\b(?:change|set|move|make)\b[^.\n]{0,24}\b(?:privacy|schedule|publishAt|public)\b`. `J3121` bypassed that regex because the brief used *"move tomorrow's ... Short a week out"*, *"Swap its slot"*, and *"Moves only private scheduled Shorts"*. Not changed in this PR (outside J3121's scope); flagged for a follow-up guard tweak if desired.
