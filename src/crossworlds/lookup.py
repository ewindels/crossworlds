import os
import json
from string import ascii_uppercase
from collections import defaultdict
from unidecode import unidecode


LookupDict = dict[tuple[int, str], set[str]]


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
    return ''.join(letter for letter in unidecode(string).upper() if letter in ascii_uppercase)


def update_lookups(words_lookups_dict: LookupDict, word: str) -> None:
    for index, letter in enumerate(normalize(word)):
        words_lookup = words_lookups_dict.get((index, letter), set())
        words_lookup.add(word)
        if (index, letter) not in words_lookups_dict:
            words_lookups_dict[(index, letter)] = words_lookup


def build_lookups(vocab: dict[str, set[str]]) -> tuple[LookupDict, dict[int, set[str]]]:
    words_lookups_dict = {}
    vocab_length_dict = defaultdict(set)
    for word in vocab:
        update_lookups(words_lookups_dict, word)
        vocab_length_dict[len(word)].add(word)
    return words_lookups_dict, vocab_length_dict
