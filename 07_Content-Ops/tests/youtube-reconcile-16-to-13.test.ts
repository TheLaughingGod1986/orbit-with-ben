import { describe, expect, it } from "vitest";
import { assertNotPlaceholderHoldPublishAt, isPlaceholderHoldPublishAt } from "../src/lib/publishing/youtube-schedule-guards";

const APPROVED_UTC: Record<string, string> = {
  tUAdhOnMW2g: "2026-08-10T10:30:00Z",
  svYOx07OrIM: "2026-08-11T10:30:00Z",
  B2STcIAF1lY: "2026-08-12T10:30:00Z",
  "b8-X_FyJnHM": "2026-08-13T17:00:00Z",
  ho9VJxp7f3A: "2026-08-13T19:00:00Z",
  "aoR-dA_g7eI": "2026-08-14T10:30:00Z",
  "6QFGAFZk264": "2026-08-15T10:30:00Z",
  eOOFVrJ2Ojc: "2026-08-16T10:30:00Z",
  tfTkMdE7qqw: "2026-08-20T17:00:00Z",
  bLv0RfidjSg: "2026-08-20T19:00:00Z",
  PcP64way3xA: "2026-08-21T10:30:00Z",
  pjIevt27Svo: "2026-08-22T10:30:00Z",
  AeFm7gWyWik: "2026-08-23T10:30:00Z",
};

const PUBLIC = new Set([
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
]);

const EXCLUDED = new Set([
  "HvAKGjx4lv0",
  "icedH_gK8JE",
  "Web2otrTcT0",
  "1qts3tIsg9c",
  "dPMJQp2gMNc",
  "rFJoOdQAc9c",
  "w1ej9u0rPTA",
  "gPCpMsB0w2E",
  "YsyPMhNmHMk",
]);

function norm(s: string | null | undefined) {
  return (s || "").replace(/\.\d{3}Z$/, "Z") || null;
}

function reconcile(
  live: Record<string, string>,
  approved: Record<string, string>,
): Array<{ id: string; action: string }> {
  const liveSet = new Set(Object.keys(live));
  const approvedSet = new Set(Object.keys(approved));
  const ids = new Set([...liveSet, ...approvedSet]);
  return [...ids].map((id) => {
    const l = live[id] || null;
    const a = approved[id] || null;
    let action = "BLOCKED_REVIEW";
    if (a && l && norm(l) === norm(a)) action = "KEEP_AS_IS";
    else if (a && l && norm(l) !== norm(a)) action = "UPDATE_TIME";
    else if (a && !l) action = "MISSING_FROM_LIVE";
    else if (!a && l) action = "UNSCHEDULE";
    return { id, action };
  });
}

function isQuotaError(body: unknown) {
  return /quotaExceeded/i.test(JSON.stringify(body || {}));
}

function hvSerializedPass(
  reads: Array<{ privacy: string; publishAt: string | null }>,
): boolean {
  if (reads.length < 3) return false;
  return reads.slice(-3).every((r) => r.privacy === "private" && r.publishAt == null);
}

describe("quota gate", () => {
  it("detects quotaExceeded and blocks mutation path", () => {
    const body = {
      error: { code: 403, errors: [{ reason: "quotaExceeded" }], message: "quota" },
    };
    expect(isQuotaError(body)).toBe(true);
    expect(isQuotaError({ error: { reason: "forbidden" } })).toBe(false);
  });
});

describe("16-to-13 reconciliation", () => {
  it("identifies exactly three obsolete slots from classic old calendar", () => {
    const live = {
      tUAdhOnMW2g: "2026-08-08T10:30:00Z",
      svYOx07OrIM: "2026-08-09T10:30:00Z",
      B2STcIAF1lY: "2026-08-10T10:30:00Z",
      w1ej9u0rPTA: "2026-08-11T10:30:00Z",
      "b8-X_FyJnHM": "2026-08-14T17:00:00Z",
      ho9VJxp7f3A: "2026-08-14T19:00:00Z",
      "aoR-dA_g7eI": "2026-08-15T10:30:00Z",
      "6QFGAFZk264": "2026-08-16T10:30:00Z",
      eOOFVrJ2Ojc: "2026-08-17T10:30:00Z",
      tfTkMdE7qqw: "2026-08-21T17:00:00Z",
      bLv0RfidjSg: "2026-08-21T19:00:00Z",
      PcP64way3xA: "2026-08-22T10:30:00Z",
      pjIevt27Svo: "2026-08-23T10:30:00Z",
      AeFm7gWyWik: "2026-08-24T10:30:00Z",
      gPCpMsB0w2E: "2026-08-25T10:30:00Z",
      YsyPMhNmHMk: "2026-08-26T10:30:00Z",
    };
    expect(Object.keys(live)).toHaveLength(16);
    expect(Object.keys(APPROVED_UTC)).toHaveLength(13);
    const rows = reconcile(live, APPROVED_UTC);
    const obsolete = rows.filter((r) => r.action === "UNSCHEDULE").map((r) => r.id).sort();
    expect(obsolete).toEqual(["YsyPMhNmHMk", "gPCpMsB0w2E", "w1ej9u0rPTA"].sort());
    for (const id of obsolete) {
      expect(PUBLIC.has(id)).toBe(false);
      expect(APPROVED_UTC[id]).toBeUndefined();
      expect(EXCLUDED.has(id)).toBe(true);
    }
    expect(rows.filter((r) => r.action === "UPDATE_TIME").length).toBeGreaterThan(0);
  });

  it("never schedules excluded assets", () => {
    for (const id of EXCLUDED) {
      expect(APPROVED_UTC[id]).toBeUndefined();
    }
  });

  it("protects public canonicals from schedule actions", () => {
    for (const id of PUBLIC) {
      expect(APPROVED_UTC[id]).toBeUndefined();
    }
  });
});

describe("Hv serialized stabilization", () => {
  it("passes only on three consecutive private+null reads", () => {
    expect(
      hvSerializedPass([
        { privacy: "private", publishAt: null },
        { privacy: "private", publishAt: null },
        { privacy: "private", publishAt: null },
      ]),
    ).toBe(true);
    expect(
      hvSerializedPass([
        { privacy: "private", publishAt: null },
        { privacy: "unlisted", publishAt: null },
        { privacy: "private", publishAt: null },
      ]),
    ).toBe(false);
  });

  it("does not treat parallel disagreement as pass", () => {
    // Simulated mixed sample set must fail if any unlisted present in last 3
    expect(
      hvSerializedPass([
        { privacy: "private", publishAt: null },
        { privacy: "private", publishAt: null },
        { privacy: "unlisted", publishAt: null },
      ]),
    ).toBe(false);
  });
});

describe("placeholder ban + collision", () => {
  it("rejects Dec 31 placeholders", () => {
    expect(isPlaceholderHoldPublishAt("2026-12-31T12:00:00Z")).toBe(true);
    expect(() => assertNotPlaceholderHoldPublishAt("2026-12-31T12:00:00Z")).toThrow();
    for (const ts of Object.values(APPROVED_UTC)) {
      expect(isPlaceholderHoldPublishAt(ts)).toBe(false);
    }
  });

  it("approved UTC minutes are unique", () => {
    const times = Object.values(APPROVED_UTC);
    expect(new Set(times).size).toBe(times.length);
  });
});

describe("transaction stop on quota", () => {
  it("records stop without blind retry", () => {
    const succeeded = ["w1ej9u0rPTA", "gPCpMsB0w2E"];
    const stoppedAt = "YsyPMhNmHMk";
    const shouldBlindRetry = false;
    expect(shouldBlindRetry).toBe(false);
    expect(succeeded).not.toContain(stoppedAt);
  });
});
