import { NextRequest, NextResponse } from "next/server";
import { recordAffiliateClickAndResolve } from "@/lib/affiliate/tracking";
import { normalizeAffiliateClickSource } from "@/lib/affiliate/social-channels";

export const dynamic = "force-dynamic";

/**
 * Tracked affiliate redirect: /go/{slug}?utm_source=threads|instagram|facebook|youtube&…
 * Records click with normalised source, then 302 to the programme affiliate URL.
 * Missing utm_source → `other` (not youtube) so probes are not counted as YouTube.
 */
export async function GET(
  request: NextRequest,
  context: { params: Promise<{ slug: string }> },
) {
  const { slug } = await context.params;
  const sp = request.nextUrl.searchParams;

  try {
    const result = await recordAffiliateClickAndResolve({
      productSlug: slug,
      videoId: sp.get("video"),
      videoSlug: sp.get("v") || sp.get("utm_campaign"),
      placementId: sp.get("placement"),
      source: normalizeAffiliateClickSource(sp.get("utm_source")),
      medium: sp.get("utm_medium") || "affiliate",
      campaign: sp.get("utm_campaign"),
      content: sp.get("utm_content") || slug,
      userAgent: request.headers.get("user-agent"),
      referrer: request.headers.get("referer"),
    });

    return NextResponse.redirect(result.destinationUrl, 302);
  } catch {
    return NextResponse.json(
      { error: "Affiliate link not found" },
      { status: 404 },
    );
  }
}
