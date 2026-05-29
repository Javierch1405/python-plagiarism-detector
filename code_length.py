"""Minimum-length gate for code pairs.

Short snippets are dominated by generic idioms (a bare for/return/assign), so
structural similarity cannot separate a real Type-3 clone from two unrelated
programs that merely share an idiom. We require a minimum number of logical lines
-- counted after `preprocess_code` strips comments, docstrings and blank lines --
before trusting a clone-type verdict.
"""

from __future__ import annotations

from lexical_statistical_layer import preprocess_code

MIN_CODE_LINES = 15


def count_logical_lines(code: str, preprocessed: bool = False) -> int:
    """Count non-blank lines after preprocessing (comments/docstrings removed)."""
    clean = code if preprocessed else preprocess_code(code)
    return sum(1 for line in clean.splitlines() if line.strip())


def meets_min_length(
    code: str, min_lines: int = MIN_CODE_LINES, preprocessed: bool = False
) -> bool:
    """True if `code` has at least `min_lines` logical lines after preprocessing."""
    return count_logical_lines(code, preprocessed=preprocessed) >= min_lines
