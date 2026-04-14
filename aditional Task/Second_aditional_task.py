class BinaryTree:
    def __init__(self, v=0):
        self.value = v
        self.left = None
        self.right = None

    def __build_from_inorder(self, values):
        if not values:
            return None
        mid = len(values) // 2
        node = BinaryTree(values[mid])
        node.left = self.__build_from_inorder(values[:mid])
        node.right = self.__build_from_inorder(values[mid + 1:])
        return node

    def __get_h(self, n):
        if not n: return 0
        return max(self.__get_h(n.left), self.__get_h(n.right)) + 1

    def __put(self, m, r, c, val):
        s = str(val)
        offset = len(s) // 2
        for i in range(len(s)):
            pos = c + i - offset
            if 0 <= r < len(m) and 0 <= pos < len(m[0]):
                m[r][pos] = s[i]

    def __fill(self, n, m, r, c, side, gr, gc):
        if not n: return
        self.__put(m, r, c, n.value)
        s_len = len(str(n.value))
        left_conn = c - (s_len // 2) - 1
        right_conn = c + (s_len - s_len // 2)
        nr = max(2, gr - 2)
        if side == "root":
            if n.left:
                m[r][left_conn] = "-"
                self.__fill(n.left, m, r, c - gc, "left", gr, gc)
            if n.right:
                m[r][right_conn] = "-"
                self.__fill(n.right, m, r, c + gc, "right", gr, gc)
        elif side == "left":
            if n.left:
                m[r - 1][left_conn] = "\\"
                self.__fill(n.left, m, r - gr, c - gc, "left", nr, gc)
            if n.right:
                m[r + 1][left_conn] = "/"
                self.__fill(n.right, m, r + gr, c - gc, "left", nr, gc)
        elif side == "right":
            if n.left:
                m[r - 1][right_conn] = "/"
                self.__fill(n.left, m, r - gr, c + gc, "right", nr, gc)
            if n.right:
                m[r + 1][right_conn] = "\\"
                self.__fill(n.right, m, r + gr, c + gc, "right", nr, gc)

    def load(self, filename):
        try:
            with open(filename, "r") as f:
                values = list(map(int, f.read().split()))
            if values:
                mid = len(values) // 2
                self.value = values[mid]
                self.left = self.__build_from_inorder(values[:mid])
                self.right = self.__build_from_inorder(values[mid + 1:])
        except Exception as e:
            print(f"Помилка читання файлу: {e}")

    def print_tree(self):
        rows, cols = 45, 80
        m = [[" " for _ in range(cols)] for _ in range(rows)]
        self.__fill(self, m, rows // 2, cols // 2, "root", 6, 6)
        print("\n")
        for r in m:
            line = "".join(r).rstrip()
            if line: print(line)

    def print_inorder(self):
        def p(n):
            if not n: return
            p(n.left)
            print(n.value, end=" ")
            p(n.right)
        print("інордер:", end=" ")
        p(self)
        print()

    def is_balanced(self):
        def check(n):
            if not n: return 0
            l, r = check(n.left), check(n.right)
            if l == -1 or r == -1 or abs(l - r) > 1: return -1
            return max(l, r) + 1
        return check(self) != -1


tree = BinaryTree()
tree.load("tree1.txt")
tree.print_inorder()
tree.print_tree()
print("")
print("збалансоване:", tree.is_balanced())