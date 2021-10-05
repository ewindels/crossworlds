import pytest
from grid import Grid
from search import recursive_search

@pytest.fixture
def grid():
    return Grid((2, 2))

@pytest.fixture
def vocab():
    return {'ab', 'bb', 'cb', 'dd'}

def test_search(grid, vocab):
    found_grids = []
    recursive_search(vocab, grid, found_grids)
    assert len(found_grids) == 6
