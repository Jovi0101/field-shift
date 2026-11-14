import type {
  ClimateResponse,
  Farm,
  FarmCreate,
  RotationAnalyzeRequest,
  RotationAnalyzeResponse,
} from "../types/api";

const BASE = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  createFarm: (data: FarmCreate) =>
    request<Farm>("/farms", { method: "POST", body: JSON.stringify(data) }),

  getFarm: (id: string) => request<Farm>(`/farms/${encodeURIComponent(id)}`),

  getClimate: (latitude: number, longitude: number) =>
    request<ClimateResponse>(
      `/environment/climate?latitude=${latitude}&longitude=${longitude}`,
    ),

  analyzeRotation: (data: RotationAnalyzeRequest) =>
    request<RotationAnalyzeResponse>("/rotation/analyze", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};
