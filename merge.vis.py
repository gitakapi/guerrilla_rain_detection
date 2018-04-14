import sys
import numpy as np
import cv2

def main():
  if len(sys.argv) != 5:
    print("Usage: python merge.vis.py <vis.01.png> <vis.02.png> <vis.03.png> <output>")
    exit(1)
  mat = mergeImg(sys.argv[1],sys.argv[2],sys.argv[3],12000,12000)
  writeImg(sys.argv[4],mat)

def mergeImg(file1,file2,file3,NX,NY):
  new = np.zeros((NX,NY,3))
  print("Loading image 1...")
  img1 = cv2.imread(file1,0)
  print("Loading image 2...")
  img2 = cv2.imread(file2,0)
  print("Loading image 3...")
  img3 = cv2.imread(file3,0)
  print("Creating image...")
  for i in range(NX):
    if i % 100 == 0:
      print(i,"th row...")
    for j in range(NY):
      new[i,j] = [img1[i,j]*3,img2[i,j]*3,img3[i,j]]
  return new

def writeImg(filename,img):
  print("Writing image...")
  cv2.imwrite(filename,img)

if __name__ == '__main__':
    main()
