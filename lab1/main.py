import math
import random
from typing import List

from PIL import Image, ImageDraw
import numpy as np
from lab2.main import *


class Point:
    def __init__(self, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    @x.setter
    def x(self, value):
        self.__x = value

    @y.setter
    def y(self, value):
        self.__y = value

    @z.setter
    def z(self, value):
        self.__z = value


def part1(rows, col):
    image1 = np.zeros((rows, col), dtype=np.uint8)
    imageBlack = Image.fromarray(image1)
    imageBlack.save('out/myBlack.png')
    image2 = np.full((rows, col), 255, dtype=np.uint8)
    imageWhite = Image.fromarray(image2)
    imageWhite.save('out/myWhite.png')
    image3 = np.full((rows, col, 3), (255, 0, 0), dtype=np.uint8)
    imageRed = Image.fromarray(image3)
    imageRed.save('out/myRed.png')
    image4 = np.zeros((rows, col, 3), dtype=np.uint8)
    # np.full((rows, col, 3), [100, 50, 200], dtype=np.uint8)
    for x in range(0, rows):
        for y in range(0, col):
            v = round((x + y) % 256)
            image4[x][y] = (v, v, v)
    imageReg = Image.fromarray(image4)
    imageReg.save('out/myReg.png')


class Color3:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def r(self):
        return self.r

    def g(self):
        return self.g

    def b(self):
        return self.b


class Image3:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = np.zeros(w * h, dtype=Color3)
        self.initial_data()
        self.z_matrix = np.zeros((w, h))

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

    def draw_triangle(self, points: List[Point]):
        if len(points) != 3:
            raise Exception('Error', 'Incorrect count of points')

        x_list = list(map(lambda e: e.x, points))
        y_list = list(map(lambda e: e.y, points))
        y_min = min(y_list)
        x_min = min(x_list)
        y_max = max(y_list)
        x_max = max(x_list)
        if x_max > self.h or x_min < 0 or y_max > self.w or y_min < 0:
            raise Exception('Error', 'Triangle coordinates are out of bounds')

        point1 = points[0]
        point2 = points[1]
        point3 = points[2]
        n = np.cross([point2.x - point1.x, point2.y - point1.y, point2.z - point1.z],
                     [point2.x - point3.x, point2.y - point3.y, point2.z - point3.z])
        v = [0, 0, 1]
        cos_alpha = (n @ v) / np.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
        if cos_alpha > 0:
            return
        color = Color3(255 * abs(cos_alpha), 0, 0)
        try:
            for x in range(round(x_min), round(x_max)):
                for y in range(round(y_min), round(y_max)):
                    bc = barycentric_coordinates(x, y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)
                    if np.all(bc >= 0):
                        z_val = bc[0] * point1.z + bc[1] * point2.z + bc[2] * point3.z
                        if z_val > self.z_matrix[x][y]:
                            self.z_matrix[x][y] = z_val
                            self.set(x, y, color)
        except Exception as e:
            print(e.args)

    def draw_polygons(self, points: List[Point], polygons: List):
        for i in range(len(polygons)):
            polygon1 = polygons[i][0]
            polygon2 = polygons[i][1]
            polygon3 = polygons[i][2]
            self.draw_triangle([points[polygon1 - 1], points[polygon2 - 1], points[polygon3 - 1]])


def part3_1(x0, y0, image, color):
    for i in range(0, 13):
        alpha = 2 * math.pi * i / 13
        x1 = 100 + 95 * math.cos(alpha)
        y1 = 100 + 95 * math.sin(alpha)
        for t in np.arange(0, 1, 0.01):
            x = round(x0 * (1 - t) + x1 * t)
            y = round(y0 * (1 - t) + y1 * t)
            image.putpixel((x, y), color)
    image.save('out/var1.png')


def part3_2(x0, y0, image, color):
    for i in range(0, 13):
        alpha = 2 * math.pi * i / 13
        x1 = 100 + 95 * math.cos(alpha)
        y1 = 100 + 95 * math.sin(alpha)
        for x in np.arange(x0, x1, 1):
            t = (x - x0) / (x1 - x0)
            y = round(y0 * (1 - t) + y1 * t)
            image.putpixel((round(x), y), color)
    image.save('out/var2.png')


def part3_3(x0, y0, image, color):
    for i in range(0, 13):
        alpha = 2 * math.pi * i / 13
        x1 = 100 + 95 * math.cos(alpha)
        y1 = 100 + 95 * math.sin(alpha)
        x0 = 100
        y0 = 100
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        for x in np.arange(x0, x1, 1):
            t = (x - x0) / (x1 - x0)
            y = round(y0 * (1 - t) + y1 * t)
            if steep:
                image.putpixel((round(y), round(x)), color)
            else:
                image.putpixel((round(x), round(y)), color)
    image.save('out/var3.png')


def part3_4(x0, y0, x1, y1, image, color):
    steep = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    if dx == 0 and dy == 0:
        return
    derror = abs(dy / dx)
    error = 0
    y = y0
    for x in np.arange(x0, x1, 1):
        if steep:
            image.putpixel((round(y), round(x)), color)
        else:
            image.putpixel((round(x), round(y)), color)
        error = error + derror
        if error > 0.5:
            if y1 > y0:
                y = y + 1
            else:
                y = y - 1
            error = error - 1


def part3_4draw(image, color):
    for i in range(0, 13):
        part3_4(100, 100, 100 + 95 * math.cos(2 * math.pi * i / 13), 100 + 95 * math.sin(2 * math.pi * i / 13), image,
                color)
        image.save('out/var4.png')


class OBJ3DModel:
    def __init__(self, source_file_path):
        self.__verticles = None
        self.__polygons = None
        self.source_file_path = source_file_path
        self.parse()

    def parse(self):
        verticles = []
        polygons = []
        with open(self.source_file_path) as f:
            lines = f.readlines()

        f.close()

        for line in lines:
            if line.startswith('v '):
                verticles.append(line.split()[1:])
            if line.startswith('f '):
                polygon_infos = line.split()[1:]
                polygon = []
                for polygon_info in polygon_infos:
                    polygon.append(int(polygon_info.split('/')[0]))
                polygons.append(polygon[:3])

        verticles = list(map(lambda x: list(map(lambda b: float(b), x)), verticles))

        self.__verticles = np.array(verticles)
        self.__polygons = np.array(polygons)

    def get_verticles(self):
        return self.__verticles

    def get_polygons(self):
        return self.__polygons

    def get_polygons_points(self):
        return list(map(lambda x: list(map(lambda b: self.__verticles[b], x)), self.__polygons))


def part5(model: OBJ3DModel, scale: int = 10, shift: int = 500):
    image1 = np.zeros((1000, 1000), dtype=np.uint8)
    imageBlack = Image.fromarray(image1)
    for point in model.get_verticles():
        x = round(scale * point[0] + shift)
        y = round(-scale * point[1] + shift)
        if 0 <= x < 1000 and 0 <= y < 1000:
            imageBlack.putpixel((x, y), 255)
    imageBlack.save('out/vertex-st.png')


def part7(model: OBJ3DModel, scale: int = 50, shift: int = 500):
    image1 = np.zeros((1000, 1000), dtype=np.uint8)
    imageBlack = Image.fromarray(image1)
    for polygon_point in model.get_polygons_points():
        part3_4(scale * polygon_point[0][0] + shift, -scale * polygon_point[0][1] + shift,
                scale * polygon_point[1][0] + shift, -scale * polygon_point[1][1] + shift, imageBlack, 255)
        part3_4(scale * polygon_point[1][0] + shift, -scale * polygon_point[1][1] + shift,
                scale * polygon_point[2][0] + shift, -scale * polygon_point[2][1] + shift, imageBlack, 255)
        part3_4(scale * polygon_point[0][0] + shift, -scale * polygon_point[0][1] + shift,
                scale * polygon_point[2][0] + shift, -scale * polygon_point[2][1] + shift, imageBlack, 255)
    imageBlack.save('out/poligon-st.png')


if __name__ == '__main__':
    # -------------1-----------
    part1(200, 200)
    # #------------3-----------
    image1 = np.zeros((200, 200), dtype=np.uint8)
    imageBlack = Image.fromarray(image1)
    part3_1(100, 100, imageBlack, color=255)
    imageBlack = Image.fromarray(image1)
    part3_2(100, 100, imageBlack, color=255)
    imageBlack = Image.fromarray(image1)
    part3_3(100, 100, imageBlack, color=255)
    imageBlack = Image.fromarray(image1)
    part3_4draw(imageBlack, color=255)
    # -------------5-----------
    obj3dmodel = OBJ3DModel('stuff/StormTrooper.obj')
    part5(obj3dmodel, scale=100)
    # --------------7-----------
    part7(obj3dmodel, scale=100)
