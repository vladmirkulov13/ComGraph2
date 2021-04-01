from Parser import Parser
from PIL import Image, ImageDraw
from DrawingLines import lineByBresenhem

# создаем цветное изображение
img = Image.new("RGB", (1000, 1000))
draw = ImageDraw.Draw(img)
# создаем объект типа парсера
parser = Parser()
# считываем координаты вершин в поле parser.points
parser.load_points("Test.obj", False)
point_list = []
# проходим по массиву points и масштабируя координаты
# добавляем их в point_list
# добавляем на изображение
for pair in parser.points:
    x = int(-10000 * pair[0] + 500)
    y = int(-10000 * pair[1] + 1000)
    point_list.append((x, y))
    draw.point((x, y))

img.save("images/RabbitByPoints.jpg")
# считываем полигоны из файла
parser.load_polygons("Test.obj")
# проходим по массиву polygons
# рисуем линии по алг. Брезенхема
# соединяя точки, указанные в элементе массива polygons
for polygon in parser.polygons:
    lineByBresenhem(point_list[polygon[0] - 1], point_list[polygon[1] - 1], img)
    lineByBresenhem(point_list[polygon[1] - 1], point_list[polygon[2] - 1], img)
    lineByBresenhem(point_list[polygon[2] - 1], point_list[polygon[0] - 1], img)

img.save("images/RabbitByPoints&Polygons.jpg")