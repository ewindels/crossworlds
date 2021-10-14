from __future__ import annotations
from abc import ABC, abstractmethod
from itertools import chain
from collections import defaultdict
from typing import Optional, Union
from lookup import LookupDict, normalize

EMPTY_TOKEN = ''
DEF_TOKEN = '[def]'


class CrossingWordPatterns:
    def __init__(self,
                 horizontal: Optional[WordPatternHorizontal] = None,
                 vertical: Optional[WordPatternVertical] = None
                 ) -> None:
        self.horizontal = horizontal
        self.vertical = vertical

    def get_aligned(self, word_pattern: WordPattern) -> Union[None, WordPattern]:
        if isinstance(word_pattern, WordPatternHorizontal):
            return self.horizontal
        elif isinstance(word_pattern, WordPatternVertical):
            return self.vertical

    def set_aligned(self, word_pattern: WordPattern) -> None:
        if isinstance(word_pattern, WordPatternHorizontal):
            self.horizontal = word_pattern
        elif isinstance(word_pattern, WordPatternVertical):
            self.vertical = word_pattern

    def get_orthogonal(self, word_pattern: WordPattern) -> Union[None, WordPattern]:
        if isinstance(word_pattern, WordPatternHorizontal):
            return self.vertical
        elif isinstance(word_pattern, WordPatternVertical):
            return self.horizontal

    def set_orthogonal(self, word_pattern: Optional[WordPattern]) -> None:
        if isinstance(word_pattern, WordPatternHorizontal):
            self.vertical = word_pattern
        elif isinstance(word_pattern, WordPatternVertical):
            self.horizontal = word_pattern


class WordPattern(ABC):
    def __init__(self, row: int, col: int, length: int, grid: Grid) -> None:
        self.row = row
        self.col = col
        self.length = 0
        self.grid = grid
        self.valid_word_lengths = set()
        self.set_length(length)
        self.letters_indices = set()
        self.linked_letters_indices = set()
        self.filled = False

    @abstractmethod
    def get_coor(self, index: int) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_coor_orthogonal(self, index: int, orthogonal_offset: int) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_index(self, row: int, col: int) -> int:
        pass

    @abstractmethod
    def create_pattern_aligned(self, row: int, col: int, length: int) -> WordPattern:
        pass

    @abstractmethod
    def create_pattern_orthogonal(self, row: int, col: int, length: int) -> WordPattern:
        pass

    def get_content(self, index: int) -> Union[None, str]:
        return self.grid.get_content(*self.get_coor(index))

    def get_content_orthogonal(self, index: int, orthogonal_offset: int) -> Union[None, str]:
        return self.grid.get_content(*self.get_coor_orthogonal(index, orthogonal_offset))

    def set_content(self, index: int, content: str) -> None:
        row, col = self.get_coor(index)
        self.grid.set_content(row, col, content)

    def add_letter_index(self, row: int, col: int) -> None:
        index = self.get_index(row, col)
        self.letters_indices.add(index)

    def remove_letter_index(self, row: int, col: int) -> None:
        index = self.get_index(row, col)
        self.letters_indices.discard(index)

    def update_crossing_word_patterns(self, index: int) -> None:
        self.grid.crossing_word_patterns[self.get_coor(index)].set_aligned(self)

    def get_orthogonal_word_pattern(self, index: int) -> Union[None, WordPattern]:
        coor = self.get_coor(index)
        return self.grid.crossing_word_patterns[coor].get_orthogonal(self)

    def update_orthogonal_word_pattern_letters(self, index: int) -> None:
        coor = self.get_coor(index)
        if crossed_word_pattern := self.get_orthogonal_word_pattern(index):
            crossed_word_pattern.add_letter_index(*coor)

    def unset_orthogonal_word_pattern_letters(self, index: int) -> None:
        coor = self.get_coor(index)
        if crossed_word_pattern := self.get_orthogonal_word_pattern(index):
            crossed_word_pattern.remove_letter_index(*coor)

    def update_orthogonal_word_patterns_length(self, index: int) -> None:
        coor = self.get_coor(index)
        if crossed_word_pattern := self.get_orthogonal_word_pattern(index):
            length = crossed_word_pattern.get_index(*coor) - 1
            crossed_word_pattern.set_length(length)

    def unset_orthogonal_word_patterns_length(self, index: int) -> None:
        coor = self.get_coor(index)
        if crossed_word_pattern := self.get_orthogonal_word_pattern(index):
            length = crossed_word_pattern.get_index(*coor) - 1
            crossed_word_pattern.set_length(length)

    def set_aligned_word_pattern(self, def_index: int) -> None:
        if (
                self.get_content(def_index + 2) not in (None, DEF_TOKEN)
                and self.get_content(def_index + 1) != DEF_TOKEN
        ):
            row, col = self.get_coor(def_index + 1)
            new_length = self.length - def_index
            new_aligned_word_pattern = self.create_pattern_aligned(row, col, new_length)
            self.set_length(def_index - 1)
            for new_index in range(new_length):
                new_aligned_word_pattern.update_crossing_word_patterns(new_index)
                if new_index + def_index in self.letters_indices:
                    new_aligned_word_pattern.letters_indices.add(new_index)
            self.grid.word_patterns.add(new_aligned_word_pattern)

    def unset_aligned_word_pattern(self, def_index: int) -> None:
        coor = self.get_coor(def_index + 1)
        if aligned_word_pattern := self.grid.crossing_word_patterns[coor].get_aligned(self):
            previous_length = self.length + aligned_word_pattern.length + 1
            self.set_length(previous_length)
            self.grid.word_patterns.discard(aligned_word_pattern)
            del aligned_word_pattern

    def set_orthogonal_word_pattern(self, def_index: int) -> None:
        if (
                self.get_content_orthogonal(def_index, 2) not in (None, DEF_TOKEN)
                and self.get_content_orthogonal(def_index, 1) != DEF_TOKEN
                and (orthogonal_word_pattern := self.get_orthogonal_word_pattern(def_index))
        ):
            row, col = self.get_coor_orthogonal(def_index, 1)
            orthogonal_length = orthogonal_word_pattern.length
            orthogonal_def_index = orthogonal_word_pattern.get_index(*self.get_coor(def_index))
            new_length = orthogonal_length - orthogonal_def_index
            new_orthogonal_word_pattern = self.create_pattern_orthogonal(row, col, new_length)
            orthogonal_word_pattern.set_length(orthogonal_def_index - 1)
            for new_index in range(orthogonal_length):
                new_orthogonal_word_pattern.update_crossing_word_patterns(new_index)
                if new_index + def_index in orthogonal_word_pattern.letters_indices:
                    new_orthogonal_word_pattern.letters_indices.add(new_index)
            self.grid.word_patterns.add(new_orthogonal_word_pattern)

    def unset_orthogonal_word_pattern(self, def_index: int) -> None:
        coor = self.get_coor_orthogonal(def_index, 1)
        if orthogonal_word_pattern := self.grid.crossing_word_patterns[coor].get_orthogonal(self):
            coor_prev = self.get_coor_orthogonal(def_index, -1)
            if prev_orthogonal_word_pattern := self.grid.crossing_word_patterns[coor_prev].get_orthogonal(self):
                previous_length = orthogonal_word_pattern.length + prev_orthogonal_word_pattern.length + 1
                prev_orthogonal_word_pattern.set_length(previous_length)
            else:
                for index in range(orthogonal_word_pattern.length):
                    coor_index = orthogonal_word_pattern.get_coor(index)
                    self.grid.crossing_word_patterns[coor_index].set_orthogonal(None)
            self.grid.word_patterns.discard(orthogonal_word_pattern)
            del orthogonal_word_pattern

    def set_length(self, length: int) -> None:
        if length > self.length:
            for index in range(self.length, length):
                if (
                        self.get_content(index + 1) is None
                        or (
                        self.get_content(index + 1) == EMPTY_TOKEN
                        and (
                                self.get_content(index + 3) != DEF_TOKEN
                                and self.get_content_orthogonal(index + 1, 2) != DEF_TOKEN
                                and self.get_content_orthogonal(index + 1, -2) not in (DEF_TOKEN, None)
                            )
                        )
                ):
                    self.valid_word_lengths.add(index + 1)
                self.update_crossing_word_patterns(index)
        else:
            for valid_length in self.valid_word_lengths.copy():
                if valid_length > length:
                    self.valid_word_lengths.discard(valid_length)

    def match_word(self, word: str) -> bool:
        return (
            len(word) in self.valid_word_lengths
            and all(normalize(word[index]) == self.get_content(index) for index in self.letters_indices)
        )

    def match_vocab(self, vocab: set[str]) -> str:
        for word in list(vocab):
            if self.match_word(word):
                yield word

    def match_lookups(self, words_lookups_dict: LookupDict, vocab_length_dict: dict[int, set[str]]):
        matching_words = set(chain.from_iterable(vocab_length_dict.get(length, {})
                                                 for length in self.valid_word_lengths))
        for index in self.letters_indices:
            letter = self.get_content(index)
            if not (lookup := words_lookups_dict.get((index, letter))):
                return {}
            matching_words = matching_words.intersection(lookup.vocab)
            if not matching_words:
                return {}
        return matching_words

    def set_word(self, word: str) -> None:
        self.grid.words_dict[self] = word
        self.grid.word_patterns.discard(self)
        for index, letter in enumerate(normalize(word)):
            if self.get_content(index) == EMPTY_TOKEN:
                self.set_content(index, letter)
                self.linked_letters_indices.add(index)
                self.update_orthogonal_word_pattern_letters(index)
        def_index = len(word) + 1
        if self.get_content(def_index) is not None:
            self.set_content(def_index, DEF_TOKEN)
            self.update_orthogonal_word_patterns_length(def_index)
            self.set_aligned_word_pattern(def_index)
            self.set_orthogonal_word_pattern(def_index)

    def remove_word(self) -> None:
        self.grid.words_dict.pop(self)
        self.grid.word_patterns.add(self)
        for index in self.linked_letters_indices:
            self.set_content(index, EMPTY_TOKEN)
            self.unset_orthogonal_word_pattern_letters(index)
        self.linked_letters_indices = set()
        def_index = self.length + 1
        if self.get_content(def_index) == DEF_TOKEN:
            self.set_content(def_index, EMPTY_TOKEN)
            self.unset_orthogonal_word_patterns_length(def_index)
            self.unset_aligned_word_pattern(def_index)
            self.unset_orthogonal_word_pattern(def_index)


class WordPatternHorizontal(WordPattern):
    def __repr__(self) -> str:
        return f'WordPatternH({self.row}, {self.col})'

    def __str__(self) -> str:
        return f'H({self.row}, {self.col})'

    def get_coor(self, index: int) -> tuple[int, int]:
        return self.row, self.col + index

    def get_coor_orthogonal(self, index: int, orthogonal_offset: int) -> tuple[int, int]:
        return self.row + orthogonal_offset, self.col + index

    def get_index(self, row: int, col: int):
        return col - self.col

    def create_pattern_aligned(self, row: int, col: int, length: int) -> WordPatternHorizontal:
        return WordPatternHorizontal(row, col, length, self.grid)

    def create_pattern_orthogonal(self, row: int, col: int, length: int) -> WordPatternVertical:
        return WordPatternVertical(row, col, length, self.grid)

    def get_pattern_aligned(self, row: int, col: int) -> Union[None, WordPatternHorizontal]:
        return self.grid.crossing_word_patterns[(row, col)].horizontal

    def get_pattern_orthogonal(self, row: int, col: int) -> Union[None, WordPatternVertical]:
        return self.grid.crossing_word_patterns[(row, col)].vertical


class WordPatternVertical(WordPattern):
    def __repr__(self) -> str:
        return f'WordPatternV({self.row}, {self.col})'

    def __str__(self) -> str:
        return f'V({self.row}, {self.col})'

    def get_coor(self, index: int) -> tuple[int, int]:
        return self.row + index, self.col

    def get_coor_orthogonal(self, index: int, orthogonal_offset: int) -> tuple[int, int]:
        return self.row + index, self.col + orthogonal_offset

    def get_index(self, row: int, col: int):
        return row - self.row

    def create_pattern_aligned(self, row: int, col: int, length: int) -> WordPatternVertical:
        return WordPatternVertical(row, col, length, self.grid)

    def create_pattern_orthogonal(self, row: int, col: int, length: int) -> WordPatternHorizontal:
        return WordPatternHorizontal(row, col, length, self.grid)

    def get_pattern_aligned(self, row: int, col: int) -> Union[None, WordPatternVertical]:
        return self.grid.crossing_word_patterns[(row, col)].vertical

    def get_pattern_orthogonal(self, row: int, col: int) -> Union[None, WordPatternHorizontal]:
        return self.grid.crossing_word_patterns[(row, col)].horizontal


class Grid:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.words_dict = {}
        self.letters_count = defaultdict(int)
        self.grid = self._init_grid()
        self.crossing_word_patterns = defaultdict(CrossingWordPatterns)
        self.word_patterns = self._init_word_patterns()

    def _init_grid(self) -> list[list[str]]:
        self.grid = [[EMPTY_TOKEN for _ in range(self.width)] for _ in range(self.height)]
        for col in range(0, self.width, 2):
            self.set_content(0, col, DEF_TOKEN)
        for row in range(0, self.height, 2):
            self.set_content(row, 0, DEF_TOKEN)
        return self.grid

    def _init_word_patterns(self) -> set[WordPattern]:
        word_patterns = set()
        for col in range(1, self.width):
            row = (col + 1) % 2
            word_pattern = WordPatternVertical(row, col, self.height - row, self)
            word_patterns.add(word_pattern)
        for row in range(1, self.height):
            col = (row + 1) % 2
            word_pattern = WordPatternHorizontal(row, col, self.width - col, self)
            word_patterns.add(word_pattern)
        return word_patterns

    def __str__(self):
        return self.prettify()

    @property
    def best_word_pattern(self) -> WordPattern:
        return max(self.word_patterns, key=lambda w_pat: (len(w_pat.letters_indices), -w_pat.col, -w_pat.row))

    @property
    def is_full(self) -> bool:
        return all(content != EMPTY_TOKEN for content in chain.from_iterable(self.grid))

    def get_content(self, row: int, col: int) -> Optional[str]:
        if (0 <= row < self.height) and (0 <= col < self.width):
            return self.grid[row][col]

    def set_content(self, row: int, col: int, content: str) -> None:
        self.grid[row][col] = content

    def prettify(self):
        grid_str = '┌──' + ('─┬──' * (self.width - 1)) + '─┐\n'
        for row_n, row in enumerate(self.grid):
            for content in row:
                if content == DEF_TOKEN:
                    grid_str += '│ ■ '
                elif content == EMPTY_TOKEN:
                    grid_str += '│   '
                else:
                    grid_str += f'│ {content} '
            grid_str += '│\n'
            if row_n < self.height - 1:
                grid_str += '├──' + ('─┼──' * (self.width - 1)) + '─┤\n'
            else:
                grid_str += '└──' + ('─┴──' * (self.width - 1)) + '─┘\n'
        return grid_str
