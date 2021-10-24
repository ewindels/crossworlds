from grid import Grid


def main():
    for height in range(8, 9):
        for width in range(7, 8):
            for expansion in ['horizontal']:
                new_grids = []
                with open(f'output/{height}x{width}.grids', 'r') as fp:
                    for grid_string in fp.read().split('-\n'):
                        grid = Grid(height, width)
                        grid.load_from_string(grid_string)
                        new_grids.extend(grid.find_valid_grids_expansion(expansion))

                new_height = height + (expansion == 'vertical')
                new_width = width + (expansion == 'horizontal')
                with open(f'output/{new_height}x{new_width}.grids', 'w') as fp:
                    fp.write('-\n'.join(new_grids))


if __name__ == '__main__':
    main()