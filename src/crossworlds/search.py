from copy import copy
from typing import Union
from crossworlds.grid import WordGrid


def recursive_search(grid: WordGrid,
                     output_pretty: bool) -> None:
    if grid.word_patterns:
        word_pattern = grid.best_word_pattern
        for word in word_pattern.candidates:
            grid.used_words.add(word)
            word_pattern.set_word(word)
            yield from recursive_search(grid, output_pretty)
            word_pattern.remove_word()
            grid.used_words.remove(word)
    else:
        yield grid.prettify() if output_pretty else copy(grid.words_dict)


def get_full_grids(height: int,
                   width: int,
                   definitions: set,
                   vocab: dict[str, set[str]],
                   output_pretty: bool = False) -> Union[list[dict], list[str]]:
    grid = WordGrid(height, width, definitions, vocab, output_pretty)
    return recursive_search(grid, output_pretty)
