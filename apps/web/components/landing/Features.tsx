import { Reveal } from "./Reveal";

type Feature = {
  k: string;
  title: string;
  body: string;
  visual: "memory" | "severity" | "stream" | "loop" | "context" | "git";
  span: string;
  size: "sm" | "md" | "lg";
};

const features: Feature[] = [
  {
    k: "01",
    title: "Memory that scopes itself.",
    body: "Each repository keeps its own library of precedent. Frontend conventions stay with the frontend, services with services.",
    visual: "memory",
    span: "sm:col-span-2 lg:col-span-3",
    size: "md",
  },
  {
    k: "02",
    title: "Severity, ranked the way you would.",
    body: "Every comment carries a tier. Style stays quiet, real bugs surface first, following your past triage.",
    visual: "severity",
    span: "sm:col-span-2 lg:col-span-3",
    size: "md",
  },
  {
    k: "03",
    title: "Streams as it thinks.",
    body: "Comments appear inline the moment they are formed. No waiting for a full review to finish before you can act on the early signal.",
    visual: "stream",
    span: "sm:col-span-2 lg:col-span-4",
    size: "lg",
  },
  {
    k: "04",
    title: "Closed feedback loop.",
    body: "Accept, dismiss, or rewrite a comment. Lineage adjusts the weight of similar comments next time without asking you to maintain rules.",
    visual: "loop",
    span: "sm:col-span-2 lg:col-span-4",
    size: "lg",
  },
  {
    k: "05",
    title: "Reads the codebase, not just the diff.",
    body: "Lineage references the files around your change so suggestions sit inside the architecture, not on top of it.",
    visual: "context",
    span: "sm:col-span-1 lg:col-span-2",
    size: "sm",
  },
  {
    k: "06",
    title: "Native to your workflow.",
    body: "Lives inside GitHub. Posts as a review and threads with your teammates.",
    visual: "git",
    span: "sm:col-span-1 lg:col-span-2",
    size: "sm",
  },
];

export function Features() {
  return (
    <section
      id="features"
      className="relative z-10 mx-auto max-w-[1240px] px-6 py-24 md:px-10 md:py-32"
    >
      <Reveal className="flex flex-col gap-4">
        <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
          Chapter two
        </span>
        <h2 className="max-w-[20ch] font-display text-[clamp(2.2rem,5vw,4rem)] leading-none tracking-[-0.03em]">
          The small <span className="italic text-accent">refinements</span> that
          make reviews feel native.
        </h2>
      </Reveal>

      <ul className="mt-16 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-6 lg:grid-flow-dense">
        {features.map((f, i) => (
          <Reveal key={f.k} as="li" delay={(i % 3) * 90} className={f.span}>
            <FeatureCard f={f} />
          </Reveal>
        ))}
      </ul>
    </section>
  );
}

function FeatureCard({ f }: { f: Feature }) {
  const titleScale =
    f.size === "lg"
      ? "text-[1.65rem] md:text-[1.85rem] leading-[1.08]"
      : f.size === "md"
        ? "text-[1.4rem] leading-[1.12]"
        : "text-[1.25rem] leading-[1.18]";
  const padding = f.size === "lg" ? "p-7 md:p-8" : "p-6 md:p-7";
  const bodyWidth =
    f.size === "lg" ? "max-w-[58ch]" : f.size === "md" ? "max-w-[44ch]" : "";

  return (
    <article
      className={`lift relative flex h-full flex-col gap-5 rounded-[18px] border border-line bg-paper/60 ${padding}`}
    >
      <div className="flex items-start justify-between">
        <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
          {f.k}
        </span>
        <Visual kind={f.visual} size={f.size} />
      </div>

      <h3 className={`font-display tracking-tight ${titleScale}`}>{f.title}</h3>
      <p className={`text-[0.95rem] leading-[1.55] text-ink-soft ${bodyWidth}`}>
        {f.body}
      </p>
    </article>
  );
}

function Visual({
  kind,
  size,
}: {
  kind: Feature["visual"];
  size: Feature["size"];
}) {
  const scale =
    size === "lg" ? "h-16 w-28" : size === "md" ? "h-14 w-24" : "h-12 w-20";
  const common = `${scale} text-ink-soft`;
  switch (kind) {
    case "memory":
      return (
        <svg viewBox="0 0 80 48" className={common} aria-hidden>
          <g stroke="currentColor" strokeWidth="1" fill="none">
            <rect x="6" y="10" width="22" height="28" rx="2" />
            <rect x="30" y="6" width="22" height="32" rx="2" />
            <rect x="54" y="12" width="20" height="26" rx="2" />
            <line x1="11" y1="17" x2="23" y2="17" />
            <line x1="11" y1="22" x2="20" y2="22" />
            <line x1="35" y1="14" x2="47" y2="14" />
            <line x1="35" y1="19" x2="44" y2="19" />
            <line x1="35" y1="24" x2="46" y2="24" />
            <line x1="59" y1="20" x2="69" y2="20" />
            <line x1="59" y1="25" x2="66" y2="25" />
          </g>
          <circle cx="40" cy="33" r="2" fill="var(--accent)" />
        </svg>
      );
    case "severity":
      return (
        <svg viewBox="0 0 80 48" className={common} aria-hidden>
          <g>
            <rect
              x="6"
              y="34"
              width="10"
              height="8"
              fill="var(--sage)"
              opacity="0.65"
            />
            <rect
              x="20"
              y="26"
              width="10"
              height="16"
              fill="var(--sage)"
              opacity="0.85"
            />
            <rect
              x="34"
              y="20"
              width="10"
              height="22"
              fill="currentColor"
              opacity="0.45"
            />
            <rect
              x="48"
              y="14"
              width="10"
              height="28"
              fill="var(--accent)"
              opacity="0.65"
            />
            <rect x="62" y="6" width="10" height="36" fill="var(--accent)" />
          </g>
        </svg>
      );
    case "stream":
      return (
        <svg viewBox="0 0 80 48" className={common} aria-hidden>
          <g stroke="currentColor" strokeWidth="1" fill="none">
            <path d="M4 24 C 18 6, 28 42, 42 24 S 64 6, 76 24" />
          </g>
          <circle cx="42" cy="24" r="3" fill="var(--accent)" />
          <circle
            cx="42"
            cy="24"
            r="6"
            fill="none"
            stroke="var(--accent)"
            strokeOpacity="0.35"
          />
        </svg>
      );
    case "loop":
      return (
        <svg viewBox="0 0 80 48" className={common} aria-hidden>
          <g stroke="currentColor" strokeWidth="1" fill="none">
            <ellipse cx="40" cy="24" rx="28" ry="14" />
            <path d="M64 16 L70 12 L66 22" strokeLinejoin="round" />
          </g>
          <circle cx="40" cy="10" r="2.5" fill="var(--accent)" />
          <circle cx="40" cy="38" r="2.5" fill="var(--sage)" />
        </svg>
      );
    case "context":
      return (
        <svg viewBox="0 0 80 48" className={common} aria-hidden>
          <g stroke="currentColor" strokeWidth="1">
            <rect x="6" y="10" width="68" height="6" fill="none" />
            <rect x="6" y="20" width="50" height="6" fill="none" />
            <rect x="6" y="30" width="60" height="6" fill="none" />
            <rect
              x="20"
              y="20"
              width="14"
              height="6"
              fill="var(--accent)"
              opacity="0.7"
              stroke="none"
            />
          </g>
        </svg>
      );
    case "git":
      return (
        <svg viewBox="0 0 80 48" className={common} aria-hidden>
          <g stroke="currentColor" strokeWidth="1.2" fill="none">
            <path d="M14 8 L14 40" />
            <path d="M14 22 C 26 22, 26 12, 38 12" />
            <path d="M38 12 L38 40" />
            <path d="M38 28 C 50 28, 50 18, 62 18" />
          </g>
          <circle cx="14" cy="8" r="3" fill="currentColor" />
          <circle cx="14" cy="40" r="3" fill="currentColor" />
          <circle cx="38" cy="12" r="3" fill="var(--accent)" />
          <circle cx="38" cy="40" r="3" fill="currentColor" />
          <circle cx="62" cy="18" r="3" fill="var(--sage)" />
        </svg>
      );
  }
}
