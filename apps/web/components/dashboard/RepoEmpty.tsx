type Props = {
  installUrl: string;
};

export function RepoEmpty({ installUrl }: Props) {
  return (
    <div className="relative overflow-hidden rounded-lg border border-dashed border-line bg-bg-elevated/40 px-5 py-6 text-center sm:px-8 sm:py-8">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.18]"
        style={{
          backgroundImage:
            "radial-gradient(circle at 1px 1px, var(--line) 1px, transparent 0)",
          backgroundSize: "18px 18px",
        }}
      />
      <div className="relative mx-auto flex max-w-[44ch] flex-col items-center gap-3">
        <span className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted-2">
          Empty shelf
        </span>
        <h3 className="font-display text-[1.25rem] italic leading-tight text-ink">
          No repositories on watch yet.
        </h3>
        <p className="text-[0.86rem] leading-relaxed text-ink-soft">
          Install the Lineage GitHub App on the projects you want reviewed. Each
          merged PR becomes an entry in your archive.
        </p>
        <a
          href={installUrl}
          target="_blank"
          rel="noreferrer noopener"
          className="btn btn-primary mt-1 px-4 py-2 text-[0.85rem]"
        >
          Install GitHub App
          <span aria-hidden className="arrow">
            →
          </span>
        </a>
      </div>
    </div>
  );
}
