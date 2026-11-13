# J2711 — missing social hashtags, 12 November 2026

Codex covering as elected acting Chief. £0.

## Findings and fixes

- Read every upload in both channels' authenticated uploads playlists, deduplicated video IDs, and fetched live snippets/statuses: **117 public or scheduled Orbit videos; 42 HOS**. One Orbit video had no tags (`dH_yCRmzkMo`); none on HOS did.
- Matched 48 Orbit and 12 HOS videos to an explicit package tag array or its tag file. Older records without an unambiguous package are marked null in TAG_AUDIT.json, rather than inventing a match. This is a limitation: the complete historical package comparison remains unfinished.
- Five Orbit videos had exactly the first 15 package tags: `Js6EQJ8qDi8`, `rVqgtkBV3jc`, `VBaYRPp85Sw`, `m09jUdwC5hk`, `h8HGfyShEHI`. The shared uploader's `safeTags` explicitly sliced at 15. Removed this silent truncation and added a request-level regression test; synchronized the shared uploader, test and core lock into HOS.
- Restored the exact package tags for the empty video and those five truncated listings. Read back each and compare all writable snippet fields and the complete status against the pre-change record. Exact immediate repair results are in REPAIRS.json. A later check against the initial inventory found Mars long defaultAudioLanguage had changed from absent to en-US; its title, description, category, defaultLanguage and status still match. The repair payload did not introduce a new audio-language value. The origin of this derived or concurrent language change is unproven; it was not blindly reset. FINAL_VERIFICATION.json records this qualification.
- `ffYKoNVPoqg` has all three package tags plus five more specific live tags. Preserve these intentional additions.
- The Mars wind Short `uhZSRcvngvE` currently has all six package tags. Buffer confirms **all three sent posts (Instagram/Facebook/Threads) have no hashtags**. Do not edit, delete or repost them.
- During the empty-tag repair, the immediate API read still omitted tags, while a subsequent read showed the new set. This demonstrates stale read-back; it supports, but does not prove, an upload-time read delay as the Mars trigger. Current reusable title/description writers preserve tags. No evidence identifies a snippet-update call that deleted all Mars tags, so do not attribute it to one.
- The mirror previously accepted an empty live tag list and built successful hashtag-free posts. It now uses the exact registered Orbit package only when live tags are absent; if there are still no usable tags, it refuses new posts before hosting/creation. HOS continues using its own live metadata and receives the same creation guard; never resolve HOS package paths against Orbit.
- All **24 existing future Buffer posts** read back with hashtags (12 Orbit, 12 HOS). Pluto Instagram has three because its package has only three tags; all other five-tag networks checked have five. No future captions needed editing.
- The Mars six-tag regression verifies caption endings: Instagram 5, Facebook 3, Threads 1, TikTok 5. No posts are created by these tests.

## Latest ten Orbit Facebook posts

Buffer reach, read 12 November; metrics last updated about 14:07Z. Ages differ, especially today's Mars post, so these are descriptive totals rather than a controlled link test. Every post retains its existing YouTube link.

| Video | Kind | Reach | Sent |
|---|---|---:|---|
| uhZSRcvngvE | short | 18 | 2026-11-12 |
| B1z2dv7m7Vk | short | 172 | 2026-11-11 |
| ffYKoNVPoqg | short | 218 | 2026-11-10 |
| iyvWYFP_ETA | short | 1277 | 2026-11-09 |
| Js6EQJ8qDi8 | long | 331 | 2026-11-08 |
| T9fVlG3CCzU | short | 569 | 2026-11-07 |
| ZpEA8stoSPA | short | 306 | 2026-11-03 |
| hZH0C7fpCk4 | short | 1044 | 2026-11-02 |
| rVqgtkBV3jc | long | 265 | 2026-11-01 |
| VfDm3E2bUgU | short | 4070 | 2026-10-31 |

- short: 8 posts; total reach 7674, mean 959.2.
- long: 2 posts; total reach 596, mean 298.0.

A link-free test would need a separately scoped comparison; these observations alone do not establish that links reduce reach. No link policy change in this job.

## Validation and remaining work

Six relevant Vitest files: 99 tests pass. TypeScript check passes. Studio core hash check and email/private-network ratchets pass. Code goes through pull requests. Historical package mapping and the exact original Mars trigger remain unresolved; no unsupported causal claim is made.

## Follow-up run, 20:29 UTC

A fresh authenticated read of the same 117 Orbit and 42 HOS IDs finds **zero empty tag lists on either channel**. The six earlier repairs remain in place; this run made no YouTube or Buffer changes.

`HISTORICAL_COMPARISON.json` now compares every inventoried ID with all safely identified original packages and release indexes: **51 Orbit and 22 HOS baselines** (73 total). This adds seven package baselines and six release records to the earlier 60 package matches. Exact missing/extra tag sets are listed per ID. All those baselines' tags remain present except the two HOS longs described below. Extra live tags are preserved.

- HOS Germs `_C92tIJCk8A` and Periodic Table `AL_-qlWko_g` have shorter live sets than their old packages. The local `07_Content-Ops/tmp_ben_1447_retag.json` and its result identify a later Ben-ordered retag. Their current live sets contain that later requested set, with an additional subject tag on Germs. Reverting to the old package would undo that deliberate change. Preserve the live tags.
- `HISTORICAL_RECORDS.json` separately records older listing recommendations and API snapshots. They are evidence of changes, not proof that a proposed listing was applied. They are not used to overwrite live tags.
- Read-only inspection also checked package/upload/release JSON under the two channels' NAS archive project roots. Eleven candidate records were found; no additional unambiguous tag baseline was established beyond the current checkout records. The NAS was not modified.
- **86 original tag baselines remain unavailable or unproven**: 66 Orbit and 20 HOS. These are explicit per-ID limitations, not missing live tags. Further recovery would require a separate bounded search of deleted historical git paths or older upload artifacts; do not repeat the six repairs or restore old proposed listings.

The snippet-writing inspection also covered HOS's retag, language-repair and one-off description/title scripts. The inspected non-tag edits send existing tags back; explicit retag calls send their requested tags. No inspected writer proves the Mars Short's original empty read. Its upload result records six package tags and successful creation of all three Buffer posts, but does not retain the live snippet used to build those captions. The exact trigger therefore remains unknown; accepting an empty tag list was the demonstrated prevention fault and is already fixed.

**Stopping point:** operational prevention is merged and the live empty-tag fault is resolved. J2711 remains incomplete only for the requested exhaustive historical package comparison and exact original Mars-trigger attribution. Further artifact recovery is longer than a short unattended handover; release with these exact gaps rather than assert completion. No Ben action is needed.

## Follow-up run, 22:00–22:15 UTC

Resumed the original four-step plan at 3/4; earlier six repairs and intentional retags remain in force. Reviewed and merged evidence PR #865 after its CI passed. This run refreshed the inventory using uploads playlists **and** registered IDs: **120 Orbit and 42 HOS public/scheduled videos, zero empty tag lists**. Three scheduled Orbit records missing from the older playlist-only inventory are included. The current per-video comparison is `jobs/reviews/J2711/current_comparison.json`: **56 Orbit and 22 HOS baseline matches**, with **84 explicitly unavailable original baselines**.

Recovered two older long tag files through explicit parent-video IDs in their Shorts upload indexes. Exoplanets retains all its old tags. Fermi Paradox has extra newer tags and two old tags absent; preserve this historical variation rather than undo later listings. A bounded all-ref deleted-path search found no deleted Orbit package/tag artifacts. HOS's 13 deleted tag files were old Orbit scaffold (Aliens, Black Hole and Exoplanets), not HOS originals; do not assign these across channels. Evidence is in `deleted_git_artifacts.json` and `recovered_long_baselines.json`.

**One additional confirmed truncation repaired:** the newly inventoried nearest-star long `c5AdqQsnnys` carried exactly the first 15 of its 19 package tags. Restored the exact 19-tag set with an ETag conditional update. An independent batched read verifies all 19, with title, description, category, languages and complete status unchanged. Earlier single-ID reads remained stale even while the update response and later batched read carried 19. The full payload and readbacks are in `nearest_star_repair.json`. No privacy or schedule change.

**Three scheduled Voyager captions repaired:** Buffer's full organisation query found the 18 November posts for `dH_yCRmzkMo` absent from the local ledger and without hashtags. Matched their exact unique social hook, channel IDs and video source to that registered Short. Appended only the reviewed hashtag tail: Instagram 5, Facebook 3, Threads 1. Preserved the 18 November 11:30Z schedule, video URL, cover offset, Reel metadata and caption body. Saved the existing post IDs in `BUFFER_POSTS.json` so the daily mirror can recognise them. All **27** scheduled posts now have hashtags: 15 Orbit and 12 HOS. Pluto still has only its three available tags; no invented tags.

Buffer requires existing Reel metadata and video assets on Facebook edits; text-only attempts were rejected without changing that post. Supplying Facebook's existing URL through its annotation input coerced it to a mention. Cleared that override and verified Buffer reparsed the same text as a URL; the final body, video and schedule are unchanged apart from the hashtag addition. Exact final evidence: `facebook_final_annotation.json`, `all_scheduled_after.json`. Published posts were never edited, deleted or reposted.

The latest ten **all** Orbit Facebook posts include automatic blank-text cross-post records and a post not in the local mirror ledger. Reach, newest first: **2, 18, 5, 6, 172, 4, 218, 3, 1277, 4**. Four map directly to known Shorts (reach total 1685, mean 421.25); six are not safely classified from the mirror ledger (total 24); no long is directly mapped in this ten. These differ from the earlier ten *mirror* posts above. Retained the unknown classifications in `facebook_latest_ten_current.json`; no link-effect inference or policy change.

**Validation:** TypeScript check passes. 49 relevant uploader/Buffer tests pass, plus two recovery guard tests (never edit sent/sending/changed/near-due posts; repair only an exact first-15 truncation). Offline previews show 5/3/1 endings for the Voyager posts; the prior Mars regression covers TikTok's 5. Live organisation queries verify the scheduled caption endings. £0 spent. Required scratch offload ran under the existing rules and found no eligible old scratch.

**Remaining:** 84 original package baselines have no identified artifact, and no retained upload-time Mars snippet proves the precise original trigger. Do not repeat the seven completed tag repairs, the three caption edits or revert deliberate retags. Those evidence gaps remain explicit; this is not a claim that an exhaustive original-package comparison is complete. The demonstrated prevention fault (accepting empty input tags) and uploader truncation were already fixed in #857/#571. No Ben action is needed.

## Follow-up run, 23:49–23:51 UTC

Read the previous run history before further platform work and retained the existing four-step plan at 3/4. No YouTube or Buffer changes were repeated. A new bounded recovery searched **all-ref historical upload-index revisions**, rather than repeating the live inventory or deleted-tag-file searches: **40 Orbit and 37 HOS index versions** were readable.

Recovered one additional explicit video-ID/tag baseline, Orbit `n2WbOfJhOwc` (Star Recycling Isn't Perfect), from commit `22a3bc5bab5973efb8869d22c0f8210808b78977`. Its fresh authenticated read at 23:50Z contains every one of the historical index's 24 tags, plus `leftover mass`. Preserve the additional live tag; no repair is indicated. Evidence: `historical_index_recovery.json`, `historical_index_readback.json` and the updated `current_comparison.json` under `jobs/reviews/J2711/`.

Coverage is now **79 of the 162 videos inventoried at 22:02Z**: 57 Orbit and 22 HOS. **83 original baselines remain unavailable** (63 Orbit, 20 HOS); the recovery file lists their exact IDs. This is not a new complete live-channel sweep. The precise Mars creation-time input remains unavailable because that upload result did not retain the live snippet used for the Buffer captions. Do not infer causation from the current snippet.

The operational fixes remain merged in OWB #857/#870 and HOS #571: seven confirmed tag repairs, three future caption repairs, uploader truncation prevention, exact registered-package fallback and refusal to create hashtag-free posts. The earlier published Mars posts remain untouched. The next useful recovery needs an **original upload artifact with a video ID and tags for one of those 83 IDs, or the actual Mars creation-time snippet/log**. Repeating the same inventories cannot reconstruct either. J2711 remains unfinished only for those requested historical evidence gaps, with no Ben action or payment needed. Scratch offload was requested under the existing under-20-GB policy; it reported an already-running offload, so no second copy was started.


## Worker follow-up, 13 November 2026, 01:09–01:12 UTC

Codex covering as a specialist worker; Claude is Chief. Preserved the resumed four-step plan at 3/4. No platform listing or social-post changes in this run.

A bounded search of all-ref historical **upload-result revisions and their same-revision package manifests** read 139 Orbit and 80 HOS result versions. It recovered five previously unavailable original package baselines:

| Channel | Video | Package tags | Fresh live comparison |
|---|---|---:|---|
| Orbit | `1NeQFVnzO2Q` | 6 | Exact set match |
| Orbit | `Cka7_TVVOUQ` | 6 | Exact set match |
| HOS | `Bks_JLId1ew` | 6 | Exact set match |
| HOS | `ChbsigHD5_o` | 6 | Exact set match |
| HOS | `LCZRHUyTiq0` | 6 | Exact set match |

Each match has an explicit upload-result video ID, a manifest from that exact git revision, and an authenticated fresh snippet/status read. No title-based inference, guessed tags or repairs. Evidence: `historical_upload_result_recovery.json` and `historical_upload_result_readback.json` under `jobs/reviews/J2711/`. The recovery script is read-only against git and writes only its evidence file.

Coverage of the existing 162-video inventory is now **84 baselines: 59 Orbit and 25 HOS**. **78 originals remain unidentified: 61 Orbit and 17 HOS.** This was a targeted five-video live read, not another complete live-channel sweep. Updated `current_comparison.json` preserves all prior decisions and intentional retags.

The historical Mars result has package, upload and Buffer outcome fields, but does not retain the snippet used for caption creation. A bounded inspection of local worker log files under 20 MB found seven files mentioning the video; all were later gate/review artifacts without a tags field. Neither search supplies the original creation-time input, so the exact trigger remains unproven. No private log contents were copied into this public report.

The operational prevention and seven listing/three future-caption repairs from earlier runs remain complete; published posts stay untouched. Chief review remains required for this evidence PR. Exhaustive historical comparison remains incomplete; further work needs original artifacts for one of the 78 listed IDs or the actual Mars creation-time snippet. Do not repeat the repaired listings/captions. No Ben action or spend.

Disk maintenance: the required detached scratch offload completed with exit 0; no eligible old scratch existed. Thread read to #6840721900.
