# J1208 preflight — 4 November 2026

Codex video worker and elected acting Chief. **STOP before spending.**
No source, cut, KEEP, generation launcher or publishing approval is delivered.

## Demonstrated reads

- Live `ai_spend_daily.read_vertex()` via existing signed-in billing browser:
  monthly Google Developer Program `CREDIT_TYPE_MONTHLY`, **GBP69.48 Available**.
  Free Trial GBP0 Used; other Used/Expired rows excluded. This is monthly promo,
  not Free Trial. Private reading: `~/_desk/handoff/J1208/balance-read.json`.
- Credential-safe ADC GET for the specified project's billingInfo: **HTTP 403**.
  No billing linkage proven by this probe. gcloud separately has no active
  account; no sign-in or account configuration was changed.
- Credential-safe ADC GET for the exact served project/model/region resource:
  **HTTP 404**. This proves neither that generation is served nor that it is
  unavailable; do not use a billable request as a probe.
- [Current official pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
  lists Veo 3.1 Fast video-only 1080p at USD0.10 per count in its table.
  The page directs non-USD customers to local Cloud Platform SKUs. **No exact
  current regional GBP/second SKU was verified.** Historical GBP0.075/s is
  rejected as a budget input. No GBP estimate is represented as verified here.
- The existing ledger has historical unpriced Omni takes at zero, including
  late-billed entries. A new balance reading is not proof that those costs
  have all posted. No authoritative cross-project pending-spend cutoff or
  bounded outstanding-cost total was established.
- Session tools demonstrate still-image and text access only. Neither audio
  nor native moving-video review is claimed. A later source review still needs
  demonstrated native-video input; finished cuts separately need audio input.

## Exact proposed source recipe, subject to source review

For **each** S5 and S6 take: native silent 1080x1920, 8 seconds, speed 1.
Use source **1.15–3.85s** for the 2.70-second opening; use **0.00–1.15s** as
the forward loop preroll. Thus the end runs into frame 0's source timestamp
without reversal, repeated frames, stretching or manufactured camera motion.
8s covers the required 3.85s; the source must visibly support the subject
through both intervals. This is an edit plan, not evidence the image exists.
Full-frame native 9:16 would scale 1x, with no crop needed. Actual dimensions,
hashes, frame continuity, phone review and gates can only follow generation.
The remaining 4.15s is unused headroom, not permission for extra takes.

S5: continuous realistic meteor crossing a night sky over unobtrusive terrain,
visible in the preroll and already moving at opening source t=1.15. No named
event, exploding star, diagram, impact, Orbit, labels or invented observation.
S6: low-relief Titan terrain under muted orange haze with physically plausible
visible atmospheric movement; no mountains, blue sky, underwater picture,
rings, radar reconstruction or measured landing-site claim. Haze illustrates
appearance only; it does not measure or prove the locked pressure number.
Both are generated explanatory illustrations and require later package
disclosure, never NASA observational credit. No corner credit on Shorts.

## Guard implementation boundary

`promo_guard.py` is a **no-network prototype**, isolated to this job. It has no
generation entry point and changes no shared core or existing spend CLI.
It requires fresh matching credit/link/service/price/usage evidence, a current
GBP rate plus >=10% margin, full-scope estimate <=GBP4, and >=GBP1 left after
pending costs and remaining scope. Duplicate takes and zero/unpriced pending
spend fail closed. Reservations and exactly-once reconciliation use the
existing ledger; ordinary completed spends retain its existing schema.

Do not wire this helper to a billable client yet. Its live evidence collector,
trusted billing reconciliation, desk-lock ownership/crash handling and
submission journal must receive Chief code review before any generation.
No reservation was written to the live ledger. Tests use temporary fixtures.

## Remaining action in this same job

Finish independent guard review and fix any findings; prove exact project /
billing-account linkage, entitlement terms and served model/region through
non-billable reads; obtain the current GBP SKU and all-project pending-cost
bound, then implement/review the live guarded caller with atomic submission
tracking. Re-read immediately before each take under the Vertex desk lock.
If any condition remains unverified, spend nothing. Never restart the
exhausted archive search or bypass this guard with the old mint script.

J1199 and the existing scheduled-copy fallback remain unchanged. The final
source/correction checkpoint is 5 November 12:00Z. No YouTube, Buffer,
UPLOADS, description, privacy, schedule or Ben-watch state changed.

Disk: required `nas_offload.py --apply` found no eligible old scratch; about
14.5GB remains free. No NAS deletion or forced offload was attempted.
