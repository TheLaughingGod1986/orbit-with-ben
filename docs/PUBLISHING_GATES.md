# Publishing gates (J3291)

The upload preflight (`07_Content-Ops/scripts/youtube-package-upload.ts` via
`07_Content-Ops/src/lib/publishing/shorts-gate.ts`) and the 14-day scheduled-video
sweep (`00_Brand/Channel-Setup/tools/gate_upcoming.py` via `scripts/scheduled_gates.py`)
both call `scripts/publishing_gates.py`.

They recompute every blocking gate the film's channel requires for Shorts and longs
before anything is sent to YouTube — never trusting recorded PASS strings. Dry runs
enforce the exact same gates. `scripts/approved_deliver.py` queues `youtube:package`
jobs rather than uploading directly.

## Blocking gates per channel

Each channel's `studio/channel.json` may declare `publishing_gates.by_format`
(`short` / `long`) and additive `publishing_gates.required`. Defaults when unset:

- **Orbit With Ben (`owb`)**:
  - Shorts: `shorts_open` (`gate_shorts_open.py`), `music` (`music_gate.py`), `sfx` (`sfx_kit.py level`), plus `picture` (`picture_qa.py`) when a cut list is supplied.
  - Longs: `music`, `picture` (`picture_qa.py`, which runs `polish_gate.py`), `sfx`.
- **History of Science (`hos`)**:
  - Shorts: `shorts_open`, `music`, `sfx`, `lint_package` (`07_Content-Ops/scripts/package-lint.ts`).
  - Longs: `music`, `sfx`, `lint_package`.
- **Field Order History (`ww2`)**:
  - Shorts: `shorts_open`, `music`.
  - Longs: `music`, `archive_provenance` (`03_Picture/ARCHIVE_PROVENANCE.md`).

Any unknown gate name added to `studio/channel.json` fails closed until its runner is wired.
`youtube-package-upload.ts` resolves the owning channel checkout from `--package` so
multi-channel uploads (e.g. WW2 packages uploaded from the studio ops CLI) run that
channel's own gate set.

## Input resolution and waivers

Explicit inputs in `<export>_meta.json` under `publishing_gates` take priority, with
export SHA-256 verification whenever a hash is recorded in metadata or `UPLOADS.json`:

```json
{
  "sha256": "<export sha256>",
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

For existing exports whose sidecars predate `publishing_gates`, `publishing_gates.py`
deterministically derives the film folder (`02_Video-Projects/<film>` or NAS `studio-live`),
`05_Music` bed, adjacent `_vo`/`_sfx`/`_bed` stems, and `_cuts`/`_pool`/`_reviewed_ok` files.
If a required input cannot be resolved, the gate fails closed.

Waivers use each gate's existing format and never waive tool errors (exit 2):

- **Music**: `05_Music/music_gate_*_chief_waiver.json` (`accept: true`, exact `bed` filename, `waive: ["reused"]`).
- **Shorts opening**: `<export>_gate.json` (`waivers: [{"fail": "<exact line>", "waived_by": "Chief ..."}]`).
- **Picture QA**: `--reviewed-ok` JSON.

## Daily 14-day scheduled sweep and alerts

`scripts/refill.py` queues one daily `python3 scripts/scheduled_gates.py --apply --git` job
per London day. It checks every registered channel's scheduled Shorts and longs in the next
14 days (merging studio `social/<slug>/UPLOADS.json` with the channel's own `UPLOADS.json`
so HOS Shorts registered for Buffer are always found), with no PASS cache so tightened or
newly added gates re-check everything already scheduled.

- **Per-channel fault isolation**: a prelaunch channel with no snapshots or upload register
  is skipped cleanly; a stale (>36 h) or missing snapshot on a live channel is reported as an
  explicit coverage error without blocking the remaining channels from being checked and queued.
- **Urgent Chief fixes (< 7 days)**: any unwaived FAIL airing within 7 days queues one
  deduplicated urgent `kind: chief` fix job.
- **Ben's alert (J3292 integration)**: `raise_ben_alert_if_needed` arms Ben's alert ONLY when
  a cut-level gate (`shorts_open`, `music`, `picture`, `sfx`) failed (`needs_watch: true`),
  delegating to `scripts/urgent_alerts.py` when present and deduplicating via board state.
  Metadata, missing-input, coverage or package-lint findings never alert Ben.

## Post-merge rollout

`studio-core/CORE_FILES.json` locks the shared upload and gate files (`youtube-package-upload.ts`,
`shorts-gate.ts`, `shorts-gate.test.ts`, `music_gate.py`, `publishing_gates.py`). Once this PR
merges to `orbit-with-ben` `main`, run `python3 scripts/core_sync.py push --to "../History Of Science"`
to land the matching core files in History of Science.
