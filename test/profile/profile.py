# python -m cProfile -o test/profile_output test/profile.py
# python -m pstats test/profile_output
# sort time
# stats 10

from search import get_full_grids
from lookup import init_vocab

vocab = init_vocab()
sub_vocab = {}
limit = 13_000
for i, word in enumerate(sorted(vocab)):
    sub_vocab[word] = set()
    if i == limit:
        break
print(f'{limit} words in sub vocab')
found_grids = get_full_grids(4, 4, sub_vocab)
