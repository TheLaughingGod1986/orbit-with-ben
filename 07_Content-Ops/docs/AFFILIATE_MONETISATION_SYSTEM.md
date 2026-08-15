# Affiliate Monetisation System

Long-term monetisation platform for **Orbit With Ben**, integrated into Content Ops (`07_Content-Ops/`). Relevance before revenue — never recommend a product solely because it pays commission.

## Philosophy

Every recommendation must pass: *Would we still recommend this if there were no commission?*  
Editorial / scientific interest is primary. Max **4** affiliate links per video. No spam.

## Architecture

```
src/lib/affiliate/
  types.ts              Shared constants & DTOs
  schemas.ts            Zod validation
  matching.ts           Deterministic relevance + Creator topic→slot menu
  topic-product-map.ts  Topic → 4-slot recommendation menu (leave empty rules)
  creator-description-voice.ts  Official description templates + disclosure
  description.ts        Pure YouTube affiliate block builder (Creator voice)
  description-service.ts DB-backed templates + video placement merge
  urls.ts               Redirect base, UTM, programme tag injection
  tracking.ts           Click recording + destination resolve
  placements.ts         Video ↔ product placements / regenerate
  products.ts / programs.ts
  revenue.ts            Commission, EPC, affiliate RPM, Total Content RPM prep
  opportunity.ts        Affiliate Opportunity Score 0–100
  csv-import.ts         Amazon/Brilliant/generic report parsing
  conversions.ts        Preview + commit import (dedupe by content hash)
  health.ts             Throttled URL health-check abstraction
  analytics.ts          Dashboard, opportunities, video panel
  goals.ts              Goals ladder math (reporting only)
  goals-service.ts      Clock from first approved placement / click
  gear.ts               Phase 5 gear catalogue JSON shape
  social-copy-rules.ts  Hard constraints for affiliate-aware social copy
  social-copy.ts        Sanitize + one soft mention on platform captions
  social-context.ts     Resolve placement context for Shorts generation
  social-channels.ts    Live channel → AffiliateClick.source + UTM map
  social-snippets.ts    Deterministic Threads / IG / Facebook Page snippets
  social-snippet-templates.ts  Social Media Manager fixtures + renderers
  facebook-page-rules.ts  Facebook Page feed hard rejects
  social-snippet-service.ts  DB-backed snippet pack + draft enqueue
  editorial-trust-gate.ts  Video Auditor trust gate (approve + description)
```

UI lives under `/affiliate/*` and on each long-form video detail page. Redirects: `/go/[slug]`.

## Editorial trust gate (Video Auditor)

Matching may still surface **up to 4 candidates** on the video Affiliate Monetisation card so an editor can see options. **Auto-insert, description generation, and APPROVED placements** must pass this gate. Relevance and trust beat the old “max 4 links in the description” default.

**Hard rule:** would we still name this product if there were no commission? If no, it does not go in.

### Placement checklist (before a link hits a description)

1. Named on screen or in the VO of **this** video — not “related,” not “viewers also bought.”
2. A curious viewer is better off after using it (see the sky, read the paper, understand the picture).
3. **One** primary affiliate link per long-form film. A second only if it is a free/cheap companion (e.g. paper + book). Never a stack. Hard cap: **2**. Matching may still show **up to 4** card candidates (Creator topic menu) — empty a slot rather than force a product.
4. Disclosure once, as the **last line** of the affiliate block (Creator):  
   `Some of these links are affiliate links. We only share things we’d still point you to with no commission.`  
   Do not put the affiliate block in the first screen. Block sits **after** chapters + subscribe, **before** playlist / next film / hashtags.
5. Tone stays documentary (Creator templates). No “buy now / must-have / limited / support the channel by shopping.”
6. Must not compete with the real CTA (film title + subscribe). Affiliate sits **below** that. Never read affiliate links on camera; never in the first 90s of the film.
7. Shorts: **zero** description links — film CTA only.

### Video types

| Type | Affiliate policy |
|------|------------------|
| All Shorts / companion Shorts | **Zero** links |
| Wonder films (picture is the point) | Zero unless a specific book/paper is named on screen |
| Explainer (JWST, Fermi, black hole) | At most one book, paper, or sky app that was used or named |
| How-to / “look tonight” | One relevant tool max, only if shown |

### Reject spam patterns

More than 1 link on a Short (should be 0) or more than 2 on a film · product never in the video (VPN, hosting, protein) · high-commission junk (crypto, supplements, mystery boxes, generic space merch) · same link on every video · stacked disclosures · salesy VO/end card · link that outranks the film title.

### Code

```ts
import {
  evaluateEditorialTrustGate,
  filterDescriptionLinksThroughTrustGate,
} from "@/lib/affiliate/editorial-trust-gate";

// Approve / auto-insert
evaluateEditorialTrustGate(video, product); // must .pass

// Description generation
filterDescriptionLinksThroughTrustGate({ video, candidates });
```

`setPlacementStatus(..., "APPROVED")` and description builders call this gate. Card candidates may remain `PENDING` when they fail.

## Social copy house rules (hard constraints)

Affiliate must not turn Orbit into a spam channel. These rules apply wherever Content Ops **generates or stores** social copy next to affiliate placements (`generatePlatformCopy`, clip platform-copy / distribution-pack / export). This is **not** a new social product — only guardrails.

### Every platform

- Max **one** soft mention per post. If the video is not actually about the thing, say nothing.
- Never stack brands. Never open on a product. Never “links in bio” as the hook.
- No raw affiliate / merchant URLs, no “use my code”, no percent-off, no haul energy.
- Point to the **YouTube description** or an Orbit **`/go/`** link only. That is the only place a tracked URL lives on social.
- Disclose once, quietly, where the platform requires it. Do not make the disclosure the joke.
- Sky / science first. The tool is an afterthought.

### Platform notes

| Platform | Rule |
|----------|------|
| YouTube Shorts / TikTok | Mention only in the last 1–2s **or** caption tail; no spoken list of links; no URL on screen; no TikTok Shop. **Short description itself: zero affiliate links** (Auditor gate). |
| Instagram Reels | Keep the mention out of the reel; one caption line (or a reply if asked); sticker/bio → YouTube or `/go/`, never a merchant. Caption may say “I left the one thing under the film.” |
| Instagram Feed | Distinct from Reels. One soft caption mention; never merchant stickers. |
| Facebook Reels | Same soft-mention rules as other Reels — not the Page feed. |
| Facebook Page | Documentary **feed/page** post (distinct from `facebook_reels`). One optional `/go/` or YouTube link at the end. No Amazon stickers, no “shop now,” no boost/shop energy. |
| X / Threads | The post is the thought; one extra line or a reply — not a product thread; links only to `youtube.com` or `/go/` |

### Live Orbit social channels (Threads · Instagram · Facebook Page)

Affiliate-aware captions for the live channels Ben runs are generated inside Content Ops — **not** a separate social app. Copy patterns are encoded as fixtures/templates in `social-snippet-templates.ts` (Social Media Manager).

| Content Ops platform id | `utm_source` / `AffiliateClick.source` | Notes |
|-------------------------|----------------------------------------|--------|
| `threads` | `threads` | Thought first, one extra line, one link |
| `instagram_reels` | `instagram` | Soft mention in caption only; sticker/bio → YouTube or `/go/` |
| `instagram_feed` | `instagram` | Same caption pattern as Facebook Page |
| `facebook_page` | `facebook` | Distinct from `facebook_reels` — feed/page only |
| `facebook_reels` | `facebook` | Reels path; same click source bucket |
| YouTube description `/go/` | `youtube` | Default when utm_source omitted |

**UTM on social → `/go/` or YouTube links**

| Param | Value |
|-------|--------|
| `utm_source` | `threads` \| `instagram` \| `facebook` (or `youtube` from description) |
| `utm_medium` | `affiliate` when a product is soft-mentioned; `social` when the post only points at the film |
| `utm_campaign` | `{video-slug}` |
| `utm_content` | `{affiliate-product-slug}` when a product is mentioned |

Tracked URLs on social may **only** be the YouTube film URL or an Orbit `/go/{slug}` redirect — never `amazon.co.uk`, Brilliant checkout, or other merchant URLs. Never put `/go/{slug}` on line 1 of a Short/Reel/post.

#### Social Media Manager templates

**First live pack — JWST Thursday film** (`FIXTURE_JWST_LIVE`). Soft mention = explainer book (`beginner-astronomy-book` / Turn Left at Orion) under the film via YouTube description or `/go/beginner-astronomy-book`. **Never** attach a telescope product. LEGO stays out. Never raw Amazon URLs. Snippets ship with `approvedForPublish: false` — **do not auto-post**.

Threads (only after **Thu 20 Aug 2026 18:00 Europe/London**):

```
JWST keeps finding galaxies that should not be there yet.

Orbit walks through what the pictures actually show.

Film is up. I left the one explainer I used under it.
[JWST YouTube URL]
```

Instagram (same night):

```
JWST keeps finding galaxies that should not be there yet. Orbit walks through what the pictures actually show, and what they do not.

Full film on YouTube. I left the one explainer I used under it.
[JWST URL or sticker to that URL]
```

Facebook Page (Thursday night):

```
JWST keeps finding galaxies that should not be there yet.

Orbit walks through what the pictures actually show, and what they do not.

Film is up. If you want the one explainer I used, it is under the film.
[JWST URL]
```

**Telescope / observing caption — HELD** (`FIXTURE_TELESCOPE_OBSERVING_HELD`) until a real observing post (not Thursday JWST):

```
I spent a night on this patch of sky. This is what it looked like.

If you want that kind of view, I left the one I use under the film. I get a small cut if you grab it.

Watch the film first.
[film URL] or /go/beginner-telescope
```

**Never on these posts:** Amazon URL, Shop now, product preview cards, LEGO, more than one brand.

**Instagram Reels** — mention stays in the caption (or one reply). Link sticker / bio = `/go/{slug}` or YouTube. Never a merchant sticker.

**Comment reply** (“what telescope?”) — one honest reply, point to the film description or `/go/beginner-telescope`, disclose once, stop. Fixture: `FIXTURE_COMMENT_REPLY_TELESCOPE` / `renderTelescopeCommentReply()`.

#### Never on the Facebook Page (generator + tests reject)

- Raw Amazon / Brilliant / merchant URLs (preview becomes a shop card)
- Link stickers or buttons to Amazon, “Shop now”, store tabs, product tags
- Boosting as a conversion/shop ad or catalogue
- More than one brand in a post
- “Use my code”, percent-off, haul, unboxing-as-the-post
- Comment-spam “link in comments” with a merchant URL
- Pinning an affiliate comment
- Posting the same `/go/` link three days in a row with no new film

Code: `facebookPageCaptionViolations` / `assertFacebookPageCaptionSafe` in `facebook-page-rules.ts`.

**Approval:** snippets render with `approvedForPublish: false`. Editors copy from the video Affiliate Monetisation card or `GET /api/affiliate/social-snippets?videoId=…`, or enqueue PlatformPost **drafts** (`POST … action: enqueue-drafts`) after an approved description placement. Same publish/approval flow as other social posts — never auto-post affiliate mentions.

```ts
import { generateAffiliateSocialSnippets } from "@/lib/affiliate/social-snippets";
import {
  FIXTURE_JWST_LIVE,
  FIXTURE_TELESCOPE_OBSERVING_HELD,
  renderJwstLiveCaption,
  isJwstThreadsPublishAllowed,
} from "@/lib/affiliate/social-snippet-templates";
import { buildSocialGoUrl, buildSocialYouTubeUrl } from "@/lib/affiliate/urls";
import { socialPlatformToClickSource } from "@/lib/affiliate/social-channels";
```

Dashboard `/affiliate` shows **clicks & revenue by source** including `youtube`, `threads`, `instagram`, `facebook`.

### Skip soft mentions when

- the short has no natural object, or
- that platform already soft-mentioned something this week, or
- you cannot name a specific film (no YouTube URL / title).

### Code entry points

```ts
import { applyAffiliateSocialConstraints, assertAffiliateSafeSocialCopy } from "@/lib/affiliate/social-copy";
import { resolveAffiliateSocialContextForVideo } from "@/lib/affiliate/social-context";

// generatePlatformCopy({ …, affiliate }) applies constraints automatically
```

`assertAffiliateSafeSocialCopy` rejects captions that still contain merchant URLs or banned promo language before posts are written.

## Data model

| Model | Role |
|-------|------|
| `AffiliateProgram` | Amazon UK, Brilliant, Astronomy Retailer, LEGO, … |
| `AffiliateProduct` | Offers / kits / courses / category landings |
| `AffiliateTag` + `AffiliateProductTag` | Semantic matching tags |
| `AffiliatePlacement` | Video ↔ product link with type, score, approval |
| `AffiliateClick` | Redirect tracking (no fingerprinting / PII) |
| `AffiliateConversion` | Manual / CSV revenue attribution |
| `AffiliateUrlHealthCheck` | HEALTHY / REDIRECTED / BROKEN / UNKNOWN |
| `AffiliateDescriptionTemplate` | Editable YouTube snippet copy |
| `AffiliateImportBatch` | CSV import audit + duplicate hash |

`LongFormVideo` gains relations for placements, clicks, and conversions. Existing video metadata (`topic`, keywords, script, category) is reused for matching — not duplicated.

Migration: `20260815140000_affiliate_monetisation`

## Programme setup

1. Apply migration: `npx prisma migrate deploy`
2. Seed (dev): `npm run db:seed`
3. Set env IDs (never commit real values):

```bash
AMAZON_ASSOCIATE_TAG=orbitgo-21
BRILLIANT_AFFILIATE_ID=your-brilliant-id
AFFILIATE_REDIRECT_BASE_URL=https://orbitwithben.com/go   # optional; defaults to ${APP_BASE_URL}/go
```

**Never commit** `AMAZON_ASSOCIATE_TAG` (Ben’s live tag is `orbitgo-21` — set it only in the operator’s env / host secrets). `/go/{slug}` stamps `tag=` at redirect time from that env var.

Weekday / daily routines read clicks and conversions from this system (`AffiliateClick` / `AffiliateConversion` / `/affiliate` goals panel).

### Live Amazon UK destinations (additive)

Confirmed product pages live in `src/lib/affiliate/live-product-urls.ts`. Apply without resetting the DB:

```bash
npm run affiliate:apply-urls
# or: npm run affiliate:apply-urls -- --dry-run
```

| Slug | Destination |
|------|-------------|
| `beginner-astronomy-book` | Turn Left at Orion (ASIN `1108457568`) |
| `beginner-telescope` | Celestron Cometron FirstScope 76 (ASIN `B00DV6SBRO`) |
| `space-lego` | Inactive stub — LEGO programme stays **INACTIVE**; not for social/descriptions |

Unconfirmed Amazon products (`astronomy-binoculars`, `mars-book`) keep `example.invalid` TODOs until an ASIN is verified — do not invent ASINs. Affiliate URL may be empty; redirect builds from destination + env tag.

Seed URLs for confirmed Amazon products are the live amazon.co.uk pages above. For an existing DB, run `affiliate:apply-urls` (do **not** `db:reset`).

| Programme | Slug | Notes |
|-----------|------|-------|
| Amazon Associates UK | `amazon-associates-uk` | Tag from `AMAZON_ASSOCIATE_TAG` at redirect time |
| Brilliant | `brilliant` | `BRILLIANT_AFFILIATE_ID` |
| Astronomy Retailer | `astronomy-retailer` | Generic specialist slot (FLO / HPS later) |
| LEGO | `lego` | Seeded **INACTIVE** until access is ready — never on social/descriptions |

## Adding products

1. Open `/affiliate/products?new=1`
2. Choose programme, set destination + affiliate URLs, category, tags, commission estimates
3. Mark **featured** / **evergreen** carefully — featured boosts score; evergreen fills the Orbit recommendation slot
4. Or POST `/api/affiliate/products`

## Matching & recommendations

Deterministic first (`scoreAffiliateRelevance`). Future LLM strategy can implement the same `RelevanceStrategy` interface via `setRelevanceStrategy()`.

Scoring highlights: exact topic +40, related +20, category +15, evergreen +5, featured +10. Inactive programmes/products excluded. Max 4 links: 1 primary · ≤2 secondary · 1 evergreen.

On a video page: **Regenerate recommendations** → Approve / Reject / Remove.

## YouTube descriptions (Creator voice)

```ts
import { generateYouTubeDescriptionWithAffiliates } from "@/lib/affiliate/description-service";
import { mergeDescriptionWithAffiliateLinks } from "@/lib/publishing/youtube-package";
import { buildCreatorDescriptionTemplateMap } from "@/lib/affiliate/creator-description-voice";
```

- Editable templates in `AffiliateDescriptionTemplate` (seeded from Creator playbook — Brilliant, telescope, books, LEGO, topic-tuned book/LEGO first lines, headers, disclosure)
- Header (pick one): `If you want to go further` · `Orbit’s next steps (not a shop)`
- Disclosure is the **last line** of the affiliate block (never the first line of the description)
- Block placement: after chapters + subscribe · before playlist / next film / hashtags · not in the first screen
- Links use Orbit redirects (`/go/{slug}`), not raw affiliate URLs — placeholders only in templates
- Shorts: no affiliate block

### Topic → 4-slot recommendation menu

Encoded in `topic-product-map.ts` and applied by `recommendProductsForVideo`. Card may show up to 4 candidates; description auto-insert still follows Auditor (≤1 primary + optional companion). Empty a slot rather than force.

| Topic | Primary | Secondary | Evergreen | Leave empty |
|-------|---------|-----------|-----------|-------------|
| black holes | Book | Brilliant | Brilliant (if book primary) | Telescope, LEGO |
| Mars | Telescope | Book, LEGO | Brilliant | (contextual) |
| telescopes | Telescope | Book, LEGO | Brilliant | (contextual) |
| JWST | Explainer book | Brilliant | Brilliant | Telescope, LEGO |
| relativity | Brilliant | Book | Book | Telescope, LEGO |
| kids astronomy | LEGO | Kids book, telescope | Brilliant (not if under ~10) | **Never Brilliant as primary** |
| Starship | Book | LEGO, Brilliant | Brilliant | Telescope (unless launch/sky) |
| cosmology | Book | Brilliant | Brilliant | Telescope, LEGO |
| exoplanets | Book | Brilliant | Brilliant | Telescope as “exoplanet finder” |

## Link tracking

`GET /go/{slug}?utm_campaign={video-slug}&video={id}`

1. Resolve product  
2. Record click (video, placement, UTM, timestamp, destination)  
3. Apply programme tag from env  
4. 302 to affiliate URL with UTM preserved  

Recommended UTM (YouTube description): `utm_source=youtube` · `utm_medium=affiliate` · `utm_campaign={video-slug}` · `utm_content={product-slug}`

Social UTM map: see **Live Orbit social channels** above (`threads` / `instagram` / `facebook`).

## Reporting

- `/affiliate` — summary + **internal goals panel** + warnings + clicks/revenue by source (youtube, threads, instagram, facebook, …)
- `/affiliate/opportunities` — opportunity score, views, links, RPM  
- Homepage **Monetisation** card — month revenue, clicks, affiliate RPM, missing links  
- Metrics: clicks, CTR, conversions, EPC, revenue / 1k views, affiliate RPM (alongside YouTube RPM when ads data exists). `totalContentRpm()` ready for AdSense + Affiliate + Sponsorship.

### Goals ladder (internal, reporting only)

Shown on `/affiliate` — not a public page. The goals engine **never** auto-inserts placements to catch up; the editorial trust gate still decides links.

**Clock start:** earliest of (1) first `APPROVED`/`ACTIVE` `AffiliatePlacement.updatedAt`, or (2) first `AffiliateClick.timestamp`. Do not hard-code a calendar start date.

**Months:** anniversary months from that clock (Month 1 = first 30/31-day window from the start day).

| Period | Target | Floor |
|--------|--------|-------|
| Month 1 | £20 | £10 |
| Month N (N ≥ 2) | **2 × previous month’s actual commission** (not the previous target) | — |

Panel shows: current month number + date range · revenue so far vs target · clicks · working vs broken links · on track / behind (vs linear pace to target; Month 1 also treats floor hit as on track) · last month actual once Month 2+.

```ts
import { buildAffiliateGoalsSnapshot, computeMonthTargetGbp } from "@/lib/affiliate/goals";
import { getAffiliateGoalsPanel } from "@/lib/affiliate/goals-service";
```

## CSV imports

`/affiliate/import` or `POST /api/affiliate/import`

1. Preview (`dryRun`)  
2. Commit with `programmeSlug`  
3. Duplicate `contentHash` rejected  

Sample: `content/samples/csv/affiliate_amazon_sample.csv`

## URL health

`POST /api/affiliate/health` with `{ due: true, limit: 10 }` — throttled; does not hammer every URL. Prefer weekly manual/scheduled runs.

## Gear / public site (Phase 5 prep)

`GET /api/affiliate/gear` returns SEO-ready category + product JSON (`goUrl`, tags, programme). Ready for orbitwithben.com/gear — no full public marketing site in this app.

## Commands

```bash
cd 07_Content-Ops
npx prisma migrate deploy
npx prisma generate
npm run affiliate:apply-urls   # additive live amazon.co.uk destinations (no DB reset)
npm test                 # includes tests/affiliate.test.ts
npm run dev
```

Open http://localhost:3000/affiliate

## Manual account setup still required

- Amazon Associates UK approval + `AMAZON_ASSOCIATE_TAG=orbitgo-21` in operator env (never commit)
- Brilliant affiliate approval + `BRILLIANT_AFFILIATE_ID`
- Specialist retailer programme contracts / tracking links
- LEGO Affiliate access (programme seeded inactive; `space-lego` product inactive)
- Confirm remaining Amazon ASINs (`astronomy-binoculars`, `mars-book`) then `npm run affiliate:apply-urls`
- Production `AFFILIATE_REDIRECT_BASE_URL=https://orbitwithben.com/go` + DNS/hosting for redirects (or proxy to Content Ops)
