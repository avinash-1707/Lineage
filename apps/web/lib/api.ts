export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  body: unknown;
  constructor(message: string, status: number, body: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

type RequestOptions = Omit<RequestInit, "body"> & {
  body?: unknown;
  parseJson?: boolean;
};

export async function apiFetch<T = unknown>(
  path: string,
  { body, parseJson = true, headers, ...init }: RequestOptions = {}
): Promise<T> {
  const url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
  const finalHeaders = new Headers(headers);
  let serializedBody: BodyInit | undefined;

  if (body !== undefined) {
    if (body instanceof FormData || body instanceof URLSearchParams) {
      serializedBody = body;
    } else {
      serializedBody = JSON.stringify(body);
      if (!finalHeaders.has("Content-Type")) {
        finalHeaders.set("Content-Type", "application/json");
      }
    }
  }

  if (!finalHeaders.has("Accept")) {
    finalHeaders.set("Accept", "application/json");
  }

  const resp = await fetch(url, {
    ...init,
    headers: finalHeaders,
    credentials: "include",
    body: serializedBody,
  });

  if (resp.status === 204) {
    return undefined as T;
  }

  const isJson = resp.headers.get("content-type")?.includes("application/json");
  const data = isJson ? await resp.json().catch(() => null) : await resp.text();

  if (!resp.ok) {
    throw new ApiError(
      typeof data === "object" && data !== null && "detail" in data
        ? String((data as { detail: unknown }).detail)
        : resp.statusText,
      resp.status,
      data
    );
  }

  return (parseJson ? data : (undefined as unknown)) as T;
}
