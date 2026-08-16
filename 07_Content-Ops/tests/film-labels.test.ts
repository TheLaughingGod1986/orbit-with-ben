import { describe, expect, it } from "vitest";
import {
  auditorFilmStatusLine,
  excludeFromNextThursdayHero,
  namedInFilmBookLine,
  resolveYoutubeId,
} from "../src/app/videos/film-labels";

describe("film-labels (Auditor)", () => {
  it("names last-star v11 and Europa v02 only", () => {
    expect(
      namedInFilmBookLine({ youtubeVideoId: "REXYxuLOBoI", youtubeUrl: null }),
    ).toBe("Named: The End of Everything");
    expect("REXYxuLOBoI".includes("0")).toBe(false);
    expect(
      namedInFilmBookLine({ youtubeVideoId: "NbW5G1BpPY0", youtubeUrl: null }),
    ).toBe("Named: Alien Oceans");
    expect(
      namedInFilmBookLine({ youtubeVideoId: "z-fUtdjWn5o", youtubeUrl: null }),
    ).toBeNull();
    expect(
      namedInFilmBookLine({ youtubeVideoId: "dbBojuwg4r8", youtubeUrl: null }),
    ).toBeNull();
    expect(
      namedInFilmBookLine({ youtubeVideoId: "3_W_jl2GR8w", youtubeUrl: null }),
    ).toBeNull();
    expect(
      namedInFilmBookLine({ youtubeVideoId: "Mo93x0fxB1Q", youtubeUrl: null }),
    ).toBeNull();
  });

  it("excludes private cuts from next Thursday hero", () => {
    expect(
      excludeFromNextThursdayHero({ youtubeVideoId: "dbBojuwg4r8", youtubeUrl: null }),
    ).toBe(true);
    expect(
      excludeFromNextThursdayHero({ youtubeVideoId: "z-fUtdjWn5o", youtubeUrl: null }),
    ).toBe(true);
    expect(
      excludeFromNextThursdayHero({ youtubeVideoId: "3_W_jl2GR8w", youtubeUrl: null }),
    ).toBe(true);
    expect(
      excludeFromNextThursdayHero({ youtubeVideoId: "REXYxuLOBoI", youtubeUrl: null }),
    ).toBe(false);
    expect(
      excludeFromNextThursdayHero({ youtubeVideoId: "NbW5G1BpPY0", youtubeUrl: null }),
    ).toBe(false);
  });

  it("maps status honestly without inventing private/live", () => {
    expect(
      auditorFilmStatusLine({
        status: "published",
        youtubeVideoId: "Mo93x0fxB1Q",
        youtubeUrl: null,
      }),
    ).toBe("Long · Film-only · Published");
    expect(
      auditorFilmStatusLine({
        status: "scheduled",
        youtubeVideoId: "REXYxuLOBoI",
        youtubeUrl: null,
      }),
    ).toBe("Long · Film-only · Scheduled");
    expect(
      auditorFilmStatusLine({
        status: "ready",
        youtubeVideoId: "abc",
        youtubeUrl: null,
      }),
    ).toBe("Long · Film-only · Not published");
  });

  it("resolves youtube id from url when needed", () => {
    expect(
      resolveYoutubeId({
        youtubeVideoId: null,
        youtubeUrl: "https://youtu.be/NbW5G1BpPY0",
      }),
    ).toBe("NbW5G1BpPY0");
  });
});
