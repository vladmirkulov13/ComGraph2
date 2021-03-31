from PIL import Image
import numpy as np
# задание номер 1
h = 200
w = 200
# создание массива из изображения, чтобы в дальнейшем попиксельно проводить изменения
# черное одноканальное изображение
image = np.array(Image.new('L', (h, w)))
image = Image.fromarray(image)
image.save("images/Black.png")
image = np.array(Image.new('L', (h, w)))
# делаем белым
for i in range(h):
    for j in range(w):
        image[i][j] = 255
image = Image.fromarray(image)
image.save("images/White.png")
# цветное трехканальное изображение
image = np.array(Image.new('RGB', (h, w)))
# делаем красным
for i in range(h):
    for j in range(w):
        image[i][j][0] = 255
# делаем градиент
for i in range(h):
    for j in range(w):
        image[i][j][0] = (i + j) % 256
# достаем изображение из массива
image = Image.fromarray(image)
# сохраняем в файл image.png
# для просмотра изменений нужно добавить сохранение после нужного изменения
image.save("images/Gradient.png")
