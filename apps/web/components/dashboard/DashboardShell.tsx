"use client";

import type { ReactNode } from "react";

import type { UserMe } from "@/lib/auth";
import { MobileBar } from "./MobileBar";
import { Sidebar } from "./Sidebar";

type Props = {
  user: UserMe;
  children: ReactNode;
};

export function DashboardShell({ user, children }: Props) {
  return (
    <div className="relative z-10 flex min-h-dvh w-full">
      <Sidebar user={user} />
      <div className="flex min-w-0 flex-1 flex-col">
        <MobileBar user={user} />
        <main className="relative flex-1">
          <GuideRails />
          <div className="relative mx-auto w-full max-w-[1100px] px-5 pb-10 pt-6 sm:px-8 md:pt-8 lg:px-12">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

function GuideRails() {
  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 hidden lg:block"
    >
      <div className="mx-auto h-full max-w-[1100px] px-12">
        <div className="grid h-full grid-cols-12 gap-0">
          {Array.from({ length: 13 }).map((_, i) => (
            <span
              key={i}
              className="col-span-1 border-l border-line-soft/40 first:border-l-0"
              style={{ gridColumn: `span 1 / span 1` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
