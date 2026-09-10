# Shorts open library

First-frame (0.3 s) dHash + Orbit-visor score for every Orbit Short that is live or scheduled. Read and written by `00_Brand/Channel-Setup/tools/gate_shorts_open.py`.

- `library.json` — committed. One entry per YouTube id: `date` (UK air date), `dhash` (64-bit hex), `orbit.visor_frac`, `source` (`yt-dlp_public` · `local_export` · `studio_player_capture` — the last is approximate, ~16 bits off the real file), `status` (`live` · `scheduled` · `retired`).
- `frames/<id>.jpg` — local only (`*.jpg` is gitignored). Re-create with `gate_shorts_open.py fetch/add`.

Workflow: `check` every export before upload → `add` after the upload is scheduled → `status --status retired` when an id goes Private. `compare` prints every pair inside 16 bits.
