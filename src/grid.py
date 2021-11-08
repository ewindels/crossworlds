from __future__ import annotations
from abc import ABC, abstractmethod

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

    def get_content(self,
                    row: int,
                    col: int) -> Optional[str]:
        return self.letters[(row, col)]


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

    @abstractmethod
    def get_coor(self,
                 index: int,
                 orthogonal_offset: int = 0) -> tuple[int, int]:
        pass

    def __eq__(self, other: WordPattern) -> bool:
        return self.row == other.row and self.col == other.col and self.length == other.length

    def __hash__(self) -> str:
        return hash((self.row, self.col, self.length))

    def get_content(self, index: int) -> Optional[str]:
        return self.grid.get_content(*self.get_coor(index))


class WordPatternHorizontal(WordPattern):
    def __repr__(self) -> str:
        return f'WordPatternH({self.row}, {self.col} | {self.length})'

    def __str__(self) -> str:
        return f'H({self.row}, {self.col} | {self.length})'

    def get_coor(self,
                 index: int,
                 orthogonal_offset: int = 0) -> tuple[int, int]:
        return self.row + orthogonal_offset, self.col + index


class WordPatternVertical(WordPattern):
    def __repr__(self) -> str:
        return f'WordPatternV({self.row}, {self.col} | {self.length})'

    def __str__(self) -> str:
        return f'V({self.row}, {self.col} | {self.length})'

    def get_coor(self,
                 index: int,
                 orthogonal_offset: int = 0) -> tuple[int, int]:
        return self.row + index, self.col + orthogonal_offset
