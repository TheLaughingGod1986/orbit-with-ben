# J3885 — MacBook engine preparation

27 November 2026. Agent `macbook`. Preparation only; J3012 retains the coordinated drain and live switch. No service was paused, stopped, installed or started. No active-engine marker was created. No board, film, credential, origin or remote default was changed. No rehearsal queue writer or queue selection was run.

Both independent engine clones are staged from private `TheLaughingGod1986/studio`, branch `rehearsal/j3012-20261127`, at exact parentless commit `eda81876dc28c11b6a0d7b6cb0281b801bfd00c9`:

- Slot 1: `~/_desk/worker/studio`.
- Slot 2: `~/_desk/worker/slot2/studio`.

Both were absent before staging. Both now have clean local `main` branches at that exact source, with no remote `main` published. They have no home-channel property, retain the explicit Orbit thread repository, and contain no active workflow YAML. Git clone access succeeded with the existing credentials; GitHub metadata independently confirmed PRIVATE. The rehearsal queue remains stale and inactive; it must be replaced from the coordinated frozen source before live work.

Each slot retains its separate `orbit-with-ben`, `history-of-science` and `ww2-channel` content roots, all observed on clean `main`. No content checkout was reset or updated by this preparation. The old slot-1 source before progress recording was `cda850825091c1b13e87aaccd747f325313d1ebf`; old slot-2 source was `653ad408aac867d93d99a1843aa7b5d079277d22`. Both old worker files have identical SHA-256 and contain `require_active` retirement enforcement and the worker pause check. These are code-presence observations, not a live drain demonstration.

## Installed policy and private rollback material

The installed `com.owb.macbook-worker` plist was parsed, and its loaded launchd definition read successfully: running. One shared service starts both slots; there is no second worker service to install. Its bootstrap is an inline zsh command, saved separately rather than inventing an external wrapper file.

Private directory: `~/_desk/state/j3885-preparation/` (mode 0700). Backups and proposal are mode 0600:

- `installed.plist`: exact installed service definition.
- `installed-bootstrap.zsh`: exact inline bootstrap text, backup only.
- `loaded-private.txt`: full loaded definition, private only.
- `old-worker.py`: retained old worker source backup.
- `future-renderer.py`: exact rehearsal renderer backup.
- `proposed.plist`: staged replacement proposal, **not installed**.

Exact SHA-256 values are in `EVIDENCE.json`. No plist, loaded environment values, model value or loaded device details are published.

The proposal was generated with the rehearsal's `scripts/macbook/render_worker_plist.py`, then combined with the actual installed definition: all existing environment values and every non-bootstrap service setting are preserved exactly. Only the engine bootstrap and the two new engine environment entries change. The engine root becomes slot 1's new studio clone; existing Orbit and HOS content roots stay as installed. No setup script was run.

No loaded `MACBOOK_*` overrides were observed. Therefore current source defaults remain: mains power required, two slots, round-the-clock policy, slot 1 may work during user activity at background priority, slot 2 requires ten minutes idle, 15 GB minimum free, 1500-second job cap, 13-minute loop budget, installed tool detection with the existing routing chain. The proposal retains the installed PATH and local text-model policy. Both old workers contain the same policy code.

At observation slot 1's lock was held, slot 2's lock existed but was not held. The only claimed MacBook job in the authoritative local queue was J3885, owned by `macbook`. Pause and active-engine marker were absent. No locks were deleted or edited.

## Verification

- `plutil -lint` on the staged proposal: OK.
- Installed service settings and environment equality assertions: passed.
- Offline rehearsal suite: `test_macbook_launcher`, `test_macbook_worker`, `test_engine_guard`: **104 tests passed**. Tests use fake launch commands, temporary Git repositories and mocked dispatch; no worker run was launched against the rehearsal. Two mocked legacy tests attempted to open the existing log path and were sandbox-refused; the suite still passed. The additional slot test below uses a temporary log directory.
- An additional mocked `start_other_slots` test loaded the **actual future registry** and verified slot 2 receives its own `STUDIO_REPO`, `OWB_REPO`, `HOS_REPO` and `WW2_REPO`, each under `~/_desk/worker/slot2`, without starting a subprocess.
- Both engine heads, zero-parent ancestry, clean trees, retained thread repo, lack of home property and absence of workflow YAML: asserted.

No live migration acceptance is claimed. The frozen production queue, final source refresh, coordinated drain, installed/loaded switch, relay cycle, board publication and tick round-trip remain J3012's gates.

## How to deliver the next instruction

Use the existing authoritative queue and installed MacBook worker, as for this child: a new `needs macbook` preparation/cutover job with an explicit brief and the Chief's coordination. Do not make it depend on completion of J3012, which would create a cycle. The currently installed old worker receives it on its normal tick. A drain/install instruction must account for its own claimed job and both slots, then use the existing pause mechanism and verify other writers have drained before installation. This report grants no authority to perform that next phase. No SSH reachability is claimed or required.

No concrete blocker to this staging remains. The private proposal is ready for Chief review against the final frozen source. J3012 remains open.
