"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export function ProductForm({
  programmes,
  initial,
}: {
  programmes: Array<{ id: string; name: string; slug: string }>;
  initial?: {
    id: string;
    affiliateProgramId: string;
    name: string;
    slug: string;
    description: string | null;
    destinationUrl: string;
    affiliateUrl: string;
    category: string;
    subcategory: string | null;
    price: number | null;
    currency: string;
    estimatedCommission: number | null;
    active: boolean;
    featured: boolean;
    priority: number;
    evergreen: boolean;
    notes: string | null;
    tagSlugs: string[];
  };
}) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    const fd = new FormData(e.currentTarget);
    const tagSlugs = String(fd.get("tags") || "")
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);

    const payload = {
      id: initial?.id,
      affiliateProgramId: String(fd.get("affiliateProgramId")),
      name: String(fd.get("name")),
      slug: String(fd.get("slug")),
      description: String(fd.get("description") || "") || null,
      destinationUrl: String(fd.get("destinationUrl")),
      affiliateUrl: String(fd.get("affiliateUrl")),
      category: String(fd.get("category")),
      subcategory: String(fd.get("subcategory") || "") || null,
      price: fd.get("price") ? Number(fd.get("price")) : null,
      currency: String(fd.get("currency") || "GBP"),
      estimatedCommission: fd.get("estimatedCommission")
        ? Number(fd.get("estimatedCommission"))
        : null,
      active: fd.get("active") === "on",
      featured: fd.get("featured") === "on",
      priority: Number(fd.get("priority") || 0),
      evergreen: fd.get("evergreen") === "on",
      notes: String(fd.get("notes") || "") || null,
      tagSlugs,
    };

    const res = await fetch("/api/affiliate/products", {
      method: initial ? "PATCH" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setSaving(false);
    if (!res.ok) {
      setError(typeof data.error === "string" ? data.error : "Save failed");
      return;
    }
    router.push("/affiliate/products");
    router.refresh();
  }

  const field =
    "w-full rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2 text-sm text-[#F5E8D2]";

  return (
    <form onSubmit={onSubmit} className="card-panel space-y-4 p-5">
      <div className="grid gap-4 md:grid-cols-2">
        <label className="space-y-1 text-sm">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Programme</span>
          <select
            name="affiliateProgramId"
            defaultValue={initial?.affiliateProgramId || programmes[0]?.id}
            className={field}
            required
          >
            {programmes.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </label>
        <label className="space-y-1 text-sm">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Name</span>
          <input name="name" defaultValue={initial?.name} className={field} required />
        </label>
        <label className="space-y-1 text-sm">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Slug</span>
          <input name="slug" defaultValue={initial?.slug} className={field} required />
        </label>
        <label className="space-y-1 text-sm">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Category</span>
          <input name="category" defaultValue={initial?.category} className={field} required />
        </label>
        <label className="space-y-1 text-sm md:col-span-2">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
            Destination URL
          </span>
          <input
            name="destinationUrl"
            defaultValue={initial?.destinationUrl}
            className={field}
            required
          />
        </label>
        <label className="space-y-1 text-sm md:col-span-2">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Affiliate URL</span>
          <input
            name="affiliateUrl"
            defaultValue={initial?.affiliateUrl}
            className={field}
            required
          />
        </label>
        <label className="space-y-1 text-sm md:col-span-2">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Description</span>
          <textarea
            name="description"
            defaultValue={initial?.description || ""}
            rows={3}
            className={field}
          />
        </label>
        <label className="space-y-1 text-sm">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Price</span>
          <input
            name="price"
            type="number"
            step="0.01"
            defaultValue={initial?.price ?? ""}
            className={field}
          />
        </label>
        <label className="space-y-1 text-sm">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
            Est. commission (£)
          </span>
          <input
            name="estimatedCommission"
            type="number"
            step="0.01"
            defaultValue={initial?.estimatedCommission ?? ""}
            className={field}
          />
        </label>
        <label className="space-y-1 text-sm">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Priority</span>
          <input
            name="priority"
            type="number"
            defaultValue={initial?.priority ?? 0}
            className={field}
          />
        </label>
        <label className="space-y-1 text-sm">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
            Tags (comma-separated)
          </span>
          <input
            name="tags"
            defaultValue={initial?.tagSlugs.join(", ") || ""}
            className={field}
            placeholder="black-hole, physics, beginner"
          />
        </label>
        <label className="space-y-1 text-sm md:col-span-2">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Notes</span>
          <textarea name="notes" defaultValue={initial?.notes || ""} rows={2} className={field} />
        </label>
      </div>
      <div className="flex flex-wrap gap-4 text-sm">
        <label className="flex items-center gap-2">
          <input name="active" type="checkbox" defaultChecked={initial?.active ?? true} /> Active
        </label>
        <label className="flex items-center gap-2">
          <input name="featured" type="checkbox" defaultChecked={initial?.featured ?? false} />{" "}
          Featured
        </label>
        <label className="flex items-center gap-2">
          <input name="evergreen" type="checkbox" defaultChecked={initial?.evergreen ?? false} />{" "}
          Evergreen
        </label>
        <input type="hidden" name="currency" value={initial?.currency || "GBP"} />
        <input type="hidden" name="subcategory" value={initial?.subcategory || ""} />
      </div>
      {error ? <p className="text-sm text-red-400">{error}</p> : null}
      <button
        type="submit"
        disabled={saving}
        className="rounded-full bg-[#FF7A24] px-5 py-2 text-sm text-[#0A0C12] disabled:opacity-50"
      >
        {saving ? "Saving…" : initial ? "Update product" : "Add product"}
      </button>
    </form>
  );
}
