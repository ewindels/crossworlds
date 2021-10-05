from itertools import chain
from collections import defaultdict
from typing import Optional, NamedTuple

class Coor(NamedTuple):
    row: int
    col: int

class WordStart(NamedTuple):
    coor: Coor
    direction: str

DEF_TOKEN = '[def]'

class Grid:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.words_dict = {}
        self.word_start_dict = defaultdict(list)
        self.letters_count = defaultdict(int)
        self.grid = self.__init_grid()
        self.word_starts = self.__init_word_starts()
        self.word_grid_impact = {}
        self.word_settable_impact = {}

    def __set_square(self, coor: Coor, content: str) -> None:
        row_n, col_n = coor
        self.grid[row_n][col_n] = content

    def __init_grid(self) -> list[list[str]]:
        self.grid = [['' for _ in range(self.width)] for _ in range(self.height)]
        for col_n in range(0, self.width, 2):
            self.__set_square(Coor(0, col_n), DEF_TOKEN)
        for row_n in range(0, self.height, 2):
            self.__set_square(Coor(row_n, 0), DEF_TOKEN)
        return self.grid

    def __init_word_starts(self) -> set[WordStart]:
        word_starts = set()
        for col_i in range(1, self.width):
            if col_i % 2:
                row_n = 0
            else:
                row_n = 1
            word_start = WordStart(Coor(row_n, col_i), 'V')
            word_starts.add(word_start)
            for row_i in range(row_n, self.height):
                self.word_start_dict[Coor(row_i, col_i)].append(word_start)
        for row_i in range(1, self.height):
            if row_i % 2:
                col_n = 0
            else:
                col_n = 1
            word_start =  WordStart(Coor(row_i, col_n), 'H')
            word_starts.add(word_start)
            for col_i in range(col_n, self.width):
                self.word_start_dict[Coor(row_i, col_i)].append(word_start)
        return word_starts

    @property
    def best_word_start(self) -> WordStart:
        return max(self.word_starts, key=lambda word_start: (self.letters_count[word_start], -word_start.coor.col, -word_start.coor.row))

    @property
    def is_full(self) -> bool:
        return all(square != '' for square in chain.from_iterable(self.grid))

    @staticmethod
    def normalize(letter: str) -> str:
        return letter.upper()

    def get_col(self, col_n: int) -> Optional[list[str]]:
        if 0 <= col_n < self.width:
            return [self.grid[row_n][col_n] for row_n in range(self.height)]

    def get_row(self, row_n: int) -> Optional[list[str]]:
        if 0 <= row_n < self.height:
            return self.grid[row_n]

    def get_square(self, row_n: int, col_n: int):
        if (0 <= row_n < self.height) and (0 <= col_n < self.width):
            return self.grid[row_n][col_n]

    def check_impact_and_update_grid(self, coor: Coor, coor_start: Coor, content: str) -> bool:
        if coor not in self.word_grid_impact:
            self.word_grid_impact[coor] = coor_start
            self.__set_square(coor, content)
            return True
        return False

    def check_impact_and_update_settable(self, word_start: WordStart, coor_start: Coor) -> bool:
        if word_start not in self.word_settable_impact:
            self.word_settable_impact[word_start] = coor_start
            self.word_starts.add(word_start)
            return True
        return False

    def __set_word_vertical(self, coor_start: Coor, word: str) -> None:
        for row_i, letter in enumerate(word, coor_start.row):
            coor_letter = Coor(row_i, coor_start.col)
            if self.check_impact_and_update_grid(coor_letter, coor_start, self.normalize(letter)):
                for word_start in self.word_start_dict[coor_letter]:
                    self.letters_count[word_start] += 1
        if coor_start.row + len(word) + 1 < self.height:
            self.check_impact_and_update_grid(Coor(coor_start.row + len(word) + 1, coor_start.col), coor_start, '[def]')
            if coor_start.row + len(word) + 3 < self.height:
                word_start = WordStart(Coor(coor_start.row + len(word) + 2, coor_start.col), 'V')
                self.check_impact_and_update_settable(word_start, coor_start)
            if coor_start.col + 2 < self.width:
                word_start = WordStart(Coor(coor_start.row + len(word) + 1, coor_start.col + 1), 'H')
                self.check_impact_and_update_settable(word_start, coor_start)

    def __set_word_horizontal(self, coor_start: Coor, word: str) -> None:
        for col_i, letter in enumerate(word, coor_start.col):
            coor_letter = Coor(coor_start.row, col_i)
            if self.check_impact_and_update_grid(coor_letter, coor_start, self.normalize(letter)):
                for word_start in self.word_start_dict[coor_letter]:
                    self.letters_count[word_start] += 1
        if coor_start.col + len(word) + 1 < self.width:
            self.check_impact_and_update_grid(Coor(coor_start.row, coor_start.col + len(word) + 1), coor_start, '[def]')
            if coor_start.col + len(word) + 3 < self.width:
                word_start = WordStart(Coor(coor_start.row, coor_start.col + len(word) + 2), 'H')
                self.check_impact_and_update_settable(word_start, coor_start)
            if coor_start.row + 2 < self.height:
                word_start = WordStart(Coor(coor_start.row + 1, coor_start.col + len(word) + 1), 'V')
                self.check_impact_and_update_settable(word_start, coor_start)

    def set_word(self, word_start: WordStart, word: str) -> None:
        self.words_dict[word_start] = word
        self.word_starts.discard(word_start)
        if word_start.direction == 'V':
            self.__set_word_vertical(word_start.coor, word)
        elif word_start.direction == 'H':
            self.__set_word_horizontal(word_start.coor, word)

    def check_and_remove_letter(self, letter_coor: Coor, coor_start: Coor) -> None:
        if self.word_grid_impact[letter_coor] == coor_start:
            self.__set_square(letter_coor, '')
            self.word_grid_impact.pop(letter_coor)
            for word_start in self.word_start_dict[letter_coor]:
                self.letters_count[word_start] -= 1

    def __remove_word_vertical(self, coor_start: Coor, word: str) -> None:
        for row_i, _ in enumerate(word, coor_start.row):
            self.check_and_remove_letter(Coor(row_i, coor_start.col), coor_start)
        if coor_start.row + len(word) + 1 < self.height:
            def_coor = Coor(coor_start.row + len(word) + 1, coor_start.col)
            if self.word_grid_impact[def_coor] == coor_start:
                self.__set_square(def_coor, '')
            if coor_start.row + len(word) + 3 < self.height:
                word_start = WordStart(Coor(coor_start.row + len(word) + 2, coor_start.col), 'V')
                if self.word_settable_impact[word_start] == coor_start:
                    self.word_starts.discard(word_start)
            if coor_start.col + 2 < self.width:
                word_start = WordStart(Coor(coor_start.row + len(word) + 1, coor_start.col + 1), 'V')
                if self.word_settable_impact[word_start] == coor_start:
                    self.word_starts.discard(word_start)

    def __remove_word_horizontal(self, coor_start: Coor, word: str) -> None:
        for col_i, _ in enumerate(word, coor_start.col):
            self.check_and_remove_letter(Coor(coor_start.row, col_i), coor_start)
        if coor_start.col + len(word) + 1 < self.width:
            def_coor = Coor(coor_start.row, coor_start.col + len(word) + 1)
            if self.word_grid_impact[def_coor] == coor_start:
                self.__set_square(def_coor, '')
            if coor_start.col + len(word) + 3 < self.width:
                word_start = WordStart(Coor(coor_start.row, coor_start.col + len(word) + 2), 'H')
                if self.word_settable_impact[word_start] == coor_start:
                    self.word_starts.discard(word_start)
            if coor_start.row + 2 < self.height:
                word_start = WordStart(Coor(coor_start.row + 1, coor_start.col + len(word) + 1), 'V')
                if self.word_settable_impact[word_start] == coor_start:
                    self.word_starts.discard(word_start)

    def remove_word(self, word_start: WordStart, word: str):
        self.words_dict.pop(word_start)
        self.word_starts.add(word_start)
        if word_start.direction == 'V':
            self.__remove_word_vertical(word_start.coor, word)
        elif word_start.direction == 'H':
            self.__remove_word_horizontal(word_start.coor, word)

    def __check_word_vertical(self, coor_start: Coor, word: str):
        if self.get_square(coor_start.row + len(word) - 1, coor_start.col) is None:
            return False
        elif (
            self.get_square(coor_start.row + len(word), coor_start.col) in ('', '[def]')
            and (
                self.get_square(coor_start.row + len(word), coor_start.col - 2) in (None, '[def]')
                or self.get_square(coor_start.row + len(word) + 2, coor_start.col) == '[def]'
                or self.get_square(coor_start.row + len(word), coor_start.col + 2) == '[def]'
            )
        ):
            return False
        for row_i, letter in enumerate(word, coor_start.row):
            square = self.get_square(row_i, coor_start.col)
            if not (square == '' or square == self.normalize(letter)):
                return False
        return True
    
    def __check_word_horizontal(self, coor_start: Coor, word: str):
        if self.get_square(coor_start.row, coor_start.col + len(word) - 1) is None:
            return False
        elif (
            self.get_square(coor_start.row, coor_start.col + len(word)) in ('', '[def]')
            and (
                self.get_square(coor_start.row - 2, coor_start.col + len(word)) in (None, '[def]')
                or self.get_square(coor_start.row, coor_start.col + len(word) + 2) == '[def]'
                or self.get_square(coor_start.row + 2, coor_start.col + len(word)) == '[def]'
            )
        ):
            return False
        for col_i, letter in enumerate(word, coor_start.col):
            square = self.get_square(coor_start.row, col_i)
            if not (square == '' or square == self.normalize(letter)):
                return False
        return True

    def check_word(self, word_start: WordStart, word):
        if word_start.direction == 'V':
            return self.__check_word_vertical(word_start.coor, word)
        elif word_start.direction == 'H':
            return self.__check_word_horizontal(word_start.coor, word)

    def print(self):
        grid_str = '┌' + ('───┬───' * (self.width - 1)) + '┐\n'
        for row_n, row in enumerate(self.grid):
            for content in row:
                if content == '[def]':
                    grid_str += '│ ■ '
                elif content == '':
                    grid_str += '│   '
                else:
                    grid_str += f'│ {content} '
            grid_str += '│\n'
            if row_n < self.height - 1:
                grid_str += '├' + ('───┼───' * (self.width - 1)) + '┤\n'
            else:
                grid_str += '└' + ('───┴───' * (self.width - 1)) + '┘\n'
        print(grid_str)