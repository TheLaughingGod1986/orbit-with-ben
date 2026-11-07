# J2089 checkpoint v15 — R08 and R19 reviewed exports

6 November 2026 · Codex · original four-step plan stays at 1/4 · GBP0.

Rendered r08_orbit_period under J2262 with unchanged frame generator and source.
Rendered r19_distance under J2260 with its exact approved PIA14909 source/crop
and dynamic limb mask. Both new PNG hashes exactly match the respective review.
PIA14909 source hash matches J2260; PIA14922 matches J2262. No script/VO changes.

Each MOV is 1920x1080 qtrle ARGB, 30fps, 108 frames, 3.6 seconds, no audio.
All 216 decoded RGBA frames match the generators byte for byte. The two
*_EXPORT_VERIFICATION_v01.json records contain hashes and probe evidence.
*_RENDER_CHECKS_v01.json record 109 safe-area/alpha samples per item,
R19's exact 9.5 ratio, R08's monotonic period dial and rejection without approval.
The verifier supports --only orbit_period|distance to avoid repeating prior work.

Media: /Users/benjaminoats/_desk/cache/J2089/{orbit_period,distance}_renders_v01.
Preserved all 56 prior exports; total 58. No background process remains.
Reviewed source allocations remain: PIA14922 R06+R08 only; PIA14602 R09+R35
only; PIA14909 R19. Final shot/cut source-count reconciliation is still required.

Remaining work exceeds one unattended run: fix r10_spectrum/r32_scalemap under
J2177 and obtain still review before export; apply reviewed source allocations;
finish licensed harvest, R18/R23 builds and graded composites. Frame0 native
motion and JHUAPL Dragonfly permission remain unresolved. No film-stage PASS,
perceived motion/audio, final reuse, composite contrast, or final gates claimed.
J2260's closing list names different mechanism fixes than J2177: its body is
not used to override J2177's explicit r10_spectrum/r32_scalemap ruling.

Worktree /private/tmp/J2089-ocean-wt, worker/J2089-ocean. Clean at start.
Inherited public-push rejection respected: local checkpoint only, no push retry.
No merge, publishing or spend. NAS offload --apply correctly deferred to its
01:00–06:00 window (8,736 MB free; above daytime under-8GB exception).
