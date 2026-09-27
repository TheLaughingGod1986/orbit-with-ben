#!/usr/bin/env tsx
/**
 * One-time YouTube sign-in for the local scripts. Opens Google's consent page, catches
 * the reply on localhost, and saves YOUTUBE_REFRESH_TOKEN into 07_Content-Ops/.env.
 * Nothing secret is printed. Run it again if a script says the login expired.
 *
 *   cd 07_Content-Ops && npx tsx --env-file=.env scripts/youtube-auth.ts
 *
 * Needs GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET in .env (the Google Cloud OAuth client),
 * with http://localhost:3000/api/oauth/google/callback as an authorised redirect URI
 * (or set YOUTUBE_AUTH_REDIRECT_URI to another localhost URI registered on the client).
 * Sign in as the Orbit With Ben channel.
 */
import fs from "fs";
import http from "http";
import path from "path";
import crypto from "crypto";
import { execFile } from "child_process";
import { YOUTUBE_SCOPES } from "../src/lib/youtube/upload";

const ENV_FILE = path.resolve(__dirname, "../.env");
const CHANNEL_ID = "UC_esArsDKd3GJvOkeO0DUog";

function redirectUri(): URL {
  const candidates = [process.env.YOUTUBE_AUTH_REDIRECT_URI, process.env.GOOGLE_REDIRECT_URI];
  const local = candidates.find((u) => u && /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?\//.test(u));
  return new URL(local || "http://localhost:3000/api/oauth/google/callback");
}

/** Replace or add KEY=value in .env without touching other lines. */
export function upsertEnvLine(text: string, key: string, value: string): string {
  const line = `${key}=${value}`;
  const re = new RegExp(`^${key}=.*$`, "m");
  if (re.test(text)) return text.replace(re, line);
  return `${text.replace(/\n*$/, "\n")}${line}\n`;
}

async function main() {
  const { GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET } = process.env;
  if (!GOOGLE_CLIENT_ID || !GOOGLE_CLIENT_SECRET) throw new Error("GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET missing from .env");
  const redirect = redirectUri();
  const state = crypto.randomBytes(16).toString("hex");
  const auth = new URL("https://accounts.google.com/o/oauth2/v2/auth");
  auth.search = new URLSearchParams({
    client_id: GOOGLE_CLIENT_ID,
    redirect_uri: redirect.toString(),
    response_type: "code",
    scope: YOUTUBE_SCOPES.join(" "),
    access_type: "offline",
    prompt: "consent",
    state,
  }).toString();

  const code = await new Promise<string>((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const url = new URL(req.url || "/", redirect.origin);
      if (url.pathname !== redirect.pathname) {
        res.writeHead(404).end();
        return;
      }
      const ok = url.searchParams.get("state") === state && url.searchParams.get("code");
      res.writeHead(ok ? 200 : 400, { "Content-Type": "text/plain" });
      res.end(ok ? "Orbit With Ben: YouTube connected. You can close this tab." : "Sign-in failed. Check the terminal.");
      server.close();
      if (ok) resolve(url.searchParams.get("code")!);
      else reject(new Error(`Google returned ${url.searchParams.get("error") || "a mismatched state"}`));
    });
    server.listen(Number(redirect.port || 80), redirect.hostname, () => {
      console.log(`Open this link and sign in as Orbit With Ben:\n\n${auth.toString()}\n`);
      if (process.platform === "darwin") execFile("open", [auth.toString()], () => undefined);
    });
    server.on("error", reject);
  });

  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      code,
      client_id: GOOGLE_CLIENT_ID,
      client_secret: GOOGLE_CLIENT_SECRET,
      redirect_uri: redirect.toString(),
      grant_type: "authorization_code",
    }),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok || !body.refresh_token) {
    throw new Error(`Token exchange failed: ${body.error || res.status}${body.refresh_token ? "" : " (no refresh token returned)"}`);
  }

  const current = fs.existsSync(ENV_FILE) ? fs.readFileSync(ENV_FILE, "utf8") : "";
  fs.writeFileSync(ENV_FILE, upsertEnvLine(current, "YOUTUBE_REFRESH_TOKEN", body.refresh_token), { mode: 0o600 });

  const ch = await fetch("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", {
    headers: { Authorization: `Bearer ${body.access_token}` },
  }).then((r) => r.json());
  const channel = ch.items?.[0];
  console.log(`Saved YOUTUBE_REFRESH_TOKEN to .env. Signed in as: ${channel?.snippet?.title ?? "unknown"} (${channel?.id ?? "?"})`);
  if (channel?.id !== CHANNEL_ID) console.error(`Warning: that is not Orbit With Ben (${CHANNEL_ID}). Run again and pick the right channel.`);
}

if (require.main === module) {
  main().catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exit(1);
  });
}
