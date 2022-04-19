import numpy as np


class OBJ3DModel:
    def __init__(self, source_file_path):
        self.__verticles = None
        self.__polygons = None
        self._normals = None
        self._id_normals = None
        self.source_file_path = source_file_path
        self.parse()

    def parse(self):
        verticles = []
        polygons = []
        id_normals = []
        normals = []
        with open(self.source_file_path) as f:
            lines = f.readlines()

        f.close()

        for line in lines:
            if line.startswith('v '):
                verticles.append(line.split()[1:])
            if line.startswith('f '):
                polygon_infos = line.split()[1:]
                polygon = []
                id_norm = []
                for polygon_info in polygon_infos:
                    polygon.append(int(polygon_info.split('/')[0]))
                    id_norm.append(int(polygon_info.split('/')[2]))
                id_normals.append(id_norm[:3])
                polygons.append(polygon[:3])
            if line.startswith('vn '):
                normals.append(line.split()[1:])

        verticles = list(map(lambda x: list(map(lambda b: float(b), x)), verticles))
        normals = list(map(lambda x: list(map(lambda b: float(b), x)), normals))

        self.__verticles = np.array(verticles)
        self.__polygons = np.array(polygons)
        self._normals = np.array(normals)
        self._id_normals = np.array(id_normals)

    def get_verticles(self):
        return self.__verticles

    def get_polygons(self):
        return self.__polygons

    def get_normals(self):
        return self._normals

    def get_id_normals(self):
        return self._id_normals

    def get_polygons_points(self):
        return list(map(lambda x: list(map(lambda b: self.__verticles[b], x)), self.__polygons))
