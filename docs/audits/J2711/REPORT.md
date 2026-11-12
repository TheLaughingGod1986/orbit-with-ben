# J2711 — missing social hashtags, 12 November 2026

Codex covering as elected acting Chief. £0.

## Findings and fixes

- Read every upload in both channels' authenticated uploads playlists, deduplicated video IDs, and fetched live snippets/statuses: **117 public or scheduled Orbit videos; 42 HOS**. One Orbit video had no tags (`dH_yCRmzkMo`); none on HOS did.
- Matched 48 Orbit and 12 HOS videos to an explicit package tag array or its tag file. Older records without an unambiguous package are marked null in TAG_AUDIT.json, rather than inventing a match. This is a limitation: the complete historical package comparison remains unfinished.
- Five Orbit videos had exactly the first 15 package tags: `Js6EQJ8qDi8`, `rVqgtkBV3jc`, `VBaYRPp85Sw`, `m09jUdwC5hk`, `h8HGfyShEHI`. The shared uploader's `safeTags` explicitly sliced at 15. Removed this silent truncation and added a request-level regression test; synchronized the shared uploader, test and core lock into HOS.
- Restored the exact package tags for the empty video and those five truncated listings. Read back each and compare all writable snippet fields and the complete status against the pre-change record. Exact results are in REPAIRS.json.
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
