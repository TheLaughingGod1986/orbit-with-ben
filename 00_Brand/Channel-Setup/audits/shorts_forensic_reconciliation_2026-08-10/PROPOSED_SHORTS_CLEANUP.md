# Proposed Shorts Cleanup

Generated: `2026-08-10T11:55:29.774Z`

**NO DELETIONS PERFORMED. AWAITING EXPLICIT APPROVAL.**

## SAFE_TO_DELETE_HIGH_CONFIDENCE

_None._ Historical duplicates and Studio Draft rows mapping to existing private uploads are retained under KEEP_PRIVATE / forensic policy.

## KEEP_PRIVATE

19 assets — historical/superseded private Shorts with confirmed or likely canonical replacements. Deletion provides little benefit vs forensic / anti-reupload value.

## PROTECT_CANONICAL

All approved public + scheduled catalogue IDs (13-slot calendar with natural publishes).

## INVESTIGATE

11 low/medium confidence or orphan rows — see `STUDIO_PRIVATE_SHORTS_FORENSIC.json`.

## STUDIO_DRAFT_CANDIDATES

15 Studio Draft rows on Content → Shorts.

| Title | udvid / ID | Appears | Classification | Confidence |
|---|---|---|---|---|
| Falling In Wouldn't Feel Like Falling | `z-kgwJaz5pY` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| The Discovery That Doesn't Add Up | `Cw-tfP1QnBE` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| Is the Universe Older Than We Thought? | `trrKgW7m_98` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| Why JWST Pictures Don't Match the Textbook | `ItuOwgTvS1Y` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| How Did Black Holes Get So Big So Fast? | `slCssHVBOz0` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| These Galaxies Appeared Too Early | `4dGXJt9dElk` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| What JWST's Infrared Eyes Can See | `lUvMhe1BWJM` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| blackhole nf01 time appears to stop v01 | `B95wuAH68QY` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| What If Aliens Are Watching Us? | `IvSMHnngXdE` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| Space Is Rude About Distance | `6dSntxIQgXI` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| Where Is Everybody? The Fermi Paradox #Space #Shor | `dFO50RT5s14` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| We Found Planets Made of Diamond | `J_uLnRIwqu0` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| What If the First Alien Clue Is Already Here? | `zc79sRBCDnU` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| You'll Never Have a Real-Time Chat with Aliens #Sp | `z8-haBeF6mI` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |
| Cross This Line and You Never Come Back | `RF6wivuPYqI` | duplicate | `HISTORICAL_DUPLICATE` | HIGH |

### Interpretation

Most Draft rows are **not empty abandoned uploads**. Opening "Edit draft" reveals `udvid=` pointing at an **existing private historical upload**. Studio labels them Draft in the Shorts tab while the Data API reports them as normal `private` processed videos.

Videos-tab Draft filter remains empty — that was the previous audit blind spot.
