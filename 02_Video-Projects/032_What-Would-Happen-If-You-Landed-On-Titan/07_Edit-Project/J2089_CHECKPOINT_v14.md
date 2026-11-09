# J2089 checkpoint v14 — reviewed exports

6 November 2026 · Codex worker · original 1/4 retained · GBP0.

Rendered 15 J2177 KEEP mechanism items (excluding r10_spectrum/r32_scalemap),
J2247 r09_sizes with its MESSENGER rights reference, and J2264 r35_ocean.
Ocean implements reviewed qtrle export; its frame function is unchanged.
All 17 preview hashes match the individual review records.

REVIEWED_EXPORTS_VERIFICATION_v01.json records hashes, 1920x1080 qtrle ARGB,
30 fps, 108 frames and 3.6s per clip. All 1,836 decoded RGBA frames match their
generator byte for byte. Reproduce with verify_reviewed_exports.py --review-root
pointing to a checkout containing reviews J2177/J2247/J2264. Unapproved ocean
render correctly exits 2 before creating output. Existing 39 exports untouched.

Media: /Users/benjaminoats/_desk/cache/J2089/{mechanism,size,ocean}_renders_v01.
Detached J2089-reviewed-exports completed exit0; log and done marker:
/Users/benjaminoats/_desk/logs/J2089-reviewed-exports.{log,done}.
No background process remains running.

Next: fix r10_spectrum/r32_scalemap per J2177 and review before rendering; apply
J2177 allocations in shot/cut records; finish licensed harvest, real-body builds
and composites. J2177 names PIA17163+PIA21450 for R25 and PIA07870/PIA07871 for
R16/R51; application/harvest remains. J2264 allocates PIA14602 to R09+R35 only.
J2260/J2262, frame0 and APL rights holds remain. No perceived motion/audio,
composite contrast/placement, final reuse/gates or film-stage approval claimed.

Clean-start worktree /private/tmp/J2089-ocean-wt, worker/J2089-ocean. Inherited
public-push rejection respected: checkpoint stays local for Chief integration.
No push retry, merge, publishing, script/VO change or credit spend. NAS offload
deferred outside permitted window (8,857 MB free at start).
