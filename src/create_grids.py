import json
from grid import Grid


def main():
    for height in range(5, 8):
        for width in range(height, 8):
            for expansion in ['horizontal', 'vertical']:
                new_grids = []
                with open(f'output/{height}x{width}.grids', 'r') as fp:
                    for values_str in fp.read().splitlines():
                        grid = Grid(height, width, Grid.parse_str(values_str))
                        new_grids.extend(grid.find_valid_grids_expansion(expansion))

                new_height = height + (expansion == 'vertical')
                new_width = width + (expansion == 'horizontal')
                with open(f'output/{new_height}x{new_width}.grids', 'w') as fp:
                    fp.write(Grid.to_str(new_grids))
                with open(f'output/sizes.json', 'r') as fp:
                    size_dict = json.load(fp)
                size_dict[f'{new_height}x{new_width}'] = len(new_grids)
                with open(f'output/sizes.json', 'w') as fp:
                    json.dump(size_dict, fp, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()