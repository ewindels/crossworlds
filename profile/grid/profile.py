# python -m cProfile -o test/profile_output test/profile.py
# python -m pstats test/profile_output
# sort time
# stats 10

from grid import Grid


def main():
    height = 7
    width = 8
    expansion = 'horizontal'
    new_grids = []
    with open(f'output/{height}x{width}.grids', 'r') as fp:
        for grid_string in fp.read().split('-\n'):
            grid = Grid(height, width)
            grid.load_from_string(grid_string)
            new_grids.extend(grid.find_valid_grids_expansion(expansion))


if __name__ == '__main__':
    main()
