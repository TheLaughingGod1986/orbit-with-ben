# Orbit With Ben: thumbnail audit (4 Oct 2026, 09:45 BST)

Read-only. Nothing was changed on YouTube and nothing was generated. Contact sheet: `CONTACT_SHEET.png`.
Sources: TubeAlfred (public longs and Shorts, views as of 4 Oct). For the scheduled videos, the thumbnail files were taken from the Mac mini repo using the upload records (`social/UPLOADS.json` and `PACKAGE_UPLOAD_RESULT_*.json`, which say "thumbnail set"). Those videos are private, so i.ytimg returns 404 for them.

## What is scheduled, and which thumbnail is set

| ID | Goes public | Title | Thumbnail set (from records) |
|---|---|---|---|
| `-jmMROGoZCM` | today 4 Oct 18:00 | Why You Can't Stand On Jupiter | `jupiter_thumb_cloud-no-floor.jpg`: NO FLOOR, all white |
| `55AEQwvs36g` | 11 Oct 18:00 | How Long Do Saturn's Rings Have Left? | `saturn_thumb_A_already-falling.jpg`: ALREADY **FALLING** |
| `Qn56D6TOi0k` (Short) | 12 Oct 11:30 | Saturn's Rings Are Already Falling | `cover_monday-saturn-falling.jpg`: HOW LONG? **FALLING**. Frame 0 says IT'S **FALLING** |
| `mZ82-ijANk4` (Short) | 16 Oct 11:30 | Why No Black Dwarf Exists Yet | `cover_friday-black-dwarf.jpg`: NOT **YET**. This is a Last Star Short, **not a Saturn Short** |
| Sun (022, 18 Oct) / Venus (023) | — | — | **No thumbnail exists yet.** `08_Thumbnail/` has only a README |

## The short answer: why the new ones look weaker

They read better at small sizes than the old ones. The text is bigger and cleaner. What they lost is the **art**. The top performers are full-bleed, glowing, colour-rich scenes with one lit subject in the middle of a starfield. The new ones are flat NASA-style plates on large areas of pure black, with oversized text sitting on or beside a subject that is cropped.

Measured on the actual files (`metrics.json`):

| | Near-black pixels | Text line height | Yellow hook |
|---|---:|---:|---|
| Top 4 longs (LAST LIGHT, TOO EARLY?, CRUSHED FLAT, A HIDDEN OCEAN) | **3–27%** (mean 13%) | **~10.5%** of frame | yes (3 of 4) |
| Jupiter NO FLOOR | **41%** (solid black slab across the bottom 40%) | **17%** | **none: all white** |
| Saturn ALREADY FALLING | **70%** | 15% | yes |
| Saturn Short cover (16:9 view) | 31% | 20% | yes |
| Black dwarf Short cover (16:9 view) | 54% | 19% | yes |
| Shorts frame-0 captions (Qn56 / mZ82) | — | **~3%** (rule: 8–10%) | yes |

## Top 3 problems

1. **No scene: dead black space and flat plates.** Jupiter is a cropped strip of texture on top of a black text panel. It looks like a title card, and at small sizes you can't tell it's Jupiter. Saturn sits on 70% pure black with no glow or colour grade. The older thumbs have a lit, glowing subject, nebula colour and depth. Likely cause: from 1 Oct the rule was "approved material only (NASA pool), no new generation" (Saturn README). Raw NASA plates went straight into the builder without being graded.
2. **The text is too big and lands on the subject.** Ben's 1 Oct note asked for "bigger text (~20% frame height/line)", which pushes the text to 15–20% line height against ~10.5% on the winners. The text then covers Saturn and the black dwarf, against the locked rule 2.6 "keep text off the subject". The text now dominates the image and the planet is secondary.
3. **Weak hook, no reference point, and one broken locked rule.** NO FLOOR, NOT YET and ALREADY FALLING are fragments with nothing they refer to. There is no question or tension object, and nothing for scale or story (no probe, person, Earth or Sun). The winners each imply an event (crushed, last light, hidden, too early) and show it happening. Jupiter also has **no yellow hook word**, which breaks the locked rule 2.5 in `THUMBNAIL_AND_TITLE_RULES.md`. The Saturn Short cover mixes two hooks (HOW LONG? + FALLING) that don't match its title, against rule 4.1. Both frame-0 captions are about a third of the required size (rule 3.3).

## Scores against Ben's house rules (22 Sep). 1–5 each, total /30

| Thumb | TV/small | Question/emotion | References | Low clutter | Main character obvious | Text variation/hook | **Total** |
|---|---|---|---|---|---|---|---|
| Jupiter NO FLOOR (set) | 4 | 2 | 1 | 3 | 2 | 1 | **13** |
| Saturn ALREADY FALLING (set) | 4 | 3 | 1 | 3 | 3 | 4 | **18** |
| Saturn Short HOW LONG? FALLING | 4 | 3 | 2 | 3 | 4 | 3 | **19** |
| Black dwarf Short NOT YET | 4 | 2 | 1 | 4 | 2 | 3 | **16** |
| *Benchmarks:* LAST LIGHT (41 views) | 3 | 4 | 2 | 3 | 5 | 4 | 21 |
| TOO EARLY? (29) | 4 | 4 | 4 | 3 | 3 | 3 | 21 |
| CRUSHED FLAT (15) | 3 | 4 | 2 | 4 | 5 | 4 | 22 |
| A HIDDEN OCEAN (15) | 3 | 4 | 3 | 4 | 5 | 4 | 23 |

Scheduled average **16.5** against **21.8** for the top performers. The scheduled ones win on TV/small-size reading and lose on emotion, references and the main character.

## Ranked fixes per scheduled thumbnail

**Jupiter `-jmMROGoZCM` (public 18:00 today, so this is the urgent one)**
1. Make **FLOOR** yellow. This is a locked rule, and it is a two-minute rebuild with the existing builder.
2. Remove the black slab. Go full-bleed: either variant C's cloud-deck plate across the whole frame, or the whole globe with the Great Red Spot so it reads as Jupiter. Put the text over the darker cloud and cut the line height to ~11–12%.
3. Add a reference that tells a story: a tiny probe (the Galileo probe from variant A) or a silhouette dropping into the clouds. Hook options: **NO FLOOR?** or **NOWHERE TO LAND**.
4. Once it's public, it becomes eligible for Test & Compare (REFRESH_LOG). Run NO FLOOR, the rebuilt version and THE FALL.

**Saturn long `55AEQwvs36g` (11 Oct, a week to fix)**
1. Show the whole planet. Don't crop it on the right, and keep the text in the black space on the left, off Saturn.
2. Grade the plate: warm rim glow and a faint starfield instead of 70% flat black. Variant C's ring-rain streaks show the event, so use them as the base.
3. Hook: **RAINING IN** or **GONE SOON?** both add to the title. ALREADY FALLING is fine but doesn't say what is falling.
4. Optional reference: Cassini, or Earth to scale against the rings.

**Saturn Short `Qn56D6TOi0k` (12 Oct)**
1. Cover text from the title's hook words, per rule 4.1: **ALREADY / FALLING**. Drop HOW LONG?, which belongs to the long.
2. Move the text off the ring streaks, and use a different still from frame 0 (rule 4.3). Today they are the same plate.
3. Make the frame-0 caption IT'S FALLING about 3× bigger, to 8–10% cap height (rule 3.3).

**Black dwarf Short `mZ82-ijANk4` (16 Oct)**
1. Give the hook a referent: **NO BLACK DWARFS / YET** or **DOESN'T EXIST YET**.
2. Make the subject read as a dying star: a glowing white dwarf fading to black, with the Sun beside it for scale. Keep the text off the disc.
3. Make the frame-0 caption about 3× bigger (rule 3.3), and use a different still for the cover.

**Sun (18 Oct) and Venus.** No thumbs exist yet, so build them to the rules below from the start.

## General rules to adopt (proposed additions to `THUMBNAIL_AND_TITLE_RULES.md` §2)

1. **Full-bleed scene, never a text slab.** Near-black pixels ≤30% (winners are 3–27%). Use a starfield or nebula, not flat #000.
2. **Grade NASA plates before use:** rim glow, saturation and contrast on the subject. "Approved material" still needs finishing.
3. **Text line height of about 10–12%.** That is enough for 168×94 and TV. 20% lines crowd out the subject.
4. **Whole subject visible, at least ⅓ of the frame, with text never on it.** This is already rule 2.1 and 2.6; add it to the gate check.
5. **One reference object** (probe, person, Earth, Sun) gives scale and a story. TOO EARLY? and A HIDDEN OCEAN both have one.
6. **The hook implies an event or question** (CRUSHED, LAST, HIDDEN, TOO EARLY?). Avoid bare fragments like NOT YET.
7. **Always one yellow hook word.** Add an automatic check to the builder (Jupiter shipped without one).
8. **Vary the layout week to week.** The last four use the same giant block text, which makes the shelf look repetitive. Give A/B/C different text as well as different art.

## Caveats and gaps
- The view counts are tiny (4–41 on longs). Every long thumbnail was swapped on 26 Sep, so most long views came in under the old art. The benchmark points to a direction; it isn't proof. Shorts views come mostly from frame 0 in the feed, not the cover.
- No CTR or impressions data was used, because Studio analytics weren't accessed.
- I did **not** call the YouTube Data API with the Content Ops OAuth token. That would mean using the refresh token in `07_Content-Ops/.env`, and the hosted ops app was retired on 27 Sep. The set thumbnails come from the repo upload records ("thumbnail set" via thumbnails.set) and haven't been checked live in Studio. If Studio was edited after upload, what's live could differ.
- The Saturn v02 iCloud folder (`OWB UAT/saturn_thumbs_v02/`) wasn't checked. The same A/B/C files were in the repo.
