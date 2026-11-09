# J1317 — Chief picture ruling, 31 October 2026

Codex covering as elected acting Chief. Scope: J1317 evidence from J1308, not a new facts, script or audio review. Authority rechecked with chief_relay.py status: Codex elected; Grok and Claude marked down.

## Decision

**Frame-evidence delivery ACCEPTED. AR1 v01 picture PASS. AR2 v02 and AR3 v02 FIX. The three-Short cohort remains held: no Ben-watch handoff, upload or scheduling approval.** J1317 can close as a completed review once the correction job is recorded; completion is not a cohort picture PASS.

Reviewed all three full-size frame-0 JPEGs and every tile on the 0.5-second contact sheets (39/39/37 tiles), plus AR3's 10.0-second frame extracted directly from its master at full size. All three local master SHA-256 values match ASSEMBLY_REPORT.md and review_frames/README.md. Frame-0 images are 1080×1920; all sheets are 1008×4480 and below 1.5 MB. Existing script/facts/audio and automated composite-gate decisions in J1308 remain recorded; those passes do not replace visual review.

## Findings and required correction

| Cut | Ruling | Evidence and next action |
|---|---|---|
| AR1 v01 | Picture PASS | Clear Moon/asteroid hook, readable dated odds and miss-distance progression, no Orbit, and no title/graphic collision on the sampled sequence. Retain master SHA 49b3e4f0f7276885f942d3451978eba33c9a2fec68216fcafdd79466f877cd07 unchanged. This is picture approval only. |
| AR2 v02 | FIX | Frame 0, 0–2 s and later non-DATA station shots show a flat icon made from four blue rectangles and a white rounded block. assemble_j1308.py draw_iss() confirms this is a Pillow schematic, not the NASA 3D Resources model. h37 C4 explicitly permits moving footage of the actual ISS or a code render **from that NASA model**. Replace the opening, loop return and other non-DATA draw_iss shots with verified Crew-2 fly-around footage or a faithful render of that sourced model over sunlit Earth. Do not replace or reopen the separately h42-approved 109 m DATA graphic. Preserve the approved South Pacific map and timing. |
| AR3 v02 | FIX | At 9.0–11.0 s the opaque geography map lies directly across the eclipse disc/corona; the 10.0 s master frame confirms the overlap. The image now combines a geographic path and an obscured eclipse in one focal area. This fails the standing overlay rule to keep graphics off the subject and show one idea clearly. Keep the approved path graphic, timing, countries and facts; put that interval over a suitable moving Earth/ocean plate with the graphic clear of its subject. Show the 2017 eclipse unobscured in the adjacent eclipse interval. Retain 2017 and NASA/Aubrey Gemignani attribution whenever those plates are used. |

AR2's Bahamas/Discovery exclusions and AR3's NOAA crop and 2017 attribution are visibly respected in the delivered evidence. No script/VO changes, new factual claims, title changes, paid generation or fresh music are requested. Existing test-specific length and timing authorisations remain in force.

## Follow-up acceptance

One assembly correction job follows this review. It must write new AR2 and AR3 versions beside the old masters, preserve all old files/hashes, rerun the applicable picture/polish/loop/SFX gates on the actual composites, and provide new frame-0 images and 0.5 s sheets plus hashes and raw gate outputs. The next Chief checks both corrected sequences before cohort picture approval and any Ben-watch handoff. No external date/credit/Ben wait is introduced: this is actionable GBP0 assembly work dependent only on this recorded ruling. Do not start duplicate detached renders.

Disk preflight found about 9.7 GB free. Authorised nas_offload.py --apply found no eligible old scratch; no NAS files changed. The correction worker must respect the disk/render-scratch rules before rendering.
