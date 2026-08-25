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

## Where this plugs in

- **Pre-build:** generate 5–10 title candidates *from the structures above* → score in vidIQ →
  lock the highest ≥90 that passes the kill test (`PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`).
- **Shorts cluster:** every Short title uses S1–S6; covers follow scene-first rules.
- **Thumbs:** produce ABC per rule 4 above; longs start Studio/vidIQ ABC after upload.
- **Measurement:** thumbnail-impressions CTR is not yet queryable via the Analytics API for
  this channel (`videoThumbnailImpressions` metric exists but no supported query shape as of
  25 Aug 2026) — read CTR in Studio → Analytics → Content weekly and log winners in
  `RETENTION_LEARNINGS.md`.
