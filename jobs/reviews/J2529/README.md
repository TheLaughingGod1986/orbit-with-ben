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

### Batch 02 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T01:20Z` – `01:36Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch02-20261112T0120Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch02-20261112T0120Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_02_RECEIPT.json` (`archive_v01_pass1/batch-8dedd0f6f644.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_02_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `1,000 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`):** `9,940 → 9,840 → 9,740 → 9,640 → 9,540 → 9,440` (`0` pending charges; remaining `HOS013_PASS1` reservation `5,600`; headroom `9,440 - 5,600 - 800 = 3,040 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P1:04b_drawer_unlock` | `P01_04b_drawer_unlock_t1.mp4` | `90963509575e23d5cc0f5ca6ea8541b75e5c21fb8ca7fbb06d4ee6772f4064b6` | `340f21fd05d6361e6c8fbacd5830c1eaf8e723d26d11daa7e9890d1c411d42aa` | `64d7aac34b91f64ff0e2971e8cc6bc2000bf465b0fe0edf6e994cbbc7921794a` | `9,940 → 9,840` | `PENDING_REVIEW` (`keep: false`) |
| `P1:05a_museum_cases` | `P01_05a_museum_cases_t1.mp4` | `36dc0c611c7ffa4dc1b36f093fca8f8d42ef88bc5101b238d1364ef2bca690e9` | `2844329f95c01d27451fc7a7a80a011757e2ea1a726751778f3ef9793a5992dc` | `50e3e6e85c21a6a2db2ce99e62d026039326337e53d22dba98d98e1ae2cbd46a` | `9,840 → 9,740` | `PENDING_REVIEW` (`keep: false`) |
| `P1:05b_museum_plaques` | `P01_05b_museum_plaques_t1.mp4` | `e1b4148a8fdb466ea7ed74b214d9b417a4d352ca5358e3541919660276bd73e2` | `9ff6b8f946b973c90d34c6e3d44263bc0b46cc9442b8c51c7062670ce6aefe7c` | `eba80f457b8fe9bb1b3f3da78dca1dceb04cfdffc47291847915344f277a744d` | `9,740 → 9,640` | `PENDING_REVIEW` (`keep: false`) |
| `P1:06_padlock_shut` | `P01_06_padlock_shut_t1.mp4` | `c4d2efca6ce54ea72f2610869d00d5a08c794adc601ab9a8e735564ce5fa93ad` | `82cf3af45e6f4bcc3032a7f49d2aa50c01d5d528b4700d5b2537eac92595d390` | `4967e6d869cbdb1efc1cb9481986cab55401705174ea57b53e58b92779902292` | `9,640 → 9,540` | `PENDING_REVIEW` (`keep: false`) |
| `P1:07_darwin_1837_desk` | `P01_07_darwin_1837_desk_t1.mp4` | `944902b89eaa7e78bd45a79307bfe337729d55e8cff9cf45cc25b5f24bdbb863` | `87e61f0eea8705a30bb520f9fe98e44f95e706555de617859151e18b309dde63` | `59f59941661973ba184a8e079a0a2e97bc0bcdfdb5a968ab04eee34128092c34` | `9,540 → 9,440` | `PENDING_REVIEW` (`keep: false`) |

### Batch 03 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T03:25Z` – `03:40Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch03-20261112T0325Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch03-20261112T0325Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_03_RECEIPT.json` (`archive_v01_pass1/batch-23252f982f89.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_03_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `1,500 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`):** `9,440 → 9,340 → 9,240 → 9,140 → 9,040 → 8,940` (`0` pending charges; remaining `HOS013_PASS1` reservation `5,100`; headroom `8,940 - 5,100 - 800 = 3,040 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P1:09_wallace_hut_split` | `P01_09_wallace_hut_split_t1.mp4` | `64ae099145dfa1c34279a8f1933dcce5cd870e7fc002bc9e1b144343d54882f0` | `c3035db5455ae55ff211a5d2f7758d49188e1c354cce911898b0d69dad377af5` | `5ef47179c1723133770090bdf76d0ec7b06949123838b93c6729b3ab3778f414` | `9,440 → 9,340` | `PENDING_REVIEW` (`keep: false`) |
| `P1:11_beagle_cabin_explorer` | `P01_11_beagle_cabin_explorer_t1.mp4` | `923bed9d7cd90e2529405d0ed87b4a769f1037efaa531d45d95f4da3f69b9f10` | `9aaa712167f9ecd77ce71eaedd2aec07be45c13750d69cca96040f8a5d7eb8de` | `e317cabeb06f8b6229ff278804c464ffef2d30cbd6d165222e14900f1d324c9f` | `9,340 → 9,240` | `PENDING_REVIEW` (`keep: false`) |
| `P2:02_galapagos_beach_myth` | `P02_02_galapagos_beach_myth_t1.mp4` | `d3b2c39de4cc1a47140d353d33185993cada504d5a353a5d38669672b1a2aab7` | `0f751ebbf6edc54cc8f8fee6fb90641d194b392d26bbb93e28be749251dc340f` | `589e53755ae051e606fb328df8004657a0f22f7fbe6ebc669e15efe66e7c63e6` | `9,240 → 9,140` | `PENDING_REVIEW` (`keep: false`) |
| `P2:03_unlabelled_bagging` | `P02_03_unlabelled_bagging_t1.mp4` | `8813d267291dff799d545a15cb32c684d8b0545e4be06511d077a951e9fe52ca` | `703c03faae35428a273a1643bd5a19f1639b6ffa64021a0c4c0f714e4ed858bf` | `026f621f6c2ba6db24e5d7e2760228f3c750bc39321bf13194948ddc2d8ac5ab` | `9,140 → 9,040` | `PENDING_REVIEW` (`keep: false`) |
| `P2:04_blank_tags_row` | `P02_04_blank_tags_row_t1.mp4` | `fb29ad16a297f8bb32eb06eb17099f64b6927a6d38c20a8dc734686b90005fd6` | `db1949f444947d14e9a7bd4e95c76f6940dcb041ce3e608e6ca546955304defe` | `5855af33696939da05ba23c662004c883f511fd5e0a4c19977b199b25e44fb94` | `9,040 → 8,940` | `PENDING_REVIEW` (`keep: false`) |
