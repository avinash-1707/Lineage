"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { LogoMark } from "@/components/landing/LogoMark";
import type { UserMe } from "@/lib/auth";
import { DASHBOARD_NAV } from "./nav-config";
import { NavItem } from "./NavItem";
import { UserPod } from "./UserPod";

type Props = {
  user: UserMe;
};

export function MobileBar({ user }: Props) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [trackedPath, setTrackedPath] = useState(pathname);

  if (pathname !== trackedPath) {
    setTrackedPath(pathname);
    if (open) setOpen(false);
  }

  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [open]);

  return (
    <>
      <header className="sticky top-0 z-40 flex h-14 items-center justify-between border-b border-line-soft bg-bg/85 px-4 backdrop-blur-md lg:hidden">
        <Link href="/" aria-label="Lineage home" className="flex items-center gap-2">
          <span className="grid h-7 w-7 place-items-center rounded-full border border-line bg-paper text-ink">
            <LogoMark size={14} />
          </span>
          <span className="font-display text-[1rem] leading-none tracking-tight">
            Lineage
          </span>
        </Link>
        <button
          type="button"
          aria-expanded={open}
          aria-controls="dashboard-mobile-menu"
          aria-label={open ? "Close navigation" : "Open navigation"}
          onClick={() => setOpen((v) => !v)}
          className="relative grid h-9 w-9 place-items-center rounded-full border border-line bg-paper text-ink transition-colors hover:border-ink-soft"
        >
          <span aria-hidden className="relative block h-3 w-4">
            <span
              className={[
                "absolute left-0 right-0 h-[1.5px] origin-center bg-current",
                "transition-transform duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]",
                open ? "top-1/2 -translate-y-1/2 rotate-45" : "top-0",
              ].join(" ")}
            />
            <span
              className={[
                "absolute left-0 right-0 h-[1.5px] origin-center bg-current",
                "transition-transform duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]",
                open ? "top-1/2 -translate-y-1/2 -rotate-45" : "bottom-0",
              ].join(" ")}
            />
          </span>
        </button>
      </header>

      {open ? (
        <div
          id="dashboard-mobile-menu"
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-30 lg:hidden"
        >
          <button
            type="button"
            aria-label="Close navigation"
            onClick={() => setOpen(false)}
            className="absolute inset-0 bg-contrast-bg/70 backdrop-blur-sm"
          />
          <div className="absolute inset-x-0 top-14 max-h-[calc(100dvh-3.5rem)] overflow-y-auto border-b border-line-soft bg-paper/95 p-4 shadow-[0_30px_80px_-30px_rgba(0,0,0,0.7)]">
            <p className="px-2 font-mono text-[10px] uppercase tracking-[0.24em] text-muted-2">
              The archive
            </p>
            <ul className="mt-3 flex flex-col gap-0.5">
              {DASHBOARD_NAV.map((item) => (
                <li key={item.href}>
                  <NavItem
                    item={item}
                    active={
                      item.href === "/dashboard"
                        ? pathname === "/dashboard"
                        : pathname.startsWith(item.href)
                    }
                    onSelect={() => setOpen(false)}
                  />
                </li>
              ))}
            </ul>
            <div className="mt-4 border-t border-line-soft pt-4">
              <UserPod user={user} />
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
