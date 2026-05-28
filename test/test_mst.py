"""
Unit tests for the Venice MST module.

Run from the project root:
    python -m pytest test/
  or
    python -m unittest discover -s test
"""

import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure the project root is on the path so ``src`` can be imported.
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mst import (  # noqa: E402
    Edge,
    UnionFind,
    extract_edges,
    kruskal,
    load_adjacency_matrix,
    minimum_cable_length,
)


class TestUnionFind(unittest.TestCase):
    """Tests for the UnionFind data structure."""

    def test_initial_each_element_is_own_root(self):
        uf = UnionFind(5)
        for i in range(5):
            self.assertEqual(uf.find(i), i)

    def test_union_merges_two_sets(self):
        uf = UnionFind(4)
        merged = uf.union(0, 1)
        self.assertTrue(merged)
        self.assertEqual(uf.find(0), uf.find(1))

    def test_union_same_set_returns_false(self):
        uf = UnionFind(4)
        uf.union(0, 1)
        self.assertFalse(uf.union(0, 1))

    def test_union_transitivity(self):
        uf = UnionFind(5)
        uf.union(0, 1)
        uf.union(1, 2)
        self.assertEqual(uf.find(0), uf.find(2))

    def test_disjoint_sets_have_different_roots(self):
        uf = UnionFind(4)
        uf.union(0, 1)
        uf.union(2, 3)
        self.assertNotEqual(uf.find(0), uf.find(2))

    def test_path_compression(self):
        """After find(), all nodes on the path point directly to the root."""
        uf = UnionFind(5)
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(2, 3)
        root = uf.find(3)
        # After path compression every intermediate node should point to root.
        self.assertEqual(uf._parent[3], root)


class TestEdge(unittest.TestCase):
    """Tests for the Edge dataclass ordering."""

    def test_edges_sorted_by_weight(self):
        edges = [Edge(5, 0, 1), Edge(2, 1, 2), Edge(8, 0, 2)]
        self.assertEqual(sorted(edges)[0].weight, 2)
        self.assertEqual(sorted(edges)[-1].weight, 8)

    def test_edge_equality(self):
        e1 = Edge(3, 0, 1)
        e2 = Edge(3, 0, 1)
        self.assertEqual(e1, e2)


class TestExtractEdges(unittest.TestCase):
    """Tests for extract_edges()."""

    def test_basic_extraction(self):
        matrix = [
            [0, 4, 0],
            [4, 0, 2],
            [0, 2, 0],
        ]
        edges = extract_edges(matrix)
        weights = [e.weight for e in edges]
        self.assertIn(4, weights)
        self.assertIn(2, weights)
        self.assertEqual(len(edges), 2)

    def test_no_duplicate_edges(self):
        """Each undirected edge must appear exactly once."""
        matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ]
        edges = extract_edges(matrix)
        self.assertEqual(len(edges), 3)

    def test_zero_weight_means_no_edge(self):
        matrix = [
            [0, 0],
            [0, 0],
        ]
        self.assertEqual(extract_edges(matrix), [])

    def test_edges_are_sorted(self):
        matrix = [
            [0, 9, 1],
            [9, 0, 5],
            [1, 5, 0],
        ]
        edges = extract_edges(matrix)
        weights = [e.weight for e in edges]
        self.assertEqual(weights, sorted(weights))

    def test_single_node(self):
        self.assertEqual(extract_edges([[0]]), [])


class TestKruskal(unittest.TestCase):
    """Tests for the kruskal() function."""

    def test_simple_path_graph(self):
        # 0 -2- 1 -3- 2  =>  MST weight = 5
        edges = [Edge(2, 0, 1), Edge(3, 1, 2), Edge(10, 0, 2)]
        weight, mst = kruskal(3, edges)
        self.assertEqual(weight, 5)
        self.assertEqual(len(mst), 2)

    def test_single_node(self):
        weight, mst = kruskal(1, [])
        self.assertEqual(weight, 0)
        self.assertEqual(mst, [])

    def test_two_nodes(self):
        edges = [Edge(7, 0, 1)]
        weight, mst = kruskal(2, edges)
        self.assertEqual(weight, 7)
        self.assertEqual(len(mst), 1)

    def test_complete_graph_picks_minimum(self):
        # 4-node complete graph; minimum spanning tree should pick cheapest edges
        edges = [
            Edge(1, 0, 1),
            Edge(2, 0, 2),
            Edge(3, 0, 3),
            Edge(4, 1, 2),
            Edge(5, 1, 3),
            Edge(6, 2, 3),
        ]
        weight, mst = kruskal(4, edges)
        self.assertEqual(weight, 1 + 2 + 3)
        self.assertEqual(len(mst), 3)

    def test_disconnected_graph_raises(self):
        # Two isolated edges, no connection between components 0-1 and 2-3
        edges = [Edge(1, 0, 1), Edge(2, 2, 3)]
        with self.assertRaises(ValueError):
            kruskal(4, edges)

    def test_known_example(self):
        """
        Classic textbook MST example:
        Edges: (0,1,2),(0,3,6),(1,2,3),(1,3,8),(1,4,5),(2,4,7),(3,4,9)
        MST: (0,1,2),(1,2,3),(1,4,5),(0,3,6) => 16
        """
        edges = sorted(
            [
                Edge(2, 0, 1),
                Edge(6, 0, 3),
                Edge(3, 1, 2),
                Edge(8, 1, 3),
                Edge(5, 1, 4),
                Edge(7, 2, 4),
                Edge(9, 3, 4),
            ]
        )
        weight, _ = kruskal(5, edges)
        self.assertEqual(weight, 16)


class TestLoadAdjacencyMatrix(unittest.TestCase):
    """Tests for load_adjacency_matrix()."""

    def _write_csv(self, rows: list, suffix: str = ".csv") -> str:
        """Helper: write rows to a temporary CSV file and return its path."""
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, "w", newline="") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)
        return path

    def test_valid_matrix_loaded_correctly(self):
        rows = [[0, 2, 0], [2, 0, 3], [0, 3, 0]]
        path = self._write_csv(rows)
        try:
            matrix = load_adjacency_matrix(path)
            self.assertEqual(matrix, rows)
        finally:
            os.unlink(path)

    def test_file_not_found_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_adjacency_matrix("/nonexistent/path/islands.csv")

    def test_non_integer_value_raises(self):
        rows = [[0, "abc"], ["abc", 0]]
        path = self._write_csv(rows)
        try:
            with self.assertRaises(ValueError):
                load_adjacency_matrix(path)
        finally:
            os.unlink(path)

    def test_non_square_matrix_raises(self):
        rows = [[0, 1, 2], [1, 0]]
        path = self._write_csv(rows)
        try:
            with self.assertRaises(ValueError):
                load_adjacency_matrix(path)
        finally:
            os.unlink(path)

    def test_single_island(self):
        path = self._write_csv([[0]])
        try:
            matrix = load_adjacency_matrix(path)
            self.assertEqual(matrix, [[0]])
        finally:
            os.unlink(path)

    def test_empty_file_returns_empty_matrix(self):
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            matrix = load_adjacency_matrix(path)
            self.assertEqual(matrix, [])
        finally:
            os.unlink(path)


class TestMinimumCableLength(unittest.TestCase):
    """Integration tests for the top-level minimum_cable_length() function."""

    def _write_matrix_csv(self, matrix: list) -> str:
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w", newline="") as f:
            writer = csv.writer(f)
            for row in matrix:
                writer.writerow(row)
        return path

    def test_five_islands_known_result(self):
        # Corresponds to data/islands.csv shipped with the project:
        # MST: (0,1,2),(1,2,3),(1,4,5),(0,3,6) => 16
        matrix = [
            [0, 2, 0, 6, 0],
            [2, 0, 3, 8, 5],
            [0, 3, 0, 0, 7],
            [6, 8, 0, 0, 9],
            [0, 5, 7, 9, 0],
        ]
        path = self._write_matrix_csv(matrix)
        try:
            self.assertEqual(minimum_cable_length(path), 16)
        finally:
            os.unlink(path)

    def test_single_island_needs_no_cable(self):
        path = self._write_matrix_csv([[0]])
        try:
            self.assertEqual(minimum_cable_length(path), 0)
        finally:
            os.unlink(path)

    def test_two_islands(self):
        path = self._write_matrix_csv([[0, 4], [4, 0]])
        try:
            self.assertEqual(minimum_cable_length(path), 4)
        finally:
            os.unlink(path)

    def test_three_islands_triangle(self):
        # Triangle with weights 1, 2, 3 => MST picks 1 and 2
        matrix = [[0, 1, 3], [1, 0, 2], [3, 2, 0]]
        path = self._write_matrix_csv(matrix)
        try:
            self.assertEqual(minimum_cable_length(path), 3)
        finally:
            os.unlink(path)

    def test_disconnected_graph_raises(self):
        # Islands 0-1 and 2-3 are in separate components
        matrix = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 2],
            [0, 0, 2, 0],
        ]
        path = self._write_matrix_csv(matrix)
        try:
            with self.assertRaises(ValueError):
                minimum_cable_length(path)
        finally:
            os.unlink(path)

    def test_file_not_found_raises(self):
        with self.assertRaises(FileNotFoundError):
            minimum_cable_length("no_such_file.csv")

    def test_large_graph_runs_without_error(self):
        """Smoke-test with N=100 fully connected islands (all weights = 1)."""
        n = 100
        matrix = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
        path = self._write_matrix_csv(matrix)
        try:
            result = minimum_cable_length(path)
            # MST of complete graph with all weights 1 has n-1 edges
            self.assertEqual(result, n - 1)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()