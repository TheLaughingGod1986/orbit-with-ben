import { describe, expect, it } from "vitest";
import { verdict } from "../scripts/verify-swap";

const orbit = "UC_esArsDKd3GJvOkeO0DUog";
const v = (id: string, privacyStatus: string, publishAt: string | null) => ({
  id, found: true, title: "t", channelId: orbit, privacyStatus, publishAt,
});

describe("verify-swap verdict", () => {
  it("passes when the old copy is private and unscheduled and the new one scheduled", () => {
    expect(verdict(v("old", "private", null), v("new", "private", "2026-10-26T11:30:00Z"))).toEqual([]);
  });
  it("fails when the old copy still has a publishAt", () => {
    const p = verdict(v("old", "private", "2026-10-26T11:30:00Z"), v("new", "private", "2026-10-26T11:30:00Z"));
    expect(p.join(" ")).toMatch(/old old: private publishAt 2026-10-26/);
  });
  it("fails when the new copy is not scheduled or the old one is public", () => {
    expect(verdict(v("old", "public", null), v("new", "private", null))).toHaveLength(2);
  });
});
