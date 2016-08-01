# Add your Python code here. E.g.
from microbit import *
import random

matrix = []
for rowidx in range(5):
    matrix.append([random.choice([-1, 1]) for i in range(5)])

for rowidx in range(5):
    for colidx in range(5):
        display.set_pixel(rowidx, colidx, random.randint(0, 9))
        
while True:
    for rowidx in range(5):
        for colidx in range(5):
            pixel = display.get_pixel(rowidx, colidx)
            new_pixel = pixel+matrix[rowidx][colidx]
            if new_pixel>9 or new_pixel<0:
                matrix[rowidx][colidx] = 0 - matrix[rowidx][colidx]
                new_pixel = pixel + matrix[rowidx][colidx]
                
            display.set_pixel(rowidx, colidx, new_pixel)
    sleep(50)
