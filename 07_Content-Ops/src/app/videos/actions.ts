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
