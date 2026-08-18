/**
 * The six known Thursday longs only. No private old cuts
 * (z-fUtdjWn5o, dbBojuwg4r8, 3_W_jl2GR8w). No Shorts / affiliate /go/.
 */

export type KnownThursdayFilm = {
  title: string;
  slug: string;
  topic: string;
  status: "published" | "scheduled";
  youtubeVideoId: string;
  youtubeUrl: string;
  /** London YYYY-MM-DD + 18:00. Omit when publish date is unverified. */
  publicationDateLondon?: { date: string; time: string };
};

export const KNOWN_THURSDAY_FILMS: readonly KnownThursdayFilm[] = [
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
    youtubeVideoId: "REXYxuLOBoI",
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

export const KNOWN_THURSDAY_YOUTUBE_IDS: readonly string[] = KNOWN_THURSDAY_FILMS.map(
  (f) => f.youtubeVideoId,
);
