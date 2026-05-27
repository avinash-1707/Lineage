"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { ApiError } from "@/lib/api";
import { fetchCurrentUser, logoutRequest, type UserMe } from "@/lib/auth";

export const USER_QUERY_KEY = ["auth", "me"] as const;

export function useUser() {
  const query = useQuery<UserMe | null, ApiError>({
    queryKey: USER_QUERY_KEY,
    queryFn: async ({ signal }) => {
      try {
        return await fetchCurrentUser(signal);
      } catch (err) {
        if (err instanceof ApiError && err.status === 401) return null;
        throw err;
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  return {
    user: query.data ?? null,
    isAuthenticated: !!query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    refetch: query.refetch,
  };
}

export function useLogout() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: logoutRequest,
    onSettled: () => {
      qc.setQueryData(USER_QUERY_KEY, null);
      qc.invalidateQueries({ queryKey: USER_QUERY_KEY });
    },
  });
}
