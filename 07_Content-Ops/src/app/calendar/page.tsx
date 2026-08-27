import { prisma } from "@/lib/storage/prisma";
import { PLATFORMS } from "@/config/platforms";
import {
  addDays,
  eachDayOfInterval,
  endOfMonth,
  endOfWeek,
  format,
  startOfMonth,
  startOfWeek,
} from "date-fns";
import { toZonedTime } from "date-fns-tz";
import { PUBLISHING_SCHEDULE } from "@/config/publishing-schedule";
import Link from "next/link";
import { PostStatusForm } from "@/components/PostStatusForm";

export const dynamic = "force-dynamic";

export default async function CalendarPage({
  searchParams,
}: {
  searchParams: Promise<{ month?: string; view?: string }>;
}) {
  const sp = await searchParams;
  const base = sp.month ? new Date(`${sp.month}-01T12:00:00`) : new Date();
  const monthStart = startOfMonth(base);
  const monthEnd = endOfMonth(base);
  const gridStart = startOfWeek(monthStart, { weekStartsOn: 1 });
  const gridEnd = endOfWeek(monthEnd, { weekStartsOn: 1 });
  const days = eachDayOfInterval({ start: gridStart, end: gridEnd });

  const [posts, longs, filmCount] = await Promise.all([
    prisma.platformPost.findMany({
      where: {
        OR: [
          { scheduledAt: { gte: gridStart, lte: addDays(gridEnd, 1) } },
          { publishedAt: { gte: gridStart, lte: addDays(gridEnd, 1) } },
        ],
      },
      include: {
        shortClip: { include: { longFormVideo: true } },
      },
      orderBy: { scheduledAt: "asc" },
    }),
    prisma.longFormVideo.findMany({
      where: {
        publicationDate: { gte: gridStart, lte: addDays(gridEnd, 1) },
      },
    }),
    prisma.longFormVideo.count(),
  ]);

  const weekView = sp.view === "week";
  const visibleDays = weekView
    ? eachDayOfInterval({
        start: startOfWeek(new Date(), { weekStartsOn: 1 }),
        end: endOfWeek(new Date(), { weekStartsOn: 1 }),
      })
    : days;

  function dayKey(d: Date) {
    return format(toZonedTime(d, PUBLISHING_SCHEDULE.timezone), "yyyy-MM-dd");
  }

  const emptyStudio = filmCount === 0 && posts.length === 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl">
            Publishing calendar
          </h1>
          <p className="mt-2 text-[#F5E8D2]/60">
            Europe/London · edit times via each post form
          </p>
        </div>
        {!emptyStudio ? (
          <div className="flex gap-2 text-sm">
            <Link
              href={`/calendar?month=${format(monthStart, "yyyy-MM")}`}
              className="rounded-full border border-white/10 px-3 py-1.5"
            >
              Month
            </Link>
            <Link href="/calendar?view=week" className="rounded-full border border-white/10 px-3 py-1.5">
              Week
            </Link>
          </div>
        ) : null}
      </div>

      {emptyStudio ? (
        <div className="card-panel space-y-4 p-6 sm:p-8">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
            Nothing on the calendar yet.
          </h2>
          <p className="max-w-xl text-[#F5E8D2]/65">
            Add the known Thursday films (or the next Thursday film) first. Scheduled longs and
            Shorts posts show up here after that.
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
          <div className="grid grid-cols-7 gap-2 text-center text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
            {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((d) => (
              <div key={d}>{d}</div>
            ))}
          </div>

          <div className="grid grid-cols-7 gap-2">
            {visibleDays.map((day) => {
              const key = format(day, "yyyy-MM-dd");
              const dayPosts = posts.filter((p) => {
                const when = p.scheduledAt || p.publishedAt;
                return when ? dayKey(when) === key : false;
              });
              const dayLongs = longs.filter(
                (v) => v.publicationDate && dayKey(v.publicationDate) === key,
              );
              return (
                <div key={key} className="card-panel min-h-28 p-2">
                  <div className="text-xs text-[#5A6E82]">{format(day, "d")}</div>
                  <div className="mt-2 space-y-1">
                    {dayLongs.map((v) => (
                      <Link
                        key={v.id}
                        href={`/videos/${v.id}`}
                        className="block rounded-md bg-[#FF7A24]/20 px-1.5 py-1 text-[10px] text-[#FFC85A]"
                      >
                        LONG · {v.workingTitle || v.title}
                      </Link>
                    ))}
                    {dayPosts.map((p) => (
                      <Link
                        key={p.id}
                        href={`/clips/${p.shortClipId}`}
                        className="block rounded-md px-1.5 py-1 text-[10px]"
                        style={{
                          background: `${PLATFORMS[p.platform as keyof typeof PLATFORMS]?.color || "#888"}22`,
                          color: PLATFORMS[p.platform as keyof typeof PLATFORMS]?.color || "#ccc",
                        }}
                        title={p.title || p.caption || ""}
                      >
                        {PLATFORMS[p.platform as keyof typeof PLATFORMS]?.shortLabel} ·{" "}
                        {p.shortClip.workingTitle}
                      </Link>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          <section className="space-y-3">
            {posts.length === 0 ? (
              <div className="card-panel space-y-3 p-5 sm:p-6">
                <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
                  No platform posts yet
                </h2>
                <p className="max-w-xl text-sm text-[#F5E8D2]/65">
                  Shorts posts appear here after clips are scheduled. Undated published films stay
                  on the films list — they have no calendar day to place.
                </p>
                <Link
                  href="/videos"
                  className="inline-flex min-h-11 items-center justify-center rounded-full border border-white/10 px-5 py-2.5 text-sm text-[#F5E8D2]"
                >
                  Manage Thursday films
                </Link>
              </div>
            ) : (
              <>
                <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">
                  Upcoming posts — edit schedule
                </h2>
                {posts.slice(0, 12).map((p) => (
                  <div
                    key={p.id}
                    className="card-panel flex flex-wrap items-start justify-between gap-4 p-4"
                  >
                    <div>
                      <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                        {PLATFORMS[p.platform as keyof typeof PLATFORMS]?.label} · {p.uploadStatus}
                      </div>
                      <div className="mt-1 text-sm">{p.shortClip.workingTitle}</div>
                      <div className="mt-1 text-xs text-[#F5E8D2]/50">
                        {p.title || p.caption?.slice(0, 80)}
                      </div>
                    </div>
                    <PostStatusForm postId={p.id} status={p.uploadStatus} url={p.platformUrl} />
                  </div>
                ))}
              </>
            )}
          </section>
        </>
      )}
    </div>
  );
}
