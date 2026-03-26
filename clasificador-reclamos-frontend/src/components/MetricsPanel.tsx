"use client";

import { ModelMetrics } from "@/types";

interface MetricsPanelProps {
  metrics: ModelMetrics | null;
}

export default function MetricsPanel({ metrics }: MetricsPanelProps) {
  if (!metrics) {
    return (
      <div className="card-solid p-6 animate-fade-up" style={{ animationDelay: "500ms" }}>
        <h2 className="section-title mb-4">Metricas del modelo</h2>
        <div className="flex items-center justify-center h-40 text-sm text-slate/40">
          Cargando metricas...
        </div>
      </div>
    );
  }

  const report = metrics.classification_report;
  const categories = metrics.categories || [];

  // Extract per-class metrics
  const classMetrics = categories
    .filter((cat) => report[cat])
    .map((cat) => ({
      name: cat,
      precision: report[cat].precision,
      recall: report[cat].recall,
      f1: report[cat]["f1-score"],
      support: report[cat].support,
    }))
    .sort((a, b) => b.f1 - a.f1);

  return (
    <div className="card-solid p-6 animate-fade-up" style={{ animationDelay: "500ms" }}>
      <div className="flex items-center justify-between mb-5">
        <h2 className="section-title">Metricas del modelo</h2>
        <div className="flex gap-3">
          <div className="tag bg-rust/10 text-rust">
            F1: {report["weighted avg"]?.["f1-score"]?.toFixed(3) ?? "N/A"}
          </div>
          <div className="tag bg-green-50 text-green-700">
            CV: {metrics.cv_f1_mean.toFixed(3)} &plusmn; {metrics.cv_f1_std.toFixed(3)}
          </div>
        </div>
      </div>

      <div className="overflow-x-auto -mx-6 px-6">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-sand">
              <th className="text-left py-2.5 pr-4 label mb-0 font-semibold">Categoria</th>
              <th className="text-right py-2.5 px-3 label mb-0 font-semibold">Precision</th>
              <th className="text-right py-2.5 px-3 label mb-0 font-semibold">Recall</th>
              <th className="text-right py-2.5 px-3 label mb-0 font-semibold">F1-Score</th>
              <th className="text-right py-2.5 pl-3 label mb-0 font-semibold">Soporte</th>
            </tr>
          </thead>
          <tbody>
            {classMetrics.map((row, i) => (
              <tr
                key={row.name}
                className="border-b border-sand/40 hover:bg-sand/20 transition-colors"
              >
                <td className="py-2.5 pr-4 font-medium text-deep truncate max-w-[200px]" title={row.name}>
                  {row.name}
                </td>
                <td className="text-right py-2.5 px-3 font-mono text-xs">
                  {row.precision.toFixed(3)}
                </td>
                <td className="text-right py-2.5 px-3 font-mono text-xs">
                  {row.recall.toFixed(3)}
                </td>
                <td className="text-right py-2.5 px-3">
                  <span
                    className={`font-mono text-xs font-medium ${
                      row.f1 >= 0.7 ? "text-green-700" : row.f1 >= 0.4 ? "text-amber-600" : "text-red-600"
                    }`}
                  >
                    {row.f1.toFixed(3)}
                  </span>
                </td>
                <td className="text-right py-2.5 pl-3 font-mono text-xs text-slate/60">
                  {row.support}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
