import { afterEach, describe, expect, it, vi } from "vitest";
import {
  isMutatingApiPath,
  requireOperator,
  safeOperatorNextPath,
} from "../src/lib/security/operator-auth";
import { middleware } from "../src/middleware";
import { NextRequest } from "next/server";

const ORIGINAL = {
  CONTENT_OPS_OPERATOR_PASSWORD: process.env.CONTENT_OPS_OPERATOR_PASSWORD,
  ORBIT_TOKEN_ENCRYPTION_KEY: process.env.ORBIT_TOKEN_ENCRYPTION_KEY,
};

afterEach(() => {
  for (const [key, value] of Object.entries(ORIGINAL)) {
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  }
  vi.restoreAllMocks();
});

describe("safeOperatorNextPath", () => {
  it("allows a single-slash path and rejects protocol-relative / absolute URLs", () => {
    expect(safeOperatorNextPath("/videos")).toBe("/videos");
    expect(safeOperatorNextPath("/")).toBe("/");
    expect(safeOperatorNextPath("//evil.com")).toBe("/");
    expect(safeOperatorNextPath("https://evil.com")).toBe("/");
    expect(safeOperatorNextPath("evil.com")).toBe("/");
  });
});

describe("isMutatingApiPath", () => {
  it("flags mutating API methods and OAuth token flows", () => {
    expect(isMutatingApiPath("POST", "/api/affiliate/go-live")).toBe(true);
    expect(isMutatingApiPath("POST", "/api/affiliate/import")).toBe(true);
    expect(isMutatingApiPath("PATCH", "/api/posts/abc")).toBe(true);
    expect(isMutatingApiPath("GET", "/api/oauth/google/start")).toBe(true);
    expect(isMutatingApiPath("GET", "/api/oauth/google/callback")).toBe(true);
  });

  it("leaves reads and /go public", () => {
    expect(isMutatingApiPath("GET", "/api/affiliate/go-live")).toBe(false);
    expect(isMutatingApiPath("GET", "/go/exoplanet-book")).toBe(false);
    expect(isMutatingApiPath("POST", "/go/exoplanet-book")).toBe(false);
  });
});

describe("requireOperator", () => {
  it("fails closed when CONTENT_OPS_OPERATOR_PASSWORD is unset", async () => {
    delete process.env.CONTENT_OPS_OPERATOR_PASSWORD;
    await expect(requireOperator()).rejects.toThrow(/Unauthorized/);
  });
});

describe("middleware unauthenticated mutating POST", () => {
  it("returns 401 without an operator session", async () => {
    delete process.env.CONTENT_OPS_OPERATOR_PASSWORD;
    const req = new NextRequest("http://localhost:3000/api/affiliate/go-live", {
      method: "POST",
      headers: { "content-type": "application/json" },
    });
    const res = await middleware(req);
    expect(res.status).toBe(401);
    const body = await res.json();
    expect(String(body.error || "")).toMatch(/Unauthorized/i);
  });
});
