# ROLLBACK PLAN

Source of truth: `PRE_REPAIR_ROLLBACK_STATE.json`

1. For each mutated videoId, restore `privacyStatus` + `publishAt` from the rollback JSON.
2. Prefer API `videos.update` with force-ssl; else Studio CDP visibility dialog.
3. Never delete to roll back.
4. Never re-upload to roll back.
5. Registry changes: restore `YOUTUBE_CANONICAL_REGISTRY.json` from git.

Mutations that cannot be rolled back (none planned): permanent delete, analytics reset.
