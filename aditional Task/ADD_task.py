import os
import ast


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def build_balanced(values, lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    node = Node(values[mid])
    node.left = build_balanced(values, lo, mid - 1)
    node.right = build_balanced(values, mid + 1, hi)
    return node


def tree_height(node):
    if node is None:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))


def print_tree(root):
    if root is None:
        print("Дерево порожнє.")
        return
    h = tree_height(root)
    gap = max(2, h)
    lines, _, _, _ = build_lines(root, gap)
    for line in lines:
        print(line)


def build_lines(node, gap):
    label = str(node.value)
    label_len = len(label)

    if node.left is None and node.right is None:
        return [label], label_len, 0, label_len - 1

    if node.right is None:
        left_lines, left_w, left_rs, left_re = build_lines(node.left, gap)
        root_pos = left_re
        root_end = root_pos + label_len - 1
        width = max(left_w, root_end + 1)
        top = (" " * root_pos + label).ljust(width)
        connector = (" " * left_re + "/").ljust(width)
        body = [line.ljust(width) for line in left_lines]
        return [top, connector] + body, width, root_pos, root_end

    if node.left is None:
        right_lines, right_w, right_rs, right_re = build_lines(node.right, gap)
        right_offset = label_len + gap
        width = right_offset + right_w
        top = label.ljust(width)
        connector = (" " * (right_offset + right_rs) + "\\").ljust(width)
        body = [(" " * right_offset + line).ljust(width) for line in right_lines]
        return [top, connector] + body, width, 0, label_len - 1

    left_lines, left_w, left_rs, left_re = build_lines(node.left, gap)
    right_lines, right_w, right_rs, right_re = build_lines(node.right, gap)

    left_root_pos = left_re
    right_offset = left_w + gap
    right_root_pos = right_offset + right_rs

    root_pos = (left_root_pos + right_root_pos - label_len + 1) // 2
    root_pos = max(root_pos, 0)
    root_end = root_pos + label_len - 1
    width = max(right_offset + right_w, root_end + 1)

    top = (" " * root_pos + label).ljust(width)
    connector = list(" " * width)
    connector[left_root_pos] = "/"
    connector[right_root_pos] = "\\"
    connector_str = "".join(connector)

    left_height = len(left_lines)
    right_height = len(right_lines)
    max_height = max(left_height, right_height)
    left_lines += [" " * left_w] * (max_height - left_height)
    right_lines += [" " * right_w] * (max_height - right_height)

    body = []
    for l, r in zip(left_lines, right_lines):
        body.append((l.ljust(left_w) + " " * gap + r.ljust(right_w)).ljust(width))

    return [top, connector_str] + body, width, root_pos, root_end


def read_values(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        print("Помилка: файл tree.txt порожній. Запиши: [2, 5, 7, 10, 12, 15, 18]")
        exit(1)
    try:
        values = ast.literal_eval(content)
    except (SyntaxError, ValueError):
        print(f"Помилка формату. Зміст: {repr(content)}")
        print("Правильний формат: [2, 5, 7, 10, 12, 15, 18]")
        exit(1)
    if not isinstance(values, list):
        print("Помилка: потрібен список чисел, наприклад: [2, 5, 7, 10, 12, 15, 18]")
        exit(1)
    return values


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "tree.txt")
    if not os.path.exists(filepath):
        print(f"Файл не знайдено: {filepath}")
        return

    values = read_values(filepath)
    values_sorted = sorted(values)

    print(f"In-order послідовність: {values_sorted}")
    print()

    root = build_balanced(values_sorted, 0, len(values_sorted) - 1)

    print("Збалансоване дерево:")
    print()
    print_tree(root)


if __name__ == "__main__":
    main()