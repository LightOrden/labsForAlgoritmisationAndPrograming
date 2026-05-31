import os


def count_paths(width: int, height: int, corridor: list[str]) -> int:
    letter_totals: dict[str, int] = {}

    previous_column = [1] * height

    for row in range(height):
        letter = corridor[row][0]
        letter_totals[letter] = (
            letter_totals.get(letter, 0) + 1
        )

    for column in range(1, width):
        current_column = [0] * height

        for row in range(height):
            letter = corridor[row][column]

            ways = previous_column[row]
            ways += letter_totals.get(letter, 0)

            if corridor[row][column - 1] == letter:
                ways -= previous_column[row]

            current_column[row] = ways

        for row in range(height):
            letter = corridor[row][column]

            letter_totals[letter] = (
                letter_totals.get(letter, 0)
                + current_column[row]
            )

        previous_column = current_column

    if height == 1:
        return previous_column[0]
    return previous_column[0] + previous_column[height - 1]