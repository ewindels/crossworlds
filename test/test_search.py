import pytest
from grid import Grid
from search import recursive_search, init_vocab


@pytest.mark.parametrize("grid,vocab,expected", [
    (Grid(2, 2), {'ab', 'bb'}, 2),
    (Grid(2, 2), {'ab', 'dd'}, 0),
    (Grid(2, 2), {'ab', 'bb', 'cb', 'dd'}, 6),
    (Grid(3, 3), {'abc', 'bbb', 'ba', 'ca', 'ddd', 'dd'}, 2),
    (Grid(3, 3), {'arc', 'cv', 'ara', 'a'}, 0),
    (Grid(3, 3), {'are', 'ara', 'en', 'an'}, 2)
])
def test_search(grid, vocab, expected):
    found_grids = []
    recursive_search(vocab, grid, found_grids)
    assert len(found_grids) == expected


@pytest.fixture
def vocab():
    return init_vocab()


@pytest.mark.parametrize("grid", [Grid(2, 2), Grid(2, 3), Grid(3, 3), Grid(3, 4)])
def test_vocab_search(grid, vocab):
    found_grids = []
    recursive_search(vocab, grid, found_grids)
    assert found_grids
