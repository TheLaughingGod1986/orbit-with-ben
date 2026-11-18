# J2985 credits repair — J3024, Codex, 18 Nov 2026

PR #987 remains a repair for review. No merge, deployment, subscription change, purchase or generation spend in this job.

## Corrected behavior

- Weekly exhaustion means 100% used or explicit provider weekly exhaustion evidence. 94% is near limit, not exhausted.
- Weekly readings resolve provider reset text against each reading timestamp, with London timezone/DST, UTC clocks and absolute years. Recurring Wednesday text on 3, 6, 10, 13 and 17 November now yields three windows ending 4, 11 and 18 November. Windows crossing a billing-cycle start retain overlap. Sparse observations remain explicitly partial; unknown reset/quota identity is retained as uncertainty.
- Both page implementations keep cycle summaries separate from the full historical downgrade guard. Comparable earlier high usage vetoes a cheaper plan even when current-cycle usage is low. Changed/unknown quotas, partial coverage and unverified tier ratios withhold downgrade advice. Percentages are normalized against the current tier allowance.
- After the reading's weekly reset passes, it is historical and awaiting refreshed reading even before 30 hours. Current time pace, burn projection and verdict are suppressed; no refill is invented.
- Unknown billing renewal uses labelled rolling history, never an invented monthly billing cycle.

## Provider provenance and corrections

Sanitized read-only observations, timestamps and final provider pages are in [BILLING_PROVENANCE_J3024.json](BILLING_PROVENANCE_J3024.json). Only allowlisted plan labels, renewal text and credit fields were retained; account details and full provider pages were not logged.

| Reader | Result on 18 Nov UTC | Consequence |
|---|---|---|
| Google One plans | Google AI Ultra and £189.99/month; no verified account renewal | Price corroborated; renewal unverified |
| Claude billing URL | Redirected to claude.ai/new; Ultra label alone does not establish billing tier or ratios | Restore Ben's recorded £180 / Max 20x choice; renewal and quota ratios unverified |
| Cursor spending | Redirected to grok.com/dashboard/billing; Ultra and “Renews 24 Nov 2026” | Observed page renewal only; does not establish subscription identity or prove absence of another subscription |
| ChatGPT account | Reached chatgpt.com/auth/login | Renewal unread; actual login required to inspect billing; rolling history remains usable without it |
| ElevenLabs subscription API | HTTP 200, creator; 121114 allowance, 53221 used, credit reset timestamp | Confirms credit fields; credit reset alone is not billing renewal evidence |

The previous report's claim “There is no separate £20 Grok subscription” is withdrawn. A shared usage meter is separate from subscription identity. Ben's actual 9 November statement that he changed Grok Bot to £20 is preserved as his decision, not reinterpreted as a planned downgrade from a supposedly shared £180 plan. The target budget remains Ben's recorded target; it is not a verified invoice total. Newly introduced tier ratios are marked unverified and cannot support downgrade advice. Unverified billing bounds are excluded from both page calculations.

The previous screenshots were board renders, not provider billing evidence. They do not verify subscription claims. No present billing identity or ratio claim is based on those images.

## Validation

- 104 Python tests PASS: test_ai_spend, test_ai_spend_daily, test_board_site, test_kanban_snapshot.
- Both JavaScript suites PASS, including matching regressions on both page paths for the prior-history veto, changed/unknown quotas, near-limit wording, and the expired Nov 17 23:22 Codex window at Nov 18 01:00.
- Python regression cases cover recurring weekly text, near-limit versus exhaustion, explicit provider exhaustion, billing overlap, year rollover, London DST and partial uncertainty. Calculation tests use controlled plan evidence rather than live subscription metadata.
- Board static build, core_sync check, sync_rules --check and git diff --check PASS.
- 390×844 at 2× screenshots regenerated from updated credits plus the board-data snapshot. Browser overflow check is false. Viewed phone cards for readability and expired-reading wording. Files remain outside git at /Users/benjaminoats/_desk/reviews/J3024/: agents_phone.png, agents_credits_full.png, ai_phone.png, ai_credits_full.png. Full Agents credits capture expands the scroll shell for an unclipped evidence image; the viewport capture uses the actual app shell.

## Handoff

Chief re-review of J2985/PR #987 is next. The original J2985 hold is preserved. Merge, publish and live-phone verification remain pending. Billing uncertainty is represented in the product and does not require Ben to do anything unless he chooses to supply his actual ChatGPT login for a future billing read.


## Follow-up to Chief review 6968024257 (18 Nov, J3024)

Both browser reset parsers now retain explicit years and UTC/GMT/Z clocks. Matching regressions cover the 18 Nov 2026 10:00Z reading before and after reset, UTC/GMT in British Summer Time, London-local clocks, explicit past years and year rollover. Explicit past resets remain past; no refill is inferred.

Allowance evidence is independent of billing identity. A verified allowance window with both start and end supplies Time without supplying billing bounds or enabling downgrade advice. A verified end alone displays the reset date and an explicit start-unread / Time-unavailable state. The existing sanitized ElevenLabs API reset timestamp is now retained as allowance evidence; its start/duration remain unread. Flow and Vertex have no verified allowance window in the available evidence and visibly say Time unavailable instead of silently losing the second row. No billing date has been promoted to allowance evidence. Ben's recorded keep-Ultra-one-more-month / then-review decision is visible independently of calculated verdicts on both pages, including when advice is withheld.

Validation for this follow-up: 104 relevant Python tests PASS; both JS suites PASS with matching parsing and actual unverified-billing metadata fixtures, verified allowance boundaries and end-only evidence. Static board build, core sync, rules sync and diff checks PASS. Fresh 390px screenshots were generated from the rebuilt app and current local credit document in the existing J3024 evidence folder. Both full credit captures were visually inspected: Time rows, end-only ElevenLabs reset, historical Codex wording and the Ultra decision are visible. Browser horizontal overflow is false. These are local board renders, not provider captures or live deployment evidence.

Updated PR #987 returns for Chief re-review. J2985 remains held after J3024. No merge, deployment, new provider read, subscription change or spend occurred in this follow-up.
