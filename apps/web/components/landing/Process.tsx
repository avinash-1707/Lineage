import { Reveal } from "./Reveal";

const steps = [
  {
    num: "i.",
    title: "It listens.",
    body:
      "When a pull request opens, Lineage reads the diff the way a careful reviewer would. Files, hunks, intent, and the symbols you touched.",
    tag: "webhook",
  },
  {
    num: "ii.",
    title: "It remembers.",
    body:
      "Every comment your team has ever left is searchable context. Lineage pulls the closest precedents and reapplies them where they fit.",
    tag: "memory",
  },
  {
    num: "iii.",
    title: "It replies.",
    body:
      "Feedback arrives inline, ranked by severity, in the voice your team already reviews in. Accept, dismiss, or edit. Lineage learns from each move.",
    tag: "loop",
  },
];

export function Process() {
  return (
    <section
      id="how"
      className="relative z-10 mx-auto max-w-[1240px] px-6 py-28 md:px-10 md:py-40"
    >
      <Reveal className="grid grid-cols-12 gap-y-6">
        <div className="col-span-12 md:col-span-4">
          <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
            Chapter one
          </span>
          <h2 className="mt-4 font-display text-[clamp(2.4rem,5.4vw,4.4rem)] leading-[0.98] tracking-[-0.03em]">
            Three acts,
            <br />
            <span className="italic text-sage">one quiet habit.</span>
          </h2>
        </div>
        <p className="col-span-12 max-w-[44ch] self-end text-[1.05rem] leading-[1.55] text-ink-soft md:col-span-7 md:col-start-6">
          Lineage runs as a small, attentive presence in your repository.
          It reads, recalls, and replies. Then it watches what you did with
          what it said.
        </p>
      </Reveal>

      <ol className="relative mt-20 grid gap-6 md:mt-28 md:grid-cols-3 md:gap-10">
        {/* connecting hairline */}
        <div
          aria-hidden
          className="pointer-events-none absolute left-0 right-0 top-12 hidden h-px bg-line md:block"
        />
        {steps.map((s, i) => (
          <Reveal
            key={s.num}
            as="li"
            delay={i * 120}
            className="lift relative flex flex-col gap-5 rounded-2xl border border-line bg-paper p-7 md:p-8"
          >
            <div className="flex items-center justify-between">
              <span className="font-display text-[1.6rem] italic text-accent">
                {s.num}
              </span>
              <span className="font-mono text-[10px] uppercase tracking-[0.22em] text-muted-2">
                {s.tag}
              </span>
            </div>
            <h3 className="font-display text-[1.85rem] leading-[1.05] tracking-tight">
              {s.title}
            </h3>
            <p className="max-w-[36ch] text-[0.98rem] leading-[1.55] text-ink-soft">
              {s.body}
            </p>
          </Reveal>
        ))}
      </ol>
    </section>
  );
}
