# J2985 — Board credits: dual Used/Time bars, renewal dates, and monthly plan verdicts

- **Worker:** `gemini` (Mini job queue worker), 17 Nov 2026
- **Spend:** none (`£0.00` / `0 credits`). Read-only checks on billing and usage pages; no plan change, purchase, or top-up.
- **Guard check:** no account address, card, email, or private-network address in tracked files, logs, or thread notes.

## 1. Renewal dates & cycles (`05_Analytics/ai_spend/plans.json`)

The single shared `8 Oct – 12 Nov` test period has been retired and replaced by each subscription's own rolling monthly billing cycle (`cycles` in `ai_spend.py doc`):

| Subscription | Monthly price (incl. VAT) | Cycle start | Renews (London) | How verified (read-only, 17 Nov 2026) |
|---|---:|---|---|---|
| **Google AI Ultra (30 TB)** (`flow`, `gemini`, `vertex`) | `£189.99/mo` | `2026-11-12` | **Sat 12 Dec 2026** (`billingDay: 12`) | `one.google.com/about/plans`, Cloud Billing > Credits, and 12–13 Nov Flow refill on the Mini's Studio/Flow Chrome |
| **Claude Ultra (10x)** (`claude`) | `£180/mo` | `2026-11-08` | **Tue 8 Dec 2026** (`billingDay: 8`) | `claude.ai` Settings > Billing (`Your Claude Ultra plan (10x Pro usage every week), started 8 Nov 2026, auto-renews 8 Dec 2026`) |
| **ElevenLabs Creator** (`elevenlabs`) | `£20/mo` | `2026-10-30` | **Mon 30 Nov 2026** (`billingDay: 30`) | ElevenLabs API `/v1/user/subscription` (`tier=creator`, `$22.00` subtotal / `$26.40` incl. tax, resets & bills `30 Nov 2026`) |
| **Cursor & Grok (shared plan)** (`cursor`) | `£180/mo` now (`£20` planned) | `2026-10-24` | **Tue 24 Nov 2026** (`billingDay: 24`) | `grok.com/dashboard/billing` (`cursor.com/dashboard/spending` redirects there: `Ultra`, period `24 Oct – 24 Nov 2026`, `Renews 24 Nov 2026`) |
| **ChatGPT Pro (Codex)** (`codex`) | `£90/mo` | — | **Unread** | **Unread for Ben (1 line):** ChatGPT Pro has no signed-in `chatgpt.com` billing reader on the Mini (`ai_spend_daily.py` reads Codex weekly quota from local `~/.codex/sessions` logs only). |

## 2. Finding on the "separate £20 Grok plan"

- **There is no separate £20 Grok subscription.** On the Mini's billing reader, `cursor.com/dashboard/spending` redirects to `grok.com/dashboard/billing`, where **Grok Bot and Cursor share one unified weekly allowance** (this week's split on the billing page: **Grok Bot 54%, Cursor 46%**).
- The `£20` Grok entry added to `plans.json` on 9 Nov was Ben's planned downgrade of that **same shared Cursor/Grok subscription** from Ultra (`£180/mo`) to the `£20` tier — not a second subscription alongside Cursor.
- As of 17 Nov 2026, `grok.com/dashboard/billing` still shows **Ultra (`£180/mo`)** active through **Tue 24 Nov 2026** (`Renews 24 Nov 2026`), so Ben can confirm on that page before 24 Nov whether the downgrade to the `£20` tier is scheduled or whether he prefers to keep Ultra given 4/4 weeks hitting 100%.
- On the board (`Agents → Credits` and `/ai`), the duplicate `Cursor` and `Grok` tiles are consolidated into **one `Cursor & Grok` card** naming the `Grok Bot 54%, Cursor 46%` split and this billing note.

## 3. Live card readings, dual bars & verdicts (17 Nov 2026)

Every card renders **two left-to-right bars** (**Used** in the pool's active window vs **Time** elapsed in that window, with London reset/renewal labels), pace colouring (`blue` using little, `green` on pace, `amber`/`red` ahead of time or at limit), date stamps whenever any reading is older than 30 hours (never a bare percentage), and a plain monthly verdict once at least 7 days of the cycle have elapsed (`The board advises only; changing a plan is Ben's`):

| Card | Used bar (L→R) | Time bar (L→R, London) | Pace | Plain verdict shown on card |
|---|---|---|---|---|
| **Flow** (`Google AI Ultra · £189.99/mo · renews Sat 12 Dec`) | `2% used` (`500 of 25,000`) | `19% of month · renews Sat 12 Dec` | `using little` (blue) | `Verdict after 1 week of cycle (5d in) · Keeping Ultra (£189.99) this month (9 Nov decision; last cycle used 25,030), then review £90 tier (10,000)` *(plus note: "History of Science picture work, the main use of Flow, may not have run yet this cycle.")* |
| **ElevenLabs** (`ElevenLabs Creator · £20/mo · renews Mon 30 Nov`) | `34% used` (`41,250 of 121,114`) | `60% of month · renews Mon 30 Nov` | `using little` (blue) | `Keep ElevenLabs Creator (£20): used 41,250 of its 121,114 allowance with 60% of the month gone (ElevenLabs Starter's 30,000 would have run out)` |
| **Vertex** (`Google AI Ultra · £189.99/mo shared · renews Sat 12 Dec`) | `0% used` (`£0.00 of £75.18/mo (£144.66 avail)`) | `19% of month · renews Sat 12 Dec` | `using little` (blue) | `Included in Google AI Ultra (£75.18/mo Cloud credit; tier follows Flow)` |
| **Claude** (`Claude Ultra · £180/mo · renews Tue 8 Dec`) | `62% used` (`62% of weekly limit`) | `88% of week · resets Wed 18 Nov, 10:00` | `using little` (blue) | `Keep Claude Ultra (10x) (£180): used 62% of weekly limit (above Claude Max (5x)'s 50%; Fable hit 100%)` *(plus note: "Fable model weekly limit 100% used")* |
| **Codex** (`ChatGPT Pro · £90/mo · billing renewal date unread`) | `100% used` (`100% of weekly limit`) | `95% of week · resets Tue 17 Nov, 23:22` | `at limit` (red) | `Keep: hit its weekly limit 2 of 3 weeks (avg 96%/wk)` |
| **Cursor & Grok** (`Cursor & Grok · £180/mo now (£20 planned) · renews Tue 24 Nov`) | `100% used` (`100% of weekly limit`) | `80% of week · resets Thu 19 Nov` | `at limit` (red) | `Keep: hit its weekly limit 4 of 4 weeks (avg 100%/wk)` *(plus `Grok Bot 54%, Cursor 46%` & shared-plan billing note)* |
| **Gemini** (`Google AI Ultra · £189.99/mo shared · renews Sat 12 Dec`) | `49% used` (`49% of weekly limit`) | `52% of week · resets Fri 20 Nov, 23:15` | `on pace` (green) | `Included in Google AI Ultra · hit weekly limit 0 of 4 weeks (avg 57%/wk)` |

## 4. Phone-sized screen verification (390×844 @ 2× DPR)

Rendered from `05_Analytics/kanban/board_site/dist` against live `board.json` merged with `python3 scripts/ai_spend.py doc` and inspected visually on the Mini (PNG binaries kept outside git per `.gitignore`):

1. **Phone viewport (`390×844`, `Agents → Credits`):**
   - Path on Mini: `/Users/benjaminoats/_desk/reviews/J2985/credits_agents_phone_viewport_v01.png` (`218,993` bytes)
   - SHA-256: `148f6cd6235a9cea4540f13b5274f5bc6aadc9cfdf2620f5cf6bf499e9922fc0`
2. **Full 7-card `Credits` section at `390px` phone width:**
   - Path on Mini: `/Users/benjaminoats/_desk/reviews/J2985/credits_agents_phone_full_section_v01.png` (`448,468` bytes)
   - SHA-256: `f72e7921e674e34ff5022d40037613ae01338e9276ceca9e846691f06b2c90a2`
3. **`/ai` page `Credit left & pace` card at `390px` phone width:**
   - Path on Mini: `/Users/benjaminoats/_desk/reviews/J2985/credits_ai_page_phone_v01.png` (`670,120` bytes)
   - SHA-256: `2d31bec60f8a873d7e82591390ae80f2408d97205cd6b06b06bd97512ae6921c`

## 5. Post-merge step for Chief

After merging this PR to `main`:
1. Publish updated `credits.json` to `board-data`: `python3 scripts/board_publish.py --force`
2. Build and deploy static pages to Cloudflare Pages:
   `python3 05_Analytics/kanban/board_site/build.py && cd 05_Analytics/kanban/board_site && npx wrangler pages deploy dist --project-name studio-kanban`
3. Verify `https://studio-kanban.pages.dev/#agents` (`Credits` section) on a phone-sized viewport.
