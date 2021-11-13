import json
from crossworlds.lookup import init_vocab
from crossworlds.search import get_full_grids


def main():
    vocab = init_vocab()
    for height, width in [(7, 7)]:
        print(f'{height}x{width}')
        definitions = set()
        found_grids = list(get_full_grids(height, width, definitions, vocab))
        print(f'Found {len(found_grids)} grids')

        found_grids_str_list = []
        for word_dicts in found_grids:
            found_grids_str_list.append('|'.join(f'{pattern[0]},{pattern[1]},{pattern[2]}:{word_dicts[pattern]}' for pattern in sorted(word_dicts)))
        output_str = '\n'.join(sorted(found_grids_str_list))
        with open(f'output/word_grids/{height}x{width}.wordgrids', 'w', encoding='utf-8') as fp:
            fp.write(output_str)
        with open('output/word_grids/sizes.json', 'r', encoding='utf-8') as fp:
            size_dict = json.load(fp)
        size_dict[f'{height}x{width}'] = len(found_grids)
        with open('output/word_grids/sizes.json', 'w', encoding='utf-8') as fp:
            json.dump(size_dict, fp, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
