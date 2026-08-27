# Orbit Shorts — funnel metrics, monster hooks & cross-post timing

**Status:** Ops lock for kinetic-caption v02 Shorts  
**Updated:** 2026-08-27  
**Related:** `PUBLISHING_AND_SHORTS_STRATEGY.md` · `TikTok/SHORTS_ONSCREEN_TEXT_STYLE.md` · `.cursor/rules/orbit-shorts-related-video.mdc`

---

## Funnel stack (every Short)

| Layer | What | Where |
|-------|------|-------|
| 1 | Kinetic burn-in (yellow/white lowercase) | First ~8s of picture |
| 2 | Soft end CTA `watch the full film →` | Last ~4s burn-in |
| 3 | Description “Watch the full film: youtu.be/…” | YT description |
| 4 | **Related video → that Short’s Thursday long** (primary Short → long CTA) | Desktop Studio Related (SEA play-pill) |
| 5 | Pinned comment “Full film here → …” | YT comments — **optional** if Related is set; existing pins may stay |
| 6 | TikTok caption “Full film on YouTube.” | TT description (no raw URL spam) — TikTok uploads paused until ban lift |

If **Related video** is missing, treat the Short as **not funnel-complete**. A pin alone does **not** substitute.

### Related video lock (2026-08-27)

- Every Short (live, scheduled, past public): desktop Studio **Related video** → the Thursday long that Short already sells.
- Never another Short · never a dead id · never dump every Short onto one film.
- Week map: Last Star leftovers through 2 Sep → `REXYxuLOBoI` · Europa 3–9 Sep → `NbW5G1BpPY0` · Neutron from 10 Sep → `Yk1tLh23rko` · JWST leftovers Sat 22–Tue 25 → `ziKBPJ6FY0U` · live leftovers → the long they already name.
- Zero `/go/` on Shorts.
- How: Content → Short → Related video → pick the long → Save (Advanced features). Not mobile Studio. Longs do not get this field.

Canonical Cursor rule: `.cursor/rules/orbit-shorts-related-video.mdc`.

---

## Metrics checklist (48h / 7d)

Track in YouTube Analytics (Shorts) + TikTok Studio:

| Metric | Target signal | Action if weak |
|--------|---------------|----------------|
| **3s / hooked views** | Strong relative to impressions | Rewrite punch-first beat; stronger cold open |
| **Avg view duration %** | ≥ 70% on ≤45s cuts | Trim mid; cut explanation before CTA |
| **Swipe / skip early** | Spike before beat 2 | Monster hook must land by 1.5s |
| **CTR to related / long** | Any measurable related views | Confirm Related video in desktop Studio + CTA text |
| **Long-form from Shorts** | Traffic source “Shorts” on pillar | Related required; description link required; pin optional |
| **Subs from Shorts** | Non-zero on hero hooks | Lead cluster with monster hook Short |

Log weekly in `00_Brand/Channel-Setup/audits/` as `SHORTS_FUNNEL_CHECK_YYYY-MM-DD.md`.

---

## Monster-hook ordering

Per pillar cluster, publish order is **not** narrative order — it is **retention order**:

1. **Monster hook** (highest stop-scroll) — Day 1 evening after the long  
2. Visceral mechanism / “how” beat  
3. Wonder / theory beat  
4. Soft cliffhanger → “watch the full film”

Examples:

| Pillar | Monster hook Short |
|--------|--------------------|
| Aliens | “Where is everybody?” (Fermi) |
| Black hole | “Cross this line and you never come back” |
| Exoplanets | “It rains glass sideways” |

Builders: `punch_first()` in `TikTok/auto/onscreen_captions.py` forces the strongest phrase onto beat 0.

---

## Cross-post timing (YouTube → TikTok)

| Step | When | Why |
|------|------|-----|
| YouTube Short goes public / scheduled | T0 | Own the native Shorts graph + related funnel |
| TikTok upload of same cut | **T0 + 1 hour** | Avoid identical-second cross-post; YT gets first indexed engagement |
| Caption | Existential hook first + “Full film on YouTube.” | TT is discovery; YT is the product |
| Delete v01 dupes | After v02 confirms in TT content list | One live asset per idea |

Automation notes:

- YT replace: `audits/_replace_shorts_v02_youtube.py`
- TT replace: `TikTok/_replace_scheduled_v02_cdp.py`
- TT dupe cleanup: `TikTok/_delete_v01_dupes_cdp.py`
- Pin CTAs: `audits/_pin_all_shorts_fullfilm_cta.py`

---

## Pin / comment blocker

YouTube **rejects comments on Private videos** (“Comments are not supported on private videos”).

Before batch-pinning:

1. Studio → each Short → set **Public** (live cluster) or **Schedule** (future) — never leave replace uploads as Private drafts  
2. Then run `audits/_visibility_and_pin_shorts.py` or `_pin_all_shorts_fullfilm_cta.py`

---

## Caption sync

1. `TikTok/auto/_sync_shorts_caption_beats.py` — Scribe word timestamps for each Short hook  
2. Rebuild `*_shorts_v02.py` — loads `10_Shorts/07_Caption-Sync/*_beats.json` when present  
3. Re-replace scheduled assets only (public already-live cuts: pin + related first; replace if burn-in materially changes)
