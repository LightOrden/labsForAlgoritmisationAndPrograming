import unittest

from lab8 import count_paths


class TestIndianaJones(unittest.TestCase):

    def test_example_1(self) -> None:
        width = 3
        height = 3

        corridor = [
            "aaa",
            "cab",
            "def",
        ]

        expected = 5

        result = count_paths(
            width,
            height,
            corridor,
        )

        self.assertEqual(
            result,
            expected,
        )

        print(
            "Тест 1 пройдено "
            "(очікувано 5)"
        )

    def test_example_2(self) -> None:
        width = 10
        height = 1

        corridor = [
            "abcdefaghi",
        ]

        expected = 2

        result = count_paths(
            width,
            height,
            corridor,
        )

        self.assertEqual(
            result,
            expected,
        )

        print(
            "Тест 2 пройдено "
            "(очікувано 2)"
        )

    def test_example_3(self) -> None:
        width = 7
        height = 6

        corridor = [
            "aaaaaaa",
            "aaaaaaa",
            "aaaaaaa",
            "aaaaaaa",
            "aaaaaaa",
            "aaaaaaa",
        ]

        expected = 201684

        result = count_paths(
            width,
            height,
            corridor,
        )

        self.assertEqual(
            result,
            expected,
        )

        print(
            "Тест 3 пройдено "
            "(очікувано 201684)"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)