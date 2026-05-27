"""
Entrena modelos para predecir clone_type a partir de metricas de similitud.

Uso basico:
    python train_clone_type_model_v8_keep_clone0.py --csv "results/cheating_dataset_results.csv"

Comparar modelos:
    python train_clone_type_model_v8_keep_clone0.py --csv "results/cheating_dataset_results.csv" --compare

Modelos disponibles:
    - linear_svc
    - logistic_regression
    - random_forest

Notas:
    - La columna objetivo es clone_type.
    - El clone_type 0 se conserva como clase 0.
    - Si aparece clone_type 4, se convierte a 0 por consistencia con el CSV nuevo.
    - El CSV final de predicciones NO muestra clone_type_real_mapeado.
    - Se genera un CSV con predicciones por par.
    - Se generan CSVs con importancia de metricas/features.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Tuple, Any

import numpy as np
import pandas as pd
from joblib import dump

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
    cross_val_predict,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


TARGET_COL = "clone_type"

# Columnas que normalmente NO conviene usar como features porque identifican archivos,
# etiquetas o informacion que podria causar fuga de informacion.
DEFAULT_EXCLUDE_COLS = {
    "clone_type",
    "label",
    "file_a",
    "file_b",
    "filename_a",
    "filename_b",
    "path_a",
    "path_b",
    "student_a",
    "student_b",
    "pair_id",
    "id",
}

PAIR_INFO_CANDIDATES = [
    "file_a",
    "file_b",
    "filename_a",
    "filename_b",
    "path_a",
    "path_b",
    "label",
]


def to_json_safe(obj: Any) -> Any:
    """Convierte objetos de numpy/pandas a tipos serializables en JSON."""
    if isinstance(obj, dict):
        return {str(k): to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_json_safe(v) for v in obj]
    if isinstance(obj, tuple):
        return [to_json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


def load_dataset(csv_path: str | Path) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Lee el CSV, prepara X/y y devuelve tambien el dataframe original.

    Reglas:
        - Usa clone_type como objetivo.
        - Conserva 0 como clase 0.
        - Convierte 4 -> 0, por consistencia con el CSV nuevo.
        - Usa como features columnas numericas y booleanas.
        - Excluye columnas identificadoras y de etiqueta.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"No encontre el CSV en: {csv_path}\n"
            "Revisa la ruta. Ejemplo: --csv \"results/cheating_dataset_results.csv\""
        )

    df = pd.read_csv(csv_path)

    if TARGET_COL not in df.columns:
        raise ValueError(
            f"No existe la columna objetivo '{TARGET_COL}'.\n"
            f"Columnas disponibles: {list(df.columns)}"
        )

    # Objetivo original para entrenamiento.
    y_original = pd.to_numeric(df[TARGET_COL], errors="coerce")

    if y_original.isna().any():
        bad_rows = df[y_original.isna()].index.tolist()
        raise ValueError(
            f"Hay valores no numericos o vacios en {TARGET_COL}. Filas: {bad_rows[:20]}"
        )

    # IMPORTANTE: en esta version el clone_type 0 se queda como 0.
    # Solo convertimos 4 -> 0 por la regla nueva del dataset.
    y = y_original.astype(int).replace({4: 0})

    # Seleccion de features: numericas y booleanas, excluyendo identificadores/target.
    candidate_cols = []
    for col in df.columns:
        if col in DEFAULT_EXCLUDE_COLS:
            continue

        # Intentar convertir a numerico. Si tiene suficientes valores numericos, se usa.
        numeric_col = pd.to_numeric(df[col], errors="coerce")
        non_null_ratio = numeric_col.notna().mean()

        if non_null_ratio >= 0.80:
            candidate_cols.append(col)

    if not candidate_cols:
        raise ValueError(
            "No se encontraron columnas numericas para entrenar. "
            "Revisa que tu CSV tenga metricas numericas."
        )

    X = df[candidate_cols].copy()

    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors="coerce")

    return X, y, df


def build_preprocessors(feature_names: list[str]) -> Tuple[ColumnTransformer, ColumnTransformer]:
    """Crea preprocessors con escalado y sin escalado."""

    scaled_preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                feature_names,
            )
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    unscaled_preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                    ]
                ),
                feature_names,
            )
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    return scaled_preprocessor, unscaled_preprocessor


def build_models(feature_names: list[str], random_state: int = 42) -> Dict[str, Pipeline]:
    """Construye los modelos disponibles."""

    scaled_preprocessor, unscaled_preprocessor = build_preprocessors(feature_names)

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
    }


def evaluate_model(
    model_name: str,
    model: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    output_dir: Path,
    random_state: int = 42,
) -> dict:
    """Entrena/evalua un modelo con holdout y cross-validation."""

    labels = sorted(y.unique().tolist())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=random_state,
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    bal_acc = balanced_accuracy_score(y_test, y_pred)
    report = classification_report(
        y_test,
        y_pred,
        labels=labels,
        output_dict=True,
        zero_division=0,
    )
    report_text = classification_report(
        y_test,
        y_pred,
        labels=labels,
        zero_division=0,
    )
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=random_state,
    )

    cv_results = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring={
            "accuracy": "accuracy",
            "balanced_accuracy": "balanced_accuracy",
            "f1_macro": "f1_macro",
        },
        return_train_score=False,
    )

    results = {
        "model_name": model_name,
        "n_rows": int(len(X)),
        "n_features": int(X.shape[1]),
        "features": list(X.columns),
        "class_distribution_after_mapping": {
            str(k): int(v) for k, v in y.value_counts().sort_index().items()
        },
        "holdout": {
            "accuracy": float(acc),
            "balanced_accuracy": float(bal_acc),
            "classification_report": report,
            "confusion_matrix": cm.tolist(),
            "labels_order": labels,
        },
        "cv": {
            "accuracy_mean": float(cv_results["test_accuracy"].mean()),
            "accuracy_std": float(cv_results["test_accuracy"].std()),
            "balanced_accuracy_mean": float(cv_results["test_balanced_accuracy"].mean()),
            "balanced_accuracy_std": float(cv_results["test_balanced_accuracy"].std()),
            "f1_macro_mean": float(cv_results["test_f1_macro"].mean()),
            "f1_macro_std": float(cv_results["test_f1_macro"].std()),
            "accuracy_by_fold": cv_results["test_accuracy"].tolist(),
            "balanced_accuracy_by_fold": cv_results["test_balanced_accuracy"].tolist(),
            "f1_macro_by_fold": cv_results["test_f1_macro"].tolist(),
        },
    }

    print("\n" + "=" * 80)
    print(f"Modelo: {model_name}")
    print("=" * 80)
    print(f"Filas: {len(X)}")
    print(f"Features usadas: {X.shape[1]}")
    print("Distribucion de clone_type usado para entrenamiento:")
    print({int(k): int(v) for k, v in y.value_counts().sort_index().items()})

    print("\nHoldout test")
    print(f"Accuracy: {acc:.3f}")
    print(f"Balanced accuracy: {bal_acc:.3f}")
    print("\nClassification report:")
    print(report_text)
    print("Matriz de confusion")
    print(f"Orden de etiquetas: {labels}")
    print(cm)

    print("\nCross-validation 5 folds")
    print(
        f"Accuracy: {results['cv']['accuracy_mean']:.3f} "
        f"+- {results['cv']['accuracy_std']:.3f}"
    )
    print(
        f"Balanced accuracy: {results['cv']['balanced_accuracy_mean']:.3f} "
        f"+- {results['cv']['balanced_accuracy_std']:.3f}"
    )
    print(
        f"F1 macro: {results['cv']['f1_macro_mean']:.3f} "
        f"+- {results['cv']['f1_macro_std']:.3f}"
    )

    # Guardar reporte JSON individual.
    report_path = output_dir / f"{model_name}_clone_type_report.json"
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(to_json_safe(results), f, indent=2, ensure_ascii=False)

    return results


def save_cv_errors(
    model_name: str,
    model: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    original_df: pd.DataFrame,
    output_dir: Path,
    random_state: int = 42,
) -> Path:
    """Guarda errores de cross-validation para un modelo especifico."""

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=random_state,
    )

    y_pred_cv = cross_val_predict(model, X, y, cv=cv)
    error_mask = y_pred_cv != y.values

    error_df = pd.DataFrame()
    error_df["row_index"] = original_df.index

    for col in PAIR_INFO_CANDIDATES:
        if col in original_df.columns:
            error_df[col] = original_df[col].values

    if TARGET_COL in original_df.columns:
        error_df["clone_type_original"] = original_df[TARGET_COL].values

    error_df[f"{model_name}_pred"] = y_pred_cv
    error_df[f"{model_name}_acerto"] = y_pred_cv == y.values

    error_df = error_df[error_mask].copy()

    output_path = output_dir / f"{model_name}_cv_errors.csv"
    error_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"- Errores CV {model_name}: {output_path}")

    if len(error_df) == 0:
        print(f"  No hubo errores en CV para {model_name}.")
    else:
        print(f"  Errores encontrados en CV para {model_name}: {len(error_df)}")

    return output_path


def save_cv_predictions_by_pair(
    models: Dict[str, Pipeline],
    X: pd.DataFrame,
    y: pd.Series,
    original_df: pd.DataFrame,
    output_dir: Path,
    random_state: int = 42,
) -> Path:
    """
    Guarda predicciones por par usando cross-validation.

    Importante:
        Cada prediccion se hace con un modelo que NO vio esa fila durante entrenamiento.
        No se guarda clone_type_real_mapeado porque el usuario pidio quitarlo.
    """

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=random_state,
    )

    results_df = pd.DataFrame()
    results_df["row_index"] = original_df.index

    for col in PAIR_INFO_CANDIDATES:
        if col in original_df.columns:
            results_df[col] = original_df[col].values

    if TARGET_COL in original_df.columns:
        results_df["clone_type_original"] = original_df[TARGET_COL].values

    for model_name, model in models.items():
        y_pred = cross_val_predict(model, X, y, cv=cv)
        results_df[f"{model_name}_pred"] = y_pred
        results_df[f"{model_name}_acerto"] = y_pred == y.values

    output_path = output_dir / "predicciones_por_par_cv.csv"
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"- Predicciones por par CV: {output_path}")
    return output_path


def get_feature_names_from_pipeline(model: Pipeline, X: pd.DataFrame) -> list[str]:
    """Obtiene nombres de features despues del preprocesamiento."""
    preprocess = model.named_steps.get("preprocess")

    if preprocess is None:
        return list(X.columns)

    try:
        return list(preprocess.get_feature_names_out())
    except Exception:
        return list(X.columns)


def save_linear_svc_feature_importance(
    fitted_model: Pipeline,
    X: pd.DataFrame,
    output_dir: Path,
    top_n: int = 10,
) -> Tuple[Path | None, Path | None]:
    """
    Guarda importancia de features por clase para LinearSVC.

    Para LinearSVC:
        - coefficient positivo: empuja hacia esa clase.
        - coefficient negativo: aleja de esa clase.
        - importance_abs: fuerza del peso sin importar signo.
    """

    clf = fitted_model.named_steps.get("model")

    if clf is None or not hasattr(clf, "coef_"):
        print("- LinearSVC feature importance: no disponible.")
        return None, None

    feature_names = get_feature_names_from_pipeline(fitted_model, X)
    classes = list(clf.classes_)

    rows = []
    for class_index, class_label in enumerate(classes):
        coefficients = clf.coef_[class_index]

        for feature, coef in zip(feature_names, coefficients):
            rows.append(
                {
                    "clone_type": int(class_label),
                    "feature": feature,
                    "coefficient": float(coef),
                    "importance_abs": float(abs(coef)),
                    "interpretation": "empuja_hacia_la_clase" if coef > 0 else "aleja_de_la_clase",
                }
            )

    importance_df = pd.DataFrame(rows).sort_values(
        by=["clone_type", "importance_abs"],
        ascending=[True, False],
    )

    full_path = output_dir / "linear_svc_feature_importance_by_class.csv"
    importance_df.to_csv(full_path, index=False, encoding="utf-8-sig")

    top_df = (
        importance_df.sort_values(
            by=["clone_type", "importance_abs"],
            ascending=[True, False],
        )
        .groupby("clone_type", as_index=False)
        .head(top_n)
    )

    top_path = output_dir / "linear_svc_top_features_by_class.csv"
    top_df.to_csv(top_path, index=False, encoding="utf-8-sig")

    print(f"- Importancia LinearSVC completa: {full_path}")
    print(f"- Top {top_n} features LinearSVC por clase: {top_path}")

    return full_path, top_path


def save_random_forest_feature_importance(
    fitted_model: Pipeline,
    X: pd.DataFrame,
    output_dir: Path,
    top_n: int = 15,
) -> Tuple[Path | None, Path | None]:
    """
    Guarda importancia global de features para Random Forest.

    Nota:
        Random Forest no da importancia por clase de forma directa con feature_importances_.
        Da importancia global para todo el modelo.
    """

    clf = fitted_model.named_steps.get("model")

    if clf is None or not hasattr(clf, "feature_importances_"):
        print("- Random Forest feature importance: no disponible.")
        return None, None

    feature_names = get_feature_names_from_pipeline(fitted_model, X)
    importances = clf.feature_importances_

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    ).sort_values(by="importance", ascending=False)

    full_path = output_dir / "random_forest_feature_importance.csv"
    importance_df.to_csv(full_path, index=False, encoding="utf-8-sig")

    top_path = output_dir / "random_forest_top_features.csv"
    importance_df.head(top_n).to_csv(top_path, index=False, encoding="utf-8-sig")

    print(f"- Importancia Random Forest completa: {full_path}")
    print(f"- Top {top_n} features Random Forest: {top_path}")

    return full_path, top_path


def save_model_comparison_csv(comparison: dict, output_dir: Path) -> Path:
    """Guarda una tabla resumida de comparacion de modelos."""

    rows = []
    for model_name, result in comparison.items():
        rows.append(
            {
                "model": model_name,
                "holdout_accuracy": result["holdout"]["accuracy"],
                "holdout_balanced_accuracy": result["holdout"]["balanced_accuracy"],
                "cv_accuracy_mean": result["cv"]["accuracy_mean"],
                "cv_accuracy_std": result["cv"]["accuracy_std"],
                "cv_balanced_accuracy_mean": result["cv"]["balanced_accuracy_mean"],
                "cv_balanced_accuracy_std": result["cv"]["balanced_accuracy_std"],
                "cv_f1_macro_mean": result["cv"]["f1_macro_mean"],
                "cv_f1_macro_std": result["cv"]["f1_macro_std"],
            }
        )

    comparison_df = pd.DataFrame(rows).sort_values(
        by="cv_f1_macro_mean",
        ascending=False,
    )

    output_path = output_dir / "model_comparison.csv"
    comparison_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"- Comparacion CSV: {output_path}")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Entrena modelos para predecir clone_type."
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Ruta al CSV. Ejemplo: results/cheating_dataset_results.csv",
    )

    parser.add_argument(
        "--model",
        default="linear_svc",
        choices=["linear_svc", "logistic_regression", "random_forest"],
        help="Modelo a entrenar si no usas --compare.",
    )

    parser.add_argument(
        "--compare",
        action="store_true",
        help="Evalua y compara linear_svc, logistic_regression y random_forest.",
    )

    parser.add_argument(
        "--output-dir",
        default="model_outputs",
        help="Carpeta donde se guardan modelos, reportes y CSVs.",
    )

    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Semilla para reproducibilidad.",
    )

    parser.add_argument(
        "--top-n-features",
        type=int,
        default=10,
        help="Numero de features importantes por clase para LinearSVC.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    X, y, original_df = load_dataset(args.csv)
    models = build_models(feature_names=list(X.columns), random_state=args.random_state)

    if args.compare:
        models_to_run = models
    else:
        models_to_run = {args.model: models[args.model]}

    comparison = {}

    for model_name, model in models_to_run.items():
        result = evaluate_model(
            model_name=model_name,
            model=model,
            X=X,
            y=y,
            output_dir=output_dir,
            random_state=args.random_state,
        )
        comparison[model_name] = result

    # Elegir mejor modelo por F1 macro CV.
    best_model_name = max(
        comparison,
        key=lambda name: comparison[name]["cv"]["f1_macro_mean"],
    )

    print("\n" + "#" * 80)
    print(f"Mejor modelo por F1 macro en CV: {best_model_name}")
    print(f"F1 macro CV: {comparison[best_model_name]['cv']['f1_macro_mean']:.3f}")
    print("#" * 80)

    # Entrenar el mejor modelo con TODO el dataset para guardarlo como modelo final.
    best_model = models[best_model_name]
    best_model.fit(X, y)

    model_path = output_dir / f"{best_model_name}_clone_type_model.joblib"
    dump(best_model, model_path)

    features_path = output_dir / f"{best_model_name}_features.json"
    with features_path.open("w", encoding="utf-8") as f:
        json.dump(list(X.columns), f, indent=2, ensure_ascii=False)

    # Guardar comparacion completa.
    comparison_json_path = output_dir / "model_comparison.json"
    with comparison_json_path.open("w", encoding="utf-8") as f:
        json.dump(to_json_safe(comparison), f, indent=2, ensure_ascii=False)

    # Guardar comparacion resumida en CSV.
    save_model_comparison_csv(comparison, output_dir)

    # Guardar predicciones por par para TODOS los modelos disponibles, no solo el mejor.
    save_cv_predictions_by_pair(
        models=models,
        X=X,
        y=y,
        original_df=original_df,
        output_dir=output_dir,
        random_state=args.random_state,
    )

    # Guardar errores CV del mejor modelo.
    save_cv_errors(
        model_name=best_model_name,
        model=models[best_model_name],
        X=X,
        y=y,
        original_df=original_df,
        output_dir=output_dir,
        random_state=args.random_state,
    )

    # Guardar importancia de metricas/features para modelos interpretables.
    # LinearSVC: importancia por clase.
    linear_model = models["linear_svc"]
    linear_model.fit(X, y)
    save_linear_svc_feature_importance(
        fitted_model=linear_model,
        X=X,
        output_dir=output_dir,
        top_n=args.top_n_features,
    )

    # Random Forest: importancia global.
    rf_model = models["random_forest"]
    rf_model.fit(X, y)
    save_random_forest_feature_importance(
        fitted_model=rf_model,
        X=X,
        output_dir=output_dir,
        top_n=max(args.top_n_features, 15),
    )

    print("\nArchivos guardados:")
    print(f"- Modelo final: {model_path}")
    print(f"- Features: {features_path}")
    print(f"- Comparacion JSON: {comparison_json_path}")
    print(f"- Comparacion CSV: {output_dir / 'model_comparison.csv'}")
    print(f"- Predicciones por par CV: {output_dir / 'predicciones_por_par_cv.csv'}")
    print(f"- Errores CV mejor modelo: {output_dir / f'{best_model_name}_cv_errors.csv'}")
    print(f"- Top features LinearSVC por clase: {output_dir / 'linear_svc_top_features_by_class.csv'}")
    print(f"- Importancia Random Forest: {output_dir / 'random_forest_top_features.csv'}")


if __name__ == "__main__":
    main()
