# J0271 — three thumbnail B candidates

Advisory handover by Codex, 15 October 2026. Chief has not approved these candidates. No YouTube change, no test armed, no final PASS or merge.

## Deliverables

All artwork, final JPEGs and literal 168×94 A/B sheets live in `/Users/benjaminoats/_desk/J0271-thumbnails/`. The accompanying `J0271_manifest.json` records final paths, byte sizes and SHA-256 hashes. Images are not committed. The reproducible typography builder is `j0271_build.py`; it uses Arial Black with white text and a yellow hook word, clear of the duration badge. A images were fetched read-only from each video's public YouTube thumbnail URL on this run; Studio must reconfirm the current A before arming.

| Video | B hook | B file / sheet basename | Lifetime CTR | Impressions |
|---|---|---|---:|---:|
| Mo93x0fxB1Q | ALIENS HIDING? | fermi_B_v01.jpg / fermi_AB_v01.jpg | 0% | 93 |
| NbW5G1BpPY0 | A HIDDEN OCEAN | europa_B_v01.jpg / europa_AB_v01.jpg | 1.3% | 78 |
| ziKBPJ6FY0U | GALAXIES TOO SOON? | jwst_B_v01.jpg / jwst_AB_v01.jpg | 1.6% | 128 |

All are below 500 impressions; these are test priorities, not evidence of a winning redesign. Europa holds the live hook constant while changing the artwork. The full two-channel ranking and exclusions are in `THUMB_REDO_PLAN_2026-10-15.md`.

## Checks actually run

`thumb_preview.py long <B> --out <preview> --score` returned exit 0 for each final JPEG:

```
PASS  fermi_B_v01.jpg  saturation=191.0  near_black=16%
PASS  europa_B_v01.jpg  saturation=155.9  near_black=13%
PASS  jwst_B_v01.jpg  saturation=174.7  near_black=5%
```

These are automated colour-check results, not a Chief approval. Each file is RGB 1280×720 and under 2 MB (366892 / 419713 / 475032 bytes). Codex inspected each 168×94 A/B sheet: words legible, text clear of the hero and duration badge. No title, privacy, schedule or channel setting changed.

The first JWST art scored near-black 39% and failed. A built-in image edit lifted shadows; its final 5% score is above. The initial art remains saved separately. The original generated Fermi composition crops the lower Earth and places a telescope on a foreground surface: Chief should judge this conceptual scale composition against the whole-subject preference. JWST uses a generic illustrative galaxy, not an actual observation of a named early galaxy; Chief should judge whether that implication fits the film. Europa's ocean cutaway is explicitly concept art. All three need Chief's creative/content review, beyond colour metrics.

## Authorisation and handoff

Built-in image generation was used under J0271's approval; no API key, payment, top-up or paid fallback was requested. The tool exposes no model-selector field, so the provenance records the built-in tool, not an independently verified model ID. Art prompts and the lighting revision are in `J0271_PROMPTS.md`.

The brief says “Orbit for OWB”, but does not explicitly waive the Never rule banning Orbit on thumbnails; these candidates contain no robot. Chief can resolve that creative exception without another request to Ben.

`thumb_ledger.py add` created T005–T007 in this branch. Because the CLI defaults to running, these three entries were immediately corrected to `queued`, with no start date. They are proposals only.

Remaining work was queued: J0273 (Moon, Last Star, Neutron Star), J0274 (Alien Worlds, HOS Germs). Each must recheck reservations before generating. HOS generation must follow its own rules; any conflict with built-in image generation parks for Chief.

Next: Chief chooses or requests revisions, then a separately authorised Studio job arms thumbnail-only Test & Compare after checking that no test is running. Merge remains Chief's call. Nothing is needed from Ben for these prepared candidates.
