# Venus picture chapter: rejected source recipe, reusable dissolve renderer

J2452 remains incomplete. No UAT, final master, upload, spend or NAS write in this continuation.

The prior 108:22.36 clean audio candidate and all thirteen narration chapters are preserved unchanged.

## What this continuation built

`render_picture_chapter.py` renders explicit per-shot picture inputs on the MacBook, then joins separately encoded interiors and two-second endpoint dissolves without another video encode. Each dissolve uses one second of the outgoing shot plus a cloned endpoint and a cloned incoming endpoint plus its first second. The two-second result replaces the two original seconds, so it does not shorten the chapter or move narration. Cumulative frame quantization holds the Venus chapter at exactly 491.4 seconds. The helper refuses existing output directories and media overwrites.

`venus_picture_recipe_v01.json` maps v05e's actual 92 picture spans into the corrected audio slices, replacing chart/Orbit/mission-title rows for this diagnostic candidate. This is not an approved recipe. It has no inter-film breath, quiet chapter title or audio mux. The source masters are never rewritten.

## Source QA failed: do not adopt this recipe

The plan calls PIA00271 a Mariner 10 ultraviolet cloud image. The archived asset is a radar-derived **computer-simulated global view** from Magellan. NASA's official record confirms PIA00271, NASA/JPL, Magellan Radar System:

https://science.nasa.gov/photojournal/venus-computer-simulated-global-view-of-the-northern-hemisphere/

The retrieved pool also identifies PIA00104, PIA00252 and PIA00270 as computer-simulated globe views, and PIA00108 as a 3-D perspective. They do not become real cloud photographs because the plan or a filename describes them that way. The six extracted files and their actual archived titles, credits, member paths and SHA-256 values are in `venus_picture_assets_v01.json`; all media stays local.

The source-only `picture_qa.py` run rejected ten of the 92 mapped spans for reuse. Its full report is `venus_source_qa_v01/`. The gate's current kind regex does not catch the wording "Computer Simulated"; that lack of a machine flag does not override the source identity or constitute approval. No gate was changed or waived.

The original finished Venus film also contains radar perspective/globe imagery. The brief requires picture QA on joins; that does not authorize newly introducing a wrongly identified simulation as a photographic replacement. The newly rendered candidate is diagnostic only.

## Concrete next action

Before another Venus production render, replace rejected covers with correctly identified real imagery and reduce reuse below the existing gate limit. NASA's actual Mariner 10 cloud-image record is https://science.nasa.gov/photojournal/venus-from-mariner-10/ (PIA23791), already used elsewhere in v05e. This run verified the record but downloaded no new image; it is not yet a new approved cover or a solution to reuse. Use the film's existing pool and keep the source ledger honest; do not merely relabel PIA00271.

Run source-only QA before rendering the replacement recipe, then the saved-file picture/join checks. Retain the measured narration and continuous bed. Twelve other picture chapters, final AV checks, NAS master/reel copies with independent hashes and Ben's watch remain.

Additional diagnostic limitations: two sub-second source-row fragments at kept-range edges were merged into neighbouring render spans, so their baked source cuts still need individual softening. The diagnostic limiter applies to all YUV planes; the production renderer should cap luma only. These are not completed finishing items.
