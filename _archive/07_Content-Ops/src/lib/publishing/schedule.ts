import { addMinutes, parseISO } from "date-fns";
import { fromZonedTime, toZonedTime, formatInTimeZone } from "date-fns-tz";
import { PUBLISHING_SCHEDULE } from "@/config/publishing-schedule";
import { PlatformId, VIDEO_PLATFORMS, TEXT_PLATFORMS } from "@/config/platforms";

export function londonDateTime(isoDate: string, timeHhMm: string): Date {
  const [y, m, d] = isoDate.split("-").map(Number);
  const [hh, mm] = timeHhMm.split(":").map(Number);
  const local = new Date(y, m - 1, d, hh, mm, 0);
  return fromZonedTime(local, PUBLISHING_SCHEDULE.timezone);
}

export function formatLondon(date: Date): string {
  return formatInTimeZone(date, PUBLISHING_SCHEDULE.timezone, "yyyy-MM-dd HH:mm zzz");
}

export function scheduleClipAcrossPlatforms(input: {
  youtubeShortAt: Date;
  includeTextPlatforms?: boolean;
}): { platform: PlatformId; scheduledAt: Date }[] {
  const platforms: PlatformId[] = [
    ...VIDEO_PLATFORMS,
    ...(input.includeTextPlatforms === false ? [] : TEXT_PLATFORMS),
  ];
  return platforms.map((platform) => ({
    platform,
    scheduledAt: addMinutes(
      input.youtubeShortAt,
      PUBLISHING_SCHEDULE.crossPlatformOffsetsMinutes[platform],
    ),
  }));
}

export function suggestShortSlot(input: {
  longFormPublicationDate: Date;
  clipIndexZeroBased: number;
}): Date {
  const zoned = toZonedTime(input.longFormPublicationDate, PUBLISHING_SCHEDULE.timezone);
  const base = new Date(zoned);
  if (input.clipIndexZeroBased === 0) {
    base.setHours(21, 0, 0, 0);
    return fromZonedTime(base, PUBLISHING_SCHEDULE.timezone);
  }
  base.setDate(base.getDate() + input.clipIndexZeroBased);
  base.setHours(12, 30, 0, 0);
  return fromZonedTime(base, PUBLISHING_SCHEDULE.timezone);
}

export function isValidScheduleDate(value: string): boolean {
  try {
    const d = parseISO(value);
    return !Number.isNaN(d.getTime());
  } catch {
    return false;
  }
}
