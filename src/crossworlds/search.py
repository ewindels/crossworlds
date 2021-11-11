from copy import copy
from typing import Union
from crossworlds.grid import WordGrid


def recursive_search(grid: WordGrid,
                     found_grids: list[tuple[dict, str]],
                     output_pretty: bool) -> None:
    if grid.word_patterns:
        word_pattern = grid.best_word_pattern
        if not word_pattern.candidates:
            return
    else:
        if output_pretty:
            found_grids.append(grid.prettify())
        else:
            found_grids.append(copy(grid.words_dict))
        return
    for word in word_pattern.candidates:
        grid.used_words.add(word)
        word_pattern.set_word(word)
        recursive_search(grid, found_grids, output_pretty)
        word_pattern.remove_word()
        grid.used_words.remove(word)


def get_full_grids(height: int,
                   width: int,
                   definitions: set,
                   vocab: dict[str, set[str]],
                   output_pretty: bool = False) -> Union[list[dict], list[str]]:
    grid = WordGrid(height, width, definitions, vocab, output_pretty)
    found_grids = []
    recursive_search(grid, found_grids, output_pretty)
    return found_grids
