/**
 * Resolve the public origin for OAuth callbacks and operator UI.
 * Prefer configured APP_BASE_URL when it is not localhost; otherwise use the
 * incoming request host or Vercel’s VERCEL_URL. Never invent orbitwithben.com.
 */

function stripTrailingSlash(url: string): string {
  return url.replace(/\/$/, "");
}

function isLocalhostUrl(url: string): boolean {
  try {
    const host = new URL(url).hostname;
    return host === "localhost" || host === "127.0.0.1" || host === "::1";
  } catch {
    return /localhost|127\.0\.0\.1/i.test(url);
  }
}

export function getPublicBaseUrl(request?: Request | { headers: Headers }): string {
  const configured = process.env.APP_BASE_URL?.trim();
  if (configured && !isLocalhostUrl(configured)) {
    return stripTrailingSlash(configured);
  }

  if (request) {
    const headers = request.headers;
    const host =
      headers.get("x-forwarded-host")?.split(",")[0]?.trim() ||
      headers.get("host")?.trim();
    if (host && !/^(localhost|127\.0\.0\.1)(:\d+)?$/i.test(host)) {
      const proto =
        headers.get("x-forwarded-proto")?.split(",")[0]?.trim() ||
        (host.includes("localhost") ? "http" : "https");
      return stripTrailingSlash(`${proto}://${host}`);
    }
  }

  const vercel = process.env.VERCEL_URL?.trim();
  if (vercel) {
    const host = vercel.replace(/^https?:\/\//, "");
    return stripTrailingSlash(`https://${host}`);
  }

  if (configured) return stripTrailingSlash(configured);
  return "http://localhost:3000";
}

export function oauthCallbackUrl(
  provider: "google" | "meta" | "tiktok" | "x" | "threads",
  request?: Request | { headers: Headers },
): string {
  const envKey = {
    google: "GOOGLE_REDIRECT_URI",
    meta: "META_REDIRECT_URI",
    tiktok: "TIKTOK_REDIRECT_URI",
    x: "X_REDIRECT_URI",
    threads: "THREADS_REDIRECT_URI",
  }[provider];
  const override = process.env[envKey]?.trim();
  if (override && !isLocalhostUrl(override)) {
    return override;
  }
  // Ignore localhost overrides on a non-local deploy so Connect works on Vercel.
  const base = getPublicBaseUrl(request);
  if (override && isLocalhostUrl(override) && !isLocalhostUrl(base)) {
    return `${base}/api/oauth/${provider}/callback`;
  }
  if (override) return override;
  return `${base}/api/oauth/${provider}/callback`;
}
