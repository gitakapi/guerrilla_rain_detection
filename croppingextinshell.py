import numpy as np
import cv2
import sys

img = cv2.imread(sys.argv[1], 0)

#    x = 9269
#    y = 4756
#    width = 720
#    height = 720
x = 
y = 
width = 160
height = 160

cropped = img[y:y+height, x:x+width]

cv2.imwrite(sys.argv[2], cropped)
