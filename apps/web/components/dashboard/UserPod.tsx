"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";

import { useLogout } from "@/hooks/useUser";
import type { UserMe } from "@/lib/auth";

type Props = {
  user: UserMe;
  compact?: boolean;
};

export function UserPod({ user, compact = false }: Props) {
  const router = useRouter();
  const logout = useLogout();
  const initials = (user.name ?? user.email).slice(0, 1).toUpperCase();

  return (
    <div className="flex items-center gap-3 rounded-lg border border-line bg-bg-elevated/60 p-3">
      <span className="grid h-9 w-9 shrink-0 place-items-center overflow-hidden rounded-full border border-line bg-paper">
        {user.avatar_url ? (
          <Image
            src={user.avatar_url}
            alt=""
            aria-hidden
            width={36}
            height={36}
            unoptimized
            className="h-full w-full object-cover"
          />
        ) : (
          <span className="font-display text-[0.9rem] italic text-ink">
            {initials}
          </span>
        )}
      </span>
      {!compact ? (
        <div className="min-w-0 flex-1">
          <p className="truncate text-[0.84rem] text-ink">
            {user.name ?? user.email.split("@")[0]}
          </p>
          <button
            type="button"
            onClick={() =>
              logout.mutate(undefined, { onSuccess: () => router.refresh() })
            }
            disabled={logout.isPending}
            className="mt-0.5 text-[10.5px] uppercase tracking-[0.2em] text-muted-2 transition-colors hover:text-accent disabled:opacity-60"
          >
            {logout.isPending ? "Signing out…" : "Sign out →"}
          </button>
        </div>
      ) : null}
    </div>
  );
}
