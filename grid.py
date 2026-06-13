# Grid class for Game of Life implementation
# uses a padded grid
# TODO gpu accelerate so each cell runs their update in parallel
class Grid:
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.grid = [[0 for _ in range(cols + 2)] for _ in range(rows + 2)]
        print(f"Initialized grid with {cols} cols and {rows} rows")

    def set_cell(self, r: int, c: int, value: int):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            print(f"Cell coordinates ({r}, {c}) are out of bounds")
            return
        self.grid[r + 1][c + 1] = value

    def get_cell(self, r: int, c: int) -> int:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r + 1][c + 1]
        return 0

    def count_alive_neighbors(self, r: int, c: int) -> int:
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                count += self.get_cell(nr, nc)
        return count

    def update(self):
        new_grid = [[0 for _ in range(self.cols + 2)] 
                    for _ in range(self.rows + 2)]
        for r in range(self.rows):
            for c in range(self.cols):
                alive_neighbors = self.count_alive_neighbors(r, c)
                if self.get_cell(r, c) == 1:  # currently alive
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        new_grid[r + 1][c + 1] = 0  # dies
                    else:
                        new_grid[r + 1][c + 1] = 1  # stays alive
                else:  # currently dead
                    if alive_neighbors == 3:
                        new_grid[r + 1][c + 1] = 1  # becomes alive
                    else:
                        new_grid[r + 1][c + 1] = 0  # stays dead
        self.grid = new_grid