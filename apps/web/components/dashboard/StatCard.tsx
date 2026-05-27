type Props = {
  ordinal: string;
  label: string;
  value: string;
  hint?: string;
  trend?: { delta: string; tone?: "up" | "down" | "neutral" };
};

export function StatCard({ ordinal, label, value, hint, trend }: Props) {
  const toneColor =
    trend?.tone === "up"
      ? "text-sage"
      : trend?.tone === "down"
        ? "text-highlight"
        : "text-muted";

  return (
    <article className="lift relative flex flex-col gap-3 overflow-hidden rounded-lg border border-line bg-paper px-4 py-4">
      <span
        aria-hidden
        className="absolute -right-3 -top-3 font-display text-[2.8rem] italic leading-none text-line-soft/80"
      >
        {ordinal}
      </span>
      <div className="relative">
        <span className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted-2">
          {label}
        </span>
        <p className="mt-2 font-display text-[1.55rem] leading-none tracking-tight text-ink">
          {value}
        </p>
      </div>
      <div className="relative flex items-baseline justify-between gap-3 border-t border-line-soft pt-2">
        <span className="text-[0.78rem] text-ink-soft">{hint ?? ""}</span>
        {trend ? (
          <span
            className={[
              "font-mono text-[10.5px] uppercase tracking-[0.18em]",
              toneColor,
            ].join(" ")}
          >
            {trend.delta}
          </span>
        ) : null}
      </div>
    </article>
  );
}
