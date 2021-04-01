import numpy as np
from PIL import Image, ImageDraw
import math
from Parser import Parser
import DrawingTriangles as dr

size = 5000


class Z_buf:
    def __init__(self):
        # z-буфер - это матрица из вещественных значений по размеру совпадающая с
        # изображением. Изначально все элементы инициализируются значением 10000
        self.buffer = [[10000 for i in range(size)] for j in range(size)]


# метод отрисовки треугольников для объемных фигур
def draw_triangles(x0, y0, z0, x1, y1, z1, x2, y2, z2, image, color, size, z_buf):
    draw = ImageDraw.Draw(image)
    xMin = math.floor(np.min([x0, x1, x2]))
    yMin = math.floor(np.min([y0, y1, y2]))
    xMax = math.ceil(np.max([x0, x1, x2]))
    yMax = math.ceil(np.max([y0, y1, y2]))
    if (xMin < 0):
        xMin = 0
    if (yMin < 0):
        yMin = 0
    for x in range(xMin, xMax):
        for y in range(yMin, yMax):
            lambda0, lambda1, lambda2 = dr.bar_coord(x0, y0, x1, y1, x2, y2, x, y)
            if lambda0 > 0 and lambda1 > 0 and lambda2 > 0:
                # z-координата исходного полигона через z-координаты вершин
                z_ishod = lambda0 * z0 + lambda1 * z1 + lambda2 * z2
                if z_ishod < z_buf.buffer[x][y]:
                    draw.point((x, size - y), color)
                    z_buf.buffer[x][y] = z_ishod

# изменения функции отрисовки полигонов с учетом требований задания 13
def draw_polygons(image):
    parser = Parser()
    parser.load_points("Test.obj", True)
    parser.load_polygons("Test.obj")
    z_buf = Z_buf()
    for polygon in parser.polygons:
        triangle = []
        for point in polygon:
            x, y, z = parser.points[point - 1]
            triangle.append((28000 * x + 2500, 28000 * y + 1500, 20000 * z + 2000))
        normal = count_norm(triangle)
        cos = get_cos(normal)
        if cos < 0:
            draw_triangles(triangle[0][0], triangle[0][1], triangle[0][2], triangle[1][0], triangle[1][1],
                           triangle[1][2], triangle[2][0], triangle[2][1], triangle[2][2], image,
                           (-int(255 * cos), 0, 0), size, z_buf)
            # белый кролик при цвете (-int(255 * cos),-int(255 * cos), -int(255 * cos))
        else:
            continue
    image.save("images/RabbitIn3D(1).jpg")


# вычисление нормали к поверхности треугольника
# параметр функции - треугольник, координаты которого используются
def count_norm(triangle):
    return np.cross([triangle[1][0] - triangle[0][0], triangle[1][1] - triangle[0][1], triangle[1][2] - triangle[0][2]],
                    [triangle[1][0] - triangle[2][0], triangle[1][1] - triangle[2][1], triangle[1][2] - triangle[2][2]])


# вычисление косинуса угла падения направленного света как
# скалярное произведение нормали треугольника и направление света / роизведение нормали этих векторов
def get_cos(n):
    return np.dot(n, [0, 0, 1]) / (np.linalg.norm(n) * np.linalg.norm([0, 0, 1]))


image = Image.new('RGB', (5000, 5000))
draw_polygons(image)
