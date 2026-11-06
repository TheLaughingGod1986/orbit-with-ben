# J2249 — Titan real-surface thumbnail A v04

Built 6 November 2026 by Codex under J2162. Worker delivery; independent review remains required.

The requested 1280×720 JPEG, MANIFEST_v04.json and PHONE_PREVIEW_v04.jpg are in the shared Mini checkout at:
`02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Thumbnails/J2144_v02/`.
The manifest here duplicates the delivery manifest and records exact file hashes. Media remains outside git.

One contiguous crop of PIA07232, the real DISR surface photograph, supplies every background pixel. No compositing, synthetic detail or generated image. Arial Black 112 px (82 px cap height), yellow REAL and white SURFACE in the top band. Duration corner contains no text. The largest pebbles remain unobscured.

Source verified against [NASA’s official caption](https://science.nasa.gov/photojournal/first-color-view-of-titans-surface/), identifying the surface photograph and instrument. Credit: NASA/JPL/ESA/University of Arizona. [JPL policy](https://www.jpl.nasa.gov/jpl-image-use-policy/) requires credit and no endorsement; carry this credit in the eventual description. PIA06438 was checked and rejected: it is a descent mosaic, not the single surface frame required here. PIA08115 is a composite poster and was also excluded.

Validation: `thumb_preview.py long … --score` passes with mean HSV saturation 200.8 and near-black 0.016 (1.6%). Codex visually inspected both the full-size JPEG and generated 168×94 / 360×202 phone sheet: both words read clearly; the pebble pair is recognizable. B and C match J2162’s hashes exactly (see manifest).

Material limitation: the original image is intrinsically low resolution. The 304×171 landscape crop is enlarged 4.21× and looks soft at full size. This is not film picture-QA upscale compliance, and this delivery does not waive any applicable upscale gate. Independent review must explicitly judge the source softness and crop before approving it for Test & Compare. There is no AI upscaling or invented surface detail. The crop excludes the horizon; the foreground pebbles carry the promise.

Reproduce using the existing Mini Pillow environment:
`/Users/benjaminoats/_desk/venvs/thumbs/bin/python jobs/reviews/J2249/build_thumbnail.py --assets <delivery-directory>`
Then run `00_Brand/Channel-Setup/tools/thumb_preview.py long <A-v04.jpg> --out <PHONE_PREVIEW_v04.jpg> --score`.

Next: independent thumbnail review; retain B as lead and C unchanged per J2162. No publishing, upload, schedule or new spend. £0.
