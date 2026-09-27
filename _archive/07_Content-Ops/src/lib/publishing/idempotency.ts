import { createHash } from "crypto";

export function buildIdempotencyKey(input: {
  platform: string;
  platformConnectionId: string;
  platformPostId: string;
  mediaChecksum?: string | null;
  scheduleVersion?: string | null;
}): string {
  const raw = [
    input.platform,
    input.platformConnectionId,
    input.platformPostId,
    input.mediaChecksum || "nochecksum",
    input.scheduleVersion || "v1",
  ].join("|");
  return createHash("sha256").update(raw).digest("hex");
}
