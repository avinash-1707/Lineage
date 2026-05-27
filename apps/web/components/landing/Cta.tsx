"use client";

import Link from "next/link";

import { useAuthModal } from "@/components/auth/AuthModalProvider";
import { useUser } from "@/hooks/useUser";
import { Reveal } from "./Reveal";

export function Cta() {
  const { open } = useAuthModal();
  const { isAuthenticated } = useUser();

  return (
    <section
      id="cta"
      className="relative z-10 mx-auto max-w-[1240px] px-6 py-24 md:px-10 md:py-32"
    >
      <Reveal>
        <div className="relative overflow-hidden rounded-[28px] border border-line bg-contrast-bg px-6 py-20 text-contrast-fg md:px-16 md:py-28">
          {/* decorative serif glyph */}
          <span
            aria-hidden
            className="pointer-events-none absolute -right-8 -top-12 font-display text-[18rem] italic leading-none text-contrast-fg/5 md:text-[26rem]"
          >
            L
          </span>

          <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-contrast-fg/55">
            The closing chapter
          </span>

          <h2 className="mt-6 max-w-[18ch] font-display text-[clamp(2.4rem,6vw,5rem)] leading-[0.98] tracking-[-0.03em]">
            Let the next review
            <br />
            <span className="italic text-highlight">
              remember the last one.
            </span>
          </h2>

          <p className="mt-8 max-w-[52ch] text-[1.05rem] leading-[1.55] text-contrast-fg/75">
            Lineage is in private beta with a small group of engineering teams.
            Sign in with GitHub and we will reach out as installation slots open
            through the quarter.
          </p>

          <div className="mt-10 flex flex-wrap items-center gap-3">
            {isAuthenticated ? (
              <Link
                href="/dashboard"
                className="btn rounded-full bg-ink px-5 py-3 text-[0.92rem] font-medium text-contrast-bg hover:bg-highlight"
              >
                Open dashboard
                <span aria-hidden className="arrow">
                  →
                </span>
              </Link>
            ) : (
              <button
                type="button"
                onClick={open}
                className="btn rounded-full bg-ink px-5 py-3 text-[0.92rem] font-medium text-contrast-bg hover:bg-highlight"
              >
                Continue with GitHub
                <span aria-hidden className="arrow">
                  →
                </span>
              </button>
            )}
            <a
              href="#features"
              className="btn rounded-full border border-contrast-fg/15 px-5 py-3 text-[0.92rem] font-medium text-contrast-fg/85 hover:border-contrast-fg/35 hover:text-contrast-fg"
            >
              See how it works
            </a>
          </div>

          <div className="mt-10 flex flex-wrap items-center gap-x-8 gap-y-3 font-mono text-[11px] uppercase tracking-[0.2em] text-contrast-fg/55">
            <span>No card required.</span>
            <span>Roll out per repository.</span>
            <span>Off any time.</span>
          </div>
        </div>
      </Reveal>
    </section>
  );
}
