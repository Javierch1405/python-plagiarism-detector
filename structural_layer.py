"""Structural layer for Python code similarity based on AST features.

This module implements a lightweight Layer 2. It uses Python's built-in AST to
compare structural patterns, but it intentionally avoids heavier techniques such
as APTED or full Tree Edit Distance.
"""

from __future__ import annotations

import ast
from collections import Counter
from difflib import SequenceMatcher
from typing import Any

from lexical_statistical_layer import preprocess_code


IGNORED_AST_NODE_TYPES = {"Load", "Store", "Del"}


def parse_python_ast(code: str) -> ast.AST:
    """Preprocess Python code and parse it into an AST."""
    if not isinstance(code, str):
        raise TypeError("code must be a string")

    clean_code = preprocess_code(code)
    if not clean_code:
        return ast.Module(body=[], type_ignores=[])

    try:
        return ast.parse(clean_code)
    except SyntaxError as exc:
        raise ValueError(f"Could not parse Python code: {exc}") from exc


def ast_node_type_sequence(tree: ast.AST) -> list[str]:
    """Return a preorder-like sequence of AST node type names."""
    sequence: list[str] = []

    def visit(node: ast.AST) -> None:
        node_type = type(node).__name__
        if node_type not in IGNORED_AST_NODE_TYPES:
            sequence.append(node_type)
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)
    return sequence


def ast_node_distribution(node_types: list[str]) -> dict[str, float]:
    """Convert AST node types into a probability distribution."""
    if not node_types:
        return {}

    counts = Counter(node_types)
    total = len(node_types)
    return {node_type: count / total for node_type, count in counts.items()}


def ast_jaccard_similarity(nodes_a: list[str], nodes_b: list[str]) -> float:
    """Compute Jaccard similarity over unique AST node types."""
    set_a = set(nodes_a)
    set_b = set(nodes_b)

    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0

    return len(set_a & set_b) / len(set_a | set_b)


def ast_sequence_similarity(nodes_a: list[str], nodes_b: list[str]) -> float:
    """Compare AST preorder node sequences using SequenceMatcher."""
    if not nodes_a and not nodes_b:
        return 1.0
    if not nodes_a or not nodes_b:
        return 0.0

    return SequenceMatcher(None, nodes_a, nodes_b).ratio()


def ast_depth(tree: ast.AST) -> int:
    """Return the maximum depth of an AST."""
    children = list(ast.iter_child_nodes(tree))
    if not children:
        return 1

    return 1 + max(ast_depth(child) for child in children)


def numeric_similarity(value_a: int, value_b: int) -> float:
    """Compare two non-negative numeric AST properties as a 0-1 similarity."""
    if value_a < 0 or value_b < 0:
        raise ValueError("numeric values must be non-negative")
    if value_a == 0 and value_b == 0:
        return 1.0

    denominator = max(value_a, value_b)
    if denominator == 0:
        return 0.0

    return 1.0 - (abs(value_a - value_b) / denominator)


def analyze_structural_similarity(code_a: str, code_b: str) -> dict[str, Any]:
    """Run Layer-2 AST-based structural similarity metrics."""
    tree_a = parse_python_ast(code_a)
    tree_b = parse_python_ast(code_b)

    node_types_a = ast_node_type_sequence(tree_a)
    node_types_b = ast_node_type_sequence(tree_b)

    node_count_a = len(node_types_a)
    node_count_b = len(node_types_b)
    depth_a = ast_depth(tree_a)
    depth_b = ast_depth(tree_b)

    node_type_jaccard = ast_jaccard_similarity(node_types_a, node_types_b)
    sequence_similarity = ast_sequence_similarity(node_types_a, node_types_b)
    node_count_similarity = numeric_similarity(node_count_a, node_count_b)
    depth_similarity = numeric_similarity(depth_a, depth_b)

    structural_score = (
        0.35 * node_type_jaccard
        + 0.35 * sequence_similarity
        + 0.15 * node_count_similarity
        + 0.15 * depth_similarity
    )

    return {
        "ast_node_types_a": node_types_a,
        "ast_node_types_b": node_types_b,
        "ast_node_distribution_a": ast_node_distribution(node_types_a),
        "ast_node_distribution_b": ast_node_distribution(node_types_b),
        "ast_node_count_a": node_count_a,
        "ast_node_count_b": node_count_b,
        "ast_depth_a": depth_a,
        "ast_depth_b": depth_b,
        "ast_node_type_jaccard": node_type_jaccard,
        "ast_sequence_similarity": sequence_similarity,
        "ast_node_count_similarity": node_count_similarity,
        "ast_depth_similarity": depth_similarity,
        "structural_score": structural_score,
    }


def print_structural_report(results: dict[str, Any]) -> None:
    """Print a compact report for Layer-2 structural metrics."""
    print("=== Capa 2: Similitud estructural basada en AST ===")
    print(f"- AST node type Jaccard: {results['ast_node_type_jaccard']:.4f}")
    print(f"- AST sequence similarity: {results['ast_sequence_similarity']:.4f}")
    print(f"- AST node count similarity: {results['ast_node_count_similarity']:.4f}")
    print(f"- AST depth similarity: {results['ast_depth_similarity']:.4f}")
    print(f"- Structural score: {results['structural_score']:.4f}")


if __name__ == "__main__":
    code_a = """
def sum_even_numbers(values):
    total = 0
    for number in values:
        if number % 2 == 0:
            total += number
    return total
"""

    code_b = """
def add_pairs(items):
    result = 0
    for item in items:
        if item % 2 == 0:
            result = result + item
    return result
"""

    analysis = analyze_structural_similarity(code_a, code_b)
    print_structural_report(analysis)
