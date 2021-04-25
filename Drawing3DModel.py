import numpy as np
from PIL import Image, ImageDraw
import math
from Parser import Parser


# класс z буффер: поле - матрица изначально заполнена большими значениями - 5000
class Z_buf:
    def __init__(self):
        self.buffer = [[5000 for i in range(size + 1)] for j in range(size + 1)]


# задание 12 - найти нормаль к поверхности треугольника
def find_normal(triangle):
    # 𝑛̅ = [𝑋1 − 𝑋0,𝑌1 − 𝑌0, 𝑍1 − 𝑍0] × [𝑋1 − 𝑋2, 𝑌1 − 𝑌2, 𝑍1 − 𝑍2] - векторное произведение
    return np.cross([triangle[1][0] - triangle[0][0], triangle[1][1] - triangle[0][1], triangle[1][2] - triangle[0][2]],
        [triangle[1][0] - triangle[2][0], triangle[1][1] - triangle[2][1], triangle[1][2] - triangle[2][2]])


# задание 13 - отсечение нелицевых гранец черезз косинус угла падения направленного света
def get_cos(n):
    # нормализовонное скалярное произведение n - нормаль
    # 〈𝑛̅,𝑙〉̅
    # ‖𝑛̅‖∙‖𝑙‖̅
    # направление света - [0, 0 , 1], linalg.norm - норма матрицы
    return np.dot(n, [0, 0, -1]) / (np.linalg.norm(n) * np.linalg.norm([0, 0, -1]))


# бар координаты и отрисовка треугольников изменены для задания 13
def bar_coord(x0, y0, x1, y1, x2, y2, x, y):
    lambda0 = ((x1 - x2) * (y - y2) - (y1 - y2) * (x - x2)) / ((x1 - x2) * (y0 - y2) - (y1 - y2) * (x0 - x2))
    lambda1 = ((x2 - x0) * (y - y0) - (y2 - y0) * (x - x0)) / ((x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0))
    lambda2 = ((x0 - x1) * (y - y1) - (y0 - y1) * (x - x1)) / ((x0 - x1) * (y2 - y1) - (y0 - y1) * (x2 - x1))
    return lambda0, lambda1, lambda2


# задание 16 - проективное преобразование координат
def proj_coord(x, y, z):
    init_vec = np.array([[x], [y], [z]])
    ax = 10000
    ay = 10000
    u0 = 500
    v0 = 500
    matrix = np.array([[ax, 0, u0], [0, ay, v0], [0, 0, 1]])
    final_vec = matrix.dot(init_vec)
    return final_vec[0][0] / final_vec[2][0], final_vec[1][0] / final_vec[2][0]


# задание 17 - поворот модели
def turn_coord(x, y, z):
    init_vec = np.array([[x], [y], [z]])
    alpha = 0
    beta = - (np.pi / 2)
    gamma = 0
    R_1 = np.array([[1, 0, 0], [0, np.cos(alpha), np.sin(alpha)], [0, -np.sin(alpha), np.cos(alpha)]])
    R_2 = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
    R_3 = np.array([[np.cos(gamma), np.sin(gamma), 0], [-np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])
    final_vec = ((R_1.dot(R_2)).dot(R_3)).dot(init_vec)
    return final_vec[0][0], final_vec[1][0], final_vec[2][0]


# тестовые значения из задания 16
def move_coord(x, y, z):
    init_vec = np.array([[x], [y], [z]])
    t_vec = np.array([[0.005], [-0.045], [1.5]])
    final_vec = init_vec + t_vec
    return final_vec[0][0], final_vec[1][0], final_vec[2][0]


# поворот нормалей с поворотом модели
def turn_norms(x, y, z):
    init_vec = np.array([[x], [y], [z]])
    alpha = 0
    beta = np.pi / 2
    gamma = 0
    R_1 = np.array([[1, 0, 0], [0, np.cos(alpha), np.sin(alpha)], [0, -np.sin(alpha), np.cos(alpha)]])
    R_2 = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
    R_3 = np.array([[np.cos(gamma), np.sin(gamma), 0], [-np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])
    final_vec = ((R_1.dot(R_2)).dot(R_3)).dot(init_vec)
    return final_vec[0][0], final_vec[1][0], final_vec[2][0]


# изменение отрисовки треугольников после введение z-буффера
# а также после введения нормалей в задании 18
def draw_triangles(x0, y0, z0, x1, y1, z1, x2, y2, z2, image, z_buf, norms, size):
    draw = ImageDraw.Draw(image)
    # определяем минимальные и максимальные значения огранич. прямоугольника
    xmin = math.floor(np.min([x0, x1, x2]))
    ymin = math.floor(np.min([y0, y1, y2]))
    xmax = math.ceil(np.max([x0, x1, x2]))
    ymax = math.ceil(np.max([y0, y1, y2]))
    if xmin < 0:
        xmin = 0
    if ymin < 0:
        ymin = 0
    # направление света
    l = [0, 0, 1]
    l0 = np.dot(norms[0], l) / (np.linalg.norm(norms[0]) * np.linalg.norm(l))
    l1 = np.dot(norms[1], l) / (np.linalg.norm(norms[1]) * np.linalg.norm(l))
    l2 = np.dot(norms[2], l) / (np.linalg.norm(norms[2]) * np.linalg.norm(l))
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            lambda0, lambda1, lambda2 = bar_coord(x0, y0, x1, y1, x2, y2, x, y)
            if lambda0 > 0 and lambda1 > 0 and lambda2 > 0:
                z_ishodn = lambda0 * z0 + lambda1 * z1 + lambda2 * z2
                if z_ishodn < z_buf.buffer[x][y]:
                    z_buf.buffer[x][y] = z_ishodn
                    # яркость пикселя в зависимости от полученных l0, l1 ,l2
                    light_of_pixel = int(255 * (lambda0 * l0 + lambda1 * l1 + lambda2 * l2))
                    draw.point((x, size - y), (light_of_pixel, light_of_pixel, light_of_pixel))
                else:
                    continue


# задание 13
# изменение отрисовки полигонов в зависимости от косинуса угла + цвет зависит от косинуса
# + используя нормали для задания 18
def draw_polygons(image):
    parser = Parser()
    parser.load_points("Test.obj", True)
    parser.load_polygons("Test.obj")
    parser.load_normals("Test.obj")
    parser.load_normal_indexes("Test.obj")
    z_buf = Z_buf()
    # идем по polygons
    for polygon, ind in zip(parser.polygons, parser.indexes_of_normals):
        triangle = []
        projective_triangle = []
        # заходим внутрь каждого полигона
        for point in polygon:
            # достаем x, y, z по номеру точки, указанном в полигоне
            x, y, z = parser.points[point - 1]
            t_coord = turn_coord(x, y, z)
            x, y, z = t_coord[0], t_coord[1], t_coord[2]
            t_coord = move_coord(x, y, z)
            x, y, z = t_coord[0], t_coord[1], t_coord[2]
            coord = proj_coord(x, y, z)
            triangle.append((x, y, z))
            projective_triangle.append((coord[0], coord[1], 1.0))
            # triangle.append(((-10000 * x + 500), (-10000 * y + 1000), (-10000 * z + 500)))
        norm1, norm2, norm3 = turn_norms(parser.normals[ind[0] - 1][0], parser.normals[ind[0] - 1][1],
            parser.normals[ind[0] - 1][2])
        norm4, norm5, norm6 = turn_norms(parser.normals[ind[1] - 1][0], parser.normals[ind[1] - 1][1],
            parser.normals[ind[1] - 1][2])
        norm7, norm8, norm9 = turn_norms(parser.normals[ind[2] - 1][0], parser.normals[ind[2] - 1][1],
            parser.normals[ind[2] - 1][2])
        norms = ((norm1, norm2, norm3), (norm4, norm5, norm6), (norm7, norm8, norm9))
        n = find_normal(triangle)
        cos = get_cos(n)
        if cos < 0:
            # отрисовка повернутой модели
            draw_triangles(projective_triangle[0][0], projective_triangle[0][1], triangle[0][2],projective_triangle[1][0],
                projective_triangle[1][1], triangle[1][2], projective_triangle[2][0], projective_triangle[2][1],
                triangle[2][2], image, z_buf, norms, size)
            # отрисовка 3D модели с цветом в зависимости от косинуса ( модель не повернута)
            # draw_triangles(triangle[0][0], triangle[0][1], triangle[0][2],
            #     triangle[1][0],
            #     triangle[1][1], triangle[1][2], triangle[2][0], triangle[2][1],
            #     triangle[2][2], image, z_buf, (int(-float(255) * float(cos)), 0, 0))

        else:
            continue
    # RabbitIn3D.jpg - красный неповернутый кролик
    # RabbitIn3D_move.jpg - повернутый
    # image.save("images/RabbitIn3D.jpg")
    image.save("images/RabbitIn3D_move.jpg")


size = 1000
image = Image.new('RGB', (size, size))
draw_polygons(image)
