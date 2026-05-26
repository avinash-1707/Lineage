import Link from "next/link";

export function Hero() {
  return (
    <section className="relative z-10 mx-auto max-w-[1240px] px-6 pt-28 pb-24 md:px-10 md:pt-40 md:pb-32">
      <div className="grid grid-cols-12 gap-y-10">
        {/* Left rail: numeral + caption */}
        <aside className="col-span-12 md:col-span-2 md:pt-6">
          <div
            className="reveal flex items-start gap-3 md:flex-col md:items-start md:gap-4"
            style={{ ["--d" as string]: "180ms" }}
          >
            <span className="font-display text-5xl leading-none md:text-6xl">
              <span className="italic text-accent">01</span>
            </span>
            <p className="max-w-[14ch] font-mono text-[11px] uppercase tracking-[0.2em] text-muted-2 md:mt-1">
              Memory.
              <br />
              Pattern.
              <br />
              Review.
            </p>
          </div>
        </aside>

        {/* Hero type block */}
        <div className="col-span-12 md:col-span-10">
          <h1 className="font-display text-ink">
            <span
              className="reveal block text-[clamp(3.4rem,10vw,9.5rem)] font-[450] leading-[0.92] tracking-[-0.035em]"
              style={{ ["--d" as string]: "220ms" }}
            >
              Code review
            </span>

            <span
              className="reveal mt-1 block text-[clamp(3.4rem,10vw,9.5rem)] leading-[0.92] tracking-[-0.04em]"
              style={{ ["--d" as string]: "340ms" }}
            >
              <span className="italic font-[400] text-accent">
                that&nbsp;remembers
              </span>
            </span>

            <span
              className="reveal mt-2 flex flex-wrap items-baseline gap-x-5 gap-y-2 text-[clamp(2rem,5.4vw,4.5rem)] leading-[1.02] tracking-[-0.025em] text-ink-soft"
              style={{ ["--d" as string]: "460ms" }}
            >
              <span>every pull request.</span>
              <sup className="font-mono text-[0.7rem] font-normal uppercase tracking-[0.22em] text-muted-2">
                [forever]
              </sup>
            </span>
          </h1>

          {/* Sub block */}
          <div className="mt-10 grid grid-cols-12 gap-6">
            <p
              className="reveal col-span-12 max-w-[58ch] text-[1.05rem] leading-[1.55] text-ink-soft md:col-span-7 md:text-[1.15rem]"
              style={{ ["--d" as string]: "580ms" }}
            >
              Lineage studies the way your team actually reviews code. It picks
              up naming habits, structural preferences, and the small decisions
              that never make it into a style guide. Then it brings them back,
              quietly, in every future review.
            </p>

            <div
              className="reveal col-span-12 flex flex-col items-start gap-3 sm:flex-row sm:items-center md:col-span-5 md:justify-end"
              style={{ ["--d" as string]: "700ms" }}
            >
              <Link href="#cta" className="btn btn-primary text-[0.95rem]">
                Connect a repository
                <span aria-hidden className="arrow">
                  →
                </span>
              </Link>
              <Link href="#how" className="btn btn-ghost text-[0.95rem]">
                See how it works
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* hero footer rail: hairline + signals */}
      <div
        className="reveal mt-20 grid grid-cols-2 gap-y-6 border-t border-line pt-6 text-[11px] uppercase tracking-[0.2em] text-muted-2 md:mt-28 md:grid-cols-4"
        style={{ ["--d" as string]: "820ms" }}
      >
        <Signal k="Latency" v="streamed" sub="first byte under 1s" />
        <Signal k="Memory" v="per repository" sub="vectorized review history" />
        <Signal k="Signal" v="closed loop" sub="accept, dismiss, modify" />
        <Signal k="Connect" v="GitHub native" sub="webhook driven" />
      </div>
    </section>
  );
}

function Signal({ k, v, sub }: { k: string; v: string; sub: string }) {
  return (
    <div className="flex flex-col gap-1.5 font-mono">
      <span className="text-muted-2">{k}</span>
      <span className="font-display text-[1.4rem] normal-case tracking-tight text-ink not-italic">
        {v}
      </span>
      <span className="normal-case tracking-[0.08em] text-muted">{sub}</span>
    </div>
  );
}
