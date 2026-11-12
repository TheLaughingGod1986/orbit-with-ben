# J2176 — J2196 source scope exhausted

5 November 2026 · Codex · OWB:032 · £0

**FIX / incomplete.** Inspected the three official originals in the order J2196 specifies. No new thumbnail A passes this scope. B and repaired C SHA-256s still match the existing manifest. No panel release, publishing or final PASS.

- **PIA14602:** 1024×1024. A full-moon 16:9 crop `(0,235,1024,811)`, saturation 2× and brightness 1.25×, still measures **67.56% near-black**, above 30%, before text. Source itself is 81.98%. The smaller-hero fallback increases the empty dark field. This is a background/layout conflict, not a resolution failure; the resolution-only fallback does not waive it.
- **PIA21890:** 1024×1024. Visually inspected the official JPG: Titan is already clipped at the top and bottom. A crop cannot recover the whole hero. No invented pixels or image extension.
- **PIA14922:** 1417×1326. Titan is roughly 125 px tall in the source (under 130 even allowing a generous limb bound). At 2.35× it remains under 306 px, below J2196’s explicit smaller-hero floor of 324 px (45% of 720). Saturn otherwise dominates. The official caption also gives 46 km/pixel for a 5,150 km Titan, corroborating the low native detail. No upscale waiver.

These are source and composition rejections, not a claim that a finished candidate passed `thumb_preview.py`. No new final JPEG or phone sheet was produced for a rejected source. Existing delivery manifest remains unchanged and explicitly incomplete.

## Next action

Stop unchanged-source retries. A separate review must choose a materially different composition scope: the concrete proposal is the already verified PIA14602 real Titan over a separately rendered, graded space background, keeping the moon whole, source resolution, exact THIS IS TITAN / yellow TITAN, cap height, text clearance, near-black/saturation and phone gates. That proposal changes the current single-image/no-composite requirement and is **not authorised or executed by this worker delivery**. No generation or spend is needed. The current brief remains blocked on failed composition constraints; it is not waiting merely because a Chief is unavailable.

The independent panel J2159–J2161 and synthesis J2162 remain dependent on a complete repaired set. Do not send them the rejected A as a replacement. Preserve B/C exact hashes in the JSON evidence.

## Provenance

- https://www.jpl.nasa.gov/images/pia14602-hazy-orange-orb/
- https://www.jpl.nasa.gov/images/pia21890-a-last-look-at-titan/
- https://www.jpl.nasa.gov/images/pia14922-colorful-colossuses-and-changing-hues/
- https://www.jpl.nasa.gov/jpl-image-use-policy/

Official JPEG downloads and hashes are in J2196_SOURCE_CHECK.json. Credit: NASA/JPL-Caltech/Space Science Institute. Official captions identify real natural-colour Cassini imagery (published filter combinations); no additional third-party ownership restriction was found on these captions. No logo, person, or implied endorsement is used.

Operational: both repos up to date; HOS inbox empty. Input inventory supports still inspection, with no demonstrated audio/moving-video input. NAS offload ran and found no eligible old scratch. Existing shared staged changes were left untouched; evidence committed from an isolated clean worktree.
