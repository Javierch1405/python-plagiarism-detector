"""Checker de longitud minima para los codigos del dataset.

Cuenta las lineas logicas (tras `preprocess_code`: sin comentarios, docstrings ni
lineas en blanco) de cada archivo .py y marca los que estan por debajo del minimo.
Pensado para correrlo sobre los codigos que vas a ir agregando al dataset.

Uso:
    python check_min_length.py cases/                 # revisa un directorio (recursivo *.py)
    python check_min_length.py a.py b.py              # revisa archivos sueltos
    python check_min_length.py cases/ --min-lines 15  # umbral personalizado
    python check_min_length.py cases/ --only-failures # solo lista los que no cumplen

Codigo de salida: 1 si algun archivo no cumple (util para un pre-commit/CI), 0 si todos pasan.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from code_length import MIN_CODE_LINES, count_logical_lines


def iter_py_files(paths: list[Path]):
    seen: set[Path] = set()
    for path in paths:
        if path.is_dir():
            candidates = sorted(path.rglob("*.py"))
        elif path.suffix == ".py":
            candidates = [path]
        else:
            print(f"[skip] {path}: no es .py ni directorio")
            continue
        for f in candidates:
            resolved = f.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield f


def check_paths(paths: list[Path], min_lines: int, only_failures: bool) -> int:
    files = list(iter_py_files(paths))
    if not files:
        print("No se encontraron archivos .py en las rutas dadas.")
        return 0

    failures = 0
    for f in files:
        try:
            n = count_logical_lines(f.read_text(encoding="utf-8"))
        except Exception as exc:  # archivos del dataset pueden venir mal formados
            print(f"ERROR {f}: no se pudo procesar ({type(exc).__name__}: {exc})")
            failures += 1
            continue

        ok = n >= min_lines
        if not ok:
            failures += 1
        if ok and only_failures:
            continue
        status = "OK   " if ok else "CORTO"
        print(f"{status} {n:4d} lineas  {f}")

    print(f"\n{len(files)} archivo(s) revisados; {failures} por debajo de {min_lines} lineas.")
    return 1 if failures else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verifica que los archivos .py cumplan la longitud minima de lineas logicas."
    )
    parser.add_argument("paths", type=Path, nargs="+", help="Archivos .py o directorios a revisar.")
    parser.add_argument(
        "--min-lines",
        type=int,
        default=MIN_CODE_LINES,
        help=f"Minimo de lineas logicas (default: {MIN_CODE_LINES}).",
    )
    parser.add_argument(
        "--only-failures",
        action="store_true",
        help="Imprime solo los archivos que no cumplen el minimo.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    exit_code = check_paths(args.paths, args.min_lines, args.only_failures)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
