x3import sys
import numpy as np
import cv2
import datetime

#image size----------------------
width = 720
height = 720
distance = 30

#import image---------------------------------------
for x in range(23):
    date1 = datetime.datetime(int(sys.argv[1][0:4]),int(sys.argv[1][4:6]),int(sys.argv[1][6:8]),int(sys.argv[1][8:10]),int(sys.argv[1][10:12])) + datetime.timedelta(minutes=10 * x)
    print(date1)
    date1format = format("%04d%02d%02d%02d%02d" % (date1.year, date1.month, date1.day, date1.hour, date1.minute))
    date1extname = date1format + '.ext.01.cropped.tyugokusikoku.png'
    img1 = cv2.imread(date1extname, 0)

    date2 = date1 + datetime.timedelta(minutes=10)
    date2format = format("%04d%02d%02d%02d%02d" % (date2.year, date2.month, date2.day, date2.hour, date2.minute))
    date2extname = date2format + '.ext.01.cropped.tyugokusikoku.png'

    img2 = cv2.imread(date2extname, 0)
    img3 = cv2.imread(date2extname, 1)
    #img6 = cv2.imread(date1extname, 1)
    date2sirname = date2format + '.sir.01.cropped.tyugokusikoku.png'

    img4 = cv2.imread(date2sirname, 0)

#SIR-------------------------------------------------------------------------------------
    resized = cv2.resize(img2, (180, 180), interpolation = cv2.INTER_AREA)

    cv2.imwrite('resized.png', resized)
    resized = cv2.imread('resized.png', 0)
    resized = np.array(resized).astype(float)
    img4 = np.array(img4).astype(float)

    #defference
    icecloud = resized - img4
    for j in range(180) :
        for k in range(180) :
            if icecloud[j,k] < 0 :
                icecloud[j,k] = 0
    cv2.imwrite('ice.png', icecloud)

    #threshold
    icecloud = cv2.imread('ice.png', 0)
    threshold = cv2.threshold(icecloud, 100, 255,cv2.THRESH_BINARY)[1]
    cv2.imwrite('thresholdsir.png', threshold)
    threshold = cv2.imread('thresholdsir.png', 1)
    #closing = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, (7, 7), 3)
    #kakudai
    kakudai = cv2.resize(threshold, (720,720), interpolation = cv2.INTER_NEAREST)
    #red
    for i in range(width):
        for j in range(height):
            if kakudai[i,j].any() != 0 :
                img3[i,j,0] = 0
                img3[i,j,1] = 0
                img3[i,j,2] = 255

#EXT---------------------------------------------------------------------------------
    #optical flow
    flow = cv2.calcOpticalFlowFarneback(img1, img2, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    #nearest
    nearest = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            newi = int((i + flow[i,j,0]) + 0.5)
            newj = int((j + flow[i,j,1]) + 0.5)
            if newi in range(width) and newj in range(height):
                nearest[newi,newj] = img2[i,j]
    cv2.imwrite('nearest.png', nearest)

    #gaussian blur
    gaussianblur = cv2.GaussianBlur(nearest, (5, 5), 3)
    cv2.imwrite('gaussianblur.png', gaussianblur)
    gaussianblur = cv2.imread('gaussianblur.png', 0)

    #difference
    img1 = np.array(img1).astype(float)
    gaussianblur = np.array(gaussianblur).astype(float)
    difference = gaussianblur - img1
    for i in range(width) :
        for j in range(height) :
            if difference[i,j] < 0 :
                difference[i,j] = 0
    cv2.imwrite('difference.png', difference)

    #threshold
    difference = cv2.imread('difference.png', 0)
    threshold = cv2.threshold(difference, 90, 255,cv2.THRESH_BINARY)[1]
    cv2.imwrite('thresholdext.png', threshold)
    #opening
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, (7, 7), 3)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, (7, 7), 3)
    cv2.imwrite('closing.png', closing)

    #green
    img5 = cv2.imread('closing.png', 1)
    for i in range(width):
        for j in range(height):
            if img5[i,j].any() != 0 :
                img3[i,j,0] = 0
                img3[i,j,1] = 255
                img3[i,j,2] = 0
    finalname = date2format + '.tyugokusikoku.png'
    cv2.imwrite(finalname, img3)

#create result image-----------------------------------------------------------

    result = cv2.imread(img3, 1)
    old_img = cv2.imread(img2, 1)
    finalname = date2format + '.final.png'

    for x in range(width):
        for y in range(height):
            if img[x,y,2] == 255: # green
                flag = False
                for i in range(max(0,x-distance),min(width,x+distance)):
                    for j in range(max(0,y-distance),min(height,y+distance)):
                        if new_result[i,j,1] == 255: # red
                            flag = True
                            if not flag:
                                new_result[x,y] = old_img[x,y]

                                for x in range(width):
                                    for y in range(height):
                                        if new_result[x,y,1] == 255: # green
                                            flag = False
                                            for i in range(max(0,x-distance),min(width,x+distance)):
                                                for j in range(max(0,y-distance),min(height,y+distance)):
                                                    if new_result[i,j,2] == 255: # red
                                                        flag = True
                                                        if not flag:
                                                            print(x)
                                                            new_result[x,y] = old_img[x,y]

                                                            cv2.imwrite(finalname, result)
