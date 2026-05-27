type Props = {
  chapter: string;
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  meta?: React.ReactNode;
};

export function SectionHeader({ chapter, title, subtitle, meta }: Props) {
  return (
    <header className="flex flex-col gap-3 border-b border-line-soft pb-5 md:flex-row md:items-end md:justify-between md:gap-10">
      <div className="flex flex-col gap-2">
        <span className="font-mono text-[10.5px] uppercase tracking-[0.26em] text-muted">
          {chapter}
        </span>
        <h1 className="font-display text-[clamp(1.6rem,3.2vw,2.4rem)] leading-[1.04] tracking-tight text-ink">
          {title}
        </h1>
        {subtitle ? (
          <p className="max-w-[58ch] text-[0.9rem] leading-relaxed text-ink-soft">
            {subtitle}
          </p>
        ) : null}
      </div>
      {meta ? <div className="shrink-0">{meta}</div> : null}
    </header>
  );
}
