/**
 * Canonical YouTube upload registry — ONE package = ONE video ID.
 */
import { createHash } from "crypto";
import fs from "fs";
import path from "path";

export type CanonicalRegistryRecord = {
  internalContentId: string;
  contentType: "longform" | "shorts";
  sourceFileFingerprint: string;
  title: string;
  youtubeVideoId: string | null;
  uploadTimestamp: string | null;
  scheduledPublishTimestamp: string | null;
  privacyStatus: "private" | "public" | "unlisted" | null;
  packageVersion: string;
  metadataVersion: string;
  relatedLongFormVideoId: string | null;
  lastVerificationTimestamp: string | null;
  lastApiResponseStatus: string | null;
  packagePath?: string | null;
};

export type CanonicalRegistryFile = {
  version: number;
  updatedAt: string;
  records: CanonicalRegistryRecord[];
};

export type RegistryLookupResult = {
  blocked: boolean;
  matched: CanonicalRegistryRecord | null;
  reason: string | null;
};

export function resolveCanonicalRegistryPath(fromCwd = process.cwd()): string {
  const candidates = [
    path.resolve(fromCwd, "../00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json"),
    path.resolve(fromCwd, "00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json"),
    path.resolve(fromCwd, "../00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json"),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return candidates[0];
}

export function loadCanonicalRegistry(registryPath?: string): CanonicalRegistryFile {
  const p = registryPath || resolveCanonicalRegistryPath();
  if (!fs.existsSync(p)) {
    return { version: 1, updatedAt: new Date().toISOString(), records: [] };
  }
  return JSON.parse(fs.readFileSync(p, "utf8")) as CanonicalRegistryFile;
}

export function saveCanonicalRegistry(
  file: CanonicalRegistryFile,
  registryPath?: string,
): string {
  const p = registryPath || resolveCanonicalRegistryPath();
  fs.mkdirSync(path.dirname(p), { recursive: true });
  const next = { ...file, updatedAt: new Date().toISOString() };
  fs.writeFileSync(p, JSON.stringify(next, null, 2) + "\n");
  return p;
}

export function fingerprintSourceFile(filePath: string): string {
  const buf = fs.readFileSync(filePath);
  const stat = fs.statSync(filePath);
  return createHash("sha256")
    .update(buf)
    .update(`|${stat.size}|${path.basename(filePath)}`)
    .digest("hex");
}

export function lookupCanonicalConflicts(input: {
  registry: CanonicalRegistryFile;
  internalContentId?: string | null;
  sourceFileFingerprint?: string | null;
  youtubeVideoId?: string | null;
}): RegistryLookupResult {
  for (const rec of input.registry.records) {
    if (
      input.internalContentId &&
      rec.internalContentId &&
      rec.internalContentId === input.internalContentId &&
      rec.youtubeVideoId
    ) {
      return {
        blocked: true,
        matched: rec,
        reason: `UPLOAD BLOCKED: This content package is already mapped to YouTube video ${rec.youtubeVideoId}. Use the canonical update workflow instead.`,
      };
    }
    if (
      input.sourceFileFingerprint &&
      rec.sourceFileFingerprint &&
      rec.sourceFileFingerprint === input.sourceFileFingerprint &&
      rec.youtubeVideoId
    ) {
      return {
        blocked: true,
        matched: rec,
        reason: `UPLOAD BLOCKED: Source fingerprint already mapped to YouTube video ${rec.youtubeVideoId}.`,
      };
    }
    if (
      input.youtubeVideoId &&
      rec.youtubeVideoId &&
      rec.youtubeVideoId === input.youtubeVideoId
    ) {
      return {
        blocked: true,
        matched: rec,
        reason: `UPLOAD BLOCKED: YouTube video ${input.youtubeVideoId} is already the canonical ID for ${rec.internalContentId}.`,
      };
    }
  }
  return { blocked: false, matched: null, reason: null };
}

export function upsertCanonicalRecord(
  registry: CanonicalRegistryFile,
  record: CanonicalRegistryRecord,
): CanonicalRegistryFile {
  const idx = registry.records.findIndex(
    (r) => r.internalContentId === record.internalContentId,
  );
  const records = [...registry.records];
  if (idx >= 0) {
    const existing = records[idx];
    if (
      existing.youtubeVideoId &&
      record.youtubeVideoId &&
      existing.youtubeVideoId !== record.youtubeVideoId
    ) {
      throw new Error(
        `Refusing to replace canonical YouTube ID ${existing.youtubeVideoId} with ${record.youtubeVideoId} for ${record.internalContentId}`,
      );
    }
    records[idx] = { ...existing, ...record, youtubeVideoId: existing.youtubeVideoId || record.youtubeVideoId };
  } else {
    records.push(record);
  }
  return { ...registry, records, updatedAt: new Date().toISOString() };
}

/** Seed helper for known Orbit catalogue. */
export function seedOrbitCanonicalRecords(): CanonicalRegistryRecord[] {
  return [
    {
      internalContentId: "v001-fermi-long",
      contentType: "longform",
      sourceFileFingerprint: "seed:Mo93x0fxB1Q",
      title: "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained | Orbit's Cosmic Journey",
      youtubeVideoId: "Mo93x0fxB1Q",
      uploadTimestamp: "2026-07-30T17:00:09Z",
      scheduledPublishTimestamp: null,
      privacyStatus: "public",
      packageVersion: "v001",
      metadataVersion: "cleanup-2026-08-07",
      relatedLongFormVideoId: null,
      lastVerificationTimestamp: null,
      lastApiResponseStatus: null,
    },
    {
      internalContentId: "v001-fermi-short-01",
      contentType: "shorts",
      sourceFileFingerprint: "seed:1HuV8o3gOss",
      title: "Why Haven't We Found Aliens Yet? #FermiParadox #Space #Shorts",
      youtubeVideoId: "1HuV8o3gOss",
      uploadTimestamp: "2026-08-02T23:17:18Z",
      scheduledPublishTimestamp: null,
      privacyStatus: "public",
      packageVersion: "v001",
      metadataVersion: "cleanup-2026-08-07",
      relatedLongFormVideoId: "Mo93x0fxB1Q",
      lastVerificationTimestamp: null,
      lastApiResponseStatus: null,
    },
    {
      internalContentId: "v001-fermi-short-02",
      contentType: "shorts",
      sourceFileFingerprint: "seed:KcKBixwmcV4",
      title: "What If the First Alien Clue Is Already Here?",
      youtubeVideoId: "KcKBixwmcV4",
      uploadTimestamp: "2026-08-03T11:30:08Z",
      scheduledPublishTimestamp: null,
      privacyStatus: "public",
      packageVersion: "v001",
      metadataVersion: "cleanup-2026-08-07",
      relatedLongFormVideoId: "Mo93x0fxB1Q",
      lastVerificationTimestamp: null,
      lastApiResponseStatus: null,
    },
    {
      internalContentId: "v002-bh-long",
      contentType: "longform",
      sourceFileFingerprint: "seed:3xrxdmaOwJI",
      title: "What Happens If You Fall Into a Black Hole? Orbit's Cosmic Journey",
      youtubeVideoId: "3xrxdmaOwJI",
      uploadTimestamp: "2026-08-05T17:00:09Z",
      scheduledPublishTimestamp: null,
      privacyStatus: "public",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      relatedLongFormVideoId: null,
      lastVerificationTimestamp: null,
      lastApiResponseStatus: null,
    },
    {
      internalContentId: "v002-bh-short-01",
      contentType: "shorts",
      sourceFileFingerprint: "seed:JRfhE6yWom4",
      title: "Why This Line Is a Point of No Return #Space #Shorts",
      youtubeVideoId: "JRfhE6yWom4",
      uploadTimestamp: "2026-08-05T20:00:05Z",
      scheduledPublishTimestamp: null,
      privacyStatus: "public",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: null,
      lastApiResponseStatus: null,
    },
    {
      internalContentId: "v002-bh-short-02",
      contentType: "shorts",
      sourceFileFingerprint: "seed:L2OFjL4neOo",
      title: "Falling In Wouldn't Feel Like Falling",
      youtubeVideoId: "L2OFjL4neOo",
      uploadTimestamp: "2026-08-06T11:30:09Z",
      scheduledPublishTimestamp: null,
      privacyStatus: "public",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: null,
      lastApiResponseStatus: null,
    },
    {
      internalContentId: "v002-bh-nf01",
      contentType: "shorts",
      sourceFileFingerprint: "seed:tUAdhOnMW2g",
      title: "Time Appears to Stop at a Black Hole",
      youtubeVideoId: "tUAdhOnMW2g",
      uploadTimestamp: "2026-08-04T23:25:39Z",
      scheduledPublishTimestamp: "2026-08-07T10:30:00Z",
      privacyStatus: "private",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: null,
      lastApiResponseStatus: null,
    },
  ];
}
