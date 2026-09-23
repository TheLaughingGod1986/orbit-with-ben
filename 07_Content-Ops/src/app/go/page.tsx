import type { Metadata } from "next";
import Link from "next/link";
import { prisma } from "@/lib/storage/prisma";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Orbit recommendations — tracked affiliate links",
  description:
    "Public recommendation door for Orbit with Ben. Educational space and astronomy books and tools named in the films, with clear affiliate disclosure.",
  robots: { index: true, follow: true },
  openGraph: {
    title: "Orbit with Ben — recommendations",
    description:
      "Space and astronomy recommendations from the Orbit with Ben YouTube channel. Tracked /go/{slug} links with affiliate disclosure.",
    url: "https://orbit-content-ops.vercel.app/go",
    type: "website",
  },
};

/** Fallback catalogue when the DB is unavailable — still real crawlable HTML. */
const FALLBACK_RECOMMENDATIONS: Array<{
  slug: string;
  name: string;
  blurb: string;
}> = [
  {
    slug: "jwst-book",
    name: "Webb’s Universe (Maggie Aderin-Pocock)",
    blurb:
      "A guided look at JWST images and what they mean — named when the film is about the telescope.",
  },
  {
    slug: "fermi-paradox-book",
    name: "Where Is Everybody? (Stephen Webb)",
    blurb:
      "A careful tour of Fermi paradox solutions — for the film that asks why we have not found aliens yet.",
  },
  {
    slug: "black-hole-book",
    name: "A Brief History of Black Holes (Becky Smethurst)",
    blurb: "Readable black-hole physics for the fall-into-a-black-hole film.",
  },
  {
    slug: "cosmology-end-book",
    name: "The End of Everything (Katie Mack)",
    blurb: "How the universe might end — for the Last Star / end-of-universe film.",
  },
  {
    slug: "exoplanet-book",
    name: "The Planet Factory (Elizabeth Tasker)",
    blurb: "How strange worlds form — for Alien Worlds and exoplanet explainers.",
  },
  {
    slug: "europa-icy-moons-book",
    name: "Alien Oceans (Kevin Hand)",
    blurb: "Icy moons and subsurface oceans — for Europa week.",
  },
];

async function loadRecommendations(): Promise<
  Array<{ slug: string; name: string; blurb: string }>
> {
  try {
    const products = await prisma.affiliateProduct.findMany({
      where: {
        active: true,
        affiliateProgram: { status: "ACTIVE", slug: "amazon-associates-uk" },
      },
      select: {
        slug: true,
        name: true,
        description: true,
        category: true,
      },
      orderBy: [{ featured: "desc" }, { priority: "desc" }, { name: "asc" }],
      take: 24,
    });
    if (products.length === 0) return FALLBACK_RECOMMENDATIONS;
    return products.map((p) => ({
      slug: p.slug,
      name: p.name,
      blurb:
        (p.description && p.description.trim()) ||
        `${p.category} recommendation from Orbit with Ben films.`,
    }));
  } catch {
    return FALLBACK_RECOMMENDATIONS;
  }
}

export default async function GoLandingPage() {
  const recommendations = await loadRecommendations();

  return (
    <div className="space-y-8">
      <section className="relative overflow-hidden rounded-3xl border border-white/5 bg-[#0d1018]/70 p-8 md:p-10">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(255,122,36,0.2),transparent_40%)]" />
        <p className="text-xs uppercase tracking-[0.28em] text-[#FF7A24]">
          Orbit with Ben
        </p>
        <h1 className="mt-3 max-w-3xl font-[family-name:var(--font-orbit-display)] text-4xl leading-tight text-[#F5E8D2] md:text-5xl">
          Recommendations from the films
        </h1>
        <p className="mt-4 max-w-2xl text-[#F5E8D2]/70">
          This is the public affiliate door for{" "}
          <strong className="font-medium text-[#F5E8D2]">Orbit with Ben</strong> — a
          YouTube channel about space, astronomy, and cosmic scale. When a long-form film
          names a book or tool on screen or in the narration, we may leave one tracked
          link here so curious viewers can go further.
        </p>
        <p className="mt-3 max-w-2xl text-sm text-[#F5E8D2]/55">
          Site:{" "}
          <a
            className="text-[#FFC85A] hover:underline"
            href="https://orbit-content-ops.vercel.app/go"
          >
            https://orbit-content-ops.vercel.app/go
          </a>
          . Channel:{" "}
          <a
            className="text-[#FFC85A] hover:underline"
            href="https://www.youtube.com/@OrbitWithBen"
            rel="noopener noreferrer"
            target="_blank"
          >
            youtube.com/@OrbitWithBen
          </a>
          .
        </p>
      </section>

      <section className="card-panel space-y-4 p-6 md:p-8">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
          What this site is
        </h2>
        <p className="text-[#F5E8D2]/75">
          Orbit Content Ops hosts educational content operations for the channel and the
          public <code className="text-[#FFC85A]">/go</code> recommendation links used in
          YouTube descriptions. We recommend space books and learning tools only when they
          belong in that film — relevance before commission.
        </p>
        <ul className="list-disc space-y-2 pl-5 text-[#F5E8D2]/75">
          <li>
            <strong className="text-[#F5E8D2]">Named in the film</strong> — a product only
            appears when it is spoken or shown in that cut.
          </li>
          <li>
            <strong className="text-[#F5E8D2]">One primary link</strong> on a long-form
            documentary; Shorts carry no affiliate links.
          </li>
          <li>
            <strong className="text-[#F5E8D2]">Tracked doors</strong> use paths like{" "}
            <code className="text-[#FFC85A]">/go/jwst-book</code> — each slug records a
            click, then redirects to the merchant product page.
          </li>
        </ul>
      </section>

      <section className="card-panel space-y-5 p-6 md:p-8">
        <div>
          <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
            Featured recommendations
          </h2>
          <p className="mt-2 text-sm text-[#F5E8D2]/55">
            Open a tracked link to visit the retailer. These are editorial picks tied to
            Orbit films — not a shop catalogue.
          </p>
        </div>
        <ul className="grid gap-4 sm:grid-cols-2">
          {recommendations.map((item) => (
            <li
              key={item.slug}
              className="rounded-2xl border border-white/5 bg-[#0a0c12]/50 p-5"
            >
              <h3 className="font-[family-name:var(--font-orbit-display)] text-lg text-[#F5E8D2]">
                {item.name}
              </h3>
              <p className="mt-2 text-sm text-[#F5E8D2]/65">{item.blurb}</p>
              <p className="mt-3 text-sm">
                <Link
                  href={`/go/${item.slug}`}
                  className="font-medium text-[#FF7A24] hover:underline"
                >
                  Open tracked link → /go/{item.slug}
                </Link>
              </p>
            </li>
          ))}
        </ul>
      </section>

      <section className="card-panel space-y-3 p-6 md:p-8">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
          How /go links work
        </h2>
        <p className="text-[#F5E8D2]/75">
          This page (<code className="text-[#FFC85A]">/go</code>) is the public landing
          for Amazon Associates and other affiliate programmes. Individual product doors
          live at <code className="text-[#FFC85A]">/go/&#123;slug&#125;</code>. Visiting a
          slug records the click for the channel operator, then issues an HTTP redirect to
          the product on the merchant site (for example Amazon.co.uk). The landing page
          itself is ordinary HTML — not a blank redirect.
        </p>
        <p className="text-sm text-[#F5E8D2]/55">
          Example:{" "}
          <Link href="/go/jwst-book" className="text-[#FFC85A] hover:underline">
            /go/jwst-book
          </Link>
        </p>
      </section>

      <section className="card-panel space-y-3 p-6 md:p-8">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
          Affiliate disclosure
        </h2>
        <p className="text-[#F5E8D2]/75">
          Some of these links are affiliate links. As an Amazon Associate we earn from
          qualifying purchases. We only share things we would still point you to with no
          commission. Prices and availability are set by the retailer.
        </p>
        <p className="text-sm text-[#F5E8D2]/55">
          Questions about a recommendation? Leave a comment on the related Orbit with Ben
          YouTube film, or contact the channel operator via the YouTube channel About
          tab.
        </p>
        <p className="text-sm text-[#F5E8D2]/45">
          Related:{" "}
          <Link href="/legal/privacy" className="text-[#FFC85A] hover:underline">
            Privacy
          </Link>
          {" · "}
          <Link href="/legal/terms" className="text-[#FFC85A] hover:underline">
            Terms
          </Link>
        </p>
      </section>
    </div>
  );
}
