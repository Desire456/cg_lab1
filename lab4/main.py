from lab1.main import *
from lab1.main import OBJ3DModel
from lab2.main import *
import numpy as np


def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


def vector_len(v):
    return np.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def dot_product_norm(v1, v2):
    return dot_product(v1, v2) / (vector_len(v1) * vector_len(v2))


if __name__ == '__main__':
    image3 = Image3(1000, 1000)
    obj3dmodel = OBJ3DModel('../stuff/storm_trooper_triang.obj')
    scale = 500.0
    points = list(map(lambda point: Point(scale * -point[0] + 500.0,
                                          scale * point[1] + 500.0,
                                          scale * point[2]),
                      obj3dmodel.get_verticles()))
    # points = obj3dmodel.get_verticles()
    polygons = obj3dmodel.get_polygons()
    normals = obj3dmodel.get_normals()
    id_normals = obj3dmodel.get_id_normals()
    image3.draw_polygons(points, polygons, normals, id_normals)
    image3.save('../out/lab4.png')
