# Orbit Content Ops (local CLIs)

Command-line tools for **Orbit With Ben**. There is no web app and no database: the hosted ops app (Vercel project `orbit-content-ops`, Neon Postgres) was retired on 27 Sep 2026 and lives in `_archive/07_Content-Ops/`.

## Vercel / `/go` door (do not auto-deploy)

The live affiliate door is still **https://orbit-content-ops.vercel.app/go** (Vercel project `orbit-content-ops`, root `07_Content-Ops`, Amazon tag `orbitgo-21` in Vercel env only). Git must **not** create deployments for this project: every push used to open a CANCELED Ignored Build Step deploy, and those **count** toward the Hobby `api-deployments-free-per-day` (100/day) quota.

- Project: Git Hub `createDeployments` is **disabled**, and `vercel.json` has `"git": { "deploymentEnabled": false }`.
- `ignoreCommand` / `scripts/vercel-ignore-build.sh` stays as a backstop if git deploys are ever re-enabled.
- Studio/jobs/board pushes to `main` must not touch this project's deploy quota.

### Ship a real `/go` change (Chief OK only)

1. Get **Chief OK** (Ben via Chief of Staff).
2. From a machine signed into Vercel team **ben's projects**, with the CLI linked to `orbit-content-ops`:
   ```bash
   cd 07_Content-Ops
   vercel --prod
   ```
3. Confirm `https://orbit-content-ops.vercel.app/go` returns **200** and a known slug (e.g. `/go/jwst-book`) still redirects with `tag=orbitgo-21`.
4. Do **not** reconnect git auto-deploy, pause, delete the project, or change env vars unless Ben asked.

Note: today's `07_Content-Ops` tree is local CLIs (no Next.js). The door is the last READY Next deploy from before the 27 Sep ops-app retire. If you need to change `/go` code, restore the Next app into this root (or point the project Root Directory at the restored app) **before** `vercel --prod`, or you will overwrite the live door with a non-app build. Money King owns the door; ask Chief before either restore or prod CLI deploy.

## Setup (once)

```bash
cd 07_Content-Ops
cp .env.example .env      # fill in locally; never commit or print values
npm install
npm run youtube:auth      # sign in as Orbit With Ben; saves YOUTUBE_REFRESH_TOKEN into .env
```

## Commands

| Command | Purpose |
|---------|---------|
| `npm run review:script -- --file <script.md>` | Script reviewer (long scripts need 90+) |
| `npm run gate:episode -- --project <…>` | Episode gate (blocks VO/picture until PASS) |
| `npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> [--dry-run]` | Upload to YouTube, then mirror to Buffer (`--no-buffer` to skip) |
| `npx tsx --env-file=.env scripts/retitle-videos.ts --file <fixes.json> --dry-run` | Title-only changes |
| `npx tsx --env-file=.env scripts/update-pinned-comment.ts --dry-run` | Weekly pinned-comment refresh |
| `npm run buffer:mirror -- --video <id> --long <longId> --media <mp4>` | Mirror an upload made another way to Buffer |
| `npm run buffer:check` | Keep Buffer in step with Studio, and mirror scheduled uploads not in Buffer yet (the Mac runs it daily: `launchd/dev.orbit.buffer-check.plist`) |
| `npx tsx scripts/buffer-mirror.ts register --video <id> --media <mp4> --long <longId>` | Tell the daily check which file a hand-made upload came from |
| `npm run diagnose:youtube -- --file <metrics.json>` / `npm run brief:next` | Growth diagnostics and next-episode brief |
| `npm test` / `npm run typecheck` / `npm run lint` | Checks |

Rules for all of it: `AGENTS.md` and `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` (§9 upload, §12 Buffer).

### Mini writer lock

YouTube uploads, listing/comment/disclosure writers and every Buffer CLI command
acquire the shared `youtube-buffer` lock, including direct `npx tsx` calls and the
daily shell wrapper. The atomic mkdir lock lives at
`~/_desk/locks/youtube-buffer.lock/`; `DESK_LOCK_ROOT` overrides the root for tests.
It covers the entire command, including an upload's Buffer mirror and local
records. Dry runs also take the lock.

A held lock stops with exit **75**. Wait for the owner to finish; inspect with
`bash scripts/desk-lock.sh held-by youtube-buffer`. Acquisition reclaims a lock
only when the owner pid is dead **and** `owner.txt` is older than 5 minutes
(SIGKILL leftovers). Missing or fresh owner metadata stays held, since another
process may still be writing it. Force-clear with
`DESK_LOCK_FORCE=1 bash scripts/desk-lock.sh release youtube-buffer` only when
ops has verified it is safe.

`launchd/buffer-check.sh` stays quiet on a single exit 75 (temporary contention).
A second consecutive 75 posts a macOS notification so a stuck lock cannot stall
the daily mirror silently.

`youtube-package-upload.ts` refuses a second live upload of the same package +
file sha256 unless `--force-new`. Buffer mirror already skips channels that have
a post id, and `executeActions` re-checks the ledger under the lock before each
create.
