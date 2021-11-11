from copy import copy
from crossworlds.grid import WordGrid


def recursive_search(grid: WordGrid,
                     found_grids: list[tuple[dict, str]]) -> None:
    if grid.word_patterns:
        word_pattern = grid.best_word_pattern
        if word_pattern.complexity_score == 0:
            return
    else:
        found_grids.append((copy(grid.words_dict), grid.prettify()))
        return
    for word in word_pattern.match_lookups():
        grid.vocab_length_dict[len(word)].discard(word)
        word_pattern.set_word(word)
        recursive_search(grid, found_grids)
        word_pattern.remove_word()
        grid.vocab_length_dict[len(word)].add(word)


def get_full_grids(height: int,
                   width: int,
                   definitions: set,
                   vocab: dict[str, set[str]]) -> list[dict]:
    grid = WordGrid(height, width, definitions, vocab)
    found_grids = []
    recursive_search(grid, found_grids)
    return found_grids
