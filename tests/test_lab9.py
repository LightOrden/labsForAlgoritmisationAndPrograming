import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from lab9 import fa_find_all


class FiniteAutomatonSearchTests(unittest.TestCase):

    def test_single_occurrence(self):
        self.assertEqual(fa_find_all("HELLO WORLD", "WORLD"), [6])

    def test_multiple_occurrences(self):
        self.assertEqual(fa_find_all("ABCABCABC", "ABC"), [0, 3, 6])

    def test_overlapping(self):
        self.assertEqual(fa_find_all("AAAAAA", "AAA"), [0, 1, 2, 3])

    def test_no_occurrence(self):
        self.assertEqual(fa_find_all("ABCDEF", "XYZ"), [])

    def test_empty_text(self):
        self.assertEqual(fa_find_all("", "ABC"), [])

    def test_empty_pattern(self):
        self.assertEqual(fa_find_all("ABCDEF", ""), [])

    def test_pattern_equals_text(self):
        self.assertEqual(fa_find_all("PYTHON", "PYTHON"), [0])

    def test_pattern_longer_than_text(self):
        self.assertEqual(fa_find_all("AB", "ABCDE"), [])

    def test_special_chars(self):
        self.assertEqual(fa_find_all("foo@bar.com foo@bar.com", "foo@bar"), [0, 12])


if __name__ == '__main__':
    unittest.main()