

class Parser:
    # у объекта создается три поля:
    # point - массив точек
    # polygons - массив полигонов
    # vertex_list_z -
    def __init__(self):
        self.points = []
        self.polygons = []
        self.vertex_list_z = []

# считываем координаты вершин из файла
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

# считвание номеров вершин для полигонов из файла

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

