from __future__ import print_function
import numpy as np
import math
import cv2
#!/usr/bin/env python

#'''
#example to show optical flow

#USAGE: opt_flow.py [<video_source>]

#Keys:
# 1 - toggle HSV flow visualization
# 2 - toggle glitch

#Keys:
#    ESC    - exit
#'''

width = 720
height = 720

#import
def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr


def warp_flow(img, flow):
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)
    return res

if __name__ == '__main__':
    import sys
    print(__doc__)
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 0

    #cam = video.create_capture(fn)
    img1 = cv2.imread('201608030420.ext.01.cropped.png', 0)
    #print (type(img1))
    #cv2.imshow('window', img1)
    #cv2.waitKey()
    #prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    #show_hsv = True
    #show_glitch = True
    #cur_glitch = img1.copy()

    #while True:
    img2  = cv2.imread('201608030430ext.01.cropped.png', 0)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(img1, img2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    #img1 = img2

    #cv2.imshow('flow', draw_flow(img2, flow))
    #if show_hsv:
    #    cv2.imshow('flow HSV', draw_hsv(flow))
    #if show_glitch:
    #    cur_glitch = warp_flow(cur_glitch, flow)
    #cv2.imshow('glitch', cur_glitch)

    #ch = 0xFF & cv2.waitKey()
    # ch == 27:
        #break
    #if ch == ord('1'):
    #    show_hsv = not show_hsv
    #    print('HSV flow visualization is', ['off', 'on'][show_hsv])
    #if ch == ord('2'):
    #    show_glitch = not show_glitch
    #if show_glitch:
    #    cur_glitch = img1.copy()
    #    print('glitch is', ['off', 'on'][show_glitch])
    #    cv2.destroyAllWindows()

nearest = np.zeros((width+2,height+2))
for i in range(width):
    for j in range(height):
        newi = int((i - flow[i,j,0]) + 0.5) + 2
        newj = int((j - flow[i,j,1]) + 0.5) + 2
        if newi in range(width) and newj in range(height):
            nearest[newi,newj] = img2[i,j]
cv2.imwrite('nearest.png',nearest)

#create newimage
#x = 5
#y = 5
#input image
def main():
#average
#variance
    sigma1 = 0.9
    sigma2 = 0.9
#corrcoef
    rho = 0.9

    img = np.zeros((724,724))
    for x in range(2,720):
        for y in range(2,720):
            gauss = np.array(gaussarray(5, 5, 2, 2, sigma1, sigma2, rho))
            #print(gauss)
            #print(nearest[x-2:x+3,y-2:y+3])
            newgrid = gauss * nearest[x-2:x+3,y-2:y+3]
            img[x-2,y-2] += newgrid[0,0]
            img[x-1,y-2] += newgrid[1,0]
            img[x,y-2] += newgrid[2,0]
            img[x+1,y-2] += newgrid[3,0]
            img[x+2,y-2] += newgrid[4,0]
            img[x-2,y-2] += newgrid[0,1]
            img[x-1,y-2] += newgrid[1,1]
            img[x,y-2] += newgrid[2,1]
            img[x+1,y-2] += newgrid[3,1]
            img[x+2,y-2] += newgrid[4,1]
            img[x-2,y-2] += newgrid[0,2]
            img[x-1,y-2] += newgrid[1,2]
            img[x,y-2] += newgrid[2,2]
            img[x+1,y-2] += newgrid[3,2]
            img[x+2,y-2] += newgrid[4,2]
            img[x-2,y-2] += newgrid[0,3]
            img[x-1,y-2] += newgrid[1,3]
            img[x,y-2] += newgrid[2,3]
            img[x+1,y-2] += newgrid[3,3]
            img[x+2,y-2] += newgrid[4,3]
            img[x-2,y-2] += newgrid[0,4]
            img[x-1,y-2] += newgrid[1,4]
            img[x,y-2] += newgrid[2,4]
            img[x+1,y-2] += newgrid[3,4]
            img[x+2,y-2] += newgrid[4,4]
            #print(img[1:30,1:30])
    cv2.imwrite('newimage.png',img)
#define gauss fanction
def norm(mu, sigma):
    return lambda x: math.exp((-(x-mu)**2)/(2*sigma**2)) / (math.sqrt(2*math.pi)*(sigma**2))

def gaussarray(x, y, mu1, mu2, sigma1, sigma2, rho):
    return [[norm(mu1,sigma1)(i) * norm(mu2+rho*sigma2*((i-mu1)/sigma1),(1-rho**2)*sigma2**2)(j) for j in range(x)] for i in range(y)]

if __name__ == '__main__':
    main()


