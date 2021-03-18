import pyautogui as pag
import numpy as np
import matplotlib.pyplot as plt
import time

while True:
    img = pag.screenshot()
    data = np.array(img)
    plt.imshow(data, interpolation='nearest')
    plt.show()


def start_up():
    pag.FAILSAFE = True

    print("Starting up", end=" ")
    for i in range(10):
        print("#", end=" ")
        time.sleep(1)
 
    print("Ready")


def main():
    start_up()


def mouse_position(duration=10):
    for i in range(duration):
        print(pag.position())
        time.sleep(1)


if __name__ == "__main__":
    main()
