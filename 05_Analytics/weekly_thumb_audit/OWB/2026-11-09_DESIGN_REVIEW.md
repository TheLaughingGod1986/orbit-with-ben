# J2374 packaging review brief — three draft Bs (9 November 2026)

Worker drafts only (`macbook-2`). No Chief approval yet, no live YouTube Studio changes, no tests armed. Review each B against its live A and unchanged live title. Title Bs are alternatives for a **separate later title-only test** with thumbnail fixed; never change both variables in the same test.

## Shared constraints & Selection basis

- **House rules (`00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md` §§2, 2.A, 2.B):** Wonder, not threat; 2–3 words in the top band, clear of the hero body; one yellow hook word (`#FFE600`), white remainder (`#FFFFFF`), heavy black stroke; no Orbit; scale reference (`Earth`) present and clear of the bottom-right duration badge; `1280×720` JPEG under 2 MB; mean HSV saturation `>= 100` (aim `120+`), near-black `<= 30%`.
- **Target selection:** In the 28-day Studio Reach window (`2026-10-12` to `2026-11-08`), only 2 longs had `>= 1,000` impressions (`h8HGfyShEHI` Sun at `2.34%` CTR — already tested to a 50/50 draw in `T012`, and `d2b633fdR0w` Venus at `4.37%` CTR). Of the 14 public longs without a running Studio Test & Compare (`T016`, `T017`, `T018`, `T019`, `T021`, `T008`, `T022` are currently running), the 3 highest-priority weakest thumbs by style & CTR are:
  1. `2fsQcea-voM` (`013_Why-The-Moon-Is-Slowly-Leaving-Us`, 111 imp, `2.70%` CTR): **FAIL** `saturation 25 < 100`, **FAIL** `near_black 79% > 30%`; two small distant circles with a faint dashed line between them.
  2. `Yk1tLh23rko` (`007_What-Happens-To-Your-Body-Near-A-Neutron-Star`, 69 imp, `0.00%` CTR): **FAIL** `near_black 42% > 30%`; live thumb has `CRUSHED FLAT` sitting directly on the upper rim of the neutron star and no scale reference.
  3. `b8-X_FyJnHM` (`003_Exoplanets-Strangest-Alien-Worlds`, 159 imp, `3.14%` CTR): **FAIL** `saturation 33 < 100`; live thumb uses a conceptual grey "eyeball planet" (`A GIANT EYE?`) with text overlapping the upper-left limb and no scale reference.

## Critique these points explicitly

1. **`2fsQcea-voM` (`NO MORE ECLIPSES`):** Does the warm golden-amber sunlit Moon (`NASA GSFC_20171208_Archive_e000868`) paired with foreground Blue Marble Earth (`as17-148-22727`) read immediately at `168×94` as our Moon receding from Earth, and does `NO MORE ECLIPSES` deliver a stronger concrete physical payoff than the live `LEAVING US?` (`sat=25`, `near_black=79%`) without repeating the title words?
2. **`Yk1tLh23rko` (`20 KM WIDE`):** Does the clean un-inpainted neutron star plate (`t=465.00s` from `neutron_star_STUDIO_OWNER.mp4`) paired with the lower-left Earth scale reference and `20 KM WIDE` in the top band make the impossible city-sized scale of a neutron star clear at phone size, while keeping the text 100% off the star's crust and flares?
3. **`b8-X_FyJnHM` (`RAINS MOLTEN GLASS`):** Does replacing the grey conceptual eyeball planet (`A GIANT EYE?`, `sat=33`) with NASA Hubble's cobalt-blue `HD 189733 b` (`GSFC_20171208_Archive_e001427`), diagonal silicate glass-rain streaks, and foreground Earth scale reference (`RAINS MOLTEN GLASS`) give a sharper, truer, high-saturation hook that matches the film's opening exoplanet showcase?
4. **Separate Title-Only B proposals:** Score each proposed question title for exact search phrasing, factual accuracy, and non-overlap with the thumbnail hook before any future title-only test.

## Draft files and pairs

### 1. `2fsQcea-voM` (`013_Why-The-Moon-Is-Slowly-Leaving-Us`)
- **Live title:** `Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone`
- **Live A:** `/Users/ben/_desk/j2374/live/2fsQcea-voM.jpg` (`LEAVING US?`, `sat=25.0`, `near_black=79%` — FAIL)
- **Draft B:** `/Users/ben/_desk/j2374/designs/2fsQcea-voM_B_v01.jpg` (`sat=124.4`, `near_black=5%` — PASS)
- **Hook:** **NO MORE ECLIPSES** (yellow `ECLIPSES`, white `NO MORE`)
- **Separate title-only B proposal:** **Why Does the Moon Drift 3.8 cm Farther Every Year?**
- **Bytes:** `305,324`; **SHA-256:** `f309e064f7b006e1bfda5d1e2af884f66c691238399477f12fed7965aafbf500`
- **Sources:** `NASA GSFC_20171208_Archive_e000868` (Full Moon, public domain) + `NASA Apollo 17 as17-148-22727` (Blue Marble Earth, public domain)

### 2. `Yk1tLh23rko` (`007_What-Happens-To-Your-Body-Near-A-Neutron-Star`)
- **Live title:** `What Happens If You Get Near a Neutron Star or Pulsar?`
- **Live A:** `/Users/ben/_desk/j2374/live/Yk1tLh23rko.jpg` (`CRUSHED FLAT`, `sat=102.6`, `near_black=42%` — FAIL)
- **Draft B:** `/Users/ben/_desk/j2374/designs/Yk1tLh23rko_B_v01.jpg` (`sat=132.5`, `near_black=3%` — PASS)
- **Hook:** **20 KM WIDE** (yellow `20`, white `KM WIDE`)
- **Separate title-only B proposal:** **What Happens to Your Body Near a Neutron Star?**
- **Bytes:** `244,360`; **SHA-256:** `5a01d73816e46096d8076dbb839f1cd02d723b7b357efb8af5237ae9f3271366`
- **Sources:** `007` master frame at `t=465.00s` (`neutron_star_STUDIO_OWNER.mp4`, clean un-inpainted hero plate) + `NASA Apollo 17 as17-148-22727` (Blue Marble Earth scale reference, public domain)

### 3. `b8-X_FyJnHM` (`003_Exoplanets-Strangest-Alien-Worlds`)
- **Live title:** `Alien Worlds: The Strangest Planets We've Ever Found`
- **Live A:** `/Users/ben/_desk/j2374/live/b8-X_FyJnHM.jpg` (`A GIANT EYE?`, `sat=33.0`, `near_black=16%` — FAIL)
- **Draft B:** `/Users/ben/_desk/j2374/designs/b8-X_FyJnHM_B_v01.jpg` (`sat=213.8`, `near_black=4%` — PASS)
- **Hook:** **RAINS MOLTEN GLASS** (yellow `GLASS`, white `RAINS MOLTEN`)
- **Separate title-only B proposal:** **What Are the Strangest Planets We've Ever Found?**
- **Bytes:** `287,718`; **SHA-256:** `74917c9d3104caa54976c7e8177bcfa4c1ef9cb19021e07ee82cb23cb299c339`
- **Sources:** `NASA Hubble GSFC_20171208_Archive_e001427` (`HD 189733 b` True Blue Planet, public domain) + `NASA Apollo 17 as17-148-22727` (Blue Marble Earth scale reference, public domain)

## Evidence and Gate Output

- **Phone sheet (`168×94` and `352×198` live A vs proposed B):** `/Users/ben/_desk/j2374/designs/PHONE_SHEET_v01.jpg` (`sha256: af22ec076b1c434c381a82ee5e3cf9f6d2140c764d521053a090e307a54ff085`)
- **Official `thumb_preview.py` sheet:** `/Users/ben/_desk/j2374/designs/THUMB_PREVIEW_SCORE_SHEET.jpg` (`sha256: 531aac97d12c3aa85cd1425dc10f16ba3c99ac43e7449c9fe6cc00159cca432f`)
- **Reproducible builder:** `00_Brand/Channel-Setup/tools/build_weekly_thumbs_j2374.py`
- **JSON manifest:** `05_Analytics/weekly_thumb_audit/OWB/2026-11-09_evidence/DESIGN_MANIFEST.json`

```text
/Users/ben/_desk/j2374/designs/THUMB_PREVIEW_SCORE_SHEET.jpg
PASS  2fsQcea-voM_B_v01.jpg  saturation=124.4  near_black=5%
PASS  Yk1tLh23rko_B_v01.jpg  saturation=132.5  near_black=3%
PASS  b8-X_FyJnHM_B_v01.jpg  saturation=213.8  near_black=4%
```
