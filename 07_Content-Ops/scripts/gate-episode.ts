#!/usr/bin/env tsx
/**
 * Growth System v2 episode gate — block VO/Veo until checks pass.
 *
 * Usage:
 *   npm run gate:episode -- --project ../02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star
 *   npm run gate:episode -- --project /abs/path --script /abs/script.md --json
 */
import fs from "fs";
import path from "path";
import { formatGateMarkdown, gateEpisode } from "../src/lib/analytics/episode-gate";

function argValue(flag: string): string | undefined {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function main() {
  const project = argValue("--project") || argValue("-p");
  if (!project) {
    console.error(
      "Usage: npm run gate:episode -- --project <02_Video-Projects/NNN_Slug> [--script file.md] [--require-checklist] [--json]",
    );
    process.exit(2);
  }
  const result = gateEpisode({
    projectDir: path.resolve(project),
    scriptPath: argValue("--script"),
    requireChecklist: process.argv.includes("--require-checklist"),
  });

  if (process.argv.includes("--json")) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(formatGateMarkdown(result));
  }

  const outFlag = argValue("--out");
  if (outFlag) {
    const out = path.resolve(outFlag);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, formatGateMarkdown(result));
    console.error(`Wrote ${out}`);
  }

  process.exit(result.passed ? 0 : 1);
}

main();
