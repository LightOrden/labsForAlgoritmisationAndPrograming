"""
Тести для модулів graph та mst.

Запуск: python -m pytest tests.py -v
"""

import os
import tempfile

import pytest

from graph import build_graph_from_csv
from mst import compute_minimum_spanning_tree


class TestBuildGraphFromCsv:
    """Тести для функції build_graph_from_csv."""

    def test_reads_valid_csv(self):
        csv_content = "0,1,2\n1,0,3\n2,3,0\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(csv_content)
            tmp_path = tmp_file.name

        try:
            matrix = build_graph_from_csv(tmp_path)
            assert matrix == [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
        finally:
            os.unlink(tmp_path)

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            build_graph_from_csv("non_existent_file.csv")

    def test_raises_on_non_square_matrix(self):
        csv_content = "0,1,2\n1,0\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(csv_content)
            tmp_path = tmp_file.name

        try:
            with pytest.raises(ValueError, match="не є квадратною"):
                build_graph_from_csv(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_raises_on_negative_distance(self):
        csv_content = "0,-1\n-1,0\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(csv_content)
            tmp_path = tmp_file.name

        try:
            with pytest.raises(ValueError, match="Від'ємна відстань"):
                build_graph_from_csv(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_raises_on_empty_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp_file:
            tmp_file.write("")
            tmp_path = tmp_file.name

        try:
            with pytest.raises(ValueError, match="порожня"):
                build_graph_from_csv(tmp_path)
        finally:
            os.unlink(tmp_path)


class TestComputeMinimumSpanningTree:
    """Тести для функції compute_minimum_spanning_tree."""

    def test_single_island(self):
        matrix = [[0]]
        assert compute_minimum_spanning_tree(matrix) == 0.0

    def test_two_islands(self):
        matrix = [[0, 5], [5, 0]]
        assert compute_minimum_spanning_tree(matrix) == 5.0

    def test_triangle_graph(self):
        # Три острови: 1-2 = 1, 2-3 = 2, 1-3 = 10
        # MST: ребра 1-2 (вага 1) та 2-3 (вага 2) = 3
        matrix = [
            [0, 1, 10],
            [1, 0, 2],
            [10, 2, 0],
        ]
        assert compute_minimum_spanning_tree(matrix) == 3.0

    def test_classic_nine_island_graph(self):
        # Класичний приклад з підручника, MST = 37
        matrix = [
            [0, 4, 0, 0, 0, 0, 0, 8, 0],
            [4, 0, 8, 0, 0, 0, 0, 11, 0],
            [0, 8, 0, 7, 0, 4, 0, 0, 2],
            [0, 0, 7, 0, 9, 14, 0, 0, 0],
            [0, 0, 0, 9, 0, 10, 0, 0, 0],
            [0, 0, 4, 14, 10, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 1, 6],
            [8, 11, 0, 0, 0, 0, 1, 0, 7],
            [0, 0, 2, 0, 0, 0, 6, 7, 0],
        ]
        assert compute_minimum_spanning_tree(matrix) == 37.0

    def test_disconnected_graph_raises(self):
        # Два острови без з'єднання між собою
        matrix = [[0, 0], [0, 0]]
        with pytest.raises(ValueError, match="не є зв'язним"):
            compute_minimum_spanning_tree(matrix)

    def test_fully_connected_graph(self):
        # Повний граф з 4 вершин — MST має 3 ребра
        matrix = [
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0],
        ]
        # MST: 0-1 (1), 0-2 (2), 0-3 (3) = 6
        assert compute_minimum_spanning_tree(matrix) == 6.0
