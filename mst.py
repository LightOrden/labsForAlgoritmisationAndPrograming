"""
Модуль для обчислення мінімального кістякового дерева (MST).

Використовується алгоритм Прима з пріоритетною чергою (heap),
що забезпечує складність O(E log V).
"""

import heapq
from typing import List


def compute_minimum_spanning_tree(adjacency_matrix: List[List[float]]) -> float:
    """
    Обчислює мінімальну загальну довжину кабелів для з'єднання всіх островів
    за допомогою алгоритму Прима.

    Args:
        adjacency_matrix: Квадратна матриця суміжності, де елемент [i][j]
                          містить відстань між островами i та j.
                          Значення 0 означає відсутність прямого з'єднання.

    Returns:
        Мінімальна сумарна довжина підводних кабелів.

    Raises:
        ValueError: Якщо граф не є зв'язним.
    """
    num_islands = len(adjacency_matrix)

    if num_islands == 1:
        return 0.0

    visited = [False] * num_islands
    min_heap: List[tuple] = [(0.0, 0)]  # (вага ребра, вершина)
    total_cable_length = 0.0
    visited_count = 0

    while min_heap and visited_count < num_islands:
        edge_weight, current_island = heapq.heappop(min_heap)

        if visited[current_island]:
            continue

        visited[current_island] = True
        total_cable_length += edge_weight
        visited_count += 1

        for neighbor_island, distance in enumerate(adjacency_matrix[current_island]):
            if not visited[neighbor_island] and distance > 0:
                heapq.heappush(min_heap, (distance, neighbor_island))

    if visited_count < num_islands:
        raise ValueError(
            "Граф не є зв'язним: неможливо з'єднати всі острови кабелями."
        )

    return total_cable_length
