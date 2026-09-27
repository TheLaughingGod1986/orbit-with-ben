import { NextRequest, NextResponse } from "next/server";
import { listProducts, createProduct, updateProduct } from "@/lib/affiliate/products";
import { affiliateProductInputSchema } from "@/lib/affiliate/schemas";
import { prisma } from "@/lib/storage/prisma";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  const sp = request.nextUrl.searchParams;
  const products = await listProducts({
    programmeId: sp.get("programmeId") || undefined,
    category: sp.get("category") || undefined,
    active: sp.has("active") ? sp.get("active") === "true" : undefined,
    featured: sp.has("featured") ? sp.get("featured") === "true" : undefined,
    evergreen: sp.has("evergreen") ? sp.get("evergreen") === "true" : undefined,
    tag: sp.get("tag") || undefined,
    search: sp.get("q") || undefined,
  });
  return NextResponse.json({ products });
}

export async function POST(request: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const body = await request.json();
  const parsed = affiliateProductInputSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const product = await createProduct(parsed.data);
  return NextResponse.json({ product }, { status: 201 });
}

export async function PATCH(request: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const body = await request.json();
  if (!body.id || typeof body.id !== "string") {
    return NextResponse.json({ error: "id required" }, { status: 400 });
  }
  const existing = await prisma.affiliateProduct.findUnique({ where: { id: body.id } });
  if (!existing) return NextResponse.json({ error: "Not found" }, { status: 404 });
  const { id, ...rest } = body;
  const product = await updateProduct(id, rest);
  return NextResponse.json({ product });
}
