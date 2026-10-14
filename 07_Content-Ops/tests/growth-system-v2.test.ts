import { describe, expect, it } from "vitest";
import {
  PASS_THRESHOLD,
  reviewScript,
  formatReviewMarkdown,
} from "../src/lib/analytics/script-reviewer";
import {
  computeCtr,
  diagnoseCatalog,
  diagnoseVideo,
  summarizeGrowthDashboard,
} from "../src/lib/analytics/youtube-growth";
import { CONTENT_RULES } from "../src/config/content-rules";

const STRONG_SCRIPT = `
# What Really Happens When You Fall Into a Black Hole?

Orbit has just crossed the event horizon — why has nothing escaped, and what would you see next?

[CHAPTER CARD: The Crossing]
[VISUAL MUST: Orbit tumbling past the photon sphere]
[ORBIT ACTS: Orbit falls toward the event horizon, arms bracing]
[TEACH: The event horizon is a boundary in spacetime, not a solid surface]

But deeper still, tidal gravity stretches anything that falls. How does light bend? What if everything we've assumed about "inside" is wrong?

[CHAPTER CARD: Spaghettification]
[VISUAL MUST: extreme tidal stretch diagram with Orbit]
[ORBIT ACTS: Orbit witnesses stars shear into luminous arcs]
[TEACH: Tidal forces grow without bound near a stellar-mass hole]

Then Orbit reaches a region where time itself slows for distant observers. Suddenly the mystery escalates — is information lost forever?

[CHAPTER CARD: The Information Paradox]
[VISUAL MUST: Hawking radiation shimmer]
[ORBIT ACTS: Orbit discovers a faint glow escaping as Hawking radiation]
[TEACH: Black holes slowly evaporate via Hawking radiation]

However, beyond that glow lies a bigger question: could quantum gravity rewrite the ending?

[CHAPTER CARD: The Bigger Question]
[VISUAL MUST: Orbit at the edge of a singularity glow]
[ORBIT ACTS: Orbit escapes the thought experiment back to safe orbit]
[TEACH: The singularity marks where known physics breaks]

Payoff: you would not "see darkness" the way cinema shows — spacetime geometry reshapes your last photons. What happens next for physics itself remains unknown — a paradox still open.
`.repeat(3); // pad toward 8–12 min word count

const WEAK_SCRIPT = `
Welcome to Orbit with Ben. In this video, what is a black hole?
Have you ever wondered about space? For centuries humanity has looked up.
Today we will explain the history of black holes in a calm lecture style.
| Orbit's Cosmic Journey
`;

describe("script reviewer v2", () => {
  it("rewards multiple science and escalation matches", () => {
    const single = reviewScript(
      "But gravity changes the view. Also motion changes the path. Also size shapes the scene. Also air fills the sky. Also energy crosses the gap. Also light reaches the detector.",
    );
    const multi = reviewScript(
      "But gravity changes the view. However orbit changes the path. Then mass shapes the scene. Worse atmosphere fills the sky. Suddenly radiation crosses the gap. Now photon reaches the detector.",
    );

    expect(multi.scores.scientificAccuracy).toBeGreaterThan(single.scores.scientificAccuracy);
    expect(multi.scores.escalation).toBeGreaterThan(single.scores.escalation);
  });

  it("rejects weak definition / intro opens", () => {
    const result = reviewScript(WEAK_SCRIPT);
    expect(result.decision).toBe("REJECT");
    expect(result.total).toBeLessThan(PASS_THRESHOLD);
    expect(result.findings.some((f) => f.dimension === "hook")).toBe(true);
  });

  it("can pass a strong cold-open story script", () => {
    const result = reviewScript(STRONG_SCRIPT, {
      hook: 10,
      curiosity: 9.5,
      storytelling: 9.5,
      scientificAccuracy: 9,
      emotion: 9,
      escalation: 9,
      retentionPotential: 9.5,
      searchPotential: 9,
      visualOpportunities: 9.5,
      narrationFlow: 9,
    });
    expect(result.total).toBeGreaterThanOrEqual(PASS_THRESHOLD);
    expect(result.passed).toBe(true);
    expect(formatReviewMarkdown(result)).toContain("PASS");
  });

  it("heuristic scorer rewards Orbit agency and cold open", () => {
    const result = reviewScript(STRONG_SCRIPT);
    expect(result.scores.visualOpportunities).toBeGreaterThanOrEqual(7);
    expect(result.scores.hook).toBeGreaterThanOrEqual(7);
    expect(result.estimates.wordCount).toBeGreaterThan(250);
  });
});

describe("youtube growth diagnostics", () => {
  it("computes CTR from impressions and views", () => {
    expect(computeCtr(1000, 50)).toBe(5);
    expect(computeCtr(0, 50)).toBeNull();
  });

  it("flags weak openings, packaging, runtime, traffic mix", () => {
    const recs = diagnoseVideo({
      title: "Black Hole Lecture",
      isShort: false,
      impressions: 5000,
      views: 500,
      ctr: 2,
      retention30s: 40,
      averagePercentageViewed: 22,
      durationSeconds: 20 * 60,
      searchPercent: 80,
      browsePercent: 5,
      suggestedPercent: 5,
      endScreenCtr: 0.5,
    });
    const cats = new Set(recs.map((r) => r.category));
    expect(cats.has("weak_opening")).toBe(true);
    expect(cats.has("weak_thumbnail") || cats.has("poor_title")).toBe(true);
    expect(cats.has("needs_update")).toBe(true);
    expect(cats.has("runtime")).toBe(true);
    expect(cats.has("traffic_mix")).toBe(true);
    expect(cats.has("funnel")).toBe(true);
  });

  it("summarises catalog leaders", () => {
    const { recommendations, leaders } = diagnoseCatalog([
      {
        title: "Short A",
        isShort: true,
        hookCategory: "mystery",
        topic: "Fermi",
        averagePercentageViewed: 80,
        impressions: 1000,
        views: 80,
        ctr: 8,
      },
      {
        title: "Short B",
        isShort: true,
        hookCategory: "mystery",
        topic: "Fermi",
        averagePercentageViewed: 70,
        impressions: 1000,
        views: 70,
        ctr: 7,
      },
      {
        title: "Short C",
        isShort: true,
        hookCategory: "scale_comparison",
        topic: "Black holes",
        averagePercentageViewed: 50,
        impressions: 1000,
        views: 40,
        ctr: 4,
      },
    ]);
    expect(leaders.topHooks[0]?.hook).toBe("mystery");
    expect(leaders.topShorts[0]?.title).toBe("Short A");
    expect(recommendations.some((r) => r.category === "top_performer")).toBe(true);
    const summary = summarizeGrowthDashboard([
      { impressions: 1000, views: 50, averagePercentageViewed: 40, subscribersGained: 2 },
    ]);
    expect(summary.impressions).toBe(1000);
    expect(summary.avgCtr).toBe(5);
  });
});

describe("content rules growth v2", () => {
  it("locks trust-building runtime and script threshold", () => {
    expect(CONTENT_RULES.longForm.preferredMinMinutes).toBe(8);
    expect(CONTENT_RULES.longForm.preferredMaxMinutes).toBe(12);
    expect(CONTENT_RULES.longForm.scriptPassThreshold).toBe(90);
    expect(CONTENT_RULES.longForm.shortsPerLong).toEqual({ min: 3, max: 5 });
  });
});
