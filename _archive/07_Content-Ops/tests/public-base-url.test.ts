import { afterEach, describe, expect, it } from "vitest";
import { getPublicBaseUrl, oauthCallbackUrl } from "../src/lib/public-base-url";

const ORIGINAL = {
  APP_BASE_URL: process.env.APP_BASE_URL,
  VERCEL_URL: process.env.VERCEL_URL,
  GOOGLE_REDIRECT_URI: process.env.GOOGLE_REDIRECT_URI,
};

afterEach(() => {
  for (const [key, value] of Object.entries(ORIGINAL)) {
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  }
});

describe("getPublicBaseUrl / oauthCallbackUrl", () => {
  it("uses non-localhost APP_BASE_URL", () => {
    process.env.APP_BASE_URL = "https://orbit-content-ops.vercel.app";
    delete process.env.VERCEL_URL;
    expect(getPublicBaseUrl()).toBe("https://orbit-content-ops.vercel.app");
    expect(oauthCallbackUrl("google")).toBe(
      "https://orbit-content-ops.vercel.app/api/oauth/google/callback",
    );
  });

  it("ignores localhost APP_BASE_URL / redirect when request host is production", () => {
    process.env.APP_BASE_URL = "http://localhost:3000";
    process.env.GOOGLE_REDIRECT_URI = "http://localhost:3000/api/oauth/google/callback";
    delete process.env.VERCEL_URL;
    const req = {
      headers: new Headers({
        host: "orbit-content-ops.vercel.app",
        "x-forwarded-proto": "https",
      }),
    };
    expect(getPublicBaseUrl(req)).toBe("https://orbit-content-ops.vercel.app");
    expect(oauthCallbackUrl("google", req)).toBe(
      "https://orbit-content-ops.vercel.app/api/oauth/google/callback",
    );
  });
});
