import json
from crossworlds.grid import Grid


def main():
    for height in range(5, 9):
        for width in range(height, 10):
            for expansion in ['horizontal', 'vertical']:
                new_grids = []
                with open(f'output/grids/{height}x{width}.grids', 'r') as fp:
                    for values_str in fp.read().splitlines():
                        grid = Grid(height, width, Grid.parse_str(values_str))
                        new_grids.extend(grid.find_valid_grids_expansion(expansion))

                new_height = height + (expansion == 'vertical')
                new_width = width + (expansion == 'horizontal')
                with open(f'output/grids/{new_height}x{new_width}.grids', 'w') as fp:
                    fp.write(Grid.to_str(new_grids))
                with open(f'output/grids/sizes.json', 'r') as fp:
                    size_dict = json.load(fp)
                size_dict[f'{new_height}x{new_width}'] = len(new_grids)
                with open(f'output/grids/sizes.json', 'w') as fp:
                    json.dump(size_dict, fp, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
