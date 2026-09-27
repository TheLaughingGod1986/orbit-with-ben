import { NextRequest, NextResponse } from "next/server";
import {
  enqueueAffiliateSocialSnippetsAsDrafts,
  getAffiliateSocialSnippetsForVideo,
} from "@/lib/affiliate/social-snippet-service";
import { assertAffiliateSafeSocialCopy } from "@/lib/affiliate/social-copy";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export const dynamic = "force-dynamic";

/**
 * GET ?videoId=… — copy-ready affiliate social snippets (draft / not auto-posted).
 * POST { action: "enqueue-drafts", videoId, clipId, platforms? } — push into PlatformPost drafts.
 */
export async function GET(request: NextRequest) {
  const videoId = request.nextUrl.searchParams.get("videoId");
  if (!videoId) {
    return NextResponse.json({ error: "videoId required" }, { status: 400 });
  }

  const pack = await getAffiliateSocialSnippetsForVideo(videoId);
  if (!pack) {
    return NextResponse.json({ error: "Video not found" }, { status: 404 });
  }

  for (const s of pack.snippets) {
    try {
      assertAffiliateSafeSocialCopy(s.caption);
    } catch (err) {
      return NextResponse.json(
        { error: err instanceof Error ? err.message : "Unsafe snippet" },
        { status: 422 },
      );
    }
  }

  return NextResponse.json({
    videoSlug: pack.videoSlug,
    placementApproved: pack.placementApproved,
    snippets: pack.snippets,
    note:
      "Snippets are draft-only. Approve description placement first; then enqueue drafts and approve each PlatformPost before publish.",
  });
}

export async function POST(request: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const body = await request.json().catch(() => null);
  if (!body || body.action !== "enqueue-drafts") {
    return NextResponse.json(
      { error: "action must be enqueue-drafts" },
      { status: 400 },
    );
  }
  if (!body.videoId || !body.clipId) {
    return NextResponse.json(
      { error: "videoId and clipId required" },
      { status: 400 },
    );
  }

  try {
    const result = await enqueueAffiliateSocialSnippetsAsDrafts({
      videoId: body.videoId,
      clipId: body.clipId,
      platforms: body.platforms,
    });
    return NextResponse.json(result);
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Enqueue failed" },
      { status: 422 },
    );
  }
}
