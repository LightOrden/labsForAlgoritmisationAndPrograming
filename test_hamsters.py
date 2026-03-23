import unittest

from hamsters import max_hamsters


class TestMaxHamsters(unittest.TestCase):

    def test_example_1(self):
        s = 7
        c = 3
        hamsters = [[1, 2], [2, 2], [3, 1]]
        self.assertEqual(max_hamsters(s, c, hamsters), 2)

    def test_example_2(self):
        s = 19
        c = 4
        hamsters = [[5, 0], [2, 2], [1, 4], [5, 1]]
        self.assertEqual(max_hamsters(s, c, hamsters), 3)

    def test_example_3(self):
        s = 2
        c = 2
        hamsters = [[1, 50000], [1, 60000]]
        self.assertEqual(max_hamsters(s, c, hamsters), 1)

    def test_zero_food(self):
        s = 0
        c = 3
        hamsters = [[1, 0], [2, 0], [3, 0]]
        self.assertEqual(max_hamsters(s, c, hamsters), 0)

    def test_single_hamster(self):
        s = 5
        c = 1
        hamsters = [[5, 100]]
        self.assertEqual(max_hamsters(s, c, hamsters), 1)

    def test_all_greedy_zero(self):
        s = 10
        c = 3
        hamsters = [[2, 0], [3, 0], [4, 0]]
        self.assertEqual(max_hamsters(s, c, hamsters), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)