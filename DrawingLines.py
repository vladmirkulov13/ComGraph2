import math

import numpy as np
from PIL import Image, ImageDraw


# задание номер 3
# алгоритмы отрисовки прямых из лекций:
# первый алгоритм:
def line1(x0, y0, x1, y1, img, color):
    t = .0
    while t < 1.0:
        x = x0 * (1. - t) + x1 * t
        y = y0 * (1. - t) + y1 * t
        img.putpixel((int(x), int(y)), color)
        t += 0.01


# второй (не работает если надо провести прямую из центра влево,
# т.к. х0>x1) y рассчитывается исходя из х :
def line2(x0, y0, x1, y1, img, color):
    x = x0
    t = 0
    while x <= x1:
        if x1 - x0!=0:
            t = (x - x0) / (float)(x1 - x0)
        y = y0 * (1. - t) + y1 * t
        x += 1
        img.putpixel((int(x), int(y)), color)


# третий (с учетом замены если х0>x1):
def line3(x0, y0, x1, y1, img, color):
    steep = False
    if math.fabs(x0 - x1) < math.fabs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    x = x0
    t = 0
    while x <= x1:
        if x1 - x0!=0:
            t = (x - x0) / (float)(x1 - x0)
        y = y0 * (1. - t) + y1 * t
        if steep:
            img.putpixel((int(x), int(y)), color)
        else:
            img.putpixel((int(y), int(x)), color)
        x += 1


# алгоритм Брезенхема:
def lineByBresenhem(start, finish, img):
    draw = ImageDraw.Draw(img)
    steep = False
    if abs(start[0] - finish[0]) < abs(start[1] - finish[1]):
        start = (start[1], start[0])
        finish = (finish[1], finish[0])
        steep = True
    if start[0] > finish[0]:
        start, finish = finish, start
    dx = -start[0] + finish[0]
    dy = -start[1] + finish[1]
    if dx==0:
        derror = 0
    else:
        derror = abs(dy / dx)
    error = 0
    y = start[1]
    for x in range(start[0], finish[0]):
        if steep:
            draw.point((y, x))
        else:
            draw.point((x, y))
        error += derror
        if error > 0.5:
            if start[1] > finish[1]:
                y += -1
            else:
                y += 1
            error -= 1


# создаем 4 изображения для отрисовки на них линий

img1 = Image.new("L", (200, 200))
img2 = Image.new("L", (200, 200))
img3 = Image.new("L", (200, 200))
img4 = Image.new("RGB", (200, 200))

# отрисовка линий согласно алгоритму из методички
for i in range(13):
    line1(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                    100 + int(math.sin(i * 2 * math.pi / 13) * 95), img1, 255)
    line2(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                    100 + int(math.sin(i * 2 * math.pi / 13) * 95), img2, 255)
    line3(100, 100, 100 + int(math.cos(i * 2 * math.pi / 13) * 95),
                    100 + int(math.sin(i * 2 * math.pi / 13) * 95), img3, 255)
    lineByBresenhem((100, 100),
        (int(100 + 95 * np.sin(2 * np.pi * i / 13)), int(100 + 95 * np.cos(2 * np.pi * i / 13))),
        img4)

img1.save("images/Star1.jpg")
img2.save("images/Star2.jpg")
img3.save("images/Star3.jpg")
img4.save("images/StarByBresenhem.jpg")
