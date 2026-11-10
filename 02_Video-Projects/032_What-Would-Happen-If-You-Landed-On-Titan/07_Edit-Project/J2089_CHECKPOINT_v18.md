# J2089 checkpoint v18 — reserved Huygens mosaics checked

6 November 2026 · codex · GBP0 · original four-step plan remains 1/4.
Based on 8ff3ddc7d6, preserving all 60 existing exports.

Downloaded J2177's reserved PIA07870 (2400×2400) and PIA07871
(1563×1497) original NASA Images files. Their returned identities are
Huygens Titan Mosaic #1 and #2. Recorded credit:
NASA/JPL/ESA/University of Arizona. Image, NASA search response and asset-list
hashes are recorded in HUYGENS_RESERVED_POOL_v01.json and HARVEST_POOL_v01.json.
NASA hosting and credit alone do not establish per-asset rights clearance.
Media and source responses: ~/_desk/cache/J2089/huygens_reserved_v01/.

Inspected contact sheet, full-size PIA07871, and both best-measured crop stills.
Neither is assembly-ready: the mosaics have conspicuous seams and inconsistent
sharpness. PIA07871 also contains large missing black areas. No KEEP is given,
no failed gate is waived, and no clean native-motion descent clip is supplied.

verify_huygens_reserved.py reproduces all six source/hash checks and searches
every pixel origin for the smallest exact-integer-16:9 crop within 2.35× upscale
(832×468, 2.308×). It checks 3,032,877 origins for PIA07870 and 753,960 for
PIA07871. The minimum below-luma-32 fractions are 0.0136% and 11.6705%.
These are diagnostic measurements, not a polish gate or proof that no possible
alternative framing exists. An earlier exploratory luma<10 filter missed lifted
grey voids; the preview exposed this and that result is not a quality approval.
Even the low-dark-fraction PIA07870 crop visibly retains seams and soft detail.

Next worker: retain these candidates as examined, not approved plates. Do not
repeat the same downloads or unchanged crops. R16/R51 require a different,
bounded crop/source approach or an existing approved plate supporting the line,
recorded in the working shot list before assembly. Frame-0 native motion and
APL rights remain unresolved. R18/R23 graphics and graded composites remain.
The complete remaining scope exceeds one unattended run; parent stays 1/4.

Clean detached worktree /private/tmp/J2089-r23-wt. No background process,
new MOV, spend, publishing, script/VO change, film PASS, merge or push.
Inherited automatic-review public-push rejection respected; local integration
checkpoint only. Both required repo pulls succeeded; HOS inbox empty.
