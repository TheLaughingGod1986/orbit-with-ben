# J2452 — rejected March 2020 observation trial

Worker macbook. Continue macbook/J2452, existing PR #789. The compilation is incomplete. No finished master, reel, UAT, upload, generation, spend or NAS write in this run. HOS untouched.

## Continue the previous adopted checkpoint

Use the ALMA checkpoint recorded in RESUME_2026-11-11_NAS_CHECKPOINT.md and RESUME_2026-11-11_ALMA.md, SHA-256 `85d0090af6bb829b314b7a10dcdb703dce3565eb216c7114802016f8ef29c73b`. The shared audio candidate and its thirteen narration chapters remain unchanged. Seven source-reuse failures remain in the adopted chapter; no progress percentage was inferred from elapsed time.

## New candidate investigated and rejected

Official source: [Image of Betelgeuse’s surface taken in March 2020](https://www.eso.org/public/images/eso2109c/), actual SPHERE observation, credit **ESO/M. Montargès et al.**, 798×798 native pixels. [ESO terms](https://www.eso.org/public/outreach/copyright/) checked live: CC BY 4.0, visible full credit, adaptations identified. Downloaded native-resolution JPEG at `https://cdn.eso.org/images/large/eso2109c.jpg`. Source SHA-256 `bc6b5b454a53c4ad6e639a42643d5fe18475f646ebfaa867c262464a947cd288`; local `_desk/J2452-sleep-scratch/march2020_source_v01/eso2109c.jpg`.

The trial replaces chapter 357.30–364.9667 and 432.00–438.60 seconds, under general discussion of the star's uncertain future. It is not presented as December 2019 or as a future event. Full credit is visible; crop, 1.2% push, 15% sleep darkening and capped luma are recorded. The crop's maximum native enlargement is 2.334×. There are two appearances. Two-second endpoint dissolves preserve the narration clock. The source still and rendered midpoint were inspected, without claiming moving-picture or listening approval.

`march2020_v02/029_picture_march2020.mp4` in local scratch fully decodes, has 14,829 frames at exact 30 fps (494.30 s), and hashes to `dcc35b07f3601544136b5a58c394294090ba35252073dbe47b8aabb72c537b21`. Every replacement frame compared at 320×180 against its separately encoded patch: maximum errors 0.539 and 0.559 (limit 2). Seven unchanged samples also pass (maximum 0.544). These checks establish placement, not visual acceptance.

**Reject this candidate.** Normal combined picture QA fails seven rows: five inherited reuse rows plus two new near-black failures (means 16.60 and 16.61). The standalone patch also fails near-black and push jitter. No exemption or changed threshold. The previous seven-reuse-failure chapter remains the adopted checkpoint; replacing one kind of failure with another is not completion. Reports, cuts, hashes and source identity are in `march2020_rejected_v02/`; media stays local. `repair_march2020.py --diagnostic --out NEW_DIRECTORY` reproduces v02 only as an explicitly rejected diagnostic. v01 had a too-late outgoing fade and is also rejected. Do not repeat this crop/grade as a production solution.

Other examined official records were rejected before downloading: eso0927d is annotated artwork; eso2010a is an artist's impression of another star. No simulation was substituted. The existing eso0927e DSS view already appears twice and is not a fresh source.

## Remaining work

Choose genuinely suitable replacement picture for the seven remaining reuse windows, and remove retained graphics/baked labels. Finish twelve other picture chapters, the brightness ramp, quiet chapter names and inter-film breaths. Then assemble/mux, run final loudness/peak/silence/CTA/picture/join gates, make the approximately twelve-minute reel, and hash-copy final files to the working-film store before Ben's watch. Earliest air remains 12 December. Full remaining assembly exceeds this unattended run's 25-minute cap, so release at this clean diagnostic checkpoint rather than start another encode.

Python compilation, seven email-ratchet tests and diff check pass. The private-network test named by current main is absent on this older work branch, so it was not run. All processes launched by this run finished. Thread read to #6791603947; trusted messages were displayed, but the normal read command could not persist its home-directory marker under the filesystem restriction.
