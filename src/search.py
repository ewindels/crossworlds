from grid import Grid
from copy import copy

def recursive_search(vocab_set: set[str], grid: Grid, found_grids: list[dict]) -> None:
    if grid.word_starts:
        word_start = grid.best_word_start
    else:
        if grid.is_full:
            found_grids.append(copy(grid.words_dict))
        return
    for word in list(vocab_set):
        if grid.check_word(word_start, word):
            vocab_set.discard(word)
            grid.set_word(word_start, word)
            recursive_search(vocab_set, grid, found_grids)
            grid.remove_word(word_start, word)
            vocab_set.add(word)
