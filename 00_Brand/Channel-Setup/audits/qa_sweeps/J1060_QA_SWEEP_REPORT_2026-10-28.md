# J1060 Per-Export QA Sweep Inventory & Report (28 Oct 2026)

- **Job:** `J1060` (`both-qa-sweep`, superseding `J1054`, `J1048`, `J0982`)
- **Agent:** `gemini` (Gemini Argon, Worker)
- **Total exports inventoried:** `138` (`83` OWB, `55` HOS)
  - **Base J1054 exports verified (`105`):** `70` OWB, `35` HOS (`0` FAILs; includes `HOS:005` `s06..s08` `v01` resolved in `J1058`)
  - **Extended J1060 sweep (`33` additional exports):** `5` OWB `020`/`022` `v01` lift Shorts (`music_gate` run), `16` HOS `001`–`004` `v01` lift Shorts (`music_gate` run), `6` OWB long/compilation masters (`023 v05e`, `025 v03f`, `027 v01m`, `028 v03`, `029 v03b`, `owb_compilation_v05`), and `6` silent visual-overlay / code-graphic packs (`OWB:028`, `OWB:029` `teaching_overlays_v01_pack`; `HOS:007`–`HOS:010` `code_graphics_v01`)
- **Spend:** `£0` / `0 credits`
- **New repair jobs created (`jobs.py add`, no spend):** `2` (`J1063` for OWB `020`/`022` `v01` lift Shorts `music_gate` FAILs; `J1064` for HOS `001`–`004` `v01` lift Shorts `music_gate` FAILs)
- **Unaddressed FAILs:** `0`

## 1. Delta Since J1054 (`2026-10-28T03:51Z`)

1. **5 OWB `020` and `022` `v01` Lift Shorts `music_gate` Run (`J1063` queued, `£0`):**
   - `OWB:020` `jupiter_no_crust_v01`: passes `picture_qa` (`0/7` FAIL, `1` WARN) and `polish_gate` (`0/7` FAIL, `1` WARN). `music_gate.py` recorded `FAIL` (`own: not in this film 05_Music`, `own: no plan next to the bed`).
   - `OWB:022` `sun_century_warming_v01`, `sun_eight_minute_light_v01`, `sun_faint_young_sun_70pct_v01`, `sun_moist_greenhouse_v01`: all 4 pass `picture_qa` (`0` FAILs) and `polish_gate` (`0` FAILs), and `sun-brighter_score_bed_v01.mp3` (`525.0 s`) has `0` similarity matches and `0` gaps, failing only `brief: the prompt has no Pace: NN-NN BPM line` in pre-8-Oct `sun-brighter_score_bed_v01_plan.json`. Queued no-spend fix job `J1063`.
2. **16 HOS `001`–`004` `v01` Lift Shorts `music_gate` Run (`J1064` queued, `£0`):**
   - `HOS:001` (`s07_semmelweis_hands_v01`, `s08_pasteur_germs_v01`, `s09_lister_antiseptic_v01`, `s10_miasma_microscope_v01`), `HOS:002` (`s06_atomic_weights_v01`, `s07_mendeleev_cards_v01`, `s08_periodic_table_work_v01`, `s09_dobereiner_triads_v01`), `HOS:003` (`s04_unknown_x_v01`, `s05_first_xray_v01`, `s06_how_xrays_work_v01`, `s07_xray_tube_v01`): all 12 pass `picture_qa` (`0` FAILs) and `polish_gate` (`0` FAILs), and their deterministic own-synthesis pads (`hos00N_<sid>_synth_pad_v01.wav`) have `0` similarity matches and `0` gaps, failing `own` (`not in this film 05_Music`, `no plan next to the bed`).
   - `HOS:004` (`s04_cathode_rays_v01`, `s06_moseley_atomic_number_v01`, `s07_outer_electrons_v01`, `s08_plum_pudding_v01`): all 4 pass `picture_qa` (`0` FAILs) and `polish_gate` (`0` FAILs); `music_gate.py` recorded `brief`/`own`/`gap`/`reused` FAILs on their pre-8-Oct temp beds. Queued no-spend fix job `J1064`.
3. **6 Newest OWB Long / Compilation Masters & 6 Silent Visual Overlay / Code-Graphic Packs Verified (`0` FAILs):**
   - `023_Venus_full_rough_v05e`, `025_MarsRobot_full_rough_v03f`, `027_EarthSpin_rough_v01m`, `028_Gliese710_full_master_v03`, `029_Betelgeuse_full_rough_v03b`, and `owb_compilation_v05` all PASS `picture_qa`, `polish_gate`, and `music_gate` with gate timestamps newer than their `.mp4` renders.
   - `OWB:028` and `OWB:029` `teaching_overlays_v01_pack` and `HOS:007`–`HOS:010` `code_graphics_v01` all PASS `picture_qa` and `polish_gate` (`0` FAILs) with gate timestamps newer than their `.mp4` renders.

## 2. Per-Export Inventory Table (138 Exports)

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
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:021` | `saturn_clock_100_300my_v01` | `c9db15aab8d7` | `2026-10-17T04:18:10Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:021` | `saturn_late_arrival_4_5b_v01` | `f4fe9b04a92c` | `2026-10-16T23:13:42Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:021` | `saturn_keck_ring_rain_v01` | `8a118ddaf25f` | `2026-10-19T12:29:59Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:021` | `saturn_mimas_mass_v01` | `68b8866c4344` | `2026-10-18T03:10:37Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:021` | `saturn_ten_hour_day_v01` | `91c8b5b67cd4` | `2026-10-19T04:40:36Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:023` | `venus_90x_thicker_air_v01` | `169cf739ac30` | `2026-10-17T14:06:42Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:023` | `venus_heavy_water_100x_v01` | `621a869effc4` | `2026-10-16T22:51:53Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:023` | `venus_less_sunlight_465c_v01` | `3e2d420693ef` | `2026-10-18T10:53:54Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:024` | `light_speed_gps_drift_v01` | `2da7087a047a` | `2026-10-17T16:12:14Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:024` | `light_speed_one_ton_energy_v01` | `5dac899c0ecb` | `2026-10-18T14:49:44Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:024` | `light_speed_shrink_10ly_v01` | `2655554470ca` | `2026-10-17T01:13:28Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:024` | `light_speed_twin_trip_v01` | `d24c4ff9445a` | `2026-10-16T19:08:43Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:025` | `mars_curiosity_nuclear_v01` | `3f9552eebc75` | `2026-10-20T03:05:32Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:025` | `mars_insight_quakes_v01` | `393dc6c2f508` | `2026-10-19T16:24:05Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:025` | `mars_radiation_3months_v01` | `fed4ffb9c064` | `2026-10-20T14:38:49Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:026` | `nearest_star_earth_pinhead_v01` | `498f51d9937c` | `2026-10-18T18:09:02Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:026` | `nearest_star_light_4_years_v01` | `2a4d23d6c21d` | `2026-10-17T19:40:45Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:026` | `nearest_star_red_dwarf_trillions_v01` | `cff1ae86313a` | `2026-10-17T07:05:49Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:026` | `nearest_star_walk_900m_v01` | `4e83558557da` | `2026-10-16T19:08:43Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:027` | `earth_40000_years_v01` | `verified_in_` | `2026-10-16T19:08:43Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:027` | `earth_ancient_eclipses_v01` | `033f9f76fda5` | `2026-10-18T21:09:52Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:027` | `earth_day_one_year_v01` | `a6b6144d77db` | `2026-10-18T09:19:12Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:024` | `024_LightSpeed_v06` | `8d0b131771c1` | `2026-10-21T20:42:41Z` | PASS (0/111F, 60W) | PASS (0/111F, 8W) | PASS (0F, 0W) | YES | — |
| OWB | `j1054_extended_lift_shorts_and_longs` | `OWB:026` | `026_NearestStar_v06` | `624562255a58` | `2026-10-22T10:00:26Z` | PASS (0/103F, 25W) | PASS (0/103F, 6W) | PASS (0F, 13W) | YES | — |
| HOS | `j1054_extended_lift_shorts_and_longs` | `HOS:005` | `hos_005_s06_blood_pressure_cuff_v01` | `b9bc921502c3` | `2026-10-18T03:25:35Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | J1058 |
| HOS | `j1054_extended_lift_shorts_and_longs` | `HOS:005` | `hos_005_s07_heart_pulse_v01` | `a6513555187f` | `2026-10-19T00:47:56Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 14W) | YES | J1058 |
| HOS | `j1054_extended_lift_shorts_and_longs` | `HOS:005` | `hos_005_s08_capillaries_v01` | `64f746e65721` | `2026-10-20T15:01:22Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | J1058 |
| HOS | `j1054_extended_lift_shorts_and_longs` | `HOS:006` | `hos_006_s04_photosynthesis_v01` | `1198f5671f29` | `2026-10-16T19:15:42Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `j1054_extended_lift_shorts_and_longs` | `HOS:006` | `hos_006_s05_charcoal_gas_v01` | `06fbeceda494` | `2026-10-16T16:59:44Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `j1054_extended_lift_shorts_and_longs` | `HOS:006` | `hos_006_s06_ingenhousz_oxygen_v01` | `3daf38e7f3f5` | `2026-10-18T07:27:09Z` | PASS (0/8F, 0W) | PASS (0/8F, 0W) | PASS (0F, 13W) | YES | — |
| HOS | `j1054_extended_lift_shorts_and_longs` | `HOS:006` | `hos_006_s07_priestley_mint_v01` | `253b56176b87` | `2026-10-19T05:07:52Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `j1054_extended_lift_shorts_and_longs` | `HOS:006` | `hos_006_s08_willow_pot_v01` | `8bce695efab2` | `2026-10-21T01:45:25Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:020` | `jupiter_no_crust_v01` | `64b8ac7316fe` | `2026-10-17T04:15:46Z` | PASS (0/4F, 1W) | PASS (0/4F, 1W) | FAIL (2F, 13W) | YES | J1063 |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:022` | `sun_century_warming_v01` | `bbd0d5d0aebb` | `2026-10-19T00:28:13Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (1F, 13W) | YES | J1063 |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:022` | `sun_eight_minute_light_v01` | `a19cbc21626e` | `2026-10-19T08:42:09Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (1F, 13W) | YES | J1063 |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:022` | `sun_faint_young_70pct_v01` | `749bb4309010` | `2026-10-21T01:31:08Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | FAIL (1F, 13W) | YES | J1063 |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:022` | `sun_moist_greenhouse_v01` | `7850073a1412` | `2026-10-17T23:24:50Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (1F, 13W) | YES | J1063 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:001` | `hos_001_s07_semmelweis_hands_v01` | `ec69d9145e95` | `2026-10-17T16:33:56Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:001` | `hos_001_s08_pasteur_germs_v01` | `221d79a7395f` | `2026-10-17T20:07:33Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:001` | `hos_001_s09_lister_antiseptic_v01` | `e86a3a31adb7` | `2026-10-18T18:23:35Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:001` | `hos_001_s10_miasma_microscope_v01` | `a4d4f4b1e016` | `2026-10-19T16:50:41Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:002` | `hos_002_s06_atomic_weights_v01` | `fb24bbdc5c12` | `2026-10-17T07:31:29Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:002` | `hos_002_s07_mendeleev_cards_v01` | `8e215ede0a5a` | `2026-10-17T12:01:15Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:002` | `hos_002_s08_periodic_table_work_v01` | `daf22bb6b9c6` | `2026-10-18T15:17:24Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:002` | `hos_002_s09_dobereiner_triads_v01` | `f04c73a572b6` | `2026-10-19T12:50:12Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:003` | `hos_003_s04_unknown_x_v01` | `3b50feaf513e` | `2026-10-16T21:16:24Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:003` | `hos_003_s05_first_xray_v01` | `f667ee2aad8c` | `2026-10-17T01:36:49Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:003` | `hos_003_s06_how_xrays_work_v01` | `6a0f0fd171a8` | `2026-10-18T11:19:58Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:003` | `hos_003_s07_xray_tube_v01` | `5ecd15678eb0` | `2026-10-19T09:07:14Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:004` | `hos_004_s04_cathode_rays_v01` | `027dc6f11efa` | `2026-10-17T14:29:30Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:004` | `hos_004_s06_moseley_atomic_number_v01` | `849264ff34b6` | `2026-10-17T23:49:15Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:004` | `hos_004_s07_outer_electrons_v01` | `b103251e736c` | `2026-10-18T21:27:32Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (3F, 0W) | YES | J1064 |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:004` | `hos_004_s08_plum_pudding_v01` | `5ddd8c32f45c` | `2026-10-20T03:33:54Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | FAIL (2F, 0W) | YES | J1064 |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:023` | `023_Venus_full_rough_v05e` | `verified_in_` | `2026-10-14T23:12:56Z` | PASS (0/96F, 25W) | PASS (0/96F, 9W) | PASS (0F, 13W) | YES | — |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:025` | `025_MarsRobot_full_rough_v03f` | `verified_in_` | `2026-10-09T03:06:49Z` | PASS (0/107F, 28W) | PASS (0/107F, 12W) | PASS (0F, 0W) | YES | — |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:027` | `027_EarthSpin_rough_v01m` | `verified_in_` | `2026-10-21T21:19:57Z` | PASS (0/88F, 40W) | PASS (0/88F, 5W) | PASS (0F, 0W) | YES | — |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:028` | `028_Gliese710_full_master_v03` | `verified_in_` | `2026-10-23T14:25:56Z` | PASS (0/65F, 7W) | PASS (0/65F, 4W) | PASS (0F, 13W) | YES | — |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:029` | `029_Betelgeuse_full_rough_v03b` | `verified_in_` | `2026-10-23T20:27:40Z` | PASS (0/84F, 6W) | PASS (0/84F, 4W) | PASS (0F, 13W) | YES | — |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:COMP` | `owb_compilation_v05` | `verified_in_` | `2026-10-15T08:40:20Z` | PASS (0/38F, 7W) | PASS (0/38F, 2W) | PASS (0F, 9W) | YES | — |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:028` | `028_teaching_overlays_v01_pack` | `silent_visua` | `2026-10-18T00:37:27Z` | PASS (0/20F, 3W) | PASS (0/20F, 1W) | N/A (silent visual pack) | YES | — |
| OWB | `j1060_extended_lift_shorts_and_longs` | `OWB:029` | `029_teaching_overlays_v01_pack` | `silent_visua` | `2026-10-18T00:32:25Z` | PASS (0/17F, 1W) | PASS (0/17F, 1W) | N/A (silent visual pack) | YES | — |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:007` | `007_code_graphics_v01` | `silent_visua` | `2026-10-16T15:05:51Z` | PASS (0/3F, 1W) | PASS (0/3F, 1W) | N/A (silent visual pack) | YES | — |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:008` | `008_code_graphics_v01` | `silent_visua` | `2026-10-16T15:11:10Z` | PASS (0/11F, 1W) | PASS (0/11F, 1W) | N/A (silent visual pack) | YES | — |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:009` | `009_code_graphics_v01` | `silent_visua` | `2026-10-16T15:12:04Z` | PASS (0/12F, 1W) | PASS (0/12F, 1W) | N/A (silent visual pack) | YES | — |
| HOS | `j1060_extended_lift_shorts_and_longs` | `HOS:010` | `010_code_graphics_v01` | `silent_visua` | `2026-10-16T15:15:54Z` | PASS (0/13F, 6W) | PASS (0/13F, 0W) | N/A (silent visual pack) | YES | — |
