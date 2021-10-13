# python -m cProfile -o test/profile_output test/profile.py
# python -m pstats test/profile_output
# sort time
# stats 10

from grid import Grid
from search import recursive_search, init_vocab

grid = Grid(3, 3)
found_grids = []
vocab = init_vocab()
recursive_search(vocab, grid, found_grids)
