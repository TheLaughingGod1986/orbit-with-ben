# Thumbnail and title rules

Set 25 Sep 2026 from [the thumbnail and title audit](audits/THUMBNAIL_TITLE_AUDIT_2026-09-25/AUDIT.md). These rules sit on top of the house thumb gate in `ORBIT_HOUSE_AND_UAT_BIBLE.md`: yellow on the hook word, white on the rest, centre-safe, no clipped lines, distinct plate, no Orbit. Where the two differ, this file is newer.

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
   | A specific contradiction | *Why JWST Pictures Don't Match the Textbook* (3.6% CTR) |

   [views]
2. **Put a familiar noun in the first four words:** the Moon, the Sun, a star, the sky, Earth, you, your body. [views]
3. **No hedges.** No "may", "might", "could", "what if". *We May Have Already Recorded Alien Life* got 10 views. *We Could Smell Alien Life in a Spectrum* got 32 views and 1.1% CTR. [views, CTR]
4. **No description of what an instrument or place can do.** *What JWST's Infrared Eyes Can See* got 39 views and 1.0% CTR. Say what it found instead. [views, CTR]
5. **No poetic images or vague stakes.** *The Sky Would Lean…* (19). *A Reply From the Stars Takes Generations* (17). *One Second… Is Enough* (20). If the title could be a caption under a still, rewrite it. [views]
6. **No hashtags, no series suffix, and never the title of an existing public video.** [views]
7. **Length is not the lever.** Top-10 median is 37.5 characters, bottom half 39.5. Keep it under about 60 characters so it isn't cut off on a phone, and spend the effort on the shape. [views]
8. **Longs use the phrase people search, as a question.** Start with "What Happens When…", "What Would You See If…" or "Why…". The topic keyword goes in the first five words. *Everything you need to know about…* is out. [views]
9. **Wonder, not threat.** No "destroy", "coming for us" or "we're doomed". This is the channel's lane rule.

## 2. Long thumbnails (16:9)

1. **One subject, big.** One object fills at least a third of the frame, on a dark, simple background. No asteroid fields, no galaxy mush. Fails: Andromeda (galaxy swirl), Last Star (asteroid field).
2. **2–4 words, one or two lines.** Every word is readable at **168×94**, the size of a phone search result. Run `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long <thumb.jpg> --out <sheet.jpg>` and look at the small tile. Fails: YOUR BODY NEAR A NEUTRON STAR (6 words), WHEN THE LAST STAR DIES (thin).
3. **The thumb adds to the title. It never repeats it.** Title: *What Happens When the Last Star Dies?* Thumb: **LAST LIGHT** or **THEN DARK**, not WHEN THE LAST STAR DIES.
4. **Short questions and tension words read best.** LEAVING US?, TOO EARLY? and A GIANT EYE? all read at phone size.
5. **One heavy sans font for every thumbnail on the channel,** in capitals. Yellow on the one hook word, white on the rest. Heavy black outline or drop shadow. The same font every week is how a returning viewer spots an Orbit video.
6. **Keep text off the subject and out of the bottom-right corner,** where YouTube puts the duration.
7. **Same promise as the title and the film.** No threat framing. The Andromeda thumb COMING FOR US? fails this.
8. **No Orbit on thumbs, for now** (house rule). The two Orbit thumbs are the two weakest longs, but they are also the two longest films, so this is not proven either way. Test it with Studio *Test & Compare* once a long passes about 1,000 impressions.
9. **Judge CTR only after about 500 impressions.** Below that, one click changes the rate by several points. Use Test & Compare with 3 variants on every long, and leave it running until YouTube picks a winner.

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
- [ ] `thumb_preview.py` sheet checked: every word is readable at the smallest tile, and nothing is clipped in the centre crop.
- [ ] One subject, dark background, house font, yellow on the hook word.
- [ ] Shorts: frame 0 passes `gate_shorts_open.py`, and the frame-0 caption is the promise, at the bigger size.
- [ ] Longs: Test & Compare set up with 3 variants.
- [ ] After 7 days: log impressions and CTR next to the thumb in the week's test log. Judge only past about 500 impressions.
