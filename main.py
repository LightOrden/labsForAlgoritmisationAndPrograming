"""
Розв'язання задачі про мінімальну довжину підводних кабелів
для з'єднання островів Венеції.

Алгоритм: мінімальне кістякове дерево (MST) методом Прима.
"""

import sys

from graph import build_graph_from_csv
from mst import compute_minimum_spanning_tree


def main() -> None:
    """Точка входу програми."""
    if len(sys.argv) != 2:
        print("Використання: python main.py <шлях_до_файлу.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]

    adjacency_matrix = build_graph_from_csv(csv_path)
    min_cable_length = compute_minimum_spanning_tree(adjacency_matrix)

    print(f"Мінімальна довжина підводних кабелів: {min_cable_length}")


if __name__ == "__main__":
    main()
