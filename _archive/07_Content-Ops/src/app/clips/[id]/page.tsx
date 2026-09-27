import Link from "next/link";
import { notFound } from "next/navigation";
import { prisma } from "@/lib/storage/prisma";
import { PLATFORMS } from "@/config/platforms";
import { formatLondon } from "@/lib/publishing/schedule";
import { ClipWorkspaceActions } from "@/components/ClipWorkspaceActions";
import { PostStatusForm } from "@/components/PostStatusForm";

export const dynamic = "force-dynamic";

export default async function ClipPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const clip = await prisma.shortClip.findUnique({
    where: { id },
    include: {
      longFormVideo: true,
      posts: { orderBy: { scheduledAt: "asc" } },
    },
  });
  if (!clip) notFound();

  const breakdown = clip.qualityBreakdown
    ? (JSON.parse(clip.qualityBreakdown) as { reasons?: string[]; total?: number })
    : null;

  return (
    <div className="space-y-8">
      <div>
        <Link
          href={`/videos/${clip.longFormVideoId}`}
          className="text-sm text-[#5A6E82] hover:text-[#F5E8D2]"
        >
          ← {clip.longFormVideo.workingTitle || clip.longFormVideo.title}
        </Link>
        <h1 className="mt-3 font-[family-name:var(--font-orbit-display)] text-3xl">
          {clip.workingTitle}
        </h1>
        <p className="mt-2 text-[#F5E8D2]/65">{clip.hook}</p>
      </div>

      <ClipWorkspaceActions clipId={clip.id} status={clip.status} />

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="card-panel p-5 text-sm text-[#F5E8D2]/75">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
            Creative brief
          </h2>
          <dl className="mt-4 space-y-3">
            <div>
              <dt className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Timestamps</dt>
              <dd>
                {clip.sourceStartTime} → {clip.sourceEndTime} ({clip.targetDurationSeconds}s)
              </dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Visual</dt>
              <dd>{clip.visualDirection}</dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">On-screen text</dt>
              <dd>{clip.onScreenText}</dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Ending</dt>
              <dd>{clip.endingLine}</dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">CTA</dt>
              <dd>{clip.callToAction}</dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Quality</dt>
              <dd>
                {clip.qualityScore}/100
                {breakdown?.reasons?.length ? (
                  <ul className="mt-2 list-disc pl-5 text-[#F5E8D2]/55">
                    {breakdown.reasons.map((r) => (
                      <li key={r}>{r}</li>
                    ))}
                  </ul>
                ) : null}
              </dd>
            </div>
          </dl>
        </div>

        <div className="card-panel p-5">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Transcript</h2>
          <p className="mt-4 text-sm text-[#F5E8D2]/75">{clip.transcript}</p>
        </div>
      </div>

      <section className="space-y-4">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl">
          Platform posts
        </h2>
        {clip.posts.map((post) => (
          <div key={post.id} className="card-panel p-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <div
                  className="text-xs font-medium uppercase tracking-[0.16em]"
                  style={{ color: PLATFORMS[post.platform as keyof typeof PLATFORMS]?.color }}
                >
                  {PLATFORMS[post.platform as keyof typeof PLATFORMS]?.label || post.platform}
                </div>
                <div className="mt-1 text-sm text-[#F5E8D2]/70">
                  {post.uploadStatus}
                  {post.scheduledAt ? ` · ${formatLondon(post.scheduledAt)}` : ""}
                </div>
              </div>
              <PostStatusForm
                postId={post.id}
                status={post.uploadStatus}
                url={post.platformUrl}
                approvedForPublish={post.approvedForPublish}
                privacyStatus={post.privacyStatus}
                madeForKids={post.madeForKids}
                platform={post.platform}
              />
            </div>
            {post.title ? (
              <p className="mt-3 text-sm font-medium text-[#F5E8D2]">{post.title}</p>
            ) : null}
            <pre className="mt-2 whitespace-pre-wrap text-sm text-[#F5E8D2]/65">{post.caption}</pre>
          </div>
        ))}
      </section>
    </div>
  );
}
