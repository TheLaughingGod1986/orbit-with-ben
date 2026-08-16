"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { prisma } from "@/lib/storage/prisma";
import { londonDateTime } from "@/lib/publishing/schedule";

function slugify(input: string): string {
  const slug = input
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60);
  return slug || "thursday-film";
}

/** Add a Thursday film with title + air date using existing LongFormVideo fields only. */
export async function addThursdayFilm(formData: FormData): Promise<void> {
  const title = String(formData.get("title") || "").trim();
  const date = String(formData.get("date") || "").trim();
  const timeRaw = String(formData.get("time") || "18:00").trim();
  const time = /^\d{2}:\d{2}$/.test(timeRaw) ? timeRaw : "18:00";

  if (!title || !/^\d{4}-\d{2}-\d{2}$/.test(date)) {
    throw new Error("Title and Thursday date (YYYY-MM-DD) are required");
  }

  const baseSlug = `${date}-${slugify(title)}`;
  let slug = baseSlug;
  for (let n = 0; n < 20; n += 1) {
    const candidate = n === 0 ? baseSlug : `${baseSlug}-${n}`;
    const exists = await prisma.longFormVideo.findUnique({ where: { slug: candidate } });
    if (!exists) {
      slug = candidate;
      break;
    }
  }

  const video = await prisma.longFormVideo.create({
    data: {
      title,
      workingTitle: title,
      slug,
      topic: "Thursday film",
      status: "idea",
      publicationDate: londonDateTime(date, time),
    },
  });

  revalidatePath("/videos");
  redirect(`/videos/${video.id}`);
}

type KnownThursdayFilm = {
  title: string;
  slug: string;
  topic: string;
  status: "published" | "scheduled";
  youtubeVideoId: string;
  youtubeUrl: string;
  /** London YYYY-MM-DD + 18:00. Omit when publish date is unverified. */
  publicationDateLondon?: { date: string; time: string };
};

/**
 * The six known Thursday longs only. No private old cuts
 * (z-fUtdjWn5o, dbBojuwg4r8, 3_W_jl2GR8w). No Shorts / affiliate /go/.
 */
const KNOWN_THURSDAY_FILMS: KnownThursdayFilm[] = [
  {
    title: "Alien Worlds: The Strangest Planets We've Ever Found",
    slug: "alien-worlds-strangest-planets",
    topic: "exoplanets",
    status: "published",
    youtubeVideoId: "b8-X_FyJnHM",
    youtubeUrl: "https://www.youtube.com/watch?v=b8-X_FyJnHM",
  },
  {
    title: "What Happens If You Fall Into a Black Hole?",
    slug: "fall-into-a-black-hole",
    topic: "black holes",
    status: "published",
    youtubeVideoId: "3xrxdmaOwJI",
    youtubeUrl: "https://www.youtube.com/watch?v=3xrxdmaOwJI",
  },
  {
    title: "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained",
    slug: "fermi-paradox-explained",
    topic: "fermi",
    status: "published",
    youtubeVideoId: "Mo93x0fxB1Q",
    youtubeUrl: "https://www.youtube.com/watch?v=Mo93x0fxB1Q",
  },
  {
    title: "JWST Found Galaxies That Shouldn't Exist Yet",
    slug: "jwst-galaxies-that-shouldnt-exist",
    topic: "jwst",
    status: "scheduled",
    youtubeVideoId: "ziKBPJ6FY0U",
    youtubeUrl: "https://www.youtube.com/watch?v=ziKBPJ6FY0U",
    publicationDateLondon: { date: "2026-08-20", time: "18:00" },
  },
  {
    title: "What Happens When the Last Star Dies?",
    slug: "last-star-dies",
    topic: "last-star",
    status: "scheduled",
    youtubeVideoId: "REXYxuLOBoI", // letter O, not zero
    youtubeUrl: "https://www.youtube.com/watch?v=REXYxuLOBoI",
    publicationDateLondon: { date: "2026-08-27", time: "18:00" },
  },
  {
    title: "Could Life Exist Under The Ice Of Europa?",
    slug: "europa-under-the-ice",
    topic: "europa",
    status: "scheduled",
    youtubeVideoId: "NbW5G1BpPY0",
    youtubeUrl: "https://www.youtube.com/watch?v=NbW5G1BpPY0",
    publicationDateLondon: { date: "2026-09-03", time: "18:00" },
  },
];

async function uniqueSlug(base: string, excludeId?: string): Promise<string> {
  for (let n = 0; n < 20; n += 1) {
    const candidate = n === 0 ? base : `${base}-${n}`;
    const exists = await prisma.longFormVideo.findUnique({ where: { slug: candidate } });
    if (!exists || (excludeId && exists.id === excludeId)) return candidate;
  }
  return `${base}-${Date.now()}`;
}

export type AddKnownThursdayFilmsResult = {
  created: number;
  updated: number;
  total: number;
};

/**
 * Idempotent upsert of the six known Thursday films by youtubeVideoId.
 * Safe to run twice. LongFormVideo fields only — no clips, posts, or affiliate rows.
 */
export async function addKnownThursdayFilms(): Promise<AddKnownThursdayFilmsResult> {
  let created = 0;
  let updated = 0;

  for (const film of KNOWN_THURSDAY_FILMS) {
    const publicationDate = film.publicationDateLondon
      ? londonDateTime(film.publicationDateLondon.date, film.publicationDateLondon.time)
      : null;

    const existing = await prisma.longFormVideo.findFirst({
      where: { youtubeVideoId: film.youtubeVideoId },
    });

    if (existing) {
      await prisma.longFormVideo.update({
        where: { id: existing.id },
        data: {
          title: film.title,
          workingTitle: film.title,
          topic: film.topic,
          status: film.status,
          youtubeVideoId: film.youtubeVideoId,
          youtubeUrl: film.youtubeUrl,
          ...(publicationDate ? { publicationDate } : {}),
        },
      });
      updated += 1;
      continue;
    }

    const slug = await uniqueSlug(film.slug);
    await prisma.longFormVideo.create({
      data: {
        title: film.title,
        workingTitle: film.title,
        slug,
        topic: film.topic,
        status: film.status,
        youtubeVideoId: film.youtubeVideoId,
        youtubeUrl: film.youtubeUrl,
        publicationDate,
      },
    });
    created += 1;
  }

  revalidatePath("/videos");
  revalidatePath("/calendar");
  revalidatePath("/pipeline");

  return { created, updated, total: KNOWN_THURSDAY_FILMS.length };
}
