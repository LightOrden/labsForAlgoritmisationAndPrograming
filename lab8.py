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

    return previous_column[0] + previous_column[height - 1]


def read_input() -> tuple[int, int, list[str]]:
    with open("ijones.in", "r", encoding="utf-8") as file:
        width, height = map(int, file.readline().split())

        corridor = [
            file.readline().strip()
            for _ in range(height)
        ]

    return width, height, corridor


def write_output(result: int) -> None:
    with open("ijones.out", "w", encoding="utf-8") as file:
        file.write(str(result))


def main() -> None:
    if not os.path.exists("ijones.in"):
        print("Помилка: файл ijones.in не знайдено.")
        return

    width, height, corridor = read_input()

    result = count_paths(
        width,
        height,
        corridor,
    )

    write_output(result)

    print("Програму виконано успішно.")


if __name__ == "__main__":
    main()