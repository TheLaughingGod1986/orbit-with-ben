# J1048 Per-Export QA Sweep Inventory & Report (28 Oct 2026)

- **Job:** `J1048` (`both-qa-sweep`, superseding `J0982`)
- **Agent:** `gemini` (Gemini Argon, Elected Acting Chief)
- **Total exports inventoried:** `73` (`46` OWB, `27` HOS)
  - **Window A — Original sweep window (`2026-10-24T18:48Z .. 2026-10-26T15:09Z`):** `37` exports
  - **Window B — Post-window revisions (through `2026-10-28T02:35Z`, including `J0935` & `J1032`):** `23` exports
  - **Window C — Standalone baseline packs (`OWB S1, S4..S8 v01` + `HOS S1..S3, S5..S8`):** `13` exports
- **Spend:** `£0` / `0 credits`
- **New repair jobs needed:** `0` (all 73 exports have `picture_qa`, `polish_gate`, and `music_gate` strictly newer than their last `.mp4` render with `0` unaddressed FAILs)

## 1. Delta Since J0982 (`2026-10-27T23:39:48Z`)

1. **4 New OWB `J0935` Short Revisions Verified (`0` FAILs):**
   - `OWB:025` `wed11_opening_testA_v05.mp4` (`2026-10-27T23:57:06Z`, sha256 `677f7d38d8c2...`): `picture_qa` PASS (`0/8` FAIL, `4` WARN, `+38.0s`), `polish_gate` PASS (`0/8` FAIL, `2` WARN, `+36.6s`), `music_gate` PASS (`+35.2s`).
   - `OWB:025` `thu12_length_test_dust_v04.mp4` (`2026-10-28T00:59:49Z`, sha256 `be9df541a4a2...`): `picture_qa` PASS (`0/16` FAIL, `5` WARN, `+129.2s`), `polish_gate` PASS (`0/16` FAIL, `2` WARN, `+120.6s`), `music_gate` PASS (`+112.4s`).
   - `OWB:025` `fri13_ingenuity_72_v05.mp4` (`2026-10-28T01:00:08Z`, sha256 `7be6197b9bc2...`): `picture_qa` PASS (`0/8` FAIL, `1` WARN, `+92.3s`), `polish_gate` PASS (`0/8` FAIL, `1` WARN, `+88.1s`), `music_gate` PASS (`+82.7s`).
   - `OWB:026` `wed18_robot_reach_nearest_star_v04.mp4` (`2026-10-28T01:41:34Z`, sha256 `de5c71547fa5...`): `picture_qa` PASS (`0/8` FAIL, `1` WARN, `+54.8s`), `polish_gate` PASS (`0/8` FAIL, `1` WARN, `+53.5s`), `music_gate` PASS (`+52.3s`). Also committed `picture_qa_v04/picture_qa.json`, which had been left untracked in `6351ad2b5`.
2. **7 HOS Standalone Baseline Packs (`S1..S3`, `S5..S8`) `music_gate` Completed & Inventoried (`0` FAILs):**
   - Placed `hos-standalone-shorts_score_bed_v01.mp3` and `hos-standalone-shorts_score_bed_v01_plan.json` (with `Pace: 72-84 BPM` and `NOT:` brief from `MUSIC_PROMPT_v01.md`) in `docs/STANDALONE_SHORTS_TEST_2026-10/05_Music/` and ran `music_gate.py` across all 7 HOS standalone baseline packs (`hos_sa_s1_herschel_infrared_v01`, `hos_sa_s2_brand_phosphorus_v01`, `hos_sa_s3_snow_pump_v02`, `hos_sa_s5_penzias_pigeons_v01`, `hos_sa_s6_fleming_mould_v01`, `hos_sa_s7_priestley_mint_v02`, `hos_sa_s8_hales_blood_v01`). All 7 exited `rc=0` (`PASS`, `0` FAIL, `1` pace WARN) and are now committed under `docs/STANDALONE_SHORTS_TEST_2026-10/qa_shorts_v01/<pack>/music_gate_<pack>.{json,txt}`.
3. **Previously Untracked OWB Gate Sidecars Committed to Git:**
   - Committed the untracked gate sidecars (`picture_qa`, `polish_gate`, `music_gate`, `cuts_v04.json`, `pool_v04.json`, `_meta.json`, `_gate.txt`, `_sfx.txt`, `sha256_manifest_v04.json`) for `OWB:021` `saturn_ten_metres_thin_v04`, `OWB:023` `venus_95pct_wide_v05`, `OWB:026` `wed18_robot_reach_nearest_star_v04`, and the 6 `J1032` Batch C `v04` Shorts (`fri20_grapefruit_cherry_v04`, `earth_equator_weight_v04`, `028_short_mon30_comets_v04`, `028_short_wed02_opening_testA_v04`, `028_short_fri04_scale_v04`, `028_short_lift_night_sky_35yr_v04`).

## 2. Per-Export Inventory Table (73 Exports)

| Ch | Window | Film | Export ID | Media SHA-256 (prefix) | Media Mtime (UTC) | `picture_qa` | `polish_gate` | `music_gate` | Fresh? | Linked Jobs |
|---|---|---|---|---|---|---|---|---|---|---|
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:021` | `saturn_ten_metres_thin_v04` | `6de9961ac45d` | `2026-10-25T14:10:46Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:023` | `venus_95pct_wide_v05` | `09e5e66332fe` | `2026-10-25T14:09:22Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:023` | `venus_two_hours_v04` | `20efc0c80d1c` | `2026-10-25T14:14:56Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:025` | `mon09_night_cold_v03` | `cfff04cdddcd` | `2026-10-26T07:21:16Z` | PASS (0/7F, 2W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:025` | `wed11_opening_testA_v04` | `788ae0e891d6` | `2026-10-26T11:46:00Z` | PASS (0/8F, 3W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:025` | `thu12_length_test_dust_v03` | `f9c4fba6550a` | `2026-10-26T10:39:53Z` | PASS (0/16F, 5W) | PASS (0/16F, 2W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:025` | `fri13_ingenuity_72_v04` | `d589d39d02d8` | `2026-10-26T11:06:07Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:026` | `mon16_cant_see_nearest_star_v03` | `cddcfb965567` | `2026-10-26T11:32:08Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:026` | `wed18_robot_reach_nearest_star_v03` | `8a264ecba447` | `2026-10-26T11:34:56Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:026` | `fri20_grapefruit_cherry_v03` | `a4024c86904c` | `2026-10-26T07:46:07Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:027` | `earth_sudden_air_v05` | `666ab5b1b16d` | `2026-10-25T08:04:55Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:027` | `earth_equator_weight_v03` | `e7220c124e4d` | `2026-10-26T12:03:39Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_mon30_comets_v03` | `01bbd942ee93` | `2026-10-26T12:20:40Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_wed02_opening_testA_v03` | `8abcd2cadd22` | `2026-10-26T12:38:43Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_fri04_scale_v03` | `bb935379881a` | `2026-10-26T12:46:32Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_lift_night_sky_35yr_v03` | `55c08d2ebfe9` | `2026-10-26T12:36:11Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_lift_oort_marbles_v03` | `344bd0d0ab04` | `2026-10-26T01:32:12Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:029` | `029_short_wed09_great_dimming_v03` | `fc3c1b30be44` | `2026-10-25T22:23:45Z` | PASS (0/8F, 4W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:029` | `029_short_fri11_opening_testA_v03` | `c12dc1774e68` | `2026-10-25T22:26:06Z` | PASS (0/12F, 3W) | PASS (0/12F, 2W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:029` | `029_short_mon14_half_moon_daylight_v03` | `1e3d9ba6830b` | `2026-10-25T22:27:39Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:030` | `030_apophis_short_v13` | `2b276eb295df` | `2026-10-26T07:01:55Z` | PASS (0/7F, 6W) | PASS (0/7F, 1W) | PASS (0F, 14W) | YES | J0974 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:SA` | `owb_sa_s2_neptune_v07` | `0919db03d432` | `2026-10-25T19:30:17Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 1W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:SA` | `owb_sa_s3_iss_sunrises_v04` | `433ce60e09d4` | `2026-10-25T05:02:45Z` | PASS (0/6F, 6W) | PASS (0/6F, 1W) | PASS (0F, 14W) | YES | — |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:SA` | `owb_sa_s2_neptune_v07a` | `de62264cbd89` | `2026-10-27T00:13:08Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 1W) | YES | — |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:030` | `030_apophis_short_v13a` | `898d26f526da` | `2026-10-27T00:42:50Z` | PASS (0/7F, 6W) | PASS (0/7F, 1W) | PASS (0F, 14W) | YES | J0974 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:029` | `029_short_lift_die_young_10my_v01` | `dc6bd3ccf387` | `2026-10-26T16:22:05Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0979, J1042 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:029` | `029_short_wed09_great_dimming_v04` | `e0459b017dda` | `2026-10-27T15:42:14Z` | PASS (0/8F, 3W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:029` | `029_short_fri11_opening_testA_v04` | `ff4194857a02` | `2026-10-27T15:43:27Z` | PASS (0/12F, 3W) | PASS (0/12F, 2W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:029` | `029_short_mon14_half_moon_daylight_v04` | `31f362f4437b` | `2026-10-27T15:44:56Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:025` | `mon09_night_cold_v04` | `ad52d7b9d65c` | `2026-10-27T22:27:37Z` | PASS (0/8F, 4W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:026` | `fri20_grapefruit_cherry_v04` | `228cb06dfd37` | `2026-10-27T11:53:47Z` | PASS (0/9F, 3W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:027` | `earth_equator_weight_v04` | `d35efd737ed0` | `2026-10-27T10:49:19Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:028` | `028_short_mon30_comets_v04` | `65e58aea2a20` | `2026-10-27T11:20:08Z` | PASS (0/8F, 2W) | PASS (0/8F, 2W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:028` | `028_short_wed02_opening_testA_v04` | `0eb18596d2d6` | `2026-10-27T11:20:36Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:028` | `028_short_fri04_scale_v04` | `37fbe8b9ed33` | `2026-10-27T11:21:02Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:028` | `028_short_lift_night_sky_35yr_v04` | `91b297a262c1` | `2026-10-27T11:54:12Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s1_mercury_v01` | `590f4e693d5c` | `2026-10-17T04:40:33Z` | PASS (0/5F, 4W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | — |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s4_uranus_v01` | `0aec6e86525d` | `2026-10-17T04:48:23Z` | PASS (0/6F, 4W) | PASS (0/6F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s5_shooting_stars_v01` | `f21070efa726` | `2026-10-12T22:54:37Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s6_titan_v01` | `3f2f51d4f8ff` | `2026-10-17T04:43:45Z` | PASS (0/5F, 4W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s7_pluto_heart_v01` | `a3572604f0da` | `2026-10-12T23:01:19Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s8_voyager1_v01` | `b8bb56f7ef66` | `2026-10-17T04:44:42Z` | PASS (0/6F, 4W) | PASS (0/6F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `post_2026-10-27T23:39Z_j0935_revision` | `OWB:025` | `wed11_opening_testA_v05` | `efe446a4dd6f` | `2026-10-27T23:57:06Z` | PASS (0/8F, 4W) | PASS (0/8F, 2W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `post_2026-10-27T23:39Z_j0935_revision` | `OWB:025` | `thu12_length_test_dust_v04` | `2ab18322e416` | `2026-10-28T00:59:49Z` | PASS (0/16F, 5W) | PASS (0/16F, 2W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `post_2026-10-27T23:39Z_j0935_revision` | `OWB:025` | `fri13_ingenuity_72_v05` | `90134bf06c1b` | `2026-10-28T01:00:08Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `post_2026-10-27T23:39Z_j0935_revision` | `OWB:026` | `wed18_robot_reach_nearest_star_v04` | `f7ccc2f5232a` | `2026-10-28T01:41:34Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:006` | `hos_006_master_v06` | `36c54e684b8a` | `2026-10-24T23:29:39Z` | PASS (0/96F, 5W) | PASS (0/96F, 5W) | PASS (0F, 0W) | YES | J0958 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:007` | `hos_007_master_v04` | `c7f62adbb241` | `2026-10-24T23:45:35Z` | PASS (0/102F, 6W) | PASS (0/102F, 6W) | PASS (0F, 0W) | YES | J0960 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:SA` | `hos_sa_s4_curie_notebooks_v07` | `38d643470b2d` | `2026-10-25T13:39:07Z` | PASS (0/11F, 1W) | PASS (0/11F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:001` | `hos_001_s11_curved_flask_v07` | `5de76a824e88` | `2026-10-25T15:16:21Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:002` | `hos_002_backcat_four_elements_v03` | `9340cae9cd5b` | `2026-10-26T00:47:56Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:004` | `hos_004_backcat_gold_foil_v03` | `f1cb7ec072c7` | `2026-10-26T00:45:03Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:004` | `hos_004_s05_dalton_v03` | `f93745e95558` | `2026-10-26T13:14:18Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | J0966 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s01_the_sum_v04` | `e98ce5602b63` | `2026-10-25T11:58:02Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s02_the_tied_arm_v05` | `c31fbb5c88f6` | `2026-10-26T00:50:45Z` | PASS (0/12F, 1W) | PASS (0/12F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s03_never_saw_v03` | `3646009fc651` | `2026-10-26T13:13:27Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s04_galen_stove_v04` | `f15fb5ba050b` | `2026-10-25T14:42:10Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s05_valves_v03` | `e3aa2c6cfc56` | `2026-10-26T00:51:47Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:007` | `hos_007_s04_smallpox_test_v02` | `745de3f56a11` | `2026-10-26T07:57:45Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 14W) | YES | J0966 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:007` | `hos_007_s05_vacca_jesty_v03` | `c94af4f919a4` | `2026-10-26T07:59:04Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 14W) | YES | J0966 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:005` | `hos_005_s03_never_saw_v04` | `e1f862ba737a` | `2026-10-26T21:33:48Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:007` | `hos_007_s04_smallpox_test_v03` | `858495ea7dcb` | `2026-10-26T19:08:19Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:007` | `hos_007_s04_smallpox_test_v04` | `3ef3fa773750` | `2026-10-27T22:42:13Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:007` | `hos_007_s05_vacca_jesty_v04` | `7a3a736069e2` | `2026-10-26T19:11:04Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:007` | `hos_007_s05_vacca_jesty_v05` | `e5ea76f012fb` | `2026-10-26T20:38:29Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:004` | `hos_004_s05_dalton_v04` | `8ce07a605697` | `2026-10-27T22:42:47Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `standalone_baseline_pack` | `HOS:SA` | `hos_sa_s1_herschel_infrared_v01` | `e00f20b39383` | `2026-10-17T05:02:35Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | — |
| HOS | `standalone_baseline_pack` | `HOS:SA` | `hos_sa_s2_brand_phosphorus_v01` | `66462ea90615` | `2026-10-12T20:24:11Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 1W) | YES | — |
| HOS | `standalone_baseline_pack` | `HOS:SA` | `hos_sa_s3_snow_pump_v02` | `634abd5ef8a0` | `2026-10-17T05:03:33Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | — |
| HOS | `standalone_baseline_pack` | `HOS:SA` | `hos_sa_s5_penzias_pigeons_v01` | `77cc187a0794` | `2026-10-12T23:46:55Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 1W) | YES | J0967 |
| HOS | `standalone_baseline_pack` | `HOS:SA` | `hos_sa_s6_fleming_mould_v01` | `fd5bf3469734` | `2026-10-12T23:47:26Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 1W) | YES | J0967 |
| HOS | `standalone_baseline_pack` | `HOS:SA` | `hos_sa_s7_priestley_mint_v02` | `6857ac9374bc` | `2026-10-13T00:04:37Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | J0967 |
| HOS | `standalone_baseline_pack` | `HOS:SA` | `hos_sa_s8_hales_blood_v01` | `56ea2256cee6` | `2026-10-12T23:48:23Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 1W) | YES | J0967 |
