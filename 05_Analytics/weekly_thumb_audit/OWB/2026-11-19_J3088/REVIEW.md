# J3088 — Saturn and JWST revised candidates

19 Nov 2026 · worker macbook · maker Codex · £0 spend · proposed only.

Implements J2844 FIX. T038 Fermi and its approved file remain unchanged (hash rechecked). No YouTube, title, privacy, schedule or test changes. T037 and T039 remain proposed with no start date. Their previous proposals are preserved in ledger history.

## Revisions and visual checks

- **T037:** real PIA08329 Saturn remains dominant; RINGS ARE LEAVING retained. Smaller white arrow points at the rings, not a direct image of ring rain. Added NASA Cassini illustration in a separate lower-left inset, with the long antenna tips cropped to make the bus/dish readable. This is a story character, not a physical size comparison. No Orbit.
- **T039:** BABY GALAXIES, with GALAXIES yellow; NASA Webb illustration in a separate lower-left inset. The 440-pixel loupe is 34.375% of the 1280-pixel frame, centre (950,373), bottom 593; its black outline ends before the badge zone at y=600. Existing JADES source and -28 degree roll retained. Native 64-pixel patch enlarged to 440: **6.875 times linear resize**, not 4.5x and not an angular magnification claim. No generative detail. Removed the old synthetic origin brightening; source circle remains (468,434), radius 34. The redder lower component is the target; the adjacent foreground component remains visible and is not independently marked as the high-redshift galaxy.
- Inspected both full-size candidates and exact 168x94 tiles with a simulated duration badge. Hooks and spacecraft silhouettes remain recognizable; small inset name labels are secondary, not relied on for phone recognition. Saturn/rings and the JWST loupe remain the heroes. Independent reviewers must still judge composition and scientific target clarity.
- `thumb_preview.py long --score`: Saturn saturation 171.9, near-black 14.5%; JWST saturation 175.8, near-black 15.0%; both colour checks PASS. This is not Chief approval.
- Both JPEGs are 1280x720, under 2 MB. SHA-256 checked after each NAS copy. Prior v03 files, including Fermi, still match the J2983 manifest. No prior file replaced or deleted. PHONE_SHEET_v01 is an initial layout with overlap; **use PHONE_SHEET_v02** below.

## Required independent panel and Chief decision

Critics: independently assess the exact candidates below at 168x94, against the unchanged titles and film promises; do not read one another's critiques. In particular, check **BABY GALAXIES** against JWST Scene 04 and the current title, its plural wording, and the distinction between a young universe and a measured galaxy age. The scene says that some confirmed galaxies shine when the universe was about three hundred million years old, then calls that cosmically young. The hook is a proposed shorthand, not a script rewrite. Check the two-component source and whether the origin/loupe link is honest. Check Cassini/Webb recognition and the inset's clear non-scale relationship.

After the independent panel synthesis, the elected Chief must review exact files and either (a) issue exact-file PASS plus explicit successor-test authorization over **the recorded finished T018 report for T037** and **the recorded finished T007 report for T039**, conditional on a fresh Studio read showing that exact finished report and no running test, or (b) give an exact fix list. No authorization is implied by colour scores, this worker report or panel advice. Do not replace a running test.

**J2845 and J2847 remain blocked.** Only the Chief decision may update their briefs to the new paths, hashes and current ledger IDs and release them if all conditions hold. Keep live A, titles and all other YouTube settings unchanged. Historical title-B proposals are not authorization.

## Source verification

- [NASA PIA08329, In Saturn's Shadow](https://science.nasa.gov/resource/in-saturns-shadow/): actual Saturn/ring image; NASA/JPL/Space Science Institute credit.
- [NASA JADES-GS-z14-0 pullout](https://science.nasa.gov/asset/webb/jades-gs-z14-0-pullout-nircam/): annotated source inspected against the existing cutout, preserving the redder component. Credit NASA/ESA/CSA/STScI.
- [NASA spacecraft icons](https://science.nasa.gov/multimedia/spacecraft-icons/): existing NASA transparent illustrations of Cassini and Webb, not newly generated. Download URLs and hashes below. NASA-created illustrations are used with NASA credit; no third-party credit appears on these icon entries.

## Exact files and provenance

### T037 — m09jUdwC5hk

Title (retained from existing package): How Long Will Anything in Space Last?

Candidate: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J3088_v01/m09jUdwC5hk_B_v06.jpg`

SHA-256: `7b0f6c44e870820881dba0309bf73ef0cc5601fef83cf080438a06648c9eb19f` (285269 bytes).

Live A: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/m09jUdwC5hk_live_A.jpg`

### T039 — ziKBPJ6FY0U

Title (retained from existing package): JWST Found Galaxies That Shouldn't Exist Yet

Candidate: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J3088_v01/ziKBPJ6FY0U_B_v07.jpg`

SHA-256: `e2bd0c629610195b6fa858bd7969d7ebcb97c4a37d3420084409d0dfa828446b` (429754 bytes).

Live A: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J2834_v03/ziKBPJ6FY0U_live_A.jpg`

Phone sheet: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J3088_v01/PHONE_SHEET_v02.jpg`

SHA-256: `b5b78f36adefff3c472c2c38d0a5b8d2e67a8bd43e6355a13f361a9538cc0346`

Full manifest:

```json
{
  "job": "J3088",
  "date": "2026-11-19",
  "agent": "macbook",
  "maker": "codex",
  "status": "proposed; independent panel and Chief exact-file decision required",
  "builder": "00_Brand/Channel-Setup/tools/build_weekly_thumbs_j3088.py",
  "spend": 0,
  "source_pages": [
    "https://science.nasa.gov/multimedia/spacecraft-icons/",
    "https://science.nasa.gov/resource/in-saturns-shadow/",
    "https://science.nasa.gov/asset/webb/jades-gs-z14-0-pullout-nircam/"
  ],
  "inputs": [
    {
      "name": "JADES_GS_z14_0_cutout.png",
      "sha256": "e9b2342e36302c7394e754db6c3b9f0b389e3b5db0cd373e03a278683df0c886"
    },
    {
      "name": "JADES_GS_z14_0_field.jpg",
      "sha256": "b666562568d2777565014d3495d6c7f369ff32e4ef99aac51787adc447d7066b"
    },
    {
      "name": "PIA08329.jpg",
      "sha256": "a8ed6971f419c2a7ae5f997d67db9ce7f42c9407a30bfcafceccd0728044a0fe"
    },
    {
      "name": "PIA08329.tif",
      "sha256": "646c5e8d7d68f30f939d9e3d6f54ddf7a9575deb3b7882a9353b003ef9671e69"
    }
  ],
  "phone_sheet": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J3088_v01/PHONE_SHEET_v02.jpg",
  "phone_sheet_sha256": "b5b78f36adefff3c472c2c38d0a5b8d2e67a8bd43e6355a13f361a9538cc0346",
  "designs": [
    {
      "video": "m09jUdwC5hk",
      "ledger_id": "T037",
      "prior_draft_file": "m09jUdwC5hk_B_v05.jpg",
      "film": "005_The-Last-Star-In-The-Universe (owb_compilation_v05)",
      "live_title": "How Long Will Anything in Space Last?",
      "hook": "RINGS ARE LEAVING",
      "yellow": "LEAVING",
      "file": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J3088_v01/m09jUdwC5hk_B_v06.jpg",
      "bytes": 285269,
      "sha256": "7b0f6c44e870820881dba0309bf73ef0cc5601fef83cf080438a06648c9eb19f",
      "sources": [
        "NASA/JPL/Space Science Institute PIA08329.tif (Cassini 'In Saturn's Shadow' backlit Saturn & rings mosaic PIA08329, public domain)"
      ],
      "hook_box": [
        51,
        30,
        1210,
        122
      ],
      "score": {
        "file": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J3088_v01/m09jUdwC5hk_B_v06.jpg",
        "saturation": 171.9,
        "near_black": 0.145,
        "fails": []
      },
      "prior_file": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/m09jUdwC5hk_B_v05.jpg",
      "prior_sha256": "6f9512774d0d4e3bab181017729dfda396c0612755a4b57bf02810cd62dd8b69",
      "live_a_file": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/m09jUdwC5hk_live_A.jpg",
      "live_a_sha256": "d86457f3a6d6b96dc448a7ac72840d4e341b6e5e95eb52d91b00cf5741a6bcef",
      "craft_source": "https://science.nasa.gov/wp-content/uploads/2023/05/cassini.png",
      "craft_sha256": "3466f42b90c07ba0271db0686cfd39f6e07536642e1e238516ce124d04c180f3",
      "craft_credit": "NASA; existing spacecraft illustration, cropped and scaled as a separate non-scale story inset"
    },
    {
      "video": "ziKBPJ6FY0U",
      "ledger_id": "T039",
      "prior_draft_file": "ziKBPJ6FY0U_B_v06.jpg",
      "film": "004_JWST-Discoveries-That-Change-Everything",
      "live_title": "JWST Found Galaxies That Shouldn't Exist Yet",
      "hook": "BABY GALAXIES",
      "yellow": "GALAXIES",
      "file": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J3088_v01/ziKBPJ6FY0U_B_v07.jpg",
      "bytes": 429754,
      "sha256": "e2bd0c629610195b6fa858bd7969d7ebcb97c4a37d3420084409d0dfa828446b",
      "origin_circle_px": [
        468,
        434,
        34
      ],
      "loupe_px": [
        950,
        373,
        220
      ],
      "sources": [
        "NASA/ESA/CSA/STScI JADES-GS-z14-0 NIRCam deep field & pullout (STScI-01HZ083EXXCJNE64ERAH2ER2FM / STScI-01HZ08HBSZYHDA52NPPB1BP4SR, spectroscopically confirmed z=14.32 galaxy ~290-300 Myr after the Big Bang, public domain)"
      ],
      "script_verification": "02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/01_Script/jwst_script_master_v01.md Scene 04 line 143: 'Some of the galaxies Webb confirmed are luminous when the universe was only about three hundred million years old.'",
      "hook_box": [
        105,
        25,
        1157,
        127
      ],
      "score": {
        "file": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J3088_v01/ziKBPJ6FY0U_B_v07.jpg",
        "saturation": 175.8,
        "near_black": 0.15,
        "fails": []
      },
      "prior_file": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J2834_v03/ziKBPJ6FY0U_B_v06.jpg",
      "prior_sha256": "ffcb7a69ad24434fb2c814682aa58e126de6cb77e047916316b3fb8dd9a14478",
      "live_a_file": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J2834_v03/ziKBPJ6FY0U_live_A.jpg",
      "live_a_sha256": "a25ab9578e3d583bb826597ee52e631bb902ed3c5e2a82f3d307d72751e24adc",
      "craft_source": "https://science.nasa.gov/wp-content/uploads/2023/05/webb_1.png",
      "craft_sha256": "9f520a9bf2d9b39659088b8c2fd963c128fcdd2f71dfbd4563e5466246e758a3",
      "craft_credit": "NASA; existing spacecraft illustration, cropped and scaled as a separate non-scale story inset",
      "loupe_resampling": {
        "input_patch_px": 64,
        "output_diameter_px": 440,
        "linear_resize_factor": 6.875,
        "frame_width_fraction": 0.34375,
        "center_px": [
          950,
          373
        ],
        "bottom_px": 593,
        "roll_degrees": -28,
        "target": "redder lower component; adjacent foreground component retained, not identified as target"
      }
    }
  ],
  "prior_files_verified": {
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/m09jUdwC5hk_B_v05.jpg": "6f9512774d0d4e3bab181017729dfda396c0612755a4b57bf02810cd62dd8b69",
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/08_Thumbnails/repackage_2026-11/J2834_v03/Mo93x0fxB1Q_B_v05.jpg": "95d1a92bd988667743c068e4fe69d67b5d6eeea7097aad2a28de9151d7836578",
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J2834_v03/ziKBPJ6FY0U_B_v06.jpg": "ffcb7a69ad24434fb2c814682aa58e126de6cb77e047916316b3fb8dd9a14478"
  }
}
```
