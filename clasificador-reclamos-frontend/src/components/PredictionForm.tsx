"use client";

import { useState } from "react";
import { ClaimInput, PredictionResult } from "@/types";
import { predictClaim } from "@/lib/api";

const FIELD_OPTIONS: Record<string, string[]> = {
  sector: [
    "MUEBLERO", "TURÍSTICO", "TIENDA DE ACCESORIOS DE VESTIR",
    "TIENDA DEPARTAMENTAL", "ELECTRÓNICO", "AUTOMOTRIZ",
    "TELECOMUNICACIONES", "INMOBILIARIO", "FINANCIERO", "OTRO",
  ],
  tipo_reclamacion: [
    "Garantías", "Cambios, devoluciones o bonificaciones",
    "Contratos", "Incumplimiento", "Cobros", "Otros",
  ],
  procedimiento: [
    "Conciliación personal", "Conciliación telefónica",
    "Conciliación por medios electrónicos", "Arbitraje",
  ],
  bien_o_serv: ["Bien", "Servicio"],
  medio_ingreso: ["Escrito", "Personal", "Electrónico", "Telefónico"],
  tipo_prod: ["Producto nuevo", "Producto usado", "Servicio normal"],
  modalidad_compra: [
    "En establecimiento físico", "Por internet",
    "Por teléfono", "A domicilio", "Fuera de establecimiento",
  ],
  modalidad_pago: [
    "Contado", "Crédito", "Apartado", "No aplica",
  ],
  prob_especial: [
    "No problema especial", "Adulto mayor",
    "Persona con discapacidad", "Menor de edad",
  ],
};

const FIELD_LABELS: Record<string, string> = {
  sector: "Sector",
  tipo_reclamacion: "Tipo de reclamacion",
  procedimiento: "Procedimiento",
  bien_o_serv: "Bien o servicio",
  medio_ingreso: "Medio de ingreso",
  tipo_prod: "Tipo de producto",
  modalidad_compra: "Modalidad de compra",
  modalidad_pago: "Modalidad de pago",
  prob_especial: "Problema especial",
  costo_bien_servicio: "Costo del bien/servicio ($)",
  monto_reclamado: "Monto reclamado ($)",
  monto_recuperado: "Monto recuperado ($)",
  dias_resolucion: "Dias de resolucion",
};

interface PredictionFormProps {
  onResult: (result: PredictionResult) => void;
}

export default function PredictionForm({ onResult }: PredictionFormProps) {
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState<ClaimInput>({
    sector: "MUEBLERO",
    tipo_reclamacion: "Garantías",
    procedimiento: "Conciliación personal",
    bien_o_serv: "Bien",
    medio_ingreso: "Escrito",
    tipo_prod: "Producto nuevo",
    modalidad_compra: "En establecimiento físico",
    modalidad_pago: "Contado",
    prob_especial: "No problema especial",
    costo_bien_servicio: 0,
    monto_reclamado: 0,
    monto_recuperado: 0,
    dias_resolucion: 30,
  });

  const handleChange = (key: string, value: string | number) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await predictClaim(form);
      onResult(result);
    } catch (err: any) {
      alert(err.message || "Error al clasificar");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card-solid p-6 animate-fade-up" style={{ animationDelay: "200ms" }}>
      <h2 className="section-title mb-1">Clasificar reclamo</h2>
      <p className="text-sm text-slate/60 mb-6">
        Completa los datos del reclamo para obtener una prediccion
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-4">
        {Object.entries(FIELD_OPTIONS).map(([key, options]) => (
          <div key={key}>
            <label className="label">{FIELD_LABELS[key]}</label>
            <select
              className="input-field"
              value={(form as any)[key]}
              onChange={(e) => handleChange(key, e.target.value)}
            >
              {options.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
          </div>
        ))}

        {["costo_bien_servicio", "monto_reclamado", "monto_recuperado", "dias_resolucion"].map(
          (key) => (
            <div key={key}>
              <label className="label">{FIELD_LABELS[key]}</label>
              <input
                type="number"
                step="any"
                min="0"
                className="input-field"
                value={(form as any)[key]}
                onChange={(e) => handleChange(key, parseFloat(e.target.value) || 0)}
              />
            </div>
          )
        )}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="btn-primary w-full mt-6 flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Clasificando...
          </>
        ) : (
          <>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Clasificar reclamo
          </>
        )}
      </button>
    </form>
  );
}
