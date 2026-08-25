# Omni long-form playbook

**Locked:** 2026-08-16 after Europa v02 · Last Star v11 · BH v09 · AW v05 · Fermi v20.
**Intent:** Build every future Orbit long in this format. Reiterate when QA teaches a better rule. Do not silently revert to Europa v01 broadcast polish.

Cursor rules: `orbit-omni-longform-playbook.mdc` · `orbit-longform-open-end-affiliate.mdc` · `orbit-omni-section-qa.mdc` · `orbit-cutscene-no-reuse.mdc` · `orbit-shorts-punch-first.mdc` · `orbit-character-consistency.mdc` · `orbit-affiliate-named-in-film.mdc`

## Why this format

- Minute-by-minute QA catches twins, env lies, and floaty Orbit before they compound.
- Omni Flash + native SFX under Ben Orbit Narrator reads as a character *in* the world.
- Soft A/V joins keep the soundtrack continuous; freeze-pad looks broken.
- Picture-first open + Studio end screens + one named-book `/go/` is the locked later standard. Brand sting first and baked like/subscribe outro are retired.

## Why (16 Aug 2026 Studio)

Live channel, last 28 days — do not invent AVD / CTR / long-form retention on top of this:

- Shorts: **759 views** · **28.8% stayed / 71.2% swiped**. Three Suns loop is the rewatch outlier.
- Longs: **21 views / 28d**. YouTube: not enough data for audience-retention curves.
- Do **not** claim a measured long-form first-30s drop.
- Titles are not the bottleneck (already 86–98).

## End-to-end steps

### A. Gate (unchanged)

Growth System v2 · topic score · cluster plan · vidIQ audit · script ≥90 · `gate:episode` PASS.

### B. Part loop (~1 min each)

1. Write part script (VO-literal journey beats table).
2. TTS → `02_Voiceover/parts/` (Ben Orbit Narrator lock).
3. Plate plan JSON: ~8–10 unique ~8s Omni takes; tag `env: underwater|surface|space`.
   **≥2 of them pure scenery — no Orbit** (the object VO names). They cut fine in the film and
   they are the only native source of scene-first Shorts covers; all-Orbit minutes forced
   parent-film cover rescues on 25 Aug 2026 (`TITLE_THUMBNAIL_FORMULA.md`).
4. Generate Omni Flash (Flow) with Orbit identity lock; archive rejects; bump `v0N`.
5. Assemble: paired `xfade` + `acrossfade`; Omni SFX under VO (~0.18–0.2); water bed only underwater.
6. Picture QA (start/mid/end twin + face spot-check). **Stop and check with Ben.** Do not start the next minute until he UAT-passes this one. Then `PART0N_LESSONS.md` → next part.

### C. Broadcast polish (locked later standard)

1. **Open:** first 3 seconds = strange picture only. No Orbit, no logo, no title, no “ORBIT / Stories from the sky”. Orbit after ~8s. Curiosity by 5s, stakes by 15s, journey by 30s — in the **script**, not a title card. Do not hard-cut A/V through a leftover sting (chops mid-word).
2. Chapter cards for mid-film acts only (locked stills — **never** Ken Burns on text). No chapter card on the open.
3. Soft-join approved part roughs in story order.
4. **Outro:** strip baked like/subscribe VO and graphics. Hold last real picture **10s** for official YouTube Studio end screens (Subscribe + next film when an id exists). Soft spoken CTA only if it is not a shop read.
5. **Affiliate (long only):** one named product late, after the wonder line — VO + on-screen 4–6s (not a shop card). URL only in the description: `https://orbit-content-ops.vercel.app/go/{slug}`. Do not bolt a book on to unlock a link. Do not name telescope / LEGO / Brilliant unless the film is about them and the door is live.
6. Export → `09_Final-Export/<slug>_broadcast_v0N.mp4`. Verify picture-first open, 10s end hold, A/V locked. Recut = new filename + new YouTube id.

### D. Shorts cluster (4–8)

1. Punch-first cuts **~22–28s** from locked **part roughs** (not chapter silence).
2. Open on the picture; keep the loop; captions the whole way; Thursday film title on screen.
3. Strongest fact/question in 0–1.5s; curiosity-gap end; full-film CTA only. **Zero** `/go/` or shop URLs on Shorts.
4. Abort if any Short ≥40s.
5. Package `10_Shorts/` + `SHORTS_UPLOAD_INDEX.json` when scheduling.
6. **Covers:** scene-first 9:16 per `TITLE_THUMBNAIL_FORMULA.md` — scored frame pick
   (`tools/build_scene_first_short_covers.py`), parent-film frame when the Short is
   Orbit-dominated (`tools/build_covers_from_parent_episode.py`), uploaded via **Studio
   desktop only** (`tools/upload_shorts_covers_studio.py`; the Data API cannot set Shorts
   covers, and Studio caps custom-thumbnail changes per ~24h).

## Hard locks

| Lock | Rule |
|------|------|
| Picture flatten | One VO idea → one literal image. When VO and picture disagree, picture is wrong. Orbit *in* the scene, not a sticker. Mute the VO: the beat should still read. At most **one** Orbit + distant-remnant hang per minute (Neutron Star Part 02, 17 Aug 2026). |
| oneVideoOneUpload | Recut = new id. Leave old live until new is public, then unpublish. Do not reuse ids. |
| Length | Aug 13 lock: **~18–25 min** documentary. Do not silently revert to 8–12. Older `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` and `templates/PRODUCTION_CHECKLIST_V2.md` still say 8–12 — ignore that line. |

## Hard rejects

| Reject | Why |
|--------|-----|
| Brand intro / logo / title card in first 3s | Kills the strange-picture open |
| Baked like/subscribe VO or graphic | Studio end screens own the last 10s |
| Freeze-pad / scenery loop | Broken / against cutscene rules |
| Twin Orbit / second face / blank white eyes | Character break |
| Formula corner-approach plate (Orbit in a corner, destination opposite, fly toward it — repeated) | Not VO-literal; feels like a template, not a film |
| Orbit + distant remnant as the default plate | Pretty wallpaper under clever VO — not an episode |
| Bubbles in vacuum/surface | Env lie |
| Clipper underwater | Identity/env break |
| Zoompan on title/chapter text | Glyph vibration |
| ≥40s Shorts | Retention evidence |
| `/go/` or shop URL on a Short | Full-film CTA only |
| Shop-read CTA / bolted-on book | Affiliate only if named in *this* cut |

## Reference assets (later standard)

- Europa v02: `…/006_…/09_Final-Export/europa_v02_HAND_OPEN_END_UPLOAD.mp4`
- Last Star v11 · BH v09 · AW v05 · Fermi v20: `*_OPEN_END_UPLOAD.mp4` in each `07_Edit-Project/01_Masters/`
- Lessons: `…/006_…/07_Edit-Project/PART01_LESSONS.md` … `PART08_LESSONS.md`
- v01 (`europa_broadcast_v01.mp4` + brand intro/outro) is the **retired** polish — do not copy forward.

## Change control

When a future episode improves the bar: update this file + the matching `.mdc` rules in the same PR/commit, and note the episode ID + date. Do not fork a silent second standard.
