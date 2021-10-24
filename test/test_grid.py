from grid import Grid


def test_find_valid_grids_4_4():
    grid = Grid(5, 5, set())
    expansion = 'vertical'
    switchable_values = grid.expand(expansion)
    valid_grids = []
    grid.find_valid_grids(switchable_values, valid_grids)
    assert valid_grids == [set(),
                           {(5, 2)},
                           {(3, 4)},
                           {(3, 4), (5, 2)},
                           {(3, 3)},
                           {(3, 3), (5, 2)},
                           {(4, 1)},
                           {(4, 1), (5, 2)},
                           {(4, 1), (3, 4)},
                           {(4, 1), (3, 4), (5, 2)},
                           {(3, 3), (4, 1)},
                           {(3, 3), (4, 1), (5, 2)}]


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
