import pytest
from grid import Grid
from search import get_full_grids
from lookup import init_vocab


@pytest.mark.parametrize("width,height,vocab,expected", [
    (2, 2, {'ab', 'bb'}, 2),
    (2, 2, {'ab', 'dd'}, 0),
    (2, 2, {'ab', 'bb', 'cb', 'dd'}, 6),
    (3, 3, {'abc', 'bbb', 'ba', 'ca', 'ddd', 'dd'}, 2),
    (3, 3, {'arc', 'cv', 'ara', 'a'}, 0),
    (3, 3, {'are', 'ara', 'en', 'an'}, 2),
    (4, 4, {'aube', 'bus', 'but', 'beta', 'des', 'cube'}, 0),
    (4, 4, {'aube', 'bus', 'but', 'beta', 'desa', 'cube'}, 4),
    (4, 4, {'clan', 'aléa', 'ému', 'ami', 'bai', 'an'}, 0)
])
def test_search(width, height, vocab, expected):
    found_grids = get_full_grids(width, height, vocab)
    assert len(found_grids) == expected


@pytest.fixture
def vocab():
    return init_vocab()


@pytest.mark.parametrize("width,height", [(2, 2), (3, 3)])
def test_vocab_search(width, height, vocab):
    found_grids = get_full_grids(width, height, vocab)
    assert found_grids
