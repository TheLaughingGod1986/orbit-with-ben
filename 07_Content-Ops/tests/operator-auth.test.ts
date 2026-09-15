import { afterEach, describe, expect, it, vi } from "vitest";
import {
  isMutatingApiPath,
  isOAuthCallbackPath,
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
  it("flags mutating API methods and OAuth start", () => {
    expect(isMutatingApiPath("POST", "/api/affiliate/go-live")).toBe(true);
    expect(isMutatingApiPath("POST", "/api/affiliate/import")).toBe(true);
    expect(isMutatingApiPath("PATCH", "/api/posts/abc")).toBe(true);
    expect(isMutatingApiPath("GET", "/api/oauth/google/start")).toBe(true);
  });

  it("leaves reads and /go public", () => {
    expect(isMutatingApiPath("GET", "/api/affiliate/go-live")).toBe(false);
    expect(isMutatingApiPath("GET", "/go/exoplanet-book")).toBe(false);
    expect(isMutatingApiPath("POST", "/go/exoplanet-book")).toBe(false);
  });

  it("never gates OAuth callbacks — state is the CSRF check there", () => {
    expect(isOAuthCallbackPath("/api/oauth/google/callback")).toBe(true);
    expect(isOAuthCallbackPath("/api/oauth/google/start")).toBe(false);
    for (const platform of ["google", "meta", "tiktok", "x"]) {
      expect(isMutatingApiPath("GET", `/api/oauth/${platform}/callback`)).toBe(false);
      expect(isMutatingApiPath("POST", `/api/oauth/${platform}/callback`)).toBe(false);
    }
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

describe("middleware OAuth routes without an operator session", () => {
  it("lets the provider callback through so the code can be exchanged", async () => {
    delete process.env.CONTENT_OPS_OPERATOR_PASSWORD;
    const req = new NextRequest(
      "http://localhost:3000/api/oauth/google/callback?code=abc&state=xyz",
    );
    const res = await middleware(req);
    expect(res.status).toBe(200);
    expect(res.headers.get("location")).toBeNull();
  });

  it("still sends the operator to /login before starting Connect", async () => {
    delete process.env.CONTENT_OPS_OPERATOR_PASSWORD;
    const req = new NextRequest("http://localhost:3000/api/oauth/google/start");
    const res = await middleware(req);
    expect(res.status).toBe(307);
    expect(res.headers.get("location")).toContain("/login");
  });
});
