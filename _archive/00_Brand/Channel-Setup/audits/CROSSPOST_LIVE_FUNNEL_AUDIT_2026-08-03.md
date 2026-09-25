# Cross-post live funnel audit — 2026-08-03

**Goal:** Live + scheduled YouTube Shorts should be live/scheduled on TikTok, Instagram, Facebook, and Threads with Orbit branding and full-film CTAs.

## YouTube (source of truth)

### Live now (Public)

| Short | ID | Full-film link in description | Related | Pinned comment |
|-------|----|-------------------------------|---------|----------------|
| Where Is Everybody? (Fermi) | `1HuV8o3gOss` | Yes → `youtu.be/Mo93x0fxB1Q` | `Mo93x0fxB1Q` | **Still needed** |
| Space Is Rude About Distance | `dPMJQp2gMNc` | Yes → `youtu.be/Mo93x0fxB1Q` | `Mo93x0fxB1Q` | **Still needed** |
| What If Aliens Are Watching Us? | `rFJoOdQAc9c` | Yes → `youtu.be/Mo93x0fxB1Q` | set in index | **Still needed** |

These three were stuck **Scheduled/Private** after the v02 replace. Fixed to **Public** on 2026-08-03 via Studio CDP.

### Scheduled (leave scheduled — do not force-live)

| Cluster | Count | First slot | Full-film target |
|---------|-------|------------|------------------|
| Aliens 04 | 1 | 2026-08-03 12:30 UK | `Mo93x0fxB1Q` |
| Black hole 01–06 | 6 | 2026-08-05 21:00 UK | `n7CbJrOCnU0` |
| Exoplanets 01–06 | 6 | 2026-08-21 21:00 UK | `b8-X_FyJnHM` |

Index descriptions already include `Watch the full film:` + `youtu.be/…` for all of the above.

### Long-form

| Film | ID | Status |
|------|----|--------|
| Aliens / Fermi | `Mo93x0fxB1Q` | Public |
| Black hole | `n7CbJrOCnU0` | Scheduled (per production-status) |
| Exoplanets | `b8-X_FyJnHM` | In production / upload id present |

## TikTok (`@orbitwithben`)

- **Live cuts present** for Fermi + Distance (grid shows non-scheduled thumbnails).
- **Many future Shorts already scheduled** (exoplanets Aug 21–26, etc.).
- Captions template (ledger / `TIKTOK_EXISTENTIAL_CAPTIONS.json`): existential hook + **`Full film on YouTube.`** (soft CTA, no raw URL spam) — correct.
- **Bio link still wrong:** `youtube.com/OrbitWithBen` (missing `@`). Needs manual Save in Edit profile → `https://www.youtube.com/@OrbitWithBen`.

## Instagram + Facebook (Meta)

- Business Suite composer targets **Orbit with Ben + @orbitwithben**.
- Auto uploader improved (file chooser + caption fill). Latest run: `caption_ok=true` for all 3 live Shorts, status **`unconfirmed`** (Share confirmation flake / leave-page dialog).
- IG Reels grid still dominated by **old non-Orbit posts** — Orbit space Shorts not clearly live yet.
- **Action:** manually finish Share in Meta Business Suite for the 3 uploaded drafts if still open, or re-run:
  ```bash
  python3 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --once
  ```
  after dismissing leave-page dialogs in the CDP window on `:9223`.

## Threads (`@orbitwithben`)

- Branding OK: name, bio, YouTube link, Orbit avatar, intro text post.
- **No Shorts video threads visible** after auto attempts (`unconfirmed`). Module clash with Meta `_sib` fixed.
- Re-run when CDP `:9222` is stable:
  ```bash
  # clear false unconfirmed marks first if needed
  python3 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --once
  ```

## Correct caption / link contract (all platforms)

| Platform | Text | Link behaviour |
|----------|------|----------------|
| YouTube description | `Watch the full film:` + `https://youtu.be/<LONG_ID>` | Hard link |
| YouTube pinned comment | `Full film here → <title>` + URL | Hard link (pending for live 3) |
| TikTok / IG / FB / Threads | Soft CTA **`Full film on YouTube.`** | Profile link carries channel; no URL spam in caption |

## Remaining checklist

1. Pin full-film comments on YT `1HuV8o3gOss`, `dPMJQp2gMNc`, `rFJoOdQAc9c`
2. Fix TikTok bio to `@OrbitWithBen`
3. Confirm Meta Share published all 3 to **both** FB + IG with captions containing `Full film on YouTube.`
4. Post the same 3 video threads on Threads
5. Before each scheduled cluster goes live: pin CTA + related video + Meta/Threads mirror (LaunchAgents should handle after YT Public)

Artifacts: `00_Brand/Channel-Setup/audits/crosspost_live_audit_2026-08-03/`
