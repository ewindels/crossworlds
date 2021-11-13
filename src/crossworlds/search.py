from copy import copy
from crossworlds.grid import WordGrid


def recursive_search(grid: WordGrid) -> dict:
    if grid.word_patterns:
        word_pattern = grid.best_word_pattern
        for word in word_pattern.candidates:
            if word_pattern.set_word(word):
                yield from recursive_search(grid)
                grid.word_patterns.add(word_pattern)
                grid.used_words.remove(word)
            word_pattern.unset_word()
    else:
        yield copy(grid.words_dict)


def get_full_grids(height: int,
                   width: int,
                   definitions: set,
                   vocab: dict[str, set[str]]) -> dict:
    grid = WordGrid(height, width, definitions, vocab)
    return recursive_search(grid)
