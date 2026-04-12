import unittest

from treeTask import BinaryTree, find_successor


class TestFindSuccessor(unittest.TestCase):
    """
    Тестування функції find_successor на дереві:

            10
           /  \\
          5    15
         / \\  /  \\
        3   7 12  20

    In-order обхід: 3 → 5 → 7 → 10 → 12 → 15 → 20
    """

    def setUp(self):
        self.root = BinaryTree(10)

        self.node_5 = BinaryTree(5, parent=self.root)
        self.node_15 = BinaryTree(15, parent=self.root)
        self.root.left = self.node_5
        self.root.right = self.node_15

        self.node_3 = BinaryTree(3, parent=self.node_5)
        self.node_7 = BinaryTree(7, parent=self.node_5)
        self.node_5.left = self.node_3
        self.node_5.right = self.node_7

        self.node_12 = BinaryTree(12, parent=self.node_15)
        self.node_20 = BinaryTree(20, parent=self.node_15)
        self.node_15.left = self.node_12
        self.node_15.right = self.node_20

    def test_successor_of_root_has_right_subtree(self):
        """Наступник кореня (10) → мінімум правого піддерева = 12."""
        successor = find_successor(self.root, self.root)
        self.assertIsNotNone(successor)
        self.assertEqual(successor.value, 12)

    def test_successor_of_node_with_right_child(self):
        """Наступник вузла 5 (має праву дитину 7) → 7."""
        successor = find_successor(self.root, self.node_5)
        self.assertIsNotNone(successor)
        self.assertEqual(successor.value, 7)

    def test_successor_of_node_15_with_right_child(self):
        """Наступник вузла 15 (має праву дитину 20) → 20 (найлівіший у правому піддереві)."""
        successor = find_successor(self.root, self.node_15)
        self.assertIsNotNone(successor)
        self.assertEqual(successor.value, 20)

    # --- Випадок 2: вузол не має правого піддерева ---

    def test_successor_for_7_no_right_child(self):
        """Наступник вузла 7 (немає правої дитини) → перший предок, де прийшли зліва = 10."""
        successor = find_successor(self.root, self.node_7)
        self.assertIsNotNone(successor)
        self.assertEqual(successor.value, 10)

    def test_successor_for_3_no_right_child(self):
        """Наступник вузла 3 (немає правої дитини, є лівою дитиною 5) → 5."""
        successor = find_successor(self.root, self.node_3)
        self.assertIsNotNone(successor)
        self.assertEqual(successor.value, 5)

    def test_successor_for_12_no_right_child(self):
        """Наступник вузла 12 (немає правої дитини, є лівою дитиною 15) → 15."""
        successor = find_successor(self.root, self.node_12)
        self.assertIsNotNone(successor)
        self.assertEqual(successor.value, 15)

    # --- Крайній випадок: останній вузол в обході ---

    def test_successor_of_last_node_is_none(self):
        """Наступник вузла 20 (найправіший) → None."""
        successor = find_successor(self.root, self.node_20)
        self.assertIsNone(successor)


if __name__ == "__main__":
    unittest.main()