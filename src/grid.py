Coor = tuple[int, int]


class Grid:
    def __init__(self, height: int, width: int):
        self.height, self.width = height, width
        self.values = set()
        self._init_grid()

    def _init_grid(self) -> None:
        for row in range(0, self.height, 2):
            self.values.add((row, 0))
        for col in range(0, self.width, 2):
            self.values.add((0, col))

    def load_from_string(self, string: str):
        for row, row_val in enumerate(string.splitlines()):
            for col, value in enumerate(row_val):
                if value == '1':
                    self.values.add((row, col))

    def is_switch_valid(self, row: int, col: int):
        if row == 1:
            if (0, col) not in self.values:
                return False
            elif (
                    (1, col - 1) in self.values
                    or (1, col - 2) in self.values
                    or (3, col) in self.values
            ):
                return False
        elif col == 1:
            if (row, 0) not in self.values:
                return False
            elif (
                    (row - 1, 1) in self.values
                    or (row - 2, 1) in self.values
                    or (row, 3) in self.values
            ):
                return False
        else:
            if (
                    (row - 1, col) in self.values
                    or (row, col - 1) in self.values
                    or (row - 2, col) in self.values
                    or (row, col - 2) in self.values
            ):
                return False
        return True

    def expand(self, direction: str) -> None:
        if direction == 'vertical':
            self.height += 1
            if self.height % 2:
                self.values.add((self.height - 1, 0))
        elif direction == 'horizontal':
            self.width += 1
            if self.width % 2:
                self.values.add((0, self.width - 1))

    def switchable_values(self, expansion: str) -> list[Coor]:
        switchable_values = []
        if expansion == 'vertical':
            switchable_values.extend([(self.height - 2, 1),
                                      (self.height - 3, self.width - 1),
                                      (self.height - 3, self.width - 2)])
            switchable_values.extend([(self.height - 1, col) for col in range(2, self.width - 2)])
        elif expansion == 'horizontal':
            switchable_values.extend([(1, self.width - 2),
                                      (self.height - 1, self.width - 3),
                                      (self.height - 2, self.width - 3)])
            switchable_values.extend([(row, self.width - 1) for row in range(2, self.height - 2)])
        switchable_values.sort(key=lambda x: x[0] + x[1], reverse=True)
        return switchable_values

    def find_valid_grids(self, switchable_values: list[Coor], valid_grids: list[str]) -> None:
        if switchable_values:
            row, col = switchable_values.pop()
            self.find_valid_grids(switchable_values, valid_grids)
            if self.is_switch_valid(row, col):
                self.values.add((row, col))
                self.find_valid_grids(switchable_values, valid_grids)
                self.values.remove((row, col))
            switchable_values.append((row, col))
        else:
            valid_grids.append(self.to_string())

    def find_valid_grids_expansion(self, expansion: str) -> list[str]:
        self.expand(expansion)
        switchable_values = self.switchable_values(expansion)
        valid_grids = []
        self.find_valid_grids(switchable_values, valid_grids)
        return valid_grids

    def to_string(self) -> str:
        grid_string = ['0' for _ in range((self.height * (self.width + 1)))]
        for row, col in self.values:
            grid_string[row * (self.width + 1) + col] = '1'
        for row in range(self.height):
            grid_string[row * (self.width + 1) + self.width] = '\n'
        return ''.join(grid_string)
