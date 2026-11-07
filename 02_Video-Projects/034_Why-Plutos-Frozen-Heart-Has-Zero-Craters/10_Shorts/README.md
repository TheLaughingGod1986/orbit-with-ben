# 034 Shorts (`10_Shorts/`)

- **Plan in force:** [`SHORTS_PLAN_v01.md`](./SHORTS_PLAN_v01.md) (delivered in `J2360`, reconciled to locked `pluto_frozen_heart_script_master_v03.md`, `pluto_frozen_heart_vo_v03.wav`, and `J2359`'s Chief shot-list ruling).
- **Parent Long:** `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` (*Why Pluto's Frozen Heart Has Zero Craters*).
- **Build Jobs (Held until Chief plan approval + `J2361` → `J2362` picture/music/SFX delivery):**
  - `J2319`: Short 1 (Test A Opening Short, default slot `2026-12-21 11:30Z`, `30–38 s` window).
  - `J2320`: Short 2 (Keeper Question Short, default slot `2026-12-23 11:30Z`, `22–27 s` window, `55–65` words, `OWB-2026-11-E1` pacing locks: `Cut 1 ≤ 2.8 s`, `Cut 2 ≤ 4.8 s`, later plates `≤ 4.0 s`, loop tail `< 1.2 s`, zero end card/CTA).
- **Mandatory Gates Before UAT:**
  1. `python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD`
  2. `python3 scripts/picture_qa.py <short.mp4> --cuts <cuts.json> --pool <pool.json> --out-dir <qa_dir>`
  3. `python3 scripts/polish_gate.py <short.mp4>`
  4. `python3 scripts/sfx_kit.py level --vo <vo.wav> --sfx <sfx.wav> --bed <bed.wav> --minutes 0.45`
  5. `python3 00_Brand/Channel-Setup/tools/thumb_preview.py short <frame0.jpg> --out <preview.jpg>`
  6. Demonstrated `audio_input` splice check and `moving_video_input` motion check (delegated separately if the building worker lacks those modalities), followed by Ben's final UAT watch.
