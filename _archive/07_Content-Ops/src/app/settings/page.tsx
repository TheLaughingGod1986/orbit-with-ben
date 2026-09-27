import { prisma } from "@/lib/storage/prisma";
import { PLATFORMS } from "@/config/platforms";
import { getAdapterForPlatform } from "@/lib/publishing/adapters";
import { PlatformSettingsForm } from "@/components/PlatformSettingsForm";
import Link from "next/link";

export const dynamic = "force-dynamic";

export default async function SettingsPage() {
  const [settings, templates] = await Promise.all([
    prisma.platformSettings.findMany({ orderBy: { platform: "asc" } }),
    prisma.contentTemplate.findMany({ orderBy: { key: "asc" } }),
  ]);

  const connectionStatuses = await Promise.all(
    settings.map(async (s) => {
      const adapter = getAdapterForPlatform(s.platform);
      const status = await adapter.getStatus();
      return { platform: s.platform, status };
    }),
  );

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl">Platform settings</h1>
        <p className="mt-2 text-[#F5E8D2]/60">
          Secrets stay in environment variables. Tokens are never shown in the browser.{" "}
          <Link href="/settings/connections" className="text-[#FF7A24]">
            Manage OAuth connections →
          </Link>
        </p>
      </div>

      {settings.length === 0 ? (
        <div className="card-panel space-y-3 p-6">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
            No platform rows yet.
          </h2>
          <p className="text-sm text-[#F5E8D2]/65">
            Connect an account first. Platform metadata appears here after OAuth creates the
            settings row.
          </p>
          <Link href="/settings/connections" className="text-sm text-[#FF7A24] hover:underline">
            Open connections →
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {settings.map((s) => {
            const conn = connectionStatuses.find((c) => c.platform === s.platform);
            return (
              <div key={s.id} className="card-panel p-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <div
                      className="text-sm font-medium"
                      style={{ color: PLATFORMS[s.platform as keyof typeof PLATFORMS]?.color }}
                    >
                      {PLATFORMS[s.platform as keyof typeof PLATFORMS]?.label || s.platform}
                    </div>
                    <div className="mt-1 text-xs text-[#5A6E82]">
                      {s.enabled ? "Enabled" : "Disabled"} · {s.publishingMethod} · token{" "}
                      {s.tokenStatus}
                    </div>
                    <div className="mt-2 text-sm text-[#FFC85A]">
                      Connection: {conn?.status.connection.replace(/_/g, " ")}
                    </div>
                    <div className="text-xs text-[#F5E8D2]/50">{conn?.status.detail}</div>
                  </div>
                </div>
                <PlatformSettingsForm
                  id={s.id}
                  enabled={s.enabled}
                  accountDisplayName={s.accountDisplayName || ""}
                  profileUrl={s.profileUrl || ""}
                  defaultCallToAction={s.defaultCallToAction || ""}
                  defaultHashtags={s.defaultHashtags || "[]"}
                  publishingMethod={s.publishingMethod}
                  defaultVisibility={s.defaultVisibility}
                />
              </div>
            );
          })}
        </div>
      )}

      <section className="card-panel p-5">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Content templates</h2>
        {templates.length === 0 ? (
          <div className="mt-4 space-y-2 text-sm text-[#F5E8D2]/65">
            <p>No content templates stored yet.</p>
            <p className="text-[#5A6E82]">
              This section lists saved caption / CTA templates when they exist. Nothing is missing
              from the product — add templates later if you want reusable copy blocks.
            </p>
          </div>
        ) : (
          <div className="mt-4 space-y-3">
            {templates.map((t) => (
              <div key={t.id} className="rounded-xl bg-white/3 p-3">
                <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                  {t.key} {t.platform ? `· ${t.platform}` : ""}
                </div>
                <pre className="mt-2 whitespace-pre-wrap text-sm text-[#F5E8D2]/7">{t.body}</pre>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
