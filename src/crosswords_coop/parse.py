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

 
def get_box(contour: np.ndarray) -> np.ndarray:
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = box.astype(int)
    return box


def get_boxes(edges_arr: np.ndarray) -> list[np.ndarray]:
    contours, _ = cv2.findContours((~edges_arr).astype('uint8'), 1, 2)
    boxes = list()
    for contour in contours:
        if 2000 < cv2.contourArea(contour) < 10000:
            box = get_box(contour)
            if cv2.contourArea(box) < 10000:
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


def get_grid_dict(borders: tuple[list[Coordinates], ...], grid_corners: tuple[Coordinates, ...]) -> tuple[dict[Coordinates, Coordinates], int, int]:
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
    return grid_dict, n_rows, n_cols


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


def map_remaining_corners(corners: list[Coordinates], predicted_coordinates: dict[Coordinates, Coordinates], grid_dict: dict[Coordinates, Coordinates]):
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


def reconstruct_grid_img(grid_dict: dict[Coordinates, Coordinates], img_arr: np.ndarray, n_rows: int, n_cols: int) -> dict[Coordinates, np.ndarray]:
    width = 100
    grid_img_dict = dict()

    for x in range(n_rows+1):
        for y in range(n_cols+1):
            input_pts = np.array([grid_dict[(x, y)],
                                    grid_dict[(x+1, y)],
                                    grid_dict[(x+1, y+1)],
                                    grid_dict[(x, y+1)]]).astype('float32')
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
    grid_corners = get_grid_corners(corners)
    borders = get_borders(corners, grid_corners)
    grid_dict, n_rows, n_cols = get_grid_dict(borders, grid_corners)
    predicted_coordinates = get_predicted_coordinates(grid_dict, n_rows, n_cols)
    map_remaining_corners(corners, predicted_coordinates, grid_dict)
    add_outside_corners(grid_dict, n_rows, n_cols)
    grid_img_dict = reconstruct_grid_img(grid_dict, img_arr, n_rows, n_cols)
    return grid_img_dict
