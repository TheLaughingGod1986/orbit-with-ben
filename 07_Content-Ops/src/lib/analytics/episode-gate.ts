/**
 * Episode production gate — Growth System v2.
 * Blocks VO / AI Studio Veo until audit + script ≥90 + markers are present.
 */

import fs from "fs";
import path from "path";
import { reviewScript, PASS_THRESHOLD, type ScriptReviewResult } from "./script-reviewer";

export type GateCheck = {
  id: string;
  ok: boolean;
  severity: "fail" | "warn" | "info";
  message: string;
};

export type EpisodeGateResult = {
  projectDir: string;
  passed: boolean;
  checks: GateCheck[];
  scriptPath?: string;
  scriptReview?: ScriptReviewResult;
};

function exists(p: string): boolean {
  try {
    return fs.existsSync(p);
  } catch {
    return false;
  }
}

function readText(p: string): string {
  return fs.readFileSync(p, "utf8");
}

function findScripts(projectDir: string, explicit?: string): string[] {
  if (explicit) return [path.resolve(explicit)];
  const scriptDir = path.join(projectDir, "01_Script");
  const candidates: string[] = [];
  if (exists(scriptDir)) {
    for (const name of fs.readdirSync(scriptDir)) {
      if (/\.(md|txt)$/i.test(name) && !/readme/i.test(name)) {
        candidates.push(path.join(scriptDir, name));
      }
    }
  }
  // Prefer master / draft names
  candidates.sort((a, b) => {
    const score = (f: string) => {
      const n = path.basename(f).toLowerCase();
      if (n.includes("master")) return 0;
      if (n.includes("draft")) return 1;
      if (n.includes("script")) return 2;
      return 3;
    };
    return score(a) - score(b) || a.localeCompare(b);
  });
  return candidates;
}

function countMatches(text: string, re: RegExp): number {
  return (text.match(re) || []).length;
}

function auditLooksSigned(text: string): boolean {
  // Require a real name/initials after "Signed off by:" (not empty / not markdown-only)
  const signedBy = text.match(/signed\s*off\s*by:\s*\**\s*([^\n*]+)/i);
  const who = signedBy?.[1]?.trim() ?? "";
  if (who.length >= 2 && !/^_+$/.test(who) && !/^date:/i.test(who)) {
    return true;
  }

  const checked = (re: RegExp) => re.test(text);
  const hasKeywords = checked(/\[\s*[xX]\s*\].*keywords/i);
  const hasTitle = checked(/\[\s*[xX]\s*\].*title/i);
  const hasScriptReview = checked(/\[\s*[xX]\s*\].*script reviewer/i);
  if (hasKeywords && hasTitle && hasScriptReview) return true;

  return false;
}

/**
 * Run Growth System v2 gate against a video project directory.
 */
export function gateEpisode(opts: {
  projectDir: string;
  scriptPath?: string;
  requireChecklist?: boolean;
  minOrbitActs?: number;
  minVisualMust?: number;
  minTeach?: number;
}): EpisodeGateResult {
  const projectDir = path.resolve(opts.projectDir);
  const checks: GateCheck[] = [];
  const minOrbit = opts.minOrbitActs ?? 4;
  const minVisual = opts.minVisualMust ?? 4;
  const minTeach = opts.minTeach ?? 4;

  if (!exists(projectDir) || !fs.statSync(projectDir).isDirectory()) {
    return {
      projectDir,
      passed: false,
      checks: [
        {
          id: "project_dir",
          ok: false,
          severity: "fail",
          message: `Project directory not found: ${projectDir}`,
        },
      ],
    };
  }

  checks.push({
    id: "project_dir",
    ok: true,
    severity: "info",
    message: `Project: ${projectDir}`,
  });

  const auditPath = path.join(projectDir, "11_Upload-Package", "PRE_BUILD_VIDIQ_AUDIT.md");
  if (!exists(auditPath)) {
    checks.push({
      id: "prebuild_vidiq",
      ok: false,
      severity: "fail",
      message:
        "Missing 11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md — copy from PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md and sign off.",
    });
  } else {
    const audit = readText(auditPath);
    const signed = auditLooksSigned(audit);
    checks.push({
      id: "prebuild_vidiq",
      ok: signed,
      severity: signed ? "info" : "fail",
      message: signed
        ? "Pre-build vidIQ audit present and looks signed off."
        : "Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by).",
    });
  }

  const scripts = findScripts(projectDir, opts.scriptPath);
  let scriptPath: string | undefined;
  let scriptReview: ScriptReviewResult | undefined;

  if (!scripts.length) {
    checks.push({
      id: "script_file",
      ok: false,
      severity: "fail",
      message: "No script found in 01_Script/ — add a .md draft before VO/Veo.",
    });
  } else {
    scriptPath = scripts[0];
    const script = readText(scriptPath);
    checks.push({
      id: "script_file",
      ok: true,
      severity: "info",
      message: `Script: ${path.relative(projectDir, scriptPath)}`,
    });

    scriptReview = reviewScript(script);
    checks.push({
      id: "script_review",
      ok: scriptReview.passed,
      severity: scriptReview.passed ? "info" : "fail",
      message: `Script reviewer ${scriptReview.decision} ${scriptReview.total}/${PASS_THRESHOLD} (need ≥${PASS_THRESHOLD}).`,
    });

    const orbitActs = countMatches(script, /\[ORBIT ACTS:/gi);
    const visualMust = countMatches(script, /\[VISUAL MUST:/gi);
    const teach = countMatches(script, /\[TEACH:/gi);
    const chapters = countMatches(script, /\[CHAPTER CARD:/gi);

    checks.push({
      id: "orbit_acts",
      ok: orbitActs >= minOrbit,
      severity: orbitActs >= minOrbit ? "info" : "fail",
      message: `[ORBIT ACTS] count ${orbitActs} (need ≥${minOrbit}).`,
    });
    checks.push({
      id: "visual_must",
      ok: visualMust >= minVisual,
      severity: visualMust >= minVisual ? "info" : "fail",
      message: `[VISUAL MUST] count ${visualMust} (need ≥${minVisual}).`,
    });
    checks.push({
      id: "teach",
      ok: teach >= minTeach,
      severity: teach >= minTeach ? "info" : "fail",
      message: `[TEACH] count ${teach} (need ≥${minTeach}).`,
    });
    checks.push({
      id: "chapters",
      ok: chapters >= 4 && chapters <= 8,
      severity: chapters >= 4 && chapters <= 8 ? "info" : "warn",
      message: `[CHAPTER CARD] count ${chapters} (aim 4–6 film acts).`,
    });
  }

  const checklistCandidates = [
    path.join(projectDir, "11_Upload-Package", "PRODUCTION_CHECKLIST_V2.md"),
    path.join(projectDir, "PRODUCTION_CHECKLIST_V2.md"),
  ];
  const checklistPath = checklistCandidates.find(exists);
  if (opts.requireChecklist) {
    checks.push({
      id: "production_checklist",
      ok: Boolean(checklistPath),
      severity: checklistPath ? "info" : "fail",
      message: checklistPath
        ? `Checklist: ${path.relative(projectDir, checklistPath)}`
        : "Missing PRODUCTION_CHECKLIST_V2.md in project (copy from Channel-Setup/templates/).",
    });
  } else if (!checklistPath) {
    checks.push({
      id: "production_checklist",
      ok: true,
      severity: "warn",
      message: "No PRODUCTION_CHECKLIST_V2.md yet — add before publish.",
    });
  } else {
    checks.push({
      id: "production_checklist",
      ok: true,
      severity: "info",
      message: `Checklist present: ${path.relative(projectDir, checklistPath)}`,
    });
  }

  const envExample = path.join(projectDir, "07_Edit-Project", ".env.example");
  if (!exists(envExample) && !exists(path.join(projectDir, "07_Edit-Project", ".env"))) {
    checks.push({
      id: "aistudio_env",
      ok: true,
      severity: "warn",
      message:
        "No 07_Edit-Project/.env.example — ensure AI Studio Ultra login (orbit_aistudio_veo_ui.py --login) before Veo spend.",
    });
  }

  const passed = checks.every((c) => c.severity !== "fail" || c.ok);

  return { projectDir, passed, checks, scriptPath, scriptReview };
}

export function formatGateMarkdown(result: EpisodeGateResult): string {
  const lines = [
    `# Episode gate — ${path.basename(result.projectDir)}`,
    "",
    `**Decision:** ${result.passed ? "PASS" : "BLOCK"} — VO / AI Studio Veo ${result.passed ? "allowed" : "blocked"}`,
    "",
    "| Check | Status | Detail |",
    "|---|---|---|",
    ...result.checks.map((c) => {
      const icon = c.ok ? (c.severity === "warn" ? "WARN" : "OK") : "FAIL";
      return `| ${c.id} | ${icon} | ${c.message.replace(/\|/g, "/")} |`;
    }),
    "",
  ];
  if (result.scriptReview) {
    lines.push(
      `Script score: **${result.scriptReview.total}/100** · ${result.scriptReview.decision}`,
      "",
      `Cold open: ${result.scriptReview.coldOpenExcerpt.slice(0, 200)}…`,
      "",
    );
  }
  if (!result.passed) {
    lines.push(
      "## Next actions",
      "",
      ...result.checks
        .filter((c) => !c.ok && c.severity === "fail")
        .map((c) => `- Fix **${c.id}**: ${c.message}`),
      "",
    );
  }
  return lines.join("\n");
}
