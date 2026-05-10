"""
Модуль для зчитування графа з CSV-файлу.

CSV-файл містить матрицю суміжності, де елемент [i][j]
вказує на відстань між островами i та j.
"""

import csv
from typing import List


def build_graph_from_csv(file_path: str) -> List[List[float]]:
    """
    Зчитує матрицю суміжності з CSV-файлу.

    Args:
        file_path: Шлях до CSV-файлу з матрицею суміжності.

    Returns:
        Двовимірний список (матриця суміжності), де елемент [i][j]
        містить відстань між островами i та j.

    Raises:
        FileNotFoundError: Якщо файл не знайдено.
        ValueError: Якщо матриця не є квадратною або містить некоректні дані.
    """
    matrix: List[List[float]] = []

    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row:
                continue
            parsed_row = [float(value) for value in row]
            matrix.append(parsed_row)

    _validate_matrix(matrix)
    return matrix


def _validate_matrix(matrix: List[List[float]]) -> None:
    """
    Перевіряє коректність матриці суміжності.

    Args:
        matrix: Матриця суміжності для перевірки.

    Raises:
        ValueError: Якщо матриця порожня, не квадратна або має
                    недопустимі значення.
    """
    num_islands = len(matrix)

    if num_islands == 0:
        raise ValueError("Матриця суміжності порожня.")

    if not (1 <= num_islands <= 100):
        raise ValueError(
            f"Кількість островів має бути від 1 до 100, отримано: {num_islands}."
        )

    for row_index, row in enumerate(matrix):
        if len(row) != num_islands:
            raise ValueError(
                f"Матриця не є квадратною: рядок {row_index} "
                f"має {len(row)} елементів, очікується {num_islands}."
            )
        for col_index, value in enumerate(row):
            if value < 0:
                raise ValueError(
                    f"Від'ємна відстань у позиції [{row_index}][{col_index}]: {value}."
                )
