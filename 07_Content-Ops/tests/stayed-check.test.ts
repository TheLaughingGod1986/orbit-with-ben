import { describe, expect, it } from "vitest";
import { renderStayedCheck, stayedVerdict, viewedVerdict } from "../scripts/analytics-report";

describe("Shorts targets: stayed 60%+ and average viewed 70%+ (Ben, 24 Oct 2026)", () => {
  it("grades stayed-to-watch", () => {
    expect(stayedVerdict(61, 150)).toBe("PASS");
    expect(stayedVerdict(60, 100)).toBe("PASS");
    expect(stayedVerdict(56, 113)).toBe("WATCH");
    expect(stayedVerdict(32.1, 815)).toBe("MISS");
    expect(stayedVerdict(81.8, 17)).toBe("too few to judge");
  });

  it("grades average viewed", () => {
    expect(viewedVerdict(108.4, 130)).toBe("LOOP");
    expect(viewedVerdict(78.4, 113)).toBe("PASS");
    expect(viewedVerdict(70, 100)).toBe("PASS");
    expect(viewedVerdict(62.3, 881)).toBe("WATCH");
    expect(viewedVerdict(44, 1219)).toBe("MISS");
    expect(viewedVerdict(120, 40)).toBe("too few to judge");
  });

  it("lists recent Shorts only, newest first, with both reads", () => {
    const now = Date.parse("2026-10-24T18:45:00Z");
    const v = (id: string, publishedAt: string, stayed: number | undefined, viewed: number | undefined, views: number, format = "short") =>
      ({ id, title: `T ${id}`, format, publishedAt, views, studioStayedPct: stayed, studioAvgViewPct: viewed, studioViews: views }) as never;
    const r = {
      videos: [
        v("old", "2026-09-01T10:30:00Z", 41.2, 61.3, 292),
        v("mercury", "2026-10-24T10:30:00Z", 32.1, undefined, 815),
        v("sun", "2026-10-19T10:30:00Z", 56.0, 78.4, 113),
        v("ir", "2026-10-19T10:30:00Z", 41.4, 108.4, 130),
        v("long", "2026-10-21T17:00:00Z", 50, 40, 500, "long"),
        v("noread", "2026-10-22T10:30:00Z", undefined, undefined, 90),
      ],
    } as never;
    const md = renderStayedCheck(r, now);
    expect(md).toContain("stayed-to-watch 60%+ and average viewed 70%+");
    expect(md).not.toContain("youtu.be/old");
    expect(md).not.toContain("youtu.be/long");
    expect(md).not.toContain("youtu.be/noread");
    expect(md.indexOf("youtu.be/mercury")).toBeLessThan(md.indexOf("youtu.be/sun"));
    expect(md).toContain("| 8 h (early) | 815 | 32.1% | MISS | - | no read |");
    expect(md).toContain("| 5 d | 113 | 56.0% | WATCH | 78.4% | PASS |");
    expect(md).toContain("| 5 d | 130 | 41.4% | MISS | 108.4% | LOOP |");
    expect(md).toContain("Stayed to watch: 0 of 3 judged Shorts at 60%+. Average viewed: 2 of 2 at 70%+.");
  });
});
