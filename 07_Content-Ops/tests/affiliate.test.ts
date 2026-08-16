import { describe, expect, it } from "vitest";
import {
  recommendProductsForVideo,
  scoreAffiliateRelevance,
  dedupeRecommendations,
  deterministicRelevanceStrategy,
  setRelevanceStrategy,
} from "../src/lib/affiliate/matching";
import {
  appendAffiliateSectionToDescription,
  buildAffiliateDescriptionSection,
  recommendationsToDescriptionLinks,
  affiliateBlockAppearsInFirstScreen,
  CREATOR_AFFILIATE_DISCLOSURE,
} from "../src/lib/affiliate/description";
import { productFamilyOf } from "../src/lib/affiliate/topic-product-map";
import {
  affiliateRpm,
  estimateCommission,
  earningsPerClick,
  conversionRate,
  totalContentRpm,
} from "../src/lib/affiliate/revenue";
import { scoreAffiliateOpportunity } from "../src/lib/affiliate/opportunity";
import {
  buildOrbitRedirectUrl,
  buildTrackedAffiliateUrl,
  applyProgrammeAffiliateId,
  resolveAffiliateRedirectBase,
} from "../src/lib/affiliate/urls";
import {
  previewAffiliateCsv,
  parseAffiliateCsv,
  rowsToConversions,
  AFFILIATE_CSV_DEFAULT_MAPPINGS,
} from "../src/lib/affiliate/csv-import";
import { shouldCheckUrl } from "../src/lib/affiliate/health";
import { mergeDescriptionWithAffiliateLinks } from "../src/lib/publishing/youtube-package";
import type { ProductMatchInput, VideoMatchInput } from "../src/lib/affiliate/types";
import {
  sanitizeAffiliateSocialText,
  containsRawMerchantUrl,
  containsBannedAffiliatePhrase,
  isAllowedSocialTrackedUrl,
  shouldIncludeAffiliateSoftMention,
  buildSoftAffiliateMentionLine,
} from "../src/lib/affiliate/social-copy-rules";
import {
  assertAffiliateSafeSocialCopy,
} from "../src/lib/affiliate/social-copy";
import { generatePlatformCopy } from "../src/lib/platforms/generate-platform-copy";
import {
  evaluateEditorialTrustGate,
  filterDescriptionLinksThroughTrustGate,
} from "../src/lib/affiliate/editorial-trust-gate";
import type { EditorialTrustProductInput } from "../src/lib/affiliate/editorial-trust-gate";
import { generateAffiliateSocialSnippets } from "../src/lib/affiliate/social-snippets";
import {
  FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM,
  FIXTURE_FACEBOOK_PAGE_HOWTO,
  FIXTURE_JWST_LIVE,
  FIXTURE_TELESCOPE_OBSERVING_HELD,
  countCaptionLines,
  firstNonEmptyLine,
  lastNonEmptyLine,
  renderFacebookPageTemplate,
  renderTelescopeCommentReply,
  renderThreadsTemplate,
  renderInstagramReelsTemplate,
  renderJwstLiveCaption,
  renderTelescopeObservingHeldCaption,
  isJwstThreadsPublishAllowed,
} from "../src/lib/affiliate/social-snippet-templates";
import { CREATOR_TOPIC_SLOT_PLANS, familyForbiddenForPlan } from "../src/lib/affiliate/topic-product-map";
import {
  facebookPageCaptionViolations,
  assertFacebookPageCaptionSafe,
} from "../src/lib/affiliate/facebook-page-rules";
import {
  buildSocialGoUrl,
  buildSocialYouTubeUrl,
} from "../src/lib/affiliate/urls";
import {
  normalizeAffiliateClickSource,
  socialPlatformToClickSource,
} from "../src/lib/affiliate/social-channels";
import {
  buildAffiliateGoalsSnapshot,
  computeMonthTargetGbp,
  resolveGoalsClockStart,
} from "../src/lib/affiliate/goals";
import {
  evaluateAffiliateGoLive,
  isPlaceholderAffiliateUrl,
} from "../src/lib/affiliate/go-live";
import {
  LIVE_PRODUCT_URLS,
  liveUrlForSlug,
  isAmazonUkDestinationUrl,
} from "../src/lib/affiliate/live-product-urls";
import {
  resolveTopicBookWireForVideo,
  filmTopicBookPlacementTableRows,
} from "../src/lib/affiliate/film-topic-book-map";

function product(partial: Partial<ProductMatchInput> & Pick<ProductMatchInput, "id" | "name" | "slug" | "category" | "tagSlugs">): ProductMatchInput {
  return {
    active: true,
    featured: false,
    priority: 0,
    evergreen: false,
    programStatus: "ACTIVE",
    ...partial,
  };
}

describe("affiliate matching", () => {
  const blackHoleVideo: VideoMatchInput = {
    title: "What Would Happen If You Fell Into a Black Hole?",
    topic: "Black Holes",
    primaryKeyword: "black hole",
    secondaryKeywords: ["event horizon", "spaghettification", "relativity"],
    summary: "A calm journey past the event horizon.",
    category: "Space Documentary",
  };

  const catalogue: ProductMatchInput[] = [
    product({
      id: "1",
      name: "Brilliant Physics",
      slug: "brilliant-physics",
      category: "Physics",
      tagSlugs: ["physics", "black-hole", "cosmology"],
      featured: true,
      priority: 8,
      estimatedCommission: 40,
      programSlug: "brilliant",
    }),
    product({
      id: "2",
      name: "Cosmology book",
      slug: "cosmology-book",
      category: "Astronomy books",
      tagSlugs: ["books", "cosmology", "black-hole"],
      estimatedCommission: 1,
    }),
    product({
      id: "3",
      name: "Beginner astronomy book",
      slug: "beginner-astronomy-book",
      category: "Astronomy books",
      tagSlugs: ["books", "beginner", "astronomy"],
      evergreen: true,
    }),
    product({
      id: "4",
      name: "Beginner telescope",
      slug: "beginner-telescope",
      category: "Beginner telescopes",
      tagSlugs: ["telescope", "beginner", "astronomy"],
      evergreen: true,
      featured: true,
    }),
    product({
      id: "5",
      name: "Random high-commission gadget",
      slug: "spam-gadget",
      category: "Kitchen",
      tagSlugs: ["unrelated"],
      estimatedCommission: 200,
      featured: true,
      priority: 99,
    }),
    product({
      id: "6",
      name: "Inactive leftover",
      slug: "inactive",
      category: "Physics",
      tagSlugs: ["physics", "black-hole"],
      active: false,
    }),
  ];

  it("scores black-hole episode toward book + Brilliant, not telescope or spam", () => {
    const set = recommendProductsForVideo(blackHoleVideo, catalogue);
    expect(set.all.length).toBeGreaterThan(0);
    expect(set.all.length).toBeLessThanOrEqual(4);
    const slugs = set.all.map((r) => r.product.slug);
    expect(slugs).toContain("cosmology-book");
    expect(slugs).toContain("brilliant-physics");
    expect(slugs).not.toContain("beginner-telescope");
    expect(slugs).not.toContain("spam-gadget");
    expect(slugs).not.toContain("inactive");
    expect(set.primary?.product.slug).toBe("cosmology-book");
    expect(productFamilyOf(set.primary!.product)).toBe("books");
  });

  it("kids film never uses Brilliant as primary", () => {
    const kidsVideo: VideoMatchInput = {
      title: "Kids Astronomy: Meet the Moon",
      topic: "Kids astronomy",
      primaryKeyword: "kids moon",
      summary: "A gentle first look at the Moon for children.",
      category: "Kids",
    };
    const kidsCatalogue = [
      ...catalogue,
      product({
        id: "7",
        name: "Space LEGO Hubble",
        slug: "space-lego-hubble",
        category: "Space LEGO",
        tagSlugs: ["lego", "kids", "telescope"],
        featured: true,
        priority: 5,
      }),
      product({
        id: "8",
        name: "Kids space book",
        slug: "kids-space-book",
        category: "Astronomy books",
        tagSlugs: ["books", "kids", "astronomy"],
      }),
    ];
    const set = recommendProductsForVideo(kidsVideo, kidsCatalogue);
    expect(set.primary).toBeTruthy();
    expect(productFamilyOf(set.primary!.product)).not.toBe("brilliant");
    expect(set.primary?.product.slug).not.toBe("brilliant-physics");
  });

  it("excludes inactive products from relevance", () => {
    const inactive = catalogue.find((p) => p.slug === "inactive")!;
    const { score } = scoreAffiliateRelevance(blackHoleVideo, inactive);
    expect(score).toBe(0);
  });

  it("supports interchangeable relevance strategy", () => {
    setRelevanceStrategy({
      scoreAffiliateRelevance: () => ({ score: 99, reasons: ["llm stub"] }),
    });
    const { score, reasons } = scoreAffiliateRelevance(blackHoleVideo, catalogue[0]);
    expect(score).toBe(99);
    expect(reasons[0]).toBe("llm stub");
    setRelevanceStrategy(deterministicRelevanceStrategy);
  });
});

describe("affiliate description generation", () => {
  const links = [
    {
      productName: "Beginner telescope",
      productSlug: "beginner-telescope",
      category: "Beginner telescopes",
      programSlug: "astronomy-retailer",
      url: "https://example.invalid/aff/beginner-telescope",
    },
    {
      productName: "Brilliant Physics",
      productSlug: "brilliant-physics",
      category: "Physics",
      programSlug: "brilliant",
      url: "https://example.invalid/aff/brilliant-physics",
    },
  ];

  it("builds Creator-voice section with disclosure as last line", () => {
    const section = buildAffiliateDescriptionSection({
      links,
      topicKey: "telescopes",
    });
    expect(section).toContain("If you want to go further");
    expect(section).toContain("beginner-telescope");
    expect(section.toLowerCase()).not.toContain("buy now");
    expect(section.toLowerCase()).not.toContain("must-have");
    expect(section.trim().endsWith(CREATOR_AFFILIATE_DISCLOSURE)).toBe(true);
    expect(section.indexOf("If you want to go further")).toBeLessThan(
      section.indexOf(CREATOR_AFFILIATE_DISCLOSURE),
    );
  });

  it("places block after subscribe, before playlist; disclosure last; not first screen", () => {
    const withDupes = [...links, links[0]];
    const base = [
      "What happens at the event horizon is stranger than a horror story.",
      "",
      "Orbit walks through the pictures and the evidence.",
      "",
      "Chapters",
      "0:00 Cold open",
      "1:00 The horizon",
      "",
      "Subscribe for the next film.",
      "",
      "Playlist",
      "More Orbit documentaries",
      "",
      "#OrbitWithBen #BlackHoles",
    ].join("\n");

    const desc = appendAffiliateSectionToDescription({
      description: base,
      links: withDupes,
    });

    expect(desc.startsWith("Some")).toBe(false);
    expect(desc.indexOf("Subscribe for the next film")).toBeLessThan(
      desc.indexOf("If you want to go further"),
    );
    expect(desc.indexOf("If you want to go further")).toBeLessThan(
      desc.indexOf("Playlist"),
    );
    expect(desc.indexOf(CREATOR_AFFILIATE_DISCLOSURE)).toBeGreaterThan(
      desc.indexOf("/go/"),
    );
    expect(desc.indexOf(CREATOR_AFFILIATE_DISCLOSURE)).toBeLessThan(
      desc.indexOf("Playlist"),
    );
    expect(affiliateBlockAppearsInFirstScreen(desc)).toBe(false);
    expect(desc.match(/beginner-telescope/g)?.length).toBe(1);

    const again = appendAffiliateSectionToDescription({
      description: desc,
      links,
    });
    expect(
      again.toLowerCase().split("some of these links are affiliate").length - 1,
    ).toBe(1);
  });

  it("Shorts get no affiliate block", () => {
    const desc = appendAffiliateSectionToDescription({
      description: "Short CTA — watch the full film on the channel.",
      links,
      trustVideo: {
        title: "Diamond Planet Short",
        topic: "Wonder",
        isShort: true,
      },
    });
    expect(desc).toBe("Short CTA — watch the full film on the channel.");
    expect(desc).not.toContain("If you want to go further");
  });

  it("uses topic-tuned black-hole book first line", () => {
    const section = buildAffiliateDescriptionSection({
      links: [
        {
          productName: "Cosmology book",
          productSlug: "cosmology-book",
          category: "Astronomy books",
          url: "https://example.invalid/x",
        },
      ],
      topicKey: "black-holes",
    });
    expect(section).toContain(
      "How we actually know a black hole is there, without turning it into a horror story.",
    );
  });

  it("integrates with YouTube package description merge", () => {
    const merged = mergeDescriptionWithAffiliateLinks("Base description", links);
    expect(merged).toContain("Base description");
    expect(merged).toContain("If you want to go further");
    expect(merged.trim().includes(CREATOR_AFFILIATE_DISCLOSURE)).toBe(true);
  });

  it("dedupes recommendation lists", () => {
    const recs = recommendationsToDescriptionLinks([
      {
        product: product({
          id: "1",
          name: "A",
          slug: "a",
          category: "Books",
          tagSlugs: [],
        }),
        relevanceScore: 50,
        reasons: [],
        role: "primary",
      },
      {
        product: product({
          id: "1",
          name: "A",
          slug: "a",
          category: "Books",
          tagSlugs: [],
        }),
        relevanceScore: 40,
        reasons: [],
        role: "secondary",
      },
    ]);
    expect(dedupeRecommendations([
      {
        product: product({ id: "1", name: "A", slug: "a", category: "Books", tagSlugs: [] }),
        relevanceScore: 50,
        reasons: [],
        role: "primary",
      },
      {
        product: product({ id: "1", name: "A", slug: "a", category: "Books", tagSlugs: [] }),
        relevanceScore: 40,
        reasons: [],
        role: "secondary",
      },
    ])).toHaveLength(1);
    expect(recs).toHaveLength(2); // conversion helper does not dedupe; append does
  });
});

describe("redirect URL generation", () => {
  it("builds tracked affiliate URLs with utm params", () => {
    const url = buildTrackedAffiliateUrl({
      affiliateUrl: "https://example.invalid/aff/item?existing=1",
      videoSlug: "black-hole-fall",
      productSlug: "brilliant-physics",
    });
    expect(url).toContain("utm_source=youtube");
    expect(url).toContain("utm_medium=affiliate");
    expect(url).toContain("utm_campaign=black-hole-fall");
    expect(url).toContain("utm_content=brilliant-physics");
    expect(url).toContain("existing=1");
  });

  it("builds orbit redirect paths", () => {
    process.env.AFFILIATE_REDIRECT_BASE_URL = "https://orbitwithben.com/go";
    expect(buildOrbitRedirectUrl("beginner-telescope")).toBe(
      "https://orbitwithben.com/go/beginner-telescope",
    );
    delete process.env.AFFILIATE_REDIRECT_BASE_URL;
  });

  it("applies amazon tag from env without hard-coding", () => {
    process.env.AMAZON_ASSOCIATE_TAG = "orbit-test-21";
    const url = applyProgrammeAffiliateId(
      "https://www.amazon.co.uk/dp/B00TEST?tag=old",
      "amazon-associates-uk",
    );
    expect(url).toContain("tag=orbit-test-21");
    expect(url).not.toContain("orbitgo-21");
    delete process.env.AMAZON_ASSOCIATE_TAG;
  });

  it("builds /go destination from destinationUrl when affiliateUrl is empty", () => {
    process.env.AMAZON_ASSOCIATE_TAG = "orbit-test-21";
    const base = resolveAffiliateRedirectBase({
      destinationUrl:
        "https://www.amazon.co.uk/Turn-Left-Orion-Hundreds-Telescope/dp/1108457568",
      affiliateUrl: "",
    });
    const stamped = applyProgrammeAffiliateId(base, "amazon-associates-uk");
    expect(base).toContain("amazon.co.uk");
    expect(base).toContain("1108457568");
    expect(stamped).toContain("tag=orbit-test-21");
    delete process.env.AMAZON_ASSOCIATE_TAG;
  });
});

describe("commission and RPM", () => {
  it("estimates percentage and fixed commissions", () => {
    expect(
      estimateCommission({
        price: 100,
        commissionType: "PERCENTAGE",
        commissionValue: 10,
      }),
    ).toBe(10);
    expect(
      estimateCommission({
        price: 100,
        commissionType: "FIXED",
        commissionValue: 7.5,
      }),
    ).toBe(7.5);
  });

  it("computes affiliate RPM, EPC, conversion rate", () => {
    expect(affiliateRpm(50, 10_000)).toBe(5);
    expect(earningsPerClick(50, 100)).toBe(0.5);
    expect(conversionRate(5, 100)).toBe(5);
    expect(totalContentRpm({ views: 1000, adsenseRevenue: 4, affiliateRevenue: 2 })).toBe(6);
  });
});

describe("opportunity scoring", () => {
  it("scores beginner telescope intent very high", () => {
    const products = [
      product({
        id: "1",
        name: "Beginner telescope",
        slug: "beginner-telescope",
        category: "Beginner telescopes",
        tagSlugs: ["telescope", "beginner", "astronomy"],
        price: 179,
        evergreen: true,
        featured: true,
        programSlug: "astronomy-retailer",
      }),
      product({
        id: "2",
        name: "Binoculars",
        slug: "binoculars",
        category: "Binoculars",
        tagSlugs: ["binoculars", "astronomy"],
        price: 65,
        programSlug: "amazon-associates-uk",
      }),
    ];
    const score = scoreAffiliateOpportunity(
      {
        title: "Best Telescope for Beginners",
        topic: "Telescopes",
        primaryKeyword: "best telescope for beginners",
      },
      products,
      { views: 50_000 },
    );
    expect(score.total).toBeGreaterThanOrEqual(80);
  });

  it("scores speculative science lower than gear intent", () => {
    const products = [
      product({
        id: "1",
        name: "Beginner telescope",
        slug: "beginner-telescope",
        category: "Beginner telescopes",
        tagSlugs: ["telescope", "astronomy"],
        evergreen: true,
      }),
    ];
    const score = scoreAffiliateOpportunity(
      {
        title: "Could Humans Survive Inside Jupiter?",
        topic: "Planetary Science",
        primaryKeyword: "survive inside jupiter",
      },
      products,
    );
    expect(score.total).toBeLessThan(70);
  });
});

describe("affiliate CSV import", () => {
  const csv = `Date,Product Name,Clicks,Items Shipped,Revenue,Earnings,Order ID,Currency
2026-08-01,Beginner telescope,12,1,179.00,8.95,AMZ-001,GBP
2026-08-02,Astronomy binoculars,8,2,130.00,5.20,AMZ-002,GBP`;

  it("previews and parses amazon mapping", () => {
    const preview = previewAffiliateCsv(csv, AFFILIATE_CSV_DEFAULT_MAPPINGS.amazon!);
    expect(preview.missing).toHaveLength(0);
    expect(preview.rowCount).toBe(2);
    expect(preview.sampleRows[0].commission).toBe(8.95);

    const { rows, contentHash } = parseAffiliateCsv(
      csv,
      AFFILIATE_CSV_DEFAULT_MAPPINGS.amazon!,
    );
    expect(contentHash).toHaveLength(64);
    const { conversions, errors } = rowsToConversions(rows);
    expect(errors).toHaveLength(0);
    expect(conversions).toHaveLength(2);
    expect(conversions[0].orderReference).toBe("AMZ-001");
  });
});

describe("url health scheduling", () => {
  it("only rechecks after interval", () => {
    expect(shouldCheckUrl(null)).toBe(true);
    expect(shouldCheckUrl(new Date(), 1000, Date.now())).toBe(false);
    expect(shouldCheckUrl(new Date(Date.now() - 2000), 1000, Date.now())).toBe(true);
  });
});

describe("affiliate social copy house rules", () => {
  it("strips raw merchant URLs and haul language", () => {
    const dirty =
      "Check this telescope https://www.amazon.co.uk/dp/B00TEST use my code ORBIT20 for 20% off haul";
    const { text, violations } = sanitizeAffiliateSocialText(dirty);
    expect(containsRawMerchantUrl(text)).toBe(false);
    expect(containsBannedAffiliatePhrase(text)).toBe(false);
    expect(violations.length).toBeGreaterThan(0);
    expect(text).not.toMatch(/amazon/i);
    expect(text).not.toMatch(/use my code/i);
  });

  it("allows only YouTube or /go/ tracked URLs", () => {
    expect(isAllowedSocialTrackedUrl("https://youtu.be/abc")).toBe(true);
    expect(isAllowedSocialTrackedUrl("https://orbitwithben.com/go/beginner-telescope")).toBe(
      true,
    );
    expect(isAllowedSocialTrackedUrl("/go/beginner-telescope")).toBe(true);
    expect(isAllowedSocialTrackedUrl("https://www.amazon.co.uk/dp/x")).toBe(false);
    expect(isAllowedSocialTrackedUrl("https://brilliant.org/course/physics")).toBe(false);
  });

  it("skips soft mention without natural object, film, or when platform already used", () => {
    expect(
      shouldIncludeAffiliateSoftMention({
        platform: "tiktok",
        hasNaturalObject: false,
        canNameSpecificFilm: true,
        productRelevantToVideo: true,
        hasApprovedPlacement: true,
      }).reason,
    ).toBe("no_natural_object");

    expect(
      shouldIncludeAffiliateSoftMention({
        platform: "tiktok",
        hasNaturalObject: true,
        canNameSpecificFilm: false,
        productRelevantToVideo: true,
        hasApprovedPlacement: true,
      }).reason,
    ).toBe("no_specific_film");

    expect(
      shouldIncludeAffiliateSoftMention({
        platform: "instagram_reels",
        hasNaturalObject: true,
        canNameSpecificFilm: true,
        productRelevantToVideo: true,
        hasApprovedPlacement: true,
        platformMentionedThisWeek: true,
      }).reason,
    ).toBe("platform_already_mentioned_this_week");
  });

  it("never emits raw merchant URLs when applying constraints", () => {
    const copies = generatePlatformCopy({
      shortTitle: "Event horizon",
      hook: "What happens at the event horizon?",
      topic: "Black Holes",
      youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
      longTitle: "What Would Happen If You Fell Into a Black Hole?",
      affiliate: {
        productLabel: "Brilliant Physics",
        productSlug: "brilliant-physics",
        hasNaturalObject: true,
        productRelevantToVideo: true,
        hasApprovedPlacement: true,
        youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
        longTitle: "What Would Happen If You Fell Into a Black Hole?",
      },
    });

    for (const copy of copies) {
      expect(containsRawMerchantUrl(copy.caption)).toBe(false);
      expect(containsBannedAffiliatePhrase(copy.caption)).toBe(false);
      expect(copy.caption.toLowerCase()).not.toContain("amazon.");
      expect(copy.caption.toLowerCase()).not.toContain("brilliant.org");
      // Soft mention is a caption tail afterthought — never the opening line
      const first = copy.caption.split("\n").find((l) => l.trim()) || "";
      expect(first.toLowerCase().startsWith("brilliant")).toBe(false);
    }

    const tiktok = copies.find((c) => c.platform === "tiktok")!;
    expect(tiktok.caption).toContain("YouTube description");
  });

  it("assertAffiliateSafeSocialCopy rejects merchant leaks", () => {
    expect(() =>
      assertAffiliateSafeSocialCopy("Buy here https://www.amazon.co.uk/dp/x"),
    ).toThrow(/house rules/);
    expect(() =>
      assertAffiliateSafeSocialCopy("Thought about silence.\n\nFull film: https://youtu.be/abc"),
    ).not.toThrow();
  });

  it("soft mention line never includes merchant hosts", () => {
    const line = buildSoftAffiliateMentionLine({
      platform: "x",
      productLabel: "Beginner telescope",
      goUrl: "https://orbitwithben.com/go/beginner-telescope",
    });
    expect(line).toBeTruthy();
    expect(line!).toContain("/go/");
    expect(containsRawMerchantUrl(line!)).toBe(false);
  });
});

describe("editorial trust gate (Video Auditor)", () => {
  const howToVideo = {
    title: "How to Find Jupiter Through a Telescope Tonight",
    topic: "Stargazing",
    script:
      "Tonight we use a sky atlas and look through the beginner telescope to find Jupiter.",
    primaryKeyword: "find jupiter telescope",
  };

  const namedTelescope: EditorialTrustProductInput = {
    ...product({
      id: "t1",
      name: "Beginner telescope",
      slug: "beginner-telescope",
      category: "Beginner telescopes",
      tagSlugs: ["telescope", "beginner"],
      price: 179,
    }),
    namedInVideo: true,
    helpsViewerDoTheThing: true,
    shownOnScreen: true,
    wouldRecommendWithoutCommission: true,
  };

  it("rejects Shorts — zero affiliate links", () => {
    const gate = evaluateEditorialTrustGate(
      { ...howToVideo, isShort: true },
      namedTelescope,
    );
    expect(gate.pass).toBe(false);
    expect(gate.failures).toContain("SHORTS_ZERO_AFFILIATE");

    const filtered = filterDescriptionLinksThroughTrustGate({
      video: { title: "Diamond Planet Short", topic: "Wonder", isShort: true },
      candidates: [{ product: namedTelescope, role: "primary" }],
    });
    expect(filtered.accepted).toHaveLength(0);
  });

  it("rejects unnamed products (not in VO / on screen)", () => {
    const vpn: EditorialTrustProductInput = {
      ...product({
        id: "vpn",
        name: "OrbitVPN Pro",
        slug: "orbit-vpn",
        category: "VPN",
        tagSlugs: ["vpn"],
      }),
      wouldRecommendWithoutCommission: true,
      namedInVideo: false,
    };
    const gate = evaluateEditorialTrustGate(howToVideo, vpn);
    expect(gate.pass).toBe(false);
    expect(gate.failures).toContain("NOT_NAMED_IN_VIDEO");
  });

  it("rejects no-commission fail", () => {
    const junk: EditorialTrustProductInput = {
      ...product({
        id: "j1",
        name: "Crypto Space Token",
        slug: "crypto-space",
        category: "Crypto",
        tagSlugs: ["crypto"],
      }),
      wouldRecommendWithoutCommission: false,
      namedInVideo: true,
    };
    const gate = evaluateEditorialTrustGate(
      {
        title: "Black Holes Explained",
        topic: "Black Holes",
        script: "Crypto Space Token is named somehow",
      },
      junk,
    );
    expect(gate.pass).toBe(false);
    expect(gate.failures).toContain("NO_COMMISSION_FAIL");
  });

  it("rejects more than 2 links on a film", () => {
    const paper: EditorialTrustProductInput = {
      ...product({
        id: "p1",
        name: "JADES survey paper",
        slug: "jades-paper",
        category: "Astronomy books",
        tagSlugs: ["books"],
        price: 0,
      }),
      namedInVideo: true,
      helpsViewerDoTheThing: true,
      isFreeOrCheapCompanion: true,
      wouldRecommendWithoutCommission: true,
    };
    const book: EditorialTrustProductInput = {
      ...product({
        id: "b1",
        name: "Cosmology companion book",
        slug: "cosmo-book",
        category: "Astronomy books",
        tagSlugs: ["books"],
        price: 12,
      }),
      namedInVideo: true,
      helpsViewerDoTheThing: true,
      isFreeOrCheapCompanion: true,
      wouldRecommendWithoutCommission: true,
    };
    const extra: EditorialTrustProductInput = {
      ...product({
        id: "e1",
        name: "Sky Guide app",
        slug: "sky-app",
        category: "Planetarium app",
        tagSlugs: ["astronomy"],
      }),
      namedInVideo: true,
      helpsViewerDoTheThing: true,
      wouldRecommendWithoutCommission: true,
    };

    const explainer = {
      title: "JWST and the JADES survey explained",
      topic: "JWST",
      script:
        "We discuss the JADES survey paper and the cosmology companion book and Sky Guide app.",
    };

    const { accepted, rejected } = filterDescriptionLinksThroughTrustGate({
      video: explainer,
      candidates: [
        { product: paper, role: "primary" },
        { product: book, role: "companion" },
        { product: extra, role: "secondary" },
      ],
    });
    expect(accepted.length).toBeLessThanOrEqual(2);
    expect(
      rejected.some(
        (r) =>
          r.gate.failures.includes("TOO_MANY_LINKS") ||
          r.gate.failures.includes("STACK_NOT_COMPANION"),
      ),
    ).toBe(true);
  });

  it("passes named sky-atlas / tool on how-to film", () => {
    const gate = evaluateEditorialTrustGate(howToVideo, namedTelescope);
    expect(gate.pass).toBe(true);
    expect(gate.videoType).toBe("HOW_TO");
  });

  it("wonder films reject telescope affiliate without named book/paper", () => {
    const gate = evaluateEditorialTrustGate(
      {
        title: "Diamond Planets Around Three Suns",
        topic: "Exoplanets",
        script: "A beautiful world of diamond.",
      },
      namedTelescope,
    );
    expect(gate.pass).toBe(false);
    expect(gate.failures).toContain("WONDER_REQUIRES_NAMED_BOOK_OR_PAPER");
  });

  it("description generator refuses ungated auto-insert without trust metadata", () => {
    const desc = appendAffiliateSectionToDescription({
      description: "Film body.\nSubscribe for more.",
      links: [
        {
          productName: "Random VPN",
          productSlug: "vpn",
          category: "VPN",
          url: "https://example.invalid/vpn",
        },
      ],
      trustVideo: { title: "Black Holes Explained", topic: "Physics", isShort: false },
    });
    expect(desc).toBe("Film body.\nSubscribe for more.");
  });
});

describe("live social channel affiliate snippets", () => {
  const baseInput = {
    videoSlug: "black-hole-fall",
    videoTitle: "What Would Happen If You Fell Into a Black Hole?",
    topic: "Black Holes",
    hook: "What happens at the event horizon?",
    youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
    productLabel: "Brilliant Physics",
    productSlug: "brilliant-physics",
    hasNaturalObject: true,
    productRelevantToVideo: true,
    hasApprovedPlacement: true,
    preferYouTubePointer: true as const,
  };

  it("produces Threads, Instagram Reels, Instagram Feed, and Facebook Page as distinct platforms", () => {
    const snippets = generateAffiliateSocialSnippets(baseInput);
    const platforms = snippets.map((s) => s.platform);
    expect(platforms).toEqual([
      "threads",
      "instagram_reels",
      "instagram_feed",
      "facebook_page",
    ]);
    expect(platforms).not.toContain("facebook_reels");
    expect(snippets.find((s) => s.platform === "facebook_page")).toBeTruthy();
    expect(snippets.every((s) => s.approvedForPublish === false)).toBe(true);
  });

  it("never contains raw merchant URLs", () => {
    const withGo = generateAffiliateSocialSnippets({
      ...baseInput,
      preferYouTubePointer: false,
    });
    for (const s of [...generateAffiliateSocialSnippets(baseInput), ...withGo]) {
      expect(containsRawMerchantUrl(s.caption)).toBe(false);
      expect(s.caption.toLowerCase()).not.toContain("amazon.");
      expect(s.caption.toLowerCase()).not.toContain("brilliant.org");
      expect(s.caption.toLowerCase()).not.toContain("shop now");
      if (s.trackedUrl) {
        expect(isAllowedSocialTrackedUrl(s.trackedUrl)).toBe(true);
      }
    }
  });

  it("stamps utm_source per channel on /go/ and YouTube links", () => {
    const goThreads = buildSocialGoUrl({
      productSlug: "brilliant-physics",
      platform: "threads",
      videoSlug: "black-hole-fall",
      hasAffiliateMention: true,
    });
    expect(goThreads).toContain("utm_source=threads");
    expect(goThreads).toContain("utm_medium=affiliate");
    expect(goThreads).toContain("utm_campaign=black-hole-fall");
    expect(goThreads).toContain("utm_content=brilliant-physics");
    expect(socialPlatformToClickSource("threads")).toBe("threads");

    const goIg = buildSocialGoUrl({
      productSlug: "brilliant-physics",
      platform: "instagram_reels",
      videoSlug: "black-hole-fall",
    });
    expect(goIg).toContain("utm_source=instagram");
    expect(socialPlatformToClickSource("instagram_feed")).toBe("instagram");

    const goFb = buildSocialGoUrl({
      productSlug: "brilliant-physics",
      platform: "facebook_page",
      videoSlug: "black-hole-fall",
    });
    expect(goFb).toContain("utm_source=facebook");
    expect(socialPlatformToClickSource("facebook_page")).toBe("facebook");
    expect(socialPlatformToClickSource("facebook_reels")).toBe("facebook");

    const yt = buildSocialYouTubeUrl({
      youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
      platform: "threads",
      videoSlug: "black-hole-fall",
      productSlug: "brilliant-physics",
      hasAffiliateMention: true,
    });
    expect(yt).toContain("utm_source=threads");
    expect(yt).toContain("utm_medium=affiliate");

    expect(normalizeAffiliateClickSource("instagram_reels")).toBe("instagram");
    expect(normalizeAffiliateClickSource("facebook_page")).toBe("facebook");
    expect(normalizeAffiliateClickSource("threads")).toBe("threads");
  });

  it("Facebook Page caption stays documentary — link at end, no shop energy", () => {
    const fb = generateAffiliateSocialSnippets(baseInput).find(
      (s) => s.platform === "facebook_page",
    )!;
    expect(fb.caption.toLowerCase()).not.toContain("shop now");
    const lines = fb.caption.trim().split("\n").filter(Boolean);
    expect(lines[0].toLowerCase().startsWith("brilliant")).toBe(false);
    if (fb.trackedUrl) {
      expect(fb.caption.trim().endsWith(fb.trackedUrl) || fb.caption.includes(fb.trackedUrl)).toBe(
        true,
      );
    }
  });

  it("encodes Social Media Manager Thursday-film Facebook pattern", () => {
    const door = "https://youtu.be/jwst-example";
    const caption = renderFacebookPageTemplate({
      style: "thursday_film",
      wonder: FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.wonder,
      body: FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.body,
      doorUrl: door,
      hasFilmThisWeek: true,
      includeSoftMention: true,
    });
    expect(caption).toBe(
      `${FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.captionWithoutUrl}\n${door}`,
    );
    expect(firstNonEmptyLine(caption)).toBe(FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.wonder);
    expect(lastNonEmptyLine(caption)).toBe(door);
    expect(countCaptionLines(caption)).toBeGreaterThanOrEqual(3);
    expect(countCaptionLines(caption)).toBeLessThanOrEqual(5);
    expect(caption).toContain(FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.softLine);
  });

  it("encodes Social Media Manager how-to Facebook pattern (+ /go/ when no film)", () => {
    const yt = "https://youtu.be/telescope-night";
    const withFilm = renderFacebookPageTemplate({
      style: "how_to",
      wonder: FIXTURE_FACEBOOK_PAGE_HOWTO.wonder,
      doorUrl: yt,
      hasFilmThisWeek: true,
      includeSoftMention: true,
    });
    expect(withFilm).toBe(
      `${FIXTURE_FACEBOOK_PAGE_HOWTO.captionWithFilmWithoutUrl}\n${yt}`,
    );

    const go = "https://orbitwithben.com/go/telescope";
    const noFilm = renderFacebookPageTemplate({
      style: "how_to",
      wonder: FIXTURE_FACEBOOK_PAGE_HOWTO.wonder,
      doorUrl: go,
      hasFilmThisWeek: false,
      includeSoftMention: true,
    });
    expect(noFilm).toContain(FIXTURE_FACEBOOK_PAGE_HOWTO.softLineWithoutFilm);
    expect(noFilm).not.toContain("Watch the film first");
    expect(lastNonEmptyLine(noFilm)).toBe(go);
  });

  it("Threads + Reels templates: thought first, one extra line, door last; never /go/ on line 1", () => {
    const go = "https://orbitwithben.com/go/telescope";
    const threads = renderThreadsTemplate({
      wonder: "The sky was quieter than I expected.",
      doorUrl: go,
      includeSoftMention: true,
      doorIsGo: true,
    });
    expect(firstNonEmptyLine(threads)).not.toContain("/go/");
    expect(lastNonEmptyLine(threads)).toBe(go);

    const reels = renderInstagramReelsTemplate({
      wonder: "What happens at the event horizon?",
      doorUrl: go,
      includeSoftMention: true,
      doorIsGo: true,
    });
    expect(firstNonEmptyLine(reels)).not.toContain("/go/");
    expect(reels).toContain("If you want to look at this yourself:");
  });

  it("generator Facebook/IG feed matches SMM thursday_film shape", () => {
    const snippets = generateAffiliateSocialSnippets({
      videoSlug: "jwst-early-galaxies",
      videoTitle: "JWST and the Galaxies That Should Not Be There",
      topic: "JWST",
      hook: FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.wonder,
      body: FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.body,
      youtubeUrl: "https://youtu.be/jwst-film",
      productLabel: "JWST explainer",
      productSlug: FIXTURE_JWST_LIVE.softMentionGoSlugWhenReady,
      hasNaturalObject: true,
      productRelevantToVideo: true,
      hasApprovedPlacement: true,
      postStyle: "thursday_film",
    });
    const fb = snippets.find((s) => s.platform === "facebook_page")!;
    const ig = snippets.find((s) => s.platform === "instagram_feed")!;
    expect(fb.caption).toContain(FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.softLine);
    expect(firstNonEmptyLine(fb.caption)).toBe(FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM.wonder);
    expect(ig.caption).toContain(FIXTURE_JWST_LIVE.softLineInstagram);
    expect(containsRawMerchantUrl(fb.caption)).toBe(false);
    expect(fb.approvedForPublish).toBe(false);
    expect(fb.caption).not.toMatch(/Turn Left at Orion/i);
    expect(fb.caption.toLowerCase()).not.toMatch(/\btelescope\b/);
  });

  it("rejects Facebook Page never-list (merchant, shop now, haul, multi-brand, …)", () => {
    expect(
      facebookPageCaptionViolations(
        "Buy this telescope\nhttps://www.amazon.co.uk/dp/x",
        { brandNames: ["Beginner telescope"] },
      ),
    ).toEqual(
      expect.arrayContaining(["raw_merchant_url", "door_not_youtube_or_go"]),
    );

    expect(
      facebookPageCaptionViolations("Shop now for space merch\nhttps://youtu.be/x"),
    ).toEqual(expect.arrayContaining(["boost_or_catalog_language"]));

    expect(
      facebookPageCaptionViolations(
        "Brilliant Physics is amazing and Amazon has deals\nhttps://youtu.be/x",
        { brandNames: ["Brilliant", "Amazon"] },
      ),
    ).toEqual(expect.arrayContaining(["more_than_one_brand"]));

    expect(
      facebookPageCaptionViolations("Use my code SPACE20 for 20% off\nhttps://youtu.be/x"),
    ).toEqual(expect.arrayContaining(["banned_shop_phrase"]));

    expect(
      facebookPageCaptionViolations("Link in comments for the telescope\nhttps://youtu.be/x"),
    ).toEqual(expect.arrayContaining(["link_in_comments_spam"]));

    expect(() =>
      assertFacebookPageCaptionSafe(
        "Haul unboxing of Amazon gear\nhttps://www.amazon.com/x",
      ),
    ).toThrow(/Facebook Page caption violates/);

    // Soft mention must not be line 1
    expect(
      facebookPageCaptionViolations(
        "If you want that kind of view, I left the one I use under the film.\nhttps://youtu.be/x",
      ),
    ).toEqual(expect.arrayContaining(["soft_mention_on_line_1"]));

    // Same /go/ three days, no film
    expect(
      facebookPageCaptionViolations(
        "Quiet night.\nhttps://orbitwithben.com/go/telescope",
        {
          productSlug: "telescope",
          recentGoSlugs: ["telescope", "telescope"],
          hasFilmThisWeek: false,
        },
      ),
    ).toEqual(expect.arrayContaining(["same_go_three_days_no_film"]));
  });

  it("comment reply fixture discloses once and points at film or /go/", () => {
    expect(renderTelescopeCommentReply({ hasFilm: true })).toContain("under the film");
    expect(renderTelescopeCommentReply({ hasFilm: true })).toContain("affiliate");
    const go = renderTelescopeCommentReply({
      hasFilm: false,
      doorUrl: "https://orbitwithben.com/go/telescope",
    });
    expect(go).toContain("/go/telescope");
    expect(containsRawMerchantUrl(go)).toBe(false);
  });

  it("Shorts description path still gets zero affiliate links", () => {
    const filtered = filterDescriptionLinksThroughTrustGate({
      video: { title: "Diamond Planet Short", topic: "Wonder", isShort: true },
      candidates: [
        {
          product: {
            ...product({
              id: "t1",
              name: "Beginner telescope",
              slug: "beginner-telescope",
              category: "Beginner telescopes",
              tagSlugs: ["telescope"],
            }),
            namedInVideo: true,
            helpsViewerDoTheThing: true,
            wouldRecommendWithoutCommission: true,
          },
          role: "primary",
        },
      ],
    });
    expect(filtered.accepted).toHaveLength(0);
  });
});

describe("affiliate goals ladder (reporting only)", () => {
  it("resolves clock from earlier of first approval or first click", () => {
    const click = new Date("2026-03-01T12:00:00Z");
    const approved = new Date("2026-03-10T12:00:00Z");
    const start = resolveGoalsClockStart({
      firstApprovedPlacementAt: approved,
      firstClickAt: click,
    });
    expect(start?.toISOString().startsWith("2026-03-01")).toBe(true);
  });

  it("Month 1 target £20 with floor £10; Month 2 = 2× previous actual", () => {
    expect(computeMonthTargetGbp({ monthNumber: 1, previousMonthActualGbp: 0 })).toEqual({
      targetGbp: 20,
      floorGbp: 10,
    });
    expect(computeMonthTargetGbp({ monthNumber: 2, previousMonthActualGbp: 12.5 })).toEqual({
      targetGbp: 25,
      floorGbp: null,
    });
    expect(computeMonthTargetGbp({ monthNumber: 3, previousMonthActualGbp: 40 }).targetGbp).toBe(
      80,
    );
  });

  it("builds snapshot with month range, pace status, and last-month actual from Month 2+", () => {
    const clockStart = new Date(2026, 0, 15); // 15 Jan 2026 local
    const now = new Date(2026, 1, 20); // 20 Feb 2026 → Month 2 (starts 15 Feb)
    const commissions = [
      { date: new Date(2026, 0, 20), commissionAmount: 12 }, // Month 1
      { date: new Date(2026, 1, 16), commissionAmount: 5 }, // Month 2
    ];
    const snap = buildAffiliateGoalsSnapshot({
      now,
      clockStart,
      commissions,
      clicksThisMonth: 3,
      workingLinks: 8,
      brokenLinks: 1,
    });
    expect(snap.reportingOnly).toBe(true);
    expect(snap.clockStarted).toBe(true);
    expect(snap.monthNumber).toBe(2);
    expect(snap.lastMonthActualGbp).toBe(12);
    expect(snap.targetGbp).toBe(24); // 2 × 12
    expect(snap.revenueSoFarGbp).toBe(5);
    expect(snap.clicksThisMonth).toBe(3);
    expect(snap.workingLinks).toBe(8);
    expect(snap.brokenLinks).toBe(1);
    expect(snap.monthStart).toBeTruthy();
    expect(snap.monthEnd).toBeTruthy();
    expect(["on_track", "behind", "ahead"]).toContain(snap.status);
  });

  it("does not invent a clock when there is no placement and no click", () => {
    const snap = buildAffiliateGoalsSnapshot({
      now: new Date("2026-08-15T12:00:00Z"),
      clockStart: null,
      commissions: [],
      clicksThisMonth: 0,
      workingLinks: 0,
      brokenLinks: 0,
    });
    expect(snap.status).toBe("not_started");
    expect(snap.monthNumber).toBeNull();
  });
});

describe("affiliate go-live readiness", () => {
  it("passes tracked redirects when catalogue is live but flags missing programme IDs", () => {
    const report = evaluateAffiliateGoLive({
      amazonTag: null,
      brilliantId: null,
      appBaseUrl: "https://ops.example.com",
      affiliateRedirectBaseUrl: "https://orbitwithben.com/go",
      activeProductCount: 8,
      placeholderUrlCount: 0,
      brokenUrlCount: 0,
      activeProgramCount: 3,
      approvedPlacementCount: 0,
      clickCount: 0,
    });
    expect(report.readyForTrackedRedirects).toBe(true);
    expect(report.readyForPaidTraffic).toBe(false);
    expect(report.checks.find((c) => c.id === "amazon_tag")?.status).toBe("fail");
  });

  it("is ready for paid traffic when a programme ID is set", () => {
    const report = evaluateAffiliateGoLive({
      amazonTag: "orbit-21",
      brilliantId: null,
      appBaseUrl: "https://ops.example.com",
      affiliateRedirectBaseUrl: "https://orbitwithben.com/go",
      activeProductCount: 8,
      placeholderUrlCount: 0,
      brokenUrlCount: 0,
      activeProgramCount: 3,
      approvedPlacementCount: 1,
      clickCount: 1,
    });
    expect(report.readyForPaidTraffic).toBe(true);
  });

  it("blocks when placeholder merchant URLs remain", () => {
    const report = evaluateAffiliateGoLive({
      amazonTag: "orbit-21",
      brilliantId: "brill-1",
      appBaseUrl: "https://ops.example.com",
      affiliateRedirectBaseUrl: "https://orbitwithben.com/go",
      activeProductCount: 8,
      placeholderUrlCount: 3,
      brokenUrlCount: 0,
      activeProgramCount: 3,
      approvedPlacementCount: 0,
      clickCount: 0,
    });
    expect(report.readyForTrackedRedirects).toBe(false);
    expect(isPlaceholderAffiliateUrl("https://example.invalid/aff/x")).toBe(true);
  });
});

describe("Amazon Associates UK live destinations", () => {
  const TOPIC_BOOK_SLUGS = [
    "fermi-paradox-book",
    "jwst-book",
    "black-hole-book",
    "cosmology-end-book",
    "exoplanet-book",
    "europa-icy-moons-book",
  ] as const;

  it("confirmed Amazon products use amazon.co.uk destination URLs", () => {
    const book = liveUrlForSlug("beginner-astronomy-book");
    const scope = liveUrlForSlug("beginner-telescope");
    expect(book).toBeTruthy();
    expect(scope).toBeTruthy();
    expect(isAmazonUkDestinationUrl(book!.destinationUrl)).toBe(true);
    expect(isAmazonUkDestinationUrl(scope!.destinationUrl)).toBe(true);
    expect(book!.destinationUrl).toContain("1108457568");
    expect(scope!.destinationUrl).toContain("B00DV6SBRO");
    expect(book!.destinationUrl).not.toMatch(/example\.invalid/i);
    expect(scope!.destinationUrl).not.toMatch(/example\.invalid/i);
  });

  it("topic books use verified amazon.co.uk /dp/ destinations (no invented ASINs)", () => {
    const expected: Record<(typeof TOPIC_BOOK_SLUGS)[number], string> = {
      "fermi-paradox-book": "3319132350",
      "jwst-book": "1789295726",
      "black-hole-book": "1529086744",
      "cosmology-end-book": "0141989580",
      "exoplanet-book": "147291774X",
      "europa-icy-moons-book": "0691227284",
    };
    for (const slug of TOPIC_BOOK_SLUGS) {
      const spec = liveUrlForSlug(slug);
      expect(spec, slug).toBeTruthy();
      expect(isAmazonUkDestinationUrl(spec!.destinationUrl), slug).toBe(true);
      expect(spec!.destinationUrl).toMatch(/amazon\.co\.uk/i);
      expect(spec!.destinationUrl).toContain(`/dp/${expected[slug]}`);
      expect(spec!.destinationUrl).not.toMatch(/example\.invalid/i);
      expect(spec!.programmeSlug).toBe("amazon-associates-uk");
      expect(spec!.active ?? true).toBe(true);
      expect(spec!.featured ?? false).toBe(false);
      expect(spec!.tags).toContain("books");
    }
  });

  it("topic book tags match film topics", () => {
    expect(liveUrlForSlug("fermi-paradox-book")!.tags).toEqual(
      expect.arrayContaining(["fermi", "aliens", "seti"]),
    );
    expect(liveUrlForSlug("jwst-book")!.tags).toEqual(expect.arrayContaining(["jwst"]));
    expect(liveUrlForSlug("jwst-book")!.tags).not.toContain("telescope");
    expect(liveUrlForSlug("black-hole-book")!.tags).toEqual(
      expect.arrayContaining(["black-hole"]),
    );
    expect(liveUrlForSlug("cosmology-end-book")!.tags).toEqual(
      expect.arrayContaining(["cosmology"]),
    );
    expect(liveUrlForSlug("exoplanet-book")!.tags).toEqual(
      expect.arrayContaining(["exoplanets"]),
    );
    expect(liveUrlForSlug("europa-icy-moons-book")!.tags).toEqual(
      expect.arrayContaining(["europa"]),
    );
  });

  it("never hard-codes the Associates tag in live URL specs", () => {
    for (const spec of LIVE_PRODUCT_URLS) {
      expect(JSON.stringify(spec)).not.toContain("orbitgo-21");
      expect(spec.destinationUrl).not.toMatch(/[?&]tag=/i);
      expect(spec.affiliateUrl || "").not.toMatch(/[?&]tag=/i);
    }
  });

  it("keeps space-lego inactive and LEGO off live social copy", () => {
    const lego = liveUrlForSlug("space-lego");
    expect(lego?.active).toBe(false);

    const snippets = generateAffiliateSocialSnippets({
      videoSlug: "mars-night",
      videoTitle: "What Would Happen If You Lived on Mars?",
      topic: "Mars",
      hook: "Dust storms that blot out the sun.",
      youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
      productLabel: "Turn Left at Orion",
      productSlug: "beginner-astronomy-book",
      hasNaturalObject: true,
      productRelevantToVideo: true,
      hasApprovedPlacement: true,
      preferYouTubePointer: false,
    });
    for (const s of snippets) {
      expect(s.caption.toLowerCase()).not.toContain("lego");
      expect(containsRawMerchantUrl(s.caption)).toBe(false);
      expect(s.caption.toLowerCase()).not.toContain("amazon.");
      expect(s.caption.toLowerCase()).not.toContain("amazon.co.uk");
      if (s.trackedUrl) {
        expect(isAllowedSocialTrackedUrl(s.trackedUrl)).toBe(true);
        expect(s.trackedUrl).toMatch(/youtu\.?be|\/go\//i);
      }
    }
  });

  it("social snippets for topic books never include merchant URLs", () => {
    const snippets = generateAffiliateSocialSnippets({
      videoSlug: "black-hole-film",
      videoTitle: "What Happens If You Fall Into a Black Hole?",
      topic: "Black Holes",
      hook: "Beyond the event horizon, the future is a direction in space.",
      youtubeUrl: "https://youtu.be/black-hole-film",
      productLabel: "A Brief History of Black Holes",
      productSlug: "black-hole-book",
      hasNaturalObject: true,
      productRelevantToVideo: true,
      hasApprovedPlacement: true,
      preferYouTubePointer: false,
    });
    for (const s of snippets) {
      expect(containsRawMerchantUrl(s.caption)).toBe(false);
      expect(s.caption.toLowerCase()).not.toContain("amazon.");
      expect(s.caption.toLowerCase()).not.toContain("amazon.co.uk");
      if (s.trackedUrl) {
        expect(isAllowedSocialTrackedUrl(s.trackedUrl)).toBe(true);
        expect(s.trackedUrl).toMatch(/youtu\.?be|\/go\//i);
      }
    }
  });

  it("does not recommend beginner telescope or beginner astronomy book on topic films", () => {
    const topicCatalogue: ProductMatchInput[] = [
      product({
        id: "bh-book",
        name: "A Brief History of Black Holes",
        slug: "black-hole-book",
        category: "Space books",
        tagSlugs: ["books", "black-hole", "physics", "cosmology"],
        priority: 7,
      }),
      product({
        id: "fermi-book",
        name: "Where Is Everybody? — Fermi Paradox (Stephen Webb)",
        slug: "fermi-paradox-book",
        category: "Space books",
        tagSlugs: ["books", "fermi", "aliens", "seti", "astronomy"],
        priority: 6,
      }),
      product({
        id: "jwst-book",
        name: "Webb’s Universe",
        slug: "jwst-book",
        category: "Space books",
        tagSlugs: ["books", "jwst", "nasa", "astronomy"],
        priority: 6,
      }),
      product({
        id: "cosmo-book",
        name: "The End of Everything",
        slug: "cosmology-end-book",
        category: "Space books",
        tagSlugs: ["books", "cosmology", "physics"],
        priority: 6,
      }),
      product({
        id: "exo-book",
        name: "The Planet Factory",
        slug: "exoplanet-book",
        category: "Space books",
        tagSlugs: ["books", "exoplanets", "astronomy"],
        priority: 6,
      }),
      product({
        id: "beginner-book",
        name: "Turn Left at Orion",
        slug: "beginner-astronomy-book",
        category: "Astronomy books",
        tagSlugs: ["books", "astronomy", "beginner", "telescope"],
        evergreen: true,
      }),
      product({
        id: "scope",
        name: "Beginner telescope",
        slug: "beginner-telescope",
        category: "Beginner telescopes",
        tagSlugs: ["telescope", "beginner", "astronomy"],
        evergreen: true,
        featured: true,
      }),
      product({
        id: "brilliant",
        name: "Brilliant Physics",
        slug: "brilliant-physics",
        category: "Physics",
        tagSlugs: ["physics", "black-hole", "cosmology"],
        programSlug: "brilliant",
        featured: true,
        priority: 8,
      }),
    ];

    const films: Array<{ video: VideoMatchInput; expectSlug: string }> = [
      {
        video: {
          title: "What Happens If You Fall Into a Black Hole?",
          topic: "Black Holes",
          primaryKeyword: "black hole",
        },
        expectSlug: "black-hole-book",
      },
      {
        video: {
          title: "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained",
          topic: "Fermi Paradox",
          primaryKeyword: "fermi paradox",
        },
        expectSlug: "fermi-paradox-book",
      },
      {
        video: {
          title: "What JWST Changed About Cosmic Dawn",
          topic: "JWST",
          primaryKeyword: "james webb",
        },
        expectSlug: "jwst-book",
      },
      {
        video: {
          title: "The End of the Universe (Astrophysically Speaking)",
          topic: "Cosmology",
          primaryKeyword: "end of the universe",
          summary: "Heat death, vacuum decay, and the big rip.",
        },
        expectSlug: "cosmology-end-book",
      },
      {
        video: {
          title: "Alien Worlds: Exoplanets Beyond Our Solar System",
          topic: "Exoplanets",
          primaryKeyword: "exoplanets",
        },
        expectSlug: "exoplanet-book",
      },
    ];

    for (const { video, expectSlug } of films) {
      const set = recommendProductsForVideo(video, topicCatalogue);
      const slugs = set.all.map((r) => r.product.slug);
      expect(slugs, video.title).toContain(expectSlug);
      expect(slugs, video.title).not.toContain("beginner-telescope");
      expect(slugs, video.title).not.toContain("beginner-astronomy-book");
      expect(productFamilyOf(set.primary!.product)).toBe("books");
    }
  });
});

describe("Social Media Manager JWST live captions", () => {
  const door = "https://youtu.be/jwst-live-film";

  function assertJwstCaptionSafe(caption: string, trackedUrl?: string | null) {
    expect(containsRawMerchantUrl(caption)).toBe(false);
    expect(caption.toLowerCase()).not.toContain("amazon.");
    expect(caption.toLowerCase()).not.toContain("shop now");
    expect(caption.toLowerCase()).not.toContain("lego");
    expect(caption.toLowerCase()).not.toMatch(/\btelescope\b/);
    expect(caption).not.toMatch(/Turn Left at Orion/i);
    expect(caption).not.toContain("beginner-astronomy-book");
    expect(caption).not.toContain("beginner-telescope");
    if (trackedUrl) {
      expect(isAllowedSocialTrackedUrl(trackedUrl)).toBe(true);
      expect(trackedUrl).not.toMatch(/amazon\.co\.uk/i);
      expect(trackedUrl).not.toContain("/go/beginner-telescope");
      expect(trackedUrl).not.toContain("/go/beginner-astronomy-book");
    }
  }

  it("encodes exact Threads / Instagram / Facebook fixtures (no auto-post)", () => {
    expect(FIXTURE_JWST_LIVE.autoPost).toBe(false);
    expect(FIXTURE_JWST_LIVE.approvedForPublish).toBe(false);
    expect(FIXTURE_JWST_LIVE.softMentionProductSlug).toBeNull();
    expect(FIXTURE_JWST_LIVE.softMentionGoSlugWhenReady).toBe("jwst-book");
    expect(FIXTURE_JWST_LIVE.forbidProductSlugs).toContain("beginner-telescope");
    expect(FIXTURE_JWST_LIVE.forbidProductSlugs).toContain(
      "beginner-astronomy-book",
    );
    expect(FIXTURE_JWST_LIVE.forbidProductSlugs).toContain("space-lego");
    expect(FIXTURE_JWST_LIVE.forbidProductLabels).toContain("Turn Left at Orion");

    // Soft-mention product fields must not point at observing guidebook / telescope
    expect(FIXTURE_JWST_LIVE.softMentionProductLabel).toBeNull();
    expect(
      `${FIXTURE_JWST_LIVE.softMentionProductSlug || ""} ${FIXTURE_JWST_LIVE.softMentionProductLabel || ""}`,
    ).not.toMatch(/Turn Left at Orion|beginner-astronomy-book|beginner-telescope/i);

    expect(renderJwstLiveCaption({ platform: "threads", doorUrl: door })).toBe(
      `${FIXTURE_JWST_LIVE.threadsCaptionWithoutUrl}\n${door}`,
    );
    expect(
      renderJwstLiveCaption({ platform: "instagram", doorUrl: door }),
    ).toBe(`${FIXTURE_JWST_LIVE.instagramCaptionWithoutUrl}\n${door}`);
    expect(
      renderJwstLiveCaption({ platform: "facebook_page", doorUrl: door }),
    ).toBe(`${FIXTURE_JWST_LIVE.facebookCaptionWithoutUrl}\n${door}`);

    for (const platform of ["threads", "instagram", "facebook_page"] as const) {
      assertJwstCaptionSafe(renderJwstLiveCaption({ platform, doorUrl: door }));
    }
  });

  it("JWST soft mention stays under-the-film copy — never telescope or Turn Left at Orion", () => {
    const fromTelescope = generateAffiliateSocialSnippets({
      videoSlug: "jwst-early-galaxies",
      videoTitle: "JWST and the Galaxies That Should Not Be There",
      topic: "JWST",
      youtubeUrl: door,
      productLabel: "Celestron FirstScope",
      productSlug: "beginner-telescope",
      hasNaturalObject: true,
      productRelevantToVideo: true,
      hasApprovedPlacement: true,
      postStyle: "thursday_film",
    });

    const fromObservingBook = generateAffiliateSocialSnippets({
      videoSlug: "jwst-early-galaxies",
      videoTitle: "JWST and the Galaxies That Should Not Be There",
      topic: "JWST",
      youtubeUrl: door,
      productLabel: "Turn Left at Orion",
      productSlug: "beginner-astronomy-book",
      hasNaturalObject: true,
      productRelevantToVideo: true,
      hasApprovedPlacement: true,
      postStyle: "thursday_film",
      preferYouTubePointer: false,
    });

    for (const s of [...fromTelescope, ...fromObservingBook]) {
      expect(s.approvedForPublish).toBe(false);
      assertJwstCaptionSafe(s.caption, s.trackedUrl);
      // Until jwst-book is the placement door, never a wrong /go/
      expect(s.trackedUrl).toMatch(/youtu\.?be/i);
    }

    const threads = fromTelescope.find((s) => s.platform === "threads")!;
    expect(threads.caption).toContain(FIXTURE_JWST_LIVE.softLineThreads);
    expect(threads.caption).toContain(FIXTURE_JWST_LIVE.bodyThreads);

    const ig = fromTelescope.find((s) => s.platform === "instagram_feed")!;
    expect(ig.caption).toContain(FIXTURE_JWST_LIVE.softLineInstagram);

    const fb = fromTelescope.find((s) => s.platform === "facebook_page")!;
    expect(fb.caption).toContain(FIXTURE_JWST_LIVE.softLineFacebook);
  });

  it("JWST door may use /go/jwst-book only — never beginner book or telescope", () => {
    const fromJwstBook = generateAffiliateSocialSnippets({
      videoSlug: "jwst-early-galaxies",
      videoTitle: "JWST and the Galaxies That Should Not Be There",
      topic: "JWST",
      youtubeUrl: door,
      productLabel: "Webb’s Universe",
      productSlug: "jwst-book",
      hasNaturalObject: true,
      productRelevantToVideo: true,
      hasApprovedPlacement: true,
      postStyle: "thursday_film",
      preferYouTubePointer: false,
    });
    for (const s of fromJwstBook) {
      expect(s.approvedForPublish).toBe(false);
      assertJwstCaptionSafe(s.caption, s.trackedUrl);
      if (s.trackedUrl?.includes("/go/")) {
        expect(s.trackedUrl).toContain("/go/jwst-book");
      }
    }
  });

  it("holds Threads until Thu 20 Aug 2026 18:00 Europe/London", () => {
    expect(
      isJwstThreadsPublishAllowed(new Date("2026-08-20T16:59:00.000Z")),
    ).toBe(false);
    expect(
      isJwstThreadsPublishAllowed(new Date("2026-08-20T17:00:00.000Z")),
    ).toBe(true);
  });

  it("holds telescope observing caption until a real observing post", () => {
    expect(FIXTURE_TELESCOPE_OBSERVING_HELD.status).toBe("held");
    expect(FIXTURE_TELESCOPE_OBSERVING_HELD.autoPost).toBe(false);
    expect(FIXTURE_TELESCOPE_OBSERVING_HELD.approvedForPublish).toBe(false);

    const held = renderTelescopeObservingHeldCaption({
      doorUrl: door,
      hasFilm: true,
    });
    expect(held.status).toBe("held");
    expect(held.approvedForPublish).toBe(false);
    expect(held.caption).toContain(FIXTURE_TELESCOPE_OBSERVING_HELD.wonder);
    expect(containsRawMerchantUrl(held.caption)).toBe(false);
    expect(held.caption.toLowerCase()).not.toContain("lego");
    expect(held.caption.toLowerCase()).not.toContain("shop now");
  });

  it("JWST topic map leaves telescope and LEGO empty", () => {
    const plan = CREATOR_TOPIC_SLOT_PLANS.find((p) => p.topicKey === "jwst")!;
    expect(plan.primary).toBe("books");
    expect(plan.leaveEmpty).toEqual(
      expect.arrayContaining(["telescope", "lego"]),
    );
    expect(familyForbiddenForPlan("telescope", plan)).toBe(true);
    expect(familyForbiddenForPlan("lego", plan)).toBe(true);
    expect(familyForbiddenForPlan("books", plan)).toBe(false);
  });
});

describe("film → topic-book wiring (Social Media Manager)", () => {
  it("resolves each film by YouTube id or title to exactly one book", () => {
    expect(
      resolveTopicBookWireForVideo({ youtubeVideoId: "b8-X_FyJnHM" })?.productSlug,
    ).toBe("exoplanet-book");
    expect(
      resolveTopicBookWireForVideo({ youtubeVideoId: "3xrxdmaOwJI" })?.productSlug,
    ).toBe("black-hole-book");
    expect(
      resolveTopicBookWireForVideo({ youtubeVideoId: "n7CbJrOCnU0" })?.productSlug,
    ).toBe("black-hole-book");
    expect(
      resolveTopicBookWireForVideo({ youtubeVideoId: "Mo93x0fxB1Q" })?.productSlug,
    ).toBe("fermi-paradox-book");
    expect(
      resolveTopicBookWireForVideo({
        title: "What the James Webb Telescope Discovered That Changes Everything",
      })?.productSlug,
    ).toBe("jwst-book");
    expect(
      resolveTopicBookWireForVideo({
        title: "The End of the Universe (Astrophysically Speaking)",
      })?.productSlug,
    ).toBe("cosmology-end-book");
    expect(
      resolveTopicBookWireForVideo({
        title: "Europa and the Ocean Worlds Under the Ice",
      })?.productSlug,
    ).toBe("europa-icy-moons-book");
  });

  it("trust gate treats wired desk book as named; telescope still fails", () => {
    const video = {
      title: "What Happens If You Fall Into a Black Hole?",
      topic: "Black Holes",
      primaryKeyword: "black hole",
      youtubeVideoId: "3xrxdmaOwJI",
    };
    const book = product({
      id: "bh",
      name: "A Brief History of Black Holes",
      slug: "black-hole-book",
      category: "Space books",
      tagSlugs: ["books", "black-hole"],
    });
    const scope = product({
      id: "scope",
      name: "Beginner telescope",
      slug: "beginner-telescope",
      category: "Beginner telescopes",
      tagSlugs: ["telescope", "beginner"],
    });
    expect(evaluateEditorialTrustGate(video, book).pass).toBe(true);
    expect(evaluateEditorialTrustGate(video, scope).pass).toBe(false);
  });

  it("builds Creator description with one /go link and disclosure last; no telescope/Brilliant/LEGO", () => {
    const rows = filmTopicBookPlacementTableRows();
    expect(rows.length).toBe(6);
    for (const row of rows) {
      expect(row.amazonUrl).toMatch(/amazon\.co\.uk\/.*\/dp\//i);
      expect(row.goPath).toBe(`/go/${row.productSlug}`);
      expect(JSON.stringify(row)).not.toContain("orbitgo-21");
    }

    const bookLink = {
      productName: "A Brief History of Black Holes",
      productSlug: "black-hole-book",
      category: "Space books",
      programSlug: "amazon-associates-uk",
      url: "https://orbitwithben.com/go/black-hole-book",
      role: "primary" as const,
      trustProduct: product({
        id: "bh-book",
        name: "A Brief History of Black Holes",
        slug: "black-hole-book",
        category: "Space books",
        tagSlugs: ["books", "black-hole"],
      }),
    };
    const section = buildAffiliateDescriptionSection({
      links: [bookLink],
      topicKey: "black-holes",
    });
    expect(section).toContain("/go/black-hole-book");
    expect(section).not.toContain("beginner-telescope");
    expect(section.toLowerCase()).not.toContain("brilliant");
    expect(section.toLowerCase()).not.toContain("lego");
    expect(section.trim().endsWith(CREATOR_AFFILIATE_DISCLOSURE)).toBe(true);

    const base = [
      "What Happens If You Fall Into a Black Hole?",
      "",
      "Chapters",
      "0:00 Cold open",
      "",
      "Subscribe for the next film.",
      "",
      "Playlist",
      "More Orbit",
      "",
      "#OrbitWithBen",
    ].join("\n");
    const desc = appendAffiliateSectionToDescription({
      description: base,
      links: [bookLink],
      trustVideo: {
        title: "What Happens If You Fall Into a Black Hole?",
        topic: "Black Holes",
        primaryKeyword: "black hole",
        youtubeVideoId: "3xrxdmaOwJI",
      },
    });
    expect(desc.indexOf("Subscribe for the next film")).toBeLessThan(
      desc.indexOf("/go/"),
    );
    expect(desc.indexOf("/go/")).toBeLessThan(desc.indexOf("Playlist"));
    expect(desc.match(/\/go\/[a-z0-9-]+/g)?.length).toBe(1);

    const shortDesc = appendAffiliateSectionToDescription({
      description: "Short CTA only",
      links: [bookLink],
      trustVideo: {
        title: "Black Hole Short",
        topic: "Black Holes",
        isShort: true,
      },
    });
    expect(shortDesc).toBe("Short CTA only");
    expect(shortDesc).not.toContain("/go/");
  });

  it("placement table lists film title, youtube id, slug, amazon URL, go path", () => {
    const bySlug = Object.fromEntries(
      filmTopicBookPlacementTableRows().map((r) => [r.productSlug, r]),
    );
    expect(bySlug["exoplanet-book"].youtubeId).toBe("b8-X_FyJnHM");
    expect(bySlug["black-hole-book"].youtubeId).toBe("3xrxdmaOwJI");
    expect(bySlug["fermi-paradox-book"].youtubeId).toBe("Mo93x0fxB1Q");
    expect(bySlug["jwst-book"].youtubeId).toContain("scheduled");
    expect(bySlug["cosmology-end-book"].amazonUrl).toContain("0141989580");
    expect(bySlug["europa-icy-moons-book"].goPath).toBe("/go/europa-icy-moons-book");
  });
});
