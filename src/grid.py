Coor = tuple[int, int]


class Grid:
    def __init__(self, height: int, width: int, values: set):
        self.height, self.width = height, width
        self.values = values

    def is_switch_valid(self, row: int, col: int):
        if row == 1:
            if col % 2:
                return False
            elif (
                    (1, col - 2) in self.values
                    or (3, col) in self.values
            ):
                return False
        elif col == 1:
            if row % 2:
                return False
            elif (
                    (row - 2, 1) in self.values
                    or (row, 3) in self.values
            ):
                return False
        else:
            if (
                    (row - 1, col) in self.values
                    or (row - 2, col) in self.values
                    or (row, col - 1) in self.values
                    or (row, col - 2) in self.values
            ):
                return False
        return True

    def expand(self, direction: str) -> list[Coor]:
        if direction == 'vertical':
            self.height += 1
        elif direction == 'horizontal':
            self.width += 1
        return self.get_switchable_values(direction)

    def get_switchable_values(self, direction: str) -> list[Coor]:
        switchable_values = []
        if direction == 'vertical':
            switchable_values.extend([(self.height - 1, col) for col in range(self.width - 3, 1, -1)])
            switchable_values.extend([(self.height - 3, self.width - 1),
                                      (self.height - 3, self.width - 2)])
            if self.height % 2 == 0:
                switchable_values.append((self.height - 2, 1))
        elif direction == 'horizontal':
            switchable_values.extend([(row, self.width - 1) for row in range(self.height - 3, 1, -1)])
            switchable_values.extend([(self.height - 1, self.width - 3),
                                      (self.height - 2, self.width - 3)])
            if self.width % 2 == 0:
                switchable_values.append((1, self.width - 2))
        return switchable_values

    def find_valid_grids(self, switchable_values: list[Coor], valid_grids: list[set[Coor]]) -> None:
        if switchable_values:
            row, col = switchable_values.pop()
            self.find_valid_grids(switchable_values, valid_grids)
            if self.is_switch_valid(row, col):
                self.values.add((row, col))
                self.find_valid_grids(switchable_values, valid_grids)
                self.values.remove((row, col))
            switchable_values.append((row, col))
        else:
            valid_grids.append(self.values.copy())

    def find_valid_grids_expansion(self, direction: str) -> list[set[Coor]]:
        switchable_values = self.expand(direction)
        valid_grids = []
        self.find_valid_grids(switchable_values, valid_grids)
        return valid_grids

    @staticmethod
    def parse_str(string: str) -> set[Coor]:
        values = set()
        if string:
            for coor in string.split('|'):
                row, col = map(int, coor.split(','))
                values.add((row, col))
        return values

    @staticmethod
    def to_str(values_list: list[set[Coor]]):
        output = '\n'.join('|'.join(','.join(map(str, coor)) for coor in values) for values in values_list)
        return output

    def prettify(self) -> str:
        pretty_list = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for row, col in self.values:
            pretty_list[row][col] = 'X'
        for row in range(0, self.height, 2):
            pretty_list[row][0] = 'X'
        for col in range(0, self.width, 2):
            pretty_list[0][col] = 'X'
        pretty_str = '\n'.join(''.join(row) for row in pretty_list)
        return pretty_str
