import json
import os
import sys
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import METRICS_PATH, CATEGORICAL_FEATURES, NUMERICAL_FEATURES


def evaluate_model(model, X_test, y_test, artifacts, best_params, cv_scores):
    print("\n--- Evaluacion del modelo ---")

    target_encoder = artifacts["target_encoder"]

    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)

    # Classification report
    report = classification_report(
        y_test, y_pred,
        target_names=target_encoder.classes_,
        output_dict=True,
    )
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Feature importance
    importance = model.feature_importances_
    feature_names = CATEGORICAL_FEATURES + NUMERICAL_FEATURES
    feature_importance = dict(zip(feature_names, importance.tolist()))
    feature_importance = dict(
        sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    )

    print("Feature Importance:")
    for feat, imp in feature_importance.items():
        bar = "#" * int(imp * 100)
        print(f"  {feat:25s} {imp:.4f} {bar}")

    # Save metrics
    metrics = {
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "feature_importance": feature_importance,
        "best_params": best_params,
        "cv_f1_mean": float(cv_scores.mean()),
        "cv_f1_std": float(cv_scores.std()),
        "categories": target_encoder.classes_.tolist(),
    }

    os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print(f"\nMetricas guardadas en: {METRICS_PATH}")
    print(f"F1-Score weighted: {report['weighted avg']['f1-score']:.4f}")
    print(f"Accuracy: {report['accuracy']:.4f}")

    return metrics
