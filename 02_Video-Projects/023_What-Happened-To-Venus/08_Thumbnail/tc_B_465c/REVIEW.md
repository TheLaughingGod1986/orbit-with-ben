# J2484 / J2487 — 023 Venus (`VBaYRPp85Sw`) Thumbnail Test & Compare B: `'465°C'` (Fixed per `J2486`)

- **Video:** `023_What-Happened-To-Venus` (`VBaYRPp85Sw` — *What Happened to Venus?*, title unchanged)
- **Context:** `T011` (`A: MELTS LEAD` vs `B: EARTH'S TWIN`) ended 9 Nov 2026 01:10 UTC as a draw (*"Not enough impressions to declare a winner"*, `A: MELTS LEAD` visible to all). Per Chief ruling on `J1198` (29 Oct / 10 Nov 2026) and `05_Analytics/LEARNINGS.md` rules 11–13, the draw branch tests a genuinely different visual concept with a clear scale/stakes element (`LEARNINGS.md` rule 12) rather than another planet globe.
- **J2487 Fixes Applied (per `J2486` independent design review):**
  1. **Physical Accuracy at `465°C` (below the `~525°C` Draper point):** Replaced `venus_surface_glowing_lander_plate.jpg` with `venus_surface_465c_lander_plate.jpg` (`SHA256: 3374c505401ac19f3bbe902a2d5298fc0069ca911d46a4acdd90218c96892bbc`) and removed all additive red-orange `lander_glow` / `sphere_glow` boosts in `build_venus_tc_b_465c_j2484.py`. The lower hull, landing ring, and struts sit in natural cast shadow underneath the scalloped aerobrake collar (`0.0%` of lower hull pixels have `R >= 245`, down from `31.4%`), the red-lit ground pool beneath the lander is gone, and the basalt slabs have no molten red lava cracks. Only the warm amber-orange atmospheric sky cast illuminates the metallic lander from above.
  2. **Grade / Saturation (`183.3` vs `245.5`):** Brought mean HSV saturation down from `245.5 / 255` (`59.4%` of pixels pinned at `S >= 250`) to **`183.3 / 255`** (`1.97%` of pixels at `S >= 250`, almost exclusively the yellow `(255, 230, 0)` `"465°C"` hook text), matching the channel's `139.0–186.5` range and Venus search neighbours (Cool Worlds `119.2`, Astrum `208.0`), with `near_black = 24%` (`<= 30%` ceiling).
  3. **Provenance (`META.json`):** Recorded full `plate_provenance` for both `venus_surface_465c_lander_plate.jpg` (`J2487`, session `614a7af3` -> `3faf01da`, `2026-11-10T06:22:16Z`, **£0**) and the superseded `J2484` plate (`venus_surface_glowing_lander_plate.jpg`, **£0**).
- **Deliverable:** `02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_tc_B_465c_VBaYRPp85Sw.jpg`
  - **Dimensions / Size:** `1280×720` JPG, `233,366` bytes (`< 2 MB`)
  - **SHA256:** `c1c80951ab2c84826c7d103284aa006384a79f372223d8b03386ad2b4848477b`
  - **Base Plate:** `venus_surface_465c_lander_plate.jpg` (`SHA256: 3374c505401ac19f3bbe902a2d5298fc0069ca911d46a4acdd90218c96892bbc`)
  - **Builder Script:** `build_venus_tc_b_465c_j2484.py` (**£0** cost; deterministic grade + code-drawn typography)
  - **Preview Sheets:** `venus_tc_B_465c_preview_sheet.jpg` and `venus_tc_A_vs_B_465c_sheet.jpg` (side-by-side at `168×94` and `360×202` against `A: MELTS LEAD` and ended `B: EARTH'S TWIN`)

## Gate Output (`thumb_preview.py long --score`)

```text
02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_tc_B_465c_preview_sheet.jpg
PASS  venus_tc_B_465c_VBaYRPp85Sw.jpg  saturation=183.3  near_black=24%
02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_tc_A_vs_B_465c_sheet.jpg
PASS  venus_thumb_A_melts-lead.png  saturation=161.8  near_black=27%
PASS  venus_tc_B_earths-twin_VBaYRPp85Sw.jpg  saturation=154.1  near_black=19%
PASS  venus_tc_B_465c_VBaYRPp85Sw.jpg  saturation=183.3  near_black=24%
```

## Rubric (`THUMBNAIL_AND_TITLE_RULES.md` §2.B)

| Check | Result | Notes |
|---|---|---|
| **HOOK** | **PASS** | `'465°C'` (1 token, `<= 3` words); complements *What Happened to Venus?* without repeating any title word; names the physical furnace temperature baking the lander. |
| **BAND** | **PASS** | Top-left sky band (`bbox = [68, 34, 462, 138]`), `86 px` cap height (`11.94%` of `720p`), `Arial Black.ttf` in house yellow `(255, 230, 0)` with `9 px` black outline and drop shadow; completely off the lander hero on the right and clear of the bottom-right duration corner. |
| **GRADE** | **PASS** | Mean HSV saturation `183.3` (within `165–195` / `170–200` target), pixels pinned at `S >= 250` down to `1.97%` (from `59.4%`), near-black `24%` (`<= 30%` ceiling); warm amber-orange atmospheric sky cast over solid metallic Venera lander and dry fractured basalt slabs. |
| **PHONE** | **PASS** | Checked at `168×94` and `360×202` on `venus_tc_A_vs_B_465c_sheet.jpg`; `'465°C'` and the metallic Venera-style lander silhouette on Venus's surface read in under a second with no glowing red fireball; no Orbit (§2.8). |

## Status
Parked for fresh independent design review before `J1198` is reopened. Nothing changed in YouTube Studio. **£0.**
