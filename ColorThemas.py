"""
Варіант 1. Заливка поля (Flood Fill).

Алгоритм flood fill визначає область, пов'язану з певним вузлом
у багатовимірному масиві, та замінює колір усіх вузлів цієї
області на колір заміни.

Формат вхідного файлу input.txt:
    рядок 1: висота та ширина поля (розділені комою), напр. 10,10
    рядок 2: координати початкової точки (рядок,стовпець), напр. 3,9
    рядок 3: колір заміни у лапках, напр. 'C'
    рядки 4+: рядки матриці у форматі ['A', 'B', ...],

Результат записується у файл output.txt.
"""

from collections import deque


def flood_fill(
    grid: list[list[str]],
    start_row: int,
    start_col: int,
    replacement_color: str,
) -> list[list[str]]:
    rows = len(grid)
    cols = len(grid[0])
    target_color = grid[start_row][start_col]

    if target_color == replacement_color:
        return [row[:] for row in grid]

    result = [row[:] for row in grid]

    queue = deque()
    queue.append((start_row, start_col))
    result[start_row][start_col] = replacement_color

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current_row, current_col = queue.popleft()

        for delta_row, delta_col in directions:
            neighbor_row = current_row + delta_row
            neighbor_col = current_col + delta_col

            if (
                0 <= neighbor_row < rows
                and 0 <= neighbor_col < cols
                and result[neighbor_row][neighbor_col] == target_color
            ):
                result[neighbor_row][neighbor_col] = replacement_color
                queue.append((neighbor_row, neighbor_col))

    return result


def parse_color(raw: str) -> str:
    cleaned = raw.strip().strip("'\"")
    if not cleaned:
        raise ValueError(f"Неможливо розпізнати колір з рядка: {raw!r}")
    return cleaned[0]


def parse_grid_line(line: str) -> list[str]:
    cleaned = line.strip().rstrip(",").strip("[]")
    cells = [token.strip().strip("'\"") for token in cleaned.split(",")]
    return [cell for cell in cells if cell]


def read_input(
    filepath: str,
) -> tuple[list[list[str]], int, int, str]:
    with open(filepath, encoding="utf-8") as file:
        lines = [line.rstrip("\n") for line in file]

    non_empty = [line for line in lines if line.strip()]

    if len(non_empty) < 4:
        raise ValueError(
            "Файл має містити щонайменше 4 рядки: "
            "розміри, координати, колір заміни та матрицю."
        )

    size_parts = non_empty[0].split(",")
    height = int(size_parts[0].strip())
    width = int(size_parts[1].strip())

    coord_parts = non_empty[1].split(",")
    start_row = int(coord_parts[0].strip())
    start_col = int(coord_parts[1].strip())

    replacement_color = parse_color(non_empty[2])

    grid = [parse_grid_line(line) for line in non_empty[3:]]

    if len(grid) != height:
        raise ValueError(
            f"Очікувано {height} рядків матриці, отримано {len(grid)}."
        )
    for i, row in enumerate(grid):
        if len(row) != width:
            raise ValueError(
                f"Рядок {i} матриці має {len(row)} клітинок, "
                f"очікувалось {width}."
            )

    return grid, start_row, start_col, replacement_color


def write_output(filepath: str, grid: list[list[str]]) -> None:
    with open(filepath, "w", encoding="utf-8") as file:
        for row in grid:
            formatted = "[" + ", ".join(f"'{cell}'" for cell in row) + "]"
            file.write(formatted + "\n")
    

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"

    grid, start_row, start_col, replacement_color = read_input(input_file)

    target_color = grid[start_row][start_col]
    print(f"Початкова точка: ({start_row}, {start_col})")
    print(f"Цільовий колір (target): '{target_color}'")
    print(f"Колір заміни (replacement): '{replacement_color}'")

    result = flood_fill(grid, start_row, start_col, replacement_color)

    write_output(output_file, result)
    print(f"Результат збережено у файл '{output_file}'.")
