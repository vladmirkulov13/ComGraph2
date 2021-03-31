from Parser import Parser
from PIL import Image, ImageDraw
from DrawingLines import lineByBresenhem

img = Image.new("RGB", (1000, 1000))
draw = ImageDraw.Draw(img)
parser = Parser()
parser.load_points("Test.obj", False)
point_list = []

for pair in parser.points:
    x = int(-10000 * pair[0] + 500)
    y = int(-10000 * pair[1] + 1000)
    point_list.append((x, y))
    draw.point((x, y))

img.save("images/RabbitByPoints.jpg")

parser.load_polygons("Test.obj")

for polygon in parser.polygons:
    lineByBresenhem(point_list[polygon[0] - 1], point_list[polygon[1] - 1], img)
    lineByBresenhem(point_list[polygon[1] - 1], point_list[polygon[2] - 1], img)
    lineByBresenhem(point_list[polygon[2] - 1], point_list[polygon[0] - 1], img)

img.save("images/RabbitByPoints&Polygons.jpg")