# Thumbnail and title rules

Set 25 Sep 2026 from [the thumbnail and title audit](audits/THUMBNAIL_TITLE_AUDIT_2026-09-25/AUDIT.md). These rules sit on top of the house thumb gate (now in `STUDIO_PLAYBOOK.md` §8): yellow on the hook word, white on the rest, centre-safe, no clipped lines, distinct plate, no Orbit. Where the two differ, this file is newer.

Evidence strength: **[views]** means a pattern across 48 Shorts. **[CTR]** means thumbnail click-through on 80–480 impressions, which points the same way but is noisy.

## 1. Titles (Shorts and longs)

1. **Use one of the six shapes that win.**

   | Shape | Example that won |
   |---|---|
   | An ending / countdown | *What Remains After the Last Star Dies?* (622) |
   | A body impossibility | *Why You Can't Stand on a Neutron Star* (419) |
   | A yes/no about a familiar thing | *Is the Moon Leaving Us?* (290) |
   | Something hidden | *Why Europa Is Hiding a Massive Ocean* (291) |
   | One real number | *Why Does the Moon Drift 3.8 cm a Year?* (253) |
   | A specific contradiction | *Why Stars Don't Crash When Galaxies Meet* (249 in 8 days, 3.6% likes, the channel's best like rate); *Why JWST Pictures Don't Match the Textbook* (3.6% CTR) |

   [views]
2. **Put a familiar noun in the first four words:** the Moon, the Sun, a star, the sky, Earth, you, your body. [views]
3. **No hedged claims.** "We may have…", "We could…", "It might…", "What if…". *We May Have Already Recorded Alien Life* got 10 views. *We Could Smell Alien Life in a Spectrum* got 32 views and 1.1% CTR. A yes/no question that starts with "Could" (*Could a Robot Survive…?*, *Could Life Exist Under the Ice of Europa?*) is the yes/no shape, not a hedge. [views, CTR]
4. **No description of what an instrument or place can do.** *What JWST's Infrared Eyes Can See* got 39 views and 1.0% CTR. Say what it found instead. [views, CTR]
5. **No poetic images or vague stakes.** *The Sky Would Lean…* (19). *A Reply From the Stars Takes Generations* (17). *One Second… Is Enough* (20). If the title could be a caption under a still, rewrite it. [views]
6. **No hashtags, no series suffix, and never the title of an existing public video.** [views]
7. **Length is not the lever.** Top-10 median is 37.5 characters, bottom half 39.5. Keep it under about 60 characters so it isn't cut off on a phone, and spend the effort on the shape. [views]
8. **Longs use the phrase people search, as a question.** Start with "What Happens When…", "What Would You See If…" or "Why…". The topic keyword goes in the first five words. *Everything you need to know about…* is out. [views]
9. **Wonder, not threat.** No "destroy", "coming for us" or "we're doomed". This is the channel's lane rule Andromeda week, 6 Oct read: *Is Andromeda Coming to Destroy Us?* got 89 views; *Why Stars Don't Crash When Galaxies Meet*, the same topic answered with a surprising "no", got 249. [views, likes]
10. **News framing is allowed when there is a real new result** (Packaging, 11 Oct 2026): "We Found…", "We Just Saw…", or the mission name ("JWST Found…"). Astrum's top longs open this way. It needs a dated result in `SOURCES.md` from the last year or so; on an old or settled fact it is clickbait, so use the six shapes. Rules 3 and 9 still apply: no "We may have…", no threat.

## 2. Long thumbnails (16:9)

1. **One subject, big.** One object fills at least a third of the frame, on a dark, simple background. No asteroid fields, no galaxy mush. Fails: Andromeda (galaxy swirl), Last Star (asteroid field).
2. **2–4 words, one or two lines.** Every word is readable at **168×94**, the size of a phone search result. Run `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long <thumb.jpg> --out <sheet.jpg>` and look at the small tile. Fails: YOUR BODY NEAR A NEUTRON STAR (6 words), WHEN THE LAST STAR DIES (thin).
3. **The thumb adds to the title. It never repeats it.** Title: *What Happens When the Last Star Dies?* Thumb: **LAST LIGHT** or **THEN DARK**, not WHEN THE LAST STAR DIES.
4. **Name the thing or make a dare; don't ask a vague question** (Packaging, 11 Oct 2026, §2.B.1). A question is fine only when it names the subject: SIGNAL ON MARS?, not WHAT ARE THEY? or HOW LONG?.
5. **One heavy sans font for every thumbnail on the channel,** in capitals. Yellow on the one hook word, white on the rest. Heavy black outline or drop shadow. The same font every week is how a returning viewer spots an Orbit video.
6. **Keep text off the subject and out of the bottom-right corner,** where YouTube puts the duration. Since 11 Oct 2026 the text sits in a band across the top (or a clear edge), never over the subject (§2.B.2).
7. **Same promise as the title and the film.** No threat framing. The Andromeda thumb COMING FOR US? fails this.
8. **No Orbit on thumbs, for now** (house rule). The two Orbit thumbs are the two weakest longs, but they are also the two longest films, so this is not proven either way. Test it with Studio *Test & Compare* once a long passes about 1,000 impressions.
9. **Judge CTR only after about 500 impressions.** Below that, one click changes the rate by several points. Use Test & Compare with 3 variants on every long, and leave it running until YouTube picks a winner.

### 2.A Cover art rules from the 4 Oct 2026 audit

Added 4 Oct 2026 from [THUMB_AUDIT_2026-10-04](audits/THUMB_AUDIT_2026-10-04/AUDIT.md) (Claude-approved). These sharpen §2; they do not replace it.

1. **Near-black ≤30% of pixels.** Winners ran 3–27% near-black. No flat #000 text slabs or empty black panels. Prefer a graded starfield or nebula behind the subject.
2. **Colour-grade every NASA plate** before it goes on a thumb: saturation, contrast, rim glow. "Approved material only" still needs finishing — raw plates read flat at phone size.
3. **Text line height about 11–12% of frame height per line** (longs ~82 px on 720). Keep text **off the subject**. One yellow hook word; white on the rest. Oversized 15–20% lines crowd out the planet and break the subject-first read.
4. **Whole subject large:** visible and at least **⅓ of the frame** (same intent as §2.1). Do not crop the hero to a strip.
5. **A main character or a scale reference on every thumbnail** (audit 9 Oct 2026): a rover, a probe, a person, Earth beside the subject. It gives story and size. 025 and 026 do; 024 v02 didn't, and B and C read as nothing at phone size.
6. **Short cover text must fit inside the 16:9 centre band** of the 9:16 cover (the crop YouTube uses on TV / Related). Check with `thumb_preview.py short`. Set Short covers in Studio UI when the API returns blank tiles.
7. **The cover must survive both crops.** A cover designed 16:9 is cut to 9:16 in the Shorts feed: nine live Shorts lost their words that way (audit 9 Oct: "RS DO / MASS", "BILLIONS YEARS"). Keep every word inside the area common to both crops, the centre about 56% of the width.
8. **Back-to-back weeks don't share a look** (audit 9 Oct). If last week's primary was a big orange sphere on the right with two words on the left (022 Sun), this week's isn't (023 Venus). Change the layout, the colour family or the subject's size.

### 2.B Packaging rules from the Astrum study (11 Oct 2026)

Added 11 Oct 2026 by Chief (Ben delegated creative calls to Chief and the AIs). Evidence: Astrum's top and bottom longs and Shorts against our last ten longs, 11 Oct (`/workspace/astrum-pack`, longs_meta.tsv, shorts_meta.tsv, contact sheets). Their best thumbs name the object or dare the viewer; their weakest ask a vague question. These sharpen §2 and §2.A; where they differ, §2.B wins.

1. **The hook text names the object or makes a dare.** THIS IS TRITON, DON'T GO HERE, A HIDDEN OCEAN. **No vague questions or teasers:** WHAT ARE THEY?, HOW LONG?, WHEN THEY MEET. A question is allowed only if it names the subject: SIGNAL ON MARS?, BETELGEUSE NEXT?.
2. **2–3 words in a band across the top** (or along a clear edge where the frame is empty), **never over the subject.** The subject stays whole and uncovered below or beside the band. Keep the house font, the heavy outline, and **the yellow hook word**, white on the rest. Not in the bottom-right (duration). Five of our last ten broke this on 11 Oct: Andromeda, Neutron Star, Europa, Last Star, Black Hole (text centred on the subject).
3. **Grade harder.** Mean HSV saturation **120 or more** (0–255). Ours averaged about 94 on 11 Oct; Astrum's top longs about 139. Below **100** is a FAIL (85 for a naturally pale subject: the Moon, Europa's ice, Saturn, with `--pale` and a line in the review note). Push saturation, contrast and rim glow on the subject and the sky behind it, never by adding flat colour slabs. The **near-black cap stays: 30% or less** (§2.A.1). Check both with `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long <thumb.jpg> --out <sheet.jpg> --score`. Colour is necessary, not enough: Astrum's own weakest longs are also saturated (about 127), so the hook and layout still decide most of it.
4. **Optional: one small white arrow** pointing at the thing, for a "look at this" discovery story (a feature on a surface, a new object in a field). Thin, white, with the house outline, never over the subject's centre, at most one per thumb. Not on every thumb.
5. **Titles may use news framing** when there's a real new result (§1 rule 10).

**Review check (Chief and Orbit Auditor score it on every new or rebuilt long thumb, PASS or FAIL in the pack's review note):**
- **HOOK:** names the subject or dares; any question names the subject.
- **BAND:** 2–3 words in a top band or clear edge; no letter over the subject; yellow hook word present.
- **GRADE:** `thumb_preview.py --score` PASSes (saturation 100+, or 85+ with `--pale`; near-black 30% or less).
- **PHONE:** every word readable at 168×94 on the same sheet.

Any FAIL goes back to the builder before the thumb is set. Existing live thumbs are not reworked, except the five listed in rule 2 (one Studio job, 11 Oct 2026).

## 3. Shorts: the first frame is the thumbnail

In the Shorts feed (78% of Shorts views) nobody sees your custom thumbnail. They see frame 0.

1. **Frame 0 is a moving world or object. Never Orbit, never a dark card.**

   | Frame 0 | Median views |
   |---|---:|
   | World or object | **86.5** (32 Shorts) |
   | Orbit | **23.5** (8 Shorts) |
   | Dark or text card | **16.5** (4 Shorts) |

   The six opening rules in `FAMILIAR_DANGER_STRATEGY.md` apply. [views]
2. **The frame-0 caption is the promise in 2–4 words:** "what remains", "what if you stood on it?". Not a label or a fragment ("closer ≠ certain", "sideways", "cold should win"). [views]
3. **Make the frame-0 caption about twice today's size.** Cap height about 8–10% of frame height (today it is about 5%). Yellow on the hook word, heavy outline. Keep it in the vertical centre, clear of the bottom UI.
4. **A different plate from the last 14 days.** `gate_shorts_open.py` already fails a repeat. Europa ran the same globe 7 times.

## 4. Shorts: custom thumbnail (search, channel page, Related)

Search was 17% of Shorts views, and one Short got 477 thumbnail impressions, so this still matters.

1. **Use the title's hook words, not a new poetic line.** "stage is empty", "sun is middle class" and "should be a construction site" make the viewer decode something. Title *What Remains After the Last Star Dies?* → thumb **WHAT / REMAINS?** [CTR]
2. **2–4 words, big.** The stack spans at least 60% of the frame width and sits in the vertical centre, so it survives the 16:9 centre crop. Check it with `python3 00_Brand/Channel-Setup/tools/thumb_preview.py short <thumb.jpg> --out <sheet.jpg>`.
3. **Use a different picture from frame 0 when you can.** The feed already showed frame 0. The thumbnail is a second chance with the strongest still from the Short.
4. The house gate still applies: yellow and white, no Orbit, no clipped lines, distinct plate.

## 5. Checklist before upload

- [ ] The title is one of the six shapes, starts with a familiar noun, and has no hedge, hashtag or repeat.
- [ ] Thumb text is 2–4 words, adds to the title, and doesn't repeat it.
- [ ] Long thumb: hook names the subject or dares (no vague question); 2–3 words in a top band, off the subject; `thumb_preview.py --score` PASS (§2.B).
- [ ] `thumb_preview.py` sheet checked: every word is readable at the smallest tile, and nothing is clipped in the centre crop.
- [ ] One subject, dark background, house font, yellow on the hook word.
- [ ] Shorts: frame 0 passes `gate_shorts_open.py`, and the frame-0 caption is the promise, at the bigger size.
- [ ] Longs: Test & Compare set up with 3 variants.
- [ ] After 7 days: log impressions and CTR next to the thumb in the week's test log. Judge only past about 500 impressions.
