# Thumbnails and titles audit (25 Sep 2026)

**Sources:**
- Public channel pages captured 25 Sep 2026: the 9 longs and the newest 48 public Shorts.
- For every Short: the first frame the feed shows (`i.ytimg.com/vi/<id>/frame0.jpg`) and the uploaded custom thumbnail (`hqdefault.jpg`).
- Long thumbnails at `hq720`, also rendered at phone search size (168×94).
- Stayed-to-watch, thumbnail impressions and CTR from the 10 Sep Studio pull (`channel_technical_audit_2026-09-10/data/`).

Rows are in `DATA.json`. Contact sheets are gitignored images; rebuild them from the URLs above.

The rules that come out of this audit are in [THUMBNAIL_AND_TITLE_RULES.md](../../THUMBNAIL_AND_TITLE_RULES.md).

## Verdict

1. **For Shorts, the first frame is the thumbnail.** 78% of Shorts views come from the feed, and the feed shows the video, not the custom thumbnail. Shorts whose first frame is a moving world had a median of **86.5 views** (32 Shorts). Shorts whose first frame is Orbit had **23.5** (8 Shorts). A dark title card had **16.5** (4 Shorts). No Short in the top 23 opens on Orbit.
2. **Custom Short thumbnails matter less, but not zero.** They show in search and on channel pages. Search was 17% of Shorts views, and single Shorts got up to 477 thumbnail impressions. Their text is small, and often a cryptic line that isn't the title's promise: "stage is empty", "sun is middle class", "should be a construction site", "countless stars no clear hello".
3. **Long thumbnails are clean but generic.** Readable at phone size:
   - LEAVING US?
   - COMING FOR US?
   - TOO EARLY?
   - A GIANT EYE?
   - FALLING IN?
   - WHERE IS EVERYBODY?

   Not readable:
   - YOUR BODY NEAR A NEUTRON STAR (6 words, small)
   - WHEN THE LAST STAR DIES (thin white, repeats the title)
   - Europa's sub-line MORE WATER THAN EARTH

   Several long thumbs have no single subject (Andromeda's galaxy mush; Last Star's asteroid field). Fonts vary between videos, so nothing says "Orbit" at a glance.
4. **Titles win on shape, not length.** The top 10 Shorts titles have a median of 37.5 characters, and the bottom half 39.5, so length isn't the lever. What wins is one of six shapes: an ending, a body impossibility, one number, a yes/no about a familiar thing, something hidden, or a specific contradiction (the sixth is from CTR only). What loses is hedged, descriptive or poetic wording.
5. **CTR samples are small.** Longs have 13–170 lifetime impressions, and CTR under about 500 impressions is noise. Rules from CTR alone are marked as weaker below. The views pattern across 48 Shorts is the stronger evidence.

## Shorts: first frame (what the feed shows)

| First frame | Shorts | Median views | Examples |
|---|---:|---:|---|
| A world or object, with a short caption | 32 | **86.5** | #1 *What Remains* (622): ringed planet + "what remains". #2 *Can't Stand* (419): cracked glowing crust + "what if you stood on it?" |
| The same Europa globe plate | 7 | 93 | Six of the seven are within 0–3 dHash bits (10 Sep audit). The feed saw one picture a week long. |
| Orbit | 8 | **23.5** | #24 Diamond (64), #28 (53), #32 (32), #35 (25), #36 (22), #40 (16), #44 (9), #48 Under Ice (2) |
| Dark frame or text card | 4 | **16.5** | #39 "space is rude" (17), #41 "everybody?" (16), #43 "is already here?" (10). #12 "almost dark" (127) is the exception. |
| Silent uploads replaced 24 Sep | 4 | 4.5 | Not a picture result. Excluded. |

Caveat: several of the Orbit-first Shorts are from the early Alien Worlds and JWST weeks, when the channel was smaller. The direction still matches the 10 Sep finding that Orbit-first opens get about 0% Shorts-feed traffic.

**The first-frame caption.** The winners say the promise in 2–4 words: "what remains", "what if you stood on it?", "almost dark". The weak ones are fragments or labels: "closer ≠ certain", "cold should win", "you stop being useful", "sideways". Captions are currently about 5% of frame height, lowercase and centred. They are readable, but small on a phone.

## Shorts: custom thumbnail (search and channel pages)

Best thumbnail CTR among Shorts with at least 80 impressions (10 Sep, lifetime):

| CTR | Impressions | Title |
|---:|---:|---|
| 4.8% | 83 | What Remains After the Last Star Dies? |
| 3.6% | 302 | Why JWST Pictures Don't Match the Textbook |
| 3.6% | 140 | Black Holes Grew Too Big, Too Fast |
| 3.4% | 89 | The Last Star Will Be a Red Dwarf |
| 3.3% | 395 | The Day the Last Star Goes Out |

Worst:

| CTR | Impressions | Title |
|---:|---:|---|
| 0% | 191 | Most of the Universe Gives Off No Light |
| 0.7% | 137 | This Planet's Night Never Cools Down |
| 1.0% | 193 | What JWST's Infrared Eyes Can See |
| 1.0% | 101 | We May Have Already Recorded Alien Life |
| 1.1% | 378 | We Could Smell Alien Life in a Spectrum |

The winners are an ending or a specific contradiction. The losers are a capability ("can see"), a hedge ("may", "could") or an abstraction. The channel average is 1.9%.

Thumbnail text problems across the 48:

- **Small type.** Most hooks fill less than a third of the frame width in the 4:3 crop.
- **The text isn't the promise.** Poetic lines that don't say what the Short is.
- **All-white or low-contrast type** on ice or blue, which the house bible already fails.
- **Repeat plates.** Europa globe ×7.

## Longs

| Thumb text | Readable at 168×94 | One subject | Matches title | CTR (impr.) |
|---|---|---|---|---|
| COMING FOR US? (Andromeda) | yes | no, a galaxy swirl | no, a threat on an "everything you need to know" title | new |
| LEAVING US? (Moon) | yes | yes, Earth and Moon with a ruler | yes | not yet reported |
| YOUR BODY NEAR A NEUTRON STAR | **no** (6 words) | yes | yes | 0% (13, pre-premiere) |
| LIFE UNDER THE ICE / MORE WATER THAN EARTH | first line only | yes | yes | 1.7% (59) |
| WHEN THE LAST STAR DIES | **no** (thin white) | no, asteroid field | repeats the title | 2.4% (170), best long |
| TOO EARLY? (JWST) | yes | partly, telescope and spectrum | yes | 1.5% (133) |
| A GIANT EYE? (Alien Worlds) | yes | yes | loosely | 2.8% (108) |
| FALLING IN? (Black Hole) | yes | yes, **Orbit** | yes | not reported, 4 views |
| WHERE IS EVERYBODY? (Fermi) | yes | yes, **Orbit** | yes | 0% (56) |

The best long (Last Star) has the least readable thumbnail. With 170 impressions, topic and title are doing more than the thumbnail. The two thumbnails with Orbit on them are the two weakest longs, but they are also the two longest films (18–21 min). The data can't separate those causes, so the house rule (no Orbit on thumbs) stands until a real test.

## Titles

| Shape | Examples (views) |
|---|---|
| **An ending / countdown** | What Remains After the Last Star Dies? (622) · The Sky Is Already Running Out of Light (292) · The Universe Is Running Out of New Stars (229) |
| **A body impossibility** | Why You Can't Stand on a Neutron Star (419) |
| **A yes/no about a familiar thing** | Is the Moon Leaving Us? (290) |
| **Something hidden** | Why Europa Is Hiding a Massive Ocean (291) |
| **One number** | Why Does the Moon Drift 3.8 cm a Year? (253) |
| **A specific contradiction** | Why JWST Pictures Don't Match the Textbook (3.6% CTR) · Black Holes Grew Too Big, Too Fast (3.6% CTR) |
| Losers: **hedged** | We May Have Already Recorded Alien Life (10) · We Could Smell Alien Life in a Spectrum (32) · What If They're Leaving Us Alone On Purpose (55) |
| Losers: **descriptive** | What JWST's Infrared Eyes Can See (39) |
| Losers: **poetic or vague** | The Sky Would Lean Near a Neutron Star (19) · A Reply From the Stars Takes Generations (17) · One Second Near a Neutron Star Is Enough (20) |
| Losers: **hashtags in title** | The early universe is hiding a massive secret #space #JWST #discovery (53) |

Topics matter too. Titles about the Moon, the last star, the Sun, the sky and your body win. Titles about alien signals and the Fermi paradox lose whatever the wording.
