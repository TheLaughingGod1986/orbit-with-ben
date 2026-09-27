import type { UrlHealthStatus } from "./types";

export type HealthCheckResult = {
  status: UrlHealthStatus;
  httpStatus: number | null;
  finalUrl: string | null;
  notes?: string;
};

/**
 * URL health-check abstraction.
 * Call sparingly — never hammer every affiliate URL on a schedule loop.
 * Implementations may be swapped (fetch HEAD, Playwright, external monitor).
 */
export interface UrlHealthChecker {
  check(url: string): Promise<HealthCheckResult>;
}

/** Conservative checker: HEAD with GET fallback; classifies redirect vs broken. */
export const fetchUrlHealthChecker: UrlHealthChecker = {
  async check(url: string): Promise<HealthCheckResult> {
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 8_000);
      let res: Response;
      try {
        res = await fetch(url, {
          method: "HEAD",
          redirect: "follow",
          signal: controller.signal,
        });
        if (res.status === 405 || res.status === 403) {
          res = await fetch(url, {
            method: "GET",
            redirect: "follow",
            signal: controller.signal,
            headers: { Range: "bytes=0-0" },
          });
        }
      } finally {
        clearTimeout(timer);
      }

      const finalUrl = res.url || url;
      const redirected = normalizeHost(finalUrl) !== normalizeHost(url);

      if (res.status >= 200 && res.status < 400) {
        return {
          status: redirected ? "REDIRECTED" : "HEALTHY",
          httpStatus: res.status,
          finalUrl,
        };
      }
      if (res.status >= 400) {
        return {
          status: "BROKEN",
          httpStatus: res.status,
          finalUrl,
          notes: `HTTP ${res.status}`,
        };
      }
      return { status: "UNKNOWN", httpStatus: res.status, finalUrl };
    } catch (err) {
      return {
        status: "BROKEN",
        httpStatus: null,
        finalUrl: null,
        notes: err instanceof Error ? err.message : "request failed",
      };
    }
  },
};

function normalizeHost(u: string): string {
  try {
    return new URL(u).host.toLowerCase();
  } catch {
    return u;
  }
}

/** No-op checker for tests / dry runs. */
export function stubUrlHealthChecker(
  result: HealthCheckResult = {
    status: "HEALTHY",
    httpStatus: 200,
    finalUrl: null,
  },
): UrlHealthChecker {
  return {
    async check(url: string) {
      return { ...result, finalUrl: result.finalUrl ?? url };
    },
  };
}

/**
 * Decide whether a product is due for a health check.
 * Default: recheck only if never checked or older than `minIntervalMs`.
 */
export function shouldCheckUrl(
  lastCheckedAt: Date | null | undefined,
  minIntervalMs = 7 * 24 * 60 * 60 * 1000,
  now = Date.now(),
): boolean {
  if (!lastCheckedAt) return true;
  return now - lastCheckedAt.getTime() >= minIntervalMs;
}
