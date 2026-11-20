# Pluto thumbnail drafts — J3105

19 November 2026. **REVIEW ONLY. No thumbnail, title or upload approval.**

Three 1280×720 JPEG candidates built with Pillow from the film's verified New Horizons harvest. No generation, spend or Studio changes. Builder: `build_j3105.py`; exact source/output hashes and durable paths: `MANIFEST_J3105_v01.json`.

| Draft | Picture and hook | Saturation | Near-black | Builder checks |
|---|---|---:|---:|---|
| A | Whole enhanced-colour Pluto, NITROGEN GLACIER | 166.0 | 3% | Main hook readable at 168×94; whole globe; scale number; single real-image concept |
| B | Mountain horizon, ICE MOUNTAINS | 133.1 | 1% | Main hook readable at 168×94; no imagined observer or moon; full panorama width |
| C | Bright cellular ice plain, FLOWING ICE | 107.7 | 1% | Main hook readable at 168×94; bright alternative, visibly different subject framing |

`thumb_preview.py long … --score` exits 0 for all three, without `--pale`. C is above the floor but below the saturation target of 120. Phone sheet inspected with the image tool; hook lettering is clear, text stays above the photographic subject, yellow is on the hook word, and the duration corner contains no text. Numeric scale labels are secondary: readable in the home-feed tile, small in the search tile. These checks are builder observations, not an independent packaging PASS. No moving-video or audio perception is claimed.

## Picture evidence and processing

- A: [PIA19952, The Rich Color Variations of Pluto](https://science.nasa.gov/photojournal/the-rich-color-variations-of-pluto/). Existing enhanced-colour MVIC globe; margins cropped without clipping the body, saturation increased, black point lifted to navy. No second photographic object, invented terrain, moon, person or probe. The 2,377 km number is **Pluto's diameter**, as sourced in the locked script/SOURCES, not the width of the glacier. Rule 19's single-image test is preserved; the numeric diameter provides rule 12's scale element rather than adding a second object.
- B: [PIA19948, mountains, plains and hazes](https://science.nasa.gov/resource/plutos-majestic-mountains-frozen-plains-and-foggy-hazes/). Source describes a 1,250 km-wide view, taken after closest approach. Entire horizontal image retained. The 250 km bar is one fifth of that image width, an approximate scene-width reference, not a local terrain measurement; projection foreshortens distances. Warm duotone applied to monochrome data: **not natural colour**.
- C: [PIA20726, convection cells](https://science.nasa.gov/photojournal/plutos-heart-like-a-cosmic-lava-lamp/). Source describes a roughly 400 km-wide scene, with surface renewal by convection. Full horizontal width retained; vertical crop 520:1730. The 100 km reference is one quarter of source width and approximate. Cyan/cream duotone and saturation are editorial grading, **not natural colour**. Bright concept replaces the draft's dark crescent idea.

Credit for all: NASA/Johns Hopkins University Applied Physics Laboratory/Southwest Research Institute. [NASA media guidance](https://www.nasa.gov/nasa-brand-center/images-and-media/) checked for editorial educational use; no people, logos or separate third-party copyright notice on these selected records. Acknowledgment must remain in the release package. Each source SHA-256 matches `HARVEST_POOL_v01.json`.

The old metadata's PIA19968 is **Charon in Enhanced Color**, not Pluto's blue crescent. Its imagined Charon-over-Sputnik scene was not used. Old metadata and README are not design authority; these candidates supersede those concepts for review only.

## Pairing and next action

Provisional current-rule title pairing: **Why Does Pluto Have a Heart? (A Glacier With No Craters)**. Main hooks also complement the existing draft **Why Pluto's Frozen Heart Has Zero Craters**; they add material, topography or mechanism rather than repeat zero craters. The new question is a candidate search phrase, not verified keyword demand or a locked title. **J3106** owns final search evidence, collision checks, title, chapters, description and package preparation, then queues independent Codex/Gemini/Cursor packaging critiques and the Chief decision.

Review should particularly judge C's strong false-colour grade, the globe's size/background space in A, and the secondary scale labels at search size. Do not equate automatic colour PASS with publish-ready design. No title or thumbnail test has been armed. Ledger entry waits for the authorized future test job.

Keep J2868 long UAT unchanged: watch by 8 December 18:00 London, planned 13 December slot. Preserve J3065/J3066 public-parent holds. Thumbnail stage remains review.

## Durable review pack

`/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/08_Thumbnail/J3105_v01/`

Contains the three JPEGs, 168×94/360×202 review sheet, source contact sheet, score output, manifest and builder. Media is outside Git. SHA-256 checks compare the local and NAS copies before this job closes. Rebuild with the builder's `--sources` pointing to the manifest's harvest directory and `--out` to a new scratch folder. Dependencies: Python, Pillow, NumPy, macOS Arial Black.
