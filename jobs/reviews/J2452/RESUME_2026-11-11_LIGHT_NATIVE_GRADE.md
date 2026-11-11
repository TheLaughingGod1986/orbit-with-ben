# J2452 — native grade evidence; incomplete full render

Worker macbook. Progress remains 10/15. PR #789, branch macbook/J2452. No NAS chapter added or UAT claimed.

Five full-resolution saved-pixel probes with spatial rounding and lossless encoding measure 84.969–84.995% brightness, within the unchanged 83–87% limit. Native measurement shows the old downsample rounds very dark values before averaging, changing some ratios; the original grade also has real rounding bias (68s, 406s, 442s still fail natively). JSON evidence is in public_light_dark_v02. No failed grade is reclassified as inherited.

The helper now streams native decoded 1920×1080 legal-range Y at 4 fps, subtracts black 16, clips at zero and averages without an intermediate resize. It fully decodes for frame count, still compares every complete two-second window, and retains the original duration, source hash, gate and loudness prerequisites. Lossless spatial rounding removes the uniform brightness bias in the five short probes. Full-chapter verification is NOT proven.

The first full lossless render was killed by the inherited 420-second helper timeout. A new eight-filter-thread ultrafast lossless render was stopped gracefully at the wake boundary: 11,958 frames / 398.600 seconds, short of 13,900 / 463.333 seconds. Both remain local, incomplete, never delivered. All launched processes exited. No NAS writes, upload, Studio change, generation, login or spend.

Next: keep the verified undarkened public_light_v06 output. Benchmark a faster ordered/diffusion conversion against native measurements on the five problem windows (prior probes were measured only after 8-bit resizing), or use bounded identical-setting segments so every wake ends cleanly. Do not restart a whole slow geq encode unchanged. Write a new version; verify full frame count/duration, all two-second native brightness ratios, and five brightest windows. Only then run save_public_light.py and record chapter eleven after NAS SHA-256 read-back. The helper currently targets incomplete dark_v03: change that output directory/version first. No verify-existing bypass can deliver the partial file: frame count must fail.

Proxima Centauri, Andromeda, final continuous bed/mix, CTA/silence/join checks, master/reel and Ben watch card remain. Source charts/labels remain under the Chief scope; the 21 full-pixel findings are recorded as inherited outside compilation edits, not waived. Source edit QA is PASS. Existing source cover-edge and edit sheets inspected as stills this wake, without playback/listening claim.

Validation: 13 privacy tests pass, helper compilation and diff checks pass. Thread read to #6804671657 at session start. OWB is returned to main after pushing; HOS untouched.
