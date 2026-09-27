/**
 * Daily Buffer check (vercel.json crons): moves or removes Buffer posts when a
 * YouTube time changed or a video no longer goes public, and lists scheduled uploads
 * that were never mirrored. STUDIO_PLAYBOOK.md §12.
 */
import { NextRequest, NextResponse } from "next/server";
import { createMirrorDeps } from "@/lib/publishing/buffer-deps";
import { runBufferCheck } from "@/lib/publishing/buffer-runner";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";
export const maxDuration = 60;

export async function GET(request: NextRequest) {
  const secret = process.env.CRON_SECRET;
  if (!secret || request.headers.get("authorization") !== `Bearer ${secret}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  try {
    const dryRun = process.env.BUFFER_DRY_RUN === "true" || !process.env.BUFFER_API_KEY;
    const outcome = await runBufferCheck(createMirrorDeps(), { dryRun });
    const failed = outcome.changes.flatMap((c) => c.results.filter((r) => !r.ok).map((r) => ({ videoId: c.videoId, ...r })));
    const summary = {
      ok: failed.length === 0,
      dryRun,
      checked: outcome.checked,
      changes: outcome.changes.map((c) => ({ videoId: c.videoId, title: c.title, actions: c.actions.map((a) => `${a.channel}:${a.action}`) })),
      failed,
      unmirrored: outcome.unmirrored,
    };
    console.log(JSON.stringify({ bufferCheck: summary }));
    return NextResponse.json(summary, { status: failed.length ? 500 : 200 });
  } catch (e) {
    console.error(JSON.stringify({ bufferCheck: { error: (e as Error).message } }));
    return NextResponse.json({ ok: false, error: (e as Error).message }, { status: 500 });
  }
}
