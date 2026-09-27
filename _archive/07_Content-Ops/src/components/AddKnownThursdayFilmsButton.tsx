"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { addKnownThursdayFilms } from "@/app/videos/actions";

export function AddKnownThursdayFilmsButton({
  primary = true,
}: {
  primary?: boolean;
}) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  function run() {
    setMessage(null);
    setError(null);
    startTransition(async () => {
      try {
        const result = await addKnownThursdayFilms();
        if (result.created === 0 && result.updated === result.total) {
          setMessage(`All ${result.total} known Thursday films already listed.`);
        } else if (result.created === result.total) {
          setMessage(`Added ${result.created} Thursday films.`);
        } else {
          setMessage(
            `Added ${result.created}, updated ${result.updated} of ${result.total} Thursday films.`,
          );
        }
        router.refresh();
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not add known films");
      }
    });
  }

  return (
    <div className="space-y-2">
      <button
        type="button"
        disabled={pending}
        onClick={run}
        className={
          primary
            ? "inline-flex min-h-11 items-center justify-center rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12] disabled:opacity-60"
            : "inline-flex min-h-11 items-center justify-center rounded-full border border-white/10 px-5 py-2.5 text-sm text-[#F5E8D2] disabled:opacity-60"
        }
      >
        {pending ? "Adding known films…" : "Add the known Thursday films"}
      </button>
      {message ? <p className="text-sm text-[#F5E8D2]/70">{message}</p> : null}
      {error ? <p className="text-sm text-[#FFC85A]">{error}</p> : null}
    </div>
  );
}
