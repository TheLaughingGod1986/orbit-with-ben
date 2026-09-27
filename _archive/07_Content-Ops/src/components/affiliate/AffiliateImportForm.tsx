"use client";

import { useState } from "react";

export function AffiliateImportForm({ programmeSlug }: { programmeSlug?: string }) {
  const [source, setSource] = useState("amazon");
  const [programme, setProgramme] = useState(programmeSlug || "amazon-associates-uk");
  const [csv, setCsv] = useState("");
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  async function previewImport() {
    setResult(null);
    const res = await fetch("/api/affiliate/import", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ csv, source, dryRun: true }),
    });
    const data = await res.json();
    if (!res.ok) {
      setPreview(data.error || "Preview failed");
      return;
    }
    setPreview(
      `Rows: ${data.preview.rowCount}\nHeaders: ${data.preview.headers.join(", ")}\nMissing: ${
        data.preview.missing.join(", ") || "none"
      }\nAlready imported: ${data.alreadyImported ? "yes" : "no"}\nSample: ${JSON.stringify(
        data.preview.sampleRows.slice(0, 2),
        null,
        2,
      )}`,
    );
  }

  async function runImport() {
    setPreview(null);
    const res = await fetch("/api/affiliate/import", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        csv,
        source,
        programmeSlug: programme,
        commit: true,
        dryRun: false,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      setResult(data.error || "Import failed");
      return;
    }
    if (data.duplicate) {
      setResult(data.message);
      return;
    }
    setResult(
      `Imported ${data.successCount}/${data.rowCount}. Skipped: ${data.skippedCount}. Errors: ${data.errorCount}`,
    );
  }

  return (
    <div className="card-panel space-y-3 p-5">
      <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">
        Affiliate conversion CSV
      </h2>
      <p className="text-sm text-[#F5E8D2]/55">
        Preview before commit. Duplicate file hashes are rejected.
      </p>
      <div className="flex flex-wrap gap-3">
        <select
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2 text-sm"
        >
          <option value="amazon">Amazon report</option>
          <option value="brilliant">Brilliant report</option>
          <option value="generic">Generic</option>
        </select>
        <select
          value={programme}
          onChange={(e) => setProgramme(e.target.value)}
          className="rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2 text-sm"
        >
          <option value="amazon-associates-uk">Amazon Associates UK</option>
          <option value="brilliant">Brilliant</option>
          <option value="astronomy-retailer">Astronomy Retailer</option>
          <option value="lego">LEGO</option>
        </select>
      </div>
      <textarea
        value={csv}
        onChange={(e) => setCsv(e.target.value)}
        rows={8}
        placeholder="Paste affiliate CSV…"
        className="w-full rounded-xl border border-white/10 bg-[#0A0C12] px-3 py-2 font-mono text-xs"
      />
      <div className="flex gap-2">
        <button
          onClick={previewImport}
          className="rounded-full border border-white/15 px-4 py-2 text-sm"
        >
          Preview
        </button>
        <button
          onClick={runImport}
          className="rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12]"
        >
          Commit import
        </button>
      </div>
      {preview ? <pre className="whitespace-pre-wrap text-xs text-[#F5E8D2]/6">{preview}</pre> : null}
      {result ? <p className="text-sm text-[#FFC85A]">{result}</p> : null}
    </div>
  );
}
