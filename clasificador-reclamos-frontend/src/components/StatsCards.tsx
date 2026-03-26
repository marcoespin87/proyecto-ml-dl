"use client";

import { DatasetStats, ModelMetrics } from "@/types";

interface StatsCardsProps {
  stats: DatasetStats | null;
  metrics: ModelMetrics | null;
}

export default function StatsCards({ stats, metrics }: StatsCardsProps) {
  const cards = [
    {
      label: "Reclamos totales",
      value: stats ? stats.total_registros.toLocaleString() : "...",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      color: "text-deep",
    },
    {
      label: "Categorias",
      value: stats ? stats.total_categorias.toString() : "...",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
      ),
      color: "text-rust",
    },
    {
      label: "F1-Score",
      value: metrics
        ? (metrics.classification_report?.["weighted avg"]?.["f1-score"] ?? metrics.cv_f1_mean).toFixed(3)
        : "...",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
      color: "text-ember",
    },
    {
      label: "Accuracy",
      value: metrics
        ? ((metrics.classification_report?.accuracy ?? 0) * 100).toFixed(1) + "%"
        : "...",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      color: "text-green-700",
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, i) => (
        <div
          key={card.label}
          className="card px-5 py-5 animate-fade-up"
          style={{ animationDelay: `${i * 80}ms` }}
        >
          <div className="flex items-center gap-2 mb-3">
            <span className={`${card.color} opacity-60`}>{card.icon}</span>
            <span className="label mb-0">{card.label}</span>
          </div>
          <div className={`metric-value ${card.color}`}>{card.value}</div>
        </div>
      ))}
    </div>
  );
}
