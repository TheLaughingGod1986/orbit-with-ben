# Thumbnail audit, Orbit With Ben and History of Science (9 Oct 2026)

Ben asked for a full thumbnail audit of both channels. This one is read-only: nothing was changed on YouTube and nothing was generated. It covers:
- every public long and Short (live thumbnails from i.ytimg.com, 9 Oct);
- the scheduled longs;
- every upcoming thumbnail set in the two repos.

Measured on the files: the share of near-black pixels (`nearblack.json`, luma under 20; the OWB rule is 30% or less).

Sheets in this folder:
- `longs_sheet.jpg`: live longs, with lifetime views.
- `upcoming_1.jpg` and `upcoming_2.jpg`: scheduled and upcoming.
- `shorts_owb.jpg` and `shorts_hos.jpg`: live Shorts as the Shorts feed shows them, sorted by views.
- `cropped_shorts.jpg`: the nine OWB Shorts whose cover text is cut off.
- `hos_004_C_v06_broken.jpg`.

## What the numbers can and can't say

The live longs have 2–42 lifetime views on OWB and 2–135 on HOS. Test & Compare only reads click-through after about 500 impressions (HOS rule 2.9), so **no thumbnail on either channel can be judged by its numbers yet.** This audit judges each one against the channel's own rules (`THUMBNAIL_AND_TITLE_RULES.md` in each repo) and looks for defects. Test & Compare does the measuring as impressions build.

## Fix before it airs

1. **HOS 004, "THE HIDDEN NUMBER" (variant C v06): broken.**
   - The Te/I tiles are a pasted rectangle with hard edges, and the right third is smeared, edge-stretched pixels (`hos_004_C_v06_broken.jpg`). That breaks HOS rules 2.1 (never a split panel) and 2.7 (every object fully in frame).
   - It is in 004's Test & Compare set (`LAUNCH_PLAN.md`), and 004 (`GHZDsiH7L7A`) airs **Thu 15 Oct 17:00Z**.
   - **Fix:** repaint C with the tiles in the scene, or take C out of Test & Compare before air. A and B are fine.
2. **OWB 024 Light Speed (airs Sun 1 Nov): no main character on any of the three.**
   - A (7 YEARS GONE?: Earth at night with a streak) reads.
   - B (YOU AGE SLOWER) is an Earth limb with no subject. C (ONE-WAY TRIP) is a blue blur nobody can name.
   - The film is the twin paradox, so the thumbnail should show a traveller.
   - **Fix:**
     - B: a NASA spacewalk astronaut (no named person) with Earth behind, YOU AGE SLOWER.
     - C: NASA's Voyager illustration (PIA17049, already in our pool) leaving a small Sun, ONE-WAY TRIP.
     - A: add a small craft at the head of the streak.
3. **OWB 023 Venus (airs 25 Oct), B "EARTH'S TWIN" shows no Earth.**
   - Put the Blue Marble Earth beside Venus (the reference rule).
   - The change also stops 023 looking identical to 022 the week before: both primaries are an orange ball on the right with two words on the left, on brown-black.
4. **OWB 025 Mars A:** the black mosaic wedge. Already step 0 of J0084.

## Live back catalogue (fix with Test & Compare, not by swapping blind)

5. **OWB Moon, "LEAVING US?" (`2fsQcea-voM`, 5 views): 75% near-black, the weakest live long.** Build a full-bleed Earth–Moon variant (the Moon Short "3.8 CM A YEAR" drew 347 views) and run it in Test & Compare against the current one.
6. **OWB Alien Worlds, "A GIANT EYE?" (`b8-X_FyJnHM`):** the planet with an eyeball is invented. It's a trust risk for a science channel. Add a real-planet variant (NASA/ESA HD 189733b, RAINS GLASS) in Test & Compare.
7. **OWB Andromeda, "WHEN THEY MEET" (`ojk-dfOpAmw`), 43% near-black:** borderline. No action until the two above have been run.
8. **HOS X-rays (`frP_YrNShsU`, 2 views):**
   - The Explorer fills the right half and the X-ray tube is tiny, against HOS rules 2.2 and 2.3. It is also 47% near-black.
   - **Fix:** repaint with the hero object at two-thirds on the right. Röntgen's 1895 X-ray of Anna Bertha's hand with the ring is the obvious hero, and real. Keep the Explorer small, lower left.
   - Run it in Test & Compare.
9. **HOS Periodic Table (`AL_-qlWko_g`, 135 views, the best on either channel): leave as is.** Its mercury hero doesn't say "periodic table", but it's the one that works, and most of its views come from Suggested. Its B/C variants (HE PREDICTED THIS, LEFT EMPTY ON PURPOSE) use OWB's sans lettering, not the HOS serif (rule 2.4). Repaint them in house lettering only if B or C wins.

## Shorts

10. **Nine OWB Shorts have cover words cut off in the 9:16 crop:**
    - `xQlV9G9lqLI` (RS DO / MASS)
    - `e-7hzJv4c80` (BILLIONS YEARS)
    - `CtllH6VOhEI` (GALAXIES COLLIDE)
    - `P9Jiw-MwUEU` (DOMIN / OR US)
    - `U5Baf_CjhKc` (FILLS THE SKY)
    - `17zpT_u7XsY` (EARTH SURVIVE)
    - `QRi6Dxq0hz0` (L SP)
    - `ZnsJTCcrTlA` (TO TO)
    - `tEOHYQbcgOw` (NIG…)

    **Fix:** re-set the custom cover only (thumbnails.set), with the words inside the centre 9:16-safe area. That is not a file swap: frame 0 and the video stay as they are.
11. **Eleven older OWB Shorts open on Orbit at frame 0** (now on the Never list). They are already live, and fixing frame 0 would mean re-uploading, which is also on the Never list. Leave them. New Shorts are gated (`gate_shorts_open`).
12. **HOS Shorts frame-0 captions run at about 3% cap height against the 8–10% rule (3.3).** Two open on blank cards (the "empty chairs" Short: 4 views; the faucet Short: 6). The top two (pond water 110, shadow 78) open on the thing itself, as rule 3.1 says. **Fix going forward:** `gate_shorts_open` should measure the caption height and fail anything under 8%, in both repos.

## Records

13. **HOS 005 has two private uploads.** `wwcjcFfC-5M` is the scheduled one (29 Oct). `0IfXGSX7Ypw` is a stray earlier upload with no publish time, but 005's `PACKAGE_MANIFEST.json` still points at the stray one. Point the manifest at `wwcjcFfC-5M`. Leave the stray private: videos are never deleted.

## Rules added (OWB `THUMBNAIL_AND_TITLE_RULES.md` §2)

- **Every thumbnail has a main character or a scale reference:** a rover, a probe, a person, Earth beside the subject. 025 and 026 do; 024 doesn't.
- **Back-to-back weeks don't share a look.** If last week's primary was a big orange sphere on the right with two words on the left, this week's isn't.

## How it compares with 4 Oct

The 4 Oct audit's fixes landed:
- Jupiter is now full-bleed with the probe.
- Saturn shows the whole planet, with Earth for scale.
- Thumbnails since 025 use real NASA rovers and telescopes with readable text.

The weak spots now are a missing main character (024) and sameness week to week (022/023).
