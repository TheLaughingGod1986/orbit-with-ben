# Vertex Omni FAIL — CoS run #7

Tried Vertex Free Trial only (`gen-lang-client-0538779324`, `us-central1`). No AI Studio prepay. No top-up.

## Clips
| Clip | Status |
|---|---|
| `omni_orbit_tumble_v05` (Ben 11:18 tumble) | FAILED after 3 retries × 2 models |
| `omni_bare_orbit_v05` (small Orbit facing bare Saturn) | FAILED after 3 retries × 2 models |

## Exact error / model IDs
- Models: `gemini-omni-flash-preview`, `gemini-omni-1.1-flash-preview`
- Every attempt: `InternalServerError` — `Error code: 500 - {'error': {'message': 'Internal error encountered.', 'code': 'api_error'}}`

## Fallback
Tumble: keep prior `veo_orbit_tumble_v03_fallback_0-3s.mp4` (WAIT Ben — §6 FAIL on full Veo tumble already recorded). Bare Omni: no clip.

Open/ice: stopped after 2 fails each — now edit-built as v06 (Ben 12:00 path B).
