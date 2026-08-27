import { prisma } from "@/lib/storage/prisma";
import { PLATFORMS } from "@/config/platforms";
import { getPublishingAdapter } from "@/lib/publishing/adapters";
import { isDryRun, hasGoogleOAuth, hasMetaOAuth, hasTikTokOAuth, hasXOAuth, hasThreadsOAuth } from "@/lib/env";
import { getPublicBaseUrl } from "@/lib/public-base-url";
import { ConnectionActions } from "@/components/ConnectionActions";
import { MetaPageSelector } from "@/components/MetaPageSelector";
import Link from "next/link";
import { headers } from "next/headers";

export const dynamic = "force-dynamic";

const CARDS: {
  platform: string;
  label: string;
  connectPath?: string;
  oauthReady: () => boolean;
}[] = [
  { platform: "youtube_shorts", label: "YouTube", connectPath: "/api/oauth/google/start", oauthReady: hasGoogleOAuth },
  { platform: "instagram_reels", label: "Instagram Reels", connectPath: "/api/oauth/meta/start", oauthReady: hasMetaOAuth },
  { platform: "facebook_reels", label: "Facebook Reels", connectPath: "/api/oauth/meta/start", oauthReady: hasMetaOAuth },
  { platform: "tiktok", label: "TikTok", connectPath: "/api/oauth/tiktok/start", oauthReady: hasTikTokOAuth },
  { platform: "x", label: "X", connectPath: "/api/oauth/x/start", oauthReady: hasXOAuth },
  { platform: "threads", label: "Threads", oauthReady: hasThreadsOAuth },
];

export default async function ConnectionsPage({
  searchParams,
}: {
  searchParams: Promise<{ connected?: string; error?: string }>;
}) {
  const sp = await searchParams;
  const headerList = await headers();
  const publicBase = getPublicBaseUrl({ headers: headerList });
  const connections = await prisma.platformConnection.findMany({
    where: { disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  const heartbeat = await prisma.workerHeartbeat.findFirst({
    orderBy: { lastHeartbeatAt: "desc" },
  });
  const workerOnline =
    heartbeat && Date.now() - heartbeat.lastHeartbeatAt.getTime() < 30_000;

  return (
    <div className="space-y-6">
      {isDryRun() ? (
        <div className="rounded-xl border border-[#FFC85A]/40 bg-[#FFC85A]/15 px-4 py-3 text-sm text-[#FFC85A]">
          Dry-run mode is active. No content will be published.
        </div>
      ) : null}
      {sp.error ? (
        <div className="rounded-xl border border-red-400/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          Connection error: {sp.error}
        </div>
      ) : null}
      {sp.connected ? (
        <div className="rounded-xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
          Connected: {sp.connected}
        </div>
      ) : null}

      <div>
        <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl">Connections</h1>
        <p className="mt-2 text-[#F5E8D2]/60">
          Official OAuth only. Tokens are encrypted server-side and never shown in the browser.
        </p>
        <p className="mt-2 text-sm text-[#5A6E82]">
          Worker: {workerOnline ? "online" : "offline"}
          {heartbeat ? ` · last heartbeat ${heartbeat.lastHeartbeatAt.toISOString()}` : ""}
          {" · "}
          Local scheduling requires `npm run worker` (or `npm run dev:all`). Sleep/offline stops publishes.
        </p>
        <p className="mt-1 text-sm text-[#5A6E82]">
          Setup guides live in <code className="text-[#FF7A24]">07_Content-Ops/docs/</code>.{" "}
          <Link href="/settings" className="text-[#FF7A24]">
            Platform metadata settings →
          </Link>
        </p>
      </div>

      <div className="grid gap-4">
        {CARDS.map((card) => {
          const conn =
            connections.find((c) => c.platform === card.platform) ||
            (card.platform === "instagram_reels" || card.platform === "facebook_reels"
              ? connections.find((c) => c.platform === "meta")
              : undefined);
          const adapter = getPublishingAdapter(card.platform);
          const caps = adapter.getCapabilities(conn || null);
          const color = PLATFORMS[card.platform as keyof typeof PLATFORMS]?.color || "#FF7A24";

          return (
            <div key={card.platform} className="card-panel p-5">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <div className="text-sm font-medium" style={{ color }}>
                    {card.label}
                  </div>
                  <div className="mt-1 text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                    {conn?.connectionStatus || "not connected"} ·{" "}
                    {caps.canPublishDirectly
                      ? "direct publish available"
                      : caps.canUploadDraft
                        ? "draft upload available"
                        : "manual fallback"}
                  </div>
                  {conn ? (
                    <div className="mt-3 space-y-1 text-sm text-[#F5E8D2]/75">
                      <div>{conn.accountName || conn.accountUsername || conn.externalUserId}</div>
                      {conn.accountUsername ? <div>@{conn.accountUsername.replace(/^@/, "")}</div> : null}
                      {conn.channelId ? <div>Channel: {conn.channelId}</div> : null}
                      {conn.pageId ? <div>Page: {conn.pageId}</div> : null}
                      {conn.instagramBusinessAccountId ? (
                        <div>IG pro: {conn.instagramBusinessAccountId}</div>
                      ) : null}
                      <div className="text-xs text-[#5A6E82]">
                        Last validated: {conn.lastValidatedAt?.toISOString() || "—"}
                      </div>
                      <div className="text-xs text-[#5A6E82]">
                        Token expiry: {conn.accessTokenExpiresAt?.toISOString() || "—"}
                      </div>
                      <div className="text-xs text-[#5A6E82]">
                        Last successful publish:{" "}
                        {conn.lastSuccessfulPublishAt?.toISOString() || "—"}
                      </div>
                      {conn.grantedScopes ? (
                        <div className="text-xs text-[#F5E8D2]/5">
                          Scopes: {(JSON.parse(conn.grantedScopes) as string[]).join(", ")}
                        </div>
                      ) : null}
                      {conn.lastConnectionError ? (
                        <div className="text-xs text-[#FFC85A]">{conn.lastConnectionError}</div>
                      ) : null}
                    </div>
                  ) : (
                    <p className="mt-3 text-sm text-[#F5E8D2]/55">
                      {card.oauthReady()
                        ? "App credentials detected. Connect your account."
                        : "Add OAuth credentials to .env, then connect."}
                    </p>
                  )}
                  <ul className="mt-3 list-disc pl-5 text-xs text-[#F5E8D2]/45">
                    {caps.limitations.map((l) => (
                      <li key={l}>{l}</li>
                    ))}
                  </ul>
                  {conn?.platform === "meta" ? (
                    <MetaPageSelector connectionId={conn.id} metadataJson={conn.metadataJson} />
                  ) : null}
                </div>
                <ConnectionActions
                  platform={card.platform}
                  connectionId={conn?.id}
                  connectPath={card.connectPath}
                  canConnect={card.oauthReady()}
                />
              </div>
            </div>
          );
        })}
      </div>

      <div className="card-panel p-5 text-sm text-[#F5E8D2]/65">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
          Callback URLs
        </h2>
        <p className="mt-2 text-xs text-[#5A6E82]">
          Register these exact URIs with each provider. Derived from{" "}
          <code className="text-[#F5E8D2]/70">APP_BASE_URL</code> / this deploy’s public host (
          {publicBase}).
        </p>
        <ul className="mt-3 space-y-1 font-mono text-xs break-all">
          <li>{publicBase}/api/oauth/google/callback</li>
          <li>{publicBase}/api/oauth/meta/callback</li>
          <li>{publicBase}/api/oauth/tiktok/callback</li>
          <li>{publicBase}/api/oauth/x/callback</li>
        </ul>
      </div>
    </div>
  );
}
