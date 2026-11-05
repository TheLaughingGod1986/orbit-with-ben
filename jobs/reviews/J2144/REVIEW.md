# J2144 — Titan thumbnail delivery

4 November 2026 · Codex worker · OWB:032 · £0 · pending independent review and Chief decision

Three finished 1280×720 JPEG concepts are in the film's local `09_Thumbnails/J2144_v01/` folder. Absolute paths and SHA-256s are in `MANIFEST.json`; no media is committed. `PHONE_PREVIEW.jpg` shows the actual 168×94 and 360×202 tiles (displayed at 2×).

| Concept | Hook | Picture | Saturation | Near-black |
|---|---|---|---:|---:|
| A / rule19 | ORANGE WORLD | Real Cassini PIA14922; whole Titan against Saturn, one source crop | 140.5 | 27.1% |
| B / rule14 | METHANE SHORE | Bright amber sky, hypothetical sealed astronaut beside a methane lake | 164.3 | 3.7% |
| C / rule12 | ICE IS ROCK | Generic hypothetical lander beside a large rounded ice cobble | 209.0 | 3.3% |

`thumb_preview.py long ... --score` returned exit 0 for all three. Each JPEG is below 600 KB. I inspected the full illustrations and the final phone sheet: hooks read, yellow words are present, no words touch the subjects, and the duration corner has no text. Final lettering is deterministic Arial Black from the supplied builders, rather than generated text. The lander's dish overlap was corrected before delivery. These are worker checks, not a Chief PASS.

## Source and honesty checks

A uses the exact PIA14922 mapping named by J2090 and this job. [JPL's asset page](https://www.jpl.nasa.gov/images/pia14922-colorful-colossuses-and-changing-hues/) identifies Titan in front of Saturn and credits NASA/JPL-Caltech/Space Science Institute. It is a published natural-colour mission mosaic assembled from six filtered exposures, not a single raw exposure. No new compositing or generative alteration was used: crop, conventional grade, resize and typography only. The approved job explicitly names this asset. The crop preserves all of Titan; Saturn supplies the background scale cue. Preserve the image credit in the eventual package under [JPL's use policy](https://www.jpl.nasa.gov/jpl-image-use-policy/).

B and C are scientific illustrations, built with the built-in imagegen tool on the existing plan. No API key, Vertex, ElevenLabs or paid API calls. B is not a record of human exploration. C is deliberately a generic lander, not a faithful reconstruction of Huygens or Dragonfly. Its glowing translucent first-draft stone was replaced with an opaque weathered cobble. Full prompts, including discarded intermediate lettering edits, are in `PROMPTS.json`; final text-free plates remain beside the JPEGs.

The locked script's chapters 2–4 support ice acting as rock and methane/ethane lakes. Recommend pairing the set with the existing draft **What Would Happen If You Landed on Titan?** The real-picture title options remain Chief's choice, but **do not pair the illustrative B/C with a title implying they are real Huygens photographs**. A is Cassini orbital imagery, not Huygens surface photography either. No title, script or public metadata was changed.

## Handoff

Ledger **T020** is **proposed**, tagged `rule19`, `tentpole`, `rule14`, `rule12`; no video id, start date, metrics or winner is invented. The three concepts require the independent packaging panel and Chief's title/picture decision before any future authorised Test & Compare job. Nothing was uploaded, scheduled or changed in Studio. Existing media and tests are untouched.

The capability record remains honest: still-image review only; no audio or moving-video perception claimed. NAS offload's dry run reported its overnight-window hold with about 10 GB free; this job produced small local thumbnail files and no render scratch batch.
