import Link from "next/link";
import { notFound } from "next/navigation";
import { formatInTimeZone } from "date-fns-tz";
import { prisma } from "@/lib/storage/prisma";
import { PUBLISHING_SCHEDULE } from "@/config/publishing-schedule";
import { PLATFORMS } from "@/config/platforms";
import { DistributionPackButton } from "@/components/DistributionPackButton";
import { ClipActions } from "@/components/ClipActions";
import { CopyFilmCaptionButton } from "@/components/CopyFilmCaptionButton";
import { CopyYoutubeIdButton } from "@/components/CopyYoutubeIdButton";
import { auditorFilmStatusLine, namedInFilmBookLine, resolveYoutubeId } from "@/app/videos/film-labels";

export const dynamic = "force-dynamic";

function publicThumbSrc(thumbnailPath: string | null): string | null {
  if (!thumbnailPath) return null;
  if (/^https?:\/\//i.test(thumbnailPath)) return thumbnailPath;
  if (thumbnailPath.startsWith("/")) return thumbnailPath;
  return null;
}

function wonderOneLiner(video: {
  summary: string | null;
  workingTitle: string | null;
  title: string;
}): string {
  const fromSummary = video.summary?.trim().split(/\n/)[0]?.trim();
  if (fromSummary) return fromSummary.slice(0, 220);
  return video.workingTitle || video.title;
}

export default async function VideoDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const video = await prisma.longFormVideo.findUnique({
    where: { id },
    include: {
      clips: {
        orderBy: { sortOrder: "asc" },
        include: { posts: true },
      },
    },
  });
  if (!video) notFound();

  const thumb = publicThumbSrc(video.thumbnailPath);
  const ytId = resolveYoutubeId(video);
  const statusLine = auditorFilmStatusLine(video);
  const namedLine = namedInFilmBookLine(video);

  return (
    <div className="space-y-8 overflow-x-hidden">
      <div className="min-w-0">
        <Link
          href="/videos"
          className="inline-flex min-h-11 items-center text-sm text-[#5A6E82] hover:text-[#F5E8D2]"
        >
          ← Thursday films
        </Link>
        <div className="mt-3 flex gap-4">
          {thumb ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={thumb}
              alt=""
              className="h-20 w-20 shrink-0 rounded-xl object-cover sm:h-24 sm:w-24"
            />
          ) : null}
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-full border border-white/10 px-2.5 py-1 text-xs uppercase tracking-[0.14em] text-[#F5E8D2]/75">
                Long
              </span>
              {video.clips.length > 0 ? (
                <span className="rounded-full border border-white/10 px-2.5 py-1 text-xs uppercase tracking-[0.14em] text-[#F5E8D2]/70">
                  Short
                </span>
              ) : null}
            </div>
            <h1 className="mt-2 break-words font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2] sm:text-3xl">
              {video.workingTitle || video.title}
            </h1>
            {video.workingTitle ? (
              <p className="mt-2 break-words text-[#F5E8D2]/55">{video.title}</p>
            ) : null}
            <p className="mt-3 text-sm text-[#FF7A24]">{statusLine}</p>
            {namedLine ? <p className="mt-1 text-sm text-[#F5E8D2]/70">{namedLine}</p> : null}
            <p className="mt-1 text-sm text-[#F5E8D2]/55">
              {video.publicationDate
                ? formatInTimeZone(
                    video.publicationDate,
                    PUBLISHING_SCHEDULE.timezone,
                    "EEE d MMM HH:mm",
                  )
                : "No Thursday date"}
              <span className="text-[#5A6E82]"> · Europe/London</span>
            </p>
          </div>
        </div>

        {/* Watch / id only — /videos never hosts shop or /go/ URLs */}
        <div className="mt-4 space-y-2">
          {video.youtubeUrl ? (
            <a
              href={video.youtubeUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="block break-all text-sm text-[#FFC85A] hover:underline"
            >
              {video.youtubeUrl}
            </a>
          ) : null}
          {ytId ? <CopyYoutubeIdButton youtubeId={ytId} /> : null}
          {video.youtubeUrl ? (
            <div className="pt-1">
              <CopyFilmCaptionButton
                oneLiner={wonderOneLiner(video)}
                youtubeUrl={video.youtubeUrl}
              />
            </div>
          ) : null}
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="card-panel p-4 sm:p-5 lg:col-span-2">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Script</h2>
          <pre className="mt-4 max-h-80 overflow-auto whitespace-pre-wrap break-words text-sm text-[#F5E8D2]/70">
            {(video.script || "").slice(0, 4000)}
            {(video.script || "").length > 4000 ? "\n…" : ""}
          </pre>
        </div>
        <div className="card-panel space-y-3 p-4 text-sm text-[#F5E8D2]/70 sm:p-5">
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">YouTube</div>
            <div className="mt-1 break-all">{video.youtubeUrl || "—"}</div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">Project folder</div>
            <div className="mt-1 break-all">{video.projectFolder || "—"}</div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">Primary keyword</div>
            <div className="mt-1 break-words">{video.primaryKeyword || "—"}</div>
          </div>
        </div>
      </div>

      <section className="space-y-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl">
            Companion Short
          </h2>
          <div className="[&_button]:min-h-11 [&_button]:rounded-full [&_button]:border [&_button]:border-white/15 [&_button]:bg-transparent [&_button]:px-4 [&_button]:py-2 [&_button]:text-sm [&_button]:font-normal [&_button]:text-[#F5E8D2]/80">
            <DistributionPackButton videoId={video.id} />
          </div>
        </div>
        {video.clips.length === 0 ? (
          <div className="card-panel p-5 text-sm text-[#F5E8D2]/65">
            No companion Short yet. When the cut is ready, propose a Short from this film.
          </div>
        ) : null}
        {video.clips.map((clip) => {
          const platformsPosted = new Set(clip.posts.map((p) => p.platform));
          const missing = Object.keys(PLATFORMS).filter((p) => !platformsPosted.has(p));
          return (
            <div key={clip.id} className="card-panel p-4 sm:p-5">
              <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-start sm:justify-between">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-full border border-white/10 px-2.5 py-1 text-xs uppercase tracking-[0.14em] text-[#F5E8D2]/75">
                      Short
                    </span>
                    <span className="text-xs uppercase tracking-[0.16em] text-[#FF7A24]">
                      #{clip.clipNumber} · {clip.status} · Film-only · No affiliate
                    </span>
                  </div>
                  <h3 className="mt-2 break-words text-xl text-[#F5E8D2]">{clip.workingTitle}</h3>
                  <p className="mt-1 break-words text-sm text-[#F5E8D2]/65">{clip.hook}</p>
                  <p className="mt-2 text-xs text-[#5A6E82]">
                    {clip.sourceStartTime} → {clip.sourceEndTime} · {clip.targetDurationSeconds}s ·{" "}
                    {clip.hookCategory}
                  </p>
                </div>
                <div className="[&_button]:inline-flex [&_button]:min-h-11 [&_button]:items-center [&_button]:px-4 [&_button]:py-2 [&_button]:text-sm">
                  <ClipActions clipId={clip.id} status={clip.status} />
                </div>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <div className="rounded-xl bg-white/3 p-3 text-sm text-[#F5E8D2]/70">
                  <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Transcript</div>
                  <p className="mt-2 break-words">{clip.transcript}</p>
                </div>
                <div className="rounded-xl bg-white/3 p-3 text-sm text-[#F5E8D2]/70">
                  <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                    Platform coverage
                  </div>
                  <p className="mt-2 break-words">
                    Tracked: {Array.from(platformsPosted).join(", ") || "none"}
                  </p>
                  <p className="mt-1 break-words text-[#FFC85A]/80">
                    Missing: {missing.join(", ") || "none"}
                  </p>
                  <Link
                    href={`/clips/${clip.id}`}
                    className="mt-3 inline-flex min-h-11 items-center text-[#FF7A24] hover:underline"
                  >
                    Open clip workspace →
                  </Link>
                </div>
              </div>
            </div>
          );
        })}
      </section>
    </div>
  );
}
