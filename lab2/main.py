from lab1.main import *
import numpy as np
from PIL import Image, ImageDraw

from lab1.main import Point
from lab4.main import *


# 1
from module.Image3 import *

if __name__ == '__main__':
    image3 = Image3(1000, 1000)

    points = [Point(100, 100, 100), Point(400, 300, 125), Point(900, 250, 0)]
    # image3.draw_triangle(points, Color3(0, 0, 0))
    # image3.save('../out/triangle.png')

    obj3dmodel = OBJ3DModel('../stuff/fox.obj')
    points = list(map(lambda point: Point(round(900 - 10 * point[1]),
                                          round(10 * point[0] + 500),
                                          round(10 * point[2])),
                      obj3dmodel.get_verticles()))
    polygons = obj3dmodel.get_polygons()
    image3.draw_polygons(points, polygons)
    image3.save('../out/fox.png')
    # image3.draw_polygons()
