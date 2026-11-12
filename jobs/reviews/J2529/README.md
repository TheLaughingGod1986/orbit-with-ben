# J2529 ⇄ HOS013_PASS1 — HOS 013 Darwin & Wallace Pass-1 Mint Receipts

## Identity Mapping

- **Queue job / receipts folder / desk reference:** `J2529`
- **Shared Flow ledger reservation identity:** `HOS013_PASS1` (`J2529 ⇄ HOS013_PASS1`)
- **Film:** `HOS:013` (`013_Darwin-Wallace-Evolution`)
- **Authorising Chief rulings:** History of Science desk `#180` comments `6805739027`, `6805898066`, and second ruling `6807600765` (11 Nov 2026)

Any spend row in this window that reads a different reservation, or no reservation, is an immediate stop.

## Scope & Guards

- **Canonical checkout:** `/Users/benjaminoats/YouTube/History Of Science` on `main` (`90711687ce8950c881f0293a8af701d41cd7436f`)
- **Runner:** `02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/_mint_flow_v01_pass1.py` (`40/40` unit tests OK in `tests/test_hos013_pass1_runner.py`)
- **Plan & scope:** `PICTURE_PLAN_v02.json` (`14212379e2132e94766abffba358dea50640329ffc86db4a6c65c221a8897182` / `PASS1_SCOPE_J2499.json`): 66 `Veo 3.1 - Quality` rows at 100 credits (`6,600` cap), 0 Fast, 2 Explorer rows, 14 batches (`13 × 5` + `1 × 1`), `P1:01_study_beaks` first, `P6:08b_darwin_mendel_synthesis` last
- **Explorer reference:** `01_Character/05_Generation-References/hos-explorer-reference-v01.jpg` (`sha256: 24659dc1d761e9371de9411ca8b56cd5ad3e2587674a8cbdf66a3b84e451476d`)
- **Headroom floor:** `--floor 3000` (`--other-reservations 0`) stated explicitly on every launch command
- **Pre-launch dry-run (`DRY_RUN_2026-11-11T2318Z.json`):**
  - Live studio Ultra Flow balance read at `2026-11-11T23:17:40Z`: `10,440` credits (`>= 9,600`)
  - Active reservations: `{}` (`remaining_reservations: 0`, `has_pending_charge: false`)
  - Unposted charges / total liability: `800` credits
  - Projected headroom after `6,600` cap: `3,040` credits (`>= 3,000`)
  - `would_allow_reserve_at_recorded_balance: true`
  - Unarmed `submit` check: refused (`exit 1`)
- **NAS archive:** `/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution/04_Generated-Clips/archive_v01_pass1`
- **Deadlines:** Go/no-go before Thu 12 Nov 2026 13:00 London; no new Create after Thu 12 Nov 2026 18:45 London (reset at 19:13 London).
