"use client";

import { useState, useEffect } from "react";
import { PredictionResult as PredResult, ModelMetrics, DatasetStats } from "@/types";
import { getMetrics, getStats } from "@/lib/api";
import StatsCards from "@/components/StatsCards";
import PredictionForm from "@/components/PredictionForm";
import PredictionResultComponent from "@/components/PredictionResult";
import MetricsPanel from "@/components/MetricsPanel";
import CategoryChart from "@/components/CategoryChart";

export default function Home() {
  const [prediction, setPrediction] = useState<PredResult | null>(null);
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [stats, setStats] = useState<DatasetStats | null>(null);

  useEffect(() => {
    getMetrics().then(setMetrics).catch(() => {});
    getStats().then(setStats).catch(() => {});
  }, []);

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-sand/60 bg-white/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-rust to-ember flex items-center justify-center shadow-lg shadow-rust/20">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div>
              <h1 className="font-display text-xl text-deep tracking-tight leading-none">
                Clasificador de Reclamos
              </h1>
              <p className="text-xs text-slate/50 mt-0.5">
                Sistema inteligente de clasificacion
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="tag bg-green-50 text-green-700 border border-green-200">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5 animate-pulse" />
              Modelo activo
            </span>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* Stats row */}
        <StatsCards stats={stats} metrics={metrics} />

        {/* Prediction section */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          <div className="lg:col-span-3">
            <PredictionForm onResult={setPrediction} />
          </div>
          <div className="lg:col-span-2">
            <PredictionResultComponent result={prediction} />
          </div>
        </div>

        {/* Charts + Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <CategoryChart stats={stats} metrics={metrics} />
          <MetricsPanel metrics={metrics} />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-sand/40 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between text-xs text-slate/40">
          <span>Clasificador Inteligente de Reclamos &mdash; XGBoost + FastAPI + Next.js</span>
          <span className="font-mono">v1.0.0</span>
        </div>
      </footer>
    </div>
  );
}
