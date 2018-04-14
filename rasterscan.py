import numpy as np
import cv2
import sys

img = cv2.imread(sys.argv[1], 1)
old_img = cv2.imread(sys.argv[2], 1)
finalname = sys.argv[1][0:12] + '.final.png'


distance = 30
width = 720
height = 720

# for x in range(width):
#     for y in range(height):
#         if img[x,y][1] == 255: # green
#             for i in range(max(0,x-distance),min(width,x+distance)):
#                 for j in range(max(0,y-distance),min(height,y+distance)):
#                     if img[i,j][2] == 255: # red
#                         print("Check.")
#                         img[x,y] = old_img[x,y]
for x in range(width):
    for y in range(height):
        if img[x,y,2] == 255: # green
            flag = False
            for i in range(max(0,x-distance),min(width,x+distance)):
                for j in range(max(0,y-distance),min(height,y+distance)):
                    if img[i,j,1] == 255: # red
                        flag = True
            if not flag:
                img[x,y] = old_img[x,y]

for x in range(width):
    for y in range(height):
        if img[x,y,1] == 255: # green
            flag = False
            for i in range(max(0,x-distance),min(width,x+distance)):
                for j in range(max(0,y-distance),min(height,y+distance)):
                    if img[i,j,2] == 255: # red
                        flag = True
            if not flag:
                print(x)
                img[x,y] = old_img[x,y]

cv2.imwrite(finalname, img)
