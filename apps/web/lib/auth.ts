import { API_BASE_URL, apiFetch } from "@/lib/api";

export type UserMe = {
  id: string;
  email: string;
  name: string | null;
  avatar_url: string | null;
  role: "member" | "admin";
  plan: "free" | "pro";
  created_at: string;
};

export function githubLoginUrl(): string {
  return `${API_BASE_URL}/auth/github/login`;
}

export async function fetchCurrentUser(signal?: AbortSignal): Promise<UserMe> {
  return apiFetch<UserMe>("/auth/me", { signal });
}

export async function logoutRequest(): Promise<void> {
  await apiFetch<void>("/auth/logout", { method: "POST", parseJson: false });
}
