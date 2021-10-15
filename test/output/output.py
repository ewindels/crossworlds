from search import get_full_grids
from lookup import init_vocab

vocab = init_vocab()
for width, height in [(2, 2), (3, 3), (4, 4)]:
    found_grids = get_full_grids(width, height, vocab)
    output_str = ''
    for word_patterns, grid_str in found_grids:
        output_str += grid_str
        for word_pattern, word in word_patterns.items():
            output_str += f'{str(word_pattern)}: {word} | '
        output_str += '\n---------\n'
    print(f'{width}x{height}: {len(found_grids)} grids')
    with open(f'test/output/output_{width}x{height}.txt', 'w') as fp:
        fp.write(output_str)
