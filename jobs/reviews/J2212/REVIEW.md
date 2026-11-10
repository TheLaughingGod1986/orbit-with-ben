# J2212: 032 thumbnail A, composition after J2196 sources failed (rule H review)

5 Nov 2026 · Claude (review lane) · £0 · evidence PR #521 (`8e1a673ac4`, J2196_SOURCE_CHECK.md/json)

## Verdict: FIX. No composite; drop the whole-moon requirement instead.

Codex's proposal (real PIA14602 Titan over a code-rendered space background) would break LEARNINGS rule 19 ("a single striking real spacecraft frame ... no composite"). It would also sidestep the ≤30% near-black cap, which AGENTS.md says stands until the Chief adopts a change. Neither is needed. The failures all come from my J2196 requirement that Titan be **whole**: a whole moon on black space is mostly black by nature. SEA/Astrum's real-image thumbs fill the frame with the subject. So:

**J2196 is amended: A = Titan filling the frame, one real frame, limb clipping allowed.** Everything else in J2196 stands: hook THIS IS TITAN with yellow TITAN in the top band, ≤2.35× upscale on the cropped region, `--score` GRADE, 168 px phone sheet, credit NASA/JPL-Caltech/Space Science Institute.

## Recipe, in order; take the first that passes every gate
1. **PIA21890** "A Last Look at Titan" (sha256 `fa57f39f…`, 1024×1024). Its only failure was "moon clipped top and bottom", which is now allowed. 16:9 crop 1024×576 centred on the brightest haze band and the limb; 1.25× to 1280×720. Grade as J2144 (saturation up to pass ≥100, or ≥85 with `--pale`, since Titan's haze is a naturally pale subject). Keep the top 25% clear enough for the hook, over haze, not black.
2. **PIA14602** "Hazy Orange Orb" (sha256 `ee4057ff…`, 1024×1024). Tight 16:9 crop with the disc at ≥85% of frame width, top and bottom of the disc clipped, crop width ≥545 px so upscale ≤2.35×.
3. If both fail near-black (>30%) or GRADE: stop and park with the `thumb_preview.py --score` numbers. Do not composite, extend or invent pixels.

The ruling is met when `thumb_preview.py long <A> --out <sheet> --score` passes, the phone sheet reads THIS IS TITAN at 168 px, B and C hashes are unchanged, and the manifest is updated. Then release the panel J2159–J2161 and synthesis J2162 as planned.

Unchanged: no spend, no generation, no publishing, no final PASS.
