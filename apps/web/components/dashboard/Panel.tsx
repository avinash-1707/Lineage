import type { ReactNode } from "react";

type Props = {
  eyebrow: string;
  title: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
};

export function Panel({ eyebrow, title, action, children, className }: Props) {
  return (
    <section
      className={[
        "rounded-lg border border-line bg-paper/70 backdrop-blur-[2px]",
        className ?? "",
      ].join(" ")}
    >
      <header className="flex items-baseline justify-between gap-4 border-b border-line-soft px-4 py-3">
        <div className="flex flex-col gap-0.5">
          <span className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted-2">
            {eyebrow}
          </span>
          <h2 className="font-display text-[1.05rem] italic leading-tight text-ink">
            {title}
          </h2>
        </div>
        {action ? <div className="shrink-0">{action}</div> : null}
      </header>
      <div className="px-4 py-3">{children}</div>
    </section>
  );
}
