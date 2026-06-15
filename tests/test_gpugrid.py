from grid import Grid
from gpugrid import GPUGrid

def test_init():
    g = GPUGrid(4, 3)
    assert g.cols == 4
    assert g.rows == 3
    assert len(g.grid) == g.rows + 2
    assert len(g.grid[0]) == g.cols + 2
    assert all(all(cell == 0 for cell in row) for row in g.grid)

def test_gpu_update():
    g = GPUGrid(3, 3)
    # Blinker pattern
    g.set_cell(1, 0, 1)
    g.set_cell(1, 1, 1)
    g.set_cell(1, 2, 1)

    ref = Grid(3, 3)
    ref.set_cell(1,0,1)
    ref.set_cell(1,1,1)
    ref.set_cell(1,2,1)

    # TODO implement gpu_update and test it correctly updates the grid
    g.update()
    ref.update()

    assert all(g.get_cell(r, c) == ref.get_cell(r, c) for r in range(3) for c in range(3))

if __name__ == "__main__":
    test_init()
    test_gpu_update()
    print("All tests passed!")