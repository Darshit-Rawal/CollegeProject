import cv2
import numpy as np


def area_find(path):
    ## Read
    img = cv2.imread(path)

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]


    #percentage diff.

    res = mask.astype(np.uint8)
    percentage = (np.count_nonzero(res) * 100)/ res.size
    print(percentage)
    return percentage