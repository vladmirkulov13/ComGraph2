import numpy as np


class Parser:
    def __init__(self):
        self.points = []
        self.polygons = []
        self.vertex_list_z = []

    def load_points(self, fileName, z):
        objFile = open(fileName)
        for line in objFile:
            split = line.split()
            if not len(split):
                continue
            if split[0] == "v":
                tmp = [float(i) for i in split[1:]]
                if z:
                    cord = (tmp[0], tmp[1], tmp[2])
                else:
                    cord = (tmp[0], tmp[1])
                self.points.append(cord)
        objFile.close()

    def load_polygons(self, fileName):
        objFile = open(fileName)
        for line in objFile:
            split = line.split()
            if not len(split):
                continue
            if split[0] == "f":
                polygons = (int(split[1:][0].partition('/')[0]), int(split[1:][1].partition('/')[0]),
                            int(split[1:][2].partition('/')[0]))
                self.polygons.append(polygons)

        objFile.close()

    # ----------------------------------------------------------------------------------------

    # def parserOBJ(self):
    #     with open('test.obj', 'r') as objFile:
    #         for line in objFile:
    #             split = line.split()
    #             if split[0] == "v":
    #                 self.points = np.append(self.points, [[float(split[1]), float(split[2]), float(split[3])]], axis=0)
    #             if split[0] == "f":
    #                 new_split1 = split[1].split('/')
    #                 new_split2 = split[2].split('/')
    #                 new_split3 = split[3].split('/')
    #                 self.polyg = np.append(self.polyg, [[int(new_split1[0]), int(new_split2[0]), int(new_split3[0])]],
    #                                        axis=0)
