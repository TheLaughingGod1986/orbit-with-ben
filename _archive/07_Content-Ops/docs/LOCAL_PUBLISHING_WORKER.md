# Local Publishing Worker

Orbit Content Ops runs on your laptop. Scheduled posts **do not** publish if:

- the Next.js server is stopped
- the worker process is not running
- the computer is asleep
- the network is offline

This is **not** cloud-level reliability. The UI surfaces worker online/offline from `WorkerHeartbeat`.

## Commands

```bash
npm run worker          # publishing worker only
npm run dev             # web UI only
npm run dev:all         # UI + worker together
```

## Behaviour

1. Poll due `PublishingJob` rows
2. Atomically claim with `lockedAt` / `lockedBy`
3. Validate connection + post
4. Publish through the platform adapter
5. Record each `PublishingAttempt`
6. Retry eligible failures with backoff + jitter
7. Recover stale locks (>15 minutes)
8. Heartbeat every poll cycle

### YouTube native schedule

For `youtube_shorts`, a future `scheduledAt` does **not** delay the claim. The worker uploads immediately with YouTube `publishAt`, then marks the post `scheduled` / job `awaiting_platform_processing`. The laptop only needs to be awake at **upload** time, not at air time.

Other platforms still wait until `scheduledAt <= now` unless they gain a native schedule path.

## Health

Overview and Connections show:

- Worker online / offline (heartbeat < 30s)
- Last heartbeat time
- Last processed job id

## Idempotency

Jobs use a stable `idempotencyKey` so restarts and dual workers cannot create duplicate successful publishes for the same post/media/schedule version.
