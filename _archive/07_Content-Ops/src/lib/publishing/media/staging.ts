import fs from "fs/promises";
import path from "path";
import { createHash } from "crypto";
import { getEnv } from "@/lib/env";

export type StagedMedia = {
  mode: "local_direct_upload" | "temporary_object_storage" | "existing_public_url" | "mock";
  localPath: string;
  publicUrl?: string;
  checksum: string;
  bytes: number;
  stagedAt: string;
};

export interface MediaStagingProvider {
  stageMedia(filePath: string): Promise<StagedMedia>;
  validateMedia(stagedMedia: StagedMedia): Promise<boolean>;
  deleteMedia(stagedMedia: StagedMedia): Promise<void>;
}

async function checksumFile(filePath: string): Promise<{ checksum: string; bytes: number }> {
  const buf = await fs.readFile(filePath);
  return {
    checksum: createHash("sha256").update(buf).digest("hex"),
    bytes: buf.length,
  };
}

export class LocalDirectUploadStaging implements MediaStagingProvider {
  async stageMedia(filePath: string): Promise<StagedMedia> {
    const abs = path.resolve(filePath);
    await fs.access(abs);
    const { checksum, bytes } = await checksumFile(abs);
    return {
      mode: "local_direct_upload",
      localPath: abs,
      checksum,
      bytes,
      stagedAt: new Date().toISOString(),
    };
  }
  async validateMedia(staged: StagedMedia): Promise<boolean> {
    try {
      await fs.access(staged.localPath);
      return staged.bytes > 0;
    } catch {
      return false;
    }
  }
  async deleteMedia(): Promise<void> {
    // Local source files are never deleted.
  }
}

/** Test-only mock — never presented as production hosting. */
export class MockStagingProvider implements MediaStagingProvider {
  async stageMedia(filePath: string): Promise<StagedMedia> {
    return {
      mode: "mock",
      localPath: filePath,
      publicUrl: `https://example.test/mock/${path.basename(filePath)}`,
      checksum: "mock",
      bytes: 1,
      stagedAt: new Date().toISOString(),
    };
  }
  async validateMedia(): Promise<boolean> {
    return true;
  }
  async deleteMedia(): Promise<void> {}
}

export class PublicUrlStaging implements MediaStagingProvider {
  constructor(private baseUrl: string) {}
  async stageMedia(filePath: string): Promise<StagedMedia> {
    const abs = path.resolve(filePath);
    const { checksum, bytes } = await checksumFile(abs);
    const name = path.basename(abs);
    return {
      mode: "existing_public_url",
      localPath: abs,
      publicUrl: `${this.baseUrl.replace(/\/$/, "")}/${name}`,
      checksum,
      bytes,
      stagedAt: new Date().toISOString(),
    };
  }
  async validateMedia(staged: StagedMedia): Promise<boolean> {
    return Boolean(staged.publicUrl);
  }
  async deleteMedia(): Promise<void> {}
}

export function getMediaStagingProvider(): MediaStagingProvider {
  const env = getEnv();
  if (env.MEDIA_STAGING_MODE === "existing_public_url" && env.MEDIA_PUBLIC_BASE_URL) {
    return new PublicUrlStaging(env.MEDIA_PUBLIC_BASE_URL);
  }
  return new LocalDirectUploadStaging();
}
