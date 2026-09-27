# Orbit Shorts — on-screen text style (TikTok / YouTube Shorts)

**Status:** Canonical for vertical Shorts overlays  
**Updated:** 2026-08-02  
**Code:** `TikTok/auto/onscreen_captions.py`  
**Benchmarks:** `SPACE_DOC_CAPTION_BENCHMARKS.json`

---

## Why this style

Space / mind-doc shorts that retain (e.g. **finalverdict**, **Life Laps**, **Actual Space**, **mindlapse**) keep the picture cinematic and put **1–3 punchy words** on screen, synced to VO — not a branded title card stack.

Orbit’s old Shorts overlays used ALL-CAPS white headlines + top/bottom chrome + a white frame. That reads “YouTube end-card,” not “stop-the-scroll doc short.”

---

## Orbit lock (mirror finalverdict)

| Trait | Spec |
|-------|------|
| Case | **lowercase** only |
| Font | Heavy sans — `Arial Black` (fallback `Arial Bold`) |
| Colors | Accent yellow `#FFE600` · white `#FFFFFF` |
| Emphasis | Alternate yellow / white by beat or by line |
| Words / beat | **1–3** (never a full sentence) |
| Position | Optical center, slightly above mid (TikTok UI safe) |
| Effects | Soft black drop shadow + thin dark stroke (`#0A0C12`) |
| Chrome | **None** during the idea — no `ORBIT • ROLE`, no series footer, no white frame |
| CTA | Soft lowercase end line only (`full story on youtube →`) — no pill card |

### Beat pattern

```
0.0–1.5s   MONSTER HOOK (yellow) — strongest phrase first
1.5–4.0s   payoff / mechanism (white)
4.0–8.0s   stacked 2–3 lines if needed (VO-synced when Scribe map exists)
…          then picture + VO breathe
last 4s    soft CTA (white, smaller): watch the full film →
```

Punch-first + VO sync: `onscreen_captions.punch_first` / `align_phrases_to_words`.  
Generate maps: `TikTok/auto/_sync_shorts_caption_beats.py` → `10_Shorts/07_Caption-Sync/`.

Funnel ops: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` §9 (metrics · monster-hook order · YT then TikTok +1h).

### Copy rules

- Wonder tone, not fearbait (Orbit brand).
- No ALL CAPS. No emoji on the burn-in.
- Prefer visceral nouns/verbs: `glass rain`, `never come back`, `where is everybody?`
- TikTok **description** still carries hashtags + “Full film on YouTube.” — that is separate from burn-in.

---

## What we observed (benchmarks)

| Account | Followers / signal | On-screen habit |
|---------|-------------------|-----------------|
| **finalverdict** (user reference) | Strong save rate on mind-doc posts | Bold sans · yellow + white · lowercase · 1–3 words · center |
| **life_laps_official** | ~594K · multi‑M likes | Lowercase · centered · minimal chrome |
| **actualspace1** | Solid space niche | Short VO-synced phrases · dark cinematic beds |
| **mind_lapse1** | ~42K · high like density | Word-by-word kinetic captions |

**Note:** `@orbitwithben` shows **0 Following** on web/Studio. Phone follows (including private accounts) are not visible here — style lock is driven by your screenshots + public niche samples above.

---

## Builder usage

Per-episode `_build_*_shorts_v02.py` scripts import `onscreen_captions` and pass `beats` + optional end CTA.

Preview frames:

```bash
python3 00_Brand/Channel-Setup/TikTok/auto/_render_caption_style_previews.py
```
