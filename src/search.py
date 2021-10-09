import os
import json
from copy import copy
from grid import Grid

def recursive_search(vocab_set: set[str], grid: Grid, found_grids: list[dict]) -> None:
    if grid.word_patterns:
        word_pattern = grid.best_word_pattern
    else:
        if grid.is_full:
            found_grids.append(copy(grid.words_dict))
        return
    for word in list(vocab_set):
        if word_pattern.match_word(word):
            vocab_set.discard(word)
            word_pattern.set_word(word)
            recursive_search(vocab_set, grid, found_grids)
            word_pattern.remove_word()
            vocab_set.add(word)

def init_vocab() -> set[str]:
    vocab_set = set()
    translations_dir = os.path.join('data', 'translations')
    for vocab_json in os.listdir(translations_dir):
        with open(os.path.join(translations_dir, vocab_json), 'r', encoding='utf-8') as fp:
            vocab_set.update(json.load(fp))
    return vocab_set
