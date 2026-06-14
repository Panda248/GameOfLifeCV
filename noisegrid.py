from noise import pnoise3

class NoiseGrid:
    def __init__(self, cols: int, rows: int, 
                 seed: int = 0, scale: float = 0.1, time_step: float = 0.1):
        self.cols = cols
        self.rows = rows
        self.seed = seed
        self.scale = scale
        self.time_step = time_step
        self.timer = 0
        self.grid = [[self.noise(j, i, self.timer)
                      for j in range(cols)] for i in range(rows)]

    def get_cell(self, r: int, c: int) -> float:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return 0.0

    def noise(self, x: int, y: int, t: float, 
              min_val: float = 0.0, max_val: float = 1.0) -> float:
        value = pnoise3(x * self.scale, y * self.scale, 
                        t * self.scale, base=self.seed)
        value = min(1, max(-1, value)) # bruh
        return (value + 1) / 2.0

    def update(self):
        self.timer += self.time_step
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = self.noise(c, r, self.timer)
