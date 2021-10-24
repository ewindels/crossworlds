# python -m cProfile -o test/profile_output test/profile.py
# python -m pstats test/profile_output
# sort time
# stats 10

from grid import Grid


def main():
    for height in range(4, 8):
        for width in range(4, 8):
            for expansion in ['horizontal', 'vertical']:
                new_grids = []
                with open(f'output/{height}x{width}.grids', 'r') as fp:
                    for grid_string in fp.read().split('-\n'):
                        grid = Grid(height, width)
                        grid.load_from_string(grid_string)
                        new_grids.extend(grid.find_valid_grids_expansion(expansion))


if __name__ == '__main__':
    main()
