# J2484 — 023 Venus (`VBaYRPp85Sw`) Thumbnail Test & Compare B: `'465°C'`

- **Video:** `023_What-Happened-To-Venus` (`VBaYRPp85Sw` — *What Happened to Venus?*, title unchanged)
- **Context:** `T011` (`A: MELTS LEAD` vs `B: EARTH'S TWIN`) ended 9 Nov 2026 01:10 UTC as a draw (*"Not enough impressions to declare a winner"*, `A: MELTS LEAD` visible to all). Per Chief ruling on `J1198` (29 Oct / 10 Nov 2026) and `05_Analytics/LEARNINGS.md` rules 11–13, the draw branch tests a genuinely different visual concept with a clear scale/stakes element (`LEARNINGS.md` rule 12) rather than another planet globe.
- **Deliverable:** `02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_tc_B_465c_VBaYRPp85Sw.jpg`
  - **Dimensions / Size:** `1280×720` JPG, `291,606` bytes (`< 2 MB`)
  - **SHA256:** `b580d47539dee75bcb19867377ddfd3384453bbf880ddf42c5675a8eabc31568`
  - **Base Plate:** `venus_surface_glowing_lander_plate.jpg` (`SHA256: 8f5f2b84fcbf27e7ec891343b64e23c1effc18542b5474d1be5ffb5e30de2aac`)
  - **Builder Script:** `build_venus_tc_b_465c_j2484.py` (£0 cost; deterministic grade + code-drawn typography)
  - **Preview Sheets:** `venus_tc_B_465c_preview_sheet.jpg` and `venus_tc_A_vs_B_465c_sheet.jpg` (side-by-side at `168×94` and `426×240` against `A: MELTS LEAD` and ended `B: EARTH'S TWIN`)

## Gate Output (`thumb_preview.py long --score`)

```text
/Users/ben/_desk/worker/slot2/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_tc_B_465c_preview_sheet.jpg
PASS  venus_tc_B_465c_VBaYRPp85Sw.jpg  saturation=245.5  near_black=15%
/Users/ben/_desk/worker/slot2/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_tc_A_vs_B_465c_sheet.jpg
PASS  venus_thumb_A_melts-lead.png  saturation=161.8  near_black=27%
PASS  venus_tc_B_earths-twin_VBaYRPp85Sw.jpg  saturation=154.1  near_black=19%
PASS  venus_tc_B_465c_VBaYRPp85Sw.jpg  saturation=245.5  near_black=15%
```

## Rubric (`THUMBNAIL_AND_TITLE_RULES.md` §2.B)

| Check | Result | Notes |
|---|---|---|
| **HOOK** | **PASS** | `'465°C'` (1 token, `<= 3` words); complements *What Happened to Venus?* without repeating any title word; names the physical furnace temperature baking the lander. |
| **BAND** | **PASS** | Top-left sky band (`bbox = [68, 34, 462, 138]`), `86 px` cap height (`11.94%` of `720p`), `Arial Black.ttf` in house yellow `(255, 230, 0)` with `9 px` black outline and drop shadow; completely off the glowing lander hero on the right and clear of the bottom-right duration corner. |
| **GRADE** | **PASS** | Mean HSV saturation `245.5` (`>= 120` target), near-black `15%` (`<= 30%` ceiling); rich incandescent red-orange thermal glow on the Venera-style lander hull, struts, and fractured basalt slabs. |
| **PHONE** | **PASS** | Checked at `168×94` and `426×240` on `venus_tc_A_vs_B_465c_sheet.jpg`; `'465°C'` and the glowing red spacecraft lander on Venus's surface read in under a second; no Orbit (§2.8). |

## Status
Parked for Chief / design review. Not armed in YouTube Studio in `J2484`; `J1198` waits on this file + passed design review to arm the Test & Compare in Studio.
