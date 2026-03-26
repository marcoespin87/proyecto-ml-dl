import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import (
    CATEGORICAL_FEATURES, NUMERICAL_FEATURES, TARGET,
    EXCLUDE_COLUMNS, TEST_SIZE, RANDOM_STATE,
)


def create_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["DIAS_RESOLUCION"] = (
        pd.to_datetime(df["FECHA_FIN"], errors="coerce")
        - pd.to_datetime(df["FECHA_INGRESO"], errors="coerce")
    ).dt.days
    return df


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in CATEGORICAL_FEATURES:
        if col in df.columns:
            df[col] = df[col].fillna("Desconocido")

    numerical_with_dias = NUMERICAL_FEATURES
    for col in numerical_with_dias:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    return df


def encode_features(df: pd.DataFrame):
    df = df.copy()
    encoders = {}

    for col in CATEGORICAL_FEATURES:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    target_encoder = LabelEncoder()
    df[TARGET] = target_encoder.fit_transform(df[TARGET])

    return df, encoders, target_encoder


def scale_features(df: pd.DataFrame):
    df = df.copy()
    scaler = StandardScaler()
    df[NUMERICAL_FEATURES] = scaler.fit_transform(df[NUMERICAL_FEATURES])
    return df, scaler


def prepare_data(df: pd.DataFrame):
    print("\n--- Feature Engineering ---")

    # Temporal features
    df = create_temporal_features(df)
    print("Feature DIAS_RESOLUCION creada.")

    # Handle nulls
    df = handle_nulls(df)
    print("Valores nulos tratados.")

    # Encode
    df, encoders, target_encoder = encode_features(df)
    print(f"Variables categoricas codificadas: {len(encoders)}")
    print(f"Categorias del target: {target_encoder.classes_.tolist()}")

    # Scale
    df, scaler = scale_features(df)
    print("Features numericas escaladas.")

    # Build X, y
    feature_cols = CATEGORICAL_FEATURES + NUMERICAL_FEATURES
    X = df[feature_cols]
    y = df[TARGET]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    print(f"Split: {len(X_train)} train / {len(X_test)} test")

    artifacts = {
        "encoders": encoders,
        "target_encoder": target_encoder,
        "scaler": scaler,
        "feature_names": feature_cols,
        "categorical_features": CATEGORICAL_FEATURES,
        "numerical_features": NUMERICAL_FEATURES,
        "categories": target_encoder.classes_.tolist(),
    }

    return X_train, X_test, y_train, y_test, artifacts
