"""Entry point: compute and print the minimum cable length."""

import sys
from pathlib import Path

# Allow running as   python main.py   from the project root.
sys.path.insert(0, str(Path(__file__).parent))

from src.mst import (  # noqa: E402
    extract_edges,
    kruskal,
    load_adjacency_matrix,
)

SEPARATOR = "─" * 48


def print_matrix(matrix: list[list[int]]) -> None:
    """Pretty-print the adjacency matrix."""
    n = len(matrix)
    header = "     " + "  ".join(f"[{j}]" for j in range(n))
    print(header)
    for i, row in enumerate(matrix):
        cells = "  ".join(f"{v:3}" for v in row)
        print(f"[{i}]  {cells}")


def main() -> None:
    """Read islands.csv, show step-by-step progress, print the result."""
    default_path = Path(__file__).parent / "data" / "islands.csv"
    filepath = sys.argv[1] if len(sys.argv) > 1 else str(default_path)

    print(SEPARATOR)
    print("Венеція — прокладання оптоволокна")
    print(SEPARATOR)

    print(f"\nЗчитуємо файл: {filepath}")
    try:
        matrix = load_adjacency_matrix(filepath)
    except (FileNotFoundError, ValueError) as exc:
        print(f"\nПомилка: {exc}", file=sys.stderr)
        sys.exit(1)

    n = len(matrix)
    print(f"Завантажено матрицю суміжності  ({n}×{n})  — {n} острів(ів)\n")
    print_matrix(matrix)

    if n <= 1:
        print("\nЛише один острів — кабель не потрібен. Довжина: 0")
        return

    edges = extract_edges(matrix)
    print(f"\n{SEPARATOR}")
    print(f"Знайдено {len(edges)} можливих з'єднань (ребер):")
    for e in edges:
        print(f"   острів {e.u} ↔ острів {e.v}   довжина = {e.weight}")

    print(f"\n{SEPARATOR}")
    print("Запускаємо алгоритм Краскала (жадібний вибір найкоротших ребер):\n")

    try:
        total_weight, mst_edges = kruskal(n, edges)
    except ValueError as exc:
        print(f"\nПомилка: {exc}", file=sys.stderr)
        sys.exit(1)

    for step, e in enumerate(mst_edges, start=1):
        print(
            f"   крок {step}: додаємо острів {e.u} ↔ острів {e.v}"
            f"   (довжина {e.weight},  всього = {sum(x.weight for x in mst_edges[:step])})"
        )

    print(f"\n{SEPARATOR}")
    print(f"Обрано {len(mst_edges)} кабел(і/ів) із {len(edges)} можливих")
    print(f"Мінімальна довжина кабелів: {total_weight}")
    print(SEPARATOR)


if __name__ == "__main__":
    main()