from search import get_full_grids
from lookup import init_vocab

found_grids = get_full_grids(4, 4, init_vocab())
output_str = ''
for word_patterns, grid_str in found_grids:
    output_str += grid_str
    for word_pattern, word in word_patterns.items():
        output_str += f'{str(word_pattern)}: {word} | '
    output_str += '\n---------\n'
print(len(found_grids))
with open('test/profile/output.txt', 'w') as fp:
    fp.write(output_str)
