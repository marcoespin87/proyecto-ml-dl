import { ClaimInput, PredictionResult, ModelMetrics, DatasetStats } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function predictClaim(data: ClaimInput): Promise<PredictionResult> {
  const res = await fetch(`${API_BASE}/api/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Error en la prediccion");
  }
  return res.json();
}

export async function getCategories(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/api/categories`);
  const data = await res.json();
  return data.categories;
}

export async function getMetrics(): Promise<ModelMetrics> {
  const res = await fetch(`${API_BASE}/api/metrics`);
  return res.json();
}

export async function getStats(): Promise<DatasetStats> {
  const res = await fetch(`${API_BASE}/api/stats`);
  return res.json();
}
