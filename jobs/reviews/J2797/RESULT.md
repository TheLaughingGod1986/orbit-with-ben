# Board custom address

The board is now available at https://board.oppti.dev. The original Pages address remains available.
Cloudflare reports the custom domain, verification and certificate validation active.
Only one proxied CNAME was added, pointing at studio-kanban.pages.dev. All 18 original DNS records
were compared by record ID and complete JSON before and after; all were unchanged.

Verified HTTPS 200 for /, /tracker, /ai, /version.json and /api/data?f=ref, plus the original
Pages home page. The home page carries X-Robots-Tag: noindex, nofollow. Product / and /pricing
still return 200. A fresh signed Play request returned 302 to R2; its target returned
206 video/mp4 for a 1 KiB range with an MP4 ftyp header. This verifies media delivery, not a motion review.
Public DNS (Cloudflare resolver) resolves the new name; the Mini temporarily retained its earlier negative
DNS answer, so initial HTTPS checks used that public answer explicitly with TLS hostname verification.

## Pages Functions requests

Read on 14 November 2026 using Cloudflare GraphQL pagesFunctionsInvocationsAdaptiveGroups,
filtered to full UTC days from 12 November inclusive to 14 November exclusive, grouped by date,
scriptName and status. Only the studio-kanban production script appeared.

| UTC day | Requests | Share of 100,000/day | Reported errors | CPU-limit failures |
|---|---:|---:|---:|---:|
| 12 November | 114 | 0.114% | 0 | 0 |
| 13 November | 124 | 0.124% | 0 | 0 |

12 November had 103 success and 11 clientDisconnected requests; 13 November had 123 success
and 1 clientDisconnected request. No exceededCpu status appeared. The dataset exposes no route/path
dimension, so busiest routes are unavailable. Neither day approached 50,000 requests.
These are Pages Functions invocation counts, not static page views or all requests across the account.

## Phone setup

Once the separate tick-token setup in J2714 is complete, open https://board.oppti.dev in Safari.
Use a newly generated private “link this phone” link for this address, then Safari’s Share → Add to Home Screen.
An icon or linked-phone cookie for the old address does not transfer. No key or pairing code belongs on the thread.

The single studio/board_site.json setting supplies Python clients and the Node watch uploader.
The minute publisher and board check consume it through scripts/board_site.py. Existing address/header tests
and signed-watch tests pass (4 and 13 tests respectively). No billing, tick-store, R2, open-tap, YouTube or Buffer
settings were changed.

## Repeat-check limitation

A repeated /api/data?f=ref check after the initial 200 responses exposed the existing GitHub
access/rate-limit problem: the original Pages address returned a GitHub 403 JSON error, and the
new address also briefly returned a Cloudflare 502. A one-time 200 is therefore insufficient to
claim sustained data access. The tick-token/private-data follow-up remains separate (J2714/J2532).
Do not call the entire job complete until repeat data reads and the normal publisher/check pass.
