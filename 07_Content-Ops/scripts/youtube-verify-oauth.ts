#!/usr/bin/env tsx
/**
 * Verify YouTube OAuth scopes + safe no-op videos.update.
 *
 *   npm run youtube:verify-oauth
 *   npm run youtube:verify-oauth -- --video 3xrxdmaOwJI
 *   npm run youtube:verify-oauth -- --print-auth-url
 *
 * Never prints access/refresh tokens.
 */
import { randomUUID } from "crypto";
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import {
  YT_FORCE_SSL_SCOPE,
  buildYouTubeOAuthAuthorizationUrl,
  classifyOAuthHttpError,
  hasForceSslScope,
  missingRequiredScopes,
  parseGrantedScopes,
} from "../src/lib/publishing/youtube-oauth";

function flag(name: string): boolean {
  return process.argv.includes(`--${name}`);
}

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

const SAFE_VIDEO = "3xrxdmaOwJI";
const AUDIT_DIR = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07",
);

async function refreshIfNeeded(connectionId: string) {
  const adapter = new YouTubePublishingAdapter();
  const connection = await prisma.platformConnection.findUnique({ where: { id: connectionId } });
  if (!connection) throw new Error("connection missing");
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    const refreshed = await adapter.refreshConnection(connection);
    if (!refreshed.ok) {
      return { ok: false as const, kind: "expired_token" as const, message: refreshed.message };
    }
  }
  const fresh = await prisma.platformConnection.findUnique({ where: { id: connectionId } });
  if (!fresh?.accessTokenEncrypted) {
    return { ok: false as const, kind: "no_connection" as const, message: "No access token" };
  }
  return { ok: true as const, connection: fresh, accessToken: decryptSecret(fresh.accessTokenEncrypted) };
}

async function main() {
  getEnv();
  const videoId = arg("video") || SAFE_VIDEO;
  const printAuthUrl = flag("print-auth-url");

  const connection = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });

  if (!connection) {
    console.log(
      JSON.stringify(
        {
          ok: false,
          failure: "no_connection",
          remediation:
            "Start Content Ops (`npm run dev`) and open /settings/connections to connect Google with youtube.force-ssl.",
        },
        null,
        2,
      ),
    );
    process.exit(2);
  }

  const scopesBefore = parseGrantedScopes(connection.grantedScopes);
  const forceSslBefore = hasForceSslScope(scopesBefore);
  const missing = missingRequiredScopes(scopesBefore);

  if (printAuthUrl || !forceSslBefore) {
    const state = `youtube-reconnect-${randomUUID()}`;
    const authUrl = buildYouTubeOAuthAuthorizationUrl({ state });
    const payload = {
      ok: forceSslBefore,
      scopesBefore,
      forceSslGranted: forceSslBefore,
      missingScopes: missing,
      reconnectRequired: !forceSslBefore,
      authorizationUrl: authUrl,
      remediation: forceSslBefore
        ? null
        : "Open authorizationUrl while Content Ops is running, complete consent, then re-run npm run youtube:verify-oauth",
      note: "Tokens are never printed. State must go through /api/oauth/google/start for CSRF — prefer that UI path.",
      preferredReconnect: `${getEnv().APP_BASE_URL}/settings/connections`,
    };
    console.log(JSON.stringify(payload, null, 2));
    fs.mkdirSync(AUDIT_DIR, { recursive: true });
    fs.writeFileSync(
      path.join(AUDIT_DIR, "OAUTH_VERIFY_LAST.json"),
      JSON.stringify({ ...payload, authorizationUrl: "[redacted-from-disk-optional]" }, null, 2) +
        "\n",
    );
    if (!forceSslBefore) {
      console.error("FAIL: youtube.force-ssl missing — reconnect required before videos.update");
      process.exit(3);
    }
  }

  const refreshed = await refreshIfNeeded(connection.id);
  if (!refreshed.ok) {
    console.log(
      JSON.stringify(
        {
          ok: false,
          failure: refreshed.kind,
          message: refreshed.message,
          remediation:
            refreshed.kind === "expired_token" || refreshed.kind === "revoked_token"
              ? "Reconnect Google OAuth from /settings/connections"
              : "Check GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET",
        },
        null,
        2,
      ),
    );
    process.exit(4);
  }

  const { accessToken, connection: fresh } = refreshed;
  const scopes = parseGrantedScopes(fresh.grantedScopes);
  const forceSsl = hasForceSslScope(scopes);

  // Fetch current resource
  const getRes = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(videoId)}`,
    { headers: { Authorization: `Bearer ${accessToken}` } },
  );
  const getBody = await getRes.json();
  if (!getRes.ok) {
    const kind = classifyOAuthHttpError(getRes.status, JSON.stringify(getBody));
    console.log(JSON.stringify({ ok: false, failure: kind, step: "videos.list", status: getRes.status }, null, 2));
    process.exit(5);
  }
  const item = getBody.items?.[0];
  if (!item) {
    console.log(JSON.stringify({ ok: false, failure: "unknown", message: `Video ${videoId} not found` }, null, 2));
    process.exit(6);
  }

  const original = {
    title: item.snippet?.title,
    description: item.snippet?.description,
    categoryId: item.snippet?.categoryId,
    tags: item.snippet?.tags || [],
    privacyStatus: item.status?.privacyStatus,
    publishAt: item.status?.publishAt || null,
    madeForKids: item.status?.madeForKids,
    selfDeclaredMadeForKids: item.status?.selfDeclaredMadeForKids,
    embeddable: item.status?.embeddable,
  };

  // Same-value update (no material change)
  const updateRes = await fetch(
    "https://www.googleapis.com/youtube/v3/videos?part=snippet,status",
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: videoId,
        snippet: {
          title: original.title,
          description: original.description,
          categoryId: original.categoryId,
          tags: original.tags,
        },
        status: {
          privacyStatus: original.privacyStatus,
          ...(original.publishAt ? { publishAt: original.publishAt } : {}),
          selfDeclaredMadeForKids: Boolean(original.selfDeclaredMadeForKids),
          embeddable: original.embeddable,
        },
      }),
    },
  );
  const updateBody = await updateRes.json().catch(() => ({}));

  if (!updateRes.ok) {
    const kind = classifyOAuthHttpError(updateRes.status, JSON.stringify(updateBody));
    const out = {
      ok: false,
      forceSslGranted: forceSsl,
      videosUpdatePermitted: false,
      failure: kind,
      httpStatus: updateRes.status,
      remediation:
        kind === "missing_scope"
          ? "Reconnect OAuth with youtube.force-ssl via /settings/connections (prompt=consent)."
          : kind === "expired_token" || kind === "revoked_token"
            ? "Token expired/revoked — reconnect Google."
            : kind === "invalid_client"
              ? "Check GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET in .env"
              : "Inspect YouTube API error; do not retry with a replacement upload.",
    };
    console.log(JSON.stringify(out, null, 2));
    console.error("FAIL: videos.update not permitted");
    process.exit(7);
  }

  const verifyRes = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(videoId)}`,
    { headers: { Authorization: `Bearer ${accessToken}` } },
  );
  const verifyBody = await verifyRes.json();
  const after = verifyBody.items?.[0];
  const unchanged =
    after?.snippet?.title === original.title &&
    after?.snippet?.description === original.description &&
    after?.snippet?.categoryId === original.categoryId &&
    after?.status?.privacyStatus === original.privacyStatus &&
    (after?.status?.publishAt || null) === original.publishAt &&
    after?.status?.madeForKids === original.madeForKids;

  const result = {
    ok: forceSsl && updateRes.ok && unchanged,
    videoId,
    scopesBefore,
    scopesAfter: scopes,
    forceSslGranted: forceSsl,
    videosUpdatePermitted: true,
    videoStateUnchanged: unchanged,
    reconnectRequired: !forceSsl,
    checks: [
      forceSsl ? "PASS: youtube.force-ssl granted" : "FAIL: youtube.force-ssl missing",
      "PASS: videos.update permitted",
      unchanged ? "PASS: video state unchanged" : "FAIL: video state changed unexpectedly",
    ],
  };

  console.log(JSON.stringify(result, null, 2));
  fs.mkdirSync(AUDIT_DIR, { recursive: true });
  fs.writeFileSync(path.join(AUDIT_DIR, "OAUTH_VERIFY_LAST.json"), JSON.stringify(result, null, 2) + "\n");

  for (const line of result.checks) console.error(line);
  process.exit(result.ok ? 0 : 8);
}

main()
  .catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
