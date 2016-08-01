
from microbit import *

def fade(source, dest, step=1):
    dirty = False
    for x in range(5):
        for y in range(5):
            src_pixel = source.get_pixel(x, y)
            dst_pixel = dest.get_pixel(x, y)
            if src_pixel > dst_pixel:
                source.set_pixel(x, y, max(src_pixel-step, dst_pixel))
                dirty = True
            elif src_pixel < dst_pixel:
                source.set_pixel(x, y, min(src_pixel+step, dst_pixel))
                dirty = True
                
    return dirty

def fade_loop(source, dest, step=1, sleep_time=100):
    while fade(source, dest, step):
        sleep(sleep_time)

heart_big = Image.HEART.invert()
heart_big.set_pixel(0, 4, 0)
heart_big.set_pixel(4, 4, 0)

while True:
    fade_loop(display, Image.HEART_SMALL)
    fade_loop(display, Image.HEART-Image.HEART_SMALL)
    #fade_loop(display, heart_big)
