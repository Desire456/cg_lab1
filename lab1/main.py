import math
from typing import List

from lab4.main import *
from module.Barycentric import barycentric_coordinates
from module.ImagePoint import ImagePoint
from module.OBJModel import OBJ3DModel
from module.Point import Point


def part1(rows, col):
    image1 = np.zeros((rows, col), dtype=np.uint8)
    imageBlack = Image.fromarray(image1)
    imageBlack.save('../out/myBlack.png')
    image2 = np.full((rows, col), 255, dtype=np.uint8)
    imageWhite = Image.fromarray(image2)
    imageWhite.save('../out/myWhite.png')
    image3 = np.full((rows, col, 3), (255, 0, 0), dtype=np.uint8)
    imageRed = Image.fromarray(image3)
    imageRed.save('../out/myRed.png')
    image4 = np.zeros((rows, col, 3), dtype=np.uint8)
    # np.full((rows, col, 3), [100, 50, 200], dtype=np.uint8)
    for x in range(0, rows):
        for y in range(0, col):
            v = round((x + y) % 256)
            image4[x][y] = (v, v, v)
    imageReg = Image.fromarray(image4)
    imageReg.save('../out/myReg.png')



def part3_1(x0, y0, image, color):
    for i in range(0, 13):
        alpha = 2 * math.pi * i / 13
        x1 = 100 + 95 * math.cos(alpha)
        y1 = 100 + 95 * math.sin(alpha)
        for t in np.arange(0, 1, 0.01):
            x = round(x0 * (1 - t) + x1 * t)
            y = round(y0 * (1 - t) + y1 * t)
            image.putpixel((x, y), color)
    image.save('../out/var1.png')


def part3_2(x0, y0, image, color):
    for i in range(0, 13):
        alpha = 2 * math.pi * i / 13
        x1 = 100 + 95 * math.cos(alpha)
        y1 = 100 + 95 * math.sin(alpha)
        for x in np.arange(x0, x1, 1):
            t = (x - x0) / (x1 - x0)
            y = round(y0 * (1 - t) + y1 * t)
            image.putpixel((round(x), y), color)
    image.save('../out/var2.png')


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
    image.save('../out/var3.png')


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
        image.save('../out/var4.png')




def part5(model: OBJ3DModel, scale: int = 10, shift: int = 500):
    image1 = np.zeros((1000, 1000), dtype=np.uint8)
    imageBlack = Image.fromarray(image1)
    for point in model.get_verticles():
        x = round(scale * point[0] + shift)
        y = round(-scale * point[1] + shift)
        if 0 <= x < 1000 and 0 <= y < 1000:
            imageBlack.putpixel((x, y), 255)
    imageBlack.save('../out/vertex-st.png')


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
    imageBlack.save('../out/poligon-st.png')


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
    obj3dmodel = OBJ3DModel('../stuff/StormTrooper.obj')
    part5(obj3dmodel, scale=100)
    # --------------7-----------
    part7(obj3dmodel, scale=100)
