import { NextRequest, NextResponse } from "next/server";
import { getGearCatalog } from "@/lib/affiliate/gear";

export const dynamic = "force-dynamic";

/** Phase 5 prep — public-ready gear catalogue JSON for orbitwithben.com/gear */
export async function GET(request: NextRequest) {
  const sp = request.nextUrl.searchParams;
  const catalog = await getGearCatalog({
    category: sp.get("category") || undefined,
    tag: sp.get("tag") || undefined,
    featuredOnly: sp.get("featured") === "true",
  });
  return NextResponse.json(catalog, {
    headers: {
      "Cache-Control": "public, s-maxage=300, stale-while-revalidate=600",
    },
  });
}
