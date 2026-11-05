# J2089 checkpoint v05

5 November 2026 · Codex worker · partial 1/4 · £0

Recovered existing PR491 branch at 8288cc1370 after its previous temporary
worktree was removed. Preserve all prior source decisions, 31 rendered overlays
and 17 mechanism previews; J2177 remains their named reviewer. No duplicate
render or motion download was started. The original four milestones remain.

## New completed harvest item

Downloaded the previously unavailable Webb Uranus image through a new official
NASA route, rather than retrying the blocked ESA CDN. Source:
https://science.nasa.gov/asset/webb/uranus-nircam-image/

Unannotated rendition: 2000×2000 PNG, 2,449,044 bytes; SHA-256
`e5f7a1a0e10a6e6c769b40ecbb2f4dd78ea2ada65f2e96efd69c113ea29f52a7`.
Media, source HTML, record and inspected preview:
`/Users/benjaminoats/_desk/cache/J2089/jwst_v01/`.
`harvest_webb_032.py` reproduces this download. `HARVEST_POOL_v01.json`
now records the file and evidence; `J2089_VERIFICATION_v05.json` records the
successful hash and decode/dimension check.

Exact credit: NASA, ESA, CSA, STScI, J. DePasquale (STScI).
The matching ESA release https://esawebb.org/images/weic2310a/ names that
credit; https://esawebb.org/copyright/ permits CC BY 4.0 use, including commercial
use, with its full visible credit and licence conditions. Both pages were read
with the web tool. Source is representative-colour infrared, not visible-light
natural colour. Codex viewed the preview: complete rings and no source labels.
Use as an inset preserving the rings over an approved graded moving plate;
1920-wide full-frame crop would cut the ring system. Final placement, near-black,
contrast and motion checks remain. This is a source still inspection, not KEEP.

## New concrete Dragonfly rights finding

The gallery's own footer links to https://www.jhuapl.edu/Home/Privacy, which
redirects to https://www.jhuapl.edu/privacy. That policy reserves redistribution
and commercial use for express written permission. Gallery playlist mediaid 503,
DragonflyatTitan2025.mp4, has an empty credit field. No asset-specific rights
grant was found. NASA sponsorship or availability of a download is insufficient
clearance. The pool now records a rights HOLD rather than an assumed PD licence.
Local policy evidence and its hash are recorded beside the Webb download.

Chief's remaining protected call: supply existing written permission or scope a
rights-cleared alternative for the APL rows. Do not send a permission request to
APL without explicit authorisation. J2177 separately owns the 17 mechanism-still
review and frame-0/reuse decisions. Preserve those existing owners; this run did
not claim or perform another job.

## Resume

Use PR491, now with this checkpoint, and the current four-step plan (1/4).
Remaining harvest, real-body mechanisms, approved mechanism renders, composites
and full checks exceed one unattended run. Read the parent queue history before
resuming: main does not yet contain PR491's production files. Worktree for this
run: `/private/tmp/J2089-wt`, branch `worker/J2089-source-completion`.
No background process, spend, publishing, script/VO change, film PASS or Ben action.

Both channel pulls completed. No HOS desk or channel-balance task was selected.
NAS offload ran under the <20GB rule; no eligible scratch, about 15.5GB free.
Audio and moving-video input remain undemonstrated. Preliminary v02 source probes
were preserved in `~/_desk/rescue/J2089-20261105-source-probe/`; they do not replace
the established harvest pool. All new committed files are text/code only.
