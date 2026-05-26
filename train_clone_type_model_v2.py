"""
Entrena modelos para predecir `clone_type` usando el CSV de métricas de similitud/plagio.

Regla aplicada:
- clone_type 0 -> 3
- clone_type 4 -> 3

Uso:
    python train_clone_type_model.py --csv "cheating_dataset_results(2).csv"

Opcional:
    python train_clone_type_model.py --csv "cheating_dataset_results(2).csv" --model linear_svc
    python train_clone_type_model.py --csv "cheating_dataset_results(2).csv" --model random_forest
    python train_clone_type_model.py --csv "cheating_dataset_results(2).csv" --model logistic_regression
    python train_clone_type_model.py --csv "cheating_dataset_results(2).csv" --compare
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Tuple

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


DROP_ALWAYS = {
    "clone_type",   # objetivo
    "file_a",       # identificadores: pueden causar fuga o memorizar pares
    "file_b",
    "label",        # en este CSV es constante; no aporta
}


def load_dataset(csv_path: Path, target_col: str = "clone_type") -> Tuple[pd.DataFrame, pd.Series]:
    """Lee el CSV, recodifica la variable objetivo y regresa X, y."""
    df = pd.read_csv(csv_path)

    if target_col not in df.columns:
        raise ValueError(f"No encontré la columna objetivo '{target_col}'. Columnas: {list(df.columns)}")

    # Convertir clone_type a numérico y aplicar la regla solicitada:
    # 0 -> 3 y 4 -> 3
    y = pd.to_numeric(df[target_col], errors="coerce")
    if y.isna().any():
        bad_rows = df.loc[y.isna(), [target_col]].head(10)
        raise ValueError(f"Hay valores no numéricos en '{target_col}'. Ejemplos:\n{bad_rows}")

    y = y.astype(int).replace({0: 3, 4: 3})

    # Para un primer modelo robusto, usamos solamente columnas numéricas y booleanas.
    # Las columnas de texto como semantic_reason o embedding_model se excluyen para evitar ruido.
    feature_cols = []
    for col in df.columns:
        if col in DROP_ALWAYS:
            continue
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]):
            feature_cols.append(col)

    if not feature_cols:
        raise ValueError("No encontré columnas numéricas/booleanas para entrenar.")

    X = df[feature_cols].copy()

    # Convertir booleanos a 0/1 y forzar numéricos.
    for col in X.columns:
        if pd.api.types.is_bool_dtype(X[col]):
            X[col] = X[col].astype(int)
        else:
            X[col] = pd.to_numeric(X[col], errors="coerce")

    # Quitar columnas completamente vacías o constantes.
    # En este CSV, por ejemplo, error y algunas columnas APTED vienen totalmente vacías.
    useful_cols = []
    for col in X.columns:
        non_null = X[col].dropna()
        if len(non_null) > 0 and non_null.nunique() > 1:
            useful_cols.append(col)

    X = X[useful_cols].copy()

    if X.empty:
        raise ValueError("No hay columnas útiles para entrenar después de limpiar el CSV.")

    return X, y


def make_models(random_state: int = 42) -> Dict[str, Pipeline]:
    """Define modelos candidatos."""
    numeric_preprocess_scaled = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    numeric_preprocess_unscaled = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    scaled_preprocessor = ColumnTransformer(
        transformers=[("num", numeric_preprocess_scaled, slice(0, None))],
        remainder="drop",
    )

    unscaled_preprocessor = ColumnTransformer(
        transformers=[("num", numeric_preprocess_unscaled, slice(0, None))],
        remainder="drop",
    )

    return {
        "linear_svc": Pipeline(
            steps=[
                ("preprocess", scaled_preprocessor),
                (
                    "model",
                    LinearSVC(
                        class_weight="balanced",
                        C=1.0,
                        max_iter=50000,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "logistic_regression": Pipeline(
            steps=[
                ("preprocess", scaled_preprocessor),
                (
                    "model",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=5000,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocess", unscaled_preprocessor),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=200,
                        class_weight="balanced",
                        max_depth=None,
                        min_samples_leaf=2,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "extra_trees": Pipeline(
            steps=[
                ("preprocess", unscaled_preprocessor),
                (
                    "model",
                    ExtraTreesClassifier(
                        n_estimators=200,
                        class_weight="balanced",
                        max_depth=None,
                        min_samples_leaf=2,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
    }


def evaluate_model(name: str, model: Pipeline, X: pd.DataFrame, y: pd.Series, random_state: int = 42) -> dict:
    """Evalúa con holdout estratificado y cross-validation."""
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=random_state,
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    cv_scores = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring={
            "accuracy": "accuracy",
            "balanced_accuracy": "balanced_accuracy",
            "f1_macro": "f1_macro",
        },
        n_jobs=1,
    )

    labels = sorted(y.unique().tolist())

    report = {
        "model": name,
        "target_distribution_after_mapping": y.value_counts().sort_index().to_dict(),
        "features_used": list(X.columns),
        "n_rows": int(len(X)),
        "n_features": int(X.shape[1]),
        "holdout_accuracy": float(accuracy_score(y_test, y_pred)),
        "holdout_balanced_accuracy": float(balanced_accuracy_score(y_test, y_pred)),
        "holdout_classification_report": classification_report(y_test, y_pred, digits=3),
        "holdout_confusion_matrix_labels": labels,
        "holdout_confusion_matrix": confusion_matrix(y_test, y_pred, labels=labels).tolist(),
        "cv_accuracy_mean": float(np.mean(cv_scores["test_accuracy"])),
        "cv_accuracy_std": float(np.std(cv_scores["test_accuracy"])),
        "cv_balanced_accuracy_mean": float(np.mean(cv_scores["test_balanced_accuracy"])),
        "cv_balanced_accuracy_std": float(np.std(cv_scores["test_balanced_accuracy"])),
        "cv_f1_macro_mean": float(np.mean(cv_scores["test_f1_macro"])),
        "cv_f1_macro_std": float(np.std(cv_scores["test_f1_macro"])),
    }

    return report


def print_report(report: dict) -> None:
    print("\n" + "=" * 80)
    print(f"Modelo: {report['model']}")
    print("=" * 80)
    print(f"Filas: {report['n_rows']}")
    print(f"Features usadas: {report['n_features']}")
    print(f"Distribución de clone_type después de mapear 0 y 4 a 3:")
    print(report["target_distribution_after_mapping"])

    print("\nHoldout test")
    print(f"Accuracy: {report['holdout_accuracy']:.3f}")
    print(f"Balanced accuracy: {report['holdout_balanced_accuracy']:.3f}")
    print("\nClassification report:")
    print(report["holdout_classification_report"])

    print("Matriz de confusión")
    print(f"Orden de etiquetas: {report['holdout_confusion_matrix_labels']}")
    print(np.array(report["holdout_confusion_matrix"]))

    print("\nCross-validation 5 folds")
    print(f"Accuracy: {report['cv_accuracy_mean']:.3f} ± {report['cv_accuracy_std']:.3f}")
    print(f"Balanced accuracy: {report['cv_balanced_accuracy_mean']:.3f} ± {report['cv_balanced_accuracy_std']:.3f}")
    print(f"F1 macro: {report['cv_f1_macro_mean']:.3f} ± {report['cv_f1_macro_std']:.3f}")


def save_artifacts(model: Pipeline, report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / f"{report['model']}_clone_type_model.joblib"
    report_path = output_dir / f"{report['model']}_clone_type_report.json"
    features_path = output_dir / f"{report['model']}_features.json"

    joblib.dump(model, model_path)

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    with features_path.open("w", encoding="utf-8") as f:
        json.dump(report["features_used"], f, indent=2, ensure_ascii=False)

    print("\nArchivos guardados:")
    print(f"- Modelo: {model_path}")
    print(f"- Reporte: {report_path}")
    print(f"- Features: {features_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path, help="Ruta del CSV de entrada.")
    parser.add_argument(
        "--model",
        default="linear_svc",
        choices=["linear_svc", "logistic_regression", "random_forest", "extra_trees"],
        help="Modelo a entrenar.",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Evalúa todos los modelos y guarda el mejor según F1 macro en cross-validation.",
    )
    parser.add_argument("--output-dir", default=Path("model_outputs"), type=Path)
    parser.add_argument("--random-state", default=42, type=int)
    args = parser.parse_args()

    X, y = load_dataset(args.csv)
    models = make_models(random_state=args.random_state)

    if args.compare:
        reports = []
        fitted_models = {}

        for model_name, model in models.items():
            report = evaluate_model(model_name, model, X, y, random_state=args.random_state)
            print_report(report)
            reports.append(report)

            # Reentrenar con todos los datos para guardar una versión final.
            model.fit(X, y)
            fitted_models[model_name] = model

        best_report = max(reports, key=lambda r: r["cv_f1_macro_mean"])
        best_name = best_report["model"]
        print("\n" + "#" * 80)
        print(f"Mejor modelo por F1 macro en CV: {best_name}")
        print(f"F1 macro CV: {best_report['cv_f1_macro_mean']:.3f}")
        print("#" * 80)

        save_artifacts(fitted_models[best_name], best_report, args.output_dir)

        comparison_path = args.output_dir / "model_comparison.json"
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with comparison_path.open("w", encoding="utf-8") as f:
            json.dump(reports, f, indent=2, ensure_ascii=False)
        print(f"- Comparación: {comparison_path}")

    else:
        model = models[args.model]
        report = evaluate_model(args.model, model, X, y, random_state=args.random_state)
        print_report(report)

        # Entrenar modelo final con todos los datos antes de guardarlo.
        model.fit(X, y)
        save_artifacts(model, report, args.output_dir)


if __name__ == "__main__":
    main()
