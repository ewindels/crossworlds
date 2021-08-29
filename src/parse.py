import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


def load_img(file: str) -> np.array:
    file_path = os.path.join('data', 'crosswords', file)
    img = cv2.imread(file_path)
    return img
