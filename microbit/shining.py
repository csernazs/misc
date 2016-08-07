# Add your Python code here. E.g.
from microbit import *
import random

random_range = [x/100.0 for x in range(20, 151)]

matrix = []
for rowidx in range(5):
    matrix.append([random.choice(random_range) for i in range(5)])

pixels = []
for rowidx in range(5):
    row = []
    pixels.append(row)
    for colidx in range(5):
        value = random.randint(0, 9)
        display.set_pixel(rowidx, colidx, value)
        row.append(value)

while True:
    for rowidx in range(5):
        for colidx in range(5):
            pixel = pixels[rowidx][colidx]
            new_pixel = pixel+matrix[rowidx][colidx]
            if new_pixel>9 or new_pixel<0:
                matrix[rowidx][colidx] = 0 - matrix[rowidx][colidx]
                new_pixel = pixel + matrix[rowidx][colidx]

            pixels[rowidx][colidx] = new_pixel
            display.set_pixel(rowidx, colidx, int(new_pixel))
    sleep(50)
    if button_a.is_():
        for rowidx in range(5):
            for colidx in range(5):
                pixels[rowidx][colidx] = 9
                matrix[rowidx][colidx] = random.choice(random_range)
                if matrix[rowidx][colidx]>0:
                    matrix[rowidx][colidx] = 0 - matrix[rowidx][colidx]
