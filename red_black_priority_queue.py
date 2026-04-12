"""
Черга з пріоритетами на основі червоно-чорного дерева.

Порядок: priority(лівий) >= priority(батько) > priority(правий)
Найвищий пріоритет — у найлівішому вузлі.
"""

RED = True
BLACK = False


class Node:
    """Вузол червоно-чорного дерева."""

    def __init__(self, value, priority):
        self.value = value
        self.priority = priority
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        color_str = "RED" if self.color == RED else "BLACK"
        return f"Node(value={self.value!r}, priority={self.priority}, color={color_str})"


class RedBlackPriorityQueue:
    """Черга з пріоритетами на основі червоно-чорного дерева."""

    def __init__(self):
        self._nil = Node(None, None)
        self._nil.color = BLACK
        self._nil.left = self._nil
        self._nil.right = self._nil
        self._nil.parent = self._nil

        self._root = self._nil
        self._size = 0

    def insert(self, value, priority):
        """Вставити елемент із заданим значенням та пріоритетом."""
        new_node = Node(value, priority)
        new_node.left = self._nil
        new_node.right = self._nil
        new_node.parent = self._nil

        self._bst_insert(new_node)
        self._fix_insert(new_node)
        self._size += 1

    def pop(self):
        """Видалити та повернути елемент з найвищим пріоритетом."""
        if self._root is self._nil:
            return None

        max_node = self._find_max(self._root)
        result = (max_node.value, max_node.priority)
        self._delete(max_node)
        self._size -= 1
        return result

    def peek(self):
        """Повернути елемент з найвищим пріоритетом без видалення."""
        if self._root is self._nil:
            return None

        max_node = self._find_max(self._root)
        return (max_node.value, max_node.priority)

    def is_empty(self):
        """Перевірити, чи черга порожня."""
        return self._root is self._nil

    def print_tree(self):
        """Вивести дерево у вигляді ASCII-графіки (корінь зліва, гілки вправо)."""
        if self._root is self._nil:
            print("  <порожнє дерево>")
            return
        self._print_node(self._root, prefix="", is_left=None)

    def __len__(self):
        return self._size

    def __repr__(self):
        items = self._inorder(self._root)
        return f"RedBlackPriorityQueue({items})"

    # --- Пошук ---

    def _find_max(self, node):
        """Найвищий пріоритет — найлівіший вузол (left >= parent)."""
        while node.left is not self._nil:
            node = node.left
        return node

    def _inorder_successor(self, node):
        """Найлівіший вузол у піддереві — inorder-наступник для видалення."""
        while node.left is not self._nil:
            node = node.left
        return node

    def _inorder(self, node):
        if node is self._nil:
            return []
        result = []
        result.extend(self._inorder(node.left))
        result.append((node.value, node.priority))
        result.extend(self._inorder(node.right))
        return result

    # --- Вставка ---

    def _bst_insert(self, new_node):
        parent = self._nil
        current = self._root

        while current is not self._nil:
            parent = current
            if new_node.priority >= current.priority:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is self._nil:
            self._root = new_node
        elif new_node.priority >= parent.priority:
            parent.left = new_node
        else:
            parent.right = new_node

    def _fix_insert(self, node):
        while node.parent.color == RED:
            if node.parent is node.parent.parent.left:
                uncle = node.parent.parent.right

                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node is node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left

                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node is node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._rotate_left(node.parent.parent)

        self._root.color = BLACK

    # --- Видалення ---

    def _delete(self, node):
        y = node
        y_original_color = y.color

        if node.left is self._nil:
            x = node.right
            self._transplant(node, node.right)

        elif node.right is self._nil:
            x = node.left
            self._transplant(node, node.left)

        else:
            # inorder-наступник: найлівіший вузол у правому піддереві
            y = self._inorder_successor(node.right)
            y_original_color = y.color
            x = y.right

            if y.parent is node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == BLACK:
            self._fix_delete(x)

    def _fix_delete(self, node):
        while node is not self._root and node.color == BLACK:
            if node is node.parent.left:
                sibling = node.parent.right

                if sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self._rotate_left(node.parent)
                    sibling = node.parent.right

                if sibling.left.color == BLACK and sibling.right.color == BLACK:
                    sibling.color = RED
                    node = node.parent
                else:
                    if sibling.right.color == BLACK:
                        sibling.left.color = BLACK
                        sibling.color = RED
                        self._rotate_right(sibling)
                        sibling = node.parent.right

                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    sibling.right.color = BLACK
                    self._rotate_left(node.parent)
                    node = self._root
            else:
                sibling = node.parent.left

                if sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self._rotate_right(node.parent)
                    sibling = node.parent.left

                if sibling.right.color == BLACK and sibling.left.color == BLACK:
                    sibling.color = RED
                    node = node.parent
                else:
                    if sibling.left.color == BLACK:
                        sibling.right.color = BLACK
                        sibling.color = RED
                        self._rotate_left(sibling)
                        sibling = node.parent.left

                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    sibling.left.color = BLACK
                    self._rotate_right(node.parent)
                    node = self._root

        node.color = BLACK

    def _transplant(self, u, v):
        if u.parent is self._nil:
            self._root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # --- Повороти ---

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left

        if y.left is not self._nil:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is self._nil:
            self._root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right

        if y.right is not self._nil:
            y.right.parent = x

        y.parent = x.parent

        if x.parent is self._nil:
            self._root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    # --- Виведення дерева ---

    def _assign_coords(self, node, depth, counter):
        """
        Обхід in-order: кожному вузлу присвоює унікальну колонку (x)
        та рівень (y = depth). Повертає словник {id(node): (x, y, label)}.
        """
        if node is self._nil:
            return {}

        coords = {}
        coords.update(self._assign_coords(node.left, depth + 1, counter))

        x = counter[0]
        counter[0] += 1
        color_tag = "R" if node.color == RED else "B"
        label = f"[{color_tag}:{node.priority}]"
        coords[id(node)] = (x, depth, label)

        coords.update(self._assign_coords(node.right, depth + 1, counter))
        return coords

    def _print_node(self, node, prefix, is_left):
        """Виводить нормалізоване дерево: кожен вузол на своєму місці."""
        col_width = 8      # ширина однієї колонки у символах
        row_height = 2     # рядків між рівнями (1 — вузол, 1 — лінії)

        counter = [0]
        coords = self._assign_coords(node, 0, counter)

        # знаходимо розміри полотна
        max_depth = max(y for _, (x, y, _l) in coords.items())
        max_col = max(x for _, (x, y, _l) in coords.items())

        total_rows = (max_depth + 1) * row_height
        total_cols = (max_col + 1) * col_width

        # заповнюємо полотно пробілами
        canvas = [[" "] * total_cols for _ in range(total_rows)]

        # зворотний індекс: (x, y) -> вузол для побудови ліній
        pos = {}
        for node_id, (x, y, label) in coords.items():
            pos[node_id] = (x, y)

        # малюємо вузли
        for node_id, (x, y, label) in coords.items():
            row = y * row_height
            col = x * col_width
            for i, ch in enumerate(label):
                if col + i < total_cols:
                    canvas[row][col + i] = ch

        # малюємо лінії від батька до нащадків
        def draw_lines(nd):
            if nd is self._nil:
                return

            px, py, _ = coords[id(nd)]
            parent_col = px * col_width + 2  # центр мітки батька

            if nd.left is not self._nil:
                cx, cy, _ = coords[id(nd.left)]
                child_col = cx * col_width + 2
                row = py * row_height + 1
                # малюємо "/" між батьком і лівим нащадком
                mid = (parent_col + child_col) // 2
                if 0 <= row < total_rows and 0 <= mid < total_cols:
                    canvas[row][mid] = "/"

            if nd.right is not self._nil:
                cx, cy, _ = coords[id(nd.right)]
                child_col = cx * col_width + 2
                row = py * row_height + 1
                mid = (parent_col + child_col) // 2
                if 0 <= row < total_rows and 0 <= mid < total_cols:
                    canvas[row][mid] = "\\"

            draw_lines(nd.left)
            draw_lines(nd.right)

        draw_lines(node)

        # виводимо полотно
        for row in canvas:
            print("".join(row).rstrip())


# --- Демонстрація ---

if __name__ == "__main__":
    pq = RedBlackPriorityQueue()

    print("=== Вставка елементів ===")
    elements = [
        ("завдання C", 3),
        ("завдання A", 10),
        ("завдання E", 1),
        ("завдання B", 7),
        ("завдання D", 5),
    ]
    for value, priority in elements:
        pq.insert(value, priority)
        print(f"  Вставлено: {value!r} з пріоритетом {priority}")

    print(f"\nРозмір черги: {len(pq)}")

    print("\n=== Структура дерева після вставки ===")
    print("  Ліворуч — вищий пріоритет, праворуч — нижчий.")
    print("  [B] — чорний вузол, [R] — червоний вузол.\n")
    pq.print_tree()

    print("\n=== Перегляд найвищого пріоритету (peek) ===")
    top = pq.peek()
    print(f"  Найвищий пріоритет: value={top[0]!r}, priority={top[1]}")
    print(f"  Розмір після peek: {len(pq)} (не змінився)")

    print("\n=== Видалення елементів (pop) ===")
    while not pq.is_empty():
        item = pq.pop()
        print(f"  Вилучено: value={item[0]!r}, priority={item[1]}")

    print(f"\nЧерга порожня: {pq.is_empty()}")
    print(f"pop з порожньої черги: {pq.pop()}")