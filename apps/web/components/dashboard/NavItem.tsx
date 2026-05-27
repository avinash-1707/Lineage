"use client";

import Link from "next/link";

import type { DashboardNavItem } from "./nav-config";

type Props = {
  item: DashboardNavItem;
  active: boolean;
  onSelect?: () => void;
};

export function NavItem({ item, active, onSelect }: Props) {
  return (
    <Link
      href={item.href}
      onClick={onSelect}
      aria-current={active ? "page" : undefined}
      className={[
        "group relative flex items-baseline gap-3 rounded-md py-2.5 pl-4 pr-3",
        "transition-[background-color,color] duration-400 ease-[cubic-bezier(0.22,1,0.36,1)]",
        active
          ? "bg-bg-elevated text-ink"
          : "text-ink-soft hover:bg-bg-elevated/60 hover:text-ink",
      ].join(" ")}
    >
      <span
        aria-hidden
        className={[
          "absolute left-0 top-1/2 h-5 w-[2px] -translate-y-1/2 rounded-full",
          "transition-[background-color,height] duration-400 ease-[cubic-bezier(0.22,1,0.36,1)]",
          active ? "bg-accent" : "bg-transparent group-hover:bg-line",
        ].join(" ")}
      />
      <span className="w-6 shrink-0 font-mono text-[10px] uppercase tracking-[0.22em] text-muted-2">
        {item.ordinal}
      </span>
      <span className="flex flex-1 flex-col">
        <span className="font-display text-[0.98rem] leading-tight">
          {item.label}
        </span>
        <span className="mt-0.5 text-[10.5px] uppercase tracking-[0.18em] text-muted-2">
          {item.hint}
        </span>
      </span>
      <span
        aria-hidden
        className={[
          "translate-x-0 text-[0.85rem] text-muted-2 transition-[transform,opacity] duration-400 ease-[cubic-bezier(0.22,1,0.36,1)]",
          active
            ? "translate-x-1 opacity-100 text-accent"
            : "opacity-0 group-hover:translate-x-1 group-hover:opacity-60",
        ].join(" ")}
      >
        →
      </span>
    </Link>
  );
}
