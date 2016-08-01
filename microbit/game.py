
import random
from microbit import *

image_left = Image("99000:"
                   "99000:"
                   "99000:"
                   "99000:"
                   "99000")

image_right= Image("00099:"
                   "00099:"
                   "00099:"
                   "00099:"
                   "00099")

image_both = Image("99099:"
                   "99099:"
                   "99099:"
                   "99099:"
                   "99099")

def blink(image, sleep_time=100, iterations=5):
    for i in range(iterations):
        display.show(image)
        sleep(sleep_time)
        display.clear()
        sleep(sleep_time)
    

def buttons_pressed():
    return (button_a.was_pressed(), button_b.was_pressed())

score_a = 0
score_b = 0
while score_a < 5 and score_b < 5:
    display.scroll("%d:%d" % (score_a, score_b))
    sleep(500)
    buttons_pressed()
    display.show(Image.HEART)
    time_to_sleep = random.randint(1000, 4000)
    sleep(time_to_sleep)
    a_btn, b_btn = buttons_pressed()
    if a_btn or b_btn:
        blink(Image.ANGRY, 50, 10)
        sleep(500)
        if a_btn and b_btn:
            blink(image_both)
        elif a_btn:
            blink(image_left)
            score_b += 1
        elif b_btn:
            blink(image_right)
            score_a += 1 
        
        sleep(1000)
        continue
            
    display.show(Image.HAPPY)
    
    while True:
        a_btn, b_btn = buttons_pressed()

        if a_btn and b_btn:
            blink(image_both)
        elif a_btn:
            blink(image_left)
            score_a += 1
        elif b_btn:
            blink(image_right)
            score_b += 1
        
        if a_btn or b_btn:
            sleep(1000)
            break

        sleep(10)
        
if score_a>score_b:
    display.scroll("A", loop=True, delay=300)
else:
    display.scroll("B", loop=True, delay=300)
    
