# Draft quality and structural validation — v03

Codex, 18 November 2026. Scope: written script and production plan, not a finished-film, audio or motion review. Separate Gemini findings and disposition are recorded alongside this file. No VO lock or final film PASS is asserted here.

- Narration: 3268 whitespace-delimited words, 19767 characters including paragraph breaks and final newline; below the 21,000-character plan limit. Estimated 24.95 minutes at 131 words/minute; measured timing awaits narration.
- 58 paragraph blocks and six chapters. All 247 sentence rows reconstruct the narration exactly, with no omitted or duplicated words. Source-register entry for every block; each picture row inherits its evidence IDs.
- Every sentence has either a specific original map/schematic instruction or a catalogued photograph with collection, ID, rights statement and source URL. Five archive items; later photographs are explicitly contextual and dated. Download inspection, resolution confirmation and file hashes remain J2996 work.
- First paragraph establishes convoy vulnerability and the enemy advantage in approximately 23 seconds. No intro, invented dialogue or expert persona. Problem progresses through range, organisation, sensors, ONS 5, SC 130 and the May reversal.
- Editorial pass: British spelling, convoy names written for speech, careful distinction between sightings and sinkings, no unsupported loss totals, no fixed 600-mile gap, no ONS 5 aircraft victory in fog. Sources distinguish testimony, official histories and explanatory inference.
- Picture plan is deliberately schematic and map-heavy; the editor should animate only the proposition being spoken, vary details within longer sentences and use the real maintenance/aircraft photographs as visual relief. No present asset is claimed to depict a particular attack.
- Automated checks: voice export matches structured text; unique sentence IDs; all paragraph texts match sentence reconstruction; complete source/picture fields; no email addresses anywhere in the film folder. No media added to git.

Narration SHA-256: `4a46801b1b586558f7ddd8886bff8317f53084d9fc44994874bedfaab039b63a`.

## Handoff

Review and merge this PR before J2995 records NARRATION_v03.txt. Old v01/v02 material in draft_history is historical context only; do not narrate or harvest from it. J2996 replaces estimated chapter/shot timing with measured narration timing, harvests and visually checks originals, draws maps and builds the first cut. One finished-film quality pass and Ben’s watch remain downstream. No account setup, upload, publishing, paid generation or paid API request was made by this job.

## Chief lock — 18 November 2026

J3031 accepts the independent Gemini review and locks unchanged narration for J2995 after merge. See jobs/reviews/J3031/DECISION.md. This supersedes the draft handoff above.
