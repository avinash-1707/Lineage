import type { Metadata } from "next";
import type { ReactNode } from "react";

import { DashboardGate } from "./DashboardGate";

export const metadata: Metadata = {
  title: {
    default: "Dashboard · Lineage",
    template: "%s · Lineage",
  },
  robots: { index: false, follow: false },
};

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return <DashboardGate>{children}</DashboardGate>;
}
