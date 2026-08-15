import { NextRequest, NextResponse } from "next/server";
import {
  applyLiveProductUrls,
  getAffiliateGoLiveReport,
} from "@/lib/affiliate/go-live-service";

export const dynamic = "force-dynamic";

/** GET — go-live readiness (no secrets in response). */
export async function GET(request: NextRequest) {
  const probe = request.nextUrl.searchParams.get("probe") === "1";
  const report = await getAffiliateGoLiveReport({ probeGoRoute: probe });
  return NextResponse.json(report);
}

/** POST { action: "apply-urls", dryRun?: boolean } — write live destination URLs. */
export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => null);
  if (!body || body.action !== "apply-urls") {
    return NextResponse.json({ error: "action must be apply-urls" }, { status: 400 });
  }
  const result = await applyLiveProductUrls({ dryRun: Boolean(body.dryRun) });
  const report = await getAffiliateGoLiveReport();
  return NextResponse.json({ ...result, report });
}
