import sys
import os
import numpy as np
import joblib
import xgboost as xgb
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.model_selection import RandomizedSearchCV, cross_val_score

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import MODEL_PATH, RANDOM_STATE
from src.data_loader import load_and_prepare
from src.feature_engineering import prepare_data
from src.evaluate import evaluate_model


def train_base_model(X_train, y_train, X_test, y_test, sample_weights):
    print("\n--- Entrenamiento base ---")
    model = xgb.XGBClassifier(
        objective="multi:softprob",
        eval_metric="mlogloss",
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=5,
        gamma=0.1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(
        X_train, y_train,
        sample_weight=sample_weights,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )
    return model


def optimize_hyperparameters(X_train, y_train, sample_weights):
    print("\n--- Optimizacion de hiperparametros (RandomizedSearchCV) ---")
    param_distributions = {
        "n_estimators": [100, 200, 300, 500],
        "max_depth": [3, 4, 5, 6, 8],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.6, 0.7, 0.8, 0.9, 1.0],
        "min_child_weight": [1, 3, 5, 7],
        "gamma": [0, 0.1, 0.2, 0.3],
        "reg_alpha": [0, 0.1, 0.5, 1.0],
        "reg_lambda": [0.5, 1.0, 1.5, 2.0],
    }

    search = RandomizedSearchCV(
        estimator=xgb.XGBClassifier(
            objective="multi:softprob",
            eval_metric="mlogloss",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        param_distributions=param_distributions,
        n_iter=50,
        scoring="f1_weighted",
        cv=5,
        random_state=RANDOM_STATE,
        verbose=1,
        n_jobs=-1,
    )

    search.fit(X_train, y_train, sample_weight=sample_weights)

    print(f"\nMejor F1 (CV): {search.best_score_:.4f}")
    print(f"Mejores parametros: {search.best_params_}")

    return search.best_estimator_, search.best_params_, search.best_score_


def cross_validate(model, X_train, y_train):
    print("\n--- Validacion cruzada del mejor modelo ---")
    cv_scores = cross_val_score(
        model, X_train, y_train,
        cv=5,
        scoring="f1_weighted",
    )
    print(f"F1 promedio (5-fold CV): {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
    return cv_scores


def save_model(model, artifacts):
    artifacts["model"] = model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(artifacts, MODEL_PATH)
    print(f"\nModelo guardado en: {MODEL_PATH}")

    # Verificar carga
    loaded = joblib.load(MODEL_PATH)
    assert loaded["model"] is not None
    assert len(loaded["encoders"]) == len(artifacts["encoders"])
    print("Modelo serializado y verificado correctamente.")


def main():
    # Phase 1: Load data
    df = load_and_prepare()

    # Phase 2: Feature engineering
    X_train, X_test, y_train, y_test, artifacts = prepare_data(df)

    # Compute sample weights for class balancing
    sample_weights = compute_sample_weight("balanced", y_train)

    # Phase 3: Train base model
    base_model = train_base_model(X_train, y_train, X_test, y_test, sample_weights)

    # Phase 3: Hyperparameter optimization
    best_model, best_params, best_score = optimize_hyperparameters(
        X_train, y_train, sample_weights
    )

    # Phase 3: Cross-validation
    cv_scores = cross_validate(best_model, X_train, y_train)

    # Phase 4: Evaluate
    evaluate_model(best_model, X_test, y_test, artifacts, best_params, cv_scores)

    # Phase 5: Save model
    save_model(best_model, artifacts)

    print("\n" + "=" * 60)
    print("  ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()
