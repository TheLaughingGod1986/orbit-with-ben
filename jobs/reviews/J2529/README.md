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

## Batch Receipts

### Batch 01 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-11T23:20Z` – `23:37Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch01-20261111T2320Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch01-20261111T2320Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_01_RECEIPT.json` (`archive_v01_pass1/batch-60200ef91167.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_01_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`):** `10,440 → 10,340 → 10,240 → 10,140 → 10,040 → 9,940` (`0` pending charges; remaining `HOS013_PASS1` reservation `6,100`; headroom `9,940 - 6,100 - 800 = 3,040 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P1:01_study_beaks` | `P01_01_study_beaks_t1.mp4` | `37a68217244b397eef0cdcbdfb0dfbb07fe7750f200134c5c400790e724c35c3` | `f369b1b6e225f65c97e99913b66912082948f7983de99f076779cfb0598ee5a3` | `7433d35b21b9d7a72aef520c598293e52681a1df1a2ad1462f76ba5e89a8e314` | `10,440 → 10,340` | `PENDING_REVIEW` (`keep: false`) |
| `P1:02_drawer_lock` | `P01_02_drawer_lock_t1.mp4` | `60dc3d6c432cc801205c785a4a7654d32327bdedfd3c6d84cf0d93bc0a90c12d` | `93491c6f5b43c420949fef2af687878b12b74ce087e0506ce8ec8f134e2ffb27` | `cfcdf75b205d46cc7aa6e11457735cffe3c6264c46a215a8de21b5de4d2f8bf2` | `10,340 → 10,240` | `PENDING_REVIEW` (`keep: false`) |
| `P1:03a_unlabelled_birds` | `P01_03a_unlabelled_birds_t1.mp4` | `ab1982700cf5c959348716060fa63037fe76d7e93b29db5483c46a0a7b1112e9` | `a83ae6e4c50469e3812d943ad1eeb8adc4788a580fb44e354cd3fcab66734c7a` | `187d7db3db4d183afabfda55157ba3bd76ea0a519c4dab29d2f2dcad36bef641` | `10,240 → 10,140` | `PENDING_REVIEW` (`keep: false`) |
| `P1:03b_malay_packet` | `P01_03b_malay_packet_t1.mp4` | `3545dfee7de7653831c33da0c0e57d92cac57da78cdc62151d1c4a841398756b` | `f25aeed5b4da439bb3e0b1e779fa34d2954a11ac5d4acb0c1ffc8dccebff63a7` | `f714778260adc3bc3a2e4692eea073229278b7dd633a86511b045a3d4d6cd8ea` | `10,140 → 10,040` | `PENDING_REVIEW` (`keep: false`) |
| `P1:04a_packet_seal` | `P01_04a_packet_seal_t1.mp4` | `594d1e30140c7d3f9a6d60a565af38ba327521659bc8d7de2ec6a050e510d07f` | `032a963b978edeacef6e1239dae433ea3ebc694969be7acf167d0cdfd6bbc224` | `6b861b83b64c3f0b909a59ed5d8ffd95cdbdab4a695f99926adb866302b4a5bd` | `10,040 → 9,940` | `PENDING_REVIEW` (`keep: false`) |
