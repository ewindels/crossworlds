import os
import json
import pytest
from crosswords_coop import parse

with open(os.path.join('data', 'content.json'), 'r') as fp:
    content_dict = json.load(fp)
    grids_with_size = [grid for grid in content_dict if 'size' in content_dict[grid]]
    grids_with_text_cells = [grid for grid in content_dict if 'text' in content_dict[grid]]

@pytest.mark.parametrize("grid_file", os.listdir(os.path.join('data', 'crosswords')))
def test_parse(grid_file):
    grid_img_dict = parse.parse(grid_file)
    assert grid_img_dict

@pytest.mark.parametrize("grid_file", grids_with_size)
def test_check_size(grid_file):
    grid_img_dict = parse.parse(grid_file)
    length, width = content_dict[grid_file]['size']
    predicted_length = max(l for l, w in grid_img_dict) + 1
    predicted_width = max(w for l, w in grid_img_dict) + 1
    assert length == predicted_length
    assert width == predicted_width
