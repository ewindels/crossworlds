import pytest
from crossworlds.grid import Grid, WordGrid, WordPatternHorizontal, WordPatternVertical


def test_parse_str():
    with open('output/grids/5x5.grids', 'r', encoding='utf-8') as fp:
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
    with open(f'output/grids/{height}x{width}.grids', 'r', encoding='utf-8') as fp:
        for values_str in fp.read().splitlines():
            grid = Grid(height, width, Grid.parse_str(values_str))
            valid_grids = grid.find_valid_grids_expansion(expansion)
            for values in valid_grids:
                assert not ((2, 3) in values and (2, 4) in values)


@pytest.mark.parametrize("grid,expected_word_patterns", [
    (WordGrid(3, 3, set(), {}), {
        WordPatternVertical(0, 1, 3, WordGrid(3, 3, set(), {})),
        WordPatternVertical(1, 2, 2, WordGrid(3, 3, set(), {})),
        WordPatternHorizontal(1, 0, 3, WordGrid(3, 3, set(), {})),
        WordPatternHorizontal(2, 1, 2, WordGrid(3, 3, set(), {})),
    }),
    (WordGrid(5, 5, {(2, 2)}, {}), {
        WordPatternVertical(0, 1, 5, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternVertical(1, 2, 4, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternVertical(0, 3, 5, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternVertical(1, 4, 4, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternHorizontal(1, 0, 5, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternHorizontal(2, 1, 4, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternHorizontal(3, 0, 5, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternHorizontal(4, 1, 4, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternVertical(3, 2, 2, WordGrid(5, 5, {(2, 2)}, {})),
        WordPatternHorizontal(2, 3, 2, WordGrid(5, 5, {(2, 2)}, {})),
    }),
])
def test_init_word_patterns(grid, expected_word_patterns):
    assert grid.word_patterns == expected_word_patterns


def test_prettify():
    grid = WordGrid(2, 2, {}, {})
    grid.letters = {
        (0, 1): 'A',
        (1, 0): 'B',
        (1, 1): 'B'
    }
    pretty_grid = grid.prettify()
    assert pretty_grid == '┌───┬───┐\n│   │ A │\n├───┼───┤\n│ B │ B │\n└───┴───┘\n'
