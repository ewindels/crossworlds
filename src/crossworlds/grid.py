from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from crossworlds.lookup import LookupDict


DEF_TOKEN = '[def]'
Coor = tuple[int, int]


class Grid:
    def __init__(self,
                 height: int,
                 width: int,
                 definitions: set[Coor]) -> None:
        self.height = height
        self.width = width
        self.definitions = definitions

    def is_switch_valid(self,
                        row: int,
                        col: int) -> bool:
        if row == 1:
            if col % 2:
                return False
            elif (
                col < 4
                or (1, col - 2) in self.definitions
                or (1, col - 4) in self.definitions
                or (3, col) in self.definitions
                or (2, col - 1) in self.definitions
                or (2, col + 1) in self.definitions
            ):
                return False
        elif col == 1:
            if row % 2:
                return False
            elif (
                row < 4
                or (row - 2, 1) in self.definitions
                or (row - 4, 1) in self.definitions
                or (row, 3) in self.definitions
                or (row - 1, 2) in self.definitions
                or (row + 1, 2) in self.definitions
            ):
                return False
        else:
            if (
                (row - 1, col) in self.definitions
                or (row, col - 1) in self.definitions
                or (row - 2, col) in self.definitions
                or (row, col - 2) in self.definitions
            ):
                return False
            if (
                (
                    (row - 1, col - 1) in self.definitions
                    and (row - 2, col - 2) in self.definitions
                )
                or (
                    (row - 1, col + 1) in self.definitions
                    and (row - 2, col + 2) in self.definitions
                )
            ):
                return False
            if row == 2:
                if (
                    col % 2 == 0
                    or (1, col - 1) in self.definitions
                    or (3, col - 1) in self.definitions
                    or (3, col + 1) in self.definitions
                ):
                    return False
            elif row == self.height - 1:
                if (
                    (row - 1, col - 1) in self.definitions
                    or (row - 1, col + 1) in self.definitions
                    or col < 4
                ):
                    return False
            elif row == self.height - 2:
                if (
                    (row + 1, col - 1) in self.definitions
                    or (row + 1, col + 1) in self.definitions
                    or (
                        col == 4
                        and (row, 1) in self.definitions
                    )
                ):
                    return False
            if col == 2:
                if (
                    row % 2 == 0
                    or (row - 1, 1) in self.definitions
                    or (row - 1, 3) in self.definitions
                    or (row + 1, 3) in self.definitions
                ):
                    return False
            elif col == self.width - 1:
                if (
                    (row - 1, col - 1) in self.definitions
                    or (row + 1, col - 1) in self.definitions
                    or row < 4
                ):
                    return False
            elif col == self.width - 2:
                if (
                    (row - 1, col + 1) in self.definitions
                    or (row + 1, col + 1) in self.definitions
                    or (
                        row == 4
                        and (1, col) in self.definitions
                    )
                ):
                    return False
            if (
                (
                    row > 5
                    or col > 5
                )
                and (
                    (row - 3, col) in self.definitions
                    or (row, col - 3) in self.definitions
                )
            ):
                return False
            if (
                (
                    row == 5
                    and (
                        (1, col) in self.definitions
                        or (2, col) in self.definitions
                    )
                )
                or (
                    col == 5
                    and (
                        (row, 1) in self.definitions
                        or (row, 2) in self.definitions
                    )
                )
            ):
                return False
            if (
                (
                    (row - 4, col) in self.definitions
                    and (
                        row < 8
                        or (row - 8, col) in self.definitions
                        or (row - 7, col) in self.definitions
                    )
                )
                or (
                    (row, col - 4) in self.definitions
                    and (
                        col < 8
                        or (row, col - 8) in self.definitions
                        or (row, col - 7) in self.definitions
                    )
                ) or (
                    (row, col - 3) in self.definitions
                    and (
                        col < 7
                        or (row, col - 7) in self.definitions
                    )
                ) or (
                    (row - 3, col) in self.definitions
                    and (
                        row < 7
                        or (row - 7, col) in self.definitions
                    )
                )
            ):
                return False
        return True

    def expand(self, direction: str) -> list[Coor]:
        if direction == 'vertical':
            self.height += 1
        elif direction == 'horizontal':
            self.width += 1
        return self.get_switchable_definitions(direction)

    def get_switchable_definitions(self, direction: str) -> list[Coor]:
        switchable_definitions = []
        if direction == 'vertical':
            for col in range(self.width - 3, 1, -1):
                switchable_definitions.extend([(self.height - 1, col), (self.height - 2, col)])
            switchable_definitions.extend([
                (self.height - 3, self.width - 1),
                (self.height - 3, self.width - 2)
            ])
            if self.height % 2 == 0 and self.height > 5:
                switchable_definitions.append((self.height - 5, 1))
        elif direction == 'horizontal':
            for row in range(self.height - 3, 1, -1):
                switchable_definitions.extend([(row, self.width - 1), (row, self.width - 2)])
            switchable_definitions.extend([
                (self.height - 1, self.width - 3),
                (self.height - 2, self.width - 3)
            ])
            if self.width % 2 == 0 and self.width > 5:
                switchable_definitions.append((1, self.width - 5))
        return switchable_definitions

    def find_valid_grids(self,
                         switchable_definitions: list[Coor],
                         valid_grids: list[set[Coor]]) -> None:
        if switchable_definitions:
            row, col = switchable_definitions.pop()
            self.find_valid_grids(switchable_definitions, valid_grids)
            if self.is_switch_valid(row, col):
                self.definitions.add((row, col))
                self.find_valid_grids(switchable_definitions, valid_grids)
                self.definitions.remove((row, col))
            switchable_definitions.append((row, col))
        else:
            valid_grids.append(self.definitions.copy())

    def find_valid_grids_expansion(self, direction: str) -> list[set[Coor]]:
        switchable_definitions = self.expand(direction)
        valid_grids = []
        self.find_valid_grids(switchable_definitions, valid_grids)
        return valid_grids

    @staticmethod
    def parse_str(string: str) -> set[Coor]:
        definitions = set()
        if string:
            for coor in string.split('|'):
                row, col = map(int, coor.split(','))
                definitions.add((row, col))
        return definitions

    @staticmethod
    def to_str(definitions_list: list[set[Coor]]) -> str:
        output = '\n'.join('|'.join(','.join(map(str, coor)) for coor in definitions) for definitions in definitions_list)
        return output

    def prettify(self) -> str:
        pretty_list = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for row, col in self.definitions:
            pretty_list[row][col] = 'X'
        for row in range(0, self.height, 2):
            pretty_list[row][0] = 'X'
        for col in range(0, self.width, 2):
            pretty_list[0][col] = 'X'
        pretty_str = '\n'.join(''.join(row) for row in pretty_list)
        return pretty_str


class WordGrid(Grid):
    def __init__(self,
                 height: int,
                 width: int,
                 definitions: set[Coor]) -> None:
        super().__init__(height, width, definitions)
        self.word_patterns = self._init_word_patterns()
        self.letters = {}
        self.words_dict = {}
        self.crossing_word_patterns = self._init_crossing_word_patterns()

    def _init_word_patterns(self) -> set[WordPattern]:
        word_patterns = set()
        for row, col in self.definitions:
            length = None
            for length in range(self.height):
                if (row + length + 1, col) in self.definitions or row + length + 1 == self.height:
                    break
            if length >= 2:
                word_patterns.add(WordPatternVertical(row + 1, col, length, self))
            for length in range(self.width):
                if (row, col + length + 1) in self.definitions or col + length + 1 == self.width:
                    break
            if length >= 2:
                word_patterns.add(WordPatternHorizontal(row, col + 1, length, self))
        for col in range(1, self.width):
            if col % 2:
                word_patterns.add(WordPatternVertical(0, col, self.height, self))
            elif (1, col) not in self.definitions:
                word_patterns.add(WordPatternVertical(1, col, self.height - 1, self))
        for row in range(1, self.height):
            if row % 2:
                word_patterns.add(WordPatternHorizontal(row, 0, self.width, self))
            elif (row, 1) not in self.definitions:
                word_patterns.add(WordPatternHorizontal(row, 1, self.width - 1, self))
        return word_patterns

    def _init_crossing_word_patterns(self) -> dict[Coor, CrossingWordPatterns]:
        crossing_word_patterns = {}
        for word_pattern in self.word_patterns:
            for index in range(word_pattern.length):
                coor = word_pattern.get_coor(index)
                if coor not in crossing_word_patterns:
                    crossing_word_patterns[coor] = CrossingWordPatterns()
                crossing_word_patterns[coor].set_aligned(word_pattern)
        return crossing_word_patterns

    def get_content(self,
                    row: int,
                    col: int) -> Optional[str]:
        return self.letters.get((row, col))

    def set_content(self,
                    row: int,
                    col: int,
                    content: str) -> None:
        self.letters[(row, col)] = content

    def remove_content(self,
                       row: int,
                       col: int) -> None:
        self.letters.pop((row, col), None)

    @staticmethod
    def score_pattern(pattern: WordPattern) -> tuple[int, int, int]:
        return len(pattern.letters_indices), -pattern.col, -pattern.row

    @property
    def best_word_pattern(self) -> WordPattern:
        return max(self.word_patterns, key=self.score_pattern)

    def prettify(self):
        grid_str = '┌──' + ('─┬──' * (self.width - 1)) + '─┐\n'
        for row in range(self.height):
            for col in range(self.width):
                if letter := self.get_content(row, col):
                    grid_str += f'│ {letter} '
                else:
                    grid_str += '│   '
            grid_str += '│\n'
            if row < self.height - 1:
                grid_str += '├──' + ('─┼──' * (self.width - 1)) + '─┤\n'
            else:
                grid_str += '└──' + ('─┴──' * (self.width - 1)) + '─┘\n'
        return grid_str


class WordPattern(ABC):
    def __init__(self,
                 row: int,
                 col: int,
                 length: int,
                 grid: WordGrid) -> None:
        self.row = row
        self.col = col
        self.length = length
        self.grid = grid
        self.letters_indices = set()
        self.linked_letters_indices = set()

    @abstractmethod
    def get_coor(self,
                 index: int,
                 orthogonal_offset: int = 0) -> Coor:
        pass

    def __eq__(self, other: WordPattern) -> bool:
        return self.row == other.row and self.col == other.col and self.length == other.length

    def __hash__(self) -> str:
        return hash((self.row, self.col, self.length))

    def get_content(self, index: int) -> Optional[str]:
        return self.grid.get_content(*self.get_coor(index))

    def match_lookups(self,
                      words_lookups_dict: LookupDict,
                      vocab_length_dict: dict[int, set[str]]) -> set[str]:
        matching_words = vocab_length_dict[self.length].copy()
        for index in self.letters_indices:
            letter = self.get_content(index)
            if not (lookup := words_lookups_dict.get((index, letter))):
                return {}
            matching_words = matching_words.intersection(lookup.vocab)
            if not matching_words:
                return {}
        return matching_words

    def set_content(self,
                    index: int,
                    content: str) -> None:
        row, col = self.get_coor(index)
        self.grid.set_content(row, col, content)

    def remove_content(self, index: int) -> None:
        row, col = self.get_coor(index)
        self.grid.remove_content(row, col)

    def set_word(self, word: str) -> None:
        self.grid.words_dict[self] = word
        self.grid.word_patterns.discard(self)
        for index, letter in enumerate(word):
            if self.get_content(index) is None:
                self.set_content(index, letter)
                self.linked_letters_indices.add(index)
                self.update_orthogonal_word_pattern_letters(index)

    def remove_word(self) -> None:
        self.grid.words_dict.pop(self)
        self.grid.word_patterns.add(self)
        for index in self.linked_letters_indices:
            self.remove_content(index)
            self.unset_orthogonal_word_pattern_letters(index)
        self.linked_letters_indices = set()

    def get_orthogonal_word_pattern(self, index: int) -> Optional[WordPattern]:
        coor = self.get_coor(index)
        return self.grid.crossing_word_patterns[coor].get_orthogonal(self)

    def update_orthogonal_word_pattern_letters(self, index: int) -> None:
        coor = self.get_coor(index)
        if crossed_word_pattern := self.get_orthogonal_word_pattern(index):
            index = crossed_word_pattern.get_index(*coor)
            crossed_word_pattern.letters_indices.add(index)

    def unset_orthogonal_word_pattern_letters(self, index: int) -> None:
        coor = self.get_coor(index)
        if crossed_word_pattern := self.get_orthogonal_word_pattern(index):
            index = crossed_word_pattern.get_index(*coor)
            crossed_word_pattern.letters_indices.remove(index)


class WordPatternHorizontal(WordPattern):
    def __repr__(self) -> str:
        return f'WordPatternH({self.row}, {self.col} | {self.length})'

    def __str__(self) -> str:
        return f'H({self.row}, {self.col} | {self.length})'

    def get_coor(self,
                 index: int,
                 orthogonal_offset: int = 0) -> Coor:
        return self.row + orthogonal_offset, self.col + index

    def get_index(self,
                  _: int,
                  col: int) -> int:
        return col - self.col


class WordPatternVertical(WordPattern):
    def __repr__(self) -> str:
        return f'WordPatternV({self.row}, {self.col} | {self.length})'

    def __str__(self) -> str:
        return f'V({self.row}, {self.col} | {self.length})'

    def get_coor(self,
                 index: int,
                 orthogonal_offset: int = 0) -> Coor:
        return self.row + index, self.col + orthogonal_offset

    def get_index(self,
                  row: int,
                  _: int) -> int:
        return row - self.row


class CrossingWordPatterns:
    def __init__(self,
                 horizontal: Optional[WordPatternHorizontal] = None,
                 vertical: Optional[WordPatternVertical] = None) -> None:
        self.horizontal = horizontal
        self.vertical = vertical

    def get_aligned(self, word_pattern: WordPattern) -> Optional[WordPattern]:
        if isinstance(word_pattern, WordPatternHorizontal):
            return self.horizontal
        elif isinstance(word_pattern, WordPatternVertical):
            return self.vertical

    def set_aligned(self, word_pattern: WordPattern) -> None:
        if isinstance(word_pattern, WordPatternHorizontal):
            self.horizontal = word_pattern
        elif isinstance(word_pattern, WordPatternVertical):
            self.vertical = word_pattern

    def get_orthogonal(self, word_pattern: WordPattern) -> Optional[WordPattern]:
        if isinstance(word_pattern, WordPatternHorizontal):
            return self.vertical
        elif isinstance(word_pattern, WordPatternVertical):
            return self.horizontal

    def set_orthogonal(self, word_pattern: Optional[WordPattern]) -> None:
        if isinstance(word_pattern, WordPatternHorizontal):
            self.vertical = word_pattern
        elif isinstance(word_pattern, WordPatternVertical):
            self.horizontal = word_pattern
