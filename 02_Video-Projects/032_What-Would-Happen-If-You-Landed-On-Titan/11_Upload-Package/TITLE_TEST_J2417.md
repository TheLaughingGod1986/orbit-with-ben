# 032 title + thumbnail-text test (J2417, MacBook, 8 Nov 2026)

Shape: Orbitra's two hits (*"When Our Solar System Lost a Planet (And It Might Still Be Out There)"* 38k; *"Our Sun Had a Twin (And It's Still Out There)"* 21k). A hidden thing, then why it still matters, in a bracketed tail. Every fact comes from the locked script `01_Script/titan_landing_script_master_v02.md`.

## Before

- Not uploaded yet (status: edit in review, upload todo). Air: Wed 25 Nov 18:00 London.
- Working title: **What Would Happen If You Landed on Titan?** (`metadata_DRAFT_v01.json` → `title_options[0]`)
- Thumbnails: none made yet (`08_Thumbnail/README.md`).

## Candidates

| # | Title | Chars | Script line it rests on |
|---|---|---|---|
| 1 | **Titan Hides an Ocean Under Its Ice (And Seas of Natural Gas on Top)** | 67 | "far beneath Titan's icy crust ... a second, hidden ocean — of liquid water" / "a drowned coastline ... filled with liquid natural gas" |
| 2 | **We Landed on Titan Once (And It's Still Our Most Distant Landing)** | 65 | "It is still the most distant landing humanity has ever made." |
| 3 | Titan Hid Its Surface for 350 Years (And Then We Landed There) | 62 | 1655 discovery to 2005 Huygens landing (350 is our own sum of two script dates, like the script's 28×) |

## Pick for Test & Compare (set at upload)

| Arm | Title | Thumbnail text (2-4 words, no title words) | One big object |
|---|---|---|---|
| A | Titan Hides an Ocean Under Its Ice (And Seas of Natural Gas on Top) | **WATER DEEP BELOW** | Titan as a cut-away sphere: orange haze shell, a thin blue water layer inside. One object, centred |
| B | We Landed on Titan Once (And It's Still Our Most Distant Landing) | **72 MINUTES** | The real Huygens surface frame (rounded ice pebbles, orange ground), graded hot, full bleed |

Why these two: A is the hidden thing (inner ocean + surface seas), B is the real landing (a real photo, which also fits LEARNINGS #19 "one clean real image thumbnail"). Different object, different picture type (diagram vs real frame).

Notes:
- Both stay under 70 characters. A is long (67); if Studio cuts it on a phone, the bracketed tail still reads.
- The "What Would Happen If…" series (LEARNINGS #20) is a playlist, not a title suffix, so it is unaffected.
- Candidate 3 dropped: the 350 is a derived sum and the shape is weaker.
- No fear framing (the "spark" fear is answered in the film, not used in the title), no hedge, no hashtag.

## After (thumbnails built 2026-11-09T01:24Z, J2430; ready for upload)

- **Built thumbnails (`08_Thumbnail/j2417_v01`, `abc_*` / `J2144_v01` untouched):**
  - **Arm A (upload primary + Slot 1):** `032_j2417_A_water_deep_below_v01.jpg` (`SHA-256: e8c86bd181fb7196ab62bf95ec19b9ce6f1096f27e06ac13fd2ff97d640eb534`, **WATER DEEP BELOW**, Titan cut-away sphere with orange haze shell and bright blue subsurface water layer centred, no Orbit) — `thumb_preview.py --score`: `PASS  032_j2417_A_water_deep_below_v01.jpg  saturation=143.5  near_black=4%`
  - **Arm B (Slot 2):** `032_j2417_B_72_minutes_v01.jpg` (`SHA-256: 68d8d57187bee9284c0b276f817cf90256bece8e62c829f5ea6d3ddb18b55390`, **72 MINUTES**, real Huygens surface frame `PIA07232` with rounded ice pebbles on orange ground graded hot, full bleed, no Orbit) — `thumb_preview.py --score`: `PASS  032_j2417_B_72_minutes_v01.jpg  saturation=208.3  near_black=2%`
  - **168×94 preview sheet:** `032_j2417_preview_sheet_v01.jpg` (`SHA-256: 67905e722808a94d307339566cf9398485a16800db03c292ca6d4bace656a902`)
- **Upload configuration (`metadata_DRAFT_v01.json`):** Updated `title_options` to lead with Arm A (`Titan Hides an Ocean Under Its Ice (And Seas of Natural Gas on Top)`) and Arm B (`We Landed on Titan Once (And It's Still Our Most Distant Landing)`), and added `j2417_test` pointing to `08_Thumbnail/j2417_v01/032_j2417_A_water_deep_below_v01.jpg` (Arm A upload primary) and `032_j2417_B_72_minutes_v01.jpg` (Arm B Test & Compare challenger).
