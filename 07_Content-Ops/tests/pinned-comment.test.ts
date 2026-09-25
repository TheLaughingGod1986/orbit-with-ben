import { describe, expect, it } from "vitest";
import { buildPinnedCommentText, lastMilestone } from "../src/lib/publishing/pinned-comment";

describe("pinned comment", () => {
  it("does not quote a count below the first milestone", () => {
    expect(lastMilestone(9)).toBeNull();
    const text = buildPinnedCommentText({ question: "How far would Orbit get?", subscribers: 9 });
    expect(text).not.toMatch(/\d/);
    expect(text.startsWith("How far would Orbit get?")).toBe(true);
  });

  it("rounds down to the last milestone reached", () => {
    expect(lastMilestone(10)).toBe(10);
    expect(lastMilestone(37)).toBe(25);
    expect(lastMilestone(1204)).toBe(1000);
    expect(buildPinnedCommentText({ question: "Q?", subscribers: 1204 })).toContain("just passed 1,000 subscribers");
  });
});
