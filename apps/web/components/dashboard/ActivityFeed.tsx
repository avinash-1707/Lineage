type Entry = {
  id: string;
  ordinal: string;
  title: string;
  meta: string;
  body: string;
};

const SAMPLE: Entry[] = [
  {
    id: "1",
    ordinal: "§ 01",
    title: "Awaiting first review",
    meta: "Once a PR opens",
    body: "When a pull request lands on a connected repository, Lineage will read the diff, recall similar precedents, and post a contextual review here.",
  },
  {
    id: "2",
    ordinal: "§ 02",
    title: "Memory still forming",
    meta: "Standards · 0 entries",
    body: "Patterns the team accepts, refuses, or rewrites are stitched into a private style guide that improves each merge.",
  },
];

export function ActivityFeed() {
  return (
    <ol className="relative flex flex-col">
      <span
        aria-hidden
        className="pointer-events-none absolute bottom-2 left-[17px] top-2 w-px bg-line-soft"
      />
      {SAMPLE.map((entry, i) => (
        <li
          key={entry.id}
          className="relative flex gap-3 py-3 first:pt-1 last:pb-1"
        >
          <span
            aria-hidden
            className="relative z-10 mt-0.5 grid h-9 w-9 shrink-0 place-items-center rounded-full border border-line bg-paper font-mono text-[10px] uppercase tracking-[0.18em] text-muted"
          >
            {String(i + 1).padStart(2, "0")}
          </span>
          <div className="flex min-w-0 flex-col gap-1">
            <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
              <span className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted-2">
                {entry.ordinal}
              </span>
              <h3 className="font-display text-[1.05rem] italic text-ink">
                {entry.title}
              </h3>
              <span className="text-[0.78rem] text-muted">· {entry.meta}</span>
            </div>
            <p className="max-w-[62ch] text-[0.9rem] leading-relaxed text-ink-soft">
              {entry.body}
            </p>
          </div>
        </li>
      ))}
    </ol>
  );
}
