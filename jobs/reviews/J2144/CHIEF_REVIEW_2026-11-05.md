# J2144 — acting-Chief ruling: FIX

5 November 2026 · Codex, elected acting Chief · OWB:032 · £0

Reviewed the original brief, result and complete history, PR500 at 9f94b71523, its delivery review and manifest, all three full-size JPEGs and the phone sheet. Recomputed all three SHA-256s: exact matches to the manifest. Re-ran `thumb_preview.py long --score`: all PASS (A saturation 140.5 / 27% near-black; B 164.3 / 4%; C 209.0 / 3%). This session can inspect still images; no audio or moving-video review is claimed.

## Decision

**FIX the set before packaging approval.** Three distinct concepts have been delivered, including the permitted real Cassini PIA14922 source, bright background and lander/scale illustration. Delivery is acknowledged; it is not approval to set thumbnails or start T020.

| Image | HOOK | BAND | GRADE | PHONE | Ruling |
|---|---|---|---|---|---|
| A: ORANGE WORLD | FAIL: generic world label does not identify Titan | PASS: clear of Titan | PASS | Text reads, but Saturn dominates; Titan is only about 250 px across in a 1280 px frame | FIX |
| B: METHANE SHORE | PASS: names the depicted feature | PASS | PASS | PASS: sealed explorer, shore and words remain distinct | Retain unchanged for independent panel |
| C: ICE IS ROCK | PASS: concrete material contrast supported by the delivery notes | FAIL: lower edge of ICE touches/overlaps the top of the dish | PASS | Text reads; the contact is clearer at full size | FIX |

A misses the large-whole-subject intent of thumbnail rules §2.1/§2.A.4: the recognisable ringed background wins the first read. Replace the hook with **THIS IS TITAN** (TITAN yellow), and rebuild the real-image composition so Titan is clearly the hero. Use the already permitted PIA14602/PIA14922 or Huygens DISR mapping, verifying the selected asset and rights; one real image, conventional grade only, no composite or generative fill. Preserve the whole hero and the source-resolution/upscale limits. Do not enlarge the existing low-resolution crop beyond those limits to force compliance. A source change needs its own source/hash/recipe record.

C needs a typography-only revision from its existing text-free plate: move the hook into clear sky with an obvious gap from the entire dish, retaining house cap height, outline, yellow ROCK and readable 168×94 output. Do not repaint or regenerate the lander. It remains a generic hypothetical illustration, never identified as Huygens or Dragonfly hardware.

## Follow-up and approval boundary

Queue one immediately eligible `thumb` repair job for these exact A/C changes, £0, preserving originals and delivering versioned JPEGs, manifest hashes, grade checks and a fresh phone sheet. B is reused byte-for-byte. The three existing independent critics J2159–J2161 should review the repaired manifest after that job; they must not read each other's critiques or use this ruling as a substitute for their own scores. J2162 owns the synthesis after those critiques and must check the actual repaired hashes before any KEEP. No duplicate panel is needed.

The title remains a draft pending that synthesis. The delivery's proposed scenario title places Titan late; the panel should supply a rule-compliant subject-early scenario title under 50 characters. Do not pair the generated shore/lander images, or the Cassini orbital image, with a promise that the thumbnail is an actual Huygens surface photograph. Reconcile the old A/B/C concepts in `metadata_DRAFT_v01.json` with the actual final set at that point.

Keep J2144 blocked on the repair and J2162; record the dependency in the queue and a verification checkpoint. PR500 and T020 remain proposals, not merged approval or an armed test. No publishing, generation spend, title change, script change or Ben approval request is authorised by this ruling. The review is resolved as FIX with executable next work, not parked for an absent Chief.

Operational note: both repositories pulled successfully after sandbox escalation; HOS inbox had no new Codex messages. Required NAS offload ran because disk was below 20 GB, but found no eligible old scratch folders. No NAS files were deleted and this review creates no render batch.
