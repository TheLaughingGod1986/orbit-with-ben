import { PrismaClient } from "@prisma/client";
import fs from "fs";
import path from "path";
import { ALL_PLATFORM_IDS, CHANNEL_NAME, PLATFORMS } from "../src/config/platforms";
import { CONTENT_RULES } from "../src/config/content-rules";
import { scoreClipQuality } from "../src/lib/content/quality-score";
import { generatePlatformCopy } from "../src/lib/platforms/generate-platform-copy";
import { scheduleClipAcrossPlatforms, londonDateTime } from "../src/lib/publishing/schedule";
import { liveUrlForSlug } from "../src/lib/affiliate/live-product-urls";

const prisma = new PrismaClient();

const SCRIPT_CANDIDATES = [
  path.resolve(
    __dirname,
    "../../02_Video-Projects/001_Will-We-Ever-Meet-Aliens/01_Script/aliens_script_master_v01.md",
  ),
  path.resolve(
    __dirname,
    "../../02_Video-Projects/001_Will-We-Ever-Meet-Aliens/01_Script/aliens_script_v01.md",
  ),
];

function loadScript(): string {
  for (const p of SCRIPT_CANDIDATES) {
    if (fs.existsSync(p)) return fs.readFileSync(p, "utf8");
  }
  return `Will We Ever Meet Aliens?\n\nWhere is everybody?\nThe Great Filter may explain the silence.\nSignals travel slowly across light-years.\nFirst contact may arrive as data, not a landing.`;
}

async function main() {
  await prisma.performanceMetric.deleteMany();
  await prisma.publishingAttempt.deleteMany();
  await prisma.publishingJob.deleteMany();
  await prisma.platformPost.deleteMany();
  await prisma.shortClip.deleteMany();

  // Affiliate FKs → LongFormVideo / products — clear before videos
  await prisma.affiliateClick.deleteMany();
  await prisma.affiliateConversion.deleteMany();
  await prisma.affiliatePlacement.deleteMany();
  await prisma.affiliateUrlHealthCheck.deleteMany();
  await prisma.affiliateProductTag.deleteMany();
  await prisma.affiliateProduct.deleteMany();
  await prisma.affiliateTag.deleteMany();
  await prisma.affiliateDescriptionTemplate.deleteMany();
  await prisma.affiliateImportBatch.deleteMany();
  await prisma.affiliateProgram.deleteMany();

  await prisma.longFormVideo.deleteMany();
  await prisma.contentInsight.deleteMany();
  await prisma.platformSettings.deleteMany();
  await prisma.contentTemplate.deleteMany();
  await prisma.analyticsImport.deleteMany();

  await prisma.appSetting.upsert({
    where: { key: "publishing_mode" },
    create: { key: "publishing_mode", value: "approve_each_post" },
    update: { value: "approve_each_post" },
  });
  await prisma.appSetting.upsert({
    where: { key: "publishing_defaults_privacy" },
    create: { key: "publishing_defaults_privacy", value: "private" },
    update: {},
  });

  const script = loadScript();
  const youtubeUrl = "https://youtu.be/Mo93x0fxB1Q";

  const video = await prisma.longFormVideo.create({
    data: {
      title: "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained",
      workingTitle: "Will We Ever Meet Aliens?",
      slug: "2026-08-will-we-ever-meet-aliens",
      topic: "Alien Civilisations",
      category: "Space Documentary",
      status: "published",
      script,
      summary:
        "A calm look at the Fermi Paradox, cosmic distances, the Great Filter, and what first contact might actually look like.",
      youtubeUrl,
      youtubeVideoId: "Mo93x0fxB1Q",
      finalVideoPath:
        "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/09_Final-Export",
      projectFolder: "02_Video-Projects/001_Will-We-Ever-Meet-Aliens",
      durationSeconds: 540,
      publicationDate: londonDateTime("2026-08-07", "19:00"),
      primaryKeyword: "fermi paradox explained",
      secondaryKeywords: JSON.stringify([
        "are we alone",
        "great filter",
        "alien contact",
      ]),
      targetAudience: "Curious learners who enjoy calm science storytelling",
    },
  });

  const clipSeeds = [
    {
      clipNumber: 1,
      workingTitle: "The Great Filter",
      hook: "The universe may be hiding something from us.",
      hookCategory: "mystery",
      transcript:
        "Some thinkers call this kind of barrier a Great Filter — a stage so difficult that almost no civilisation crosses it. We do not know if that filter is behind us… or still ahead.",
      sourceStartTime: "03:20",
      sourceEndTime: "04:00",
      targetDurationSeconds: 40,
      visualDirection: "Cosmic timeline + Orbit thoughtful PiP",
      onScreenText: "The Great Filter?",
      endingLine: "We do not know if that filter is behind us — or still ahead.",
      status: "approved",
    },
    {
      clipNumber: 2,
      workingTitle: "Why the Universe Seems Silent",
      hook: "If the universe should be full of life… why is it so quiet?",
      hookCategory: "direct_question",
      transcript:
        "If alien civilisations are common… where are they? No radio greetings. No obvious megastructures. Just silence — or at least, silence as far as we can tell.",
      sourceStartTime: "01:40",
      sourceEndTime: "02:25",
      targetDurationSeconds: 45,
      visualDirection: "Quiet starfield, telescope arrays, Orbit reaction",
      onScreenText: "Where is everybody?",
      endingLine: "That silence has inspired dozens of explanations — most incomplete.",
      status: "editing",
    },
    {
      clipNumber: 3,
      workingTitle: "How Far an Alien Signal Could Travel",
      hook: "This is why we may never reach another star.",
      hookCategory: "scale_comparison",
      transcript:
        "Our nearest star system, Alpha Centauri, is about four light-years away. Light itself takes four years to cross that gap. Our fastest spacecraft would need tens of thousands of years.",
      sourceStartTime: "00:50",
      sourceEndTime: "01:35",
      targetDurationSeconds: 38,
      visualDirection: "Distance scale Earth to Alpha Centauri",
      onScreenText: "4 light-years",
      endingLine: "And that is the close one.",
      status: "exported",
    },
    {
      clipNumber: 4,
      workingTitle: "What First Contact Might Actually Look Like",
      hook: "First contact may not look how you imagine.",
      hookCategory: "scientific_reveal",
      transcript:
        "Meeting may not mean a handshake. It might mean a radio whisper, a chemical imbalance in an atmosphere, or a pattern we finally learn how to read.",
      sourceStartTime: "06:10",
      sourceEndTime: "06:55",
      targetDurationSeconds: 42,
      visualDirection: "Biosignature spectrum + archive motif",
      onScreenText: "Not a landing",
      endingLine: "The first hello may already be waiting in the data.",
      status: "proposed",
    },
  ];

  const shortSlots = [
    londonDateTime("2026-08-07", "21:00"),
    londonDateTime("2026-08-08", "12:30"),
    londonDateTime("2026-08-09", "12:30"),
    londonDateTime("2026-08-10", "12:30"),
  ];

  for (const [i, seed] of clipSeeds.entries()) {
    const quality = scoreClipQuality({
      ...seed,
      callToAction: CONTENT_RULES.softCtas[0],
      whyItWorks: seed.workingTitle,
    });
    const clip = await prisma.shortClip.create({
      data: {
        longFormVideoId: video.id,
        clipNumber: seed.clipNumber,
        workingTitle: seed.workingTitle,
        hook: seed.hook,
        hookCategory: seed.hookCategory,
        transcript: seed.transcript,
        sourceStartTime: seed.sourceStartTime,
        sourceEndTime: seed.sourceEndTime,
        targetDurationSeconds: seed.targetDurationSeconds,
        visualDirection: seed.visualDirection,
        onScreenText: seed.onScreenText,
        endingLine: seed.endingLine,
        callToAction: CONTENT_RULES.softCtas[0],
        status: seed.status,
        qualityScore: quality.total,
        qualityBreakdown: JSON.stringify(quality),
        sortOrder: seed.clipNumber,
      },
    });

    const copies = generatePlatformCopy({
      shortTitle: seed.workingTitle,
      hook: seed.hook,
      topic: video.topic,
      transcript: seed.transcript,
      youtubeUrl,
      longTitle: video.title,
      callToAction: CONTENT_RULES.softCtas[0],
    });

    const schedule = scheduleClipAcrossPlatforms({
      youtubeShortAt: shortSlots[i],
      includeTextPlatforms: seed.clipNumber <= 3,
    });

    for (const copy of copies) {
      if (copy.platform === "x" && seed.clipNumber > 3) continue;
      if (copy.platform === "threads" && seed.clipNumber > 2) continue;

      const slot = schedule.find((s) => s.platform === copy.platform);
      await prisma.platformPost.create({
        data: {
          shortClipId: clip.id,
          platform: copy.platform,
          title: copy.title,
          caption: copy.caption,
          hashtags: JSON.stringify(copy.hashtags),
          callToAction: copy.callToAction,
          scheduledAt: slot?.scheduledAt,
          uploadStatus:
            seed.status === "exported" && copy.platform === "youtube_shorts"
              ? "ready"
              : seed.status === "proposed"
                ? "draft"
                : "ready",
          publishingMethod: "manual",
          pinnedComment: copy.pinnedComment,
          coverText: copy.coverText,
          storyCaption: copy.storyCaption,
          commentPrompt: copy.commentPrompt,
          notes: "Placeholder — not published. Record URL after manual upload.",
          platformUrl: null,
          platformPostId: null,
        },
      });
    }
  }

  for (const id of ALL_PLATFORM_IDS) {
    await prisma.platformSettings.create({
      data: {
        platform: id,
        enabled: true,
        accountDisplayName: CHANNEL_NAME,
        profileUrl:
          id === "youtube_shorts"
            ? "https://www.youtube.com/@OrbitWithBen"
            : null,
        defaultHashtags: JSON.stringify(["OrbitWithBen", "Space", "Astronomy"]),
        defaultCallToAction: CONTENT_RULES.softCtas[0],
        publishingMethod: "manual",
        connectionStatus: PLATFORMS[id].connectionStatus,
        tokenStatus: "not_configured",
        defaultVisibility: "public",
        analyticsImportNotes: `Use sample CSV templates in content/samples/csv for ${id}`,
      },
    });
  }

  const templates: { key: string; name: string; platform?: string; body: string }[] = [
    {
      key: "youtube_shorts_title",
      name: "YouTube Shorts title",
      platform: "youtube_shorts",
      body: "{{hook}}",
    },
    {
      key: "tiktok_caption",
      name: "TikTok caption",
      platform: "tiktok",
      body: "{{hook}}\n\n{{call_to_action}}\n\n#OrbitWithBen #Space",
    },
    {
      key: "instagram_reel_caption",
      name: "Instagram Reel caption",
      platform: "instagram_reels",
      body: "{{hook}}\n\n{{call_to_action}}\n\nSave this if you love big questions.",
    },
    {
      key: "facebook_reel_caption",
      name: "Facebook Reel caption",
      platform: "facebook_reels",
      body: "{{hook}}\n\nWhat do you think?\n\n{{youtube_url}}",
    },
    {
      key: "x_post",
      name: "X post",
      platform: "x",
      body: "{{hook}} {{youtube_url}}",
    },
    {
      key: "threads_post",
      name: "Threads post",
      platform: "threads",
      body: "{{hook}}\n\nFull documentary on YouTube — {{channel_name}}.",
    },
    {
      key: "youtube_pinned_comment",
      name: "Pinned YouTube comment",
      platform: "youtube_shorts",
      body: "Full documentary: {{youtube_url}}",
    },
    {
      key: "instagram_story",
      name: "Instagram Story text",
      platform: "instagram_reels",
      body: "{{hook}} — full film on YouTube.",
    },
    {
      key: "upload_checklist",
      name: "Upload checklist",
      body: "Upload clean vertical MP4 for {{short_title}} ({{topic}}). Never reuse watermarked downloads.",
    },
  ];

  for (const t of templates) {
    await prisma.contentTemplate.create({ data: t });
  }

  await prisma.contentInsight.create({
    data: {
      type: "system",
      finding:
        "More performance data is needed before this recommendation is reliable.",
      evidence: "Seed database has no imported metrics yet.",
      confidence: 0,
      recommendedAction: "Import CSV analytics after the first Shorts week.",
      sampleSize: 0,
    },
  });

  await seedAffiliateCatalog();

  console.log("Seeded Orbit content ops with Will We Ever Meet Aliens? + 4 clips + affiliate catalogue");
}

async function seedAffiliateCatalog() {
  const amazon = await prisma.affiliateProgram.create({
    data: {
      name: "Amazon Associates UK",
      slug: "amazon-associates-uk",
      description:
        "UK Amazon Associates for telescopes, books, LEGO, and astronomy accessories. Tag from AMAZON_ASSOCIATE_TAG.",
      website: "https://affiliate-program.amazon.co.uk/",
      network: "Amazon",
      defaultCommissionType: "PERCENTAGE",
      defaultCommissionValue: 3,
      cookieDurationDays: 1,
      status: "ACTIVE",
      affiliateIdEnvKey: "AMAZON_ASSOCIATE_TAG",
      categoriesJson: JSON.stringify([
        "Beginner telescopes",
        "Advanced telescopes",
        "Astronomy books",
        "Space books",
        "Kids’ astronomy books",
        "Binoculars",
        "Star projectors",
        "Astronomy accessories",
        "Astrophotography gear",
        "Space LEGO",
        "Science kits",
        "Models",
        "Space gifts",
      ]),
      disclosureText:
        "As an Amazon Associate I earn from qualifying purchases.",
    },
  });

  const brilliant = await prisma.affiliateProgram.create({
    data: {
      name: "Brilliant",
      slug: "brilliant",
      description:
        "Interactive STEM learning — physics, maths, AI, engineering. ID from BRILLIANT_AFFILIATE_ID.",
      website: "https://brilliant.org/",
      network: "Brilliant",
      defaultCommissionType: "PERCENTAGE",
      defaultCommissionValue: 50,
      cookieDurationDays: 30,
      status: "ACTIVE",
      affiliateIdEnvKey: "BRILLIANT_AFFILIATE_ID",
      categoriesJson: JSON.stringify([
        "Physics",
        "Mathematics",
        "Computer science",
        "AI",
        "Scientific thinking",
        "Engineering",
      ]),
    },
  });

  const retailer = await prisma.affiliateProgram.create({
    data: {
      name: "Astronomy Retailer",
      slug: "astronomy-retailer",
      description:
        "Generic specialist astronomy retailer slot (First Light Optics, High Point Scientific, etc.). Own reporting; higher AOV.",
      website: "https://example.invalid/astronomy-retailer",
      network: "Direct",
      defaultCommissionType: "PERCENTAGE",
      defaultCommissionValue: 5,
      cookieDurationDays: 30,
      status: "ACTIVE",
      categoriesJson: JSON.stringify([
        "Beginner telescopes",
        "Advanced telescopes",
        "Binoculars",
        "Astrophotography gear",
        "Astronomy accessories",
      ]),
    },
  });

  await prisma.affiliateProgram.create({
    data: {
      name: "LEGO",
      slug: "lego",
      description:
        "LEGO Affiliate — Space / NASA / educational sets. May start inactive until programme access is approved.",
      website: "https://www.lego.com/",
      network: "LEGO Affiliate",
      defaultCommissionType: "PERCENTAGE",
      defaultCommissionValue: 5,
      cookieDurationDays: 7,
      status: "INACTIVE",
      categoriesJson: JSON.stringify([
        "Space",
        "NASA",
        "Mars",
        "Moon",
        "Rockets",
        "Spacecraft",
        "Educational sets",
      ]),
    },
  });

  const tagSlugs = [
    "mars",
    "moon",
    "black-hole",
    "telescope",
    "astronomy",
    "astrophotography",
    "spacex",
    "starship",
    "nasa",
    "physics",
    "ai",
    "cosmology",
    "aliens",
    "seti",
    "exoplanets",
    "kids",
    "beginner",
    "books",
    "lego",
    "binoculars",
    "mathematics",
    "engineering",
  ];
  const tagIds: Record<string, string> = {};
  for (const slug of tagSlugs) {
    const tag = await prisma.affiliateTag.create({
      data: {
        slug,
        name: slug
          .split("-")
          .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
          .join(" "),
      },
    });
    tagIds[slug] = tag.id;
  }

  async function addProduct(args: {
    programId: string;
    name: string;
    slug: string;
    description: string;
    category: string;
    tags: string[];
    price: number;
    estimatedCommission: number;
    featured?: boolean;
    evergreen?: boolean;
    priority?: number;
    active?: boolean;
  }) {
    const live = liveUrlForSlug(args.slug);
    const destinationUrl =
      live?.destinationUrl || `https://example.invalid/dest/${args.slug}`;
    const affiliateUrl =
      live?.affiliateUrl ||
      live?.destinationUrl ||
      `https://example.invalid/aff/${args.slug}?ref=PLACEHOLDER`;
    const product = await prisma.affiliateProduct.create({
      data: {
        affiliateProgramId: args.programId,
        name: args.name,
        slug: args.slug,
        description: args.description,
        // Public destination URLs from live-product-urls.ts — programme tags from env at /go
        destinationUrl,
        affiliateUrl,
        category: args.category,
        price: args.price,
        currency: "GBP",
        estimatedCommission: args.estimatedCommission,
        commissionType: "PERCENTAGE",
        active: args.active ?? true,
        featured: args.featured ?? false,
        evergreen: args.evergreen ?? false,
        priority: args.priority ?? 0,
        notes:
          live?.notes ||
          "Seed placeholder — replace with real programme URLs after account approval.",
      },
    });
    for (const t of args.tags) {
      if (!tagIds[t]) continue;
      await prisma.affiliateProductTag.create({
        data: { productId: product.id, tagId: tagIds[t] },
      });
    }
    return product;
  }

  await addProduct({
    programId: retailer.id,
    name: "Beginner telescope",
    slug: "beginner-telescope",
    description: "A practical first telescope for clear nights — Orbit evergreen recommendation.",
    category: "Beginner telescopes",
    tags: ["telescope", "beginner", "astronomy"],
    price: 179,
    estimatedCommission: 9,
    featured: true,
    evergreen: true,
    priority: 5,
  });
  await addProduct({
    programId: amazon.id,
    name: "Astronomy binoculars",
    slug: "astronomy-binoculars",
    description: "Wide-field binoculars for lunar and constellation starts.",
    category: "Binoculars",
    tags: ["binoculars", "beginner", "astronomy", "moon"],
    price: 65,
    estimatedCommission: 2.5,
    evergreen: true,
    priority: 3,
  });
  await addProduct({
    programId: amazon.id,
    name: "Beginner astronomy book",
    slug: "beginner-astronomy-book",
    description: "Calm introductory astronomy reading for curious adults.",
    category: "Astronomy books",
    tags: ["books", "beginner", "astronomy"],
    price: 14.99,
    estimatedCommission: 0.6,
    evergreen: true,
    priority: 2,
  });
  await addProduct({
    programId: brilliant.id,
    name: "Brilliant Physics",
    slug: "brilliant-physics",
    description: "Interactive physics — black holes, relativity, quantum intuition.",
    category: "Physics",
    tags: ["physics", "black-hole", "cosmology", "relativity", "quantum"],
    price: 149,
    estimatedCommission: 40,
    featured: true,
    priority: 8,
  });
  await addProduct({
    programId: brilliant.id,
    name: "Brilliant Mathematics",
    slug: "brilliant-mathematics",
    description: "Maths foundations that unlock orbital mechanics and scientific thinking.",
    category: "Mathematics",
    tags: ["mathematics", "physics", "engineering"],
    price: 149,
    estimatedCommission: 40,
    priority: 4,
  });
  await addProduct({
    programId: amazon.id,
    name: "Mars book",
    slug: "mars-book",
    description: "Deep dive into Mars exploration history and science.",
    category: "Space books",
    tags: ["mars", "nasa", "books"],
    price: 18,
    estimatedCommission: 0.7,
    priority: 2,
  });
  await addProduct({
    programId: amazon.id,
    name: "Space LEGO",
    slug: "space-lego",
    description: "Buildable spacecraft sets for kids and nostalgia adults.",
    category: "Space LEGO",
    tags: ["lego", "kids", "nasa", "spacecraft"],
    price: 49.99,
    estimatedCommission: 1.5,
    priority: 1,
  });
  await addProduct({
    programId: retailer.id,
    name: "Astrophotography starter kit",
    slug: "astrophotography-starter-kit",
    description: "Entry astrophotography mount + guide for deep-sky beginners.",
    category: "Astrophotography gear",
    tags: ["astrophotography", "telescope", "astronomy"],
    price: 399,
    estimatedCommission: 20,
    featured: true,
    priority: 4,
  });

  const templates = [
    {
      key: "section_header",
      name: "Section header",
      category: "general",
      body: "If you want to go further",
    },
    {
      key: "section_header_alt",
      name: "Section header (alternate)",
      category: "general",
      body: "Orbit’s next steps (not a shop)",
    },
    {
      key: "brilliant",
      name: "Brilliant intro",
      category: "brilliant",
      body: "If this film left you wanting the math under the pictures, Brilliant is where I’d send you to practice. Not more videos. A problem you work until it clicks.",
    },
    {
      key: "telescope",
      name: "Telescope intro",
      category: "telescope",
      body: "The objects in this film are not only on a screen. A first telescope is how a lot of people meet Saturn’s rings or the Moon’s craters for real. Start simple. Learn the night. Upgrade later.",
    },
    {
      key: "binoculars",
      name: "Binoculars intro",
      category: "telescope",
      body: "The objects in this film are not only on a screen. Starting under the night sky with binoculars is how a lot of people learn the night before a first telescope.",
    },
    {
      key: "books",
      name: "Books intro",
      category: "books",
      body: "A film can open a question. A good book sits with the uncertainty longer. This is the one I’d keep on the desk after this episode.",
    },
    {
      key: "lego",
      name: "LEGO intro",
      category: "lego",
      body: "Some ideas are easier to hold when you can build them. This set is a small model of a real machine. Useful for kids, and for anyone who thinks with their hands.",
    },
    {
      key: "general",
      name: "General intro",
      category: "general",
      body: "If you want to go further on what this film opened:",
    },
    {
      key: "disclosure",
      name: "Standard disclosure",
      category: "disclosure",
      body: "Some of these links are affiliate links. We only share things we’d still point you to with no commission.",
    },
    {
      key: "amazon_disclosure",
      name: "Amazon disclosure",
      category: "amazon_disclosure",
      body: "As an Amazon Associate I earn from qualifying purchases.",
    },
    {
      key: "books_black_holes",
      name: "Book intro — black holes",
      category: "books",
      body: "How we actually know a black hole is there, without turning it into a horror story.",
    },
    {
      key: "books_mars",
      name: "Book intro — Mars",
      category: "books",
      body: "Mars as a world we can measure, not a poster.",
    },
    {
      key: "books_telescopes",
      name: "Book intro — telescopes",
      category: "books",
      body: "Why a mirror collects light, and what that lets you see from a back garden.",
    },
    {
      key: "books_jwst",
      name: "Book intro — JWST",
      category: "books",
      body: "What Webb changed about cosmic dawn, written at the pace of a desk, not a trailer.",
    },
    {
      key: "books_relativity",
      name: "Book intro — relativity",
      category: "books",
      body: "The part of spacetime you can follow with a pencil.",
    },
    {
      key: "books_kids",
      name: "Book intro — kids",
      category: "books",
      body: "A first book that treats kids as curious, not as a market.",
    },
    {
      key: "books_starship",
      name: "Book intro — Starship",
      category: "books",
      body: "How a rocket actually leaves Earth, without the press-conference fog.",
    },
    {
      key: "books_cosmology",
      name: "Book intro — cosmology",
      category: "books",
      body: "The universe at the largest scale, including the parts we still cannot close.",
    },
    {
      key: "lego_jwst",
      name: "LEGO intro — JWST",
      category: "lego",
      body: "Webb is a real machine. Building a small one is a good way to remember the unfolding mirrors, not just the pictures it sends home.",
    },
    {
      key: "lego_mars",
      name: "LEGO intro — Mars",
      category: "lego",
      body: "A rover you can hold is a decent way to feel how careful a landing has to be.",
    },
    {
      key: "lego_starship",
      name: "LEGO intro — Starship",
      category: "lego",
      body: "A stack of tanks and engines, at a scale you can walk around on a table.",
    },
    {
      key: "lego_kids",
      name: "LEGO intro — kids",
      category: "lego",
      body: "Hubble or Webb as a model, so the “eye in space” is not only a phrase.",
    },
    {
      key: "lego_telescopes",
      name: "LEGO intro — telescopes",
      category: "lego",
      body: "Hubble or Webb as a model, so the “eye in space” is not only a phrase.",
    },
  ];
  for (const t of templates) {
    await prisma.affiliateDescriptionTemplate.create({ data: t });
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
