import { prisma } from "@/lib/storage/prisma";
import { buildOrbitRedirectUrl } from "./urls";

/**
 * Phase 5 prep — SEO-ready gear catalogue shape for orbitwithben.com/gear.
 * Backend-ready now; does not build the public marketing site.
 */
export type GearProductDto = {
  slug: string;
  name: string;
  description: string | null;
  category: string;
  subcategory: string | null;
  price: number | null;
  currency: string;
  imageUrl: string | null;
  programme: string;
  programmeSlug: string;
  tags: string[];
  featured: boolean;
  evergreen: boolean;
  goUrl: string;
  destinationUrl: string;
};

export type GearCategoryDto = {
  category: string;
  productCount: number;
  products: GearProductDto[];
};

export async function getGearCatalog(opts?: {
  category?: string;
  tag?: string;
  featuredOnly?: boolean;
}): Promise<{
  generatedAt: string;
  categories: GearCategoryDto[];
  products: GearProductDto[];
}> {
  const products = await prisma.affiliateProduct.findMany({
    where: {
      active: true,
      affiliateProgram: { status: "ACTIVE" },
      category: opts?.category || undefined,
      featured: opts?.featuredOnly ? true : undefined,
      tags: opts?.tag ? { some: { tag: { slug: opts.tag } } } : undefined,
    },
    include: {
      affiliateProgram: true,
      tags: { include: { tag: true } },
    },
    orderBy: [{ featured: "desc" }, { priority: "desc" }, { name: "asc" }],
  });

  const dtos: GearProductDto[] = products.map((p) => ({
    slug: p.slug,
    name: p.name,
    description: p.description,
    category: p.category,
    subcategory: p.subcategory,
    price: p.price,
    currency: p.currency,
    imageUrl: p.imageUrl,
    programme: p.affiliateProgram.name,
    programmeSlug: p.affiliateProgram.slug,
    tags: p.tags.map((t) => t.tag.slug),
    featured: p.featured,
    evergreen: p.evergreen,
    goUrl: buildOrbitRedirectUrl(p.slug),
    destinationUrl: p.destinationUrl,
  }));

  const byCategory = new Map<string, GearProductDto[]>();
  for (const p of dtos) {
    const list = byCategory.get(p.category) || [];
    list.push(p);
    byCategory.set(p.category, list);
  }

  const categories: GearCategoryDto[] = [...byCategory.entries()]
    .map(([category, list]) => ({
      category,
      productCount: list.length,
      products: list,
    }))
    .sort((a, b) => a.category.localeCompare(b.category));

  return {
    generatedAt: new Date().toISOString(),
    categories,
    products: dtos,
  };
}
