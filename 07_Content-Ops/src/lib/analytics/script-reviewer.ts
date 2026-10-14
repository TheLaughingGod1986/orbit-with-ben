/**
 * Orbit Growth System v2 — AI Script Reviewer
 * Reject any script scoring below PASS_THRESHOLD (90).
 */

export const SCRIPT_REVIEW_DIMENSIONS = [
  "hook",
  "curiosity",
  "storytelling",
  "scientificAccuracy",
  "emotion",
  "escalation",
  "retentionPotential",
  "searchPotential",
  "visualOpportunities",
  "narrationFlow",
] as const;

export type ScriptReviewDimension = (typeof SCRIPT_REVIEW_DIMENSIONS)[number];

export const PASS_THRESHOLD = 90;

export type DimensionScores = Record<ScriptReviewDimension, number>;

export type ScriptReviewFinding = {
  dimension: ScriptReviewDimension | "overall";
  severity: "info" | "warn" | "fail";
  message: string;
};

export type ScriptReviewResult = {
  scores: DimensionScores;
  total: number;
  maxTotal: number;
  passed: boolean;
  decision: "PASS" | "REJECT";
  findings: ScriptReviewFinding[];
  estimates: {
    wordCount: number;
    estimatedMinutes: number;
    chapterMarkers: number;
    questionMarks: number;
  };
  coldOpenExcerpt: string;
};

const FORBIDDEN_OPEN_PATTERNS: RegExp[] = [
  /^\s*welcome\b/i,
  /^\s*hey (guys|everyone)\b/i,
  /^\s*today (we('re| are)|i('m| am))\b/i,
  /^\s*in this video\b/i,
  /^\s*what is (a |an |the )?/i,
  /^\s*have you ever wondered\b/i,
  /^\s*for centuries\b/i,
  /^\s*throughout history\b/i,
  /^\s*let('s| us) (start|begin) (with|by)\b/i,
];

const SERIES_SUFFIX = /\|\s*orbit['']?s?\s+cosmic\s+journey/i;

const ACTIVE_ORBIT = /\borbit\b.{0,40}\b(falls?|falling|crosses|crossed|stands?|standing|flies|flying|witnesses|witnessed|enters?|entered|dives?|diving|survives?|escapes?|discovers?|discovers)\b/i;
const ORBIT_ACTS_MARKER = /\[ORBIT ACTS:/i;
const VISUAL_MUST = /\[VISUAL MUST:/i;
const TEACH_MARKER = /\[TEACH:/i;
const CHAPTER_MARKER = /\[CHAPTER CARD:|^\s*#{1,3}\s+chapter\b|^chapter\s+\d+/gim;

const YOU_STAKES = /\b(what would you|would you|you (see|feel|hear|survive)|what happens next|what if)\b/i;
const ESCALATION = /\b(but |however |then |worse |deeper |beyond |until |suddenly |now )\b/gi;
const CURIOSITY = /\b(why |how |what if|nobody|never|secret|mystery|paradox|impossible|unknown)\b/i;
const SCIENCE = /\b(light[- ]year|gravity|orbit|mass|atmosphere|radiation|wavelength|event horizon|biosignature|parsec|neutron|photon|spectrum)\b/gi;

function clampScore(n: number): number {
  return Math.max(0, Math.min(10, Math.round(n * 10) / 10));
}

function stripMarkdownNoise(text: string): string {
  return text
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/^\s*\|.*$/gm, " ")
    .replace(/\[VISUAL MUST:[^\]]*\]/gi, " ")
    .replace(/\[ORBIT ACTS:[^\]]*\]/gi, " ")
    .replace(/\[TEACH:[^\]]*\]/gi, " ")
    .replace(/\[CHAPTER CARD:[^\]]*\]/gi, " ")
    .replace(/[#>*_`]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function firstSpokenWindow(text: string, maxChars = 450): string {
  const clean = stripMarkdownNoise(text);
  return clean.slice(0, maxChars);
}

function wordCount(text: string): number {
  const words = stripMarkdownNoise(text).match(/[A-Za-z0-9']+/g);
  return words?.length ?? 0;
}

function scoreHook(script: string, open: string): { score: number; findings: ScriptReviewFinding[] } {
  const findings: ScriptReviewFinding[] = [];
  let score = 7;

  for (const re of FORBIDDEN_OPEN_PATTERNS) {
    if (re.test(open)) {
      score -= 4;
      findings.push({
        dimension: "hook",
        severity: "fail",
        message: `Cold open matches forbidden pattern (${re.source}). Begin with mystery/tension, not definition or intro.`,
      });
      break;
    }
  }

  if (/\?/.test(open.slice(0, 180))) {
    score += 1.5;
  } else {
    findings.push({
      dimension: "hook",
      severity: "warn",
      message: "No question mark in the first spoken window — consider an immediate unanswered question.",
    });
    score -= 0.5;
  }

  if (CURIOSITY.test(open)) score += 1;
  if (/\borbit\b/i.test(open)) score += 0.5;

  if (SERIES_SUFFIX.test(script)) {
    findings.push({
      dimension: "searchPotential",
      severity: "warn",
      message: "Series suffix detected (e.g. | Orbit's Cosmic Journey). Prefer one-promise titles without series branding.",
    });
  }

  return { score: clampScore(score), findings };
}

function scoreDimension(
  base: number,
  hits: number,
  bonusPerHit: number,
  capBonus: number,
): number {
  return clampScore(base + Math.min(capBonus, hits * bonusPerHit));
}

/**
 * Heuristic reviewer for markdown / plain scripts.
 * Manual overrides can replace any dimension after the fact.
 */
export function reviewScript(
  script: string,
  overrides?: Partial<DimensionScores>,
): ScriptReviewResult {
  const open = firstSpokenWindow(script);
  const words = wordCount(script);
  const estimatedMinutes = words / 150; // calm narration pace
  const chapterMarkers = (script.match(CHAPTER_MARKER) || []).length;
  const questionMarks = (script.match(/\?/g) || []).length;
  const findings: ScriptReviewFinding[] = [];

  const hook = scoreHook(script, open);
  findings.push(...hook.findings);

  const curiosityHits = (script.match(/\b(why|what if|mystery|paradox|unknown|secret)\b/gi) || []).length;
  const curiosity = scoreDimension(5.5, curiosityHits, 0.4, 4);

  let storytelling = 6;
  if (/\b(danger|risk|cross|fall|survive|escape|horizon|signal)\b/i.test(open)) storytelling += 1.5;
  if (chapterMarkers >= 4 && chapterMarkers <= 6) storytelling += 1.5;
  else if (chapterMarkers > 8) {
    storytelling -= 1.5;
    findings.push({
      dimension: "storytelling",
      severity: "warn",
      message: `Found ~${chapterMarkers} chapter markers — aim for 4–6 film-act chapters, not many tiny ones.`,
    });
  } else if (chapterMarkers < 4) {
    findings.push({
      dimension: "storytelling",
      severity: "warn",
      message: "Fewer than 4 chapter markers detected — ensure 4–6 named acts.",
    });
  }
  if (/HOOK|ESCALATION|DISCOVERY|PAYOFF|BIGGER QUESTION/i.test(script)) storytelling += 0.5;
  storytelling = clampScore(storytelling);

  const scienceHits = (script.match(SCIENCE) || []).length;
  const scientificAccuracy = scoreDimension(6.5, scienceHits, 0.25, 3);

  let emotion = YOU_STAKES.test(script) ? 8 : 5.5;
  if (/\byou\b/i.test(script)) emotion += 0.5;
  emotion = clampScore(emotion);
  if (emotion < 7) {
    findings.push({
      dimension: "emotion",
      severity: "warn",
      message: "Add lived stakes (what would YOU see/feel?) so viewers imagine themselves with Orbit.",
    });
  }

  const escalationHits = (script.match(ESCALATION) || []).length;
  const escalation = scoreDimension(5.5, escalationHits, 0.2, 4);

  let retentionPotential = 6;
  if (estimatedMinutes >= 8 && estimatedMinutes <= 12) retentionPotential += 2;
  else if (estimatedMinutes > 16) {
    retentionPotential -= 2;
    findings.push({
      dimension: "retentionPotential",
      severity: "fail",
      message: `Estimated ~${estimatedMinutes.toFixed(1)} min VO — trust-building target is 8–12 minutes.`,
    });
  } else if (estimatedMinutes < 7) {
    findings.push({
      dimension: "retentionPotential",
      severity: "warn",
      message: `Estimated ~${estimatedMinutes.toFixed(1)} min — may be thin; ensure payoff depth.`,
    });
  }
  if (questionMarks >= 6) retentionPotential += 1;
  retentionPotential = clampScore(retentionPotential);

  let searchPotential = 6.5;
  if (/\b(what if|could |happen|survive|inside|dyson|mars|moon|alien|black hole|jupiter)\b/i.test(script)) {
    searchPotential += 1.5;
  }
  if (SERIES_SUFFIX.test(script)) searchPotential -= 1;
  searchPotential = clampScore(searchPotential);

  let visualOpportunities = 5.5;
  if (ORBIT_ACTS_MARKER.test(script) || ACTIVE_ORBIT.test(script)) visualOpportunities += 2.5;
  else {
    findings.push({
      dimension: "visualOpportunities",
      severity: "fail",
      message: "Orbit agency weak — add [ORBIT ACTS: …] where Orbit experiences the science.",
    });
  }
  if (VISUAL_MUST.test(script)) visualOpportunities += 1.5;
  else {
    findings.push({
      dimension: "visualOpportunities",
      severity: "warn",
      message: "Missing [VISUAL MUST: …] markers — required for VO–picture lock.",
    });
  }
  visualOpportunities = clampScore(visualOpportunities);

  let narrationFlow = 7;
  if (TEACH_MARKER.test(script)) narrationFlow += 1;
  if (words > 0 && questionMarks / Math.max(1, words / 200) >= 1) narrationFlow += 0.5;
  if (FORBIDDEN_OPEN_PATTERNS.some((re) => re.test(open))) narrationFlow -= 2;
  narrationFlow = clampScore(narrationFlow);

  const scores: DimensionScores = {
    hook: hook.score,
    curiosity: clampScore(curiosity),
    storytelling,
    scientificAccuracy: clampScore(scientificAccuracy),
    emotion,
    escalation: clampScore(escalation),
    retentionPotential,
    searchPotential,
    visualOpportunities,
    narrationFlow,
  };

  // Structural completeness bonus — Growth System v2 gates present
  const structureGates = [
    !FORBIDDEN_OPEN_PATTERNS.some((re) => re.test(open)),
    ORBIT_ACTS_MARKER.test(script) || ACTIVE_ORBIT.test(script),
    VISUAL_MUST.test(script),
    TEACH_MARKER.test(script),
    chapterMarkers >= 4 && chapterMarkers <= 6,
    estimatedMinutes >= 8 && estimatedMinutes <= 12,
    YOU_STAKES.test(script) || /\byou\b/i.test(open),
    CURIOSITY.test(open),
  ];
  const gatesHit = structureGates.filter(Boolean).length;
  if (gatesHit >= 6) {
    const boostDims: ScriptReviewDimension[] = [
      "escalation",
      "scientificAccuracy",
      "searchPotential",
      "narrationFlow",
      "emotion",
    ];
    const boost = Math.min(1.5, 0.35 * (gatesHit - 5));
    for (const d of boostDims) {
      scores[d] = clampScore(scores[d] + boost);
    }
    findings.push({
      dimension: "overall",
      severity: "info",
      message: `Structure gates ${gatesHit}/8 — applied +${boost.toFixed(2)} completeness boost to supporting dimensions.`,
    });
  }

  Object.assign(scores, overrides);

  // Re-clamp overrides
  for (const key of SCRIPT_REVIEW_DIMENSIONS) {
    scores[key] = clampScore(scores[key]);
  }

  const total = Math.round(
    SCRIPT_REVIEW_DIMENSIONS.reduce((sum, key) => sum + scores[key], 0) * 10,
  ) / 10;
  const passed = total >= PASS_THRESHOLD;

  if (!passed) {
    findings.push({
      dimension: "overall",
      severity: "fail",
      message: `Total ${total}/100 is below pass threshold ${PASS_THRESHOLD}. Rewrite before VO or picture gen.`,
    });
  } else {
    findings.push({
      dimension: "overall",
      severity: "info",
      message: `PASS ${total}/100 — proceed to VO after production checklist.`,
    });
  }

  return {
    scores,
    total,
    maxTotal: 100,
    passed,
    decision: passed ? "PASS" : "REJECT",
    findings,
    estimates: {
      wordCount: words,
      estimatedMinutes: Math.round(estimatedMinutes * 10) / 10,
      chapterMarkers,
      questionMarks,
    },
    coldOpenExcerpt: open.slice(0, 280),
  };
}

export function formatReviewMarkdown(result: ScriptReviewResult, title = "Script review"): string {
  const lines = [
    `# ${title}`,
    "",
    `**Decision:** ${result.decision} · **Score:** ${result.total} / ${result.maxTotal}`,
    "",
    `| Dimension | Score |`,
    `|---|---:|`,
    ...SCRIPT_REVIEW_DIMENSIONS.map(
      (d) => `| ${d} | ${result.scores[d]} |`,
    ),
    "",
    `Words: ${result.estimates.wordCount} · Est. min: ${result.estimates.estimatedMinutes} · Chapters: ${result.estimates.chapterMarkers}`,
    "",
    "## Cold open excerpt",
    "",
    `> ${result.coldOpenExcerpt}`,
    "",
    "## Findings",
    "",
    ...result.findings.map((f) => `- **[${f.severity}] ${f.dimension}:** ${f.message}`),
    "",
  ];
  return lines.join("\n");
}
