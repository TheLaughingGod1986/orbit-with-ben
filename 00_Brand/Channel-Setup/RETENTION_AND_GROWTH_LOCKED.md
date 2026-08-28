# Retention & growth — locked going forward (Orbit with Ben)

**Locked:** 2026-08-06 · **Growth System v2**  
**Applies to:** every Short + every long from **next new production after current ships**  
**Success:** Impressions · CTR · AVD · APV · session time · returning viewers · Browse / Suggested / Search  

Canonical system: `YOUTUBE_GROWTH_SYSTEM_V2.md`  
Detail: `docs/ORBIT_GROWTH_PLAYBOOK.md` · memory: `docs/RETENTION_LEARNINGS.md`  
Pre-build: `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` · story/VO: `LONGFORM_STORY_AND_VO_PICTURE_GATE.md`  
Gates: script reviewer (≥90) · `templates/PRODUCTION_CHECKLIST_V2.md`

---

## P0 — Retention

1. **Cold open** — curiosity **0–5s** · stakes **~15s** · journey clear **~30s**. No logo/welcome/history/definition open.  
2. **Long open ≤15–20s to first paradox** — story tension before explanation.  
3. **Structure** — Question → Danger → Story begins → Explain while story continues → Escalation → Ending.  
4. **Framework** — Hook → Question → Escalation → Discovery → Payoff → Bigger question.  
5. **World does the science** — Orbit appears in **1–2** inquisitive / story-narrative beats only (not wallpaper on every plate).  
6. **Curiosity reset every 30–60s** — chapter card / new Q / number / turn.  
7. **VO–picture lock** — show or act the narration; no generic filler under specific VO.  
8. **One teach-point per chapter** — 4–6 film-act chapters.  
9. **Runtime** — **7–9 min NOW**; expand to 15–20–30 only after an 8-min film gets real impressions and hold past ~5 min.  
10. **Payoff before outro** — answer the open loop; soft CTA only at the end.  
10b. **Picture path (27 Aug 2026)** — Google AI Studio: **Veo** for world · **Omni only** when Orbit must move · stills first · 2–3 Veo Fast money shots · mute Veo audio · **never Omni the whole film** · no Kling.

## P0 — Growth

11. **Shorts = discovery engine** — **4–8** per long; **22–27s**; picture in 1s · picture thumb no Orbit · exact listing title on screen · CTA that week’s Thursday id · curiosity-gap end.  
12. **Related video pill only** on every Short → that week’s Thursday long (desktop Studio Related). **No new Short pins.** Pin not required when Related is set. Long-form pins stay. Existing live Short pins may stay (do not mass-unpin / remint). See `.cursor/rules/orbit-shorts-related-video.mdc`.  

13. **Pre-build vidIQ audit (blocking)** — keywords · title ≥90 · outliers → then script.  
14. **Script reviewer ≥ 90 / 100** before VO / picture gen.  
15. **Title = one promise** · prefer ≤~60 chars · **no series suffix** on every upload.  
16. **Long thumb = picture + SEA-style hook** — **no Orbit**, no generic CTA. Short thumb = custom picture, **no Orbit**.  
17. **No dead ends** — end screen · cards · long pin · description → another Orbit documentary; Shorts use Related pill only.  
18. **Soft “follow for the next mystery”** at end only — never interrupt the hook.

## P1 — Habits

19. **Weekly scorecard** — impressions / CTR / AVD / APV · traffic mix · Shorts stayed-to-watch · subs.  
20. **Post-upload recommendations** — Content Ops analytics flags weak opens / drops / packaging.  
21. **Series rhythm** — next mysteries feel like “next lesson.”  
22. **Reuse only branding + Orbit kit** — unique story plates per episode.  
23. **No niche pivot under ~1k views** — sample still directional.

## Do not

- Fearbait titles (even if vidIQ scores higher)  
- Stretch Shorts to 45–60s  
- Mid-flight rebuild of shipping episodes for length  
- Meme/movie outlier chasing  
- Schedule thrash during experiment windows  
- Explain-first openings (“What is X?”) before story tension  
- Passive Orbit as corner decoration for the whole film  

---

## Per-episode checklist (quick)

**Before gen**

- [ ] Pre-build vidIQ audit signed off  
- [ ] Script reviewer ≥ 90  
- [ ] Title one promise · no series suffix · thumb matches  
- [ ] 4–6 chapters with teach-points + Orbit-in-scene plan  
- [ ] Cold-open clock (5 / 15 / 30s) written  

**Shorts**

- [ ] 22–30s standalone micro-story  
- [ ] Strongest-fact open · curiosity-gap end  
- [ ] Related video pill → that week’s Thursday long (no new Short pin; pin not required when Related is set)  


**Before publish**

- [ ] `templates/PRODUCTION_CHECKLIST_V2.md` complete  
- [ ] End screen · cards · long pin · description links · Shorts Related pill

**After publish**

- [ ] Import metrics · read recommendations  
- [ ] Log into `RETENTION_LEARNINGS.md` / `SHORTS_EXPERIMENTS.md`  

---

## Agent reminder

Follow `YOUTUBE_GROWTH_SYSTEM_V2.md` + this file + longform VO–picture gate + pre-build vidIQ audit. Prefer these over ad-hoc process changes.

**Cursor hooks (project):**

- `sessionStart` → injects checklist + sets `ORBIT_RETENTION_GATE` env  
- `preToolUse` (Shell) → reminds before Veo/Omni/VO gen-looking commands  

Config: `.cursor/hooks.json` · scripts: `.cursor/hooks/orbit-*.py`  
Primary enforcement remains `alwaysApply` rules in `.cursor/rules/`.
