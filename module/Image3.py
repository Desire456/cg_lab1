import sys
from typing import List

import numpy as np

from lab4.main import dot_product_norm
from module.Barycentric import barycentric_coordinates
from module.Color3 import Color3
from module.ImagePoint import ImagePoint
from module.Point import Point
from PIL import Image, ImageDraw

class Image3:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = np.zeros(w * h, dtype=Color3)
        self.initial_data()
        self.z_matrix = np.full((w, h), sys.maxsize)

    def set(self, x, y, color3):
        self.data[x + y * self.w] = color3

    def get(self, x, y):
        return self.data[x + y * self.w]

    def initial_data(self):
        for i in range(self.w):
            for j in range(self.h):
                self.set(i, j, Color3(255, 255, 255))

    def save(self, filename):
        image_arr = np.zeros([self.w, self.h, 3], dtype=np.uint8)
        for i in range(self.w):
            for j in range(self.h):
                for k in range(3):
                    color3 = self.get(i, j)
                    image_arr[i, j] = [color3.r, color3.g, color3.b]
        Image.fromarray(image_arr).save(filename)

    def draw_triangle(self, points: List[Point], normals: List):
        if len(points) != 3:
            raise Exception('Error', 'Incorrect count of points')

        x_list = list(map(lambda e: round(e.x), points))
        y_list = list(map(lambda e: round(e.y), points))
        y_min = max(min(y_list), 0)
        x_min = max(min(x_list), 0)
        y_max = min(max(y_list), self.h)
        x_max = min(max(x_list), self.w)

        point1 = points[0]
        point2 = points[1]
        point3 = points[2]
        n = np.cross([point2.x - point1.x, point2.y - point1.y, point2.z - point1.z],
                     [point2.x - point3.x, point2.y - point3.y, point2.z - point3.z])
        v = [0, 0, 1]
        cos_alpha = (n @ v) / np.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
        # cos_alpha = 0
        if cos_alpha <= 0:
            return
        color = Color3(255 * abs(cos_alpha), 0, 0)
        l0 = dot_product_norm(normals[0], v)
        l1 = dot_product_norm(normals[1], v)
        l2 = dot_product_norm(normals[2], v)
        # try:
        for x in range(round(x_min), round(x_max) + 1):
            for y in range(round(y_min), round(y_max) + 1):
                bc = barycentric_coordinates(float(x), float(y), point1.x, point1.y, point2.x, point2.y, point3.x,
                                             point3.y)
                intencity = 255 * (bc[0] * l0 + bc[1] * l1 + bc[2] * l2)
                color = Color3(intencity, intencity, intencity)
                if np.all(bc >= 0):
                    z_val = bc[0] * point1.z + bc[1] * point2.z + bc[2] * point3.z
                    if z_val > self.z_matrix[x][y]:
                        self.z_matrix[x][y] = z_val
                        self.set(x, y, color)

    def draw_polygons(self, points: List[Point], polygons: List, normals: List, id_normals: List):
        for i in range(len(polygons)):
            polygon1 = polygons[i][0]
            polygon2 = polygons[i][1]
            polygon3 = polygons[i][2]
            normal1 = id_normals[i][0]
            r_n1 = normals[normal1 - 1]
            normal2 = id_normals[i][1]
            r_n2 = normals[normal2 - 1]
            normal3 = id_normals[i][2]
            r_n3 = normals[normal3 - 1]
            self.draw_triangle([points[polygon1 - 1], points[polygon2 - 1], points[polygon3 - 1]], [r_n1, r_n2, r_n3])

    def draw_polygons_perspective(self, points: List[ImagePoint], polygons: List, normals: List, id_normals: List):
        for i in range(len(polygons)):
            polygon1 = polygons[i][0]
            polygon2 = polygons[i][1]
            polygon3 = polygons[i][2]
            normal1 = id_normals[i][0]
            r_n1 = normals[normal1 - 1]
            normal2 = id_normals[i][1]
            r_n2 = normals[normal2 - 1]
            normal3 = id_normals[i][2]
            r_n3 = normals[normal3 - 1]
            self.draw_triangle_perspective([points[polygon1 - 1], points[polygon2 - 1], points[polygon3 - 1]],
                                           [r_n1, r_n2, r_n3])

    def draw_triangle_perspective(self, points: List[ImagePoint], normals: List):
        if len(points) != 3:
            raise Exception('Error', 'Incorrect count of points')

        x_list = list(map(lambda e: e.u, points))
        y_list = list(map(lambda e: e.v, points))
        y_min = max(min(y_list), 0)
        x_min = max(min(x_list), 0)
        y_max = min(max(y_list), self.h)
        x_max = min(max(x_list), self.w)

        point1 = points[0]
        point2 = points[1]
        point3 = points[2]
        n = np.cross(
            [point2.point.x - point1.point.x, point2.point.y - point1.point.y, point2.point.z - point1.point.z],
            [point2.point.x - point3.point.x, point2.point.y - point3.point.y, point2.point.z - point3.point.z])
        v = [0, 0, 1]
        cos_alpha = (n @ v) / np.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
        if cos_alpha >= 0:
            return
        color = Color3(255 * abs(cos_alpha), 0, 0)
        l0 = dot_product_norm(normals[0], v)
        l1 = dot_product_norm(normals[1], v)
        l2 = dot_product_norm(normals[2], v)
        # try:
        for x in range(round(x_min), round(x_max) + 1):
            for y in range(round(y_min), round(y_max) + 1):
                bc = barycentric_coordinates(float(x), float(y), point1.u, point1.v, point2.u,
                                             point2.v, point3.u, point3.v)
                intencity = 255 * abs(bc[0] * l0 + bc[1] * l1 + bc[2] * l2)
                # color = Color3(intencity, intencity, intencity)
                if np.all(bc >= 0):
                    z_val = bc[0] * point1.point.z + bc[1] * point2.point.z + bc[2] * point3.point.z
                    if z_val < self.z_matrix[x][y]:
                        self.z_matrix[x][y] = z_val
                        self.set(x, y, color)
