from dataclasses import dataclass

import numpy as np

from module.Image3 import *
from module.ImagePoint import *
from module.OBJModel import *
from module.Point import *


def to_projective(a_x, a_y, u_0, v_0, z0, point):
    new_z = point[2] + z0
    new_point = Point(point[0], -point[1], new_z)
    u = a_x * new_point.x / new_z + u_0
    v = a_y * new_point.y / new_z + v_0
    return ImagePoint(u, v, new_point)


def to_projective_list(a_x, a_y, u_0, v_0, z0, point_list: list):
    return list(map(lambda x: to_projective(a_x, a_y, u_0, v_0, z0, x),
                    point_list))


if __name__ == '__main__':
    image3 = Image3(1000, 1000)
    obj3dmodel = OBJ3DModel('../stuff/storm_trooper_triang.obj')
    scale = 1000.0
    shift = 500.0
    points = to_projective_list(scale, scale, shift, shift, 1.5, obj3dmodel.get_verticles())
    polygons = obj3dmodel.get_polygons()
    normals = obj3dmodel.get_normals()
    id_normals = obj3dmodel.get_id_normals()
    image3.draw_polygons_perspective(points, polygons, normals, id_normals)
    image3.save('../out/lab3.png')
