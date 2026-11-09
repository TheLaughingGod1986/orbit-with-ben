import { describe, expect, it } from "vitest";
import { verdict } from "../scripts/verify-swap";

const orbit = "UC_esArsDKd3GJvOkeO0DUog";
const hos = "UCXp7HkBIl1LgaznXuZHJyRg";
const v = (id: string, privacyStatus: string, publishAt: string | null, channelId = orbit) => ({
  id, found: true, title: "t", channelId, privacyStatus, publishAt,
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
  it("passes a History of Science swap on the HOS channel", () => {
    expect(verdict(
      v("old", "private", null, hos),
      v("new", "private", "2026-11-03T11:30:00Z", hos),
    )).toEqual([]);
  });
  it("fails when the two copies are on different channels", () => {
    expect(verdict(v("old", "private", null, orbit), v("new", "private", "2026-11-03T11:30:00Z", hos)).join(" ")).toMatch(/different channels/);
  });
});
