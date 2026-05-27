"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { LogoMark } from "@/components/landing/LogoMark";
import type { UserMe } from "@/lib/auth";
import { DASHBOARD_NAV } from "./nav-config";
import { NavItem } from "./NavItem";
import { UserPod } from "./UserPod";

type Props = {
  user: UserMe;
};

export function Sidebar({ user }: Props) {
  const pathname = usePathname();

  return (
    <aside
      aria-label="Dashboard navigation"
      className="sticky top-0 hidden h-screen w-[280px] shrink-0 flex-col border-r border-line-soft bg-paper/40 backdrop-blur-sm lg:flex"
    >
      <div className="flex h-16 items-center gap-2.5 border-b border-line-soft px-6">
        <Link
          href="/"
          aria-label="Lineage home"
          className="group flex items-center gap-2.5"
        >
          <span className="grid h-8 w-8 place-items-center rounded-full border border-line bg-paper text-ink transition-transform duration-400 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:scale-[1.06]">
            <LogoMark size={16} />
          </span>
          <span className="font-display text-[1.1rem] leading-none tracking-tight text-ink">
            Lineage
          </span>
        </Link>
      </div>

      <div className="border-b border-line-soft px-6 py-4">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted-2">
          The archive
        </p>
        <p className="mt-1.5 font-display text-[0.9rem] italic leading-snug text-ink-soft">
          Every review is a footnote in your codebase&apos;s memory.
        </p>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4">
        <ul className="flex flex-col gap-0.5">
          {DASHBOARD_NAV.map((item) => (
            <li key={item.href}>
              <NavItem
                item={item}
                active={
                  item.href === "/dashboard"
                    ? pathname === "/dashboard"
                    : pathname.startsWith(item.href)
                }
              />
            </li>
          ))}
        </ul>
      </nav>

      <div className="border-t border-line-soft p-4">
        <UserPod user={user} />
      </div>
    </aside>
  );
}
