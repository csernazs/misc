# Add your Python code here. E.g.
from microbit import *
from random import randint

display.show(Image.HAPPY)
while True:
    sleep_count = randint(200, 700)
    while sleep_count > 0:
        if accelerometer.was_gesture("shake"):
            display.show(Image.ANGRY)
            sleep(2000)
            display.show(Image.HAPPY)
            break
        
        sleep(10)
        sleep_count -= 1
        
    display.set_pixel(1, 1, 0)
    display.set_pixel(3, 1, 0)
    sleep(100)
    display.set_pixel(1, 1, 9)
    display.set_pixel(3, 1, 9)
