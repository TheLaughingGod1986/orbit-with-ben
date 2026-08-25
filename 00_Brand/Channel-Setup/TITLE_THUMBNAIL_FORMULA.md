# Orbit — title + thumbnail formula (locked 25 Aug 2026)

Derived from real channel data (25 public Shorts + 5 longs, `audits/channel_review_2026-08-24/`).
Rule file: `.cursor/rules/orbit-title-thumb-formula.mdc`. VidIQ scoring is still the gate
(`orbit-vidiq-source-of-truth.mdc`) — this formula generates the candidates that get scored.

## Evidence (24–25 Aug 2026)

| Views | Title | Why it worked / failed |
|---|---|---|
| 141 | Three Suns in the Sky — Real Alien Worlds | concrete strange image, stated as fact · **717% avg view (loops ~7x)** |
| 121 | Most of the Universe Gives Off No Light | concrete fact that sounds wrong |
| 89 | These Galaxies Appeared Too Early | declarative wrongness |
| 83 | Why JWST Pictures Don't Match the Textbook | named subject + contradiction |
| 68 | Why This Alien World Looks Like a Giant Eye | concrete image (won despite title hashtags) |
| 63 | We Found Planets Made of Diamond | discovery + impossible object |
| 57 | Is the Universe Older Than We Thought? | question, but the wrongness is *inside* it |
| 56 | What You Would See Falling Into a Black Hole | experiential "you" + named subject |
| … | | |
| 19 | How Did Black Holes Get So Big So Fast? | abstract question, no image |
| 17 | Space Is Rude About Distance | cute abstraction, no image |
| 16 | The Hottest Nights in the Universe | superlative without a picture |
| 5 | Falling In Wouldn't Feel Like Falling | subject missing (into *what*?) |
| 4 | Why This Line Is a Point of No Return | "this line" names nothing + hashtags |
| 3 | Would You Look Back? | zero context |

Three failure diseases in the bottom half: **abstract question** (no image), **missing subject**
("this line", "falling in"), **hashtags in the title** (4 of bottom 8; keep hashtags in tags).

## Shorts title structures (pick one)

Fill the slot with a *concrete strange image* and a *named subject*. Target ≤ ~50 chars / ≤ 8 words,
image words first. No hashtags. No series suffix. vidIQ `type=short` score ≥90.

| # | Structure | Example (real winner) |
|---|---|---|
| S1 | `[Strange image stated as plain fact]` | Most of the Universe Gives Off No Light |
| S2 | `We Found [impossible object]` | We Found Planets Made of Diamond |
| S3 | `Why [named subject] [contradicts expectation]` | Why JWST Pictures Don't Match the Textbook |
| S4 | `What You Would [see/feel] [extreme place]` | What You Would See Falling Into a Black Hole |
| S5 | `What If [unsettling concrete idea]` | What If They're Leaving Us Alone On Purpose |
| S6 | `Is [X] [wronger than we thought]?` — question ONLY if the wrongness is inside it | Is the Universe Older Than We Thought? |

**Kill test (all must pass):**
1. Can you *draw* the title? (concrete image)
2. Is the subject named — no orphan "this/it/the line"?
3. Zero hashtags, zero series suffix?
4. Does it state or contain the wrongness, not just promise a topic?

## Long-form titles

One promise, search-phrase-first (locks already in `orbit-longform-vo-picture-gate.mdc`):
`[Search phrase as a question or promise]` — e.g. "What Happens If You Fall Into a Black Hole?".
No series suffix on new longs. vidIQ `type=long` ≥90, prefer 95+.

## Thumbnails — scene-first (EARLY_POSITIVE_SIGNAL, Ben call 25 Aug 2026)

Observation: thumbnails **without** the Orbit character are outperforming. Sample is small —
treat as directional, keep A/B testing — but default flips to scene-first now:

1. **The strange object IS the thumbnail.** One focal object (three suns, cracked ice moon,
   red dwarf, lensed galaxy). No Orbit character by default.
2. **Text ≤ 4 words**, high contrast, readable at 168 px. The text states the wrongness
   ("NO LIGHT", "TOO EARLY?", "THREE SUNS").
3. Orbit may appear on **at most one** ABC variant, as a small corner accent (≤ ~12% frame
   width, never covering the subject) — and that variant must be tested against no-Orbit variants.
4. ABC set = three **scene-first** concepts: **A object** (hero shot) · **B emotion/scale**
   (same subject, angle or colour that makes it feel vast/wrong) · **C question** (subject +
   ≤4-word question text).
5. Wonder brand still applies: no fearbait comps, no red-arrow clickbait grammar.
6. Re-evaluate after the first A/B test resolves with a clear winner (Fermi + Black Hole tests
   ended "no clear winner" — too few impressions; Alien Worlds ends ~27 Aug).

### Picking the frame (Shorts covers) — 25 Aug 2026 lesson

Grabbing a frame at a fixed percentage of the clip does **not** produce a scene-first cover.
The first pass grabbed 42% of duration for all 44 Shorts and roughly half landed on an Orbit
face close-up (the exact thing scene-first exists to avoid), several on top of the clip's own
burned-in caption, giving doubled text.

Scan the whole clip and score every candidate frame instead:

1. Penalise **Orbit-orange pixel fraction**, weighted harder in the centre of frame.
2. Penalise **near-white pixels in the lower two-thirds** — that is the clip's own caption band.
3. Penalise a **busy top band** where the punch text goes, and near-black frames.
4. Reward overall detail, so the cover is not an empty starfield.
5. **Auto-fit the punch text** — 118 px Arial Black overflows 1080 px on strings like
   "NIGHTS HOTTER"; step the size down until the longest line clears both margins.

Builder: `00_Brand/Channel-Setup/tools/build_scene_first_short_covers.py`.
Some clips are Orbit-heavy end to end, so the best available frame still shows him — that is a
source-material limit, not a cover bug. Fix it upstream by shooting more non-Orbit scenery.

### Shorts covers cannot be set by the Data API (verified 25 Aug 2026)

`thumbnails.set` returns `ok` for a Short and genuinely writes a thumbnail — but it treats every
image as a **16:9 video thumbnail** and letterboxes a 1080x1920 file into 1280x720. It never
populates the **vertical cover slot** that the Shorts shelf, the channel Shorts tab and Studio
read, so a Short keeps showing a raw video frame no matter how many times the API says `ok`.

Verified by inspecting what the public shelf actually loads: every tile came from `oar2.jpg` or
`hq720_2.jpg`, all plain video frames, none of the uploaded covers. Studio's own widget requested
`sd2.jpg` / `mq2.jpg` and got 404, which is the grey placeholder seen in the Studio mobile app.

Google's own doc: *"Custom thumbnails for Shorts are currently only available to add in YouTube
Studio on a computer."*

So for Shorts:

1. Build the cover at **1080x1920, 9:16, under 2 MB** (correct spec — do not switch to 16:9).
2. Upload it through **Studio desktop** → video → Thumbnail → Options → Change.
   Driver: `00_Brand/Channel-Setup/tools/upload_shorts_covers_studio.py`.
3. **Studio enforces a daily custom-thumbnail cap** ("Daily customised thumbnail limit reached…
   up to 24 hours"). Bulk API writes burn the same quota, so do not spray `thumbnails.set` across
   the catalogue first — it both fails to take effect and locks out the path that works.
4. Long-form 16:9 thumbnails are unaffected; the API is still correct for those.

## Where this plugs in

- **Pre-build:** generate 5–10 title candidates *from the structures above* → score in vidIQ →
  lock the highest ≥90 that passes the kill test (`PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`).
- **Shorts cluster:** every Short title uses S1–S6; covers follow scene-first rules.
- **Thumbs:** produce ABC per rule 4 above; longs start Studio/vidIQ ABC after upload.
- **Measurement:** thumbnail-impressions CTR is not yet queryable via the Analytics API for
  this channel (`videoThumbnailImpressions` metric exists but no supported query shape as of
  25 Aug 2026) — read CTR in Studio → Analytics → Content weekly and log winners in
  `RETENTION_LEARNINGS.md`.
