
from microbit import *
import random

value = 9
x = 0
y = 0

while True:
    if button_a.was_pressed() and value>0:
        value -= 1
    if button_b.was_pressed() and value<9:
        value += 1
    
        
    display.set_pixel(x, y, 0)
    x = random.randint(0, 4)
    y = random.randint(0, 4)
    display.set_pixel(x, y, value)
    sleep(20)
