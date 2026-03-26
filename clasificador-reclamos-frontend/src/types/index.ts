export interface ClaimInput {
  sector: string;
  tipo_reclamacion: string;
  procedimiento: string;
  bien_o_serv: string;
  medio_ingreso: string;
  tipo_prod: string;
  modalidad_compra: string;
  modalidad_pago: string;
  prob_especial: string;
  costo_bien_servicio: number;
  monto_reclamado: number;
  monto_recuperado: number;
  dias_resolucion: number;
}

export interface PredictionResult {
  prediccion: string;
  confianza: number;
  probabilidades: Record<string, number>;
}

export interface ModelMetrics {
  classification_report: Record<string, any>;
  confusion_matrix: number[][];
  feature_importance: Record<string, number>;
  best_params: Record<string, any>;
  cv_f1_mean: number;
  cv_f1_std: number;
  categories: string[];
}

export interface DatasetStats {
  total_registros: number;
  total_categorias: number;
  distribucion: Record<string, number>;
  promedio_costo: number;
  promedio_monto_reclamado: number;
  promedio_monto_recuperado: number;
}
