from camera import Camera
from grid import Grid
import cv2 as cv
import pygame
import random
import sys


# Configuration: adjust these values to change resolution and grid size
# Window resolution (pixels)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Grid size (columns, rows)
GRID_COLS = 200
GRID_ROWS = 150

# Appearance
BG_COLOR = (10, 10, 10)
LINE_COLOR = (50, 50, 50)
FPS = 60
TICKS_PER_UPDATE = 1
ALIVE_COLOR = (200, 200, 200)

def generate_random_grid(cols: int, rows: int) -> Grid:
    grid = Grid(cols, rows)
    for r in range(rows):
        for c in range(cols):
            grid.set_cell(r, c, random.choice([0, 1]))
    return grid

def write_from_camera(grid: Grid, camera: Camera):
    frame = camera.get_skin()
    if frame is None:
        return
    frame = cv.resize(frame, (grid.cols, grid.rows))
    for r in range(grid.rows):
        for c in range(grid.cols):
            if(frame[r, c] > 0):
                grid.set_cell(r, c, 1)

def draw_grid(surface : pygame.Surface, grid : Grid,
              width=WINDOW_WIDTH, height=WINDOW_HEIGHT, color=LINE_COLOR):
    cell_w = width / grid.cols
    cell_h = height / grid.rows

    # vertical lines
    for i in range(grid.cols + 1):
        x = int(i * cell_w)
        pygame.draw.line(surface, color, (x, 0), (x, height))

    # horizontal lines
    for j in range(grid.rows + 1):
        y = int(j * cell_h)
        pygame.draw.line(surface, color, (0, y), (width, y))


def draw_cells(surface: pygame.Surface, grid: Grid, 
               width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
               alive_color=ALIVE_COLOR):
    rows = grid.rows
    cols = grid.cols
    if cols == 0 or rows == 0:
        return

    cell_w = int(width / cols)
    cell_h = int(height / rows)

    for r in range(rows):
        for c in range(cols):
            if grid.get_cell(r, c) == 1:
                rect = pygame.Rect(c * cell_w + 1, r * cell_h + 1,
                                   max(0, cell_w - 1), max(0, cell_h - 1))
                pygame.draw.rect(surface, alive_color, rect)

def main():
    print("initializing camera")
    camera = Camera()
    print("camera initialized")

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game Of Life Computer Vis")
    clock = pygame.time.Clock()

    # initialize grid: rows x cols (row = y)
    # grid = generate_random_grid(GRID_COLS, GRID_ROWS)
    grid = Grid(GRID_COLS, GRID_ROWS)
    update_counter = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # toggle cell state on click
                mouse_x, mouse_y = event.pos
                cell_w = WINDOW_WIDTH / grid.cols
                cell_h = WINDOW_HEIGHT / grid.rows
                c = int(mouse_x // cell_w)
                r = int(mouse_y // cell_h)
                current_state = grid.get_cell(r, c)
                grid.set_cell(r, c, 0 if current_state == 1 else 1)

        update_counter += 1
        if update_counter >= TICKS_PER_UPDATE:
            update_counter = 0
            grid.update()  # update grid state for next frame
            write_from_camera(grid, camera)
        # TODO: try one with faster framerate
        screen.fill(BG_COLOR)
        draw_cells(screen, grid)
        draw_grid(screen, grid)

        pygame.display.flip()
        clock.tick(FPS)
    # camera.release()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()

