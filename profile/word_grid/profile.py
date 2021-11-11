from crossworlds.lookup import init_vocab
from crossworlds.search import get_full_grids


def main():
    height = 5
    width = 5
    definitions = {}
    vocab = init_vocab()
    for _ in get_full_grids(height, width, definitions, vocab):
        pass


if __name__ == '__main__':
    main()
