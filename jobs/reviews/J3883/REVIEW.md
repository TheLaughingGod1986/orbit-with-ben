# J3883 — corrected OWB:064 package integration

2026-11-27 · codex, elected acting Chief (relay status rechecked before ruling).

**KEEP / PASS for the corrected pre-assembly package.** Accept PR #1361 at 9ff96bd97b0d018d8a5825858a0d2ebc382fcce9 and the fresh independent J3818 review in PR #1359 at b597831b6825d37f3202bd334ad0f097e35bcdfe. This replaces the pre-correction unconditional KEEP and resolves J3829's FIX. It is not a completed-film PASS, UAT approval, or publishing permission.

Evidence checked directly in this run:

- Trusted-owner PRs target main. Reviewed all 14 changed files, including the thumbnail builder, corrected cut/pool/provenance, shot list, panel decision and fresh review. PR #1359 contains #1361; merge the descendant without restoring the superseded #1358 branch.
- Recomputed NAS hashes of PIA00215, all four thumbnail/sheet JPEGs and locked VO: all match J3835/EVIDENCE.json. Recomputed all 25 existing per-row graphic hashes: all match CODE_GRAPHICS_J3022_v01.json. All 12 correction-record hashes match the exact #1361 commit (the fresh review deliberately replaces its old review-file hash).
- R11 is real Magellan overhead SAR PIA00215, 2782x2666, SHA-256 46dc965a02d4bff533685892ad16a76845a384d482ffaedda024c870b5b8a7b4. Directly inspected the source and both specified 1920x1080 crops: no black borders/data gaps, no invented perspective; scale 0.873x to 0.941x. NASA's official page identifies PIA00215, Magellan radar and NASA/JPL: https://science.nasa.gov/photojournal/venus-alpha-regio/ . The cut comparison changes only entry 13 of 86; 118.05–124.40 s and the following graphic timing remain intact.
- PIA18033 attribution is corrected to NASA/NOAA Suomi NPP Blue Marble 2012. Official identity checked: https://science.nasa.gov/image-detail/amf-pia18033/ . Preserve the full NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring credit. This is a satellite-photo composite, not an Apollo 17 exposure.
- Exact thumbnail preview sheet inspected; all three hooks read clearly, B's minus sign is distinct, text clears subjects, no Orbit, and duration space is usable. Re-ran thumb_preview.score: A PASS saturation 172.3 / near-black 18.1%; B PASS 161.5 / 19.5%; C PASS 180.6 / 18.1%. Editorial lineup/insets are not scientific scale diagrams. J3818 also records full-size inspection.
- Ledger comparison against merge-base changes only T045; three exact JPEG hashes populated, status proposed, video null. Unrelated newer main ledger rows must survive integration.
- SHOT_LIST_v02 has ten contiguous <=4 s opening beats through 32.85 s, real Mercury imagery between the split graphics, R09 uses real Venus imagery, R11 requires PIA00215, first chapter card 81.90 s. The locked VO hash remains 4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa.
- JSON/Python parsing and git diff --check passed. Privacy tests: 13 tests, OK. Default Python lacked Pillow; scoring/crop checks used the existing thumbs virtual environment successfully.

## Required J3023 assembly work

J3022's preparation and independent packaging-review deliverables are accepted once the corrected records land. Its existing graphics are verified preparation assets; they do not approve an assembled cut. Reconcile J3818 and J3022 as complete only after integration read-back. Keep J3023.after = J3022 and carry all of the following into its brief:

1. Create new v02 executable cut/pool/provenance inputs matching SHOT_LIST_v02, including all ten opening beats and R09 PIA23791 right globe plus pvo_uv_790205. Remove PIA00271 from active inputs. Never run the historical build_j3022_plan_and_pool.py generator or render directly from v01 cut inputs.
2. Render the split Mercury sunlight/night graphics and the revised 01 / 08 MERCURY progress strip. Preserve PIA00215 R11 source/hash/crop/timing and corrected Suomi NPP attribution. Keep all historical versions and locked script/VO intact.
3. Treat shot-table rows as narration blocks, not permission for long static holds: enforce actual picture changes, animation, reuse and upscale rules across the entire timeline. Inspect every flagged source/frame; no prior-film use or earlier machine PASS waives a failing asset.
4. Run picture_qa on final v02 inputs, polish_gate, music_gate on the actual laid score, sfx_kit level, clip_check with word timings and gate:episode. Resolve flags and record chapter teaching and polish reviews before UAT. The stored music_gate_v01 PASS has comparison-input warnings and does not replace this final check.
5. Use the panel's description/title pairing, verify final runtime and chapter timestamps, include exact source/image credits, honest making-of disclosure, social copy/trailer, and independent completed-cut/package review. Ben's final watch provides actual motion/audio review; this session claims neither hearing nor moving-video perception.

Ben watch remains 11 Dec 2026 18:00 London; planned air remains 16 Dec 2026 18:00 London. T045 stays proposed/video null. No upload, schedule, test arming, paid generation or spend authorized.

Disk maintenance: prescribed nas_offload --apply completed with no eligible old scratch; no files moved. Build scratch remains on MiniWork (139 GiB available at check).

## Integration read-back

PR #1359 merged as 9b3ca6cb52150da77af2c38a575e3be39e74a8b0; #1361 is also MERGED by ancestry. #1358 is CLOSED unmerged. Corrected shot/cut/pool files on main match #1361 exactly; the fresh post-J3835 review is present. Unrelated T044 main changes survived. Both delivered music stems match the v05 plan hashes. Completion reconciliation changes only J3022, J3818 and the J3023 handoff; no extra task was claimed. J3023.after remains J3022.

Publication handoff: automatic approval review rejected the branch-push command before execution, treating the remote as unverified and directing publication through Claude Code. The completed local branch is codex/J3883-integration in /Volumes/MiniWork/scratch/J3883-integration. Claude Code must review its entire diff for privacy, publish and merge when checks pass, then close J3883. Until that merge, J3022/J3818 remain blocked on main and assembly remains held; the original package PR merge is already complete.
