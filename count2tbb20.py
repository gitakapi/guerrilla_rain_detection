import sys
import numpy as np
import cv2

def main():
  if len(sys.argv) != 4:
    print("Usage: python3 grid2png-new.py <lookup table> <input> <output>")
    exit(1)
  mat = readGrid(sys.argv[2],6000,6000)
  writeImg(sys.argv[3],mat)


def readGrid(grid,NY,NX):
  fp = open(grid,"rb")
  mat = np.zeros((NY,NX),dtype=np.uint16)
  print("Loading image...")
  for i in range(NY):
    for j in range(NX):
      mat[i,j] = (int.from_bytes(fp.read(2),byteorder='big',signed=False))*32
  return mat

def writeImg(filename,img):
  print("Writing image...")
  cv2.imwrite(filename,img)

if __name__ == '__main__':
    main()
