import pyautogui as pag
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Rectangle

from colormath.color_objects import sRGBColor,LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

import cv2
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'Tesseract\tesseract.exe'


BAR_BOT_LEFT = (1765,880)
BAR_BOT_RIGHT = (1817,880)
BAR_TOP_LEFT = (1765,467)
BAR_TOP_RIGHT = (1817,467)

THRESHOLD = 3.5

BAR_LEFT_X=1770
BAR_RIGHT_X=1813

LOWER_BAR_RGB = sRGBColor(23/255.0, 168/255.0, 195/255.0)
LOWER_BAR_TOP_Y=842
LOWER_BAR_BOT_Y=835

HIGHER_BAR_RGB = (27/255.0, 171/255.0, 179/255.0)
HIGHER_BAR_TOP_Y=820
HIGHER_BAR_BOT_Y=828

DISTANCE_BOX=(1520, 925, 1630, 1001)


def start_up():
    pag.FAILSAFE = True

    print("Starting up")
    for i in range(3):
        print("#")
        time.sleep(1)
 
    print("Ready")


def main():
    start_up()
    
    while True:
        cast()
        bait()
        return_fish()

        pag.mouseUp()
        pag.mouseUp(button="right")
        time.sleep(3)

    #mouse_position(100)

    pag.mouseUp()
    pag.mouseUp(button="right")
    

def cast():
    pag.mouseDown()
    time.sleep(1.9)
    pag.mouseUp()
    time.sleep(5)
    print("done with cast")

def is_zero(data):
    bounds=(1540, 955, 1545, 979) #left top right bot
    offset_x= 31     # 1771 - 1740

    segment=data[bounds[1]:bounds[3], bounds[0]:bounds[2]]
    if (segment== (247, 247, 247)).all():
        return True
    else:
        return False

def return_fish():
    pag.mouseDown()
    pag.mouseDown(button="right")
    
    while True:
        img = pag.screenshot()
        data = np.array(img)
        if is_zero(data):
            print("reeled in something maybe")
            pag.mouseUp()
            pag.mouseUp(button="right")
            got_fish()
            break
        time.sleep(0.5)

def got_fish():
    bounds=(1048, 935, 1050, 938)
    time.sleep(4)

    img = pag.screenshot()
    data = np.array(img)
    segment=data[bounds[1]:bounds[3], bounds[0]:bounds[2]]

    if (segment == (220, 143, 73)).all():
        print("reeled in fish for real")
        pag.moveTo(1048,935)
        time.sleep(0.2)
        pag.leftClick()
        return True
    elif (segment == (61, 61, 61)).all():
        print("no space for this fish")
        pag.moveTo(800,935)
        time.sleep(0.2)
        pag.leftClick()
        return True
    else:
        print("reeled in jack shit mannen") 
        return False


def bait():
    since_pulling=time.time()-0.5
    is_pulling=True
    since_releasing=time.time()
    while True:
        if time.time() - since_pulling > 0.5 and is_pulling:
            pag.mouseUp()
            is_pulling=False
            since_releasing = time.time()
        elif time.time() - since_releasing > 0.3 and not is_pulling:
            pag.mouseDown()
            is_pulling=True
            since_pulling=time.time()
        else:
            img = pag.screenshot()
            data = np.array(img)

            if is_zero(data):
                pag.mouseUp()          
                return
            #start=time.time()
            #value=np.average(data[i,left_bound:right_bound])

            bar=data[LOWER_BAR_BOT_Y:LOWER_BAR_TOP_Y, BAR_LEFT_X:BAR_RIGHT_X]
            #print(bar)
            color_r = np.mean(data[LOWER_BAR_BOT_Y:LOWER_BAR_TOP_Y, BAR_LEFT_X:BAR_RIGHT_X,0])
            color_g = np.mean(data[LOWER_BAR_BOT_Y:LOWER_BAR_TOP_Y, BAR_LEFT_X:BAR_RIGHT_X,1])
            color_b = np.mean(data[LOWER_BAR_BOT_Y:LOWER_BAR_TOP_Y, BAR_LEFT_X:BAR_RIGHT_X,2])
            color=sRGBColor(color_r/255.0,color_g/255.0,color_b/255.0)
            #color=(color_r,color_g,color_b)
            #show_color(color)
            
            diff=difference(color,LOWER_BAR_RGB)

            
            if diff<THRESHOLD:
            
                print("got fish mayte#######################")
                time.sleep(0.7)
                strike()
                pag.mouseUp()
                return


def difference(color_a, color_b):
    color_a_lab = convert_color(color_a,LabColor)
    color_b_lab = convert_color(color_b,LabColor)
    return delta_e_cie2000(color_a_lab,color_b_lab)
       

def strike():
    pag.mouseDown(button="right")
    time.sleep(1)
    pag.mouseUp(button="right")



def show_color(color):

    value = [x/255.0 for x in color]

    someX, someY = 0.5, 0.5
    fig,ax = plt.subplots()
    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((someX - 0.1, someY - 0.1), 0.2, 0.2,alpha=1, facecolor=value))
    plt.show()


def reel_in():
    pag.mouseDown()
    time.sleep(0.5)
    pag.mouseUp()
    time.sleep(0.3)


def mouse_position(duration=10):
    for i in range(duration):
        print(pag.position())
        time.sleep(1)


if __name__ == "__main__":
    main()
