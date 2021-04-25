class Parser:

    # у объекта создается три поля:
    # point - массив точек
    # polygons - массив полигонов
    def __init__(self):
        self.points = []
        self.polygons = []
        self.normals = []
        self.indexes_of_normals = []

    # задание 4
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

    # задание 6
    # считывание номеров вершин для полигонов из файла
    def load_polygons(self, fileName):
        objFile = open(fileName)
        for line in objFile:
            split = line.split()
            if not len(split):
                continue
            if split[0]=="f":
                polygons = (int(split[1:][0].partition('/')[0]), int(split[1:][1].partition('/')[0]),
                            int(split[1:][2].partition('/')[0]))
                self.polygons.append(polygons)

        objFile.close()

    # задание 18 - загрузка нормалей для затеменения Гуро
    def load_normals(self, fileName):
        objFile = open(fileName)
        for line in objFile:
            split = line.split()
            if split[0] == "vn":
                norms = (float(split[1]), float(split[2]),
                         float(split[3]))
                self.normals.append(norms)

        objFile.close()

    # загрузка индексов нормалей
    # т.к. после буквы f идёт Вершина / Текстурные координаты / индекс нормали
    def load_normal_indexes(self, fileName):
        objFile = open(fileName)
        for line in objFile:
            split = line.split()
            # if blank line, skip
            if not len(split):
                continue
            if split[0] == "f":
                first = (split[1:][0])[::-1]
                second = (split[1:][1])[::-1]
                third = (split[1:][2])[::-1]
                indexes = (int(first.partition('/')[0][::-1]), int(second.partition('/')[0][::-1]),
                           int(third.partition('/')[0][::-1]))
                self.indexes_of_normals.append(indexes)
        objFile.close()
