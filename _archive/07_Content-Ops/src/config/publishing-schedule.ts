import { PlatformId } from "./platforms";

/**
 * Canonical Orbit schedule (Europe/London).
 * Preserves existing channel ops from OPTIMAL_PUBLISH_SCHEDULE.json
 * and adds staggered cross-platform offsets within a 24h window.
 */
export const PUBLISHING_SCHEDULE = {
  timezone: "Europe/London",
  channelName: "Orbit with Ben",
  longForm: {
    day: "Thursday" as const,
    time: "19:00",
    window: "18:00-20:00",
  },
  youtubeShorts: {
    day1: { offsetDays: 0, time: "21:00" },
    subsequent: { time: "12:30" },
    pattern: "Day1 @21:00 then Days2-7 @12:30",
  },
  /**
   * Same core clip across platforms within 24h, staggered minutes.
   * Applied relative to the YouTube Short slot for that clip.
   */
  crossPlatformOffsetsMinutes: {
    youtube_shorts: 0,
    tiktok: 30,
    instagram_reels: 60,
    instagram_feed: 75,
    facebook_reels: 90,
    facebook_page: 105,
    x: 120,
    threads: 150,
  } as Record<PlatformId, number>,
  cadenceMonthlyTargets: {
    longForm: 4,
    shortClips: 16,
    youtubeShorts: 16,
    tiktok: 16,
    instagramReels: 16,
    facebookReels: 16,
    facebookPage: 8,
    instagramFeed: 8,
    x: { min: 12, max: 20 },
    threads: { min: 8, max: 16 },
  },
  rules: {
    neverShortBeforeLongPublic: true,
    neverDumpClusterDay1: true,
    softCtaOnly: true,
  },
} as const;

export type PublishingSchedule = typeof PUBLISHING_SCHEDULE;
