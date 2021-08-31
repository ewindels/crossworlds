# python -m cProfile -o test\profile_output test\profile.py
# python -m pstats test\profile_output
from crosswords_coop import parse

parse.parse('crossword_0.jpg')
