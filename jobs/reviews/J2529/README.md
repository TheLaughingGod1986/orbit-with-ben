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

### Batch 04 of 14 — Runner `STOP` Before Browser/Create (`2026-11-12T05:31Z`, `0` Credits Spent)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch04-20261112T0531Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch04-20261112T0531Z.done` (`exit 2`)
- **Exact runner output:** `STOP first pass must start with Part 01`
- **Root cause (read-only; runner, scope, plan, and ledgers untouched):** Batch 03 completed the final 2 rows of Part 01 (`12/12`), so `remaining[0]` for Batch 04 is `P2:05_tortoise_overboard` (`part == 2`). In `_mint_flow_v01_pass1.py`, `next_batch()` (line `1638`) calls `batch_rows(remaining)[0]`, and `batch_rows()` (line `449`) calls `order_rows(remaining)`, which raises `GuardError("first pass must start with Part 01")` at line `403`.
- **Cumulative stop summary (parked for Chief):**
  - **Takes per part (`15 / 66` Quality takes, `GENERATED` / `PENDING_REVIEW`, `keep: false`):** `part_01` `12/12`, `part_02` `3/11`, `part_03` `0/14`, `part_04` `0/12`, `part_05` `0/9`, `part_06` `0/8`
  - **Credits spent:** `1,500` Flow credits (`15 × 100` Quality; `15 × 0` start stills; £0 cash; `0` pending charges; `0` refused takes)
  - **Balance before → after:** `10,440 → 8,940` (`5,100` remaining on `HOS013_PASS1`; `800` historical unposted liability; headroom `3,040 >= 3,000`)

### Batch 04 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T08:18Z` – `08:33Z`, after PR `#564` & Ruling `6818142702`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch04-20261112T0818Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch04-20261112T0818Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_04_RECEIPT.json` (`archive_v01_pass1/batch-b0ff484ec9ae.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_04_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `2,000 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`, post-batch `8,440` re-verified live on CDP `:9222`):** `8,940 → 8,840 → 8,740 → 8,640 → 8,540 → 8,440` (`0` pending charges; remaining `HOS013_PASS1` reservation `4,600`; headroom `8,440 - 4,600 - 800 = 3,040 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P2:05_tortoise_overboard` | `P02_05_tortoise_overboard_t1.mp4` | `15dec197839c6d4314a7b0bdd8abfc5dee3316891c5fc95b1f3a164202be0b6a` | `023bc315d49c12987fad300647530bc75858221014b7bada3b4a00e66360f978` | `839c023d553dc8bcb45bcca613f8aff41902b98d80e912af7e62964fd4efef29` | `8,940 → 8,840` | `PENDING_REVIEW` (`keep: false`) |
| `P2:06a_lawson_jetty` | `P02_06a_lawson_jetty_t1.mp4` | `3ad6f3b95a57e1804a58d8b5f3f5d47731283c98776ad905bb5e7e1b513989d9` | `fd4f0f379dad19c0e4844ac85084a2565e78fc5a8e35b27e3b4bfa583566c8e3` | `27e89c744c12d4a1737a1596e8316c4ee01439d6d42e8f92a7e8b24bea12dcbf` | `8,840 → 8,740` | `PENDING_REVIEW` (`keep: false`) |
| `P2:07_darwin_notebook_wait` | `P02_07_darwin_notebook_wait_t1.mp4` | `a897c9984f49800a59bb991d6461f3883df6a62a7f1bf11249f5c441a8a89ecd` | `353e387d2c21616a40758ad1b1fcec4bb466376468c138c12bf0f61f11559448` | `9915ab0f8787bc2febe26eb4ddeeb518c1f1a77bc9ae0fadb4f092a8d2849f81` | `8,740 → 8,640` | `PENDING_REVIEW` (`keep: false`) |
| `P2:08a_gould_sorting` | `P02_08a_gould_sorting_t1.mp4` | `fa5f78e0cd1a9cbe4da35aa388868ec416ee320d27eaed5c06ea68d130117cd5` | `2ccbd9d13161af8a2e780634bd17fd7c40e4998f8445c66373ead6dcad4b2eda` | `5c01df6668d24a1f02fdbda183ba740b93ef2850b5924e52dce077537b0c668a` | `8,640 → 8,540` | `PENDING_REVIEW` (`keep: false`) |
| `P2:08b_gould_skins_closeup` | `P02_08b_gould_skins_closeup_t1.mp4` | `47fc7ca5445b772b4e1f2201fd5fb5956e1de86bc3d02e4a4f4802473e011318` | `8f52b44f487808c61e9f3b1a3c95636da4a37d82376cc93d04e13aea3f3e18fa` | `d9e0b66054818d4711d31b290032f7253d6677d80fce3b92f6a6e19e88c24249` | `8,540 → 8,440` | `PENDING_REVIEW` (`keep: false`) |

### Batch 05 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T09:18Z` – `09:35Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch05-20261112T0918Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch05-20261112T0918Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_05_RECEIPT.json` (`archive_v01_pass1/batch-e08781d724a5.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_05_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `2,500 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`, post-batch `7,940` re-verified live on CDP `:9222`):** `8,440 → 8,340 → 8,240 → 8,140 → 8,040 → 7,940` (`0` pending charges; remaining `HOS013_PASS1` reservation `4,100`; headroom `7,940 - 4,100 - 800 = 3,040 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P2:10a_explorer_shipmates` | `P02_10a_explorer_shipmates_t1.mp4` | `4c72bdc24dd89a9cfedbc91caa2224b63a3d8231691aea6d597e1adfb4001fce` | `422123ef6d8082dc2fc96919ccbb406ae7648f6bb3f4e3d07603ac6e3febb9f5` | `181bb413f79954c4e45fc7e43b0c61e6e0edb2a1205050f9a8e5d25528499a4a` | `8,440 → 8,340` | `PENDING_REVIEW` (`keep: false`) |
| `P2:11_island_split_vision` | `P02_11_island_split_vision_t1.mp4` | `4d0ae5f4484b699038efe4f864fc3314a1b55a0d28b7ad12d28da7e463c7444f` | `6d6ed4e85753cf4ccdaf1be596600d9b30ce6b9784306fd5cd92125ed52dcd4d` | `e1c37362e6903883a0de0a9d5417f734df43e47de5f2a9fad139ee9645c51038` | `8,340 → 8,240` | `PENDING_REVIEW` (`keep: false`) |
| `P2:12b_tree_question` | `P02_12b_tree_question_t1.mp4` | `7958d7a6ccde9113b76eb7228f616915f41544a3474c37b80de6893a08809269` | `6ba0c1ce058dde5cd5895d38590ba07826750a85b6b40859461d67d6979bf092` | `0568f6da96cda6b793dce5d0cfcad7d23766825369c995f47adec4cae5478367` | `8,240 → 8,140` | `PENDING_REVIEW` (`keep: false`) |
| `P3:02a_malthus_lamplight` | `P03_02a_malthus_lamplight_t1.mp4` | `20f4cb58fab0fdca4e01fee5a530ad924263713bacf1bcaaa523df3d1657a486` | `5564f50e5b760b9e5177fea02e0272b4913c1544b347dd032ec0b1358d2defd9` | `adcf660493e9db3dadb47e961d9a7ebae8a894cb9713d6c3f06b40c21580a6f5` | `8,140 → 8,040` | `PENDING_REVIEW` (`keep: false`) |
| `P3:02b_notebook_d_open` | `P03_02b_notebook_d_open_t1.mp4` | `5ede492e92cdbbf2e5b434ac6994033b60cbce42db14e5563905162b7d17a3d7` | `7e30c700ae4957a5f5342fe1aeee5c4d837d78bae84570536314078847d76a8d` | `8edfcaafd4fdb94d09d9fc370d91df81119289dace71bcbb5d818e5065f1e22a` | `8,040 → 7,940` | `PENDING_REVIEW` (`keep: false`) |

### Batch 06 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T11:18Z` – `11:33Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch06-20261112T1118Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch06-20261112T1118Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_06_RECEIPT.json` (`archive_v01_pass1/batch-90ddad093b92.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_06_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `3,000 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`, post-batch `7,440` re-verified live on CDP `:9222`):** `7,940 → 7,840 → 7,740 → 7,640 → 7,540 → 7,440` (`0` pending charges; remaining `HOS013_PASS1` reservation `3,600`; headroom `7,440 - 3,600 - 800 = 3,040 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P3:04a_drought_island_seeds` | `P03_04a_drought_island_seeds_t1.mp4` | `a943ffaaa083d456c32097713f2a58106a69d149df94e89fe9db92f2fb96e56b` | `9f6c7b85ac1b64f3dc6db89683727baa7eb3dd86d1407e0f0faaaf64583db790` | `d029b3066dd302e57af68f27f62c92458eb8f55523cc1ad13e2f4da01f4cff2f` | `7,940 → 7,840` | `PENDING_REVIEW` (`keep: false`) |
| `P3:04b_finch_cracks_seed` | `P03_04b_finch_cracks_seed_t1.mp4` | `575014b1213eeac34e99e88eb33b06243208fc25934a8b5d54f4d87494599336` | `d405dc98d72bc8cf5f2ec633bb2c4fbc112045dd6505bf6d325a731483d85459` | `ce8c4d1e915a68faf7c12ff6984ef5fa0b6c498a98d58859ddd1983a6fb80a51` | `7,840 → 7,740` | `PENDING_REVIEW` (`keep: false`) |
| `P3:05a_chicks_deep_beaks` | `P03_05a_chicks_deep_beaks_t1.mp4` | `4425168f215dbb043e98fc8cacf793efd9464a98fdcad3938ec6f436de78424c` | `e654718106e025c1855f5dfe39f9b6d49f12576c6e63485fa699a6869511b400` | `8b051ce8dd6fb10e44cf22a33e58e82f87c9dacfa37e15fe037017bb2df4b39e` | `7,740 → 7,640` | `PENDING_REVIEW` (`keep: false`) |
| `P3:05b_finches_next_generation` | `P03_05b_finches_next_generation_t1.mp4` | `0a62a9536568604611f05d2537c0e9f3aeba242f04c04abc5fb1835a7895dff4` | `c6e5ff090e1957005f761ab063d8aff53c326b9fc7efcf74a28c5b817a7cdf13` | `2c635dc3a8aae0b7bb8ce57c9517c9889c478d475e8f0ed6c92ebfac1da091c5` | `7,640 → 7,540` | `PENDING_REVIEW` (`keep: false`) |
| `P3:07a_darwin_afraid_window` | `P03_07a_darwin_afraid_window_t1.mp4` | `95a93ef7c184718db5ec595478cd8cd002e3d1915848d82bdcff6b4fff60d779` | `3665b4590720e6c0dbeebb3099dd9d1597b775d8428a58a7d326aecb5ad71062` | `815affb389b3b07606b4d6b5cc185acb2a097de840e04e49ff3593f5c17b06bd` | `7,540 → 7,440` | `PENDING_REVIEW` (`keep: false`) |

### Batch 07 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T12:56Z` – `13:13Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch07-20261112T1256Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch07-20261112T1256Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_07_RECEIPT.json` (`archive_v01_pass1/batch-fb7c5a6fd68c.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_07_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `3,500 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`, post-batch `6,940` re-verified live on CDP `:9222`):** `7,440 → 7,340 → 7,240 → 7,140 → 7,040 → 6,940` (`0` pending charges; remaining `HOS013_PASS1` reservation `3,100`; headroom `6,940 - 3,100 - 800 = 3,040 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P3:07b_confessing_murder_letter` | `P03_07b_confessing_murder_letter_t1.mp4` | `8b7e15d52cab8480be9a6d3ceb37e845cb4d6be84ee5cc832522f7dc79c5bdb3` | `7c80d3d7456fc5e32062a47b5aed3a5371bfa8b788ec2fcb5432a331630fa98f` | `e17fdd3bf5d72e437ef797a8ffefe1bb3c2ebff1b79ca00d021580602eefc932` | `7,440 → 7,340` | `PENDING_REVIEW` (`keep: false`) |
| `P3:08_emma_study` | `P03_08_emma_study_t1.mp4` | `cd6bf7c794a47c81efea3f1a72d56113720400ad1e10a514f4fd178d28f4c16c` | `852a4ac006c014377431a91196a3ea6c0f19da4ce94e8aca6f72d4af1ecfcb3f` | `8dd18222d5f6a7ea651ac7fcbf5c35c3832eb3b070e21b7b41b39cb6de0b768f` | `7,340 → 7,240` | `PENDING_REVIEW` (`keep: false`) |
| `P3:09b_emma_letter_cupboard` | `P03_09b_emma_letter_cupboard_t1.mp4` | `6187e461f0e9b151ca26fa4dfaea7fc368811b04c917bde035c82e16511e33e1` | `ad28026bdd31ac0a570269fbf890b8c6c55deb2b95c28d9021612a7364e4bb4c` | `10940a719563649fab7bb912238ec8183081d72625e6b6b2dc030d9f96490655` | `7,240 → 7,140` | `PENDING_REVIEW` (`keep: false`) |
| `P3:10b_vestiges_torn_apart` | `P03_10b_vestiges_torn_apart_t1.mp4` | `cf820f0e63a0dc92b824cf96cc59bfeedb17ec22c418ae556d99dec5156ae383` | `4b296eaaba07fe52b632460d8df3fe38b633d2f103010188c550c3720d5cf9fd` | `a4ade93784c9d20ac8d8207d39b8e38f63a2528f6baa147eaa810f454b02c1d9` | `7,140 → 7,040` | `PENDING_REVIEW` (`keep: false`) |
| `P3:11_barnacles_microscope` | `P03_11_barnacles_microscope_t1.mp4` | `a9311278fb722a3c5effc619b66ba9e7ecd86bfa72c13bf16c90afad425a79f3` | `0a5444723b567efc2ab82811a4addbbe3f28df8f5d486894500265461f1e563e` | `4ac4a83bc0f9d2c0ea1d7bd703664dd92b7e4853a098862fcd323eaf49b3da8b` | `7,040 → 6,940` | `PENDING_REVIEW` (`keep: false`) |

### Batch 08 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T16:08Z` – `16:25Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch08-20261112T1608Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch08-20261112T1608Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_08_RECEIPT.json` (`archive_v01_pass1/batch-406aea3d573c.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_08_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`, review branch `review/013-pass1-sheets` `6490d971`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `4,000 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`, post-batch `6,490` re-verified live on CDP `:9222`):** `6,940` (through all 5 `0`-credit stills at `16:09–16:12Z`) → `+50` account credit grant → `6,990 → 6,890 → 6,790 → 6,690 → 6,590 → 6,490` (`0` pending charges; remaining `HOS013_PASS1` reservation `2,600`; headroom `6,490 - 2,600 - 800 = 3,090 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P3:13a_lyell_warning` | `P03_13a_lyell_warning_t1.mp4` | `2c8b14f9967d62f26f8b56368617ac0fa25cc32c5a29aa8b231c4b60127e9aa4` | `88313fae5ca6e0712a5f3926dd2dc67f900953d78180fe077391518c55683f70` | `cabf9962a1d42227f11758916bac635b43740b03036ea1bb46dc93207aa90860` | `6,990 → 6,890` | `PENDING_REVIEW` (`keep: false`) |
| `P3:13b_brass_globe_turn` | `P03_13b_brass_globe_turn_t1.mp4` | `780f0ddcea03ef5157e3388536e920fb36aaece0bf4abe2dc1aa3940c441a548` | `1823c16b5345f26f49e682ce8aa7c0b25de2b91a6488d857d53e78882cfd6d48` | `4de3e44a58fca27c4d4d50f8f66ead2fb0b1764493d1cc4561f3a7ce8ceb15a8` | `6,890 → 6,790` | `PENDING_REVIEW` (`keep: false`) |
| `P4:02_wallace_collector` | `P04_02_wallace_collector_t1.mp4` | `6a41beae9fc9cc9f894ecfc2758ce82b41b0ac700546a04ebafd48cb4186aa14` | `5bc3ed66c406332163f8a9c233eed3f8c4bbb6bfc211e6adb504c5cb46f7c84b` | `ec16d0915bd243b3c7a6ab0a87376b8da944d3d16f8379fd8d72300e87d45f79` | `6,790 → 6,690` | `PENDING_REVIEW` (`keep: false`) |
| `P4:03a_helen_burning` | `P04_03a_helen_burning_t1.mp4` | `e14296654ffc8da956cd6db5d767eaab056a82f343ce44e564427432eb149928` | `152fed7a8a4eddd5c3c4243a49798ece10e4604cfaebc138f4b093ecdfb344cd` | `7439b9027077dc4c90d4b366f22c0b23dc891cef73300cc87d34f3202acec278` | `6,690 → 6,590` | `PENDING_REVIEW` (`keep: false`) |
| `P4:03b_crates_sinking` | `P04_03b_crates_sinking_t1.mp4` | `ab90ba926e16f9e3d4319c1836a6d5701b90e9a55a90ac5e46ebfccfa20e61ed` | `2bc59ccc1d127b8c58204777534eb98acb9b0a5f32de828dbdbfb3400817f11c` | `bc9d832f113456de6a0cd43732e87361c6d698ed2ab5d1ee669bbab20ff7bd09` | `6,590 → 6,490` | `PENDING_REVIEW` (`keep: false`) |

### Batch 09 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T16:30Z` – `16:46Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch09-20261112T1630Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch09-20261112T1630Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_09_RECEIPT.json` (`archive_v01_pass1/batch-ce4a2b8dd953.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_09_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`, review branch `review/013-pass1-sheets` `72d21fc1`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `4,500 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`, post-batch `5,990` re-verified live on CDP `:9222`):** `6,490 → 6,390 → 6,290 → 6,190 → 6,090 → 5,990` (`0` pending charges; remaining `HOS013_PASS1` reservation `2,100`; headroom `5,990 - 2,100 - 800 = 3,090 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P4:04_open_boat_ten_days` | `P04_04_open_boat_ten_days_t1.mp4` | `66781e8f6ed37db653f445c58d7b4aac60fa915f9a00c6f00377e1ccb6569390` | `1d4ac60d2078d4614f785090e66c7bae0aa253da90cb3a702b6e51925a2c6004` | `296e7da5fb8d2766bb5ad24b4832e8671973b0eb26162a3fbe521415bcb3b103` | `6,490 → 6,390` | `PENDING_REVIEW` (`keep: false`) |
| `P4:06a_wallace_fever` | `P04_06a_wallace_fever_t1.mp4` | `9009bd468846095522ca1b7814c8bb22a036d192745b3a3f230c6394cc77211c` | `7a9cef5b0cf3052866bb7fe0879ae74101082172b5db0fc15aa9a63e17d2d59b` | `1b7173e4ace6cf2797464d158dfbedce01412dc8d0ed46c38a7354fee51a6daa` | `6,390 → 6,290` | `PENDING_REVIEW` (`keep: false`) |
| `P4:07a_wallace_writes_hut` | `P04_07a_wallace_writes_hut_t1.mp4` | `cf336394e0f48cc9f1ccabd747cd98acdf42eedf7cd34e8929dfa073f1d01a59` | `c015c7bb4420201415866769f6ba054ed0dd73d93a4fce1600e1cc24c70b95dc` | `f9e05430b0c934ba724fd1ca171bfb92d46fd234492beb21eb73f99f6a50b6f2` | `6,290 → 6,190` | `PENDING_REVIEW` (`keep: false`) |
| `P4:08_midpoint_twist_packet` | `P04_08_midpoint_twist_packet_t1.mp4` | `bad6741aececb51d2d77db09c7a633925375537c9cc2428a9fcb6bc4dcda57df` | `4739310cda94d99f196c4c621caec76ab40102fcecce3e163a24bf6039036f7b` | `800d0ed382023612534812eeafd2bd8f39873b02cc3f863478728d5a92718c5a` | `6,190 → 6,090` | `PENDING_REVIEW` (`keep: false`) |
| `P4:09a_darwin_reads_wallace` | `P04_09a_darwin_reads_wallace_t1.mp4` | `d167fdaa96d52e661a861052daea49d84a59ce17bfb03ded0a6591c861598fc2` | `ed4dcee94c18822da008d8226161701358b35fc8171d44521c64ea5e97f38a50` | `86971ea385e1a8137469d1b56788ec175916f531cbb28340f0ec20df07d1ab0c` | `6,090 → 5,990` | `PENDING_REVIEW` (`keep: false`) |

### Batch 10 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T16:51Z` – `17:07Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch10-20261112T1651Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch10-20261112T1651Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_10_RECEIPT.json` (`archive_v01_pass1/batch-8df42d99e77f.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_10_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`, review branch `review/013-pass1-sheets` `2704fc98`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `5,000 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`, post-batch `5,490` re-verified live on CDP `:9222`):** `5,990 → 5,890 → 5,790 → 5,690 → 5,590 → 5,490` (`0` pending charges; remaining `HOS013_PASS1` reservation `1,600`; headroom `5,490 - 1,600 - 800 = 3,090 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P4:09b_smashed_letter_pen` | `P04_09b_smashed_letter_pen_t1.mp4` | `dacb60bd68a5c892d5f9fd5e0e2e36f9e2a4866d7bbe933bfbcf8ae92ed8b89a` | `4fcc6595578042967e61b469d4b5ffe611a096c56c318c6acdde359da7b76a2e` | `2794962ba9b0d9d524d1830ed7c521aceafabdc8602c0e8fd17d3108b62b154a` | `5,990 → 5,890` | `PENDING_REVIEW` (`keep: false`) |
| `P4:10_fairness_25_june` | `P04_10_fairness_25_june_t1.mp4` | `a3008b0a20514a8a273fb7492c55409ec5d9a0eb145f2d5400e828d7b1d6f841` | `b088c6ee972abfb385ffbbe21d36df6c2fe5dacbe146817c56c83faf4d17f39f` | `d7d42f5e5bd5ff75726c7d8560472cd37747ba0a72fcddbee69383b755afafc0` | `5,890 → 5,790` | `PENDING_REVIEW` (`keep: false`) |
| `P4:11_down_house_grief` | `P04_11_down_house_grief_t1.mp4` | `797eaadce55c54113c0c56ada50473b85e49c9fbe810ef8d3e7ebf8dbea058dc` | `56f808e833a6a1295402c92f092a917de26e0d8aedcf02a7774825eae4b4046c` | `3c4e284649863daf31548ea965855d1007fbc805a5dd09754b67f58da486a6d3` | `5,790 → 5,690` | `PENDING_REVIEW` (`keep: false`) |
| `P4:12_lyell_hooker_bundle` | `P04_12_lyell_hooker_bundle_t1.mp4` | `820c1433ca609245b150409f709c287d6c25a58770ad962b6ea22768ff3a492a` | `696d7eb39e0f083c174125456ed882bcab881ce7a0082be26f8c88f53a6661b1` | `80fefc8d6f78a40dded9055bec3504b7c1170f2b726afb308df1627483db8d24` | `5,690 → 5,590` | `PENDING_REVIEW` (`keep: false`) |
| `P5:02a_linnean_reading` | `P05_02a_linnean_reading_t1.mp4` | `dc7de232f76b5bde854dd1cb512cf2a868349fa81f9126e6d0ccfda39b9911ea` | `91d742b73943ef1cfe144f418b4a5b737600201025e6e103eaac2441bf0a6b6f` | `840c96180b6d274814670bbc18632e1ab5fb65f837a3001c1669b80e4eadb58a` | `5,590 → 5,490` | `PENDING_REVIEW` (`keep: false`) |

### Batch 11 of 14 — `GENERATED` / `PENDING_REVIEW` (`2026-11-12T17:13Z` – `17:29Z`)

- **Log / done:** `/Users/benjaminoats/_desk/logs/J2529-batch11-20261112T1713Z.log`, `/Users/benjaminoats/_desk/logs/J2529-batch11-20261112T1713Z.done` (`exit 0`)
- **Batch receipt:** `BATCH_11_RECEIPT.json` (`archive_v01_pass1/batch-0a0cabea0bc1.receipt.json`)
- **Full-clip `0.5s` contact sheets:** `BATCH_11_SHEETS.json` (`archive_v01_pass1/sheets/*_sheet.jpg`, review branch `review/013-pass1-sheets` `3a47bd83`)
- **Reservation / floor:** `HOS013_PASS1` (`--floor 3000 --other-reservations 0`)
- **Credits spent:** `500` (`5 × 100` Quality; 5 start stills at `0` credits via `Nano Banana 2.1`; cumulative `5,500 / 6,600`)
- **Live balance chain (all 5 posted in `~/_desk/state/flow/shared/account.jsonl`, post-batch `4,990` re-verified live on CDP `:9222`):** `5,490 → 5,390 → 5,290 → 5,190 → 5,090 → 4,990` (`0` pending charges; remaining `HOS013_PASS1` reservation `1,100`; headroom `4,990 - 1,100 - 800 = 3,090 >= 3,000`)

| Row | Clip | Clip SHA-256 | Start Still SHA-256 | Sheet SHA-256 | Before → After | Status |
|---|---|---|---|---|---|---|
| `P5:03a_two_empty_chairs` | `P05_03a_two_empty_chairs_t1.mp4` | `c9bb651faf9d6d17266df305bbeca5308f73ff9f45134506eb0305dc66b15a4e` | `567ba05fd4fad03414087b7da1be55fe29eb8646e7e0141f2c3aefe316ef5852` | `a2b108e611ba12f7e4111b9c7d85e22dcdec997af6c2d0ba22fb0502b2d3ffc5` | `5,490 → 5,390` | `PENDING_REVIEW` (`keep: false`) |
| `P5:03b_wallace_jungle_clearing` | `P05_03b_wallace_jungle_clearing_t1.mp4` | `470715a0d13e5aeae43c97251b61d04d715d1d74a2d091efe47ab5e7794893f8` | `5c8d6d0a1c772a48ca6f618e57fae88a228c5863d260166c8e4bc4f9834e9e89` | `ec5f26b435944f1edccb0cbbd98b491d910dbb18c3d3527566a956f2d88092c5` | `5,390 → 5,290` | `PENDING_REVIEW` (`keep: false`) |
| `P5:04a_empty_linnean_hall` | `P05_04a_empty_linnean_hall_t1.mp4` | `c9d642728dcddba3f0ee4896ec85e3dc450124c947abc11a95547780c897a439` | `eb773a5f25d2de7106a7d461b6c58e1e0a2b50f434abb9334e735b9ee3ddba6f` | `454ec6a5e7a28aa2ddd39c9f0d3de71bc0d7100de5137a45868d850452536910` | `5,290 → 5,190` | `PENDING_REVIEW` (`keep: false`) |
| `P5:05a_darwin_writes_origin` | `P05_05a_darwin_writes_origin_t1.mp4` | `5b7a829f49a556d76247358d894cde276fb17031137a14cac197582bd1187905` | `07deb98f62cf8790a5f4116eaabe2a621e74abfffa775c49fdb4b71c6233da81` | `2d15c0b9cfc46576b0e5aa985e19905ea2f230302ba9c61cb68412ae4646a6c2` | `5,190 → 5,090` | `PENDING_REVIEW` (`keep: false`) |
| `P5:06_murray_bookshop` | `P05_06_murray_bookshop_t1.mp4` | `87e35853e7c047bf5ed9e970498bcd0d67cfd16a02a4143535faadd3f7411ef5` | `a43d7a8732e1d8f55ae531e0ed997aa2b484a5c95ae4adc39c9e6697768b666f` | `d23f02873440c62d8cdbf22f55e7a4b26b8562f8356665544938abfc18fd9ec3` | `5,090 → 4,990` | `PENDING_REVIEW` (`keep: false`) |

## Chief Review State (`REVIEW_STATE.json`)

- **Rows 1–15 (`6815870258`):** `keep: true` on `1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15`; `RETAKE` on `3, 10`.
- **Rows 16–20 (`6819995428` / `6819976359`):** `keep: true` on `16, 17, 18, 19, 20` (row `19` trimmed `0.00–4.50 s`; row `20` used `0.00–6.00 s`).
- **Rows 21–25 (`6822411223` / `6822483718`):** `keep: true` on `21, 22, 23, 25` (row `22` retime `7.917→8.00 s`, no freeze; row `25` clip `4.00–7.90 s`); `RETAKE` on `24`.
- **Rows 26–40 (`6829662956`):** `keep: true` on `26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40` as cut; `RETAKE` on `28` (`P3:05a_chicks_deep_beaks`).
- **Rows 41–45 (`6830257530`, closing `6830137619`):** `keep: true` on `41, 42, 43, 44, 45` as cut (`2.25–3.75 s` strip skipped; row `45` off retake batch).
- **Rows 46–50 (`6830884885` / `6830918005`, withdrawing `6830830084` on rows `49–50`):** `keep: true` on `46, 48, 50` as cut; `RETAKE` on `47` (`P4:10_fairness_25_june`) and `49` (`P4:12_lyell_hooker_bundle`).
- **Held retake batch after pass 1:** rows `3, 10, 24, 28, 47, 49`, reservation `600` Flow credits under `--floor 3000` (`£0` cash).
