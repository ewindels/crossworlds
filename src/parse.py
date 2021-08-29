from cv2 import cv2
import os
import numpy as np
from collections import defaultdict
from typing import Union

Coordinates = tuple[Union[float, int], Union[float, int]]

def load_img(file: str) -> np.ndarray:
    file_path = os.path.join('data', 'crosswords', file)
    img_arr = cv2.imread(file_path)
    return img_arr


def preprocess_img(img_arr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (5, 5))
    edges = cv2.Canny(blur, 90, 150)
    kernel_size = (7, 7)
    kernel = np.ones(kernel_size, np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    kernel = np.ones(kernel_size, np.uint8)
    edges = cv2.erode(edges, kernel, iterations=1)
    edges_arr = edges.astype(bool)
    return edges_arr


def fill_zone(pixel_x: int, pixel_y: int, done_arr: np.ndarray, edges_arr: np.ndarray) -> set[tuple[int, int]]:
    zone = set()
    stack = [(pixel_x, pixel_y)]
    while stack:
        x, y = stack.pop()
        zone.add((x, y))
        done_arr[x, y] = True
        for offset_x, offset_y in zip([0, 0, 1, -1], [1, -1, 0, 0]):
            new_x = x + offset_x
            new_y = y + offset_y
            if (0 <= new_x < edges_arr.shape[0]
                and 0 <= new_y < edges_arr.shape[1]
                and not edges_arr[new_x, new_y]
                and not done_arr[new_x, new_y]):
                stack.append((new_x, new_y))
    return zone

 
def get_zones(edges_arr: np.ndarray) -> list[set[tuple[int, int]]]:
    zones = list()
    done_arr = np.zeros(edges_arr.shape).astype(bool)
    for pixel_x in range(edges_arr.shape[0]):
        for pixel_y in range(edges_arr.shape[1]):
            if not done_arr[pixel_x, pixel_y] and not edges_arr[pixel_x, pixel_y]:
                zone = fill_zone(pixel_x, pixel_y, done_arr, edges_arr)
                zones.append(zone)
    return zones


def get_contours(zone: set[tuple[int, int]]) -> tuple[np.ndarray, tuple[int, ...]]:
    zone_arr = np.array([[x, y] for x, y in zone])
    x_min, y_min = zone_arr.min(axis=0)
    x_max, y_max = zone_arr.max(axis=0)
    shape_arr = np.zeros((x_max - x_min + 1, y_max - y_min + 1), dtype=bool)
    for x, y in zone:
        shape_arr[x - x_min, y - y_min] = True
    shape_arr = np.pad(shape_arr, ((5, 5), (5, 5)))
    contours, _ = cv2.findContours(shape_arr.astype('uint8'), 1, 2)
    bounds = (x_min, x_max, y_min, y_max)
    return contours, bounds

 
def get_box(contours: np.ndarray) -> np.ndarray:
    cnt = contours[0]
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = box.astype(int)
    return box


def get_boxes(zones: list) -> list[np.ndarray]:
    boxes = list()
    for zone in zones:
        if 1000 < len(zone) < 10000:
            contours, bounds = get_contours(zone)
            box = get_box(contours)
            x_min, _, y_min, _ = bounds
            box[:, 0] += y_min - 5
            box[:, 1] += x_min - 5
            boxes.append(box)    
    return boxes


def distance(pixel_1: Coordinates, pixel_2: Coordinates) -> float:
    return ((pixel_1[0] - pixel_2[0]) ** 2 + (pixel_1[1] - pixel_2[1]) ** 2) ** 0.5


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
                if distance(pixel, cluster_centroid) < 20:
                    clusters[cluster_centroid].append((pixel, i))
                    break
            else:
                clusters[tuple(pixel)] = [(pixel, i)]
    return clusters


def get_corners(clusters: dict[tuple[int, int], list[tuple[Coordinates, int]]]) -> list[Coordinates]:
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

    print(f'{len(corners)} corners found')
    print(f'{len(kept_shape_ids)} squares found')
    return corners


def get_grid_corners(corners: list[Coordinates]) -> tuple[Coordinates, ...]:
    top_left_corner = min(corners, key=lambda p: p[0] + p[1])
    bottom_right_corner = max(corners, key=lambda p: p[0] + p[1])
    top_right_corner = min(corners, key=lambda p: -p[0] + p[1])
    bottom_left_corner = min(corners, key=lambda p: p[0] - p[1])
    return top_left_corner, bottom_right_corner, top_right_corner, bottom_left_corner


def get_borders(corners: list[Coordinates], grid_corners: tuple[Coordinates, ...]) -> tuple[list[Coordinates], ...]:
    top_left_corner, bottom_right_corner, top_right_corner, bottom_left_corner = grid_corners
    top_row = list()
    left_column = list()
    bottom_row = list()
    right_column = list()
    tol = 10

    for corner in corners:
        if distance_point_to_line(top_left_corner, top_right_corner, corner) < tol:
            top_row.append(corner)
            continue
        if distance_point_to_line(top_left_corner, bottom_left_corner, corner) < tol:
            left_column.append(corner)
        if distance_point_to_line(bottom_left_corner, bottom_right_corner, corner) < tol:
            bottom_row.append(corner)
        if distance_point_to_line(bottom_right_corner, top_right_corner, corner) < tol:
            right_column.append(corner)
    return top_row, left_column, bottom_row, right_column


def get_grid_dict(borders: tuple[list[Coordinates], ...], grid_corners: tuple[Coordinates, ...]) -> dict[Coordinates, Coordinates]:
    top_left_corner, _, top_right_corner, bottom_left_corner = grid_corners
    top_row, left_column, bottom_row, right_column = borders
    grid_dict = dict()
    n_rows = len(left_column)
    n_cols = len(top_row)

    for col, corner in enumerate(sorted(top_row, key=lambda c: distance(top_left_corner, c)), 1):
        grid_dict[(1, col)] = corner
    for row, corner in enumerate(sorted(left_column, key=lambda c: distance(top_left_corner, c)), 1):
        grid_dict[(row, 1)] = corner
    for col, corner in enumerate(sorted(bottom_row, key=lambda c: distance(bottom_left_corner, c)), 1):
        grid_dict[(n_rows, col)] = corner
    for row, corner in enumerate(sorted(right_column, key=lambda c: distance(top_right_corner, c)), 1):
        grid_dict[(row, n_cols)] = corner
    return grid_dict


def get_predicted_coordinates(grid_dict: dict[Coordinates, Coordinates], n_rows: int, n_cols: int) -> dict[Coordinates, Coordinates]:
    predicted_coordinates = dict()

    for row in range(2, n_rows):
        for col in range(2, n_cols):
            l1_p1 = grid_dict[(1, col)]
            l1_p2 = grid_dict[(n_rows, col)]
            l2_p1 = grid_dict[(row, 1)]
            l2_p2 = grid_dict[(row, n_cols)]
            predicted_coordinates[(row, col)] =  lines_intersection(l1_p1, l1_p2, l2_p1, l2_p2)
    return predicted_coordinates


def map_remaining_corners(corners, predicted_coordinates: dict[Coordinates, Coordinates], grid_dict: dict[Coordinates, Coordinates]):
    mapped_corners = {corner for corner in grid_dict.values()}
    for corner in corners:
        if corner in mapped_corners:
            continue
        closest_coor_prediction = min(predicted_coordinates, key=lambda c: distance(corner, predicted_coordinates[c]))
        grid_dict[closest_coor_prediction] = corner
        predicted_coordinates.pop(closest_coor_prediction)


def mirror_point(center: Coordinates, point: Coordinates) -> Coordinates:
    x = 2 * center[0] - point[0]
    y = 2 * center[1] - point[1]
    return x, y


def add_outside_corners(grid_dict: dict[Coordinates, Coordinates], n_rows: int, n_cols: int):
    for row in range(1, n_rows+1):
        grid_dict[(row, 0)] = mirror_point(grid_dict[(row, 1)], grid_dict[(row, 2)])
    grid_dict[(0, 0)] = mirror_point(grid_dict[(1, 1)], grid_dict[(2, 2)])

    for row in range(1, n_rows+1):
        grid_dict[(row, n_cols+1)] = mirror_point(grid_dict[(row, n_cols)], grid_dict[(row, n_cols-1)])
    grid_dict[(n_rows+1, n_cols+1)] = mirror_point(grid_dict[(n_rows, n_cols)], grid_dict[(n_rows-1, n_cols-1)])

    for col in range(1, n_cols+1):
        grid_dict[(0, col)] = mirror_point(grid_dict[(1, col)], grid_dict[(2, col)])
    grid_dict[(n_rows+1, 0)] = mirror_point(grid_dict[(n_rows, 1)], grid_dict[(n_rows-1, 2)])

    for col in range(1, n_cols+1):
        grid_dict[(n_rows+1, col)] = mirror_point(grid_dict[(n_rows, col)], grid_dict[(n_rows-1, col)])
    grid_dict[(0, n_cols+1)] = mirror_point(grid_dict[(1, n_cols)], grid_dict[(2, n_cols-1)])


def reconstruct_grid_img(grid_dict: dict[Coordinates, Coordinates], img_arr: np.ndarray, n_rows: int, n_cols: int):
    squares_width = 100
    flat_img = np.zeros(((n_rows + 1) * squares_width, (n_cols + 1) * squares_width, 3)).astype(int)

    for x in range(n_rows+1):
        for y in range(n_cols+1):
            input_pts = np.array([grid_dict[(x, y)],
                                    grid_dict[(x+1, y)],
                                    grid_dict[(x+1, y+1)],
                                    grid_dict[(x, y+1)]]).astype('float32')
            output_pts = np.array([(0, 0), (0, 100), (100, 100), (100, 0)]).astype('float32')

            M = cv2.getPerspectiveTransform(input_pts, output_pts)
            out = cv2.warpPerspective(img_arr, M, (100, 100), flags=cv2.INTER_LINEAR)
            flat_img[x * squares_width:(x + 1) * squares_width, y * squares_width:(y + 1) * squares_width] = out
            flat_img = cv2.circle(flat_img, (y * squares_width + squares_width//2, x * squares_width + squares_width//2), radius=5, color=(255, 0, 0), thickness=-1)
