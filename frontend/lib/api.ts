export type ApiResponse<T> = {
  data?: T;
  error?: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

async function request<T>(path: string): Promise<ApiResponse<T>> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    return { error: `Request failed: ${response.status}` };
  }

  const data = (await response.json()) as T;
  return { data };
}

export const api = {
  health: () => request<{ status: string; service: string; version: string }>('/api/v1/health'),
};
