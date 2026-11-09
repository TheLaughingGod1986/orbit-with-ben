# J2185 — metadata transactions cannot publish worker history

5 November 2026, macbook. Proposed code change; elected-Chief system review required.

Both `jobs.with_git` and `studio.with_git` now use `studio.git_transaction`.
The transaction fails closed before applying a mutation unless the caller is on
main with a clean worktree/index. It fetches remote main and allows only a
fast-forward: unpublished or diverged local commits stop the operation.
Feature branches, detached HEADs and linked feature worktrees are not switched,
rebased or pushed. A common-Git-directory advisory lock serializes cooperating
metadata writers, including linked worktrees.

The callback runs after the fast-forward so concurrent queue updates are read
before applying the requested mutation. Only declared metadata paths are
committed. Before pushing, the helper verifies a single parent equal to the
fetched main and that every changed path belongs to the metadata path list.
The push names the verified commit SHA explicitly; it never uses HEAD:main.
No force push, autostash, rebase, reset or checkout is used.

A push race fails closed, preserving the local metadata commit and the other
writer's remote update. Further mutations refuse that unpublished/diverged
main until explicitly reconciled. This intentionally replaces the destructive
reset/retry path; it does not automatically replay preserved commits. Dirty
checkouts must be saved separately before using --git. The advisory lock does
not coordinate arbitrary manual Git commands; parent/path verification and
normal Git non-fast-forward rejection are additional safeguards.

## Validation

- `python3 -m unittest discover -s scripts -p test_metadata_git.py -v`: 4 tests
  PASS, including 10 feature/detached/ahead/diverged/worktree rejection subcases
  across queue and studio callers; clean-main writes; fast-forward preserving
  another agent's queue marker; dirty work/index preservation; rejected push
  preserving both histories and refusing an unsafe retry. All remotes are local
  temporary bare repositories; tests do not contact GitHub.
- `python3 -m unittest discover -s scripts -p test_studio.py`: 17 PASS.
- `python3 -m unittest discover -s scripts -p test_jobs.py`: 30 PASS.
- `python3 scripts/core_sync.py check`: 56 shared files PASS. None of the three
  changed scripts is listed in CORE_FILES.json, so no HOS copy/lock change is
  applicable. HOS checkout was not touched.
- `git diff --check`: PASS.

The J2179 incident's unsafe feature-branch invocation is reproduced as a
rejection with unchanged branch/HEAD, unchanged remote main, and absent
implementation.py on remote main. No production state or media was changed.
