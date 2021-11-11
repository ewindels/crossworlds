import pytest
from crossworlds.search import get_full_grids
# from crossworlds.lookup import init_vocab


@pytest.mark.parametrize(("width", "height", "vocab", "expected"), [
    (2, 2, {'AB': set(), 'BB': set()}, 2),
    (2, 2, {'AB': set(), 'DD': set()}, 0),
    (2, 2, {'AB': set(), 'BB': set(), 'CB': set(), 'DD': set()}, 6),
    (3, 3, {'ABC': set(), 'BBB': set(), 'BA': set(), 'CA': set(), 'DDD': set(), 'DD': set()}, 2),
    (3, 3, {'ARC': set(), 'CV': set(), 'ARA': set(), 'A': set()}, 0),
    (3, 3, {'ARE': set(), 'ARA': set(), 'EN': set(), 'AN': set()}, 2),
    (4, 4, {'AUBE': set(), 'BUS': set(), 'BUT': set(), 'BETA': set(), 'DES': set(), 'CUBE': set()}, 0),
    (4, 4, {'AUBE': set(), 'BUS': set(), 'BUT': set(), 'BETA': set(), 'DESA': set(), 'CUBE': set()}, 4),
    (4, 4, {'CLAN': set(), 'ALEA': set(), 'EMU': set(), 'AMI': set(), 'BAI': set(), 'AN': set()}, 0),
    (4, 4, {'HUIT': set(), 'JUDO': set(), 'DO': set(), 'ION': set(), 'CON': set(), 'ET': set()}, 0)
])
def test_search(height, width, vocab, expected):
    found_grids = get_full_grids(height, width, {}, vocab, False)
    assert len(found_grids) == expected


def test_prettify():
    found_grids = get_full_grids(2, 2, {}, {'AB': set(), 'BB': set()}, True)
    pretty_grids = set(found_grids)
    assert pretty_grids ==  {'┌───┬───┐\n│   │ B │\n├───┼───┤\n│ A │ B │\n└───┴───┘\n',
                             '┌───┬───┐\n│   │ A │\n├───┼───┤\n│ B │ B │\n└───┴───┘\n'}
