"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { DatasetStats, ModelMetrics } from "@/types";

interface CategoryChartProps {
  stats: DatasetStats | null;
  metrics: ModelMetrics | null;
}

const COLORS = [
  "#b85c38", "#e8734a", "#c4a882", "#8b6f47", "#d4956a",
  "#a0522d", "#cd853f", "#deb887", "#966b3f", "#bf8040",
  "#cc7040", "#b8860b", "#d2a679", "#c08050", "#a67b5b",
];

export default function CategoryChart({ stats, metrics }: CategoryChartProps) {
  if (!stats && !metrics) {
    return (
      <div className="card-solid p-6 animate-fade-up" style={{ animationDelay: "400ms" }}>
        <h2 className="section-title mb-4">Distribucion</h2>
        <div className="flex items-center justify-center h-60 text-sm text-slate/40">
          Cargando datos...
        </div>
      </div>
    );
  }

  // Distribution chart data
  const distData = stats
    ? Object.entries(stats.distribucion)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 12)
        .map(([name, value]) => ({
          name: name.length > 25 ? name.slice(0, 22) + "..." : name,
          fullName: name,
          value,
        }))
    : [];

  // Feature importance data
  const fiData = metrics
    ? Object.entries(metrics.feature_importance)
        .map(([name, value]) => ({ name, value: Math.round(value * 1000) / 10 }))
    : [];

  return (
    <div className="card-solid p-6 animate-fade-up" style={{ animationDelay: "400ms" }}>
      <h2 className="section-title mb-5">Distribucion de reclamos</h2>

      {distData.length > 0 && (
        <div className="mb-8">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={distData} layout="vertical" margin={{ left: 10, right: 20, top: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11 }} />
              <YAxis
                dataKey="name"
                type="category"
                width={170}
                tick={{ fontSize: 11 }}
              />
              <Tooltip
                formatter={(value: number, name: string, props: any) => [
                  value.toLocaleString(),
                  props.payload.fullName,
                ]}
                contentStyle={{
                  background: "#fffdf8",
                  border: "1px solid #e8e0d0",
                  borderRadius: "12px",
                  fontSize: "13px",
                  fontFamily: "'Source Sans 3', sans-serif",
                }}
              />
              <Bar dataKey="value" radius={[0, 6, 6, 0]} maxBarSize={28}>
                {distData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {fiData.length > 0 && (
        <>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate/60 mb-4">
            Importancia de features
          </h3>
          <div className="space-y-2.5">
            {fiData.map((feat, i) => (
              <div key={feat.name} className="flex items-center gap-3">
                <span className="text-xs text-slate/70 w-[140px] truncate font-medium" title={feat.name}>
                  {feat.name}
                </span>
                <div className="flex-1 h-2 bg-sand/50 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{
                      width: `${feat.value}%`,
                      backgroundColor: COLORS[i % COLORS.length],
                      animationDelay: `${i * 50}ms`,
                    }}
                  />
                </div>
                <span className="font-mono text-xs text-slate/50 w-10 text-right">
                  {feat.value}%
                </span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
