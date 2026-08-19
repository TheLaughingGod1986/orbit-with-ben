import { NextRequest, NextResponse } from "next/server";
import {
  previewConversionImport,
  commitConversionImport,
} from "@/lib/affiliate/conversions";
import { AFFILIATE_CSV_DEFAULT_MAPPINGS } from "@/lib/affiliate/csv-import";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const body = await request.json();
  const csv = body.csv as string | undefined;
  if (!csv?.trim()) {
    return NextResponse.json({ error: "csv required" }, { status: 400 });
  }

  const source = (body.source as string) || "generic";
  const mapping =
    body.mapping ||
    AFFILIATE_CSV_DEFAULT_MAPPINGS[source] ||
    AFFILIATE_CSV_DEFAULT_MAPPINGS.generic;

  if (body.dryRun !== false && body.commit !== true) {
    const result = await previewConversionImport({
      csvText: csv,
      source,
      mapping,
    });
    return NextResponse.json(result);
  }

  if (!body.programmeSlug) {
    return NextResponse.json({ error: "programmeSlug required to commit" }, { status: 400 });
  }

  const result = await commitConversionImport({
    csvText: csv,
    source,
    programmeSlug: body.programmeSlug,
    filename: body.filename,
    mapping,
    dryRun: Boolean(body.dryRun),
  });
  return NextResponse.json(result);
}
