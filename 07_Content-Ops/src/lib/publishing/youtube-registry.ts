/**
 * Canonical YouTube upload registry — ONE package = ONE video ID.
 */
import { createHash } from "crypto";
import fs from "fs";
import path from "path";

export type CanonicalRegistryRecord = {
  internalContentId: string;
  contentFamily?: string;
  contentType: "longform" | "shorts";
  sourceFileFingerprint: string;
  title: string;
  youtubeVideoId: string | null;
  youtubeState?: "public" | "private" | "unlisted" | "scheduled" | null;
  uploadTimestamp: string | null;
  scheduledPublishTimestamp: string | null;
  publishedAt?: string | null;
  privacyStatus: "private" | "public" | "unlisted" | null;
  packageVersion: string;
  metadataVersion: string;
  thumbnailVersion?: string | null;
  relatedLongFormVideoId: string | null;
  lastVerificationTimestamp: string | null;
  lastApiResponseStatus: string | null;
  lastVerifiedAt?: string | null;
  packagePath?: string | null;
  /** Never become upload targets again. */
  historicalDuplicateIds?: string[];
};

export type CanonicalRegistryFile = {
  version: number;
  updatedAt: string;
  records: CanonicalRegistryRecord[];
  /** Global blocklist of IDs that must never be re-targeted for upload/replace. */
  historicalDuplicateIdsGlobal?: string[];
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

function collectHistoricalIds(registry: CanonicalRegistryFile): Set<string> {
  const ids = new Set<string>(registry.historicalDuplicateIdsGlobal || []);
  for (const rec of registry.records) {
    for (const id of rec.historicalDuplicateIds || []) ids.add(id);
  }
  return ids;
}

export function lookupCanonicalConflicts(input: {
  registry: CanonicalRegistryFile;
  internalContentId?: string | null;
  sourceFileFingerprint?: string | null;
  youtubeVideoId?: string | null;
  contentFamily?: string | null;
}): RegistryLookupResult {
  const historical = collectHistoricalIds(input.registry);

  if (input.youtubeVideoId && historical.has(input.youtubeVideoId)) {
    return {
      blocked: true,
      matched: null,
      reason: `UPLOAD BLOCKED: YouTube video ${input.youtubeVideoId} is a historical duplicate ID and must never be reused as an upload target.`,
    };
  }

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
    const mergedHistorical = [
      ...new Set([
        ...(existing.historicalDuplicateIds || []),
        ...(record.historicalDuplicateIds || []),
      ]),
    ];
    records[idx] = {
      ...existing,
      ...record,
      youtubeVideoId: existing.youtubeVideoId || record.youtubeVideoId,
      historicalDuplicateIds: mergedHistorical,
    };
  } else {
    records.push(record);
  }
  return { ...registry, records, updatedAt: new Date().toISOString() };
}

/** Seed helper for known Orbit catalogue (post full-catalogue repair). */
export function seedOrbitCanonicalRecords(): CanonicalRegistryRecord[] {
  const verifiedAt = new Date().toISOString();
  return [
    {
      internalContentId: "v001-fermi-long",
      contentFamily: "FERMI",
      contentType: "longform",
      sourceFileFingerprint: "seed:Mo93x0fxB1Q",
      title: "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained | Orbit's Cosmic Journey",
      youtubeVideoId: "Mo93x0fxB1Q",
      youtubeState: "public",
      uploadTimestamp: "2026-07-30T17:00:09Z",
      scheduledPublishTimestamp: null,
      publishedAt: "2026-07-30T17:00:09Z",
      privacyStatus: "public",
      packageVersion: "v001",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: null,
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: [],
    },
    {
      internalContentId: "v001-fermi-short-01",
      contentFamily: "FERMI",
      contentType: "shorts",
      sourceFileFingerprint: "seed:1HuV8o3gOss",
      title: "Why Haven't We Found Aliens Yet? #FermiParadox #Space #Shorts",
      youtubeVideoId: "1HuV8o3gOss",
      youtubeState: "public",
      uploadTimestamp: "2026-08-02T23:17:18Z",
      scheduledPublishTimestamp: null,
      publishedAt: "2026-08-02T23:17:18Z",
      privacyStatus: "public",
      packageVersion: "v001",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "Mo93x0fxB1Q",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["z-DLqoSoEBo"],
    },
    {
      internalContentId: "v001-fermi-short-02",
      contentFamily: "FERMI",
      contentType: "shorts",
      sourceFileFingerprint: "seed:KcKBixwmcV4",
      title: "What If the First Alien Clue Is Already Here?",
      youtubeVideoId: "KcKBixwmcV4",
      youtubeState: "public",
      uploadTimestamp: "2026-08-03T11:30:08Z",
      scheduledPublishTimestamp: null,
      publishedAt: "2026-08-03T11:30:08Z",
      privacyStatus: "public",
      packageVersion: "v001",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "Mo93x0fxB1Q",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: [],
    },
    {
      internalContentId: "v001-fermi-short-rude",
      contentFamily: "FERMI",
      contentType: "shorts",
      sourceFileFingerprint: "seed:dPMJQp2gMNc",
      title: "Space Is Rude About Distance",
      youtubeVideoId: "dPMJQp2gMNc",
      youtubeState: "public",
      uploadTimestamp: null,
      scheduledPublishTimestamp: null,
      publishedAt: null,
      privacyStatus: "public",
      packageVersion: "v001",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "Mo93x0fxB1Q",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["UWwNKYf_aU8"],
    },
    {
      internalContentId: "v001-fermi-short-zoo",
      contentFamily: "FERMI",
      contentType: "shorts",
      sourceFileFingerprint: "seed:rFJoOdQAc9c",
      title: "Don't Look Up: The Zoo Hypothesis #Shorts #Aliens #Science",
      youtubeVideoId: "rFJoOdQAc9c",
      youtubeState: "public",
      uploadTimestamp: null,
      scheduledPublishTimestamp: null,
      publishedAt: null,
      privacyStatus: "public",
      packageVersion: "v001",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "Mo93x0fxB1Q",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: [],
    },
    {
      internalContentId: "v002-bh-long",
      contentFamily: "BLACK_HOLE",
      contentType: "longform",
      sourceFileFingerprint: "seed:3xrxdmaOwJI",
      title: "What Happens If You Fall Into a Black Hole? Orbit's Cosmic Journey",
      youtubeVideoId: "3xrxdmaOwJI",
      youtubeState: "public",
      uploadTimestamp: "2026-08-05T17:00:09Z",
      scheduledPublishTimestamp: null,
      publishedAt: "2026-08-05T17:00:09Z",
      privacyStatus: "public",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: null,
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["RCs6MMxF3ko", "n7CbJrOCnU0"],
    },
    {
      internalContentId: "v002-bh-short-01",
      contentFamily: "BLACK_HOLE",
      contentType: "shorts",
      sourceFileFingerprint: "seed:JRfhE6yWom4",
      title: "Why This Line Is a Point of No Return #Space #Shorts",
      youtubeVideoId: "JRfhE6yWom4",
      youtubeState: "public",
      uploadTimestamp: "2026-08-05T20:00:05Z",
      scheduledPublishTimestamp: null,
      publishedAt: "2026-08-05T20:00:05Z",
      privacyStatus: "public",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["IwpO33AJaPQ", "2777WlMGM8M", "eZGAhF8dN7w"],
    },
    {
      internalContentId: "v002-bh-short-02",
      contentFamily: "BLACK_HOLE",
      contentType: "shorts",
      sourceFileFingerprint: "seed:L2OFjL4neOo",
      title: "Falling In Wouldn't Feel Like Falling",
      youtubeVideoId: "L2OFjL4neOo",
      youtubeState: "public",
      uploadTimestamp: "2026-08-06T11:30:09Z",
      scheduledPublishTimestamp: null,
      publishedAt: "2026-08-06T11:30:09Z",
      privacyStatus: "public",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["IqII5mVGdrs", "jyzrl9ueKq4", "C4GuFEFGySI"],
    },
    {
      internalContentId: "v002-bh-nf01",
      contentFamily: "BLACK_HOLE",
      contentType: "shorts",
      sourceFileFingerprint: "seed:tUAdhOnMW2g",
      title: "Time Appears to Stop at a Black Hole",
      youtubeVideoId: "tUAdhOnMW2g",
      youtubeState: "scheduled",
      uploadTimestamp: "2026-08-04T23:25:39Z",
      scheduledPublishTimestamp: "2026-08-07T10:30:00Z",
      publishedAt: null,
      privacyStatus: "private",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["2C-eiSMsBLc"],
    },
    {
      internalContentId: "v002-bh-nf-look-back",
      contentFamily: "BLACK_HOLE",
      contentType: "shorts",
      sourceFileFingerprint: "seed:svYOx07OrIM",
      title: "Would You Look Back?",
      youtubeVideoId: "svYOx07OrIM",
      youtubeState: "scheduled",
      uploadTimestamp: null,
      scheduledPublishTimestamp: "2026-08-08T10:30:00Z",
      publishedAt: null,
      privacyStatus: "private",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["lIHb_tyxQSM"],
    },
    {
      internalContentId: "v002-bh-nf02",
      contentFamily: "BLACK_HOLE",
      contentType: "shorts",
      sourceFileFingerprint: "seed:B2STcIAF1lY",
      title: "What You Would See Falling Into a Black Hole",
      youtubeVideoId: "B2STcIAF1lY",
      youtubeState: "scheduled",
      uploadTimestamp: null,
      scheduledPublishTimestamp: "2026-08-09T10:30:00Z",
      publishedAt: null,
      privacyStatus: "private",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["wOlnj7nZWJM"],
    },
    {
      internalContentId: "v002-bh-nf-point",
      contentFamily: "BLACK_HOLE",
      contentType: "shorts",
      sourceFileFingerprint: "seed:w1ej9u0rPTA",
      title: "The Point of No Return Explained",
      youtubeVideoId: "w1ej9u0rPTA",
      youtubeState: "scheduled",
      uploadTimestamp: null,
      scheduledPublishTimestamp: "2026-08-10T10:30:00Z",
      publishedAt: null,
      privacyStatus: "private",
      packageVersion: "v002",
      metadataVersion: "cleanup-2026-08-07",
      thumbnailVersion: null,
      relatedLongFormVideoId: "3xrxdmaOwJI",
      lastVerificationTimestamp: verifiedAt,
      lastVerifiedAt: verifiedAt,
      lastApiResponseStatus: "verified",
      historicalDuplicateIds: ["2uT3wXJLybw"],
    },
  ];
}

export function buildRepairedCanonicalRegistry(): CanonicalRegistryFile {
  const records = seedOrbitCanonicalRecords();
  const historicalDuplicateIdsGlobal = [
    ...new Set(records.flatMap((r) => r.historicalDuplicateIds || [])),
  ];
  return {
    version: 2,
    updatedAt: new Date().toISOString(),
    records,
    historicalDuplicateIdsGlobal,
  };
}
