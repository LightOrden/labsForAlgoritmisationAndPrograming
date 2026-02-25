def zigzag_traversal(matrix):
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])
    result = []

    for s in range(rows + cols - 1):
        if s % 2 == 0:
            row = min(s, rows - 1)
            col = s - row

            while row >= 0 and col < cols:
                result.append(matrix[row][col])
                row -= 1
                col += 1
        else:
            col = min(s, cols - 1)
            row = s - col

            while col >= 0 and row < rows:
                result.append(matrix[row][col])
                row += 1
                col -= 1

    return result