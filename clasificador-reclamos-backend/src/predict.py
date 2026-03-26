import numpy as np
import pandas as pd


def predict_claim(input_data: dict, artifacts: dict) -> dict:
    model = artifacts["model"]
    encoders = artifacts["encoders"]
    target_encoder = artifacts["target_encoder"]
    scaler = artifacts["scaler"]
    categorical_features = artifacts["categorical_features"]
    numerical_features = artifacts["numerical_features"]

    # Map input keys to column names
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

    # Encode categorical features
    for col in categorical_features:
        val = str(row[col])
        le = encoders[col]
        if val in le.classes_:
            row[col] = le.transform([val])[0]
        else:
            # Unknown value: use most frequent class (index 0)
            row[col] = 0

    # Scale numerical features
    num_values = np.array([[row[col] for col in numerical_features]])
    num_scaled = scaler.transform(num_values)[0]
    for i, col in enumerate(numerical_features):
        row[col] = num_scaled[i]

    # Build feature array
    feature_order = categorical_features + numerical_features
    X = np.array([[row[col] for col in feature_order]])

    # Predict
    proba = model.predict_proba(X)[0]
    pred_idx = int(np.argmax(proba))
    pred_label = target_encoder.inverse_transform([pred_idx])[0]

    # Build probabilities dict
    probabilidades = {}
    for idx, class_name in enumerate(target_encoder.classes_):
        probabilidades[class_name] = round(float(proba[idx]), 4)

    # Sort by probability descending
    probabilidades = dict(
        sorted(probabilidades.items(), key=lambda x: x[1], reverse=True)
    )

    return {
        "prediccion": pred_label,
        "confianza": round(float(proba[pred_idx]), 4),
        "probabilidades": probabilidades,
    }
