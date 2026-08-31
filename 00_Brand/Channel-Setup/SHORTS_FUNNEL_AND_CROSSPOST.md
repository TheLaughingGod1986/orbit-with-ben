# Orbit Shorts — funnel metrics, monster hooks & cross-post timing

**Status:** Ops lock for kinetic-caption v02 Shorts  
**Updated:** 2026-08-31 — Related pill only / no new Short pins · house+UAT bible  

**Related:** `ORBIT_HOUSE_AND_UAT_BIBLE.md` · `PUBLISHING_AND_SHORTS_STRATEGY.md` · `TikTok/SHORTS_ONSCREEN_TEXT_STYLE.md` · `.cursor/rules/orbit-shorts-related-video.mdc`

---

## Funnel stack (every Short)

| Layer | What | Where |
|-------|------|-------|
| 1 | Kinetic burn-in (yellow/white lowercase) | First ~8s of picture |
| 2 | Soft end CTA `watch the full film →` | Last ~4s burn-in |
| 3 | Description “Watch the full film: youtu.be/…” | YT description |
| 4 | **Related video pill** → that week’s Thursday long | Desktop Studio Related (only Short → long CTA) |

**Locked 28 Aug 2026:** no new pinned comments on Shorts. Related pill only. Pin not required when Related is set. Long-form pins stay. Existing live Short pins may stay (do not mass-unpin / remint). See `.cursor/rules/orbit-shorts-related-video.mdc`.

Week map: Last Star leftovers through 2 Sep → `REXYxuLOBoI` · Europa 3–9 Sep → `NbW5G1BpPY0` · Neutron from 10 Sep → `Yk1tLh23rko` · JWST leftovers Sat 22–Tue 25 → `ziKBPJ6FY0U` · live leftovers → the long they already name. Zero `/go/` on Shorts. Desktop Studio only (Advanced features). Longs do not get this field.

If Related is missing, treat the Short as **not funnel-complete** (auditor FAIL). A pin alone does **not** substitute.

UAT (31 Aug): score Studio Related and the public Shorts-player overlay **separately**. Overlay FAIL is not an automatic remint. Thumb PASS only on contrast + crop + no Orbit + distinct plate — see `ORBIT_HOUSE_AND_UAT_BIBLE.md`.


---

## Metrics checklist (48h / 7d)

Track in YouTube Analytics (Shorts) + TikTok Studio:

| Metric | Target signal | Action if weak |
|--------|---------------|----------------|
| **3s / hooked views** | Strong relative to impressions | Rewrite punch-first beat; stronger cold open |
| **Avg view duration %** | ≥ 70% on ≤45s cuts | Trim mid; cut explanation before CTA |
| **Swipe / skip early** | Spike before beat 2 | Monster hook must land by 1.5s |
| **CTR to related / long** | Any measurable related views | Confirm Related pill + on-screen CTA + description URL |
| **Long-form from Shorts** | Traffic source “Shorts” on pillar | Related + description link required (no new Short pins) |

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
- Pin CTAs (long-form only going forward): `audits/_pin_all_shorts_fullfilm_cta.py` — **do not** use to add new Short pins after 28 Aug 2026 lock

---

## Pin / comment blocker (legacy Short pins)

YouTube **rejects comments on Private videos** (“Comments are not supported on private videos”).

**Going forward (28 Aug 2026):** do **not** add new Short pins. Related pill only. Existing live Short pins may stay.

Before any legacy pin maintenance (grandfathered only):

1. Studio → each Short → set **Public** (live cluster) or **Schedule** (future) — never leave replace uploads as Private drafts  
2. Then run helpers only if Ben explicitly asks to touch an existing pin — default is leave them alone

---

## Caption sync

1. `TikTok/auto/_sync_shorts_caption_beats.py` — Scribe word timestamps for each Short hook  
2. Rebuild `*_shorts_v02.py` — loads `10_Shorts/07_Caption-Sync/*_beats.json` when present  
3. Re-replace scheduled assets only (public already-live cuts: Related pill first; replace if burn-in materially changes)
