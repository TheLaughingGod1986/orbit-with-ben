#!/usr/bin/env node
/**
 * prisma migrate deploy with Neon-friendly unpooled DIRECT_URL + P1002 retry.
 *
 * Vercel Neon integration exposes DATABASE_URL_UNPOOLED / POSTGRES_URL_NON_POOLING.
 * Advisory locks via a pooled URL often flake as Prisma P1002 during Vercel builds.
 *
 * Preference (first non-empty wins):
 *   DATABASE_URL_UNPOOLED → POSTGRES_URL_NON_POOLING → DIRECT_URL → DATABASE_URL
 *
 * Never logs connection strings.
 */
import { spawn } from "node:child_process";

const MAX_ATTEMPTS = 5;
const BASE_DELAY_MS = 2500;

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

function runMigrate(directUrl) {
  return new Promise((resolve) => {
    const child = spawn("npx", ["prisma", "migrate", "deploy"], {
      env: { ...process.env, DIRECT_URL: directUrl },
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

  let delay = BASE_DELAY_MS;
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    const code = await runMigrate(picked.value);
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
      `prisma-migrate-deploy: attempt ${attempt}/${MAX_ATTEMPTS} failed (often Prisma P1002 advisory lock). Retrying in ${delay}ms…`,
    );
    await sleep(delay);
    delay = Math.min(delay * 2, 20_000);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
