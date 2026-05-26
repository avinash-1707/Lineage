import Link from "next/link";
import { LogoMark } from "./LogoMark";

const cols = [
  {
    head: "Product",
    items: [
      { label: "How it works", href: "#how" },
      { label: "Features", href: "#features" },
      { label: "Preview", href: "#preview" },
      { label: "Changelog", href: "#" },
    ],
  },
  {
    head: "Resources",
    items: [
      { label: "Documentation", href: "#" },
      { label: "Guides", href: "#" },
      { label: "Field notes", href: "#" },
    ],
  },
  {
    head: "Company",
    items: [
      { label: "About", href: "#" },
      { label: "Careers", href: "#" },
      { label: "Contact", href: "#" },
    ],
  },
];

export function Footer() {
  return (
    <footer className="relative z-10 mx-auto max-w-[1240px] px-6 pb-10 pt-24 md:px-10 md:pb-14 md:pt-32">
      <div className="border-t border-line pt-14">
        <div className="grid grid-cols-12 gap-y-12">
          <div className="col-span-12 md:col-span-5">
            <div className="flex items-center gap-2.5">
              <span
                aria-hidden
                className="grid h-9 w-9 place-items-center rounded-full border border-line bg-paper text-ink"
              >
                <LogoMark size={18} />
              </span>
              <span className="font-display text-[1.25rem] tracking-tight">
                Lineage
              </span>
            </div>
            <p className="mt-5 max-w-[36ch] text-[0.95rem] leading-[1.55] text-ink-soft">
              Code review that remembers every pull request.
              <br />
              Made for teams that care about how they ship.
            </p>
          </div>

          <div className="col-span-12 grid grid-cols-3 gap-6 md:col-span-7">
            {cols.map((c) => (
              <div key={c.head} className="flex flex-col gap-3">
                <span className="font-mono text-[10.5px] uppercase tracking-[0.22em] text-muted-2">
                  {c.head}
                </span>
                <ul className="flex flex-col gap-2.5">
                  {c.items.map((it) => (
                    <li key={it.label}>
                      <Link
                        href={it.href}
                        className="text-[0.92rem] text-ink-soft transition-colors hover:text-ink"
                      >
                        {it.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-16 flex flex-col items-start justify-between gap-4 border-t border-line-soft pt-6 font-mono text-[11px] uppercase tracking-[0.2em] text-muted-2 md:flex-row md:items-center">
          <span>© {new Date().getFullYear()} Lineage Labs</span>
          <div className="flex items-center gap-6">
            <Link href="#" className="transition-colors hover:text-ink">
              Privacy
            </Link>
            <Link href="#" className="transition-colors hover:text-ink">
              Terms
            </Link>
            <Link href="#" className="transition-colors hover:text-ink">
              Security
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
