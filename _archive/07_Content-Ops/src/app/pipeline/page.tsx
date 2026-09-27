import { prisma } from "@/lib/storage/prisma";
import Link from "next/link";
import { CONTENT_RULES } from "@/config/content-rules";

export const dynamic = "force-dynamic";

export default async function PipelinePage({
  searchParams,
}: {
  searchParams: Promise<{ video?: string; platform?: string; status?: string; topic?: string }>;
}) {
  const sp = await searchParams;
  const videos = await prisma.longFormVideo.findMany({
    where: {
      ...(sp.video ? { id: sp.video } : {}),
      ...(sp.topic ? { topic: { contains: sp.topic } } : {}),
    },
    include: {
      clips: {
        where: sp.status ? { status: sp.status } : undefined,
        include: {
          posts: {
            where: sp.platform ? { platform: sp.platform } : undefined,
            include: { metrics: true },
          },
        },
        orderBy: { sortOrder: "asc" },
      },
    },
    orderBy: { updatedAt: "desc" },
  });

  const counts = {
    proposed: 0,
    approved: 0,
    editing: 0,
    exported: 0,
    scheduledPosts: 0,
    publishedPosts: 0,
    analysed: 0,
  };
  for (const v of videos) {
    for (const c of v.clips) {
      if (c.status === "proposed") counts.proposed++;
      if (c.status === "approved") counts.approved++;
      if (c.status === "editing") counts.editing++;
      if (c.status === "exported") counts.exported++;
      for (const p of c.posts) {
        if (p.uploadStatus === "scheduled") counts.scheduledPosts++;
        if (p.uploadStatus === "published") counts.publishedPosts++;
        if (p.metrics.length) counts.analysed++;
      }
    }
  }

  const empty = videos.length === 0 && !sp.video && !sp.topic && !sp.status && !sp.platform;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl">Content pipeline</h1>
        <p className="mt-2 text-[#F5E8D2]/60">
          Filter by long-form video, platform, status, or topic.
        </p>
      </div>

      {empty ? (
        <div className="card-panel space-y-4 p-6 sm:p-8">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
            Pipeline is empty.
          </h2>
          <p className="max-w-xl text-[#F5E8D2]/65">
            There are no Thursday films in Content Ops yet. Add the known films (or the next
            Thursday film), then Shorts and posts will show up in this pipeline.
          </p>
          <Link
            href="/videos"
            className="inline-flex min-h-11 items-center justify-center rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12]"
          >
            Go to Thursday films
          </Link>
        </div>
      ) : (
        <>
          <form className="card-panel grid gap-3 p-4 md:grid-cols-4">
            <input
              name="topic"
              defaultValue={sp.topic || ""}
              placeholder="Topic"
              className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2 text-sm"
            />
            <input
              name="status"
              defaultValue={sp.status || ""}
              placeholder="Clip status"
              className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2 text-sm"
            />
            <input
              name="platform"
              defaultValue={sp.platform || ""}
              placeholder="Platform id"
              className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2 text-sm"
            />
            <button className="rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12]">
              Filter
            </button>
          </form>

          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-[#F5E8D2]/65">
              Films in list:{" "}
              <span className="font-medium text-[#F5E8D2]">{videos.length}</span>
              <span className="text-[#5A6E82]"> · counters below are Shorts clips / posts</span>
            </p>
            <div className="flex flex-wrap gap-2">
              {CONTENT_RULES.pipelineStages.map((stage) => (
                <span key={stage} className="pipeline-step rounded-full px-3 py-1.5 text-xs">
                  {stage}
                </span>
              ))}
            </div>
          </div>

          <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
            {[
              ["Clips proposed", counts.proposed],
              ["Clips approved", counts.approved],
              ["Clips editing", counts.editing],
              ["Clips exported", counts.exported],
              ["Posts scheduled", counts.scheduledPosts],
              ["Posts analysed", counts.analysed],
            ].map(([label, value]) => (
              <div key={label as string} className="card-panel p-4">
                <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                  {label}
                </div>
                <div className="mt-2 text-2xl">{value as number}</div>
              </div>
            ))}
          </div>

          <div className="space-y-4">
            {videos.length === 0 ? (
              <div className="card-panel p-5 text-sm text-[#F5E8D2]/65">
                No films match these filters.{" "}
                <Link href="/pipeline" className="text-[#FF7A24] hover:underline">
                  Clear filters
                </Link>
              </div>
            ) : (
              videos.map((video) => (
                <div key={video.id} className="card-panel p-5">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <Link
                      href={`/videos/${video.id}`}
                      className="text-lg text-[#F5E8D2] hover:text-[#FF7A24]"
                    >
                      {video.workingTitle || video.title}
                    </Link>
                    <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                      {video.status} · {video.topic}
                    </span>
                  </div>
                  <div className="mt-4 space-y-2">
                    {video.clips.length === 0 ? (
                      <p className="text-sm text-[#F5E8D2]/50">No Shorts clips for this film yet.</p>
                    ) : (
                      video.clips.map((clip) => (
                        <Link
                          key={clip.id}
                          href={`/clips/${clip.id}`}
                          className="flex flex-wrap items-center justify-between gap-2 rounded-xl bg-white/3 px-3 py-2 text-sm hover:bg-white/5"
                        >
                          <span>
                            #{clip.clipNumber} {clip.workingTitle} · {clip.status}
                          </span>
                          <span className="text-[#5A6E82]">
                            {clip.posts.length} posts · missing analytics{" "}
                            {
                              clip.posts.filter(
                                (p) => p.uploadStatus === "published" && !p.metrics.length,
                              ).length
                            }
                          </span>
                        </Link>
                      ))
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}
