"use client";

import type { ReactNode } from "react";
import { useEffect } from "react";

import { useAuthModal } from "@/components/auth/AuthModalProvider";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { DashboardSkeleton } from "@/components/dashboard/DashboardSkeleton";
import { SignInGate } from "@/components/dashboard/SignInGate";
import { useUser } from "@/hooks/useUser";

export function DashboardGate({ children }: { children: ReactNode }) {
  const { user, isAuthenticated, isLoading } = useUser();
  const { open } = useAuthModal();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) open();
  }, [isLoading, isAuthenticated, open]);

  if (isLoading) return <DashboardSkeleton />;
  if (!isAuthenticated || !user) return <SignInGate />;

  return <DashboardShell user={user}>{children}</DashboardShell>;
}
