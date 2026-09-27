import Link from "next/link";
import { notFound } from "next/navigation";
import { prisma } from "@/lib/storage/prisma";
import { formatLondon } from "@/lib/publishing/schedule";

export const dynamic = "force-dynamic";

export default async function PublishingJobPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const job = await prisma.publishingJob.findUnique({
    where: { id },
    include: {
      attempts: { orderBy: { attemptNumber: "desc" } },
      platformPost: { include: { shortClip: true } },
      platformConnection: true,
    },
  });
  if (!job) notFound();

  return (
    <div className="space-y-6">
      <div>
        <Link href="/calendar" className="text-sm text-[#5A6E82]">
          ← Calendar
        </Link>
        <h1 className="mt-3 font-[family-name:var(--font-orbit-display)] text-3xl">
          Publishing job
        </h1>
        <p className="mt-2 font-mono text-xs text-[#5A6E82]">{job.id}</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="card-panel space-y-2 p-5 text-sm">
          <div>Status: {job.status}</div>
          <div>Platform: {job.platformPost.platform}</div>
          <div>Clip: {job.platformPost.shortClip.workingTitle}</div>
          <div>Account: {job.platformConnection?.accountName || "—"}</div>
          <div>Scheduled: {job.scheduledAt ? formatLondon(job.scheduledAt) : "—"}</div>
          <div>Attempts: {job.attemptCount}/{job.maxAttempts}</div>
          <div>External ID: {job.externalPostId || "—"}</div>
          <div>
            External URL:{" "}
            {job.externalPostUrl ? (
              <a className="text-[#FF7A24]" href={job.externalPostUrl} target="_blank" rel="noreferrer">
                {job.externalPostUrl}
              </a>
            ) : (
              "—"
            )}
          </div>
          <div>Last error: {job.lastErrorMessage || "—"}</div>
          <div>Retryable: {String(job.lastErrorRetryable)}</div>
          <div>Next attempt: {job.nextAttemptAt ? formatLondon(job.nextAttemptAt) : "—"}</div>
          <div>Dry-run: {String(job.dryRun)}</div>
        </div>
        <div className="card-panel p-5">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Attempts</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {job.attempts.map((a) => (
              <li key={a.id} className="rounded-lg bg-white/3 p-3">
                #{a.attemptNumber} · {a.status}
                {a.httpStatus ? ` · HTTP ${a.httpStatus}` : ""}
                {a.errorMessage ? ` · ${a.errorMessage}` : ""}
              </li>
            ))}
            {!job.attempts.length ? <li className="text-[#5A6E82]">No attempts yet</li> : null}
          </ul>
        </div>
      </div>
    </div>
  );
}
