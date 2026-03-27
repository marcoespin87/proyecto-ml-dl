import json
import os

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import MODEL_PATH, METRICS_PATH, DATA_PATH, TARGET

app = FastAPI(title="Clasificador de Reclamos API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    texto: str


@app.post("/api/predict")
def predict(claim: ClaimInput):
    if artifacts is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado. Entrena primero.")

    model = artifacts["model"]
    tfidf = artifacts["tfidf"]
    target_encoder = artifacts["target_encoder"]

    texto = claim.texto.lower().strip()
    if not texto:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacio.")

    X = tfidf.transform([texto])
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
    }
    return stats


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_loaded": artifacts is not None,
    }
