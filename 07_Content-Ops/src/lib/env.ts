import { z } from "zod";

const optionalString = z.string().optional();

export const envSchema = z.object({
  /** Postgres connection URL (pooled on Vercel/Neon). Required for runtime DB access. */
  DATABASE_URL: z.string().min(1),
  /** Direct (non-pooled) URL for migrations; optional at runtime. */
  DIRECT_URL: optionalString,
  APP_BASE_URL: z.string().url().default("http://localhost:3000"),
  ORBIT_TOKEN_ENCRYPTION_KEY: optionalString,
  NODE_ENV: z.string().optional(),
  PUBLISHING_DRY_RUN: z.string().optional(),
  PUBLISHING_WORKER_ID: z.string().optional(),
  GOOGLE_CLIENT_ID: optionalString,
  GOOGLE_CLIENT_SECRET: optionalString,
  GOOGLE_REDIRECT_URI: optionalString,
  META_APP_ID: optionalString,
  META_APP_SECRET: optionalString,
  META_REDIRECT_URI: optionalString,
  TIKTOK_CLIENT_KEY: optionalString,
  TIKTOK_CLIENT_SECRET: optionalString,
  TIKTOK_REDIRECT_URI: optionalString,
  X_CLIENT_ID: optionalString,
  X_CLIENT_SECRET: optionalString,
  X_REDIRECT_URI: optionalString,
  THREADS_APP_ID: optionalString,
  THREADS_APP_SECRET: optionalString,
  THREADS_REDIRECT_URI: optionalString,
  MEDIA_STAGING_MODE: z
    .enum(["local_direct_upload", "temporary_object_storage", "existing_public_url"])
    .optional(),
  MEDIA_PUBLIC_BASE_URL: optionalString,
  /** Amazon Associates UK tag — never hard-code in seed/source; set in operator env only */
  AMAZON_ASSOCIATE_TAG: optionalString,
  /** Brilliant affiliate / referral ID */
  BRILLIANT_AFFILIATE_ID: optionalString,
  /** Base for /go/{slug} redirects; defaults to ${APP_BASE_URL}/go when unset */
  AFFILIATE_REDIRECT_BASE_URL: optionalString,
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

export function requireEncryptionKeyInProduction(): void {
  const env = getEnv();
  if (env.NODE_ENV === "production" && !env.ORBIT_TOKEN_ENCRYPTION_KEY) {
    throw new Error("ORBIT_TOKEN_ENCRYPTION_KEY is required in production");
  }
}

export function hasGoogleOAuth(): boolean {
  const e = getEnv();
  return Boolean(e.GOOGLE_CLIENT_ID && e.GOOGLE_CLIENT_SECRET);
}

export function hasMetaOAuth(): boolean {
  const e = getEnv();
  return Boolean(e.META_APP_ID && e.META_APP_SECRET);
}

export function hasTikTokOAuth(): boolean {
  const e = getEnv();
  return Boolean(e.TIKTOK_CLIENT_KEY && e.TIKTOK_CLIENT_SECRET);
}

export function hasXOAuth(): boolean {
  const e = getEnv();
  return Boolean(e.X_CLIENT_ID && e.X_CLIENT_SECRET);
}

export function hasThreadsOAuth(): boolean {
  const e = getEnv();
  return Boolean(e.THREADS_APP_ID && e.THREADS_APP_SECRET);
}
