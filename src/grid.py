from collections import defaultdict
from typing import Optional


class Grid:
    def __init__(self, size):
        self.width, self.height = size
        self.words_dict = {}
        self.word_start_dict = defaultdict(list)
        self.letters_count = defaultdict(int)
        self.grid = self.__init_grid()
        self.settable_squares = self.__init_settable()

    def __init_grid(self) -> list[list[str]]:
        grid = [['' for _ in range(self.width)] for _ in range(self.height)]
        for col_n in range(0, self.width, 2):
            grid[0][col_n] = '[def]'
        for row_n in range(0, self.height, 2):
            grid[row_n][0] = '[def]'
        return grid

    def __init_settable(self) -> set:
        settable_squares = set()
        for col_i in range(1, self.width):
            if col_i % 2:
                row_n = 0
            else:
                row_n = 1
            settable_squares.add((row_n, col_i, 'V'))
            for row_i in range(row_n, self.height):
                self.word_start_dict[(row_i, col_i)].append((row_n, col_i, 'V'))
        for row_i in range(1, self.height):
            if row_i % 2:
                col_n = 0
            else:
                col_n = 1
            settable_squares.add((row_i, col_n, 'H'))
            for col_i in range(col_n, self.width):
                self.word_start_dict[(row_i, col_i)].append((row_i, col_n, 'H'))
        return settable_squares

    @property
    def max_settable_square(self):
        return max(self.settable_squares, key=lambda square: (self.letters_count[square], -square[0], -square[1]))

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

    def __set_word_vertical(self, row_n: int, col_n: int, word: str) -> None:
        for row_i, letter in enumerate(word, row_n):
            self.grid[row_i][col_n] = self.normalize(letter)
            for square_start in self.word_start_dict[(row_i, col_n)]:
                self.letters_count[square_start] += 1
        if row_n + len(word) + 1 < self.height:
            self.grid[row_n + len(word) + 1][col_n] = '[def]'
            if row_n + len(word) + 3 < self.height:
                self.settable_squares.add((row_n + len(word) + 2, col_n, 'V'))
            if col_n + 2 < self.width:
                self.settable_squares.add((row_n + len(word) + 1, col_n + 1, 'H'))

    def __set_word_horizontal(self, row_n: int, col_n: int, word: str) -> None:
        for col_i, letter in enumerate(word, col_n):
            self.grid[row_n][col_i] = self.normalize(letter)
            for square_start in self.word_start_dict[(row_n, col_i)]:
                self.letters_count[square_start] += 1
        if col_n + len(word) + 1 < self.width:
            self.grid[row_n][col_n + len(word) + 1] = '[def]'
            if col_n + len(word) + 3 < self.width:
                self.settable_squares.add((row_n, col_n + len(word) + 2, 'H'))
            if row_n + 2 < self.height:
                self.settable_squares.add((row_n + 1, col_n + len(word) + 1, 'V'))

    def set_word(self, direction: str, *args):
        row_n, col_n, word = args
        start_square = (row_n, col_n, direction)
        self.words_dict[start_square] = word
        self.settable_squares.discard(start_square)
        if direction == 'V':
            self.__set_word_vertical(*args)
        elif direction == 'H':
            self.__set_word_horizontal(*args)

    def __remove_word_vertical(self, row_n: int, col_n: int, word: str) -> None:
        for row_i, _ in enumerate(word, row_n):
            self.grid[row_i][col_n] = ''
            for square_start in self.word_start_dict[(row_i, col_n)]:
                self.letters_count[square_start] -= 1
        if row_n + len(word) + 1 < self.height:
            self.grid[row_n + len(word) + 1][col_n] = ''
            if row_n + len(word) + 3 < self.height:
                self.settable_squares.discard((row_n + len(word) + 2, col_n, 'V'))
            if col_n + 2 < self.width:
                self.settable_squares.discard((row_n + len(word) + 1, col_n + 1, 'H'))

    def __remove_word_horizontal(self, row_n: int, col_n: int, word: str) -> None:
        for col_i, _ in enumerate(word, col_n):
            self.grid[row_n][col_i] = ''
            for square_start in self.word_start_dict[(row_n, col_i)]:
                self.letters_count[square_start] -= 1
        if col_n + len(word) + 1 < self.width:
            self.grid[row_n][col_n + len(word) + 1] = ''
            if col_n + len(word) + 3 < self.width:
                self.settable_squares.discard((row_n, col_n + len(word) + 2, 'H'))
            if row_n + 2 < self.height:
                self.settable_squares.discard((row_n + 1, col_n + len(word) + 1, 'V'))

    #only remove letter if only belonging word is the one we're erasing
    def remove_word(self, direction: str, *args):
        row_n, col_n, _ = args
        start_square = (row_n, col_n, direction)
        self.words_dict.pop(start_square)
        self.settable_squares.add(start_square)
        if direction == 'V':
            self.__remove_word_vertical(*args)
        elif direction == 'H':
            self.__remove_word_horizontal(*args)

    def __check_word_vertical(self, row_n, col_n, word):
        if self.get_square(row_n + len(word) - 1, col_n) is None:
            return False
        elif (
            self.get_square(row_n + len(word), col_n) in ('', '[def]')
            and (
                self.get_square(row_n + len(word), col_n - 2) in (None, '[def]')
                or self.get_square(row_n + len(word) + 2, col_n) == '[def]'
                or self.get_square(row_n + len(word), col_n + 2) == '[def]'
            )
        ):
            return False
        for row_i, letter in enumerate(word, row_n):
            square = self.get_square(row_i, col_n)
            if not (square == '' or square == self.normalize(letter)):
                return False
        return True
    
    def __check_word_horizontal(self, row_n, col_n, word):
        if self.get_square(row_n, col_n + len(word) - 1) is None:
            return False
        elif (
            self.get_square(row_n, col_n + len(word)) in ('', '[def]')
            and (
                self.get_square(row_n - 2, col_n + len(word)) in (None, '[def]')
                or self.get_square(row_n, col_n + len(word) + 2) == '[def]'
                or self.get_square(row_n + 2, col_n + len(word)) == '[def]'
            )
        ):
            return False
        for col_i, letter in enumerate(word, col_n):
            square = self.get_square(row_n, col_i)
            if not (square == '' or square == self.normalize(letter)):
                return False
        return True

    def check_word(self, direction, *args):
        if direction == 'V':
            return self.__check_word_vertical(*args)
        elif direction == 'H':
            return self.__check_word_horizontal(*args)

    def print(self):
        grid_str = '┌' + ('───┬───' * (self.width - 1)) + '┐\n'
        for row_n, row in enumerate(self.grid):
            for square in row:
                if square == '[def]':
                    grid_str += '│ ■ '
                elif square == '':
                    grid_str += '│   '
                else:
                    grid_str += f'│ {square} '
            grid_str += '│\n'
            if row_n < self.height - 1:
                grid_str += '├' + ('───┼───' * (self.width - 1)) + '┤\n'
            else:
                grid_str += '└' + ('───┴───' * (self.width - 1)) + '┘\n'
        print(grid_str)