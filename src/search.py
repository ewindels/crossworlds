from itertools import chain
from grid import Grid
from copy import copy

def recursive_search(vocab_set: set[str], grid: Grid, found_grids: list[dict]):
    if grid.settable_squares:
        row_n, col_n, direction = grid.max_settable_square
    else:
        if all(square != '' for square in chain.from_iterable(grid.grid)):
            found_grids.append(copy(grid.words_dict))
        return
    for word in list(vocab_set):
        if grid.check_word(direction, row_n, col_n, word):
            vocab_set.discard(word)
            grid.set_word(direction, row_n, col_n, word)
            recursive_search(vocab_set, grid, found_grids)
            grid.remove_word(direction, row_n, col_n, word)
            vocab_set.add(word)