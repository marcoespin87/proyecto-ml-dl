import json
import os

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import MODEL_PATH, METRICS_PATH, DATA_PATH, TARGET

app = FastAPI(title="Clasificador de Reclamos API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model artifacts at startup
artifacts = None


@app.on_event("startup")
def load_model():
    global artifacts
    if os.path.exists(MODEL_PATH):
        artifacts = joblib.load(MODEL_PATH)
        print(f"Modelo cargado desde {MODEL_PATH}")
    else:
        print(f"ADVERTENCIA: No se encontro modelo en {MODEL_PATH}. Entrena primero.")


class ClaimInput(BaseModel):
    sector: str
    tipo_reclamacion: str
    procedimiento: str
    bien_o_serv: str
    medio_ingreso: str
    tipo_prod: str
    modalidad_compra: str
    modalidad_pago: str
    prob_especial: str
    costo_bien_servicio: float
    monto_reclamado: float
    monto_recuperado: float
    dias_resolucion: float


def predict_claim(input_data: dict, artifacts: dict) -> dict:
    model = artifacts["model"]
    encoders = artifacts["encoders"]
    target_encoder = artifacts["target_encoder"]
    scaler = artifacts["scaler"]
    categorical_features = artifacts["categorical_features"]
    numerical_features = artifacts["numerical_features"]

    key_to_col = {
        "sector": "SECTOR",
        "tipo_reclamacion": "TIPO_RECLAMACION",
        "procedimiento": "PROCEDIMIENTO",
        "bien_o_serv": "BIEN O SERV",
        "medio_ingreso": "MEDIO INGRESO",
        "tipo_prod": "TIPO PROD",
        "modalidad_compra": "MODALIDAD COMPRA",
        "modalidad_pago": "MODALIDAD PAGO",
        "prob_especial": "PROB ESPECIAL",
        "costo_bien_servicio": "COSTO BIEN SERVICIO",
        "monto_reclamado": "MONTO RECLAMADO",
        "monto_recuperado": "MONTO RECUPERADO",
        "dias_resolucion": "DIAS_RESOLUCION",
    }

    row = {}
    for key, col in key_to_col.items():
        if key not in input_data:
            raise ValueError(f"Campo requerido faltante: {key}")
        row[col] = input_data[key]

    for col in categorical_features:
        val = str(row[col])
        le = encoders[col]
        if val in le.classes_:
            row[col] = le.transform([val])[0]
        else:
            row[col] = 0

    num_values = np.array([[row[col] for col in numerical_features]])
    num_scaled = scaler.transform(num_values)[0]
    for i, col in enumerate(numerical_features):
        row[col] = num_scaled[i]

    feature_order = categorical_features + numerical_features
    X = np.array([[row[col] for col in feature_order]])

    proba = model.predict_proba(X)[0]
    pred_idx = int(np.argmax(proba))
    pred_label = target_encoder.inverse_transform([pred_idx])[0]

    probabilidades = {}
    for idx, class_name in enumerate(target_encoder.classes_):
        probabilidades[class_name] = round(float(proba[idx]), 4)

    probabilidades = dict(
        sorted(probabilidades.items(), key=lambda x: x[1], reverse=True)
    )

    return {
        "prediccion": pred_label,
        "confianza": round(float(proba[pred_idx]), 4),
        "probabilidades": probabilidades,
    }


@app.post("/api/predict")
def predict(claim: ClaimInput):
    if artifacts is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado. Entrena primero.")

    try:
        result = predict_claim(claim.model_dump(), artifacts)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/categories")
def get_categories():
    if artifacts is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado.")
    return {"categories": artifacts["categories"]}


@app.get("/api/metrics")
def get_metrics():
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(status_code=404, detail="Metricas no encontradas. Entrena el modelo primero.")
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    return metrics


@app.get("/api/stats")
def get_stats():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Dataset no encontrado.")

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    distribution = df[TARGET].value_counts().to_dict()
    stats = {
        "total_registros": len(df),
        "total_categorias": df[TARGET].nunique(),
        "distribucion": distribution,
        "promedio_costo": round(float(df["COSTO BIEN SERVICIO"].mean()), 2),
        "promedio_monto_reclamado": round(float(df["MONTO RECLAMADO"].mean()), 2),
        "promedio_monto_recuperado": round(float(df["MONTO RECUPERADO"].mean()), 2),
    }
    return stats


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_loaded": artifacts is not None,
    }
