from grid import Grid


def test_parse_str():
    with open(f'output/5x5.grids', 'r') as fp:
        for values_str in fp.read().splitlines():
            _ = Grid(5, 5, Grid.parse_str(values_str))


def test_switchable_values():
    grid = Grid(5, 5, set())
    expansion = 'horizontal'
    switchable_values = grid.expand(expansion)
    valid_grids = []
    grid.find_valid_grids(switchable_values, valid_grids)
    assert (3, 5) not in switchable_values


def test_switchable_values_2():
    height = 5
    width = 8
    expansion = 'horizontal'
    with open(f'output/{height}x{width}.grids', 'r') as fp:
        for values_str in fp.read().splitlines():
            grid = Grid(height, width, Grid.parse_str(values_str))
            valid_grids = grid.find_valid_grids_expansion(expansion)
            for values in valid_grids:
                assert not ((2, 3) in values and (2, 4) in values)
