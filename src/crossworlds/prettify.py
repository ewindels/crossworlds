from crossworlds.grid import Grid


def main():
    height = 8
    width = 8
    output_str = ''
    with open(f'output/{height}x{width}.grids', 'r') as fp:
        for values_str in fp.read().splitlines():
            grid = Grid(height, width, Grid.parse_str(values_str))
            output_str += values_str + '\n'
            output_str += grid.prettify() + '\n\n'
    with open('output/pretty.txt', 'w') as fp:
        fp.write(output_str)


if __name__ == '__main__':
    main()
