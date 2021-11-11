import json
from crossworlds.lookup import init_vocab
from crossworlds.search import get_full_grids


def main():
    height = 3
    width = 4
    definitions = {}
    vocab = init_vocab()
    found_grids = get_full_grids(height, width, definitions, vocab)
    print(f'Found {len(found_grids)} grids')
    found_grids_str = ''
    for word_dict, pretty_grid in found_grids:
        found_grids_str += pretty_grid
        found_grids_str += str(word_dict) + '\n'
    with open(f'output/word_grids/{height}x{width}.wordgrids', 'w', encoding='utf-8') as fp:
        fp.write(found_grids_str)
    with open(f'output/word_grids/sizes.json', 'r') as fp:
        size_dict = json.load(fp)
    size_dict[f'{height}x{width}'] = len(found_grids)
    with open(f'output/word_grids/sizes.json', 'w') as fp:
        json.dump(size_dict, fp, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
