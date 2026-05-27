"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuthModal } from "@/components/auth/AuthModalProvider";
import { Nav } from "@/components/landing/Nav";
import { useLogout, useUser } from "@/hooks/useUser";

export function DashboardClient() {
  const { user, isAuthenticated, isLoading } = useUser();
  const { open } = useAuthModal();
  const router = useRouter();
  const logout = useLogout();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) open();
  }, [isLoading, isAuthenticated, open]);

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (!isAuthenticated || !user) {
    return (
      <main className="relative z-10 flex min-h-screen flex-col">
        <Nav />
        <section className="mx-auto flex w-full max-w-[640px] flex-1 flex-col items-center justify-center px-6 text-center">
          <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted">
            Authentication required
          </span>
          <h1 className="mt-4 font-display text-[clamp(2rem,4.2vw,2.6rem)] italic leading-[1.05] text-ink">
            Sign in to continue.
          </h1>
          <p className="mt-4 max-w-[44ch] text-[0.95rem] text-ink-soft">
            Your session has ended or you have not signed in yet.
          </p>
          <button
            type="button"
            onClick={open}
            className="btn btn-primary mt-8 text-[0.92rem]"
          >
            Continue with GitHub
            <span aria-hidden className="arrow">→</span>
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="relative z-10 flex min-h-screen flex-col">
      <Nav />
      <section className="mx-auto w-full max-w-[1240px] flex-1 px-6 pb-24 pt-32 md:px-10 md:pt-36">
        <div className="flex flex-col gap-3">
          <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted">
            Chapter · Dashboard
          </span>
          <h1 className="font-display text-[clamp(2.4rem,5vw,3.6rem)] leading-[1.02] tracking-[-0.025em] text-ink">
            Welcome back,{" "}
            <span className="italic text-accent">
              {firstName(user.name, user.email)}.
            </span>
          </h1>
          <p className="max-w-[58ch] text-[1rem] text-ink-soft">
            This is the placeholder dashboard. Repositories, reviews, and team
            settings will appear here.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <ProfileCard
            label="Signed in as"
            primary={user.email}
            secondary={user.name ?? undefined}
          />
          <ProfileCard label="Plan" primary={user.plan} secondary={`Role: ${user.role}`} />
          <ProfileCard
            label="Joined"
            primary={new Date(user.created_at).toLocaleDateString()}
            secondary={user.id.slice(0, 8)}
          />
        </div>

        <div className="mt-12 flex flex-wrap items-center gap-3 border-t border-line-soft pt-6">
          <a
            href={githubAppInstallUrl()}
            target="_blank"
            rel="noreferrer noopener"
            className="btn btn-ghost text-[0.88rem]"
          >
            Install GitHub App
            <span aria-hidden className="arrow">→</span>
          </a>
          <button
            type="button"
            onClick={() => logout.mutate(undefined, { onSuccess: () => router.refresh() })}
            disabled={logout.isPending}
            className="btn btn-ghost text-[0.88rem]"
          >
            {logout.isPending ? "Signing out…" : "Sign out"}
          </button>
        </div>
      </section>
    </main>
  );
}

function ProfileCard({
  label,
  primary,
  secondary,
}: {
  label: string;
  primary: string;
  secondary?: string;
}) {
  return (
    <div className="rounded-[20px] border border-line bg-paper px-5 py-5">
      <span className="font-mono text-[10px] uppercase tracking-[0.22em] text-muted">
        {label}
      </span>
      <p className="mt-3 truncate font-display text-[1.15rem] italic text-ink">
        {primary}
      </p>
      {secondary ? (
        <p className="mt-1 truncate text-[0.85rem] text-ink-soft">{secondary}</p>
      ) : null}
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <main className="relative z-10 flex min-h-screen flex-col">
      <Nav />
      <section className="mx-auto w-full max-w-[1240px] flex-1 px-6 pb-24 pt-36 md:px-10">
        <div className="h-3 w-32 animate-pulse rounded-full bg-line" />
        <div className="mt-4 h-14 w-2/3 animate-pulse rounded-md bg-line" />
        <div className="mt-3 h-4 w-1/2 animate-pulse rounded-md bg-line-soft" />
        <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="h-28 animate-pulse rounded-[20px] border border-line bg-paper"
            />
          ))}
        </div>
      </section>
    </main>
  );
}

function firstName(name: string | null, email: string): string {
  if (name) return name.split(" ")[0];
  return email.split("@")[0];
}

function githubAppInstallUrl(): string {
  const slug = process.env.NEXT_PUBLIC_GITHUB_APP_SLUG;
  return slug
    ? `https://github.com/apps/${slug}/installations/new`
    : "https://github.com/apps";
}
