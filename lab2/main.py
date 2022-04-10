from lab1.main import *


# 1


def barycentric_coordinates(x, y, x0, y0, x1, y1, x2, y2):
    try:
        lambda0 = ((x1 - x2) * (y - y2) - (y1 - y2) * (x - x2)) / ((x1 - x2) * (y0 - y2) - (y1 - y2) * (x0 - x2))
        lambda1 = ((x2 - x0) * (y - y0) - (y2 - y0) * (x - x0)) / ((x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0))
        lambda2 = ((x0 - x1) * (y - y1) - (y0 - y1) * (x - x1)) / ((x0 - x1) * (y2 - y1) - (y0 - y1) * (x2 - x1))
    except Exception as e:
        print(x, y, x0, y0, x1, y1, x2, y2)
    return np.array([lambda0, lambda1, lambda2])


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
