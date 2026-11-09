# J2089 checkpoint v22 — reviewed R23 export

6 November 2026 · Codex · GBP0 · original milestone 1/4.

Resumed clean local 510197ffe4 in /private/tmp/codex-J2089. Applied J2304:
exported r23_landing_record with unchanged frame generator, source crop and
reviewed preview hash. SHOT_LIST_v06 records qualitative landing record instead
of unsupported quantitative landings_chart; duplicate r23_fact stays preserved
but is omitted from assembly. PIA14909 allocation is R19+R23 only, recorded in
HARVEST_POOL_v01. R23 requires real moving separation from R22 and a graded
plate, with final rights/contrast/timing/reuse gates still required.

Verified 108 decoded frames exactly equal reviewed generator pixels, qtrle ARGB
1920x1080, 30fps, 3.6s; preview/source/render hashes match. Three invalid approval
combinations rejected before creating output. All 61 earlier MOV hashes remain
unchanged; 62 total in J2089_EXPORT_HASHES_v22.json. All 52 shot-list row timing,
duration and cut signatures unchanged. No moving-video/audio perception claimed.
Render is in ~/_desk/cache/J2089/landing_record_renders_v01. No background job.

Remaining licensed harvest, frame0, Huygens seam/crop and APL permission holds,
composites and final gates exceed this run. Original 1/4 remains. Existing
automatic-review public-push rejection is retained: local checkpoint only,
no push attempted or bypassed. No spend, publishing, locked VO/script change,
film-stage PASS, merge or Ben request. Resume this local branch, not main.
