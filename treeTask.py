"""
Варіант 1: Пошук наступника при серединному обході бінарного дерева.

Наступник (in-order successor) — це вузол з найменшим значенням,
яке більше за значення заданого вузла при серединному обході (left → root → right).
"""

from collections import deque


class BinaryTree:
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent


def find_successor(tree: "BinaryTree | None", node: BinaryTree) -> "BinaryTree | None":
    if node.right is not None:
        current = node.right
        while current.left is not None:
            current = current.left
        return current

 
    current = node
    parent = node.parent

    while parent is not None and parent.right is current:
        current = parent
        parent = parent.parent

    return parent


def print_tree(root: "BinaryTree | None") -> None:

    if root is None:
        print("<порожнє дерево>")
        return

    levels = []
    current_level = [root]

    while any(node is not None for node in current_level):
        levels.append(current_level)
        next_level = []
        for node in current_level:
            if node is not None:
                next_level.append(node.left)
                next_level.append(node.right)
            else:
                next_level.extend([None, None])
        current_level = next_level

    total_levels = len(levels)
    node_width = 3

    for depth, level in enumerate(levels):
        gap_between = node_width * (2 ** (total_levels - depth - 1) - 1)
        indent = gap_between // 2

        node_str = ""
        for i, node in enumerate(level):
            label = str(node.value) if node is not None else " "
            if i == 0:
                node_str += " " * indent + label.center(node_width)
            else:
                node_str += " " * gap_between + label.center(node_width)
        print(node_str)

        if depth < total_levels - 1:
            connector_str = ""
            connector_indent = indent - 1

            for i, node in enumerate(level):
                left_sym = "/" if (node is not None and node.left is not None) else " "
                right_sym = "\\" if (node is not None and node.right is not None) else " "

                if i == 0:
                    connector_str += " " * max(connector_indent, 0)
                else:
                    connector_str += " " * max(gap_between - 1, 0)

                connector_str += left_sym + " " * node_width + right_sym

            print(connector_str)



if __name__ == "__main__":
 

    root = BinaryTree(10)

    node_5 = BinaryTree(5, parent=root)
    node_15 = BinaryTree(15, parent=root)
    root.left = node_5
    root.right = node_15

    node_3 = BinaryTree(3, parent=node_5)
    node_7 = BinaryTree(7, parent=node_5)
    node_5.left = node_3
    node_5.right = node_7

    node_12 = BinaryTree(12, parent=node_15)
    node_20 = BinaryTree(20, parent=node_15)
    node_15.left = node_12
    node_15.right = node_20

    print("Бінарне дерево:")
    print()
    print_tree(root)
    print()

    test_cases = [
        (node_3,  "3  → очікується 5"),
        (node_5,  "5  → очікується 7"),
        (node_7,  "7  → очікується 10"),
        (root,    "10 → очікується 12"),
        (node_12, "12 → очікується 15"),
        (node_15, "15 → очікується 20"),
        (node_20, "20 → очікується None"),
    ]

    print("In-order обхід: 3 → 5 → 7 → 10 → 12 → 15 → 20")
    print()
    print(f"{'Вузол':<8} {'Наступник':<12} {'Перевірка'}")
    print("-" * 38)
    for node, description in test_cases:
        successor = find_successor(root, node)
        result = str(successor.value) if successor is not None else "None"
        print(f"{node.value:<8} {result:<12} {description}")