import pytest
from grid import Grid


@pytest.fixture()
def grid():
    return Grid(3, 3)


def test_set_word_letter_indices(grid):
    word_pattern = grid.crossing_word_patterns[1, 1].horizontal
    word_pattern.set_word('abc')
    assert grid.crossing_word_patterns[1, 1].vertical.letters_indices == {1}
    assert grid.crossing_word_patterns[1, 2].vertical.letters_indices == {0}
