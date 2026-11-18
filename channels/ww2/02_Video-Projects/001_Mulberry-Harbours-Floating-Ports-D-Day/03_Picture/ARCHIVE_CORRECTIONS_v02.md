# WW2:001 archive correction pass — J2993

Codex covering, 18 November 2026. Work in progress; no finished cut or QA PASS.

Inspected a contact sheet of all 17 downloaded files against their supplied mirror captions and the original shot list. All 17 file hashes match the harvest manifest. Exact findings and source links are in `archive_editorial_review_v02.json`. This is subject screening, not full-resolution picture QA or primary-source rights clearance.

The original shot list is not safe to assemble literally. 80-G-285167 shows a vehicle unloading from LST-543, not a caisson tow or storm damage. 80-G-285176 likewise shows LST unloading, not blockships. 80-G-285123 shows a Gooseberry ship line, not broken bridge spans. SC 195881 shows a half-track on a floating roadway, not storm aftermath. A 24066 is a Rhino ferry, not a Phoenix tow. BU 1024 is a September overview: any June opening must label it as a later view, not date the photograph to the narration.

Use 80-G-285176/285167 for the unloading section and 80-G-285123 for the blockship section once rights and full-resolution inspection are complete. Obtain real storm photographs before cutting S35–S41. Do not invent visual proof by changing captions.

Nine archive IDs ended in HTTP errors; six short IWM T/TR identifiers remained unresolved. A downloader exit of zero is not success for these individual assets. One ERROR record already contains a successfully downloaded candidate, so inspect files within error records too. Duplicate A 24066 scans are the same scene, not additional coverage.

The channel permits US/UK official photographs. Do not use Canadian C-029878 or the proposed Tate painting; replace these with eligible official photographs or a clearly labelled code diagram. No exception is granted here. Several mirrors are only 800 pixels wide and need larger originals before full-screen treatment. No credit was spent, no upload occurred, and no media was committed.

Next: retry failed eligible IDs; resolve PLUTO photographs using specific catalogue records; verify primary captions and rights; replace mismatched and underspecified shots; inspect the four fuzzy audio anchors; finish remaining graphics; assemble, perform technical QA and submit the finished film for Ben’s watch.

## Detached continuation

Retry only the eight failed US/UK IDs, excluding Canadian C-029878. Session `J2993-archive-v02`; launcher `/Users/benjaminoats/_desk/ww2/J2993/retry_archive_harvest_v02.sh`; log `/Users/benjaminoats/_desk/logs/J2993-archive-v02.log`; completion `/Users/benjaminoats/_desk/logs/J2993-archive-v02.done`. Missing completion means still running. Do not start another copy. Read individual manifest records after exit. Existing PR #1012 and worktree `/tmp/J2993-wt` remain the continuation point.
