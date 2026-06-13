from grid import Grid


def test_init():
    g = Grid(4, 3)
    assert g.cols == 4
    assert g.rows == 3
    assert len(g.grid) == g.rows + 2
    assert len(g.grid[0]) == g.cols + 2
    assert all(all(cell == 0 for cell in row) for row in g.grid)


def test_set_get_cell_inside():
    g = Grid(3, 3)
    g.set_cell(1, 1, 1)
    assert g.get_cell(1, 1) == 1


def test_set_cell_out_of_bounds_does_nothing():
    g = Grid(2, 2)
    g.set_cell(-1, 0, 1)
    g.set_cell(0, 2, 1)
    # ensure valid cells unchanged
    assert g.get_cell(0, 0) == 0
    assert g.get_cell(1, 1) == 0


def test_get_cell_out_of_bounds_returns_zero():
    g = Grid(2, 2)
    assert g.get_cell(-1, 0) == 0
    assert g.get_cell(10, 10) == 0


def test_count_alive_neighbors_center():
    g = Grid(3, 3)
    neighbors = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    for r, c in neighbors:
        g.set_cell(r, c, 1)
    assert g.count_alive_neighbors(1, 1) == 8


def test_count_alive_neighbors_corner():
    g = Grid(3, 3)
    # top-left corner (0,0) has three neighbors set
    g.set_cell(0, 1, 1)
    g.set_cell(1, 0, 1)
    g.set_cell(1, 1, 1)
    assert g.count_alive_neighbors(0, 0) == 3

if __name__ == "__main__":
    test_init()
    test_set_get_cell_inside()
    test_set_cell_out_of_bounds_does_nothing()
    test_get_cell_out_of_bounds_returns_zero()
    test_count_alive_neighbors_center()
    test_count_alive_neighbors_corner()
    print("All tests passed!")