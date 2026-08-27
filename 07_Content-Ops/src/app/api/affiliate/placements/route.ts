import { NextRequest, NextResponse } from "next/server";
import {
  generateRecommendationsForVideo,
  regeneratePlacementsForVideo,
  upsertPlacement,
  setPlacementStatus,
  removePlacement,
  listPlacementsForVideo,
  EditorialTrustGateError,
} from "@/lib/affiliate/placements";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  const videoId = request.nextUrl.searchParams.get("videoId");
  if (!videoId) {
    return NextResponse.json({ error: "videoId required" }, { status: 400 });
  }
  const placements = await listPlacementsForVideo(videoId);
  return NextResponse.json({ placements });
}

export async function POST(request: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const body = await request.json();
  const action = body.action as string | undefined;

  try {
    if (action === "recommend") {
      if (!body.videoId) {
        return NextResponse.json({ error: "videoId required" }, { status: 400 });
      }
      const result = await generateRecommendationsForVideo(body.videoId);
      return NextResponse.json(result);
    }

    if (action === "regenerate") {
      if (!body.videoId) {
        return NextResponse.json({ error: "videoId required" }, { status: 400 });
      }
      const result = await regeneratePlacementsForVideo(body.videoId, {
        replaceAll: Boolean(body.replaceAll),
        autoApprove: Boolean(body.autoApprove),
      });
      return NextResponse.json(result);
    }

    if (action === "status") {
      if (!body.placementId || !body.status) {
        return NextResponse.json(
          { error: "placementId and status required" },
          { status: 400 },
        );
      }
      const placement = await setPlacementStatus(body.placementId, body.status);
      return NextResponse.json({ placement });
    }

    if (action === "remove") {
      if (!body.placementId) {
        return NextResponse.json({ error: "placementId required" }, { status: 400 });
      }
      const placement = await removePlacement(body.placementId);
      return NextResponse.json({ placement });
    }

    const placement = await upsertPlacement(body);
    return NextResponse.json({ placement }, { status: 201 });
  } catch (err) {
    if (err instanceof EditorialTrustGateError) {
      return NextResponse.json(
        { error: err.message, failures: err.failures, trustGate: true },
        { status: 422 },
      );
    }
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Invalid placement" },
      { status: 400 },
    );
  }
}
