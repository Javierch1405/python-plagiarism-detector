"""Script one-time: limpia Clone_type en el dataset.

- Rellena Clone_type=0 donde Clone_type está vacío y Label es 0 o 1.
- Elimina las filas con Clone_type=4 (fuera de la taxonomía 0-3).

Uso:
    python fix_clone_type.py
    python fix_clone_type.py --csv cheating_dataset_clean.csv  # ruta personalizada
    python fix_clone_type.py --dry-run                         # solo muestra qué cambiaría
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = SCRIPT_DIR / "cheating_dataset_clean.csv"


def fix_clone_type(csv_path: Path, dry_run: bool = False) -> None:
    rows = []
    filled: list[int] = []
    removed: list[int] = []

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for i, row in enumerate(reader, start=2):  # start=2 porque fila 1 es header
            label = row.get("Label", "").strip()
            clone_type = row.get("Clone_type", "").strip()

            # Si Clone_type=4, eliminar el registro (no se incluye en la salida)
            if clone_type == "4":
                removed.append(i)
                continue

            # Si Clone_type es vacío y Label es 0 o 1, establecer Clone_type=0
            if clone_type == "" and (label == "0" or label == "1"):
                filled.append(i)
                if not dry_run:
                    row["Clone_type"] = "0"

            rows.append(row)

    if not filled and not removed:
        print("No hay filas que corregir.")
        return

    if filled:
        print(f"Filas con Clone_type vacío -> 0: {len(filled)}")
        for line_num in filled:
            print(f"  línea {line_num}")
    if removed:
        print(f"Filas con Clone_type=4 a ELIMINAR: {len(removed)}")
        for line_num in removed:
            print(f"  línea {line_num}")

    if dry_run:
        print("--dry-run activo: no se escribió nada.")
        return

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV actualizado: {csv_path} ({len(rows)} filas conservadas, {len(removed)} eliminadas)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Limpia Clone_type: rellena vacíos con 0 y elimina filas con Clone_type=4.")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--dry-run", action="store_true", help="Muestra qué cambiaría sin modificar el archivo.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    fix_clone_type(args.csv, dry_run=args.dry_run)
