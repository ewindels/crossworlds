from itertools import chain
from unidecode import unidecode
from collections import defaultdict
from typing import Optional, NamedTuple


DEF_TOKEN = '[def]'


class Coor(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Coor(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        return Coor(self.row - other.row, self.col - other.col)

    def __mul__(self, other):
        return Coor(self.row * other, self.col * other)


class WordStart(NamedTuple):
    coor: Coor
    direction: str


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

    def __set_content(self, coor: Coor, content: str) -> None:
        row_n, col_n = coor
        self.grid[row_n][col_n] = content

    def __init_grid(self) -> list[list[str]]:
        self.grid = [['' for _ in range(self.width)] for _ in range(self.height)]
        for col_n in range(0, self.width, 2):
            self.__set_content(Coor(0, col_n), DEF_TOKEN)
        for row_n in range(0, self.height, 2):
            self.__set_content(Coor(row_n, 0), DEF_TOKEN)
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
        return all(content != '' for content in chain.from_iterable(self.grid))

    @staticmethod
    def normalize(letter: str) -> str:
        return unidecode(letter).upper()

    def get_col(self, col_n: int) -> Optional[list[str]]:
        if 0 <= col_n < self.width:
            return [self.grid[row_n][col_n] for row_n in range(self.height)]

    def get_row(self, row_n: int) -> Optional[list[str]]:
        if 0 <= row_n < self.height:
            return self.grid[row_n]

    def get_content(self, coor: Coor):
        if (0 <= coor.row < self.height) and (0 <= coor.col < self.width):
            return self.grid[coor.row][coor.col]

    def __check_impact_and_update_grid(self, coor_start: Coor, coor: Coor, content: str) -> None:
        if coor not in self.word_grid_impact:
            self.word_grid_impact[coor] = coor_start
            self.__set_content(coor, content)
            for word_start in self.word_start_dict.get(coor, []):
                self.letters_count[word_start] += 1

    def __check_impact_and_update_settable(self, coor_start: Coor, word_start: WordStart) -> None:
        if word_start not in self.word_settable_impact:
            self.word_settable_impact[word_start] = coor_start
            self.word_starts.add(word_start)

    def __set_def_and_word_starts(self, coor_start: Coor, coor_end: Coor) -> None:
        self.__check_impact_and_update_grid(coor_start, coor_end, DEF_TOKEN)
        if coor_end.row + 2 < self.height:
            word_start = WordStart(coor_end + Coor(1, 0), 'V')
            self.__check_impact_and_update_settable(coor_start, word_start)
        if coor_end.col + 2 < self.width:
            word_start = WordStart(coor_end + Coor(0, 1), 'H')
            self.__check_impact_and_update_settable(coor_start, word_start)

    def __set_word_vertical(self, coor_start: Coor, word: str) -> None:
        for row_i, letter in enumerate(word, coor_start.row):
            coor_letter = Coor(row_i, coor_start.col)
            self.__check_impact_and_update_grid(coor_start, coor_letter, self.normalize(letter))
        coor_end = coor_start + Coor(len(word), 0)
        if coor_end.row < self.height:
            self.__set_def_and_word_starts(coor_start, coor_end)

    def __set_word_horizontal(self, coor_start: Coor, word: str) -> None:
        for col_i, letter in enumerate(word, coor_start.col):
            coor_letter = Coor(coor_start.row, col_i)
            self.__check_impact_and_update_grid(coor_start, coor_letter, self.normalize(letter))
        coor_end = coor_start + Coor(0, len(word))
        if coor_end.col < self.width:
            self.__set_def_and_word_starts(coor_start, coor_end)

    def set_word(self, word_start: WordStart, word: str) -> None:
        self.words_dict[word_start] = word
        self.word_starts.discard(word_start)
        if word_start.direction == 'V':
            self.__set_word_vertical(word_start.coor, word)
        elif word_start.direction == 'H':
            self.__set_word_horizontal(word_start.coor, word)

    def __check_and_remove_letter(self, coor_start: Coor, coor: Coor) -> None:
        if self.word_grid_impact.get(coor) == coor_start:
            self.__set_content(coor, '')
            self.word_grid_impact.pop(coor)
            for word_start in self.word_start_dict.get(coor, []):
                self.letters_count[word_start] -= 1

    def __remove_def_and_word_starts(self, coor_start: Coor, coor_end: Coor) -> None:
        self.__check_and_remove_letter(coor_start, coor_end)
        if coor_end.row + 2 < self.height:
            word_start = WordStart(coor_end + Coor(1, 0), 'V')
            if self.word_settable_impact[word_start] == coor_start:
                self.word_starts.discard(word_start)
        if coor_end.col + 2 < self.width:
            word_start = WordStart(coor_end + Coor(0, 1), 'H')
            if self.word_settable_impact[word_start] == coor_start:
                self.word_starts.discard(word_start)

    def remove_word(self, word_start: WordStart, word: str):
        if word_start.direction == 'V':
            coor_direction = Coor(1, 0)
        else:
            coor_direction = Coor(0, 1)
        self.words_dict.pop(word_start)
        self.word_starts.add(word_start)
        for offset in range(len(word)):
            coor_offset = coor_direction * offset
            self.__check_and_remove_letter(word_start.coor, word_start.coor + coor_offset)
        coor_offset = coor_direction * len(word)
        coor_end = word_start.coor + coor_offset
        if self.get_content(coor_end):
            self.__remove_def_and_word_starts(word_start.coor, coor_end)

    def __check_word_vertical(self, coor_start: Coor, word: str):
        coor_end = coor_start + Coor(len(word), 0)
        if self.get_content(coor_end - Coor(1, 0)) is None:
            return False
        elif not self.get_content(coor_end) in ('', DEF_TOKEN, None):
            return False
        elif (
            self.get_content(coor_end) in ('', DEF_TOKEN)
            and (
                self.get_content(coor_end - Coor(2, 0)) in (None, DEF_TOKEN)
                or self.get_content(coor_end + Coor(2, 0)) == DEF_TOKEN
                or self.get_content(coor_end + Coor(0, 2)) == DEF_TOKEN
            )
        ):
            return False
        for row_i, letter in enumerate(word, coor_start.row):
            content = self.get_content(Coor(row_i, coor_start.col))
            if not (content == '' or content == self.normalize(letter)):
                return False
        return True
    
    def __check_word_horizontal(self, coor_start: Coor, word: str):
        coor_end = coor_start + Coor(0, len(word))
        if self.get_content(coor_end - Coor(0, 1)) is None:
            return False
        elif not self.get_content(coor_end) in ('', DEF_TOKEN, None):
            return False
        elif (
            self.get_content(Coor(coor_start.row, coor_start.col + len(word))) in ('', DEF_TOKEN)
            and (
                self.get_content(coor_end - Coor(0, 2)) in (None, DEF_TOKEN)
                or self.get_content(coor_end + Coor(0, 2)) == DEF_TOKEN
                or self.get_content(coor_end + Coor(2, 0)) == DEF_TOKEN
            )
        ):
            return False
        for col_i, letter in enumerate(word, coor_start.col):
            content = self.get_content(Coor(coor_start.row, col_i))
            if not (content == '' or content == self.normalize(letter)):
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
                if content == DEF_TOKEN:
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