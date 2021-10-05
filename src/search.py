import os
import json
from copy import copy
from grid import Grid

def recursive_search(vocab_set: set[str], grid: Grid, found_grids: list[dict]) -> None:
    if grid.word_starts:
        word_start = grid.best_word_start
    else:
        if grid.is_full:
            found_grids.append(copy(grid.words_dict))
        return
    for word in sorted(vocab_set):
        if grid.check_word(word_start, word):
            vocab_set.discard(word)
            grid.set_word(word_start, word)
            recursive_search(vocab_set, grid, found_grids)
            grid.remove_word(word_start, word)
            vocab_set.add(word)

def init_vocab() -> set[str]:
    vocab_set = set()
    translations_dir = os.path.join('data', 'translations')
    for vocab_json in os.listdir(translations_dir):
        with open(os.path.join(translations_dir, vocab_json), 'r', encoding='utf-8') as fp:
            vocab_set.update(json.load(fp))
    return vocab_set
