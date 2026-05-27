"use client";

import { ActivityFeed } from "@/components/dashboard/ActivityFeed";
import { Panel } from "@/components/dashboard/Panel";
import { RepoEmpty } from "@/components/dashboard/RepoEmpty";
import { SectionHeader } from "@/components/dashboard/SectionHeader";
import { StatCard } from "@/components/dashboard/StatCard";
import { useUser } from "@/hooks/useUser";

export function DashboardClient() {
  const { user } = useUser();
  if (!user) return null;

  return (
    <>
      <SectionHeader
        chapter="Chapter I · Overview"
        title={
          <>
            Welcome back,{" "}
            <span className="italic text-accent">
              {firstName(user.name, user.email)}.
            </span>
          </>
        }
        subtitle="The archive is quiet for now. Connect a repository and Lineage will begin recording — every review a footnote, every merge a chapter."
        meta={
          <div className="flex items-center gap-2 rounded-full border border-line bg-paper px-3 py-1.5">
            <span className="live-dot" aria-hidden />
            <span className="font-mono text-[10px] uppercase tracking-[0.22em] text-muted">
              {user.plan} · {user.role}
            </span>
          </div>
        }
      />

      <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard
          ordinal="i"
          label="Repositories"
          value="0"
          hint="None connected yet"
          trend={{ delta: "Awaiting", tone: "neutral" }}
        />
        <StatCard
          ordinal="ii"
          label="Reviews posted"
          value="0"
          hint="Across all branches"
          trend={{ delta: "—", tone: "neutral" }}
        />
        <StatCard
          ordinal="iii"
          label="Memory entries"
          value="0"
          hint="Standards learned"
          trend={{ delta: "New shelf", tone: "up" }}
        />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-[1.4fr_1fr]">
        <Panel
          eyebrow="Folio · Repositories"
          title="Your watched sources"
          action={
            <a
              href={githubAppInstallUrl()}
              target="_blank"
              rel="noreferrer noopener"
              className="text-[0.78rem] uppercase tracking-[0.2em] text-muted-2 transition-colors hover:text-accent"
            >
              Connect →
            </a>
          }
        >
          <RepoEmpty installUrl={githubAppInstallUrl()} />
        </Panel>

        <Panel eyebrow="Marginalia" title="What happens next">
          <ActivityFeed />
        </Panel>
      </div>
    </>
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
