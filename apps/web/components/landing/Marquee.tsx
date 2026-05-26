const items = [
  "Pull requests",
  "Hunks",
  "Naming patterns",
  "Past reviews",
  "Severity ranks",
  "Repo conventions",
  "Inline comments",
  "Feedback loops",
];

export function Marquee() {
  const doubled = [...items, ...items];
  return (
    <section
      aria-hidden
      className="relative z-10 border-y border-line bg-paper/60 py-4"
    >
      <div className="overflow-hidden">
        <div className="marquee-track">
          {doubled.map((label, i) => (
            <span
              key={`${label}-${i}`}
              className="flex items-center gap-4 font-display text-[1.6rem] italic leading-none text-muted whitespace-nowrap"
            >
              <Mark />
              {label}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}

function Mark() {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 14 14"
      fill="none"
      aria-hidden
      className="text-accent"
    >
      <path
        d="M7 1 L13 7 L7 13 L1 7 Z"
        stroke="currentColor"
        strokeWidth="1.4"
      />
      <circle cx="7" cy="7" r="1.6" fill="currentColor" />
    </svg>
  );
}
