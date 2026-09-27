"use client";

import { useState } from "react";

export function AnalyticsImportForm() {
  const [platform, setPlatform] = useState("youtube");
  const [csv, setCsv] = useState("");
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  async function previewImport() {
    setResult(null);
    const res = await fetch("/api/analytics/import", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ platform, csv, dryRun: true }),
    });
    const data = await res.json();
    if (!res.ok) {
      setPreview(data.error || "Preview failed");
      return;
    }
    setPreview(
      `Headers: ${data.preview.headers.join(", ")}\nMissing: ${
        data.preview.missing.join(", ") || "none"
      }\nSample rows: ${data.preview.sampleRows.length}`,
    );
  }

  async function runImport() {
    setPreview(null);
    const res = await fetch("/api/analytics/import", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ platform, csv, dryRun: false }),
    });
    const data = await res.json();
    if (!res.ok) {
      setResult(data.error || "Import failed");
      return;
    }
    setResult(
      `Imported ${data.successCount}/${data.rowCount}. Skipped duplicates: ${data.duplicatesSkipped}. Errors: ${data.errors?.length || 0}`,
    );
  }

  return (
    <div className="card-panel space-y-3 p-5">
      <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">CSV import</h2>
      <p className="text-sm text-[#F5E8D2]/55">
        Paste analytics exports. Sample templates live in{" "}
        <code>content/samples/csv/</code>.
      </p>
      <select
        value={platform}
        onChange={(e) => setPlatform(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2 text-sm"
      >
        <option value="youtube">YouTube Analytics</option>
        <option value="tiktok">TikTok Analytics</option>
        <option value="instagram">Instagram Insights</option>
        <option value="facebook">Facebook Insights</option>
      </select>
      <textarea
        value={csv}
        onChange={(e) => setCsv(e.target.value)}
        rows={8}
        placeholder="Paste CSV…"
        className="w-full rounded-xl border border-white/10 bg-[#0A0C12] px-3 py-2 font-mono text-xs"
      />
      <div className="flex gap-2">
        <button onClick={previewImport} className="rounded-full border border-white/15 px-4 py-2 text-sm">
          Preview mapping
        </button>
        <button onClick={runImport} className="rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12]">
          Import
        </button>
      </div>
      {preview ? <pre className="whitespace-pre-wrap text-xs text-[#F5E8D2]/6">{preview}</pre> : null}
      {result ? <p className="text-sm text-[#FFC85A]">{result}</p> : null}
    </div>
  );
}
