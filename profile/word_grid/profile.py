from crossworlds.lookup import init_vocab
from crossworlds.search import get_full_grids


def main():
    height = 4
    width = 4
    definitions = {}
    vocab = init_vocab()
    found_grids = get_full_grids(height, width, definitions, vocab)
    found_grids_str = ''
    for word_dict, pretty_grid in found_grids:
        found_grids_str += pretty_grid


if __name__ == '__main__':
    main()
