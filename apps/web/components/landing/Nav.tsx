"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";

import { useAuthModal } from "@/components/auth/AuthModalProvider";
import { useUser } from "@/hooks/useUser";
import { LogoMark } from "./LogoMark";

const links = [
  { href: "#how", label: "How it works" },
  { href: "#features", label: "Features" },
  { href: "#preview", label: "Preview" },
];

export function Nav() {
  const [scrolled, setScrolled] = useState(false);
  const { isAuthenticated, isLoading, user } = useUser();
  const { open } = useAuthModal();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const ctaSizeClasses = scrolled
    ? "px-4 py-2 text-[0.82rem]"
    : "px-5 py-2.5 text-[0.88rem]";

  return (
    <header
      className="pointer-events-none fixed inset-x-0 top-0 z-50 flex justify-center px-4 pt-4 md:pt-5"
      aria-label="Primary"
    >
      <nav
        data-floating={scrolled ? "true" : "false"}
        style={{ ["--d" as string]: "0ms" }}
        className={[
          "nav-anim-drop pointer-events-auto relative flex w-full items-center justify-between",
          "transition-[max-width,padding,background-color,border-color,box-shadow,backdrop-filter]",
          "duration-600 ease-[cubic-bezier(0.22,1,0.36,1)]",
          "rounded-full border",
          scrolled
            ? "max-w-[760px] border-line bg-paper/70 px-3 py-2 shadow-[0_20px_50px_-20px_rgba(0,0,0,0.55)] backdrop-blur-md"
            : "max-w-[1240px] border-transparent bg-transparent px-2 py-2 md:px-4",
        ].join(" ")}
      >
        <Link
          href="/"
          aria-label="Lineage home"
          style={{ ["--d" as string]: "180ms" }}
          className="nav-anim-drop group flex items-center gap-2 pl-2"
        >
          <span
            aria-hidden
            className={[
              "grid place-items-center rounded-full border bg-paper text-ink",
              "transition-[height,width,border-color] duration-600 ease-[cubic-bezier(0.22,1,0.36,1)]",
              scrolled ? "h-7 w-7 border-line" : "h-9 w-9 border-line",
            ].join(" ")}
          >
            <LogoMark size={scrolled ? 14 : 18} />
          </span>
          <span
            className={[
              "font-display leading-none tracking-tight transition-[font-size] duration-600",
              scrolled ? "text-[1.05rem]" : "text-[1.25rem]",
            ].join(" ")}
          >
            Lineage
          </span>
        </Link>

        <ul className="absolute left-1/2 hidden -translate-x-1/2 items-center gap-7 md:flex">
          {links.map((l, i) => (
            <li
              key={l.href}
              style={{ ["--d" as string]: `${260 + i * 60}ms` }}
              className="nav-anim-drop"
            >
              <Link
                href={l.href}
                className="text-[0.86rem] text-muted transition-colors hover:text-ink"
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>

        <div
          style={{ ["--d" as string]: "440ms" }}
          className="nav-anim-pop flex items-center gap-2"
        >
          {isLoading ? (
            <div
              aria-hidden
              className={[
                "rounded-full border border-line bg-paper/50",
                scrolled ? "h-8 w-[120px]" : "h-9 w-[140px]",
              ].join(" ")}
            />
          ) : isAuthenticated ? (
            <Link
              href="/dashboard"
              className={[
                "btn btn-primary transition-[padding,font-size] duration-600",
                ctaSizeClasses,
              ].join(" ")}
            >
              {user?.avatar_url ? (
                <Image
                  src={user.avatar_url}
                  alt=""
                  aria-hidden
                  width={20}
                  height={20}
                  unoptimized
                  className="h-5 w-5 rounded-full border border-contrast-fg/15"
                />
              ) : null}
              <span>Dashboard</span>
              <span aria-hidden className="arrow">
                →
              </span>
            </Link>
          ) : (
            <button
              type="button"
              onClick={open}
              className={[
                "btn btn-primary transition-[padding,font-size] duration-600",
                ctaSizeClasses,
              ].join(" ")}
            >
              <span>Get started</span>
              <span aria-hidden className="arrow">
                →
              </span>
            </button>
          )}
        </div>
      </nav>
    </header>
  );
}
