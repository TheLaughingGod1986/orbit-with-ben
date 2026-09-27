import { z } from "zod";

const optionalString = z.string().optional();

/**
 * 07_Content-Ops/.env for the local scripts. The hosted ops app and its database were
 * retired on 27 Sep 2026, so nothing here needs a database. Never print or commit values.
 */
export const envSchema = z.object({
  /** Google Cloud OAuth client used by the YouTube scripts. */
  GOOGLE_CLIENT_ID: optionalString,
  GOOGLE_CLIENT_SECRET: optionalString,
  /** Localhost redirect registered on that client, for scripts/youtube-auth.ts. */
  GOOGLE_REDIRECT_URI: optionalString,
  /** The channel login, written by scripts/youtube-auth.ts. */
  YOUTUBE_REFRESH_TOKEN: optionalString,
  /** Buffer API key (Buffer → Settings → API) for the social mirror. */
  BUFFER_API_KEY: optionalString,
  /** Public Vercel Blob store token, for the mirror's media URLs. */
  BLOB_READ_WRITE_TOKEN: optionalString,
  /** "true" makes youtube:package a dry run. */
  PUBLISHING_DRY_RUN: optionalString,
  /** Base for affiliate /go/ links in generated descriptions (the app that served /go is retired). */
  APP_BASE_URL: z.string().url().default("http://localhost:3000"),
  AFFILIATE_REDIRECT_BASE_URL: optionalString,
  /** Amazon Associates UK tag — never hard-code or commit it. */
  AMAZON_ASSOCIATE_TAG: optionalString,
});

export type OrbitEnv = z.infer<typeof envSchema>;

let cached: OrbitEnv | null = null;

export function getEnv(): OrbitEnv {
  if (cached) return cached;
  const parsed = envSchema.safeParse(process.env);
  if (!parsed.success) {
    const msg = parsed.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ");
    throw new Error(`Invalid environment configuration: ${msg}`);
  }
  cached = parsed.data;
  return cached;
}

export function isDryRun(): boolean {
  const v = (process.env.PUBLISHING_DRY_RUN || "").toLowerCase();
  return v === "1" || v === "true" || v === "yes";
}
