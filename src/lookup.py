import os
import json
from collections import defaultdict
from unidecode import unidecode


class WordsLookup:
    def __init__(self, index: int, letter: str):
        self.vocab = set()
        self.index = index
        self.letter = letter


LookupDict = dict[tuple[int, str], WordsLookup]


def init_vocab() -> set[str]:
    vocab_set = set()
    translations_dir = os.path.join('data', 'translations')
    for vocab_json in os.listdir(translations_dir):
        with open(os.path.join(translations_dir, vocab_json), 'r', encoding='utf-8') as fp:
            vocab_set.update(json.load(fp))
    print(f'{len(vocab_set)} words in vocabulary')
    return vocab_set


def normalize(string: str) -> str:
    return unidecode(string).upper()


def update_lookups(words_lookups_dict: LookupDict, word: str) -> None:
    for index, letter in enumerate(normalize(word)):
        words_lookup = words_lookups_dict.get((index, letter), WordsLookup(index, letter))
        words_lookup.vocab.add(word)
        if (index, letter) not in words_lookups_dict:
            words_lookups_dict[(index, letter)] = words_lookup


def build_lookups(vocab: set[str]) -> tuple[LookupDict, dict[int, set[str]]]:
    words_lookups_dict = {}
    vocab_length_dict = defaultdict(set)
    for word in vocab:
        update_lookups(words_lookups_dict, word)
        vocab_length_dict[len(word)].add(word)
    return words_lookups_dict, vocab_length_dict
