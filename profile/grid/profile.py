# python -m cProfile -o test/profile_output test/profile.py
# python -m pstats test/profile_output
# sort time
# stats 10

from crossworlds.grid import Grid


def main():
    height = 9
    width = 9
    expansion = 'horizontal'
    new_grids = []
    with open(f'output/grids/{height}x{width}.grids', 'r') as fp:
        for values_str in fp.read().splitlines():
            grid = Grid(height, width, Grid.parse_str(values_str))
            new_grids.extend(grid.find_valid_grids_expansion(expansion))


if __name__ == '__main__':
    main()
