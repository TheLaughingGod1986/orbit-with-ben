# J1204 Uranus v04/v05 source probe — 29 Oct 2026

Chief FIX reopen (16:15Z): one no-spend source pass; assemble only if silent 2.7 s crop reaches f0diff ≥1.50 at 1.0×, ≤2.35× upscale, recognizable Uranus.
URL: https://svs.gsfc.nasa.gov/20390/ — NASA GSFC Conceptual Image Lab (Walt Feimer, Jenny McElligott). Public domain.

## Probe table (silent 2.7 s centre 9:16 crop → 1080×1920)

| File | title | t0–t1 | f0diff | black% | mean | p95 | subject | verdict |
|---|---|---|---|---|---|---|---|---|
| `Shot4_1k_mp4.mp4` | Uranus Beauty Pass 1 | 0.00–2.70 | **0.21** | — | — | — | Uranus+rings | FAIL f0diff |
| `Shot4_1k_mp4.mp4` | Uranus Beauty Pass 1 | 1.15–3.85 | **0.35** | — | — | — | Uranus+rings | FAIL f0diff |
| `Shot4_1k_mp4.mp4` | Uranus Beauty Pass 1 | 4.50–7.20 | **0.78** | — | — | — | Uranus+rings | FAIL f0diff |
| `Shot4_1k_mp4.mp4` | Uranus Beauty Pass 1 | 7.00–9.70 | **0.37** | — | — | — | Uranus+rings | FAIL f0diff |
| `CloudBRoll_1k_mp4.mp4` | Swirling clouds on Uranus | 0.00–2.70 | **2.37** | — | — | — | clouds only (no disc/rings) | PASS f0diff / REJECT subject |
| `CloudBRoll_1k_mp4.mp4` | Swirling clouds on Uranus | 0.50–3.20 | **3.27** | — | — | — | clouds only (no disc/rings) | PASS f0diff / REJECT subject |
| `CloudBRoll_1k_mp4.mp4` | Swirling clouds on Uranus | 1.00–3.70 | **3.48** | — | — | — | clouds only (no disc/rings) | PASS f0diff / REJECT subject |
| `CloudBRoll_1k_mp4.mp4` | Swirling clouds on Uranus | 2.00–4.70 | **3.48** | — | — | — | clouds only (no disc/rings) | PASS f0diff / REJECT subject |
| `Shot16_1k_mp4.mp4` | Uranus fly by | 0.00–2.70 | **0.26** | — | — | — | Uranus+rings | FAIL f0diff |
| `Shot16_1k_mp4.mp4` | Uranus fly by | 1.00–3.70 | **0.66** | — | — | — | Uranus+rings | FAIL f0diff |
| `Shot16_1k_mp4.mp4` | Uranus fly by | 2.00–4.70 | **2.18** | — | — | — | Uranus+rings | used v04 (later FAIL polish) |
| `Shot16_1k_mp4.mp4` | Uranus fly by | 4.00–6.70 | **2.17** | — | — | — | Uranus+rings | PASS candidate |
| `Shot5_1k_mp4.mp4` | Voyager flies by | 0.00–2.70 | **0.08** | 45.2 | 78.28 | 189.6 | Voyager craft (slow) | FAIL f0diff |
| `Shot5_1k_mp4.mp4` | Voyager flies by | 0.50–3.20 | **0.05** | 46.6 | 79.33 | 190.4 | Voyager craft (slow) | FAIL f0diff |
| `Shot5_1k_mp4.mp4` | Voyager flies by | 1.00–3.70 | **0.05** | 46.5 | 79.31 | 190.6 | Voyager craft (slow) | FAIL f0diff |
| `Shot5_1k_mp4.mp4` | Voyager flies by | 2.00–4.70 | **0.08** | 46.6 | 79.34 | 190.6 | Voyager craft (slow) | FAIL f0diff |
| `Shot_5_AltVoyager_1k_mp4.mp4` | Voyager flies by Uranus v2 | 0.00–2.70 | **0.01** | 49.9 | 44.38 | 121.4 | Uranus+rings | FAIL f0diff |
| `Shot_5_AltVoyager_1k_mp4.mp4` | Voyager flies by Uranus v2 | 1.00–3.70 | **0.01** | 49.9 | 44.36 | 121.3 | Uranus+rings | FAIL f0diff |
| `Shot_5_AltVoyager_1k_mp4.mp4` | Voyager flies by Uranus v2 | 3.00–5.70 | **0.03** | 49.9 | 44.32 | 121.4 | Uranus+rings | FAIL f0diff |
| `Shot_5_AltVoyager_1k_mp4.mp4` | Voyager flies by Uranus v2 | 5.00–7.70 | **0.02** | 49.9 | 44.32 | 121.4 | Uranus+rings | FAIL f0diff |
| `Shot_5_AltVoyager_1k_mp4.mp4` | Voyager flies by Uranus v2 | 8.00–10.70 | **0.02** | 50.0 | 44.31 | 121.4 | Uranus+rings | FAIL f0diff |
| `Shot6_1k_mp4.mp4` | Voyager flies by Uranus' rings | 0.00–2.70 | **1.06** | 76.7 | 15.89 | 88.2 | Uranus+rings | FAIL f0diff |
| `Shot6_1k_mp4.mp4` | Voyager flies by Uranus' rings | 1.00–3.70 | **0.39** | 63.8 | 24.08 | 92.8 | Uranus+rings | FAIL f0diff |
| `Shot6_1k_mp4.mp4` | Voyager flies by Uranus' rings | 2.00–4.70 | **0.39** | 60.8 | 24.31 | 86.3 | Uranus+rings | FAIL f0diff |
| `Shot6_1k_mp4.mp4` | Voyager flies by Uranus' rings | 3.00–5.70 | **0.53** | 64.0 | 20.62 | 78.8 | Uranus+rings | FAIL f0diff |
| `Shot8_1k_mp4.mp4` | Uranus and its moons | 0.00–2.70 | **11.91** | 74.3 | 21.68 | 119.6 | Uranus+rings | PASS f0diff / RISK near-black |
| `Shot8_1k_mp4.mp4` | Uranus and its moons | 1.00–3.70 | **12.64** | 64.5 | 32.85 | 136.3 | Uranus+rings | PASS candidate |
| `Shot8_1k_mp4.mp4` | Uranus and its moons | 2.00–4.70 | **9.55** | 57.5 | 45.95 | 154.7 | Uranus+rings | PASS candidate |
| `Shot8_1k_mp4.mp4` | Uranus and its moons | 4.00–6.70 | **3.93** | 47.2 | 67.74 | 167.8 | Uranus+rings | PASS candidate |
| `Shot9_1k_mp4.mp4` | Beauty shot of Uranus' rings | 0.00–2.70 | **4.45** | 59.3 | 31.24 | 122.3 | Uranus+rings | PASS candidate |
| `Shot9_1k_mp4.mp4` | Beauty shot of Uranus' rings | 1.00–3.70 | **4.84** | 56.1 | 33.89 | 121.6 | Uranus+rings | PASS candidate |
| `Shot9_1k_mp4.mp4` | Beauty shot of Uranus' rings | 2.00–4.70 | **4.74** | 52.2 | 37.21 | 122.3 | Uranus+rings | PASS candidate |
| `Shot9_1k_mp4.mp4` | Beauty shot of Uranus' rings | 4.00–6.70 | **3.38** | 45.6 | 41.82 | 118.6 | Uranus+rings | SELECTED for v05 |
| `Shot18_1k_mp4.mp4` | Storms on Uranus | 0.00–2.70 | **2.43** | 23.8 | 78.94 | 150.0 | clouds only (no disc/rings) | PASS f0diff / REJECT subject |
| `Shot18_1k_mp4.mp4` | Storms on Uranus | 1.00–3.70 | **2.08** | 23.8 | 61.4 | 105.3 | clouds only (no disc/rings) | PASS f0diff / REJECT subject |
| `Shot18_1k_mp4.mp4` | Storms on Uranus | 2.00–4.70 | **2.04** | 24.0 | 54.49 | 91.9 | clouds only (no disc/rings) | PASS f0diff / REJECT subject |

## Assemblies this run
- **v04** Shot16 open 2.00–4.70: f0diff **2.2 PASS**, but polish/picture_qa/loop FAIL (near-black / split gutter / black frame 84%). sha `87cf21c428c3a92ff49147c29226e707d73d31f6fd4212157517b1aab03b818a`. UAT `standalone_shorts_uranus_v04`.
- **v05** Shot9 open 4.00–6.70 assembling (silent probe f0diff 3.38, mean 41.8, Uranus+rings). Preserve v02/v03/v04.

## Rejects
- Shot4 Beauty Pass: max natural f0diff ~0.8 (Chief already refused 3×).
- CloudBRoll / Shot18: motion OK, not a recognizable Uranus disc+rings open.
- Shot5 / AltVoyager: almost static on gate metric.
- Shot6: f0diff <1.50.

