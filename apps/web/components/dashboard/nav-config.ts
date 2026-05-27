export type DashboardNavItem = {
  href: string;
  label: string;
  ordinal: string;
  hint: string;
};

export const DASHBOARD_NAV: DashboardNavItem[] = [
  { href: "/dashboard", label: "Overview", ordinal: "I", hint: "The reading room" },
  { href: "/dashboard/repositories", label: "Repositories", ordinal: "II", hint: "Sources under watch" },
  { href: "/dashboard/reviews", label: "Reviews", ordinal: "III", hint: "Annotations & verdicts" },
  { href: "/dashboard/activity", label: "Activity", ordinal: "IV", hint: "Threads of work" },
  { href: "/dashboard/settings", label: "Settings", ordinal: "V", hint: "House rules" },
];
