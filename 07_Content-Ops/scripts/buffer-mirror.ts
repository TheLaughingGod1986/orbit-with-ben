#!/usr/bin/env tsx
/**
 * Mirror a YouTube upload to Instagram, Facebook and Threads through Buffer
 * (STUDIO_PLAYBOOK.md §12). `npm run youtube:package` already does this after every
 * live upload; use this for anything uploaded another way, or to re-run one.
 *
 *   # Short: hosts the mp4 on the public Blob store, then schedules all three posts
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts mirror --video <shortId> --long <longId> --media <short.mp4>
 *   # Long: Instagram gets the thumbnail; Facebook and Threads get the YouTube link card
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts mirror --video <longId> --thumb <thumb.jpg>
 *   # See what it would do, without hosting or posting (also saves the plan for the MCP route)
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts plan --video <id> …
 *   # Keep Buffer in step with Studio, and mirror scheduled uploads made outside youtube:package
 *   # (daily on the Mac via launchd; run it after any Studio change)
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts check [--dry-run]
 *   # Tell the daily check which file an upload came from, when it was uploaded by hand
 *   npx tsx scripts/buffer-mirror.ts register --video <shortId> --media <short.mp4> --long <longId>
 *   npx tsx scripts/buffer-mirror.ts register --video <longId> --thumb <thumb.jpg>
 *   # Only when a plan was sent by hand through the Buffer MCP
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts record --video <id> --channel instagram --post-id <bufferPostId>
 *
 * Needs .env: GOOGLE_CLIENT_ID/SECRET, YOUTUBE_REFRESH_TOKEN (scripts/youtube-auth.ts),
 * BUFFER_API_KEY, BLOB_READ_WRITE_TOKEN. Without the Buffer key it plans only.
 * What was posted is kept in 00_Brand/Channel-Setup/social/BUFFER_POSTS.json: commit it.
 * Flags: --standalone (a Short with no long), --allow-late (back catalogue, Ben's OK),
 * --media-url / --thumb-url (already public files), --kind short|long.
 */
import fs from "fs";
import path from "path";
import { BUFFER_CHANNELS, type BufferChannel, type Plan } from "../src/lib/publishing/buffer-mirror";
import { REPO_ROOT, SOCIAL_DIR, UPLOADS_FILE, createMirrorDeps } from "../src/lib/publishing/buffer-deps";
import { registerUpload } from "../src/lib/publishing/media-finder";
import { mirrorVideo, runBufferCheck } from "../src/lib/publishing/buffer-runner";

const PLANS_DIR = path.join(SOCIAL_DIR, "buffer-plans");

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}
const flag = (name: string) => process.argv.includes(`--${name}`);

function localFile(p: string | undefined): string | null {
  if (!p) return null;
  const abs = path.resolve(p);
  if (!fs.existsSync(abs)) throw new Error(`File not found: ${p}`);
  return abs;
}

function savePlan(plan: Plan) {
  fs.mkdirSync(PLANS_DIR, { recursive: true });
  const out = path.join(PLANS_DIR, `${plan.videoId}.json`);
  fs.writeFileSync(out, JSON.stringify({ plannedAt: new Date().toISOString(), ...plan }, null, 2) + "\n");
  return path.relative(process.cwd(), out);
}

async function mirror(dryRun: boolean) {
  const videoId = arg("video");
  if (!videoId) throw new Error("needs --video <youtube id>");
  const deps = createMirrorDeps();
  if (!dryRun && !deps.client) console.error("BUFFER_API_KEY not set: planning only.");
  const outcome = await mirrorVideo(
    {
      videoId,
      kind: arg("kind") as "short" | "long" | undefined,
      longId: arg("long") ?? null,
      standalone: flag("standalone"),
      mediaPath: localFile(arg("media")),
      mediaUrl: arg("media-url"),
      thumbPath: localFile(arg("thumb")),
      thumbUrl: arg("thumb-url"),
      allowLate: flag("allow-late"),
      dryRun,
    },
    deps,
  );
  const saved = savePlan(outcome.plan);
  console.log(JSON.stringify({ ...outcome, savedPlan: saved }, null, 2));
  const failed = outcome.plan.errors.length > 0 || outcome.results.some((r) => !r.ok);
  if (failed) process.exit(1);
}

async function check() {
  const deps = createMirrorDeps();
  const outcome = await runBufferCheck(deps, { dryRun: flag("dry-run") });
  for (const c of outcome.changes) {
    savePlan({
      videoId: c.videoId,
      kind: c.kind,
      title: c.title,
      youtubeUrl: "",
      timing: c.timing,
      actions: c.actions,
      errors: [],
      warnings: [],
    });
  }
  console.log(JSON.stringify(outcome, null, 2));
  const failed =
    outcome.changes.some((c) => c.results.some((r) => !r.ok)) || outcome.autoMirrored.some((m) => m.results.some((r) => !r.ok));
  // Unmirrored uploads need a person (register the file), so they fail the run too: the log shows why.
  if (failed || outcome.unmirrored.length) process.exit(1);
}

function register() {
  const videoId = arg("video");
  const media = localFile(arg("media"));
  const thumb = localFile(arg("thumb"));
  const long = arg("long");
  const standalone = flag("standalone");
  if (!videoId || (!media && !thumb)) throw new Error("register needs --video <id> and --media <mp4> (Short) or --thumb <jpg> (long)");
  if (media && !long && !standalone) throw new Error("a Short needs --long <longId> (or --standalone)");
  const reg = registerUpload(UPLOADS_FILE, REPO_ROOT, videoId, {
    kind: media ? "short" : "long",
    file: media ?? undefined,
    thumb: thumb ?? undefined,
    long: long ?? undefined,
    standalone: standalone || undefined,
  });
  console.log(JSON.stringify({ registered: videoId, entry: reg.videos[videoId] }, null, 2));
}

async function record() {
  const videoId = arg("video");
  const channel = arg("channel") as BufferChannel | undefined;
  const postId = arg("post-id");
  const deleted = flag("deleted");
  if (!videoId || !channel || !BUFFER_CHANNELS.includes(channel) || (!postId && !deleted)) {
    throw new Error("record needs --video <id> --channel instagram|facebook|threads and --post-id <id> or --deleted");
  }
  const planFile = path.join(PLANS_DIR, `${videoId}.json`);
  if (!fs.existsSync(planFile)) throw new Error(`No saved plan for ${videoId}; run plan first`);
  const plan = JSON.parse(fs.readFileSync(planFile, "utf8")) as Plan;
  await createMirrorDeps().store.record(plan, channel, deleted ? null : postId!);
  console.log(JSON.stringify({ recorded: videoId, channel, postId: deleted ? null : postId }));
}

async function main() {
  const cmd = process.argv[2];
  if (cmd === "mirror") await mirror(flag("dry-run"));
  else if (cmd === "plan") await mirror(true);
  else if (cmd === "check") await check();
  else if (cmd === "record") await record();
  else if (cmd === "register") register();
  else {
    console.error("Usage: buffer-mirror.ts mirror|plan|check|register|record  (see the header of this file)");
    process.exit(1);
  }
}

main().catch((e) => {
  console.error(e instanceof Error ? e.message : e);
  process.exitCode = 1;
});
