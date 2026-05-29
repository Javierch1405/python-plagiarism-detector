"""Capa previa para detectar duplicados tipo 1 (copias casi exactas).

Esta capa normaliza el texto (quita comentarios/docstrings mediante
`preprocess_code`, colapsa espacios y líneas vacías) y proporciona
comparadores rápidos: igualdad exacta y 'similarity ratio' basada en
`difflib.SequenceMatcher`.

No pretende sustituir otras capas; es una eliminación rápida de
candidatos obvios para ahorrar trabajo a las etapas posteriores.
"""

from __future__ import annotations

import re
import difflib
from typing import Tuple, Any

from lexical_statistical_layer import preprocess_code, tokenize_code


def normalize_for_type1(code: str, preprocessed: bool = False) -> str:
    """Normaliza `code` para detección Type-1.

    - Si `preprocessed` es False, llama a `preprocess_code` para quitar
      comentarios y docstrings.
    - Tokeniza y reúne los tokens con un espacio simple, de modo que cualquier
      diferencia de espaciado (incluida la que rodea a operadores, p.ej. `s=0`
      vs `s = 0`) deje de afectar la comparación. Sigue siendo sensible al
      renombrado de identificadores/literales, que es lo propio del Tipo 2.
    - Si el código no se puede tokenizar, cae a un simple colapso de whitespace.
    """
    if not isinstance(code, str):
        raise TypeError("code must be a string")

    clean = code if preprocessed else preprocess_code(code)
    try:
        return " ".join(tokenize_code(clean))
    except ValueError:
        lines = [line.strip() for line in clean.splitlines() if line.strip()]
        joined = "\n".join(lines)
        return re.sub(r"\s+", " ", joined).strip()


def exact_match(code_a: str, code_b: str, preprocessed: bool = False) -> bool:
    """Devuelve True si las versiones normalizadas son idénticas."""
    return normalize_for_type1(code_a, preprocessed) == normalize_for_type1(code_b, preprocessed)


def similarity_ratio(code_a: str, code_b: str, preprocessed: bool = False) -> float:
    """Devuelve un ratio de similitud (0..1) usando SequenceMatcher.

    Es rápido y suficiente para detectar copias casi exactas; para búsquedas
    a gran escala se podría usar shingling/minhash.
    """
    a = normalize_for_type1(code_a, preprocessed)
    b = normalize_for_type1(code_b, preprocessed)

    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0

    return difflib.SequenceMatcher(None, a, b).ratio()


def is_near_duplicate(code_a: str, code_b: str, threshold: float = 0.95, preprocessed: bool = False) -> Tuple[bool, float]:
    """Indica si dos fragmentos son duplicados cercanos según `threshold`.

    Retorna (es_duplicado, ratio).
    """
    ratio = similarity_ratio(code_a, code_b, preprocessed)
    return (ratio >= threshold, ratio)


def analyze_string_prefilter(code_a: str, code_b: str, threshold: float = 0.95, preprocessed: bool = False) -> dict[str, Any]:
    """Analiza dos fragmentos y devuelve métricas para prefiltro tipo‑1.

    Resultado dict contiene:
    - `normalized_a`, `normalized_b`: versiones normalizadas
    - `exact_match`: True si son idénticos
    - `similarity_ratio`: ratio (0..1)
    - `threshold`: umbral usado
    - `is_near_duplicate`: True si ratio >= threshold
    """
    normalized_a = normalize_for_type1(code_a, preprocessed)
    normalized_b = normalize_for_type1(code_b, preprocessed)
    exact = normalized_a == normalized_b

    if not normalized_a and not normalized_b:
        ratio = 1.0
    elif not normalized_a or not normalized_b:
        ratio = 0.0
    else:
        ratio = difflib.SequenceMatcher(None, normalized_a, normalized_b).ratio()
    near = ratio >= threshold

    return {
        "normalized_a": normalized_a,
        "normalized_b": normalized_b,
        "exact_match": exact,
        "similarity_ratio": ratio,
        "threshold": threshold,
        "is_near_duplicate": near,
    }


def print_string_prefilter_report(results: dict[str, Any]) -> None:
    """Imprime un informe compacto similar a las otras capas."""
    print("=== Capa 0: Prefiltro de strings (Tipo 1) ===")
    print(f"- Exact match: {results['exact_match']}")
    print(f"- Similarity ratio: {results['similarity_ratio']:.4f}")
    print(f"- Threshold: {results['threshold']:.2f}")
    print(f"- Near duplicate: {results['is_near_duplicate']}")


if __name__ == "__main__":
    # Demo rápido
    code_a = '''
def sum_even_numbers(values):
    # Sum even numbers
    total = 0
    for number in values:
        if number % 2 == 0:
            total += number
    return total
'''

    code_b = '''
def sum_even_numbers(values):
    total=0
    for number in values:
        if number%2==0:
            total+=number
    return total
'''

    results = analyze_string_prefilter(code_a, code_b, threshold=0.98)
    print_string_prefilter_report(results)
