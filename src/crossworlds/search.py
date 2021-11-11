from copy import copy
from crossworlds.grid import WordGrid
from crossworlds.lookup import LookupDict, build_lookups


def recursive_search(words_lookups_dict: LookupDict,
                     vocab_length_dict: dict[int, set[str]],
                     grid: WordGrid,
                     found_grids: list[tuple[dict, str]]) -> None:
    if grid.word_patterns:
        word_pattern = grid.best_word_pattern
    else:
        found_grids.append((copy(grid.words_dict), grid.prettify()))
        return
    for word in word_pattern.match_lookups(words_lookups_dict, vocab_length_dict):
        vocab_length_dict[len(word)].discard(word)
        word_pattern.set_word(word)
        recursive_search(words_lookups_dict, vocab_length_dict, grid, found_grids)
        word_pattern.remove_word()
        vocab_length_dict[len(word)].add(word)


def get_full_grids(height: int,
                   width: int,
                   definitions: set,
                   vocab: dict[str, set[str]]) -> list[dict]:
    words_lookups_dict, vocab_length_dict = build_lookups(vocab)
    grid = WordGrid(height, width, definitions)
    found_grids = []
    recursive_search(words_lookups_dict, vocab_length_dict, grid, found_grids)
    return found_grids
