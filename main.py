import numpy as np
from PIL import Image


# 2
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


# 2
class Image3:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = np.zeros(w * h, dtype=Color3)
        self.initial_data()

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


class OBJ3DModel:
    def __init__(self, source_file_path):
        self.verticles = None
        self.polygons = None
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
                    polygon.append(polygon_info.split('/'))
                polygons.append(polygon)

        self.verticles = np.array(verticles)
        self.polygons = np.array(polygons)

    def get_verticles(self):
        return self.verticles

    def get_polygons(self):
        return self.polygons


# 3
def line_v1(x0, y0, x1, y1, image3, color3):
    for t in np.arange(0, 1, 0.01):
        x = int(x0 * (1. - t) + x1 * t)
        y = int(y0 * (1. - t) + y1 * t)
        image3.set(x, y, color3)
    return image3


# 3
def line_v2(x0, y0, x1, y1, image3, color3):
    for x in range(x0, x1):
        t = (x - x0) / float(x1 - x0)
        y = int(y0 * (1. - t) + y1 * t)
        image3.set(x, y, color3)
    return image3


# 3
def line_v3(x0, y0, x1, y1, image3, color3):
    step = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        step = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    x = x0
    while x <= x1:
        t = (x - x0) / float(x1 - x0)
        y = int(y0 * (1. - t) + y1 * t)
        if step:
            image3.set(y, x, color3)
        else:
            image3.set(x, y, color3)
        x = x + 1
    return image3


# 3
def line_v4(x0, y0, x1, y1, image3, color3):
    step = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        step = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    derror = abs(dy / float(dx))
    error = 0
    y = y0

    x = x0
    while x <= x1:
        if step:
            image3.set(y, x, color3)
        else:
            image3.set(x, y, color3)
        error += derror
        if error > .5:
            y += (1 if y1 > y0 else -1)
            error = error - 1
        x = x + 1
    return image3


def draw_star_v1():
    image = Image3(200, 200)
    for i in range(0, 13):
        image = line_v1(100, 100, int(100 + 95 * np.cos(2 * np.pi * i / 13)),
                        int(100 + 95 * np.sin(2 * np.pi * i / 13)), image, Color3(0, 0, 0))
    return image


def draw_star_v2():
    image = Image3(200, 200)
    for i in range(0, 13):
        image = line_v2(100, 100, int(100 + 95 * np.cos(2 * np.pi * i / 13)),
                        int(100 + 95 * np.sin(2 * np.pi * i / 13)), image, Color3(0, 0, 0))
    return image


def draw_star_v3():
    image = Image3(200, 200)
    for i in range(0, 13):
        image = line_v3(100, 100, int(100 + 95 * np.cos(2 * np.pi * i / 13)),
                        int(100 + 95 * np.sin(2 * np.pi * i / 13)), image, Color3(0, 0, 0))
    return image


def draw_star_v4():
    image = Image3(200, 200)
    for i in range(0, 13):
        image = line_v4(100, 100, int(100 + 95 * np.cos(2 * np.pi * i / 13)),
                        int(100 + 95 * np.sin(2 * np.pi * i / 13)), image, Color3(0, 0, 0))
    return image


w, h = 200, 200
matrix = np.zeros([w, h], dtype=np.uint8)
matrix = np.matrix(matrix)
black_img = Image.fromarray(matrix)
black_img.show()

for i in range(w):
    matrix[i].fill(255)
white_img = Image.fromarray(matrix)
white_img.show()

matrix = np.zeros([w, h, 3], dtype=np.uint8)
matrix[:, :h] = [255, 0, 0]
red_img = Image.fromarray(matrix)
red_img.show()

for i in range(w):
    for j in range(h):
        for k in range(3):
            matrix[i, j, k] = (i + j + k) % 256

gradient_img = Image.fromarray(matrix)
gradient_img.show()

# 3

draw_star_v1().save('v1.png')
draw_star_v2().save('v2.png')
draw_star_v3().save('v3.png')
draw_star_v4().save('v4.png')


# 4,5
obj3dmodel = OBJ3DModel('fox.obj')
