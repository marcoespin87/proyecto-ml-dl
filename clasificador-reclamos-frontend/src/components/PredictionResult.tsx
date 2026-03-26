"use client";

import { useState } from "react";
import { PredictionResult as PredResult } from "@/types";

interface PredictionResultProps {
  result: PredResult | null;
}

function getConfidenceColor(confidence: number) {
  if (confidence >= 0.7) return { bg: "bg-green-50", text: "text-green-700", bar: "bg-green-500", border: "border-green-200" };
  if (confidence >= 0.4) return { bg: "bg-amber-50", text: "text-amber-700", bar: "bg-amber-500", border: "border-amber-200" };
  return { bg: "bg-red-50", text: "text-red-700", bar: "bg-red-500", border: "border-red-200" };
}

export default function PredictionResult({ result }: PredictionResultProps) {
  const [expanded, setExpanded] = useState(false);

  if (!result) {
    return (
      <div className="card-solid p-6 flex flex-col items-center justify-center min-h-[320px] animate-fade-up" style={{ animationDelay: "300ms" }}>
        <div className="w-16 h-16 rounded-2xl bg-sand/40 flex items-center justify-center mb-4">
          <svg className="w-8 h-8 text-clay" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <p className="text-sm text-slate/50 text-center font-medium">
          Completa el formulario para<br />obtener una clasificacion
        </p>
      </div>
    );
  }

  const colors = getConfidenceColor(result.confianza);
  const sortedProbs = Object.entries(result.probabilidades);

  return (
    <div className="card-solid p-6 animate-scale-in">
      <h2 className="section-title mb-5">Resultado</h2>

      {/* Main prediction */}
      <div className={`${colors.bg} ${colors.border} border rounded-xl p-5 mb-5`}>
        <span className="label mb-2 block">Categoria predicha</span>
        <p className="font-display text-xl text-deep leading-tight mb-3">
          {result.prediccion}
        </p>

        {/* Confidence bar */}
        <div className="flex items-center gap-3">
          <div className="flex-1 h-2.5 bg-black/5 rounded-full overflow-hidden">
            <div
              className={`h-full ${colors.bar} rounded-full transition-all duration-700 ease-out`}
              style={{ width: `${result.confianza * 100}%` }}
            />
          </div>
          <span className={`font-mono text-sm font-medium ${colors.text}`}>
            {(result.confianza * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Probabilities */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 text-sm font-medium text-slate/60 hover:text-rust transition-colors mb-3"
      >
        <svg
          className={`w-4 h-4 transition-transform duration-200 ${expanded ? "rotate-90" : ""}`}
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
        Todas las probabilidades ({sortedProbs.length})
      </button>

      {expanded && (
        <div className="space-y-2 animate-fade-up">
          {sortedProbs.map(([cat, prob], i) => (
            <div key={cat} className="flex items-center gap-3 text-sm">
              <span className="w-[45%] truncate text-slate/80" title={cat}>{cat}</span>
              <div className="flex-1 h-1.5 bg-sand/60 rounded-full overflow-hidden">
                <div
                  className="h-full bg-rust/70 rounded-full"
                  style={{ width: `${prob * 100}%` }}
                />
              </div>
              <span className="font-mono text-xs text-slate/60 w-14 text-right">
                {(prob * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
