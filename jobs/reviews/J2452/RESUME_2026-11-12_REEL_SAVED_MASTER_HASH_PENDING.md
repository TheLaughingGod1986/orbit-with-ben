# J2452 — reel delivered; full-size master copy awaits hash

Worker macbook. Progress 14/15. PR #789 stays open; no UAT, upload, Studio action, generation or spend.

The master NAS copy now has all **26,505,479,537 bytes**. The original 10,703,863,808-byte prefix matched byte for byte, and the first bounded writer appended verified source bytes before stopping on its own budget. The second writer used a same-session provenance checkpoint (source SHA-256, exact destination size and mtime), appended the remainder and exited 0. **This is copy provenance, not a full destination SHA-256 PASS.** The master is not yet delivered or ready for UAT. Nothing existing was replaced or deleted.

The **12:26 reel is delivered**, fully decoded with exit 0 and hash-checked on NAS:
`/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/sleep_video_01_spotcheck_v01.mp4`
309,149,597 bytes; SHA-256 `1eda0d2d98a2d65afd65a1068745f04238af3e9d12dc2b65b977eb05d96d167f`.
720p proxy, measured duration 746.021333 seconds. First/last five minutes, repaired Saturn → Earth and Sun → Gliese joins, plus thirteen brightest two-second windows. A Saturn excerpt still was inspected; no playback/listening claim. Segment boundaries are review jumps.

## Next run — no rerender or copy needed

`$SCRATCH` is the MacBook's `_desk/J2452-sleep-scratch` folder.

1. Run `resume_master_safety_copy.py --scratch "$HOME/_desk/J2452-sleep-scratch" --destination /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/sleep_video_01_master_v01.mp4 --seconds-budget 1080` (without `--copy-only`). It verifies the source, then hashes the full-size destination directly, avoiding a redundant complete byte-comparison pass. It also checks mux packet payloads. No delivery claim until local `MASTER_DELIVERY_V01.json` exists. Expected master SHA-256: `05b439cbc3a0ab77d006f571f79fb8d0d9b3054a0023250c569941c70887d698`.
2. Preserve the existing reel: do not rerun its renderer or exclusive-create copy helper. Its verified `REEL_DELIVERY_V01.json` is already in local scratch and sanitized in `final_join_v04/`.
3. Complete WATCH_CARD_DRAFT_V01.md with verified master/reel paths and hashes. Keep version-one scope: source charts/labels remain; dissolves only on compilation edits; earliest air date 12 December. Running order is in the draft.
4. Only after full master hash PASS, set awaits/UAT and finish, or park for Chief if the worker's awaits is refused. No upload until Ben OKs.

The copy helper now checkpoints its own clean timeout after closing file handles, keyed to source digest and destination size/mtime. This skips only an unchanged proven prefix on a later append; full destination SHA-256 remains mandatory for delivery. A mismatching checkpoint triggers the full prefix comparison. `--copy-only` explicitly leaves delivery unverified.

Validation: Python compilation, thirteen privacy tests and diff check pass. Both copy writers, reel renderer/decoder and reel copy/hash process exited. Stopped at the clean copy boundary because the full NAS hash needs a separate bounded run, within the user's 25-minute limit. OWB is restored to main after pushing; HOS is untouched.

Thread read to #6811073119 (status reported latest #6811273695).
