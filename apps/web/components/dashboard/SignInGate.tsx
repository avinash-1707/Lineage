"use client";

import Link from "next/link";

import { LogoMark } from "@/components/landing/LogoMark";
import { useAuthModal } from "@/components/auth/AuthModalProvider";

export function SignInGate() {
  const { open } = useAuthModal();

  return (
    <main className="relative z-10 flex min-h-dvh flex-col items-center justify-center px-6">
      <Link
        href="/"
        aria-label="Lineage home"
        className="absolute left-6 top-6 flex items-center gap-2 text-ink-soft transition-colors hover:text-ink md:left-8 md:top-8"
      >
        <span className="grid h-8 w-8 place-items-center rounded-full border border-line bg-paper text-ink">
          <LogoMark size={15} />
        </span>
        <span className="font-display text-[1rem] leading-none tracking-tight">
          Lineage
        </span>
      </Link>

      <section className="mx-auto flex w-full max-w-[520px] flex-col items-center text-center">
        <span className="font-mono text-[10.5px] uppercase tracking-[0.26em] text-muted">
          The archive · Locked
        </span>
        <h1 className="mt-4 font-display text-[clamp(2rem,4.4vw,2.6rem)] italic leading-[1.05] text-ink">
          Sign in to enter the reading room.
        </h1>
        <p className="mt-4 max-w-[44ch] text-[0.95rem] leading-relaxed text-ink-soft">
          Your session has ended, or you have not signed in yet. The dashboard
          is reserved for authenticated visitors.
        </p>
        <button
          type="button"
          onClick={open}
          className="btn btn-primary mt-8 text-[0.92rem]"
        >
          Continue with GitHub
          <span aria-hidden className="arrow">
            →
          </span>
        </button>
        <Link
          href="/"
          className="mt-6 text-[0.82rem] uppercase tracking-[0.22em] text-muted-2 transition-colors hover:text-ink"
        >
          ← Back to the landing page
        </Link>
      </section>
    </main>
  );
}
