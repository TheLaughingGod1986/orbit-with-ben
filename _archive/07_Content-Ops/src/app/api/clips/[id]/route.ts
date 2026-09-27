import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import { assertClipTransition } from "@/lib/publishing/status";
import { scoreClipQuality } from "@/lib/content/quality-score";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function PATCH(
  req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const { id } = await ctx.params;
  const body = await req.json();
  const clip = await prisma.shortClip.findUnique({ where: { id } });
  if (!clip) return NextResponse.json({ error: "Clip not found" }, { status: 404 });

  const data: Record<string, unknown> = {};
  if (body.status) {
    try {
      assertClipTransition(clip.status, body.status);
    } catch (err) {
      return NextResponse.json(
        { error: err instanceof Error ? err.message : "Invalid transition" },
        { status: 400 },
      );
    }
    data.status = body.status;
  }

  for (const key of [
    "workingTitle",
    "hook",
    "hookCategory",
    "transcript",
    "sourceStartTime",
    "sourceEndTime",
    "targetDurationSeconds",
    "visualDirection",
    "onScreenText",
    "endingLine",
    "callToAction",
    "sortOrder",
  ] as const) {
    if (body[key] !== undefined) data[key] = body[key];
  }

  if (
    body.hook !== undefined ||
    body.transcript !== undefined ||
    body.callToAction !== undefined ||
    body.targetDurationSeconds !== undefined
  ) {
    const quality = scoreClipQuality({
      hook: (body.hook as string) ?? clip.hook,
      hookCategory: (body.hookCategory as string) ?? clip.hookCategory,
      transcript: (body.transcript as string) ?? clip.transcript,
      endingLine: (body.endingLine as string) ?? clip.endingLine,
      callToAction: (body.callToAction as string) ?? clip.callToAction,
      visualDirection: (body.visualDirection as string) ?? clip.visualDirection,
      targetDurationSeconds:
        (body.targetDurationSeconds as number) ?? clip.targetDurationSeconds,
    });
    data.qualityScore = quality.total;
    data.qualityBreakdown = JSON.stringify(quality);
  }

  const updated = await prisma.shortClip.update({ where: { id }, data });
  return NextResponse.json(updated);
}
