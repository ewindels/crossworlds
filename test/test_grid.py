import pytest
from grid import Grid


@pytest.fixture()
def grid_3_3():
    return Grid(3, 3)


def test_load_from_string(grid_3_3):
    grid_3_3.load_from_string('101\n000\n101')
    assert (2, 2) in grid_3_3.values


@pytest.fixture()
def grid_4_4():
    return Grid(4, 4)


def test_find_valid_grids_4_4(grid_4_4):
    expansion = 'vertical'
    grid_4_4.expand(expansion)
    switchable_values = grid_4_4.switchable_values(expansion)
    valid_grids = []
    grid_4_4.find_valid_grids(switchable_values, valid_grids)
    assert valid_grids == ['1010\n0000\n1000\n0000\n1000\n', '1010\n0000\n1001\n0000\n1000\n']
