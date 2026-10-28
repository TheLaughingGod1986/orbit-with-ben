# J1110 — verified archive, disk target unresolved

Worker: codex. 28 October 2026. GBP 0. No Chief ruling.

Archived 26 superseded exports (0.990 GB logical size). Free space: 15.822 GB before, 16.782 GB after. APFS/compression and concurrent activity mean logical size is not equal to physical space recovered.

## Verification

- Archive ran detached as `J1110-archive`; exit code 0. Log and done file: `~/_desk/logs/J1110/archive.log`, `archive.done`.
- rsync to the same relative path under `/Volumes/data/mac-mini-archive/orbit-with-ben/`. Existing different NAS copies were never overwritten.
- SHA-256 computed locally, checked on the NAS, and checked locally again before removing each source.
- Matching `<filename>.J1110.sha256` manifests remain in the local and NAS folders. Local `MOVED_TO_NAS.txt` entries identify every destination and hash.
- Final check: all 26 NAS files exist with expected lengths; source media absent; both manifests and move markers match. Full path/hash manifest: `SHA256SUMS.txt`; machine-readable record: `ARCHIVE.json`.

## Protections

Only untracked MP4 exports older than the newest two distinct numeric versions in their cut/PHONE group were eligible. Versions 13 and 13a share numeric version 13, so version 12 is also retained. Filename references in non-done/non-cancelled queue entries and both upload registries were excluded. All Betelgeuse upload media and J1100 active-fix cuts were additionally excluded. Current scheduled files, protected replacement files and newest-two versions remain local. No HOS files selected; no YouTube or NAS deletion; no paid work.

## Remaining block

The 30 GB target is unmet; free space remains below J1100's 20 GB rendering requirement. J1100 stays blocked. Chief must choose a broader safe disk cleanup or archiving scope before its disk prerequisite can be released.

`mini_repair.py` dry run identified clean pushed temporary worktrees eligible for its own cleanup, including `/private/tmp/codex-J1085-verify`, `J0961-wt`, `j0984-chief-review`, `j1066-review-complete`, `j1075-chief-review`, `j1080-verify`, `J1084-chief-review`, `J1084-wt`, `J1090-chief-review`, `J1090-wt`, `J1101-wt`, and `J1102-wt`. They are roughly 0.5 GB each, but J1110 permits local deletion only of verified archived media, so these were left in place. Revalidate ownership and pushed/clean state before any later cleanup.

The targeted folder survey found about 6.6 GB allocated across OWB film projects in total; the largest HOS edit folder was 006 at about 1.45 GB. The large current masters, source pools, and single/latest versions are not eligible. A supplementary desk media scan found no media over 100 MB. The broad home survey was stopped after it proved too slow; no claim of a complete whole-disk audit.

## Archived paths

All paths below are relative to the OWB repo; NAS copies use the identical path under the archive repo folder.

- `02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/10_Shorts/lift_ten_metres_thin/06_Final-Exports/saturn_ten_metres_thin_v02.mp4`
- `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/mon09_night_cold/06_Final-Exports/mon09_night_cold_v02.mp4`
- `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/wed11_opening_testA/06_Final-Exports/wed11_opening_testA_v04.mp4`
- `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/wed11_opening_testA/06_Final-Exports/wed11_opening_testA_v03.mp4`
- `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/wed11_opening_testA/06_Final-Exports/wed11_opening_testA_v04_PHONE.mp4`
- `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v03.mp4`
- `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/thu12_length_test_dust_v02.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v07_PHONE.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v08_PHONE.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v11_PHONE.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v09_PHONE.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v10_PHONE.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v07.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v06.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v10.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v04.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v11.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v08.mp4`
- `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v09.mp4`
- `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/mon30_comets/06_Final-Exports/028_short_mon30_comets_v02.mp4`
- `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/wed02_opening_testA/06_Final-Exports/028_short_wed02_opening_testA_v02.mp4`
- `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/lift_oort_marbles/06_Final-Exports/028_short_lift_oort_marbles_v01_PHONE.mp4`
- `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/lift_oort_marbles/06_Final-Exports/028_short_lift_oort_marbles_v01.mp4`
- `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/wed18_robot_reach_nearest_star_v02.mp4`
- `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/fri20_grapefruit_cherry/06_Final-Exports/fri20_grapefruit_cherry_v02.mp4`
- `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/10_Shorts/lift_sudden_air/06_Final-Exports/earth_sudden_air_v03.mp4`
