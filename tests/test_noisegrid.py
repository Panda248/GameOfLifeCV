import math
from noisegrid import NoiseGrid


def grids_equal(g1, g2, rel_tol=1e-9, abs_tol=1e-9):
    if len(g1) != len(g2):
        return False
    for r1, r2 in zip(g1, g2):
        if len(r1) != len(r2):
            return False
        for a, b in zip(r1, r2):
            if not math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol):
                return False
    return True


def test_constructor_dimensions():
    cols, rows = 5, 4
    ng = NoiseGrid(cols=cols, rows=rows)
    assert ng.cols == cols
    assert ng.rows == rows
    assert isinstance(ng.grid, list)
    assert len(ng.grid) == rows
    assert all(len(row) == cols for row in ng.grid)


def test_constructor_determinism_by_seed():
    cols, rows = 6, 6
    a = NoiseGrid(cols, rows, seed=123, scale=0.5)
    b = NoiseGrid(cols, rows, seed=123, scale=0.5)
    c = NoiseGrid(cols, rows, seed=124, scale=0.5)
    assert grids_equal(a.grid, b.grid)
    assert not grids_equal(a.grid, c.grid)


def test_values_in_expected_range():
    ng = NoiseGrid(3, 3)
    for row in ng.grid:
        for v in row:
            assert -1.0 <= v <= 1.0

def main():
    test_constructor_dimensions()
    test_constructor_determinism_by_seed()
    test_values_in_expected_range()
    print("All tests passed!")

if __name__ == "__main__":
    main()