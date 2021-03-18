import pyautogui as pag
import numpy as np
import matplotlib.pyplot as plt

while True:
    img = pag.screenshot()
    data = np.array(img)
    plt.imshow(data, interpolation='nearest')
    plt.show()
