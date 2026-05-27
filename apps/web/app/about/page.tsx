import type { Metadata } from "next";

import { Footer } from "@/components/landing/Footer";
import { Nav } from "@/components/landing/Nav";
import { Reveal } from "@/components/landing/Reveal";

export const metadata: Metadata = {
  title: "About · Lineage",
  description:
    "Lineage is an adaptive code review agent that learns how your team reviews and brings that judgment back to every pull request.",
};

const principles = [
  {
    k: "01",
    title: "Context over rules.",
    body:
      "Static linters reapply the same opinions everywhere. Lineage retrieves the precedents that actually fit the file in front of it.",
  },
  {
    k: "02",
    title: "Memory, scoped per repository.",
    body:
      "Conventions belong to the codebase that made them. Each repository keeps its own library of past reviews so nothing bleeds across teams.",
  },
  {
    k: "03",
    title: "Severity that mirrors triage.",
    body:
      "Style stays quiet, real bugs surface first. The ranking follows how your team has historically responded to similar comments.",
  },
  {
    k: "04",
    title: "A loop, not a broadcast.",
    body:
      "Every accept, dismiss, or rewrite reweights what Lineage retrieves next. The system improves without anyone tending rules.",
  },
];

export default function AboutPage() {
  return (
    <main className="relative z-10 isolate flex min-h-screen flex-col">
      <Nav />

      {/* Header */}
      <section className="relative z-10 mx-auto w-full max-w-[1240px] px-6 pb-20 pt-40 md:px-10 md:pb-28 md:pt-48">
        <Reveal className="flex flex-col gap-6">
          <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
            About Lineage
          </span>
          <h1 className="max-w-[18ch] font-display text-[clamp(2.8rem,7.5vw,6rem)] leading-[0.95] tracking-[-0.035em]">
            A reviewer that{" "}
            <span className="italic text-accent">remembers</span> the
            conversations your team already had.
          </h1>
          <p className="mt-2 max-w-[60ch] text-[1.05rem] leading-[1.6] text-ink-soft md:text-[1.1rem]">
            Most review tooling is either a static linter or a generic LLM
            wrapper. Neither knows your naming conventions, your past triage,
            or the comment a teammate left three months ago on a similar
            change. Lineage closes that gap.
          </p>
        </Reveal>
      </section>

      {/* Problem · Approach */}
      <section className="relative z-10 mx-auto w-full max-w-[1240px] px-6 pb-24 md:px-10 md:pb-32">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <Reveal className="lift flex flex-col gap-5 rounded-2xl border border-line bg-paper/60 p-7 md:p-9">
            <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
              The problem
            </span>
            <h2 className="font-display text-[1.65rem] leading-[1.1] tracking-tight md:text-[1.85rem]">
              Teams re-explain the same conventions on every pull request.
            </h2>
            <p className="text-[0.98rem] leading-[1.6] text-ink-soft">
              Linters are syntactic. Generic agents are context-free. Neither
              one carries memory across reviews, so the same nudges get typed
              out again and again — and nothing compounds.
            </p>
          </Reveal>

          <Reveal
            delay={120}
            className="lift flex flex-col gap-5 rounded-2xl border border-line bg-paper/60 p-7 md:p-9"
          >
            <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
              Our approach
            </span>
            <h2 className="font-display text-[1.65rem] leading-[1.1] tracking-tight md:text-[1.85rem]">
              A self-improving agent with a feedback loop at its center.
            </h2>
            <p className="text-[0.98rem] leading-[1.6] text-ink-soft">
              Lineage reads the diff, retrieves similar past reviews from a
              per-repo vector store, generates structured feedback, and
              learns from what gets accepted or dismissed — without anyone
              maintaining rules.
            </p>
          </Reveal>
        </div>
      </section>

      {/* Principles */}
      <section className="relative z-10 mx-auto w-full max-w-[1240px] px-6 pb-32 md:px-10 md:pb-40">
        <Reveal className="flex flex-col gap-4">
          <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
            What we believe
          </span>
          <h2 className="max-w-[22ch] font-display text-[clamp(2rem,4.4vw,3.4rem)] leading-[1] tracking-[-0.03em]">
            Principles that shape{" "}
            <span className="italic text-accent">every review.</span>
          </h2>
        </Reveal>

        <ul className="mt-14 grid grid-cols-1 gap-4 sm:grid-cols-2">
          {principles.map((p, i) => (
            <Reveal
              key={p.k}
              as="li"
              delay={(i % 2) * 100}
              className="lift flex h-full flex-col gap-4 rounded-[18px] border border-line bg-paper/60 p-7 md:p-8"
            >
              <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
                {p.k}
              </span>
              <h3 className="font-display text-[1.4rem] leading-[1.15] tracking-tight">
                {p.title}
              </h3>
              <p className="max-w-[44ch] text-[0.95rem] leading-[1.55] text-ink-soft">
                {p.body}
              </p>
            </Reveal>
          ))}
        </ul>
      </section>

      <Footer />
    </main>
  );
}
