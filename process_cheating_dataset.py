"""Procesa el dataset de plagio y exporta métricas por par de código.

Lee `cheating_dataset_clean.csv`, carga los archivos en `../cases/` y calcula las
métricas de las capas existentes del proyecto.

El resultado se exporta a `results/cheating_dataset_results.csv`.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from embeddings import analyze_embedding_similarity
from lexical_statistical_layer import analyze_lexical_statistical_similarity, preprocess_code
from semantic_layer import analyze_semantic_similarity
from structural_layer import analyze_structural_similarity
from string_prefilter import analyze_string_prefilter

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_CASES_DIR = PROJECT_ROOT / "cases"
DEFAULT_INPUT_CSV = SCRIPT_DIR / "cheating_dataset_clean.csv"
DEFAULT_OUTPUT_CSV = SCRIPT_DIR / "results" / "cheating_dataset_results.csv"


def parse_dataset_csv(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV de entrada no encontrado: {csv_path}")

    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for index, row in enumerate(reader, start=1):
            if "File_1" not in row or "File_2" not in row or "Label" not in row:
                raise ValueError("CSV debe contener columnas File_1, File_2, Label y Clone_type")
            rows.append({
                "file_a": row["File_1"].strip(),
                "file_b": row["File_2"].strip(),
                "label": row["Label"].strip(),
                "clone_type": row.get("Clone_type", "").strip(),
                "row_index": index,
            })
    return rows


def load_source_file(cases_dir: Path, filename: str) -> str:
    path = cases_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Archivo de caso no encontrado: {path}")
    return path.read_text(encoding="utf-8")


def normalize_clone_type(label: str, clone_type: str) -> int:
    try:
        label_value = int(label)
    except ValueError:
        label_value = 0

    if label_value != 1:
        return 0

    try:
        return int(clone_type) if clone_type else 0
    except ValueError:
        return 0


def build_metric_row(
    file_a: str,
    file_b: str,
    label: int,
    clone_type: int,
    lexical_results: dict[str, Any],
    structural_results: dict[str, Any],
    semantic_results: dict[str, Any],
    embedding_results: dict[str, Any],
    string_results: dict[str, Any],
    error: str = "",
) -> dict[str, Any]:
    return {
        "file_a": file_a,
        "file_b": file_b,
        "label": label,
        "clone_type": clone_type,
        "error": error,
        "string_exact_match": bool(string_results.get("exact_match", False)),
        "string_similarity_ratio": float(string_results.get("similarity_ratio", 0.0)),
        "jaccard_similarity": float(lexical_results.get("jaccard_similarity", 0.0)),
        "tfidf_cosine_similarity": float(lexical_results.get("tfidf_cosine_similarity", 0.0)),
        "markov_similarity": float(lexical_results.get("markov_similarity", 0.0)),
        "kl_divergence_a_to_b": float(lexical_results.get("kl_divergence_a_to_b", 0.0)),
        "kl_divergence_b_to_a": float(lexical_results.get("kl_divergence_b_to_a", 0.0)),
        "lexical_statistical_score": float(lexical_results.get("lexical_statistical_score", 0.0)),
        "ast_node_type_jaccard": float(structural_results.get("ast_node_type_jaccard", 0.0)),
        "ast_sequence_similarity": float(structural_results.get("ast_sequence_similarity", 0.0)),
        "ast_node_count_similarity": float(structural_results.get("ast_node_count_similarity", 0.0)),
        "ast_depth_similarity": float(structural_results.get("ast_depth_similarity", 0.0)),
        "tree_edit_distance": structural_results.get("tree_edit_distance", ""),
        "tree_edit_similarity": float(structural_results.get("tree_edit_similarity", 0.0)),
        "apted_available": structural_results.get("apted_available", "no"),
        "apted_tree_edit_distance": structural_results.get("apted_tree_edit_distance", ""),
        "apted_tree_edit_similarity": structural_results.get("apted_tree_edit_similarity", ""),
        "structural_score": float(structural_results.get("structural_score", 0.0)),
        "semantic_runnable": semantic_results.get("semantic_runnable", "no"),
        "semantic_reason": semantic_results.get("semantic_reason", ""),
        "semantic_function_a": semantic_results.get("function_a", ""),
        "semantic_function_b": semantic_results.get("function_b", ""),
        "semantic_tested_arity": semantic_results.get("tested_arity", ""),
        "semantic_total_cases": int(semantic_results.get("total_cases", 0)),
        "semantic_both_return_count": int(semantic_results.get("both_return_count", 0)),
        "semantic_matching_return_count": int(semantic_results.get("matching_return_count", 0)),
        "semantic_successful_overlap": float(semantic_results.get("successful_overlap", 0.0)),
        "semantic_output_similarity": float(semantic_results.get("output_similarity", 0.0)),
        "semantic_score": float(semantic_results.get("semantic_score", 0.0)),
        "embedding_model": embedding_results.get("embedding_model", "tfidf"),
        "embedding_feature_count": int(embedding_results.get("embedding_feature_count", 0)),
        "embedding_cosine_similarity": float(embedding_results.get("embedding_cosine_similarity", 0.0)),
        "embedding_score": float(embedding_results.get("embedding_score", 0.0)),
    }


def compute_metrics_for_pair(cases_dir: Path, file_a: str, file_b: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    code_a = load_source_file(cases_dir, file_a)
    code_b = load_source_file(cases_dir, file_b)

    clean_a = preprocess_code(code_a)
    clean_b = preprocess_code(code_b)

    lexical_results = analyze_lexical_statistical_similarity(clean_a, clean_b, preprocessed=True)
    structural_results = analyze_structural_similarity(clean_a, clean_b, preprocessed=True)
    semantic_results = analyze_semantic_similarity(clean_a, clean_b, preprocessed=True)
    embedding_results = analyze_embedding_similarity(clean_a, clean_b, preprocessed=True)
    string_results = analyze_string_prefilter(clean_a, clean_b, threshold=0.95, preprocessed=True)

    return lexical_results, structural_results, semantic_results, embedding_results, string_results


def export_to_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("No hay filas para exportar.")
        return

    fieldnames = list(rows[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(
    input_csv: Path,
    output_csv: Path,
    cases_dir: Path,
    only_plagiarized: bool,
) -> None:
    dataset_rows = parse_dataset_csv(input_csv)
    results: list[dict[str, Any]] = []

    for row in dataset_rows:
        file_a = row["file_a"]
        file_b = row["file_b"]
        label = int(row["label"]) if row["label"].isdigit() else 0
        clone_type = normalize_clone_type(row["label"], row["clone_type"])

        if only_plagiarized and label != 1:
            continue

        try:
            lexical_results, structural_results, semantic_results, embedding_results, string_results = compute_metrics_for_pair(
                cases_dir,
                file_a,
                file_b,
            )
            result_row = build_metric_row(
                file_a,
                file_b,
                label,
                clone_type,
                lexical_results,
                structural_results,
                semantic_results,
                embedding_results,
                string_results,
            )
        except Exception as exc:
            result_row = build_metric_row(
                file_a,
                file_b,
                label,
                clone_type,
                {},
                {},
                {},
                {},
                {},
                error=str(exc),
            )

        results.append(result_row)

    export_to_csv(results, output_csv)
    print(f"Exportado {len(results)} filas a {output_csv}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Procesa cheating_dataset_clean.csv y exporta métricas de plagio.")
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT_CSV, help="CSV de pares de código")
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV, help="CSV de salida con métricas")
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES_DIR, help="Directorio de archivos de código")
    parser.add_argument("--only-plagiarized", action="store_true", help="Exporta solo los pares con label 1")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args.input_csv, args.output_csv, args.cases_dir, args.only_plagiarized)


if __name__ == "__main__":
    main()
