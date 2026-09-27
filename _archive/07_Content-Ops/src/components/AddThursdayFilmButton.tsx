"use client";

import { useState } from "react";
import { addThursdayFilm } from "@/app/videos/actions";

export function AddThursdayFilmButton({
  primary = true,
}: {
  primary?: boolean;
}) {
  const [open, setOpen] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!open) {
    return (
      <button
        type="button"
        onClick={() => setOpen(true)}
        className={
          primary
            ? "inline-flex min-h-11 items-center justify-center rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12]"
            : "inline-flex min-h-11 items-center justify-center rounded-full border border-white/10 px-5 py-2.5 text-sm text-[#F5E8D2]"
        }
      >
        Add the next Thursday film (title + date).
      </button>
    );
  }

  return (
    <form
      className="card-panel space-y-4 p-4 sm:p-5"
      action={async (formData) => {
        setPending(true);
        setError(null);
        try {
          await addThursdayFilm(formData);
        } catch (err) {
          setError(err instanceof Error ? err.message : "Could not add film");
          setPending(false);
        }
      }}
    >
      <p className="text-sm text-[#F5E8D2]/70">Title and Thursday air time (London).</p>
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="block space-y-1.5 sm:col-span-2">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Title</span>
          <input
            name="title"
            required
            placeholder="Film title"
            className="w-full rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2.5 text-sm text-[#F5E8D2]"
          />
        </label>
        <label className="block space-y-1.5">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Thursday date</span>
          <input
            name="date"
            type="date"
            required
            className="w-full rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2.5 text-sm text-[#F5E8D2]"
          />
        </label>
        <label className="block space-y-1.5">
          <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Time</span>
          <input
            name="time"
            type="time"
            defaultValue="18:00"
            className="w-full rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2.5 text-sm text-[#F5E8D2]"
          />
        </label>
      </div>
      {error ? <p className="text-sm text-[#FFC85A]">{error}</p> : null}
      <div className="flex flex-wrap gap-3">
        <button
          type="submit"
          disabled={pending}
          className="inline-flex min-h-11 items-center justify-center rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12] disabled:opacity-60"
        >
          {pending ? "Adding…" : "Save Thursday film"}
        </button>
        <button
          type="button"
          disabled={pending}
          onClick={() => setOpen(false)}
          className="inline-flex min-h-11 items-center justify-center rounded-full border border-white/10 px-5 py-2.5 text-sm text-[#F5E8D2]"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
