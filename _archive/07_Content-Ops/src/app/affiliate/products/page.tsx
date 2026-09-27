import Link from "next/link";
import { listProducts } from "@/lib/affiliate/products";
import { listPrograms } from "@/lib/affiliate/programs";
import { ProductForm } from "@/components/affiliate/ProductForm";

export const dynamic = "force-dynamic";

export default async function AffiliateProductsPage({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | undefined>>;
}) {
  const sp = await searchParams;
  const [products, programmes] = await Promise.all([
    listProducts({
      programmeId: sp.programmeId,
      category: sp.category,
      active: sp.active === "true" ? true : sp.active === "false" ? false : undefined,
      featured: sp.featured === "true" ? true : undefined,
      evergreen: sp.evergreen === "true" ? true : undefined,
      tag: sp.tag,
      search: sp.q,
    }),
    listPrograms(),
  ]);

  const showForm = sp.new === "1";

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <Link href="/affiliate" className="text-sm text-[#5A6E82] hover:text-[#F5E8D2]">
            ← Affiliate
          </Link>
          <h1 className="mt-2 font-[family-name:var(--font-orbit-display)] text-3xl">
            Products & offers
          </h1>
        </div>
        <Link
          href="/affiliate/products?new=1"
          className="rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12]"
        >
          Add product
        </Link>
      </div>

      <form className="card-panel flex flex-wrap gap-3 p-4 text-sm">
        <input
          name="q"
          defaultValue={sp.q || ""}
          placeholder="Search…"
          className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2"
        />
        <select
          name="programmeId"
          defaultValue={sp.programmeId || ""}
          className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2"
        >
          <option value="">All programmes</option>
          {programmes.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <select
          name="active"
          defaultValue={sp.active || ""}
          className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2"
        >
          <option value="">Active: any</option>
          <option value="true">Active</option>
          <option value="false">Inactive</option>
        </select>
        <label className="flex items-center gap-2 px-2">
          <input type="checkbox" name="featured" value="true" defaultChecked={sp.featured === "true"} />
          Featured
        </label>
        <label className="flex items-center gap-2 px-2">
          <input type="checkbox" name="evergreen" value="true" defaultChecked={sp.evergreen === "true"} />
          Evergreen
        </label>
        <button type="submit" className="rounded-full border border-white/15 px-4 py-2">
          Filter
        </button>
      </form>

      {showForm ? <ProductForm programmes={programmes} /> : null}

      <div className="overflow-x-auto rounded-2xl border border-white/5">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-white/3 text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
            <tr>
              <th className="px-4 py-3">Product</th>
              <th className="px-4 py-3">Programme</th>
              <th className="px-4 py-3">Category</th>
              <th className="px-4 py-3">Tags</th>
              <th className="px-4 py-3">Flags</th>
              <th className="px-4 py-3">Health</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id} className="border-t border-white/5 text-[#F5E8D2]/8">
                <td className="px-4 py-3">
                  <div className="text-[#F5E8D2]">{p.name}</div>
                  <div className="text-xs text-[#5A6E82]">{p.slug}</div>
                </td>
                <td className="px-4 py-3">{p.affiliateProgram.name}</td>
                <td className="px-4 py-3">{p.category}</td>
                <td className="px-4 py-3 text-xs">
                  {p.tags.map((t) => t.tag.slug).join(", ") || "—"}
                </td>
                <td className="px-4 py-3 text-xs">
                  {[
                    p.active ? "active" : "off",
                    p.featured ? "featured" : null,
                    p.evergreen ? "evergreen" : null,
                  ]
                    .filter(Boolean)
                    .join(" · ")}
                </td>
                <td className="px-4 py-3 text-xs">{p.urlHealthStatus}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
