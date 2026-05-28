"""
Module for computing the Minimum Spanning Tree (MST) of a graph
represented as an adjacency matrix (Venice islands problem).

Uses Kruskal's algorithm with Union-Find for efficiency.
Time complexity: O(E log E), where E is the number of edges.
Suitable for N <= 100 islands.
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass(order=True)
class Edge:
    """Represents a weighted undirected edge between two nodes."""

    weight: int
    u: int
    v: int


class UnionFind:
    """
    Disjoint Set Union (Union-Find) data structure
    with path compression and union by rank.
    """

    def __init__(self, n: int) -> None:
        """
        Initialise Union-Find for *n* elements (0-indexed).

        Args:
            n: Number of elements.
        """
        self._parent: List[int] = list(range(n))
        self._rank: List[int] = [0] * n

    def find(self, x: int) -> int:
        """
        Return the representative of the set containing *x*.

        Applies path compression on every call.

        Args:
            x: Element whose root is sought.

        Returns:
            Root representative of the set.
        """
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Merge the sets containing *x* and *y*.

        Args:
            x: First element.
            y: Second element.

        Returns:
            True if the sets were distinct and have been merged,
            False if they already belonged to the same set.
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx
        self._parent[ry] = rx
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1
        return True


def load_adjacency_matrix(filepath: str) -> List[List[int]]:
    """
    Read an adjacency matrix from a CSV file.

    Each row must have the same number of integer columns.
    A value of 0 at position [i][j] (i != j) means no direct
    connection between island *i* and island *j*.

    Args:
        filepath: Path to the CSV file.

    Returns:
        Two-dimensional list of integers representing the matrix.

    Raises:
        FileNotFoundError: If *filepath* does not exist.
        ValueError: If the matrix is not square or contains
                    non-integer values.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    matrix: List[List[int]] = []
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row:
                continue
            try:
                matrix.append([int(cell) for cell in row])
            except ValueError as exc:
                raise ValueError(
                    f"Non-integer value found in adjacency matrix: {exc}"
                ) from exc

    n = len(matrix)
    for i, row in enumerate(matrix):
        if len(row) != n:
            raise ValueError(
                f"Row {i} has {len(row)} columns, expected {n}. "
                "The adjacency matrix must be square."
            )

    return matrix


def extract_edges(matrix: List[List[int]]) -> List[Edge]:
    """
    Convert the upper triangle of an adjacency matrix into a list of edges.

    Only positive weights are included (0 means no edge).

    Args:
        matrix: Square adjacency matrix (N x N).

    Returns:
        Sorted list of :class:`Edge` objects.
    """
    edges: List[Edge] = []
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                edges.append(Edge(weight=matrix[i][j], u=i, v=j))
    edges.sort()
    return edges


def kruskal(n: int, edges: List[Edge]) -> Tuple[int, List[Edge]]:
    """
    Compute the Minimum Spanning Tree using Kruskal's algorithm.

    Args:
        n:      Number of nodes (islands).
        edges:  List of available edges, sorted by weight ascending.

    Returns:
        A tuple ``(total_weight, mst_edges)`` where *total_weight* is
        the sum of edge weights in the MST and *mst_edges* is the list
        of edges chosen.

    Raises:
        ValueError: If the graph is disconnected and a spanning tree
                    cannot be formed.
    """
    uf = UnionFind(n)
    mst_edges: List[Edge] = []
    total_weight = 0

    for edge in edges:
        if uf.union(edge.u, edge.v):
            mst_edges.append(edge)
            total_weight += edge.weight
            if len(mst_edges) == n - 1:
                break

    if n > 1 and len(mst_edges) < n - 1:
        raise ValueError("The graph is disconnected: a spanning tree cannot be formed.")

    return total_weight, mst_edges


def minimum_cable_length(filepath: str) -> int:
    """
    High-level function: read the island graph and return the minimum
    total cable length required to connect all islands.

    Args:
        filepath: Path to the CSV file with the adjacency matrix.

    Returns:
        Minimum total cable length (sum of MST edge weights).
    """
    matrix = load_adjacency_matrix(filepath)
    n = len(matrix)

    if n == 0:
        return 0
    if n == 1:
        return 0

    edges = extract_edges(matrix)
    total_weight, _ = kruskal(n, edges)
    return total_weight