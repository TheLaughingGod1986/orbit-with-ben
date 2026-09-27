"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { prisma } from "@/lib/storage/prisma";
import { londonDateTime } from "@/lib/publishing/schedule";
import { requireOperator } from "@/lib/security/operator-auth";
import { KNOWN_THURSDAY_FILMS } from "@/app/videos/known-thursday-films";

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
  await requireOperator();
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
  await requireOperator();
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
