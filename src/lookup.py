import os
import json
from collections import defaultdict
from unidecode import unidecode


class WordsLookup:
    def __init__(self, index: int, letter: str):
        self.vocab = defaultdict(set)
        self.index = index
        self.letter = letter


LookupDict = dict[tuple[int, str], WordsLookup]


def init_vocab() -> dict[str, set[str]]:
    vocab_dict = defaultdict(set)
    translations_dir = os.path.join('data', 'translations')
    for vocab_json in os.listdir(translations_dir):
        with open(os.path.join(translations_dir, vocab_json), 'r', encoding='utf-8') as fp:
            for word in json.load(fp):
                vocab_dict[normalize(word)].add(word)
    print(f'{len(vocab_dict)} words in vocabulary')
    return vocab_dict


def normalize(string: str) -> str:
    return unidecode(string).upper()


def update_lookups(words_lookups_dict: LookupDict, word: str) -> None:
    for index, letter in enumerate(normalize(word)):
        words_lookup = words_lookups_dict.get((index, letter), WordsLookup(index, letter))
        words_lookup.vocab[len(word)].add(word)
        if (index, letter) not in words_lookups_dict:
            words_lookups_dict[(index, letter)] = words_lookup


def build_lookups(vocab: dict[str, set[str]]) -> LookupDict:
    words_lookups_dict = {}
    for word in vocab:
        update_lookups(words_lookups_dict, word)
    return words_lookups_dict
