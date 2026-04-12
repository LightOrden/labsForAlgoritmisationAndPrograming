from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


FILE_NAME = "tree.txt"


@dataclass
class Node:
    val: int
    left: Node | None = field(default=None, repr=False)
    right: Node | None = field(default=None, repr=False)


def insert(root: Node | None, val: int) -> Node:
    if root is None:
        return Node(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def build_tree(values: list[int]) -> Node | None:
    root = None
    for v in values:
        root = insert(root, v)
    return root


@dataclass
class NodeInfo:
    val: int
    col: int
    row: int
    parent: NodeInfo | None = field(default=None, repr=False)
    is_left: bool = False


def _collect(node, col, parent, is_left, ctr, result):
    if node is None:
        return
    info = NodeInfo(node.val, col, -1, parent, is_left)
    result.append(info)
    _collect(node.left, col + 1, info, True, ctr, result)
    info.row = ctr[0]
    ctr[0] += 1
    _collect(node.right, col + 1, info, False, ctr, result)


def get_positions(root):
    result = []
    _collect(root, 0, None, False, [0], result)
    return result


def _build_grid(nodes):
    root = next(n for n in nodes if n.parent is None)
    label_w = max(len(str(n.val)) for n in nodes)
    step = label_w + 2

    max_col = max(n.col for n in nodes)
    n_rows = len(nodes)
    n_cols = (max_col + 1) * step + label_w + 2

    grid = [[" "] * n_cols for _ in range(n_rows)]

    def put(r, c, s):
        for i, ch in enumerate(s):
            if 0 <= r < n_rows and 0 <= c + i < n_cols:
                grid[r][c + i] = ch

    def node_x(col):
        return col * step

    def vert_x(col):
        return node_x(col) + label_w

    for n in nodes:
        if n.parent is None:
            continue

        pr, cr = n.parent.row, n.row
        vx = vert_x(n.parent.col)

        step_r = -1 if cr < pr else 1
        for r in range(pr + step_r, cr, step_r):
            if grid[r][vx] == " ":
                put(r, vx, "|")

        put(cr, vx, "/" if n.is_left else "\\")

        cx = node_x(n.col)
        for c in range(vx + 1, cx):
            put(cr, c, "-")

    for n in nodes:
        put(n.row, node_x(n.col), str(n.val))

    lines = ["".join(r).rstrip() for r in grid]
    return lines, root.row, node_x(root.col)


def print_top_view(nodes):
    lines, center_row, root_x = _build_grid(nodes)

    print("\n  Вид зверху  (ліво <--- корінь ---> право)\n")

    for i, line in enumerate(lines):
        left = line[:root_x].rstrip()
        right = line[root_x + len(str(nodes[0].val)) :].rstrip()

        if i == center_row:
            print(f"{left}  {line[root_x:root_x+len(str(nodes[0].val))]}  {right}")
        else:
            print(f"{left}     {right}")


def _print_inorder(node):
    if node is None:
        return
    _print_inorder(node.left)
    print(node.val, end=" ")
    _print_inorder(node.right)


def _read_values(path):
    tokens = path.read_text().split()
    return [int(t) for t in tokens if t.lstrip("-").isdigit()]


def main():
    path = Path(FILE_NAME)
    if not path.exists():
        print("Файл не знайдено")
        return

    values = _read_values(path)
    root = build_tree(values)

    print("Inorder:", end=" ")
    _print_inorder(root)
    print()

    nodes = get_positions(root)
    print_top_view(nodes)


if __name__ == "__main__":
    main()