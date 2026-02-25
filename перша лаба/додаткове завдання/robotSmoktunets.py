class RoboVacuum:
    def __init__(self, room, capacity=5):
        self.room = room
        self.rows = len(room)
        self.cols = len(room[0]) if room else 0
        self.capacity = capacity
        self.current_load = 0
        self.returns_to_base = 0
        self.cells_until_full = None

    def clean(self):
        if not self.room or not self.room[0]:
            return 0, 0

        visited_cells = 0

        for s in range(self.rows + self.cols - 1):
            if s % 2 == 0:
                if s < self.rows:
                    row = s
                else:
                    row = self.rows - 1

                col = s - row

                while row >= 0 and col < self.cols:
                    visited_cells += 1
                    dirt = self.room[row][col]

                    if self.current_load + dirt > self.capacity:
                        self.returns_to_base += 1
                        self.current_load = 0

                    self.current_load += dirt

                    if self.current_load == self.capacity and self.cells_until_full is None:
                        self.cells_until_full = visited_cells

                    row -= 1
                    col += 1
            else:
                if s < self.cols:
                    col = s
                else:
                    col = self.cols - 1

                row = s - col

                while col >= 0 and row < self.rows:
                    visited_cells += 1
                    dirt = self.room[row][col]

                    if self.current_load + dirt > self.capacity:
                        self.returns_to_base += 1
                        self.current_load = 0

                    self.current_load += dirt

                    if self.current_load == self.capacity and self.cells_until_full is None:
                        self.cells_until_full = visited_cells

                    row += 1
                    col -= 1

        return self.cells_until_full, self.returns_to_base


if __name__ == "__main__":
    room = [
        [1, 2, 1],
        [2, 1, 1],
        [1, 1, 2]
    ]

    vacuum = RoboVacuum(room, capacity=5)
    full_after, returns = vacuum.clean()

    print("Вперше забився після клітинок:", full_after)
    print("Кількість повернень на базу:", returns)