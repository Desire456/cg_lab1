from dataclasses import dataclass

import numpy as np

from module.Image3 import *
from module.ImagePoint import *
from module.OBJModel import *
from module.Point import *


def to_projective(a_x, a_y, u_0, v_0, z0, point):
    new_point = Point(point[0], -point[1], point[2] + z0)
    u = a_x * new_point.x / new_point.z + u_0
    v = a_y * new_point.y / new_point.z + v_0
    return ImagePoint(u, v, new_point)


def to_projective_list(a_x, a_y, u_0, v_0, z0, point_list: list):
    return list(map(lambda x: to_projective(a_x, a_y, u_0, v_0, z0, x),
                    point_list))

def get_image_point(a_x, a_y, u_0, v_0, point: Point):
    u = a_x * point.x / point.z + u_0
    v = a_y * point.y / point.z + v_0
    return ImagePoint(u, v, point)


def rotate_point(projective_point, angles):
    alpha, beta, gamma = [180 * n / np.pi for n in angles]
    cosa = np.cos(alpha)
    sina = np.sin(alpha)
    cosb = np.cos(beta)
    sinb = np.sin(beta)
    cosg = np.cos(gamma)
    sing = np.sin(gamma)
    rotate_x = np.array([[1, 0, 0],
                         [0, cosa, sina],
                         [0, -sina, cosa]])
    rotate_y = np.array([[cosb, 0, sinb],
                         [0, 1, 0],
                         [-sinb, 0, cosb]])
    rotate_z = np.array([[cosg, sing, 0],
                        [-sing, cosg, 0],
                        [0, 0, 1]])
    R = rotate_x @ rotate_y @ rotate_z
    rotated_points = R @ np.array([projective_point.point.x, projective_point.point.y, projective_point.point.z])
    return Point(rotated_points[0], rotated_points[1], rotated_points[2])

def rotate(point_list: list, a_x, a_y, u_0, v_0, z0, angles):
    projective_point_list = to_projective_list(a_x, a_y, u_0, v_0, z0, point_list)
    return list(map(lambda x: get_image_point(a_x, a_y, u_0, v_0, rotate_point(x, angles)), projective_point_list))


if __name__ == '__main__':
    image3 = Image3(1000, 1000)
    obj3dmodel = OBJ3DModel('../stuff/storm_trooper_triang.obj')
    scale = 1000.0
    shift = 500.0
    angles = [0, 0, 0]
    polygons = obj3dmodel.get_polygons()
    normals = obj3dmodel.get_normals()
    id_normals = obj3dmodel.get_id_normals()
    points = rotate(obj3dmodel.get_verticles(), scale, scale, shift, shift, 1.5, angles)
    image3.draw_polygons_perspective(points, polygons, normals, id_normals)
    image3.save('../out/lab3.png')
