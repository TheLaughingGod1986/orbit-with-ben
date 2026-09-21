#!/usr/bin/env node
/**
 * prisma migrate deploy with Neon-friendly unpooled DIRECT_URL + P1002 handling.
 *
 * Vercel Neon integration exposes DATABASE_URL_UNPOOLED / POSTGRES_URL_NON_POOLING.
 * Neon is serverless: advisory locks often flake as Prisma P1002 (even on unpooled).
 * Prisma documents disabling the advisory lock for serverless providers.
 *
 * Preference (first non-empty wins):
 *   DATABASE_URL_UNPOOLED → POSTGRES_URL_NON_POOLING → DIRECT_URL → DATABASE_URL
 *
 * Never logs connection strings.
 */
import { spawn } from "node:child_process";

const MAX_ATTEMPTS = 4;
const BASE_DELAY_MS = 3000;

function pickDirectUrl() {
  const candidates = [
    ["DATABASE_URL_UNPOOLED", process.env.DATABASE_URL_UNPOOLED],
    ["POSTGRES_URL_NON_POOLING", process.env.POSTGRES_URL_NON_POOLING],
    ["DIRECT_URL", process.env.DIRECT_URL],
    ["DATABASE_URL", process.env.DATABASE_URL],
  ];
  for (const [name, value] of candidates) {
    const trimmed = value?.trim();
    if (trimmed) return { name, value: trimmed };
  }
  return null;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function runMigrate(directUrl, { disableAdvisoryLock }) {
  return new Promise((resolve) => {
    const env = {
      ...process.env,
      DIRECT_URL: directUrl,
    };
    if (disableAdvisoryLock) {
      // Neon / serverless: https://www.prisma.io/docs/orm/reference/environment-variables-reference
      env.PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK = "1";
    }
    const child = spawn("npx", ["prisma", "migrate", "deploy"], {
      env,
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    child.on("error", (err) => {
      console.error("prisma-migrate-deploy: failed to spawn prisma:", err.message);
      resolve(1);
    });
    child.on("close", (code) => resolve(code ?? 1));
  });
}

async function main() {
  const picked = pickDirectUrl();
  if (!picked) {
    console.error(
      "prisma-migrate-deploy: missing DATABASE_URL_UNPOOLED / POSTGRES_URL_NON_POOLING / DIRECT_URL / DATABASE_URL",
    );
    process.exit(1);
  }

  console.log(
    `prisma-migrate-deploy: DIRECT_URL resolved from ${picked.name} (value not printed)`,
  );

  // Attempt 1–2: normal migrate (lock on). Remaining: Neon serverless path without advisory lock.
  let delay = BASE_DELAY_MS;
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    const disableAdvisoryLock = attempt >= 3;
    if (disableAdvisoryLock) {
      console.warn(
        "prisma-migrate-deploy: retrying with PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK=1 (Neon serverless)",
      );
    }
    const code = await runMigrate(picked.value, { disableAdvisoryLock });
    if (code === 0) {
      process.exit(0);
    }
    if (attempt === MAX_ATTEMPTS) {
      console.error(
        `prisma-migrate-deploy: failed after ${MAX_ATTEMPTS} attempts (last exit ${code})`,
      );
      process.exit(code);
    }
    console.warn(
      `prisma-migrate-deploy: attempt ${attempt}/${MAX_ATTEMPTS} failed (often Prisma P1002). Retrying in ${delay}ms…`,
    );
    await sleep(delay);
    delay = Math.min(delay * 2, 15_000);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
