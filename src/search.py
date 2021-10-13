from copy import copy
from grid import Grid
from lookup import LookupDict, build_lookups


def recursive_search(words_lookups_dict: LookupDict,
                     vocab_length_dict: dict[int, set[str]],
                     grid: Grid, found_grids: list[dict]) -> None:
    if grid.word_patterns:
        word_pattern = grid.best_word_pattern
    else:
        if grid.is_full:
            found_grids.append(copy(grid.words_dict))
        return
    for word in word_pattern.match_lookups(words_lookups_dict, vocab_length_dict):
        vocab_length_dict[len(word)].discard(word)
        word_pattern.set_word(word)
        recursive_search(words_lookups_dict, vocab_length_dict, grid, found_grids)
        word_pattern.remove_word()
        vocab_length_dict[len(word)].add(word)


def get_full_grids(width: int, height: int, vocab: set[str]) -> list[dict]:
    words_lookups_dict, vocab_length_dict = build_lookups(vocab)
    grid = Grid(width, height)
    found_grids = []
    recursive_search(words_lookups_dict, vocab_length_dict, grid, found_grids)
    return found_grids
