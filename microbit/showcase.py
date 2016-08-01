
from microbit import *
        
IMAGES = ("HEART",
"HEART_SMALL",
"HAPPY",
"SMILE",
"SAD",
"CONFUSED",
"ANGRY",
"ASLEEP",
"SURPRISED",
"SILLY",
"FABULOUS",
"MEH",
"YES",
"NO",
"TRIANGLE",
"TRIANGLE_LEFT",
"CHESSBOARD",
"DIAMOND",
"DIAMOND_SMALL",
"SQUARE",
"SQUARE_SMALL",
"RABBIT",
"COW",
"MUSIC_CROTCHET",
"MUSIC_QUAVER",
"MUSIC_QUAVERS",
"PITCHFORK",
"XMAS",
"PACMAN",
"TARGET",
"TSHIRT",
"ROLLERSKATE",
"DUCK",
"HOUSE",
"TORTOISE",
"BUTTERFLY",
"STICKFIGURE",
"GHOST",
"SWORD",
"GIRAFFE",
"SKULL",
"UMBRELLA",
"SNAKE")

img_idx = 0

def wait_for_button(btn_a=False, btn_b=False):
    while True:
        a_pressed = button_a.was_pressed()
        b_pressed = button_b.was_pressed()
        if (a_pressed == btn_a or btn_a is None) or (b_pressed == btn_b or btn_b is None):
            return (a_pressed, b_pressed)
        sleep(10)
        
        
while True:
    display.scroll(IMAGES[img_idx], delay=100)
    display.show(getattr(Image, IMAGES[img_idx]))
    btn_a, btn_b = wait_for_button(btn_a=True, btn_b=True)
    if btn_a:
        img_idx -= 1
    if btn_b:
        img_idx += 1
        
    if img_idx<0:
        img_idx = len(IMAGES)-1
    elif img_idx>=len(IMAGES)-1:
        img_idx = 0
         
    
    
    