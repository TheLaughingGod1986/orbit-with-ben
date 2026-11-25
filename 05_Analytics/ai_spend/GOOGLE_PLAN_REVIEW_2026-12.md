# Google AI Plan Review — Before the 12 Dec 2026 Renewal (J3489)

**Prepared for:** Ben · **Date:** 25 Nov 2026 · **Renewal:** 12 Dec 2026 · **Current plan:** Google AI Ultra 20x (£189.99/mo)  
**Spend:** £0 (read-only audit). **No subscription changes are made by agents — Ben makes any plan change himself.**

---

## Recommendation

**Keep Google AI Ultra 20x (£189.99/mo) through December, then review again on Mon 4 Jan 2027.**

- **The surprise:** Flow video credits are **no longer** the main reason to keep Ultra 20x — **the Gemini / Antigravity agent quota is.**
- **Flow credits would fit on Ultra 5x (£79.99/mo, 10,000 credits, saving £110/mo):** Google is retiring Veo 3.1 Quality (100 cr) and Fast (10 cr) on **5 Dec 2026**, replacing them with Veo 3.1 Lite (5 cr on Ultra) and Omni Flash 1.2 (18–24 cr for 6–8 s at 720p). That drops a 4-long + 16-Short History of Science month from ~14,000–24,000 cr down to **~2,500–10,000 cr**, which fits inside Ultra 5x.
- **Gemini's agent quota will NOT fit on Ultra 5x at today's studio workload:** The "2–29% used" readings on 18–24 Nov were an artefact of **three early weekly quota resets** around the 18 Nov Gemini 4 Neon launch, not light use. In complete 7-day weeks on Ultra 20x, Gemini used **38–86%+** of the weekly cap (~42–95% full-week pace), and this week (23–25 Nov) it has already burned **15% in 34 hours** (~74%/week pace). Because **Ultra 5x cuts Gemini usage limits to one-quarter of Ultra 20x** (5x Pro vs 20x Pro), downgrading without throttling Gemini's routing would **exhaust Gemini's weekly cap in 2–4 days every week and visibly slow all three channels** — especially now that Cursor/Grok is £20 (capped), Codex (£90) is hitting its weekly limit, Claude is conserved to 4 cloud runs/day, and Field Order History ramps to 3 films/week on 1 Dec.
- **Google AI Pro (£18.99/mo, saving £171/mo) is not viable:** It fails **both** Flow (1,000 cr/mo vs HOS's 2,500–10,000 need) and Gemini (1/20 of Ultra 20x — exhausted in under 12 hours/week).
- **If you want to save £110/mo now anyway (Conditional Option B):** Step down to **Ultra 5x (£79.99/mo)** before 12 Dec **only if** we also throttle Gemini's routing off overflow lanes (`review`, `assembly`, `listing`, `script`, `chart` — ~70% of its runs) and reserve Gemini strictly for `studio`, moving-video `qa`, `facts`, and Chief failover, accepting slower overnight throughput whenever Codex and Claude hit their limits. Check Google One storage is under 20 TB first.

---

## 1. Last 8 Weeks of Actual Use (8 Oct – 25 Nov 2026)

*Source: `05_Analytics/ai_spend/ledger.jsonl` (starts 8 Oct 2026), `runs.jsonl` (5,378 runs), `jobs/queue.json`, and live `agy -p /usage` on 25 Nov 06:01Z.*

### Flow credits & Cloud/Vertex credits by billing cycle

| Cycle | Flow Balance Drop | Logged Flow Spend | By Channel (corrected) | Cloud / Vertex Credit |
|---|---:|---:|---|---|
| **Tail (8–12 Oct)** | 52 → 52 (0) | 0 | Exhausted prior cycle | £17.40 spent (HOS £16.50, OWB £0.90) |
| **Cycle 1 (12 Oct – 12 Nov)** | **20,060** (25,050 → 4,990; 80% used) | 16,560 *(~3,500 net unlogged in 29–30 Oct HOS:008/009 mints)* | **HOS ~19,910 (99.3%)** across 006–010 & 013 · **OWB 150 (0.7%)** *(120 on 028 mis-tagged `HOS:028`, 30 on 033)* · **WW2 0** | **£1.22** spent (HOS £0.59, OWB £0.63) |
| **Cycle 2 so far (12–24 Nov, 12 d)** | **1,600** (25,050 → 23,450; 6% used) | 1,610 | **HOS 1,610 (100%)** *(013: 1,000; 010: 600; 006: 10)* · **OWB 0** · **WW2 0** | **£0.00** spent · **£144.66 available** (£69.48 Oct + £75.18 Nov) |

*Why Cycle 2 looks quiet:* No new HOS long minted its main picture batch between 13 Nov and 24 Nov. Unused monthly Flow credits expire on billing day 12; monthly Cloud credits expire **1 year after grant**, so the existing £144.66 stays usable even after a downgrade.

### Gemini / Antigravity weekly quota & run volume (30 Oct – 25 Nov)

| Window (reset timestamp) | Span Observed | Peak Used (Ultra 20x) | Implied Full-Week Pace | Equivalent Share of Ultra 5x (÷4) | Mini Gemini Runs (mon-wk) |
|---|---:|---:|---:|---:|---:|
| Ending Fri 30 Oct 22:00Z | 6.4 d (to 08:30Z) | **55%** | ~60% | **~240%** | 390 (wk 26 Oct, 41% of Mini) |
| Ending Fri 06 Nov 22:00Z | 6.4 d (to 08:31Z) | **38%** | ~42% | **~168%** | 336 (wk 02 Nov, 35% of Mini) |
| Ending Fri 13 Nov 23:42Z | 6.4 d (to 08:31Z) | **86%** | **~95%** | **~380%** | 335 (wk 09 Nov, 46% of Mini) |
| 14–17 Nov *(reset early 18 Nov)* | 3.4 d | **49%** | ~100% | ~400% | 392 (wk 16 Nov, 48% of Mini) |
| 18–21 Nov *(reset early 22 Nov)* | 3.3 d | **29%** | ~62% | ~248% | *(same week; Neon live)* |
| 22–23 Nov *(reset early 23 Nov)* | 1.0 d | **11%** | — | — | *(partial)* |
| **Current: 23–25 Nov 06:01Z (live)** | **1.4 d** | **15%** *(+13% in 21.5 h)* | **~74%** | **~296%** | 116 in 2.3 d + MacBook shared |

Across the last 6 complete weeks (12 Oct – 22 Nov), Gemini averaged **385 Mini runs/week** (35–60% of Mini output), plus MacBook slots 1 & 2 on the same Google account (244 MacBook claims alongside 357 Mini Gemini claims in the last 7 days). Only ~12% of Gemini runs are unique lanes (`studio`, `qa`, `facts`); **~70%+** are overflow/fallback (`review`, `assembly`, `listing`, `script`, `chart`) keeping the studio moving when Claude, Codex, or Cursor hit limits. *(Bonus observation: `agy /usage` shows the bundled `Claude and GPT models` pool in Antigravity at **100% remaining / unused**.)*

---

## 2. December Projection (12 Dec 2026 – 12 Jan 2027)

- **History of Science (Flow primary driver):**
  - *Before 12 Dec (current cycle, 23,450 cr left):* Easily covers `HOS:128` Edison vs Tesla (10 Dec), Film 2 Trinity Test (17 Dec), and Film 3 Accidental Inventions (24 Dec) plus Shorts.
  - *After 12 Dec (next billing cycle):* Film 4 Wright Brothers (31 Dec) + 3–4 January longs + ~16 Shorts (16–19 s 3D cartoon). **Critical 5 Dec change:** Google retires Veo 3.1 Fast (10 cr) and Quality (100 cr) on **5 Dec 2026**; under replacement **Veo 3.1 Lite (5 cr on Ultra)** and **Omni Flash 1.2 (18–24 cr for 6–8 s 720p; 0 cr 1080p upscale)**, a 70–100 plate HOS long drops from ~3,000–6,600 cr to **~500–2,400 cr**. Monthly HOS Flow need: **~2,500–10,000 cr** (studio must update Flow scripts/rules before 5 Dec).
- **Orbit With Ben:** 031–034 & J01 already have picture done; `064` Every Planet (16 Dec) and January search-led longs rely mostly on NASA/archive + Nano Banana 2 (0 cr). Projected Flow: **~0–500 cr/mo**.
- **Field Order History (WW2):** Ramps to **3 longs/week** from 1 Dec + 2–3 Shorts/film cut from longs. **0 Flow credits** (archive photos + code maps), **high Gemini load** (moving-video QA on Neon, facts audits, Studio tasks, reviews).
- **Projected December Gemini quota:** With WW2 at 3×/wk, 4 new HOS search-led longs, Cursor/Grok dropped to £20, Codex hitting weekly caps, and Claude at 4 cloud runs/day, expect **65–95%/week of Ultra 20x**.

---

## 3. Current UK Google AI Tiers (Verified 25 Nov 2026 from Official Google Pages)

*Verified directly from `one.google.com/about/google-ai-plans/?hl=en-GB&gl=GB`, `support.google.com/flow/answer/16526234`, `antigravity.google/pricing` + `/docs/plans`, and `developers.google.com/profile/help/benefits`.*

| Feature | Google AI Plus | Google AI Pro | Google AI Ultra 5x *(replaces ledger's "~£90" guess)* | Google AI Ultra 20x *(Current)* |
|---|---|---|---|---|
| **UK Price (incl. VAT)** | £4.49 (400 GB) / £7.99 (2 TB) | **£18.99/mo** | **£79.99/mo** | **£189.99/mo** |
| **Saving vs Current** | £185.50 / £182.00/mo | **£171.00/mo** | **£110.00/mo** (£1,320/yr) | £0 |
| **Flow Credits (+50/day)** | 200/mo | **1,000/mo** | **10,000/mo** | **25,000/mo** |
| **Veo 3.1 Lite (post-5 Dec)** | 10 cr/gen | 10 cr/gen | **5 cr/gen** | **5 cr/gen** *(0 cr Lower Priority)* |
| **Gemini / Antigravity Quota** | 2x non-AI; **no 5-h refresh**, Hydrogen only | **1x Pro** (4x non-AI); 5-h refresh + weekly cap; Neon/Carbon/Claude 5.5 | **5x Pro** (1/4 of Ultra 20x); 5-h refresh + weekly cap; Neon/Carbon/Claude 5.5 | **20x Pro** (4x Ultra 5x); highest 5-h refresh + max weekly cap |
| **Google Cloud Credits** | None | **US$10/mo** (~£7.50) | **US$40/mo** (~£30) | **US$100/mo** (~£75.18) |
| **Storage (Gmail/Drive/Photos)** | 400 GB / 2 TB | 5 TB | **20 TB** | **30 TB** |
| **Other Perks** | None | YT Premium Lite (ind.), Home Std, Health | YT Premium Family, Home Adv, Health | YT Premium Family, Home Adv, Health, Project Genie |

*Notes:* (1) Google does not publish raw Antigravity token counts separately from the 5x vs 20x Pro ratio; planning assumes the published 4:1 ratio. (2) Pro and Ultra allow one-off AI credit top-ups (2,500 / 5,000 / 20,000 cr), though studio pay-per-use cap is £0 (`pay_per_use_caps.json`). (3) `one.google.com` displayed a UK Black Friday "up to 50% off selected Google AI plans" member banner on 25 Nov — worth checking on your own Google One page.

---

## 4. What Changes on a Downgrade & Next Step for Ben

| Choice before 12 Dec | Monthly Cost | Fits Dec Flow? | Fits Dec Gemini? | What You Lose / Trade-off |
|---|---:|---|---|---|
| **Option A (Recommended): Keep Ultra 20x** | £189.99 | Yes (huge headroom) | **Yes (headroom)** | No saving in Dec; re-review **4 Jan 2027** after 4 clean post-Neon weeks & first monthly channel scorecard. |
| **Option B (Budget cut): Switch to Ultra 5x** | **£79.99** *(saves £110)* | **Yes** (post-5 Dec pricing) | **Only if throttled** | Cuts Gemini quota by ~75% (will stall 3–5 d/wk unless overflow lanes are restricted), Cloud credit $100→$40 (existing £144.66 kept), storage 30→20 TB, loses 0-cr Lite Lower Priority & Project Genie. |
| **Option C: Google AI Pro** | £18.99 *(saves £171)* | **No** (short for HOS) | **No** (<12 h/wk) | Breaks HOS Flow & Antigravity; loses YT Family & 25 TB storage. Not recommended. |

**Next step (Ben only):** No action needed for **Option A**; if you prefer **Option B**, switch to **Google AI Ultra 5x (£79.99/mo)** in Google One before **12 Dec** (after checking Drive/Photos usage is <20 TB) and tell the studio to restrict Gemini to unique lanes (`studio`, `qa`, `facts`, Chief failover). Separately, the studio should schedule a pre-**5 Dec** task to adapt HOS Flow automation/rules for Veo 3.1 Lite / Omni Flash 1.2 before Veo 3.1 Fast/Quality retire.
