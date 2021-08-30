import os
import pytest
from crosswords_coop import parse

@pytest.mark.parametrize("file", os.listdir(os.path.join('data', 'crosswords')))

def test_parsefile(file):
    parse.parse(file)
