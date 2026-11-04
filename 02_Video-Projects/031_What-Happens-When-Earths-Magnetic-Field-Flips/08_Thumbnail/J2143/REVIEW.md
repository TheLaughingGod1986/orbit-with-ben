# J2143 — OWB 031 thumbnail proposal

2026-11-04 · Codex worker · **Chief approval pending.** No upload, live replacement, test start or title change. £0 cash/API spend; illustrative plates use the built-in image tool on the existing plan. No media committed.

## Deliverables

All three are 1280×720 JPEGs under 1 MB, in `/Users/benjaminoats/_desk/j2143/final/`. Phone review sheet: `/Users/benjaminoats/_desk/j2143/review/phone_ABC.jpg`. Full SHA-256 values and measurements are in `measurements.json`; inputs in `inputs.json`.

| Variant | Picture idea | Text | Test |
|---|---|---|---|
| A — `031_A_compass_v03.jpg` | Oversized brass compass, red needle to S, Earth for scale | COMPASS REVERSED | rule12 consequence |
| B — `031_B_real_v04.jpg` | One actual ISS aurora photograph, Earth's limb/city lights for scale | None | rule19 real-frame experiment |
| C — `031_C_bright_v03.jpg` | Hypothetical aurora over London, skyline/person for scale, bright cyan sky | GLOBAL AURORAS | rule12 consequence + rule14 bright background |

B replaces the earlier draft's satellite concept so the three-image set includes the specifically requested real-image trial. A and C are illustrations, not documented reversal photographs. C supports the locked script's London/city aurora scenario, not a forecast or evidence of a present reversal. A's decorative field strokes are illustrative, not a measured field model.

## Worker checks (advisory, not final PASS)

| Gate | A | B | C |
|---|---|---|---|
| HOOK | Names compass and reversal consequence | Aurora is the visual hook; zero words explicitly allowed by job/rule19 | Names auroras and global consequence |
| BAND | Two words, clear top band, white/yellow, no subject overlap | Textless exception from job: no band or yellow word required | Two words, clear top band, white/yellow, no subject overlap |
| GRADE | Tool PASS: saturation 194.5, near-black 9.0% | Tool PASS: saturation 133.3, near-black 24.1% | Tool PASS: saturation 171.0, near-black 3.6% |
| PHONE | Inspected 168×94 tile: both words readable, compass dominant | Inspected 168×94 tile: aurora arc and Earth limb recognizable | Inspected 168×94 tile: both words readable, curtain dominates skyline |

All exceed saturation target 120 and remain below 30% near-black. Full-size A/C and the source photograph were inspected, as was the final A/B/C phone sheet. No audio or motion perception is asserted or needed. Exact Arial Black lettering is rendered by `build_j2143.py`, visible cap height 82 px (11.4% of frame); the AI headline drafts are discarded. The original/generated draft files are retained outside git for traceability.

Chief should assess these three alternatives together and decide approval and final title pairing. B deliberately lacks the directional compass cue, testing whether the real picture wins attention. No claim of likely CTR uplift or a test winner. Ledger T020 is **proposed**, with no video ID or start date, tagged `rule19` (B), `rule14` (C), and `rule12` (set).

## Real-photo provenance and permission

- Identity: **ISS062-E-98264**, Expedition 62 astronaut photograph, 16 March 2020, Nikon D5 / 50 mm, provided by ISS Crew Earth Observations Facility and Earth Science and Remote Sensing Unit, NASA Johnson Space Center.
- Official source: https://science.nasa.gov/earth/earth-observatory/aurora-meet-airglow-147122/
- Download: https://assets.science.nasa.gov/content/dam/science/esd/eo/images/imagerecords/147000/147122/iss062e098264_lrg.jpg
- NASA describes this as one photograph, already cropped/enhanced and with lens artifacts removed. It depicts ordinary aurora and airglow near Alaska, not a magnetic reversal. Its factual use here illustrates the aurora subject; do not caption it as a reversal event or London.
- Credit for the eventual package: **NASA / ISS Crew Earth Observations / Johnson Space Center**. No third-party copyright notice on the image entry; no identifiable people or NASA logo in this frame. NASA's media guidelines allow factual educational use with source acknowledgement and no endorsement implication: https://www.nasa.gov/nasa-brand-center/images-and-media/ (checked this run).
- B uses only this photograph: bottom-aligned 16:9 crop, resize, saturation/gamma/brightness grade. **No generative edit, additions, compositing or text.** Exact ffmpeg recipe is in the builder. Source SHA is in `inputs.json`.
- The film's existing `GSFC_20171208_Archive_e001788` harvest is explicitly a six-orbit Blue Marble composite, so it was excluded from rule19. Other files present were Mars and Titan. This verified ISS image was sourced for this job rather than mislabelling that harvest.

## Rebuild and handoff

From the repo root, with Pillow and ffmpeg available:

```sh
python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/08_Thumbnail/build_j2143.py --assets /Users/benjaminoats/_desk/j2143/assets --out /Users/benjaminoats/_desk/j2143/final
python3 00_Brand/Channel-Setup/tools/thumb_preview.py long /Users/benjaminoats/_desk/j2143/final/031_*.jpg --out /Users/benjaminoats/_desk/j2143/review/phone_ABC.jpg --score
```

The Mini's working interpreter was `/opt/homebrew/opt/python@3.14/bin/python3.14`; the isolated worktree's default Python lacked Pillow. The explicit interpreter completed the builder and preview gate successfully. No package installation needed.

Next owner: **Chief**, review this pack/ledger and merge the evidence PR if accepted. Arm the three concepts only in the future authorised upload/Studio task, then fill the actual video ID/start date. Keep existing live tests untouched. J2143 is parked for this protected approval, not marked as an approved film stage.

Disk check: ~9 GB free; prescribed `nas_offload.py` check deferred to its 01:00–06:00 window. Only a small thumbnail pack was written; no NAS mutation or deletion.
