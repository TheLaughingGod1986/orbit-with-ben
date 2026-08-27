import { NextRequest, NextResponse } from "next/server";
import {
  listPrograms,
  createProgram,
  updateProgram,
  getProgramPerformance,
} from "@/lib/affiliate/programs";
import { affiliateProgramInputSchema } from "@/lib/affiliate/schemas";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export const dynamic = "force-dynamic";

export async function GET() {
  const programs = await listPrograms();
  const withPerf = await Promise.all(
    programs.map(async (p) => ({
      ...p,
      performance: await getProgramPerformance(p.id),
    })),
  );
  return NextResponse.json({ programs: withPerf });
}

export async function POST(request: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const body = await request.json();
  const parsed = affiliateProgramInputSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const program = await createProgram(parsed.data);
  return NextResponse.json({ program }, { status: 201 });
}

export async function PATCH(request: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const body = await request.json();
  if (!body.id || typeof body.id !== "string") {
    return NextResponse.json({ error: "id required" }, { status: 400 });
  }
  const { id, ...rest } = body;
  const program = await updateProgram(id, rest);
  return NextResponse.json({ program });
}
