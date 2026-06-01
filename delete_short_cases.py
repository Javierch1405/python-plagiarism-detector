from __future__ import annotations

import argparse
from pathlib import Path


def count_code_lines(file_path: Path) -> int:
    code_lines = 0
    with file_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            code_lines += 1
    return code_lines


def iter_files(folder: Path):
    for file_path in sorted(folder.rglob("*")):
        if file_path.is_file():
            yield file_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Elimina archivos dentro de una carpeta que tienen menos de N lineas de codigo."
    )
    parser.add_argument("folder", nargs="?", default="cases", help="Carpeta a revisar")
    parser.add_argument("--threshold", type=int, default=15, help="Numero maximo de lineas de codigo")
    parser.add_argument("--delete", action="store_true", help="Borra los archivos que cumplen la condicion")
    args = parser.parse_args()

    root = Path(args.folder)
    if not root.exists():
        raise SystemExit(f"La carpeta no existe: {root}")

    matches: list[tuple[Path, int]] = []
    for file_path in iter_files(root):
        try:
            line_count = count_code_lines(file_path)
        except UnicodeDecodeError:
            continue
        if line_count < args.threshold:
            matches.append((file_path, line_count))

    if not matches:
        print("No se encontraron archivos para eliminar.")
        return 0

    action = "Eliminado" if args.delete else "Se eliminaria"
    for file_path, line_count in matches:
        print(f"{action}: {file_path} ({line_count} lineas)")
        if args.delete:
            file_path.unlink()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())