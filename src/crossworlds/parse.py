"""
from collections import defaultdict
import os
from typing import Union
from cv2 import cv2
import numpy as np

Coordinates = tuple[Union[float, int], Union[float, int]]

def load_img(file: str) -> np.ndarray:
    file_path = os.path.join('data', 'crosswords', file)
    img_arr = cv2.imread(file_path)
    return img_arr


def preprocess_img(img_arr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (5, 5))
    edges = cv2.Canny(blur, 0, 150)
    kernel_size = (7, 7)
    kernel = np.ones(kernel_size, np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    kernel = np.ones(kernel_size, np.uint8)
    edges = cv2.erode(edges, kernel, iterations=1)
    edges_arr = edges.astype(bool)
    return edges_arr

 
def get_box(contour: np.ndarray) -> np.ndarray:
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = box.astype(int)
    return box


def get_boxes(edges_arr: np.ndarray) -> list[np.ndarray]:
    contours, _ = cv2.findContours((~edges_arr).astype('uint8'), 1, 2)
    boxes = list()
    lower_thresh = 1000
    for contour in contours:
        if lower_thresh < cv2.contourArea(contour) < 10000:
            box = get_box(contour)
            if cv2.contourArea(box) < 10000:
                boxes.append(box)
    return boxes


def distance(pixel_1: Coordinates, pixel_2: Coordinates) -> float:
    return ((pixel_1[0] - pixel_2[0]) ** 2 + (pixel_1[1] - pixel_2[1]) ** 2) ** 0.5


def l_max_distance(pixel_1: Coordinates, pixel_2: Coordinates) -> float:
    return max(abs(pixel_1[0] - pixel_2[0]), abs(pixel_1[1] - pixel_2[1]))


def l_min_distance(pixel_1: Coordinates, pixel_2: Coordinates) -> float:
    return min(abs(pixel_1[0] - pixel_2[0]), abs(pixel_1[1] - pixel_2[1]))


def distance_point_to_line(line_point_1: Coordinates, line_point_2: Coordinates, point: Coordinates) -> float:
    return abs((line_point_2[0] - line_point_1[0]) * (line_point_1[1] - point[1]) - (line_point_1[0] - point[0]) * (line_point_2[1] - line_point_1[1])) / ((line_point_2[0] - line_point_1[0]) ** 2 + (line_point_2[1] - line_point_1[1]) ** 2) ** 0.5


def lines_intersection(l1_p1: Coordinates, l1_p2: Coordinates, l2_p1: Coordinates, l2_p2: Coordinates) -> Coordinates:
    x_num = (l1_p1[1] * l1_p2[0] - l1_p1[0] * l1_p2[1]) * (l2_p1[0] - l2_p2[0]) - (l1_p1[0] - l1_p2[0]) * (l2_p1[1] * l2_p2[0] - l2_p1[0] * l2_p2[1])
    y_num = (l1_p1[1] * l1_p2[0] - l1_p1[0] * l1_p2[1]) * (l2_p1[1] - l2_p2[1]) - (l1_p1[1] - l1_p2[1]) * (l2_p1[1] * l2_p2[0] - l2_p1[0] * l2_p2[1])
    div = (l1_p1[1] - l1_p2[1]) * (l2_p1[0] - l2_p2[0]) - (l1_p1[0] - l1_p2[0]) * (l2_p1[1] - l2_p2[1])
    return x_num / div, y_num / div


def get_clusters(boxes: list[np.ndarray]) -> dict[Coordinates, list[tuple[Coordinates ,int]]]:
    clusters = dict()
    for i, box in enumerate(boxes):
        for pixel in box:
            for cluster_centroid in clusters:
                if l_max_distance(pixel, cluster_centroid) < 10:
                    clusters[cluster_centroid].append((pixel, i))
                    break
            else:
                clusters[tuple(pixel)] = [(pixel, i)]
    return clusters


def get_corners(clusters: dict[Coordinates, list[tuple[Coordinates, int]]]) -> list[Coordinates]:
    corners = list()
    kept_shape_ids = set()
    remaining_centroids = list()
    for centroid, pixels in clusters.items():
        if len(pixels) >= 3:
            true_centroid = np.mean([pixel for pixel, _ in pixels], axis=0).astype(int)
            for _, shape_id in pixels:
                kept_shape_ids.add(shape_id)
            corners.append(tuple(true_centroid))
        else:
            remaining_centroids.append(centroid)
    return corners


def get_distance_grid(corners: list[Coordinates]) -> np.ndarray:
    distance_grid = np.zeros((len(corners), len(corners)))
    for i, corner_1 in enumerate(corners[:-1]):
        for j, corner_2 in enumerate(corners[i+1:], i+1):
            corners_dist = distance(corner_1, corner_2)
            distance_grid[i, j] = corners_dist
            distance_grid[j, i] = corners_dist
    return distance_grid


def mirror_point(center: Coordinates, point: Coordinates) -> Coordinates:
    x = 2 * center[0] - point[0]
    y = 2 * center[1] - point[1]
    return x, y


def get_relative_grid_dict(corners: list[Coordinates], distance_grid: np.ndarray) -> dict[int, dict[str, int]]:
    relative_grid_dict = defaultdict(dict)
    corners_arr = np.array(corners)
    for corner_idx, corner in enumerate(corners):
        neighbours_idx = distance_grid[corner_idx].argsort()[1:5]
        neighbours = corners_arr[neighbours_idx]
        neighbours_argmin = neighbours.argmin(axis=0)
        neighbours_argmax = neighbours.argmax(axis=0)
        top = neighbours[neighbours_argmin[1]]
        bottom = neighbours[neighbours_argmax[1]]
        left = neighbours[neighbours_argmin[0]]
        right = neighbours[neighbours_argmax[0]]
        if distance(mirror_point(corner, top), bottom) < 10 and l_min_distance(corner, top) < 20:
            top_idx = neighbours_idx[neighbours_argmin[1]]
            bottom_idx = neighbours_idx[neighbours_argmax[1]]
            relative_grid_dict[corner_idx].update({'top': top_idx, 'bottom': bottom_idx})
            relative_grid_dict[top_idx].update({'bottom': corner_idx})
            relative_grid_dict[bottom_idx].update({'top': corner_idx})
        if distance(mirror_point(corner, left), right) < 10 and l_min_distance(corner, left) < 20:
            left_idx = neighbours_idx[neighbours_argmin[0]]
            right_idx = neighbours_idx[neighbours_argmax[0]]
            relative_grid_dict[corner_idx].update({'left': left_idx, 'right': right_idx})
            relative_grid_dict[left_idx].update({'right': corner_idx})
            relative_grid_dict[right_idx].update({'left': corner_idx})
    return relative_grid_dict


def get_tmp_grid_dict(relative_grid_dict: dict[int, dict[str, int]]) -> dict[int, Coordinates]:
    tmp_grid_dict = dict()
    start_corner_idx = max(relative_grid_dict, key=lambda x: len(relative_grid_dict[x]))
    tmp_grid_dict[start_corner_idx] = (0, 0)
    done_corners = set()
    stack = [start_corner_idx]
    while stack:
        corner_idx = stack.pop()
        done_corners.add(corner_idx)
        for direction, neighbour_idx in relative_grid_dict[corner_idx].items():
            if neighbour_idx in done_corners:
                continue
            if direction == 'top':
                tmp_grid_dict[neighbour_idx] = (tmp_grid_dict[corner_idx][0]-1, tmp_grid_dict[corner_idx][1])
                stack.append(neighbour_idx)
            elif direction == 'bottom':
                tmp_grid_dict[neighbour_idx] = (tmp_grid_dict[corner_idx][0]+1, tmp_grid_dict[corner_idx][1])
                stack.append(neighbour_idx)
            elif direction == 'left':
                tmp_grid_dict[neighbour_idx] = (tmp_grid_dict[corner_idx][0], tmp_grid_dict[corner_idx][1]-1)
                stack.append(neighbour_idx)
            elif direction == 'right':
                tmp_grid_dict[neighbour_idx] = (tmp_grid_dict[corner_idx][0], tmp_grid_dict[corner_idx][1]+1)
                stack.append(neighbour_idx)
    return tmp_grid_dict


def get_grid_dict(corners: list[Coordinates], tmp_grid_dict: dict[int, Coordinates]) -> tuple[dict[Coordinates, Coordinates], int, int]:
    min_row = min(x for x, y in tmp_grid_dict.values()) - 1
    min_col = min(y for x, y in tmp_grid_dict.values()) - 1
    grid_dict = dict()
    for corner_idx, (x, y) in tmp_grid_dict.items():
        grid_dict[(x - min_row, y - min_col)] = corners[corner_idx]
    n_rows = max(x for x, y in grid_dict) + 2
    n_cols = max(y for x, y in grid_dict) + 2
    return grid_dict, n_rows, n_cols

def fill_missing_corners(grid_dict: dict[Coordinates, Coordinates], n_rows: int, n_cols: int):
    cutoff = max(n_rows, n_cols)
    i = 0
    while len(grid_dict) < n_rows * n_cols:
        i += 1
        if i > cutoff:
            raise Exception('Could not fill missing corners')
        for x in range(n_rows):
            for y in range(n_cols):
                if (x, y) in grid_dict:
                    continue
                approximations = list()
                if (x-1, y) in grid_dict and (x-2, y) in grid_dict:
                    approximations.append(mirror_point(grid_dict[(x-1, y)], grid_dict[(x-2, y)]))
                if (x+1, y) in grid_dict and (x+2, y) in grid_dict:
                    approximations.append(mirror_point(grid_dict[(x+1, y)], grid_dict[(x+2, y)]))
                if (x, y-1) in grid_dict and (x, y-2) in grid_dict:
                    approximations.append(mirror_point(grid_dict[(x, y-1)], grid_dict[(x, y-2)]))
                if (x, y+1) in grid_dict and (x, y+2) in grid_dict:
                    approximations.append(mirror_point(grid_dict[(x, y+1)], grid_dict[(x, y+2)]))
                if approximations:
                    point_approximation = np.mean(approximations, axis=0).round().astype(int)
                    grid_dict[(x, y)] = (point_approximation[0], point_approximation[1])


def reconstruct_grid_img(grid_dict: dict[Coordinates, Coordinates], img_arr: np.ndarray, n_rows: int, n_cols: int) -> dict[Coordinates, np.ndarray]:
    width = 100
    grid_img_dict = dict()

    for x in range(n_rows-1):
        for y in range(n_cols-1):
            input_pts = np.array([
                grid_dict[(x, y)],
                grid_dict[(x+1, y)],
                grid_dict[(x+1, y+1)],
                grid_dict[(x, y+1)]
                ]).astype('float32')
            output_pts = np.array([(0, 0), (0, width), (width, width), (width, 0)]).astype('float32')

            M = cv2.getPerspectiveTransform(input_pts, output_pts)
            out = cv2.warpPerspective(img_arr, M, (width, width), flags=cv2.INTER_LINEAR)
            grid_img_dict[(x, y)] = out
    return grid_img_dict


def parse(file: str) -> dict[Coordinates, np.ndarray]:
    img_arr = load_img(file)
    edges_arr = preprocess_img(img_arr)
    boxes = get_boxes(edges_arr)
    clusters = get_clusters(boxes)
    corners = get_corners(clusters)
    distance_grid = get_distance_grid(corners)
    relative_grid_dict = get_relative_grid_dict(corners, distance_grid)
    tmp_grid_dict = get_tmp_grid_dict(relative_grid_dict)
    grid_dict, n_rows, n_cols = get_grid_dict(corners, tmp_grid_dict)
    fill_missing_corners(grid_dict, n_rows, n_cols)
    grid_img_dict = reconstruct_grid_img(grid_dict, img_arr, n_rows, n_cols)
    return grid_img_dict
"""
