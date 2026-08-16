# Orbit With Ben Monetisation Master Plan

Status: implementation plan
Owner: Orbit With Ben
Primary repo: `TheLaughingGod1986/orbit-with-ben`
Audience: coding agents, product agents, content agents and channel operators

## 1. Mission

Turn Orbit With Ben from a YouTube channel into a diversified science-and-space media business with multiple revenue streams that compound as the content library grows.

The system must avoid dependence on any single monetisation source. YouTube ad revenue is a base layer, not the whole business.

Target revenue pillars:

1. YouTube advertising and fan funding
2. Affiliate revenue
3. Sponsorships and brand partnerships
4. Digital products
5. Memberships and premium community
6. Orbit-owned intellectual property and physical products
7. Website and SEO monetisation
8. Email/newsletter monetisation
9. Courses and education products
10. Licensing and B2B educational use

Core rule:

> Audience trust, scientific credibility and content quality come before short-term revenue.

Do not introduce monetisation that damages retention, makes videos feel like adverts, or recommends products Orbit would not endorse without commission.

---

## 2. Existing foundation

Before implementing anything, inspect the repository and reuse existing systems.

In particular, review:

- `docs/AFFILIATE_MONETISATION_SYSTEM.md`
- existing Content Ops app
- video registry and metadata
- publishing adapters
- analytics import system
- YouTube description generation
- schedule/calendar system
- existing database schema

Do not duplicate functionality already implemented.

The affiliate implementation plan already exists and should become one component of this wider monetisation platform.

---

# 3. North-star metric

Create a channel-level metric called:

## Total Content Revenue

Total Content Revenue should combine:

- YouTube ad revenue
- affiliate commission
- sponsorship revenue
- membership revenue
- Super Thanks / fan funding
- digital product sales
- merchandise / physical product margin
- newsletter revenue
- course revenue
- licensing revenue

Create:

## Total Content RPM

Formula:

`total attributable content revenue / total views * 1000`

Also calculate revenue by episode.

For each long-form video, the system should eventually answer:

- how many views did it generate?
- how much AdSense revenue?
- how much affiliate revenue?
- was it sponsored?
- how much sponsor revenue is attributable?
- did it generate product sales?
- did it generate email subscribers?
- did it generate members?
- what is its total revenue?
- what is its total RPM?
- what is its estimated lifetime value?

This is more useful than YouTube RPM alone.

---

# 4. Revenue pillar A: YouTube native monetisation

Support tracking for all available YouTube-native revenue streams.

## Track

- advertising revenue
- YouTube Premium revenue where available
- channel memberships
- Super Thanks
- Super Chat / Super Stickers if live streaming is introduced
- YouTube Shopping revenue

## Implementation

Extend analytics models so revenue can be stored by:

- video
- date
- revenue type
- currency
- source

Create a generic `RevenueEvent` or equivalent abstraction if this fits the current architecture better than separate models.

Do not over-engineer provider-specific schemas where a clean common revenue layer works.

---

# 5. Revenue pillar B: affiliate commerce

Use `docs/AFFILIATE_MONETISATION_SYSTEM.md` as the detailed implementation spec.

Priority affiliate categories:

- telescopes
- binoculars
- astrophotography equipment
- astronomy books
- science books
- educational platforms
- Brilliant / learning products
- astronomy courses
- space LEGO and models
- STEM kits
- relevant AI/science tools

Priority principle:

Affiliate products must be relevant to the exact video topic.

Avoid generic description spam.

Each long-form video should normally contain no more than:

- 1 primary recommendation
- 2 secondary recommendations
- 1 evergreen Orbit recommendation

Create an Affiliate Opportunity Score for planned and published videos.

---

# 6. Revenue pillar C: sponsorship platform

Build sponsorship management into Content Ops.

Create route:

`/monetisation/sponsors`

## Sponsor model

Store:

- company name
- website
- industry
- contact name
- contact email
- status
- notes
- source
- date contacted
- next follow-up date
- quoted fee
- agreed fee
- currency
- campaign dates
- content restrictions
- exclusivity requirements
- required talking points
- prohibited claims
- tracking URL/code

Suggested statuses:

- PROSPECT
- RESEARCHING
- READY_TO_CONTACT
- CONTACTED
- REPLIED
- NEGOTIATING
- AGREED
- ACTIVE
- COMPLETED
- DECLINED
- PAUSED

## Sponsor categories to prioritise

- astronomy retailers
- telescope manufacturers
- STEM education companies
- science learning platforms
- AI tools relevant to the audience
- productivity software
- electronics brands
- science subscription services
- educational publishers
- space/science events

## Sponsor/video matching

Each planned episode should produce a Sponsor Fit Score.

Use:

- topic
- audience intent
- historical performance
- product relevance
- expected views
- evergreen potential
- sponsor conflict/exclusivity

Do not automatically contact brands in the first implementation.

Build prospect tracking and recommendation first.

---

# 7. Sponsorship pricing engine

Create a configurable sponsorship pricing calculator.

Inputs:

- rolling average long-form views
- median long-form views
- expected views for the episode
- channel subscribers
- audience geography
- engagement
- integration type
- exclusivity
- usage rights
- duration

Integration types:

- 15-30 second mention
- 45-60 second integrated segment
- dedicated video
- Shorts sponsorship
- newsletter bundle
- website bundle
- multi-video package

Output:

- recommended floor price
- target price
- premium price

All assumptions must be editable.

Never hard-code a universal CPM as fact.

---

# 8. Sponsor media kit

Prepare data for an automatically generated Orbit media kit.

Include:

- channel description
- brand positioning
- key topics
- latest subscriber count
- monthly views
- average long-form views
- Shorts reach
- audience geography
- audience demographics if available
- strongest videos
- engagement metrics
- sponsorship formats
- contact details

Do not expose private analytics publicly without explicit approval.

Later allow export to PDF.

---

# 9. Revenue pillar D: Orbit digital products

Build product support around low-overhead digital products before physical merchandise.

Initial product candidates:

## Beginner astronomy

- Orbit Beginner Stargazing Guide
- Telescope Buying Guide UK
- Beginner Astronomy Pack
- Planet Observation Checklist
- Monthly Sky Guide

## Family / children

- Orbit Space Activity Pack
- printable colouring sheets
- planet fact cards
- space quizzes
- family stargazing checklist

## Premium educational content

- Solar System Explained
- Black Holes Explained
- Mars Exploration Guide
- Spaceflight Explained

Store product ideas in Content Ops even before commerce implementation.

Create status:

- IDEA
- VALIDATING
- BUILDING
- READY
- LIVE
- RETIRED

Track which videos can naturally promote each product.

---

# 10. Product validation rule

Do not build products purely because they sound interesting.

Prioritise products using evidence from:

- YouTube search demand
- viewer comments
- video performance
- affiliate clicks
- website searches
- email survey responses
- repeated audience questions

Create a Product Opportunity Score using:

- audience demand
- relevance
- production effort
- margin
- evergreen value
- differentiation
- distribution potential

---

# 11. Revenue pillar E: memberships

Prepare for an Orbit membership layer once the audience is large enough to justify ongoing delivery.

Possible membership brand:

`Orbit+`

Potential benefits:

- early access
- extended episodes
- monthly Q&A
- topic voting
- behind-the-scenes production
- member-only posts
- downloadable guides
- wallpapers
- launch/event watch discussions

Avoid launching memberships until there is enough recurring audience demand.

Create a readiness dashboard with signals such as:

- returning viewers
- comments per video
- repeat commenters
- email subscribers
- watch hours
- requests for more content

---

# 12. Revenue pillar F: OrbitWithBen.com

The website should become a monetisation and audience-ownership layer, not just a brochure site.

Future sections:

- `/gear`
- `/learn`
- `/guides`
- `/newsletter`
- `/videos`
- `/space-news`
- `/about`

Potential SEO content:

- best beginner telescopes UK
- best telescope for seeing Saturn
- best telescope for kids
- best astronomy books
- beginner astrophotography gear
- how to see Jupiter
- how to see Mars
- black holes explained
- SpaceX / Starship explainers

Each article must have a genuine editorial purpose.

Do not generate thin affiliate SEO pages at scale.

---

# 13. Revenue pillar G: email newsletter

Create the foundations for an owned audience.

Working concept:

## Orbit Weekly

Positioning:

A concise weekly briefing covering the most interesting developments in space, astronomy and science.

Track:

- subscribers
- source video
- source platform
- signup date
- campaign
- opens
- clicks
- affiliate clicks
- product sales
- unsubscribes

Potential future monetisation:

- affiliate links
- sponsor placements
- premium newsletter
- digital product launches
- YouTube traffic

Every long-form video should eventually have an optional newsletter CTA.

---

# 14. Revenue pillar H: courses

Do not build a course immediately.

Prepare the model for future courses such as:

`Astronomy for Complete Beginners`

Potential modules:

1. Understanding scale in the universe
2. Stars
3. Planets
4. Galaxies
5. Black holes
6. Cosmology
7. Observing the night sky
8. Choosing a telescope
9. Beginner astrophotography
10. The future of space exploration

Only proceed once audience demand is proven.

---

# 15. Revenue pillar I: Orbit intellectual property

Treat Orbit as a potential standalone character/IP, not merely a visual overlay.

Long-term possibilities:

- children's books
- activity books
- illustrated science books
- educational videos
- plush toys
- posters
- stickers
- model kits
- classroom material
- licensing

Create an IP opportunities document/model that records:

- concept
- audience
- estimated development cost
- margin
- partner requirements
- licensing potential
- status

Do not manufacture inventory early.

Use print-on-demand or pre-orders for initial physical validation where appropriate.

---

# 16. Revenue pillar J: licensing and education

Long-term B2B opportunities may include licensing Orbit content to:

- schools
- science education platforms
- publishers
- museums
- planetariums
- STEM programmes
- broadcasters

Prepare content metadata so future licensing is possible.

Store for each asset:

- ownership
- music licence status
- stock footage licence status
- AI-generated components
- third-party footage
- commercial reuse restrictions

This is important because content with unclear rights cannot be cleanly licensed later.

---

# 17. Unified monetisation dashboard

Create route:

`/monetisation`

Dashboard should eventually show:

## Revenue cards

- YouTube revenue
- Affiliate revenue
- Sponsorship revenue
- Membership revenue
- Product revenue
- Other revenue
- Total revenue

## Efficiency metrics

- YouTube RPM
- Affiliate RPM
- Sponsor RPM
- Total Content RPM
- revenue per subscriber
- revenue per long-form video

## Opportunity cards

- videos missing affiliate links
- high-performing videos with no monetisation CTA
- sponsor-ready episodes
- potential digital products
- videos driving newsletter signups

---

# 18. Episode monetisation view

Every long-form video detail page should have a Monetisation section.

Display:

- AdSense revenue
- affiliate placements
- affiliate clicks
- affiliate revenue
- sponsor
- sponsor revenue
- product CTA
- product sales
- email signups
- member conversions
- total attributable revenue
- Total Content RPM

Also display potential opportunities.

Example:

`MONETISATION OPPORTUNITY: High-performing video has no affiliate links.`

`SPONSOR OPPORTUNITY: Episode strongly matches astronomy retailer category.`

---

# 19. Content planning integration

Monetisation should influence planning, but never dominate it.

For every video idea calculate:

- Audience Opportunity Score
- Search Opportunity Score
- Affiliate Opportunity Score
- Sponsor Opportunity Score
- Product Opportunity Score
- Evergreen Score

Then derive an optional:

## Commercial Opportunity Score

This must remain separate from editorial priority.

The system should be able to identify topics that are both genuinely interesting and commercially strong.

Example:

`Best Telescope for Seeing Saturn`

- audience: high
- affiliate: very high
- sponsor: very high
- evergreen: very high

versus:

`What Happens at the End of the Universe?`

- audience: potentially very high
- affiliate: low
- sponsor: medium
- evergreen: high

Both may be worth producing for different reasons.

---

# 20. Funnel attribution

Build towards this funnel:

YouTube / Shorts / social
→ long-form video
→ website / newsletter / affiliate / product
→ repeat viewer
→ email subscriber
→ customer/member

Track first-party attribution where reasonably possible.

Avoid invasive tracking.

Do not fingerprint users.

Respect consent requirements and applicable privacy rules.

---

# 21. Development phases

## Phase 0: audit

Agent must first:

- inspect repository architecture
- inspect Prisma/data models
- read existing affiliate plan
- inspect analytics system
- inspect video detail UI
- identify existing monetisation-related code
- document what already exists

Do not implement duplicate features.

## Phase 1: unified revenue foundation

Build:

- monetisation navigation
- common revenue model
- revenue source enum/config
- `/monetisation` dashboard shell
- episode monetisation panel
- manual revenue entry/import capability

No destructive migrations.

## Phase 2: affiliate integration

Implement or finish the existing affiliate monetisation plan.

Integrate affiliate revenue into the unified dashboard.

## Phase 3: sponsor CRM

Build:

- sponsor prospects
- pipeline
- campaign records
- episode matching
- sponsorship pricing helper
- follow-up tracking

## Phase 4: newsletter + owned audience

Build:

- newsletter CTA metadata
- subscriber attribution hooks
- email-source reporting
- conversion tracking where available

Use an adapter architecture so the email provider can change.

## Phase 5: products

Build:

- product ideas
- validation status
- product/video mapping
- sales import/API abstraction
- product revenue attribution

## Phase 6: website/SEO commerce

Prepare shared APIs/data for OrbitWithBen.com:

- gear
- guides
- products
- newsletter
- episode pages

## Phase 7: memberships and IP

Add membership analytics and IP opportunity management only when justified by audience scale.

---

# 22. Engineering requirements

Follow existing application conventions.

Use:

- TypeScript
- Prisma
- Zod where appropriate
- shared service layers
- typed analytics

Avoid:

- `any`
- duplicated provider logic
- hard-coded affiliate/sponsor credentials
- monetisation logic buried inside UI components

Suggested domain structure if compatible:

`lib/monetisation/`

Possible modules:

- `revenue.ts`
- `attribution.ts`
- `rpm.ts`
- `sponsors.ts`
- `pricing.ts`
- `products.ts`
- `opportunities.ts`

Do not force this structure if the repo already has a better domain pattern.

---

# 23. Testing

Add automated coverage for important calculations and attribution.

At minimum test:

- Total Content Revenue
- Total Content RPM
- affiliate attribution
- sponsor revenue attribution
- product revenue attribution
- duplicate revenue imports
- currency handling
- opportunity scoring
- episode revenue aggregation

Use existing test tooling.

---

# 24. Safety and editorial guardrails

The system must not:

- fabricate endorsements
- automatically claim Ben uses a product when he does not
- promote scientifically dubious products
- conceal affiliate relationships
- generate fake sponsor claims
- invent sponsorship arrangements
- automatically publish commercial claims without review

Require approval before commercial copy is published.

---

# 25. Operational targets

## Stage A: channel still small

Focus on:

- publishing consistently
- affiliate infrastructure
- email capture foundations
- analytics
- content quality

Do not spend significant time building merchandise.

## Stage B: audience traction

Prioritise:

- first sponsor outreach
- newsletter
- affiliate optimisation
- first small digital product

## Stage C: established audience

Prioritise:

- recurring sponsors
- memberships
- premium products
- website SEO engine
- course validation

## Stage D: meaningful brand/IP

Explore:

- Orbit books
- physical products
- licensing
- education partnerships
- branded astronomy products

---

# 26. Agent execution protocol

When an agent starts work from this document:

1. Read this entire plan.
2. Read `docs/AFFILIATE_MONETISATION_SYSTEM.md`.
3. Audit the current repository before editing code.
4. Write a short implementation status note stating what already exists.
5. Select the earliest incomplete phase.
6. Implement it end-to-end where practical.
7. Add migrations safely.
8. Add tests.
9. Run lint/typecheck/tests relevant to changed code.
10. Update documentation.
11. Report exactly what was changed and what remains.

Do not merely create another plan unless implementation is blocked by missing credentials or external account setup.

When blocked by credentials, complete everything that does not require them and leave precise setup instructions.

---

# 27. Definition of success

The long-term system is successful when Orbit With Ben can answer, from one dashboard:

- What did the channel earn this month?
- Which revenue stream is growing fastest?
- Which videos earn the most total revenue?
- Which videos have the highest Total Content RPM?
- Which videos are under-monetised?
- Which future topics have strong commercial opportunities?
- Which sponsors fit upcoming episodes?
- Which affiliate products actually convert?
- Which content drives email subscribers?
- Which products should be built next?
- How dependent are we on YouTube ads?

The ultimate goal is not to maximise ads.

It is to build **Orbit With Ben into a durable audience-owned science and space media business with diversified recurring revenue and valuable intellectual property.**
