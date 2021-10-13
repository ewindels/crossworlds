# python -m cProfile -o test/profile_output test/profile.py
# python -m pstats test/profile_output
# sort time
# stats 10

from search import get_full_grids
from lookup import init_vocab

found_grids = get_full_grids(4, 4, init_vocab())
