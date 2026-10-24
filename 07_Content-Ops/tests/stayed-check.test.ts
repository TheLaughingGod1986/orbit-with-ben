import { describe, expect, it } from "vitest";
import { renderStayedCheck, stayedVerdict } from "../scripts/analytics-report";

describe("stayed-to-watch vs the 60% target (Ben, 24 Oct 2026)", () => {
  it("grades a read", () => {
    expect(stayedVerdict(61, 150)).toBe("PASS");
    expect(stayedVerdict(60, 100)).toBe("PASS");
    expect(stayedVerdict(56, 113)).toBe("WATCH");
    expect(stayedVerdict(32.1, 815)).toBe("MISS");
    expect(stayedVerdict(81.8, 17)).toBe("too few to judge");
  });

  it("lists recent Shorts only, newest first, with early reads marked", () => {
    const now = Date.parse("2026-10-24T18:45:00Z");
    const v = (id: string, publishedAt: string, stayed: number | undefined, views: number, format = "short") =>
      ({ id, title: `T ${id}`, format, publishedAt, views, studioStayedPct: stayed, studioViews: views }) as never;
    const r = {
      videos: [
        v("old", "2026-09-01T10:30:00Z", 41.2, 292),
        v("mercury", "2026-10-24T10:30:00Z", 32.1, 815),
        v("sun", "2026-10-19T10:30:00Z", 56.0, 113),
        v("long", "2026-10-21T17:00:00Z", 50, 500, "long"),
        v("noread", "2026-10-22T10:30:00Z", undefined, 90),
      ],
    } as never;
    const md = renderStayedCheck(r, now);
    expect(md).toContain("vs the 60% target");
    expect(md).not.toContain("youtu.be/old");
    expect(md).not.toContain("youtu.be/long");
    expect(md).not.toContain("youtu.be/noread");
    expect(md.indexOf("youtu.be/mercury")).toBeLessThan(md.indexOf("youtu.be/sun"));
    expect(md).toContain("| 8 h (early) | 815 | 32.1% | MISS |");
    expect(md).toContain("| 5 d | 113 | 56.0% | WATCH |");
    expect(md).toContain("0 of 2 judged Shorts at 60%+.");
  });
});
