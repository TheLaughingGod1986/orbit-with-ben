# Publishing gates (J3291)

The upload preflight and upcoming-video report now call `scripts/publishing_gates.py`.
They recompute Shorts opening, music, picture QA (including polish) and SFX level checks.
Missing inputs, changed export hashes, unknown channel-required gates and tool errors
block upload. Dry runs enforce the same checks. `approved_deliver.py` only queues work.

Export metadata needs `sha256` for the exact export, plus these `publishing_gates`
inputs (paths relative to the metadata, or absolute paths):

```json
{
  "publishing_gates": {
    "film": "../../..",
    "bed": "../../../05_Music/score.mp3",
    "cuts": "cuts.json",
    "pool": "pool.json",
    "vo": "vo.wav",
    "sfx": "sfx.wav",
    "reviewed_ok": "reviewed_ok.json"
  }
}
```

`pool`, `reviewed_ok` and `terminal_loop` are optional picture-QA inputs; all other
listed inputs are required. The cut-list schema is picture_qa's existing schema.
Previously recorded gate PASS strings do not substitute for source inputs.
Music waivers retain the existing named-bed `music_gate_*_chief_waiver.json`
format. Picture review rulings retain the existing `reviewed_ok` format. Shorts
waivers use exact findings in the export's `_gate.json`, with a Chief attribution.
Tool errors cannot be waived. No gate failure creates an automatic waiver.

Refill queues one daily `scheduled_gates.py --apply --git` job. It checks every
registered channel's private scheduled Shorts and longs in the next fourteen days,
using a snapshot taken within 36 hours. No success cache skips videos when a gate
changes. A prelaunch channel with no snapshots is skipped. Incomplete sweeps must
stay open for retry; workers must not mark them complete. The sweep never calls
YouTube. Failures within seven days produce one live Chief fix job per video.
Chief determines whether a repair requires a new finished-cut watch and then uses
the existing `awaits_ben` flow; coverage/metadata findings alone never alert Ben.

## Rollout still required

This PR changes the canonical Orbit engine only. Shared upload files are hash
locked by `studio-core/CORE_FILES.json`; Chief must arrange the matching HOS core
rollout before calling this an all-channel upload guard. Channel-specific required
gates beyond the standard three currently fail closed until a runner is supplied.
Existing export sidecars need explicit input paths before uploads can resume.
The new daily sweep does not stage the full music library for a launchd sandbox;
it runs as a worker job and needs readable media. No production sweep was run by
J3291 on the MacBook. The dedicated deadline-alert integration remains outstanding.
