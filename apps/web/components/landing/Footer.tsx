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
    <footer className="relative z-10 mx-auto max-w-[1240px] px-6 pb-12 pt-32 md:px-10 md:pb-16 md:pt-44">
      <div className="border-t border-line pt-16 md:pt-20">
        <div className="grid grid-cols-12 gap-x-8 gap-y-14 lg:gap-x-16">
          {/* Brand block */}
          <div className="col-span-12 flex flex-col gap-6 lg:col-span-5">
            <div className="flex items-center gap-3">
              <span
                aria-hidden
                className="grid h-10 w-10 place-items-center rounded-full border border-line bg-paper text-ink"
              >
                <LogoMark size={20} />
              </span>
              <span className="font-display text-[1.55rem] leading-none tracking-tight">
                Lineage
              </span>
            </div>
            <p className="max-w-[38ch] text-[0.98rem] leading-[1.65] text-ink-soft">
              Code review that remembers every pull request. Made for teams
              that care about how they ship.
            </p>
            <span className="mt-2 inline-flex w-fit items-center gap-2 font-mono text-[10.5px] uppercase tracking-[0.24em] text-muted-2">
              <span className="live-dot" aria-hidden />
              Private beta · v0.1
            </span>
          </div>

          {/* Links grid */}
          <nav
            aria-label="Footer"
            className="col-span-12 grid grid-cols-2 gap-x-8 gap-y-12 sm:grid-cols-3 lg:col-span-7 lg:gap-x-10"
          >
            {cols.map((c) => (
              <div key={c.head} className="flex flex-col gap-5">
                <span className="font-mono text-[10.5px] uppercase tracking-[0.24em] text-muted-2">
                  {c.head}
                </span>
                <ul className="flex flex-col gap-3.5">
                  {c.items.map((it) => (
                    <li key={it.label}>
                      <Link
                        href={it.href}
                        className="text-[0.95rem] leading-tight text-ink-soft transition-colors duration-300 hover:text-ink"
                      >
                        {it.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </nav>
        </div>

        {/* Bottom rule */}
        <div className="mt-24 flex flex-col gap-5 border-t border-line-soft pt-8 font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2 md:mt-28 md:flex-row md:items-center md:justify-between md:gap-8">
          <span>© {new Date().getFullYear()} Lineage Labs. Composed with care.</span>
          <div className="flex items-center gap-8">
            <Link href="#" className="transition-colors duration-300 hover:text-ink">
              Privacy
            </Link>
            <Link href="#" className="transition-colors duration-300 hover:text-ink">
              Terms
            </Link>
            <Link href="#" className="transition-colors duration-300 hover:text-ink">
              Security
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
