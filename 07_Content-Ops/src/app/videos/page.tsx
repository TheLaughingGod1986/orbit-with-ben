import Link from "next/link";
import { formatInTimeZone } from "date-fns-tz";
import { prisma } from "@/lib/storage/prisma";
import { PUBLISHING_SCHEDULE } from "@/config/publishing-schedule";
import { AddKnownThursdayFilmsButton } from "@/components/AddKnownThursdayFilmsButton";
import { AddThursdayFilmButton } from "@/components/AddThursdayFilmButton";
import { CopyFilmCaptionButton } from "@/components/CopyFilmCaptionButton";
import { CopyYoutubeIdButton } from "@/components/CopyYoutubeIdButton";
import {
  auditorFilmStatusLine,
  excludeFromNextThursdayHero,
  namedInFilmBookLine,
  resolveYoutubeId,
} from "@/app/videos/film-labels";

export const dynamic = "force-dynamic";

type FilmRow = {
  id: string;
  title: string;
  workingTitle: string | null;
  slug: string;
  status: string;
  summary: string | null;
  youtubeUrl: string | null;
  youtubeVideoId: string | null;
  thumbnailPath: string | null;
  finalVideoPath: string | null;
  projectFolder: string | null;
  publicationDate: Date | null;
  _count: { clips: number };
};

function formatThursdayDate(date: Date): string {
  return formatInTimeZone(date, PUBLISHING_SCHEDULE.timezone, "EEE d MMM HH:mm");
}

/** Prefer next upcoming Thursday; else the latest dated film. Skip private cuts (e.g. last-star v09). */
function pickThisThursdayFilm(videos: FilmRow[]): FilmRow | null {
  if (!videos.length) return null;
  const eligible = videos.filter((v) => !excludeFromNextThursdayHero(v));
  if (!eligible.length) return null;
  const now = Date.now();
  const dated = eligible.filter((v) => v.publicationDate);
  const upcoming = dated
    .filter((v) => v.publicationDate!.getTime() >= now)
    .sort((a, b) => a.publicationDate!.getTime() - b.publicationDate!.getTime());
  if (upcoming[0]) return upcoming[0];
  const latest = [...dated].sort(
    (a, b) => b.publicationDate!.getTime() - a.publicationDate!.getTime(),
  );
  return latest[0] ?? eligible[0];
}

function filmTitle(video: FilmRow): string {
  return video.workingTitle || video.title;
}

function wonderOneLiner(video: FilmRow): string {
  const fromSummary = video.summary?.trim().split(/\n/)[0]?.trim();
  if (fromSummary) return fromSummary.slice(0, 220);
  return filmTitle(video);
}

/** Only render stored thumbs that are already web-addressable — no new image pipeline. */
function publicThumbSrc(thumbnailPath: string | null): string | null {
  if (!thumbnailPath) return null;
  if (/^https?:\/\//i.test(thumbnailPath)) return thumbnailPath;
  if (thumbnailPath.startsWith("/")) return thumbnailPath;
  return null;
}

export default async function VideosPage() {
  const videos = await prisma.longFormVideo.findMany({
    orderBy: { publicationDate: "desc" },
    include: { _count: { select: { clips: true } } },
  });

  const thisFilm = pickThisThursdayFilm(videos);
  const catalogue = thisFilm ? videos.filter((v) => v.id !== thisFilm.id) : videos;
  const thisIsUpcoming =
    thisFilm?.publicationDate != null && thisFilm.publicationDate.getTime() >= Date.now();
  const thisNamed = thisFilm ? namedInFilmBookLine(thisFilm) : null;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
            Thursday films
          </h1>
          <p className="mt-2 max-w-xl text-[#F5E8D2]/60">
            Next Thursday film, whether the cut is ready, the listing is written, and it is
            scheduled.
          </p>
        </div>
        {videos.length > 0 ? (
          <div className="flex flex-col items-stretch gap-2 sm:items-end">
            <AddKnownThursdayFilmsButton primary={false} />
            <AddThursdayFilmButton primary={false} />
          </div>
        ) : null}
      </div>

      {videos.length === 0 ? (
        <div className="card-panel space-y-5 p-6 sm:p-8">
          <div>
            <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
              No Thursday film here yet.
            </h2>
            <p className="mt-3 max-w-xl text-[#F5E8D2]/65">
              Load the six known Thursday films (three published, three scheduled), or add the next
              one by title and date.
            </p>
          </div>
          <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-start">
            <AddKnownThursdayFilmsButton />
            <AddThursdayFilmButton primary={false} />
          </div>
        </div>
      ) : (
        <>
          {thisFilm ? (
            <section className="card-panel overflow-hidden">
              <div className="p-4 sm:p-5">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-full bg-[#FF7A24]/15 px-3 py-1 text-xs uppercase tracking-[0.16em] text-[#FF7A24]">
                    {thisIsUpcoming ? "Next Thursday" : "This film"}
                  </span>
                  <span className="rounded-full border border-white/10 px-2.5 py-1 text-xs uppercase tracking-[0.14em] text-[#F5E8D2]/75">
                    Long
                  </span>
                  {thisFilm._count.clips > 0 ? (
                    <span className="rounded-full border border-white/10 px-2.5 py-1 text-xs uppercase tracking-[0.14em] text-[#F5E8D2]/70">
                      Short
                    </span>
                  ) : null}
                </div>

                <Link href={`/videos/${thisFilm.id}`} className="mt-4 flex gap-4">
                  {publicThumbSrc(thisFilm.thumbnailPath) ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={publicThumbSrc(thisFilm.thumbnailPath)!}
                      alt=""
                      className="h-20 w-20 shrink-0 rounded-xl object-cover sm:h-24 sm:w-24"
                    />
                  ) : null}
                  <div className="min-w-0 flex-1">
                    <h2 className="break-words font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
                      {filmTitle(thisFilm)}
                    </h2>
                    <p className="mt-2 text-sm text-[#F5E8D2]/60">
                      {thisFilm.publicationDate
                        ? formatThursdayDate(thisFilm.publicationDate)
                        : "No Thursday date"}
                      <span className="text-[#5A6E82]"> · Europe/London</span>
                    </p>
                    <p className="mt-2 text-sm text-[#FF7A24]">
                      {auditorFilmStatusLine(thisFilm)}
                    </p>
                    {thisNamed ? (
                      <p className="mt-1 text-sm text-[#F5E8D2]/70">{thisNamed}</p>
                    ) : null}
                  </div>
                </Link>

                {/* Watch / YouTube id only — /videos never hosts shop or /go/ URLs */}
                <div className="mt-4 space-y-2">
                  {thisFilm.youtubeUrl ? (
                    <a
                      href={thisFilm.youtubeUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block break-all text-sm text-[#FFC85A] hover:underline"
                    >
                      {thisFilm.youtubeUrl}
                    </a>
                  ) : null}
                  {resolveYoutubeId(thisFilm) ? (
                    <CopyYoutubeIdButton youtubeId={resolveYoutubeId(thisFilm)!} />
                  ) : null}
                </div>
              </div>
              {thisFilm.youtubeUrl ? (
                <div className="border-t border-white/5 px-4 py-3 sm:px-5">
                  <CopyFilmCaptionButton
                    oneLiner={wonderOneLiner(thisFilm)}
                    youtubeUrl={thisFilm.youtubeUrl}
                  />
                </div>
              ) : null}
            </section>
          ) : null}

          {catalogue.length > 0 ? (
            <div className="space-y-3">
              <h2 className="text-xs uppercase tracking-[0.18em] text-[#5A6E82]">Catalogue</h2>
              <ul className="divide-y divide-white/5 overflow-hidden rounded-2xl border border-white/10">
                {catalogue.map((video) => {
                  const status = auditorFilmStatusLine(video);
                  const title = filmTitle(video);
                  const ytId = resolveYoutubeId(video);
                  const named = namedInFilmBookLine(video);
                  return (
                    <li key={video.id} className="px-4 py-3.5 sm:px-5">
                      <Link
                        href={`/videos/${video.id}`}
                        className="flex min-h-11 flex-col gap-1 transition hover:opacity-90"
                      >
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="truncate text-base text-[#F5E8D2]">{title}</span>
                          <span className="shrink-0 rounded-full border border-white/10 px-2 py-0.5 text-[0.65rem] uppercase tracking-[0.14em] text-[#F5E8D2]/65">
                            Long
                          </span>
                          {video._count.clips > 0 ? (
                            <span className="shrink-0 rounded-full border border-white/10 px-2 py-0.5 text-[0.65rem] uppercase tracking-[0.14em] text-[#F5E8D2]/65">
                              Short
                            </span>
                          ) : null}
                        </div>
                        <div className="text-sm text-[#F5E8D2]/55">
                          {video.publicationDate
                            ? formatThursdayDate(video.publicationDate)
                            : "No Thursday date"}
                          <span className="mx-1.5 text-[#5A6E82]">·</span>
                          <span className="text-[#FF7A24]">{status}</span>
                        </div>
                        {named ? (
                          <div className="text-sm text-[#F5E8D2]/70">{named}</div>
                        ) : null}
                      </Link>
                      {ytId || video.youtubeUrl ? (
                        <div className="mt-2 flex flex-wrap items-center gap-2">
                          {video.youtubeUrl ? (
                            <a
                              href={video.youtubeUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="break-all text-xs text-[#FFC85A] hover:underline"
                            >
                              Watch
                            </a>
                          ) : null}
                          {ytId ? <CopyYoutubeIdButton youtubeId={ytId} /> : null}
                        </div>
                      ) : null}
                    </li>
                  );
                })}
              </ul>
            </div>
          ) : null}
        </>
      )}
    </div>
  );
}
